"use strict";
/*
 * Console de régie de Didier -- logique front, vanilla JS (pas de framework,
 * pas de build). Le contrat protocole est celui de robot_web/web_protocol.py
 * côté serveur ; les constantes numériques ci-dessous sont DUPLIQUÉES
 * volontairement (pas de partage possible entre Python serveur et JS
 * navigateur) -- même choix assumé que robot_drive/wheels_payload.py.
 *
 * SÉCURITÉ pilotage : aucun message "drive" n'est émis si l'on n'a pas
 * l'écriture (isWriter) OU si le serveur ne l'autorise pas (driveEnabled,
 * WEB_DRIVE=true). Le plafond de vitesse reste appliqué SERVEUR ; le facteur
 * "vitesse %" de l'UI ne fait que réduire davantage, jamais dépasser.
 */

// Cadence du heartbeat applicatif (alignée sur web_protocol.HEARTBEAT_PERIOD_S).
const HEARTBEAT_PERIOD_S = 1.0;

// Backoff de reconnexion WebSocket : 1 s -> 5 s, doublé à chaque échec.
const RECONNECT_MIN_MS = 1000;
const RECONNECT_MAX_MS = 5000;

// Moyenne glissante du RTT sur les 5 derniers battements.
const RTT_WINDOW = 5;

// Émission des consignes de pilotage : ~15 Hz (66 ms) tant que le pad ou la
// manette sont actifs. Aligné sur la cadence gamepad -> WebSocket du plan
// (etude-interface-web.md §5 : "gamepad -> WebSocket ~20 Hz").
const DRIVE_PERIOD_MS = 66;

// Zone morte du stick gauche de la manette (bruit du repos).
const GAMEPAD_DEADZONE = 0.15;

// --- État global du client --------------------------------------------------

const state = {
  ws: null,
  authSent: false,          // un seul message "auth" envoyé par connexion
  isWriter: false,
  tokenRequired: false,
  driveEnabled: false,      // hello.drive_enabled (WEB_DRIVE=true côté serveur)
  maxLinear: 0,             // plafond serveur affiché (m/s)
  maxAngular: 0,            // plafond serveur affiché (rad/s)
  reconnectDelayMs: RECONNECT_MIN_MS,
  rttSamples: [],           // fenêtre glissante (ms)
  hbTimer: null,
  catalog: null,
  attenteAck: {},           // topic -> bouton cliqué, flashé à l'ack (pas au clic)
  dernierBouton: null,      // dernier bouton cliqué, flashé rouge sur "err"
};

// État du flux de pilotage (pad + manette). Une seule boucle 15 Hz lit la
// source active et émet ; à l'inactivité, elle envoie UN zéro puis se tait.
const drive = {
  padActive: false,         // pointeur enfoncé dans le pad
  padX: 0, padZ: 0,         // consigne normalisée [-1,1] issue du pad
  gamepadIndex: null,       // index de la manette connectée, ou null
  lastSentZero: true,       // dernier envoi était-il un zéro ? (anti-spam côté UI)
};

// --- Utilitaires DOM ---------------------------------------------------------

function $(id) {
  return document.getElementById(id);
}

function clamp(v, lo, hi) {
  return v < lo ? lo : v > hi ? hi : v;
}

function logErreur(message) {
  const ul = $("journal-erreurs");
  const li = document.createElement("li");
  li.textContent = new Date().toLocaleTimeString() + " -- " + message;
  ul.prepend(li);
  while (ul.children.length > 5) {
    ul.lastChild.remove();
  }
}

function flash(element, ok) {
  const classe = ok ? "flash-ok" : "flash-err";
  element.classList.add(classe);
  setTimeout(() => element.classList.remove(classe), 400);
}

// --- Connexion WebSocket + reconnexion auto ---------------------------------

function urlWebSocket() {
  const protocole = location.protocol === "https:" ? "wss://" : "ws://";
  return protocole + location.host + "/ws";
}

