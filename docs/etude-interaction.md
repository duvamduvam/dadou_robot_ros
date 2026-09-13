# Plan d'interaction — David, Didier et le public

*Ouverte le 2026-09-13, à la demande de David (« on doit faire un plan
d'interaction, c'est important »), après la première vraie conversation
d'atelier entre lui et Didier.*

> **Ce document est une PROPOSITION.** Rien n'y est tranché tant que David ne
> l'a pas démonté. Les passages marqués **[DÉCIDÉ 13/09]** sont les seuls
> acquis : ce sont ses réponses de la séance, pas mes conclusions.

> ⚠️ **Ce dépôt est PUBLIC.** Le dossier de création du spectacle vit hors
> dépôt (Nextcloud, `créa/théâtre/spectacles/paradise-quest/`). Cette étude
> n'en cite que ce qui justifie une décision technique. Si David juge qu'une
> citation est de trop, elle saute — c'est son texte, pas le mien.

---

## 0. Pourquoi cette étude existe

Deux études encadrent déjà la parole de Didier :
[`etude-declenchement-conversation.md`](etude-declenchement-conversation.md)
(quand et comment il engage un passant) et
[`etude-voix-didier.md`](etude-voix-didier.md) (avec quelle voix). Elles sont
bonnes, et leurs décisions tiennent.

Mais elles ont le même angle mort : **elles ne parlent que du passant.** David
n'y existe pas — alors qu'il est sur scène, qu'il joue, et qu'il est déjà une
source de parole. Or il a dit le 13/09 la phrase qui commande tout le reste :

> « Je suis un personnage pour le public. Tout ce projet en entier est un
> prétexte pour que je joue, moi. »

Cette étude se place donc **au-dessus** des deux autres : elle arbitre le
partage entre David, Didier et le public. Elle ne re-tranche rien de ce qui
l'est déjà (§2).

Sa source première n'est pas le code : c'est la **note de création** du
spectacle (dossier hors dépôt, état du 2026-08-27). Le spectacle existait
avant le robot conversationnel ; c'est à l'IA de servir la dramaturgie, pas
l'inverse.

---

## 1. Le renversement — Didier n'est pas un robot autonome

Tout le travail conversationnel jusqu'ici visait, implicitement, un robot
capable de tenir seul un échange : détecter qu'on lui parle, comprendre,
répondre. C'est la cible qui a rendu la séance du 13/09 frustrante — David a
constaté qu'il avait « du mal à voir comment ça pourrait être le robot
au-delà des interactions en petit groupe ».

**Il a raison, et la bonne réponse n'est pas de renforcer le robot : c'est de
changer de cible.** Didier est un **instrument de jeu**. La question n'est
plus « comment le rendre capable de converser seul », mais « que doit-il
savoir faire pour que David joue avec lui devant un public ».

Conséquence immédiate sur le cahier des charges de l'IA — il **rétrécit** :

| On croyait devoir | En fait il faut |
|---|---|
| comprendre finement ce qu'on lui dit | détecter qu'on lui a répondu, et dans quel registre |
| décider seul où aller | faire avancer une mission dont les étapes sont écrites |
| être autonome | être pilotable *en jeu*, sans sortie de personnage |
| tenir 2 h de conversation | tenir cinq cases et une liste de noms |

---

## 2. Ce qui est déjà tranché — ne pas re-trancher

**Dans la note de création (dossier du spectacle, 27/08)** :

- **« Deux boulets, la rue est l'oracle »** : David et Didier sont tous deux
  incompétents, le public détient la connaissance, ils n'avancent que sur les
  indications des passants. C'est une inversion de hiérarchie voulue.
- **La règle du « oui, et »** : *toute* réponse d'un passant devient une
  avancée — la blague prise au premier degré, le refus salué comme « une
  indication très dense ». « Le passant ne doit jamais avoir le sentiment de
  s'être trompé. »
