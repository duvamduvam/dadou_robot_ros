# Télédiagnostic par agent IA — étude

*Analyse du 2026-07-12. Statut : **proposition argumentée, décisions non tranchées**
(questions ouvertes en §7). Sœur de [`etude-interface-web.md`](etude-interface-web.md),
dont elle réutilise le réseau (W2 Headscale) et le pont web.*

## 1. Le besoin

En déambulation (robot au milieu du public, opérateur occupé à jouer), des problèmes
surviennent qu'on ne peut pas régler sur place : visage figé, servo muet, node
crashé, audio silencieux… Objectif : qu'un **agent IA (Opus via Claude Code)**
puisse investiguer, à la demande, avec le moins d'intervention humaine possible.

Deux régimes, qui n'appellent pas les mêmes moyens :

- **À froid (prioritaire)** : le problème est souvent fugace — le temps de rentrer,
  il a disparu. Il faut une **boîte noire** : des traces persistantes et assez
  riches pour reconstruire l'incident après coup. Aujourd'hui, seule `robot.log`
  survit.
- **À chaud** : investiguer pendant que le spectacle continue. Exige l'accès
  distant (LAN, puis Headscale/4G = W2) et une discipline stricte de lecture seule.

## 2. État des lieux — points de lecture existants

Inventaire du code au 2026-07-12 (détails et références dans le corps du repo) :