function connecter() {
  const ws = new WebSocket(urlWebSocket());
  state.ws = ws;
  state.authSent = false;

  ws.addEventListener("open", () => {
    state.reconnectDelayMs = RECONNECT_MIN_MS; // succès : on repart à 1 s
    majBadgeConnexion(true);
  });

  ws.addEventListener("message", (event) => {
    let msg;
    try {
      msg = JSON.parse(event.data);
    } catch (e) {
      logErreur("message serveur illisible : " + e);
      return;
    }
    traiterMessageServeur(msg);
  });

  ws.addEventListener("close", () => {
    majBadgeConnexion(false);
    arreterHeartbeat();
    planifierReconnexion();
  });

  ws.addEventListener("error", () => {
    // "close" suit toujours "error" sur un WebSocket -- la reconnexion est
    // gérée là-bas, pas besoin de la dupliquer ici.
    logErreur("erreur WebSocket");
  });
}

function planifierReconnexion() {
  setTimeout(connecter, state.reconnectDelayMs);
  state.reconnectDelayMs = Math.min(state.reconnectDelayMs * 2, RECONNECT_MAX_MS);
}

function majBadgeConnexion(connecte) {
  const badge = $("badge-connexion");
  badge.textContent = connecte ? "connecté" : "déconnecté";
  badge.className = "badge " + (connecte ? "badge-on" : "badge-off");
  if (!connecte) {
    state.isWriter = false;
    majBadgeEcriture();
  }
}

// --- Traitement des messages serveur -----------------------------------------

function traiterMessageServeur(msg) {
  switch (msg.type) {
    case "hello":
      traiterHello(msg);
      break;
    case "hb_ack":
      traiterHbAck(msg);
      break;
    case "ack":
      // Le flash arrive à l'ACK serveur, pas au clic : un bouton qui flashe
      // vert = la commande est vraiment partie sur le topic ROS.
      flash(state.attenteAck[msg.topic] || $("badge-ecriture"), true);
      delete state.attenteAck[msg.topic];
      break;
    case "err":
      logErreur(msg.reason);
      flash(state.dernierBouton || $("badge-ecriture"), false);
      break;
    case "state":
      afficherEtat(msg);
      break;
    default:
      logErreur("type de message serveur inconnu : " + msg.type);
  }
}

function traiterHello(msg) {
  majBadgeMode(msg.mode, msg.domain_id);
  state.tokenRequired = msg.token_required;
  state.isWriter = msg.writer;
  // Plafonds + autorisation pilotage : l'UI verrouille/déverrouille le pad et
  // affiche les limites (le plafond DUR reste appliqué serveur).
  state.driveEnabled = !!msg.drive_enabled;
  state.maxLinear = msg.max_linear ?? 0;
  state.maxAngular = msg.max_angular ?? 0;
  majBadgeEcriture();
  majPilotageUI();
  demarrerHeartbeatSiWriter();

  if (!state.authSent) {
    state.authSent = true;
    $("token-box").hidden = !msg.token_required;
    if (!msg.token_required) {
      envoyerAuth(null);
    }
    // Si un token est requis, on attend que l'opérateur le saisisse
    // (bouton #btn-token) -- pas d'auto-tentative avec un token vide.
  }
}

function envoyerAuth(token) {
  envoyer({ type: "auth", token: token });
}

function traiterHbAck(msg) {
  const rtt = Date.now() - msg.t;
  state.rttSamples.push(rtt);
  if (state.rttSamples.length > RTT_WINDOW) {
    state.rttSamples.shift();
  }
  const moyenne = state.rttSamples.reduce((a, b) => a + b, 0) / state.rttSamples.length;
  $("rtt").textContent = "RTT " + Math.round(moyenne) + " ms";
}

const CLASSE_BADGE_PAR_MODE = {
  "SIMULATION": "badge-simulation",
  "ROBOT RÉEL": "badge-robot-reel",
};