- **Cinq critères, cinq mouvements** : Didier possède cinq critères
  (*love, tenderness, friendship, speed, strong*) et aucune valeur ; chaque
  rencontre en valide un ; une **jauge visible** progresse ; cinq séquences
  écrites servent de filets.
- **La validation comme moteur d'agrégation** : qui donne une indication
  reçoit une contrepartie visible (grade, numéro) et devient partie prenante.
- **La fin** : les cinq critères réunis, les coordonnées du paradis sont
  *ici, maintenant, avec ces gens-là* — « le paradis est littéralement fait
  de ce qu'ils ont dit ».

**Dans les études existantes du dépôt** : la FSM d'engagement et ses seuils
(§5.2 de l'étude déclenchement), le « réactif d'abord », le gate half-duplex,
la latence cible < 2 s, les personas commutables.

**Décidé par David le 13/09, en séance** :

- **[DÉCIDÉ 13/09] Il est un personnage pour le public**, pas un servant
  invisible.
- **[DÉCIDÉ 13/09] Aucune écoute préalable.** Il ne peut pas entendre les
  répliques avant le public : ça exige de sortir du jeu pour se concentrer,
  et surtout ça ne servirait à rien — *« je fais quoi si la sortie ne me
  plaît pas ? Je coupe tout, j'envoie un texto ? Non, c'est trop compliqué,
  j'assume. »* Un contrôle qu'on ne peut pas actionner n'est pas un contrôle.
- **[DÉCIDÉ 13/09] Aucune frontière jeu / régie.** Tout pilotage doit être
  intégré au jeu : *« si je dois sortir du jeu pour changer les instructions,
  c'est compliqué »*.
- **[DÉCIDÉ 13/09] Il doit pouvoir reprendre la main** si Didier « fait
  n'importe quoi » — mais en jeu, donc.
- **[DÉCIDÉ 13/09] Didier parle aux autres, pas seulement à David.** Il doit
  donc entendre le public : le problème de captation ne se dissout pas.
- **[DÉCIDÉ 13/09] Le paradis ne se trouve pas.** Et la raison est le fond du
  spectacle, dans les mots de David : *« le paradis est diabolique plutôt, il
  nous détache de l'instant dans l'espoir d'un autre instant plus adapté à la
  perception de nous-même »*. La fin de la note de création dit la même chose
  par l'autre bout : les coordonnées sont ici et maintenant.

---

## 3. Les trois décisions demandées

### 3.1 Déclenchement de la parole — une réplique, jamais un bouton

**Proposition.** Didier ne décide pas seul quand il parle. David lui donne la
parole **en s'adressant à lui à voix haute, en personnage** : « Alors Didier,
qu'est-ce que t'en dis ? », « Didier, demande-lui. »

Pourquoi c'est le bon mécanisme, et pas un pis-aller :

- c'est **déjà du théâtre** — le public lit une relance de jeu, pas une
  commande ; l'exigence « intégré au jeu » est satisfaite par construction ;
- la réplique **cadre** la réponse en même temps qu'elle la déclenche : ce que
  David dit oriente ce que Didier répond. Il pilote en jouant ;
- ça **supprime la question la plus dure** côté David : plus besoin de deviner
  quand *lui* a fini de parler, puisque c'est lui qui rend la parole ;
- ça **ne coûte rien de plus** à David, qui devrait de toute façon dire une
  réplique à cet endroit-là — point important au vu de la charge déjà lourde
  identifiée au §7.7 de la note de création (« le troisième larron »).

⚠️ **Le piège à ne pas reproduire.** Un mot-clé de réveil rigide (« Didier ! »
et rien d'autre) ferait exactement ce que David refuse : sortir du jeu, sous
un déguisement. Le déclencheur doit accepter **la variété d'une réplique
jouée**, donc être reconnu par le sens et non par la forme exacte. C'est un
travail de reconnaissance souple, pas une comparaison de chaîne.

**Reprise en main — même mécanisme, autre intention.** Reprendre la main, ce
n'est pas couper : c'est **faire avancer la mission**. « Bon, Didier, critère
suivant » est à la fois une réplique et une transition d'état. La structure
en cinq mouvements est donc **l'interface de pilotage** : les cinq filets de
sécurité de la note de création deviennent littéralement les cinq commandes.

### 3.2 Mémoire — cinq cases et des noms, pas une fenêtre glissante

**Le désaccord du 13/09 n'était pas sur la taille de la mémoire, il était sur
sa nature.** David : *« pourquoi doit-on avoir une limite ? Si je déambule
2 h, ça va être juste. »* Il a raison sur le constat (6 échanges, c'est
absurdement court) et le remède n'est pas d'allonger la fenêtre.

Ce que le spectacle exige réellement de la mémoire, c'est **ce que la finale
restitue** : qui a donné quoi, pour quel critère. Une structure minuscule :

```
mission:
  critères: love / tenderness / friendship / speed / strong
  pour chacun : valeur donnée, par qui (prénom, signalement), numéro de guide
  direction courante (la dernière indication reçue)
```

Trois propriétés qui découlent de la dramaturgie, pas de la technique :

- **permanente sur toute la déambulation** — c'est le fil du spectacle ;
- **minuscule** — quelques dizaines de mots, donc gratuite en latence, alors
  qu'un historique de 2 h se paierait à *chaque* réplique (l'historique est
  renvoyé en entier à chaque tour : c'est là qu'était la vraie raison de la
  limite) ;
- **distincte de la conversation en cours**, qui, elle, reste volatile et
  meurt avec la rencontre — conforme aux sessions déjà décidées au §5.2 de
  l'étude déclenchement (et jamais implémentées : `chat_node` n'ouvre
  aujourd'hui qu'une seule session, au démarrage du node).

