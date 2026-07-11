"use strict";
/*
 * Pont web W0 -- logique front, vanilla JS (pas de framework, pas de build).
 *
 * Le contrat protocole est celui de robot_web/web_protocol.py côté serveur ;
 * les constantes numériques ci-dessous (HEARTBEAT_PERIOD_S) sont DUPLIQUÉES
 * volontairement (pas de partage possible entre Python serveur et JS
 * navigateur) -- même choix assumé que robot_drive/wheels_payload.py pour
 * ses constantes de protocole.
 */

// Cadence du heartbeat applicatif (doit rester alignée sur
// web_protocol.HEARTBEAT_PERIOD_S côté serveur).
const HEARTBEAT_PERIOD_S = 1.0;

// Backoff de reconnexion WebSocket : 1 s -> 5 s, doublé à chaque échec.
const RECONNECT_MIN_MS = 1000;
const RECONNECT_MAX_MS = 5000;

// Moyenne glissante du RTT sur les 5 derniers battements.
const RTT_WINDOW = 5;

// --- État global du client --------------------------------------------------

const state = {
  ws: null,
  authSent: false,          // un seul message "auth" envoyé par connexion
  isWriter: false,
  tokenRequired: false,
  reconnectDelayMs: RECONNECT_MIN_MS,
  rttSamples: [],           // fenêtre glissante (ms)
  hbTimer: null,
  catalog: null,
  attenteAck: {},           // topic -> bouton cliqué, flashé à l'ack (pas au clic)
  dernierBouton: null,      // dernier bouton cliqué, flashé rouge sur "err"
};

// --- Utilitaires DOM ---------------------------------------------------------

function $(id) {
  return document.getElementById(id);
}

function logErreur(message) {
  const ul = $("journal-erreurs");
  const li = document.createElement("li");
  li.textContent = new Date().toLocaleTimeString() + " -- " + message;
  ul.prepend(li);
  // Garde les 5 dernières seulement (spec §5).
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
  majBadgeEcriture();
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
  // elle "badge " + undefined donne "badge undefined" (chaîne non vide donc
  // TRUTHY) et le fallback badge-inconnu ne se déclenche jamais.
  badge.className = "badge " + (CLASSE_BADGE_PAR_MODE[mode] || "badge-inconnu");
}

function majBadgeEcriture() {
  const badge = $("badge-ecriture");
  badge.textContent = state.isWriter ? "écriture" : "lecture seule";
  badge.className = "badge " + (state.isWriter ? "badge-on" : "badge-off");
  // Les boutons d'action (catalogue + panneau technique) sont inertes en
  // lecture seule -- pas d'interdiction côté serveur seule, l'UI l'affiche.
  document.querySelectorAll(".bouton-catalogue, .servo-ligne button, #btn-stop-contenus, "
      + "#btn-system-restart, #btn-system-shutdown")
    .forEach((btn) => { btn.disabled = !state.isWriter; });
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
  // La confirmation de prise de main arrive via le prochain "hello" -- on
  // relance le heartbeat dès qu'on la reçoit (traiterHello).
});

$("btn-token").addEventListener("click", () => {
  const token = $("token-input").value;
  envoyerAuth(token);
});

// --- Onglets -------------------------------------------------------------------

document.querySelectorAll(".onglet-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".onglet-btn").forEach((b) => b.classList.remove("actif"));
    document.querySelectorAll(".onglet").forEach((s) => s.classList.remove("actif"));
    btn.classList.add("actif");
    $("onglet-" + btn.dataset.onglet).classList.add("actif");
  });
});

// --- STOP CONTENUS ---------------------------------------------------------------

$("btn-stop-contenus").addEventListener("click", () => {
  envoyer({ type: "stop_all" });
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

// --- Gaze on/off et relais : boutons générés/statiques, gérés en un seul
// écouteur délégué (data-topic/data-value sur chaque bouton .bouton-catalogue) --

document.addEventListener("click", (event) => {
  const btn = event.target.closest(".bouton-catalogue");
  if (btn) {
    envoyerCmd(btn.dataset.topic, btn.dataset.value);
    // Pas de flash ici : il viendra de l'ack serveur (traiterMessageServeur),
    // sinon un clic "réussi" visuellement peut n'avoir rien publié du tout.
    state.attenteAck[btn.dataset.topic] = btn;
    state.dernierBouton = btn;
  }
});

// --- Catalogue (GET /api/catalog) : grilles spectacle + relais technique ------

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
    // listes de noms (le nom sert à la fois de libellé et de valeur publiée).
    const libelle = typeof entree === "string" ? entree : entree.label;
    const valeur = typeof entree === "string" ? entree : entree.value;
    grille.appendChild(creerBoutonCatalogue(topic, valeur, libelle));
  });
}

// Servos du panneau technique : mêmes 5 topics que le contrat StringTime
// (voir docs/interfaces.md), chacun avec un champ 0-100 + Envoyer/Stop.
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
  // Les boutons Envoyer/Stop viennent d'être (re)créés : ils naissent
  // "enabled" par défaut (attribut disabled absent) -- il faut leur
  // ré-appliquer l'état écriture/lecture seule courant, sinon un client en
  // lecture seule verrait des boutons cliquables jusqu'au prochain "state".
  majBadgeEcriture();
}

function chargerCatalogue() {
  fetch("/api/catalog")
    .then((r) => r.json())
    .then((catalogue) => {
      state.catalog = catalogue;
      remplirGrille("grille-animations", "animation", catalogue.animations);
      remplirGrille("grille-faces", "face", catalogue.faces);
      remplirGrille("grille-audios", "audio", catalogue.audios);
      remplirGrille("grille-robot-lights", "robot_lights", catalogue.robot_lights);
      remplirGrille("grille-relais", "relay", catalogue.relays);
      // Même remarque que construireServos() : les boutons du catalogue
      // naissent enabled, il faut réappliquer l'état écriture courant.
      majBadgeEcriture();
    })
    .catch((e) => logErreur("catalogue indisponible : " + e));
}

// --- Panneau « état » (dernier message "state") -------------------------------

// Topics affichés dans le bandeau "reçu par le robot" (onglet Spectacle) et
// surlignés dans leur grille. Source : les broadcasts "state" (donc les topics
// ROS réels), PAS nos clics -- si rien ne s'affiche, rien n'est parti.
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
  // le contenu vient des topics ROS, donc potentiellement de n'importe quel
  // publieur du graphe -- un payload contenant du HTML ne doit pas pouvoir
  // s'injecter dans la page de contrôle.
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
connecter();