function majBadgeMode(mode, domainId) {
  const badge = $("badge-mode");
  badge.textContent = mode + " (domain " + domainId + ")";
  // En sim, prévenir que les sons sont muets (pas d'audio_node dans le
  // conteneur) : sans ça, un clic "Sons" semble juste ne rien faire.
  $("note-sim").hidden = (mode !== "SIMULATION");
  // Parenthèse indispensable : "+" est plus prioritaire que "||" en JS, sans
  // elle "badge " + undefined donne "badge undefined" (chaîne TRUTHY) et le
  // fallback badge-inconnu ne se déclenche jamais.
  badge.className = "badge " + (CLASSE_BADGE_PAR_MODE[mode] || "badge-inconnu");
}

function majBadgeEcriture() {
  const badge = $("badge-ecriture");
  badge.textContent = state.isWriter ? "écriture" : "lecture seule";
  badge.className = "badge " + (state.isWriter ? "badge-on" : "badge-off");
  // Les boutons d'action (catalogue + panneau technique) sont inertes en
  // lecture seule -- l'UI le reflète (le serveur refuse déjà côté écriture).
  document.querySelectorAll(".bouton-catalogue, .servo-ligne button, #btn-stop-contenus, "
      + "#btn-system-restart, #btn-system-shutdown")
    .forEach((btn) => { btn.disabled = !state.isWriter; });
  majPilotageUI();
}

// --- Heartbeat + RTT (tant que la page a l'écriture, spec §5) ---------------

function demarrerHeartbeatSiWriter() {
  arreterHeartbeat();
  if (!state.isWriter) {
    return;
  }
  state.hbTimer = setInterval(() => {
    envoyer({ type: "hb", t: Date.now() });
  }, HEARTBEAT_PERIOD_S * 1000);
}

function arreterHeartbeat() {
  if (state.hbTimer !== null) {
    clearInterval(state.hbTimer);
    state.hbTimer = null;
  }
}

// --- Envoi de commandes -------------------------------------------------------

function envoyer(objet) {
  if (state.ws?.readyState === WebSocket.OPEN) {
    state.ws.send(JSON.stringify(objet));
  }
}

function envoyerCmd(topic, value, timeMs) {
  envoyer({ type: "cmd", topic: topic, value: value, time: timeMs || 0 });
}

// --- Bandeau : prise de main --------------------------------------------------

$("btn-prendre-main").addEventListener("click", () => {
  if (!confirm("Prendre la main écriture ? Un autre opérateur éventuellement "
      + "connecté repassera en lecture seule.")) {
    return;
  }
  envoyer({ type: "take_control" });
  // La confirmation de prise de main arrive via le prochain "hello".
});

$("btn-token").addEventListener("click", () => {
  envoyerAuth($("token-input").value);
});

// --- Onglets (colonne CONTENUS) -----------------------------------------------

document.querySelectorAll(".onglet-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".onglet-btn").forEach((b) => b.classList.remove("actif"));
    document.querySelectorAll(".onglet").forEach((s) => s.classList.remove("actif"));
    btn.classList.add("actif");
    $("onglet-" + btn.dataset.onglet).classList.add("actif");
  });
});

// --- STOP -----------------------------------------------------------------------

$("btn-stop-contenus").addEventListener("click", () => {
  // STOP contenus ET mouvement : le serveur coupe aussi cmd_vel_web (Twist nul).
  envoyer({ type: "stop_all" });
  arreterPilotage(true);
});

// --- Système (double confirmation, spec §5) ---------------------------------

function confirmerDouble(message) {
  return confirm(message) && confirm("Confirmer une seconde fois : " + message);
}

$("btn-system-restart").addEventListener("click", () => {
  if (confirmerDouble("Redémarrer le robot ?")) {
    envoyerCmd("system", "restart");
  }
});

$("btn-system-shutdown").addEventListener("click", () => {
  if (confirmerDouble("Éteindre le robot ?")) {
    envoyerCmd("system", "shutdown");
  }
});