Conséquence heureuse : la jauge visible réclamée par la note de création
**est** cet état, affiché. Didier a un visage et un corps en LED — elle peut
y vivre sans matériel supplémentaire.

⚠️ Un contrat mort à réveiller ou à enterrer : le prompt demande déjà à
Didier d'émettre `{"name": …}` quand on se présente, et `NAME_KEY` existe
dans le parseur — **rien ne le consomme**. C'est exactement la brique qu'il
faut pour la liste des guides.

### 3.3 La réponse non comprise — le « oui, et » devient un contrat technique

C'est la trouvaille de la séance, et elle est dans le dossier depuis le 27/08
sans qu'on l'ait vue : **la règle du « oui, et » est une tolérance aux erreurs
de compréhension.** Le tableau de la note de création ne demande jamais à
Didier de comprendre juste — il demande de *faire quelque chose* de n'importe
quelle réponse.

Donc, comme règle d'écriture du personnage :

- une transcription douteuse **n'est pas un échec, c'est une matière** : un
  robot qui entend « c'est fermé » là où on a dit « au fournil » est le
  numéro, pas la panne ;
- **ne jamais faire répéter plus d'une fois.** Faire répéter est l'aveu du
  dispositif ; c'est aussi ce qui met le passant en faute, ce que la règle
  d'or interdit ;
- **rien n'est jamais une mauvaise réponse** — y compris pour le silence et
  le refus, qui ont déjà leur réplique écrite.

⚠️ Ce que ça ne dispense PAS de faire : **détecter qu'une réponse a eu lieu,
et quand elle se termine.** C'est le point sur lequel David m'a repris à
juste titre — la tolérance porte sur le *contenu*, jamais sur la *détection*.
Voir §6.

---

## 4. Ce que ça change dans le code

Rien de ce qui suit n'est à faire avant validation de l'étude. C'est la
traduction, pour mesurer le coût.

1. **Deux boucles au lieu d'une.** Aujourd'hui `ConversationEngine.run_once`
   est un cycle unique et bloquant : écouter → transcrire → répondre. Il faut
   séparer une **perception continue** (qui tourne toujours) d'un **acte de
   parole** (déclenché). C'est le changement structurel principal.
