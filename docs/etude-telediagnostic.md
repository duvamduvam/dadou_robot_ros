# Télédiagnostic par agent IA — étude complète

*v2 du 2026-07-12 (la v1 du même jour proposait un agent côté PC via VPN ; David a
challengé — « pourquoi du VPN, je veux un agent sur la RPi » — et demandé une étude
complète, options comparées, avant de décider. Statut : **étude complète, décisions
listées en §8, à trancher**.*

## 1. Le besoin

En déambulation (robot au milieu du public, David occupé à jouer), des pannes
surviennent qu'on ne peut pas régler sur place : visage figé, servo muet, node
crashé, audio silencieux… Et elles sont souvent **fugaces** : le temps de rentrer,
plus rien à voir. On veut qu'un **agent IA investigue** — déclenché depuis la
télécommande (et peut-être un bouton sur le robot), avec le moins d'intervention
possible.

Deux moments, deux besoins :
- **Sur le moment** : capturer l'état au moment de la panne (sinon l'incident
  fugace est perdu à jamais) et, si possible, investiguer tout de suite.
- **Après coup** : reconstruire et expliquer la panne à partir des traces.

## 2. Ce que l'agent peut lire aujourd'hui (état des lieux)

Inventaire du code au 2026-07-12 :

| Point de lecture | Contenu | Limite |
|---|---|---|
| `robot.log` (sur la carte SD du Pi, **hors conteneur** — survit à un crash du conteneur ; rotation quotidienne, 100 jours gardés) | erreurs de payload, entrées de chaque node, commandes web, alertes système (CPU > 80 %, mémoire, disque, température > 55 °C) | niveau INFO figé ; très verbeux (~16 Mo/jour) |
| `docker logs dadou-robot-container` | la sortie ROS — dont **tout le pont web** (il logge par `get_logger()`, PAS dans robot.log) | **deux journaux séparés**, piège connu |
| Message `state` du pont web (port 8765, toutes les 2 s) | **liste des nodes vivants** (seul moyen de voir un node crashé), dernier message + âge par topic de contenu | rien sur CPU/température/batterie, rien sur la chaîne roues |
| Le graphe ROS en direct | `ros2 topic echo/hz/list` dans le conteneur | temps réel seulement — rien après coup |

**Les trous** (balayage complet du code) :
1. **Zéro rosbag** dans tout le repo : aucun enregistrement des événements ROS.
   L'incident fugace est irrécupérable. C'est LE chaînon manquant.
2. **Zéro topic de santé** : les alertes CPU/température finissent dans le fichier
   log et nulle part ailleurs ; la batterie n'a aucun capteur (code commenté).
3. **Exceptions invisibles** : les nodes principaux avalent leurs exceptions (log
   puis on continue) ; `twist_deadman`, `person_follower` et `gaze_follower`
   **meurent** sur exception — on ne le voit que par leur absence dans `state`.
4. Pièges pour l'agent : mDNS `.local` instable (IP : robot .2, vision .151),
   payload non-JSON refusé, `chat_node` qui écrase `face`, deux configs de
   logging dont une obsolète (`conf/logging/*.conf` n'est plus chargée).

## 3. Où tourne l'agent — les trois options

C'est LA décision structurante. Le malentendu de la v1 à dissiper d'abord :
**un VPN ne sert qu'à ENTRER sur le robot depuis l'extérieur**. Un agent qui
tourne SUR le Pi n'a besoin que de SORTIR en HTTPS vers `api.anthropic.com`
(port 443, seul point de contact requis — vérifié doc officielle). En
déambulation, un simple partage de connexion du téléphone suffit. Le VPN
Headscale du chantier web reste utile pour la télé-présence (piloter à
distance), mais **le diagnostic embarqué n'en dépend pas** — les deux chantiers
sont découplés.

### Option A — Agent embarqué sur le Pi robot (préférence exprimée)

Claude Code s'installe **sur le host du Pi, HORS du conteneur ROS** (binaire
natif ARM64, supporté officiellement, prérequis 4 Go de RAM). Hors conteneur
c'est voulu : **l'agent doit survivre à la mort du conteneur** — c'est
précisément une des pannes à diagnostiquer. Depuis le host il voit robot.log
(monté sur la SD), `docker logs`, et entre dans le conteneur par `docker exec`
pour l'introspection ROS.

- **Déclenchement** : un mini-service sur le host (systemd) guette le signal
  (voir §5) et lance `claude -p "investigue" …` en mode non-interactif.
  Garde-fous natifs : limite de tours, **plafond de coût en dollars par
  investigation** (`--max-budget-usd`), timeout shell, sortie JSON.
- **Verrouillage lecture seule PAR CONFIG** (pas par bonne volonté du modèle) :
  liste blanche d'outils et de motifs de commandes (`tail`, `grep`,
  `ros2 topic echo`, `docker logs`…), interdiction d'écrire des fichiers et de
  toute commande destructrice. Défense en profondeur possible avec le sandbox.