// --- Boutons catalogue + gaze : écouteur délégué (data-topic/data-value) -----

document.addEventListener("click", (event) => {
  const btn = event.target.closest(".bouton-catalogue");
  if (btn) {
    envoyerCmd(btn.dataset.topic, btn.dataset.value);
    // Pas de flash ici : il vient de l'ack serveur (sinon un clic "réussi"
    // visuellement peut n'avoir rien publié du tout).
    state.attenteAck[btn.dataset.topic] = btn;
    state.dernierBouton = btn;
  }
});

// ============================================================================
//  PILOTAGE ROUES (SIM-ONLY) : pad tactile/souris + manette -> message "drive"
// ============================================================================

function peutPiloter() {
  return state.isWriter && state.driveEnabled;
}

function facteurVitesse() {
  // Réduit la consigne côté UI (10-100 %). N'augmente JAMAIS au-delà de 1 :
  // le plafond dur reste serveur.
  return clamp(Number($("vitesse").value) / 100, 0.1, 1.0);
}

function majPilotageUI() {
  const pad = $("pad");
  const ok = peutPiloter();
  pad.classList.toggle("disabled", !ok);

  let txt;
  if (!state.driveEnabled) {
    txt = "Pilotage désactivé (WEB_DRIVE=false)";
  } else if (!state.isWriter) {
    txt = "Prends la main pour piloter";
  } else {
    txt = "Prêt — glisse dans le pad";
  }
  $("pilotage-etat").textContent = txt;
  $("pilotage-limites").textContent = state.driveEnabled
    ? "plafond " + state.maxLinear + " m/s · " + state.maxAngular + " rad/s"
    : "plafond -- · --";

  if (!ok) {
    // Perte d'autorisation en cours de mouvement : on stoppe et on rentre le
    // curseur du pad (pas de zéro réseau si on ne peut de toute façon rien
    // émettre -- mais on nettoie l'état local).
    drive.padActive = false;
    majCurseurPad(0, 0);
    drive.lastSentZero = true;
  }
}

// Consigne active courante : pad si un pointeur est enfoncé, sinon manette si
// hors zone morte, sinon null (repos).
function consignePilotage() {
  if (drive.padActive) {
    return { x: drive.padX, z: drive.padZ };
  }
  return lireManette();
}

function lireManette() {
  if (drive.gamepadIndex === null || !navigator.getGamepads) {
    return null;
  }
  const gp = navigator.getGamepads()[drive.gamepadIndex];
  if (!gp) {
    return null;
  }
  const ax = gp.axes[0] || 0;   // stick gauche X : droite positif
  const ay = gp.axes[1] || 0;   // stick gauche Y : bas positif
  if (Math.hypot(ax, ay) < GAMEPAD_DEADZONE) {
    return null;                // repos : pas de consigne
  }
  // Haut = avant (x = -ay) ; gauche = rotation à gauche (z = -ax).
  return { x: clamp(-ay, -1, 1), z: clamp(-ax, -1, 1) };
}

// Boucle unique 15 Hz : lit la source active et émet. À l'inactivité, envoie
// UN zéro puis se tait (motif anti-spam de DriveFlow côté serveur).
function bouclePilotage() {
  if (!peutPiloter()) {
    return;
  }
  const src = consignePilotage();
  if (src === null) {
    arreterPilotage(false);
    return;
  }
  const f = facteurVitesse();
  const x = clamp(src.x * f, -1, 1);
  const z = clamp(src.z * f, -1, 1);
  envoyer({ type: "drive", x: x, z: z });
  drive.lastSentZero = false;
  majDriveReadout(x, z);
}

// Arrêt du flux : envoie un zéro une seule fois (sauf si déjà au repos). Le
// paramètre `force` (STOP) émet le zéro même si l'UI se croyait au repos.
function arreterPilotage(force) {
  if (drive.lastSentZero && !force) {
    return;
  }
  if (peutPiloter() || force) {
    envoyer({ type: "drive", x: 0, z: 0 });
  }
  drive.lastSentZero = true;
  majDriveReadout(0, 0);
}