2. **Un état de mission**, porté par un module pur et testé (patron du dépôt :
   la logique sans ROS, le node autour), publié en topic latché pour la jauge
   et la console, et alimenté par les transitions de §3.1.
3. **Sessions par rencontre** — décidées en juillet, jamais faites.
4. **Consommer `{"name"}`** pour la liste des guides (§3.2).
5. **Deux entrées audio** (§6) : `MicCapture` n'ouvre aujourd'hui qu'un seul
   périphérique.
6. **La jauge sur le visage/corps LED** — chemin existant (`robot_lights`,
   expressions), aucune électronique à ajouter.

---

## 5. Garde-fous — puisqu'il n'y a pas d'écoute préalable

L'étude de juillet avait explicitement reporté la question : « confiance au
modèle pour l'instant, à réévaluer après les premières sorties ». Deux
éléments nouveaux justifient de la rouvrir **avant** la première sortie :
David découvrira chaque réplique en même temps que le public
(**[DÉCIDÉ 13/09]**), et l'objectif du spectacle est de tenir un **groupe**,
pas un passant isolé — ce qui multiplie le coût d'un dérapage.

Ce qui protège, par ordre d'efficacité réelle :

1. **la brièveté** — une réplique de deux phrases dérape moins qu'une tirade,
   et se rattrape en jeu ;
2. **le cadre de mission** — Didier a toujours une question à poser, il
   improvise donc *dans* une séquence à objectif connu, pas dans le vide ;
3. **la règle d'or du dossier** — viser le dispositif, jamais les gens ; le
   passant n'est jamais en faute. C'est une règle de sécurité autant que de
   politesse ;
4. **la reprise en main en jeu** (§3.1), qui est le vrai filet ;
5. le persona lui-même, qui porte déjà des esquives (opinions absurdes sur
   des sujets sans enjeu) — utile, mais c'est le plus faible des cinq, et il
   ne faut pas lui faire porter la sécurité à lui seul.

⚠️ **Point à trancher par David** : les enfants. Le dossier prévoit que la
distance se joue (« Didier a peur qu'on le touche, il recule ») plutôt
qu'elle ne s'impose. Si l'IA parle aux enfants, le registre doit être verrouillé
au-delà de ce que fait le socle actuel des personas.

---

## 6. Les deux oreilles

**Le problème ne se dissout pas** (correction de David, 13/09) : Didier parle
aux passants, donc il doit les entendre. Mais les deux oreilles n'ont pas le
même cahier des charges.

| | Entendre David | Entendre le public |
|---|---|---|
| Distance | proche | 2-4 m, en cortège |
| Bruit | maîtrisé | rue, foule |
| Ce qu'il faut en tirer | **le sens** (c'est un pilotage) | **qu'on a répondu**, et le registre |
| Difficulté | faible **si** canal dédié | élevée, durablement |