| Point de lecture | Contenu | Accès | Limite |
|---|---|---|---|
| `robot.log` (`/home/ros2_ws/log/robot.log`, **monté sur le host du Pi** — survit au conteneur ; rotation quotidienne, backup 100) | erreurs de payload, entrées de chaque node, commandes web (`cmd web id=…`), WARNINGs système (CPU>80 %, mem, disque, temp>55 °C via `utils/status.py`) | `ssh r` | niveau INFO figé (pas de DEBUG à chaud) ; pas lisible via le pont web |
| `docker logs dadou-robot-container` | stdout ROS — dont **tout le `web_bridge_node`** (il logge via `get_logger()` rcutils, PAS dans robot.log) | `ssh r` | **split de journaux non documenté** : deux vérités selon le node |
| Message WS `state` du pont web (2 Hz, port 8765) | **`nodes`** = nodes vivants du graphe (seule détection programmatique d'un node mort), `topics` = dernier payload + âge par topic whitelisté, clients/writer | HTTP/WS, token | rien sur CPU/temp/batterie, rien sur la chaîne roues (hors whitelist), pas de RTT |
| Graphe ROS live | `ros2 topic echo/hz/list`, `ros2 node info` | `ssh r` + `docker exec` | temps réel seulement — rien après coup |

Pièges de diagnostic déjà connus (à transmettre à l'agent) : mDNS `.local`
instable (IP : robot .2, vision .151) ; payload non-JSON = ERROR logguée
(silencieux avant le 2026-07-11) ; `chat_node` du Pi vision écrase `face` au
moindre bruit ; deux configs de logging coexistent (`conf/logging/*.conf` obsolète
vs `LoggingConf` de dadou_utils_ros — seule la seconde est chargée).

## 3. Les trous

1. **Zéro rosbag** dans tout le repo : aucune capture d'événements ROS, l'incident
   fugace est irrécupérable. `validate-cmdvel-protocol.sh` injecte, ne capture pas.
2. **Zéro topic de santé** : pas de `diagnostic_msgs`, pas de heartbeat de node,
   batterie = code entièrement commenté dans `status.py`. La surveillance
   CPU/temp/mem existe mais finit en WARNING dans le fichier log, invisible à
   distance et non corrélable aux événements ROS.
3. **Exceptions invisibles** : les nodes à boucle `spin_once` (system, wheels,
   lights, relays, audio, animations) loggent l'exception et continuent — rien ne
   remonte hors du fichier. Les nodes en `rclpy.spin` (`twist_deadman`,
   `person_follower`, `gaze_follower`) **meurent** sur exception non gérée —
   visibles uniquement par leur absence dans `state.nodes`.
4. **Pont web aveugle sur lui-même** : pas d'endpoint `/health`, pas d'accès aux
   logs, état limité à la whitelist de contenu.
5. **Pas d'accès hors LAN** : W2 (Headscale + routeur 4G) est planifié, pas fait.
   Le télédiagnostic à chaud en déambulation en dépend entièrement — c'est une
   raison de plus de faire W2.

## 4. Architecture proposée

### Où tourne l'agent — et où il ne tourne PAS

**L'agent tourne sur le PC de David (Claude Code), jamais sur le Pi.** Raisons :
pas de clé API embarquée (repo public, historique déjà purgé une fois), pas de
charge IA sur le Pi 4 (tick 20 Hz à protéger), et l'outillage (SSH, docker exec,
lecture d'artefacts) suffit. L'accès passe par le LAN aujourd'hui, par le VPN
Headscale demain (W2) — le backend robot n'a rien à savoir du VPN.

### Sécurité de l'agent (non négociable)

- **Lecture seule par défaut** : l'agent ne publie JAMAIS sur un topic de
  mouvement (`wheels`, `cmd_vel*`, servos), domain 42 ou pas. Ses outils sont
  `topic echo/hz/list`, la lecture de fichiers, les endpoints HTTP.
- **Remédiations en liste blanche, avec confirmation humaine** : restart du
  conteneur robot, restart du conteneur vision (déjà la procédure chat_node),
  relance d'un node mort. Rien d'autre.
- Ces règles vivent dans le skill projet (§4.4) — un agent qui ne les a pas lues
  ne doit pas avoir les accès.

### 4.1 Boîte noire rosbag (le chaînon manquant principal)

`ros2 bag record` en **snapshot mode** (natif Jazzy : buffer circulaire en RAM,
dump sur appel de service) sur les topics **légers** : `cmd_vel*`, `e_stop`,
`animation`, `face`, `audio`, `robot_lights`, servos, `gaze`/`follow`,
`/vision/person*`. La caméra compressed (~150 Ko/s) est exclue par défaut
(question ouverte §7). Ordres de grandeur : quelques Mo de RAM pour plusieurs
minutes d'historique. Lancée par le bringup, dump déclenché par le topic
`incident` (§5). Alternative si le crash du conteneur lui-même doit être couvert :
segments disque de 60 s + purge (coût SD) — à trancher.

### 4.2 Topic `diagnostics` + état enrichi

`system_node` publie périodiquement ce qu'il logge déjà (CPU, mem, disque, temp)
sur un topic de santé — format `StringTime` JSON maison, cohérent avec le reste
(pas de `diagnostic_msgs` : un seul consommateur, notre pont). Le pont web
l'ajoute au message `state` et l'expose. Bénéfice immédiat : la console web
devient un tableau de bord de santé, pour l'humain comme pour l'agent.

### 4.3 Endpoints de lecture sur le pont web

- `GET /api/logs?lines=500` : tail de `robot.log` (token requis, lecture seule).
- `GET /health` : liveness HTTP simple (le pont répond = conteneur vivant).
- Unification des journaux : décision documentée a minima (le split
  robot.log / docker logs est un piège), rediriger `get_logger()` du pont vers
  robot.log si simple.

### 4.4 Le contrat côté agent : skill `/diag` + collecteur

- **`conf/scripts/collect-incident.sh`** : rassemble en un tarball horodaté —
  tail robot.log, `docker logs --since`, `ros2 node list`, `ros2 topic list` +
  `hz` sur les topics clés, dump du snapshot bag, `vcgencmd measure_temp`,
  `df -h`, `free -h`, état réseau. Utile même sans IA (envoyable par mail) ;
  c'est le **format d'entrée standard** de l'agent.
- **Skill projet `/diag`** (`.claude/skills/`) : la carte des points de lecture
  (§2), les commandes exactes (`ssh r`, chemins, docker exec, sourcing ROS), les
  pièges connus, l'arbre des pannes déjà rencontrées (à enrichir à chaque
  incident — c'est la mémoire de panne du robot), et les interdits (§ sécurité).
  Un agent Opus frais + `/diag` + un tarball = investigation autonome.

## 5. Déclencheurs

| Déclencheur | Canal | Effet | Phase |
|---|---|---|---|
| **Bouton « incident »** sur la télécommande physique (en main pendant la déambulation) et la console web | topic `incident` (StringTime) | marqueur horodaté `INCIDENT` dans robot.log + dump du snapshot bag + compteur visible dans l'UI | D1 |
| Node disparu du graphe | le pont web compare `state.nodes` d'un tick à l'autre | auto-snapshot + marquage log (capture seule — pas de lancement d'agent automatique en V1, trop bruyant) | D1 |
| WARNINGs système répétés | `system_node` | idem | D1 |
| Manuel après-coup | David lance `/diag` sur le PC | collecte (ou lecture d'un tarball existant) + investigation | **D0** |
| Bouton → agent headless (`claude -p`) → rapport dans la console web | webhook à travers le VPN | investigation sans humain au clavier | D3 |

Le déclencheur vocal (« Didier, note le problème » via chat_node) est séduisant
mais hors périmètre tant que chat_node V2 (priorité 0) n'est pas validé matériel.

## 6. Phasage

- **D0 — immédiat, zéro déploiement** : `collect-incident.sh` + skill `/diag`
  + cette étude. Dès la prochaine déambulation : retour en coulisse, `/diag`,
  Opus investigue sur les traces existantes (robot.log + docker logs + state).
- **D1 — boîte noire** : snapshot bag + topic `diagnostics` + bouton incident
  (console web, puis télécommande) + `/api/logs` + `/health`. Validation en sim
  d'abord (domain 43), comme tout.
- **D2 — à chaud, à distance** : dépend de **W2** (Headscale + 4G, chantier web).
  L'agent investigue pendant la représentation, depuis n'importe où.
- **D3 — automatisation** : bouton incident → `claude -p` headless sur le PC →
  rapport déposé dans la console web. À n'ouvrir que quand D0-D2 auront montré
  ce que l'agent sait résoudre seul.

Aucune de ces phases ne touche le chemin roues ; D1 ajoute des nodes de **lecture**
au bringup (bag, diagnostics) — revue sécurité habituelle mais pas de protocole
caméra requis.

## 7. Questions ouvertes (à trancher, candidates à un grill)

1. **Snapshot RAM vs segments disque** pour la boîte noire : la RAM ne survit pas
   à un crash du process d'enregistrement ; le disque use la SD. (Proposition :
   RAM en V1 — les pannes vues sont applicatives, pas des crashs conteneur.)
2. **Inclure la caméra compressed dans le bag ?** ~9 Mo/min en RAM. Précieux pour
   « qu'est-ce que le robot voyait » ; cher. (Proposition : non en V1.)
3. **Batterie** : aucun capteur câblé (code commenté). Chantier élec à part
   entière — lien avec les cartes PCB en cours ?
4. **Périmètre exact des remédiations autorisées** à l'agent (restart conteneur
   suffit-il ? relance de node individuelle = comment, dans un launch unique ?).
5. **Bouton incident sur la télécommande physique** : quel bouton/geste sur le
   matériel existant (dépôt `dadou_control_ros`) ?
6. **D3** : le PC de dev est-il allumé/joignable pendant une déambulation, ou
   faut-il un petit serveur toujours-up (le même que Headscale §4 de l'étude web) ?