function majDriveReadout(x, z) {
  const lin = (x * state.maxLinear).toFixed(2);
  const ang = (z * state.maxAngular).toFixed(2);
  $("drive-readout").textContent = "lin " + lin + " m/s · ang " + ang + " rad/s";
}

// --- Pad : pointeur (tactile + souris unifiés via Pointer Events) ------------

function majCurseurPad(nx, nz) {
  // nx = avant (+ = haut), nz = gauche (+ = gauche). Position en % du pad :
  // centre 50%/50% au repos, course max ±40 % pour rester dans le cadre. Le
  // curseur est centré sur ce point par transform: translate(-50%,-50%) (CSS).
  const curseur = $("pad-curseur");
  curseur.style.left = (50 - nz * 40) + "%";
  curseur.style.top = (50 - nx * 40) + "%";
}

function padVersConsigne(event) {
  const pad = $("pad");
  const r = pad.getBoundingClientRect();
  // Position du pointeur dans le pad, ramenée en [-1,1] sur chaque axe.
  const nx = clamp((event.clientX - r.left) / r.width * 2 - 1, -1, 1);   // droite positif
  const ny = clamp((event.clientY - r.top) / r.height * 2 - 1, -1, 1);   // bas positif
  drive.padX = -ny;   // haut = avant
  drive.padZ = -nx;   // gauche = rotation à gauche
  majCurseurPad(drive.padX, drive.padZ);
}

function installerPad() {
  const pad = $("pad");

  pad.addEventListener("pointerdown", (event) => {
    if (!peutPiloter()) {
      return;
    }
    drive.padActive = true;
    pad.setPointerCapture(event.pointerId);
    padVersConsigne(event);
    event.preventDefault();
  });

  pad.addEventListener("pointermove", (event) => {
    if (drive.padActive) {
      padVersConsigne(event);
    }
  });

  const relacher = () => {
    if (!drive.padActive) {
      return;
    }
    drive.padActive = false;
    majCurseurPad(0, 0);
    arreterPilotage(false);   // zéro immédiat au relâchement
  };
  pad.addEventListener("pointerup", relacher);
  pad.addEventListener("pointercancel", relacher);
  pad.addEventListener("lostpointercapture", relacher);
}

// --- Manette (Gamepad API) ----------------------------------------------------

window.addEventListener("gamepadconnected", (event) => {
  drive.gamepadIndex = event.gamepad.index;
  $("gamepad-indic").hidden = false;
});

window.addEventListener("gamepaddisconnected", (event) => {
  if (drive.gamepadIndex === event.gamepad.index) {
    drive.gamepadIndex = null;
    $("gamepad-indic").hidden = true;
    arreterPilotage(false);
  }
});

// --- Vitesse : libellé synchronisé -------------------------------------------

$("vitesse").addEventListener("input", () => {
  $("vitesse-val").textContent = $("vitesse").value + " %";
});

// --- Vidéo (flux MJPEG /video) -----------------------------------------------

// Ré-essai automatique quand le flux est en erreur : sans lui, une page
// ouverte AVANT que la caméra publie (ou pendant un redémarrage de la sim)
// restait sur « pas de vidéo » jusqu'à un clic manuel sur ⟳ -- vécu, pas clair.
const VIDEO_RETRY_MS = 5000;
let videoRetryTimer = null;

function chargerVideo() {
  // Cache-buster : force une nouvelle requête (le flux précédent peut être en
  // 503 depuis, ou figé). Le serveur répond 503 si aucune frame -> onerror.
  $("video").src = "/video?ts=" + Date.now();
}