- **Clé API** : variable d'environnement dans un fichier du host, jamais dans le
  repo (le rsync de déploiement n'y touche pas). Risque « vol du robot = vol de
  la clé » → clé dédiée, plafond de dépense côté console Anthropic, révocable.
- **Coût par investigation** (20-40 tours d'outils) : ~0,10 $ en Haiku,
  ~0,30 $ en Sonnet, ~0,50 $ en Opus. Négligeable même à l'usage quotidien.
- **Restitution** : rapport écrit dans un fichier du volume partagé → la console
  web l'affiche ; et/ou le robot le **dit** (topic `audio`/TTS — en coulisse,
  pas en jeu) ; et/ou notification téléphone.
- **Inconnues à lever** : la **RAM du Pi 4 n'est documentée nulle part**
  (`cat /proc/meminfo` à faire — si 2 Go, ça se discute) ; charge CPU d'une
  investigation pendant que le tick 20 Hz tourne (à mesurer, `nice` possible) ;
  qualité du lien 4G partagé en salle.
- Variante plus intégrée : l'**Agent SDK Python** (`pip install
  claude-agent-sdk`) permettrait à un node ROS de déclencher l'investigation
  directement sur réception du topic — plus propre qu'un subprocess, mais une
  dépendance de plus dans l'embarqué. Le CLI headless suffit pour commencer.

### Option B — Agent sur le PC, accès au robot par SSH

C'est le mode « atelier » : une session Claude Code sur le PC de dev, qui lit le
Pi par SSH (`ssh r`). **Fonctionne déjà aujourd'hui en LAN, zéro déploiement.**
En déambulation hors LAN, il faudrait le VPN (chantier web, pas fait) ET le PC
allumé quelque part — deux dépendances que l'option A n'a pas. Avantages
propres : l'historique git complet (le `.git` n'est pas rsyncé sur le Pi — un
agent embarqué ne peut pas faire d'archéologie de commits), le confort d'une
session interactive, et aucun risque pour le spectacle (rien ne tourne sur le
robot).

### Option C — Hybride (recommandation)

Les deux ne s'excluent pas et partagent les mêmes fondations (collecteur, skill,
journal d'incidents) :
- **Sur le terrain** : l'agent embarqué (A), déclenché de la télécommande,
  investigation immédiate, rapport dans la console/voix.
- **À l'atelier** : la session PC (B) pour l'analyse approfondie, les
  correctifs, l'archéologie git.

Le surcoût du « les deux » est faible : c'est le même skill et le même format de
rapport, seul le lieu d'exécution change.

## 4. Le contexte de l'agent (réponse à la question « RAG ? »)

Fait vérifié : le déploiement Ansible rsync **tout le checkout** sur le Pi —
`docs/`, `CLAUDE.md`, le code, les JSON. Un agent embarqué a donc déjà le même
corpus que l'agent du PC (sauf `.git`). Claude Code cherche nativement par
grep/lecture ciblée : à l'échelle de ce corpus (quelques centaines de Ko de
docs), **un RAG vectoriel n'apporterait rien** — de l'infrastructure à
entretenir pour un gain nul. À réévaluer seulement si le corpus change d'ordre
de grandeur (archives de logs massives, transcriptions).

Ce qui manque vraiment, c'est du contexte **métier de panne**, et il se
construit avec deux fichiers :
1. **Le skill `/diag`** : la carte des points de lecture (§2), les commandes
   exactes, les pièges connus, et les interdits. C'est le « briefing » que tout
   agent (embarqué ou PC) charge avant d'investiguer.
2. **Le journal d'incidents** (`docs/incidents/`) : chaque investigation se
   termine par un court post-mortem (symptôme, cause, remède, date). L'agent
   suivant les lit — c'est la mémoire de panne du robot, et c'est le vrai
   « RAG » utile ici. Il se rsync avec le reste.

## 5. Déclencheurs — ce que l'inventaire matériel a révélé

Côté **télécommande** (dépôt `dadou_control_ros`), il y a de la place :
- **Le bouton START est libre** — sur les 12 boutons GPIO de la télécommande
  (D21, mapping explicitement vide) ET sur la manette USB (START/SELECT/MODE
  libres tous les trois). C'est le candidat naturel : David l'a en main en
  déambulant.
- La **GUI** a une place immédiate dans sa barre de menu (à côté de P/K/C/M)
  pour un bouton logiciel « incident ».
- Dans tous les cas il faut **créer le topic `incident`** : la télécommande ne
  publie que 14 topics whitelistés (`PUBLISHER_LIST`), il faut l'y ajouter.
  Anti-fausse-manip : un appui bref ne déclenche rien, exiger un appui long
  (~2 s) ou un double appui.

Côté **robot** (bouton physique sur la bête) : le mécanisme existe — le
`system_node` lit déjà deux boutons GPIO (extinction D16, redémarrage D20) et
en ajouter un est trivial logiciellement. MAIS **aucun GPIO libre n'est
documenté** (les schémas sont des images sans pinout exploitable) ; à vérifier
sur le matériel. Et un bouton accessible sur un robot au milieu du public,
c'est aussi un bouton que le public peut presser. → possible, pas prioritaire.

Déclencheurs automatiques (capture seule, jamais de lancement d'agent
automatique au début — trop bruyant) : node disparu du graphe (le pont web le
voit déjà), alertes système répétées.

## 6. La boîte noire (indispensable quelle que soit l'option)

Sans capture, même le meilleur agent ne peut rien sur un incident fugace.
`ros2 bag record` en **mode snapshot** (natif Jazzy) garde en permanence les
N dernières minutes en mémoire, et ne les écrit sur disque QUE sur demande —
le dump est déclenché par le topic `incident`. Topics enregistrés : `cmd_vel*`,
`e_stop`, `animation`, `face`, `audio`, `robot_lights`, servos, `gaze`/`follow`,
`/vision/person*` (légers : quelques Mo de RAM pour plusieurs minutes).
La caméra (~9 Mo/min) est exclue par défaut — à trancher. Le même appui sur
START écrit aussi un marqueur `INCIDENT` horodaté dans robot.log : tout est
corrélable. En complément, `collect-incident.sh` rassemble le tout (tail des
logs, état du graphe, températures, disque) en un tarball horodaté — le format
d'entrée standard de toute investigation.

Limite assumée du snapshot en RAM : il meurt avec le process qui enregistre.
L'alternative (écrire en continu sur la SD par segments) couvre aussi le crash
complet mais use la carte. Proposition : RAM d'abord — les pannes constatées
sont applicatives, et robot.log (sur SD) couvre déjà le reste.

## 7. Sécurité (non négociable, quelle que soit l'option)

- L'agent est **lecteur** : jamais de publication sur un topic de mouvement
  (`wheels`, `cmd_vel*`, servos), jamais d'écriture de fichier, verrouillé par
  la configuration de permissions (liste blanche de commandes), pas par la
  consigne seule.
- **Remédiations** en liste blanche uniquement, et jamais autonomes pendant une
  représentation : redémarrer le conteneur robot ou vision, relancer un node —
  sur confirmation de David (depuis la console web ou la télécommande).
- Budget borné par investigation (`--max-budget-usd`) + timeout — un agent qui
  boucle s'arrête tout seul.
- Clé API dédiée au robot, plafonnée et révocable dans la console Anthropic.
- Rien de tout ça ne touche le chemin roues ; la boîte noire et le topic
  `incident` sont des ajouts en lecture/capture, revue sécurité habituelle mais
  pas de protocole caméra requis.

## 8. Les décisions à prendre (le grill reprend ici)

1. **Où tourne l'agent** : embarqué (A), PC (B), hybride (C — recommandé).
2. **Modèle et budget par défaut** de l'agent embarqué : Haiku (~0,10 $),
   Sonnet (~0,30 $), Opus (~0,50 $) — recommandation : Sonnet par défaut,
   Opus à la demande depuis l'atelier.
3. **Déclencheur retenu** : START télécommande (recommandé), bouton GUI,
   bouton physique sur le robot (GPIO libre à vérifier d'abord), combinaison.
4. **Restitution du rapport** : console web (recommandé), voix du robot en
   coulisse, notification téléphone.
5. **Boîte noire** : snapshot RAM (recommandé) vs segments SD ; caméra incluse
   ou non (recommandé : non).
6. **Remédiations autorisées** : liste exacte et mécanisme de confirmation.
7. **Batterie** : aucun capteur — à parquer vers le chantier élec (cartes PCB) ?
8. **Préalables factuels** : RAM du Pi 4 (`cat /proc/meminfo`), test de charge
   d'une investigation pendant le tick 20 Hz, qualité 4G partagée en condition.

## 9. Ordre de construction proposé (après décisions)

Chaque étape est utile seule ; on peut s'arrêter à n'importe laquelle :

1. **Trousse d'atelier** — `collect-incident.sh` + skill `/diag` + journal
   d'incidents. Dès la prochaine déambulation : retour, session Claude sur le
   PC, investigation sur les traces existantes. Zéro déploiement sur le robot.
2. **Boîte noire + bouton** — enregistreur snapshot dans le bringup, topic
   `incident`, bouton START télécommande, marqueur dans robot.log, endpoints
   de lecture sur le pont web (`/api/logs`, `/health`). Validé en sim d'abord.
3. **Agent embarqué** — Claude Code sur le host du Pi, service de déclenchement,
   permissions verrouillées, rapport dans la console web. Répétition générale
   en atelier : provoquer une panne connue, appuyer sur START, lire le rapport.
4. **Itinérance** — Internet sortant en déambulation (partage téléphone, puis
   routeur 4G du flight case quand le chantier web l'apportera) ; test en
   condition réelle.