**Côté David.** Son micro HF actuel sert la ventriloquie, dont il souhaite
plutôt se séparer — mais *abandonner la ventriloquie et donner une oreille
propre au Pi sont deux décisions distinctes*. Le Pi accepte n'importe quelle
carte son USB sans pilote (c'est déjà le cas du ReSpeaker). Deux chemins :

- **sans rien acheter** : dériver la sortie ligne du récepteur HF vers
  l'adaptateur USB C-Media déjà en stock — ça teste l'idée avant d'engager
  quoi que ce soit ;
- **proprement** : un système micro sans fil dont le récepteur *est* une carte
  son USB, branché directement sur le Pi.

⚠️ Correction d'une erreur que j'ai écrite en séance : **la mixette reste
indispensable** — elle porte la sortie (enceintes, niveaux, mélange). Un micro
USB sur le Pi n'enlève rien à la chaîne son.

⚠️ Question ouverte si l'on garde le HF : ce micro porterait *deux* voix —
celle de David en personnage, et Didier ventriloqué. Il faut savoir comment
les séparer (canal, coupure de l'octaver, ou David ne parle jamais « en
David » dans ce micro).

**Côté public.** Rien ne rendra la captation facile. Deux leviers déjà payés
et inexploités : la **direction d'arrivée du son** du ReSpeaker, croisée avec
l'azimut de la caméra, pour distinguer « ça vient de la personne en face » ;
et une **VAD neuronale** à la place du seuil d'énergie actuel, calibré une
seule fois au démarrage et intenable en rue.

**Et un troisième levier, qui est du jeu.** Si Didier entend mal les
étrangers, le montrer plutôt que le cacher : **David relaie.** Il répète, il
traduit, il s'agace. Le public lit un vieux robot un peu sourd — un caractère,
pas une panne — et l'objection que David soulevait lui-même (« deux niveaux de
compréhension, c'est moins lisible pour le public ») tombe, parce qu'elle
n'est illisible que tant qu'elle est dissimulée.

---

## 7. Ce qui reste ouvert

- **Le commentaire du monde** (le bâtiment bizarre, le sol irrégulier). David
  n'a pas tranché s'il est déclenché ou spontané. L'étude note seulement qu'il
  n'est **pas structurant** : les raisons concrètes d'avancer viennent des
  cinq critères, pas de la perception. C'est un bonus, à ouvrir quand le reste
  tient. Techniquement il faudrait un chemin image → langage (il existe à
  moitié dans l'ancien code GPT-4o, jamais relié à la conversation actuelle),
  et il devra consommer le flux JPEG déjà publié par le suivi de personne —
  **surtout pas rouvrir la caméra**, tenue en exclusif.
- **La voix** reste suspendue au lot V0 du chantier voix. Si David abandonne
  la ventriloquie, cet arbitrage change de nature : ce n'est plus « assurer la
  continuité entre deux sources » mais « choisir la voix de Didier ». À
  reprendre là-bas, pas ici.
- **L'écriture des cinq séquences** (note de création §8) : c'est elle qui
  dira ce que Didier doit savoir dire à chaque mouvement.
- **Le troisième larron** (note de création §7.7). Si un régisseur existe, une
  partie du pilotage peut lui revenir — ce qui changerait §3.1.

---

## 8. Convergence à signaler — la note de création et le tableau de bord disent la même chose

Le §7.2 de la note de création (27/08) exige « un arrêt d'urgence physique
(coup de poing) accessible sur le robot, atteignable par David en un geste »
comme condition pour qu'une date soit assurable.

Le tableau de bord du dépôt (30/08, indépendamment) a établi que **`e_stop`
n'a aucun publieur**, que les deux boutons du dos font l'inverse de ce que
leur nom promet (ils éteignent le Pi, donc provoquent un emballement), et que
la carte qui porterait le coup-de-poing n'est pas fabriquée.

Les deux documents décrivent le même trou par les deux bouts. **Aucune
déambulation publique n'est possible avant que ce point soit fermé** — c'est
antérieur à tout ce que cette étude propose.

---

## 9. Lots proposés

Ordre choisi pour que chaque lot soit jouable seul, et vérifiable en
simulation avant le réel.

| Lot | Contenu | Vérifiable sans robot |
|---|---|---|
| **I0** | État de mission (module pur + topic latché) et jauge sur le visage LED | oui (sim + aperçu visage) |
| **I1** | Déclenchement de parole en jeu + transitions de mission par réplique | oui (banc PC) |
| **I2** | Mémoire des guides (`{"name"}` consommé) + sessions par rencontre | oui |
| **I3** | Deuxième oreille (canal David) et arbitrage entre les deux entrées | banc PC, puis réel |
| **I4** | Contrat « oui, et » dans l'écriture du personnage + garde-fous §5 | oui |
| **I5** | Détection de parole en rue (DoA, VAD neuronale) | non — mesures réelles |

I0 à I2 se font entièrement sur le banc PC, donc **pendant l'immobilisation du
robot**. I5 demande la rue.