function installerVideo() {
  const img = $("video");
  const placeholder = $("video-placeholder");
  img.addEventListener("load", () => {
    placeholder.hidden = true;
    if (videoRetryTimer !== null) {
      clearInterval(videoRetryTimer);
      videoRetryTimer = null;
    }
  });
  img.addEventListener("error", () => {
    placeholder.hidden = false;
    if (videoRetryTimer === null) {
      videoRetryTimer = setInterval(chargerVideo, VIDEO_RETRY_MS);
    }
  });
  $("btn-video-refresh").addEventListener("click", chargerVideo);
  chargerVideo();
}

// --- Recherche : filtre en direct la colonne CONTENUS ------------------------

$("recherche").addEventListener("input", () => {
  const q = $("recherche").value.trim().toLowerCase();
  document.querySelectorAll(".colonne-contenus .groupe").forEach((groupe) => {
    let visibles = 0;
    groupe.querySelectorAll(".bouton-catalogue, .servo-ligne").forEach((el) => {
      const match = q === "" || el.textContent.toLowerCase().includes(q);
      el.classList.toggle("filtre-cache", !match);
      if (match) {
        visibles += 1;
      }
    });
    // Masque toute la section si rien n'y correspond (seulement en recherche).
    groupe.classList.toggle("filtre-cache", q !== "" && visibles === 0);
  });
});

// --- Catalogue (GET /api/catalog) : grilles spectacle + technique ------------

function creerBoutonCatalogue(topic, value, libelle) {
  const btn = document.createElement("button");
  btn.className = "bouton-catalogue";
  btn.type = "button";
  btn.dataset.topic = topic;
  btn.dataset.value = value;
  btn.textContent = libelle;
  return btn;
}

function remplirGrille(id, topic, entrees) {
  const grille = $(id);
  grille.innerHTML = "";
  entrees.forEach((entree) => {
    // "audios" porte {label, value} ; les autres catalogues sont de simples
    // listes de noms (le nom sert de libellé ET de valeur publiée).
    const libelle = typeof entree === "string" ? entree : entree.label;
    const valeur = typeof entree === "string" ? entree : entree.value;
    grille.appendChild(creerBoutonCatalogue(topic, valeur, libelle));
  });
}

// Servos du panneau technique : mêmes 5 topics que le contrat StringTime,
// chacun avec un champ 0-99 + Envoyer/Stop.
const SERVOS = [
  ["neck", "Cou"],
  ["left_eye", "Œil gauche"],
  ["right_eye", "Œil droit"],
  ["left_arm", "Bras gauche"],
  ["right_arm", "Bras droit"],
];

function construireServos() {
  const conteneur = $("servos");
  conteneur.innerHTML = "";
  SERVOS.forEach(([topic, libelle]) => {
    const ligne = document.createElement("div");
    ligne.className = "servo-ligne";

    const label = document.createElement("label");
    label.textContent = libelle;

    const input = document.createElement("input");
    input.type = "number";
    input.min = "0";
    input.max = "99";
    input.value = "50";

    const btnEnvoyer = document.createElement("button");
    btnEnvoyer.type = "button";
    btnEnvoyer.textContent = "Envoyer";
    btnEnvoyer.addEventListener("click", () => {
      const valeur = Math.max(0, Math.min(99, Number(input.value) || 0));
      envoyerCmd(topic, valeur);
    });

    const btnStop = document.createElement("button");
    btnStop.type = "button";
    btnStop.textContent = "Stop";
    btnStop.addEventListener("click", () => envoyerCmd(topic, "stop"));

    ligne.append(label, input, btnEnvoyer, btnStop);
    conteneur.appendChild(ligne);
  });
  // Les boutons viennent d'être (re)créés (naissent "enabled") : il faut leur
  // ré-appliquer l'état écriture/lecture seule courant.
  majBadgeEcriture();
}

function chargerCatalogue() {
  fetch("/api/catalog")
    .then((r) => r.json())
    .then((catalogue) => {
      state.catalog = catalogue;
      // Les visages "calib*" (mires d'étalonnage LED) NE vont PAS en Spectacle :
      // ils partent dans le panneau Technique (cf. CLAUDE.md, calibration à l'œil
      // humain, jamais pendant le jeu).
      const faces = catalogue.faces.filter((f) => !f.startsWith("calib"));
      const calibs = catalogue.faces.filter((f) => f.startsWith("calib"));
      remplirGrille("grille-animations", "animation", catalogue.animations);
      remplirGrille("grille-faces", "face", faces);
      remplirGrille("grille-calib", "face", calibs);
      remplirGrille("grille-audios", "audio", catalogue.audios);
      remplirGrille("grille-robot-lights", "robot_lights", catalogue.robot_lights);
      remplirGrille("grille-relais", "relay", catalogue.relays);
      majBadgeEcriture();
    })
    .catch((e) => logErreur("catalogue indisponible : " + e));
}

// --- Panneau « reçu par le robot » + état (dernier message "state") ----------

const STATUT_DIRECT = [
  ["animation", "Animation", "grille-animations"],
  ["face", "Visage", "grille-faces"],
  ["audio", "Son", "grille-audios"],
  ["robot_lights", "Lumières", "grille-robot-lights"],
];

function libelleValeur(valeur) {
  if (valeur === false) {
    return "arrêtée";           // animation: false = stop d'animation
  }
  return typeof valeur === "string" ? valeur : JSON.stringify(valeur);
}

function majStatutDirect(topics) {
  const conteneur = $("statut-direct");
  conteneur.replaceChildren();
  STATUT_DIRECT.forEach(([topic, libelle, grilleId]) => {
    const info = topics[topic];

    const item = document.createElement("span");
    item.className = "statut-item";
    const nom = document.createElement("span");
    nom.className = "statut-nom";
    nom.textContent = libelle;
    const valeur = document.createElement("span");
    valeur.className = "statut-valeur" + (info ? "" : " statut-vide");
    valeur.textContent = info ? libelleValeur(info.msg) + " · " + info.age_s + " s" : "—";
    item.append(nom, valeur);
    conteneur.appendChild(item);

    // Surbrillance du contenu actif dans sa grille (comparaison en chaîne :
    // dataset.* est toujours une chaîne côté DOM).
    const attendu = info ? String(info.msg) : null;
    document.querySelectorAll("#" + grilleId + " .bouton-catalogue").forEach((btn) => {
      btn.classList.toggle("en-cours", attendu !== null && btn.dataset.value === attendu);
    });
  });
}

function afficherEtat(msg) {
  majStatutDirect(msg.topics);
  // Construction en DOM + textContent (jamais innerHTML avec les payloads) :
  // le contenu vient des topics ROS, donc de n'importe quel publieur -- un
  // payload contenant du HTML ne doit pas pouvoir s'injecter dans la page.
  const topicsDiv = $("etat-topics");
  const table = document.createElement("table");
  const entete = document.createElement("tr");
  ["Topic", "Dernier payload", "Âge"].forEach((titre) => {
    const th = document.createElement("th");
    th.textContent = titre;
    entete.appendChild(th);
  });
  table.appendChild(entete);
  Object.entries(msg.topics).forEach(([topic, info]) => {
    const tr = document.createElement("tr");
    [topic, JSON.stringify(info.msg), info.age_s + " s"].forEach((texte) => {
      const td = document.createElement("td");
      td.textContent = texte;
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });
  topicsDiv.replaceChildren(table);

  $("etat-nodes").textContent = "Nodes vivants (" + msg.nodes.length + ") : " + msg.nodes.join(", ");

  const badgeConn = $("badge-connexion");
  badgeConn.title = msg.clients + " client(s) connecté(s), écriture "
      + (msg.writer_present ? "détenue" : "libre");
}

// --- Démarrage ------------------------------------------------------------------

construireServos();
chargerCatalogue();
installerPad();
installerVideo();
setInterval(bouclePilotage, DRIVE_PERIOD_MS);
connecter();
