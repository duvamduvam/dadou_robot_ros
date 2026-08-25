# La voix de Didier — continuité entre ventriloquie et synthèse

*Étude ouverte le 2026-08-26. Le **cadre technique** ci-dessous (§3, §4, §6)
est posé et argumenté ; l'**arbitrage artistique** (§5) est explicitement
SUSPENDU au résultat du lot V0 — David tranche après avoir écouté, pas avant.
Ne pas re-trancher §3 (le principe directeur) sans argument nouveau.*

## 1. Le problème

L'IA arrive dans les réponses de Didier, et la pertinence de ces réponses sera
un travail long. Pendant toute cette phase — probablement des mois — le
spectacle alternera **deux sources de parole** :

- la **ventriloquie** : David parle dans un micro HF, sa voix sort du châssis ;
- la **synthèse** : le Pi 5 fait parler piper depuis le pipeline de
  conversation (VAD → whisper → LLM → TTS, voir
  [`etude-declenchement-conversation.md`](etude-declenchement-conversation.md)).

Or **les deux voix n'ont rien à voir**. Le public ne pardonne pas ça : un
personnage qui change de voix au milieu d'un échange n'est plus un personnage,
c'est un dispositif. Toute la crédibilité construite par la ventriloquie tombe
à la première réplique machine — et symétriquement, la moindre bonne réponse
de l'IA est gâchée par le fait qu'elle sort d'une autre bouche.

La question posée : *peut-on fabriquer une voix synthétique à partir de la
mienne, après les filtres ?*

## 2. État des lieux — comment la voix est réellement fabriquée

Relevé du 2026-08-26 (câblage confirmé par David) :

```
micro HF ──► récepteur HF ──► OCTAVER ──► mixette ──┐
                                                     ├──► ampli ──► châssis
Pi 5 (piper, bruitages) ─────────────────► mixette ──┘
```

Deux faits décisifs :

1. **« La voix de Didier » n'est pas la voix de David.** C'est *sa voix passée
   dans l'octaver*. Le personnage vit dans l'étage d'effet, pas dans le larynx.
   Voir [`hardware/overview.md`](hardware/overview.md) §« Echo » (l. 299, 311) :
   le châssis contient récepteur HF + octaver, et la sortie de la voix de
   l'interprète peut survenir à tout moment pendant un spectacle.
2. **Le Pi ne passe PAS par l'octaver.** Il entre en direct dans la mixette.
   C'est là, et seulement là, qu'est l'écart de timbre qu'on entend.

À noter aussi, parce que ça sert la suite : l'étage d'effet est **déjà
commutable par relais depuis le Pi** — `robot/actions/relays.py:105`
(`pitched_voice` / `normal_voice`, relais `effect`, sortie `voice_out`). La
plomberie de commande existe ; il manque le chemin audio.

Et le pipeline est déjà **half-duplex par architecture** (overview.md §297 :
Didier EST la sono, le micro n'est armé que quand Didier se tait). Donc
**ventriloquie et synthèse ne parlent jamais en même temps** — ce qui autorise
une commutation là où il faudrait sinon un mélangeur (§6).

## 3. Le principe directeur — cloner AVANT les filtres, unifier APRÈS

Réponse à la question littérale : **non, on ne clone pas la voix filtrée — et
c'est une bonne nouvelle.**

Un octaver est un processus **chaotique sur la parole** : il suit le
fondamental, donc il décroche sur les fricatives (`s`, `f`, `ch`), glisse sur
les attaques, et produit des artefacts qui ne se reproduisent pas deux fois à
l'identique. Un modèle TTS entraîné sur cette sortie apprendrait ce bruit comme
s'il était du timbre, et le restituerait **moyenné** : on perdrait exactement
le grain qui fait le personnage, tout en héritant d'un modèle plus difficile à
entraîner (données incohérentes = convergence molle).

L'architecture correcte est l'inverse :

```
David (voix sèche)  ──┐
                      ├──► MÊME étage d'effet ──► ampli ──► châssis
piper (voix clonée) ──┘
```

**La continuité ne vient pas du clonage : elle vient du dernier étage commun.**
C'est le seul endroit de la chaîne où l'identité peut être *garantie* au lieu
d'être *approchée*. Le clonage, lui, ne fait que réduire l'écart en entrée de
cet étage. Conséquence de méthode : **le lot V0 (faire passer piper par
l'octaver existant) doit précéder toute dépense de clonage**, parce qu'il est
possible que l'octaver écrase assez pour que l'écart résiduel ne s'entende pas.

## 4. Le clonage — les options, et celle qui gagne

Toutes supposent un corpus de **voix sèche** de David (§7, lot V3).

| Voie | Coût / effort | Latence | Hors-ligne | Verdict |
|---|---|---|---|---|
| **Fine-tune piper** sur la voix de David | ~1 h d'enregistrement + quelques € de GPU loué | inchangée | **oui** | **retenue** |
| Conversion de voix (RVC, seed-vc, knn-vc) | ~10 min d'audio, entraînement rapide | ajoutée, lourde | non sur Pi 5 | écartée |
| Clonage cloud (ElevenLabs, Cartesia…) | 1–3 min d'échantillon | réseau | **non** | écartée en spectacle |
| Zero-shot local (XTTS, F5, Fish…) | 30 s d'échantillon | GPU requis | non sur Pi 5 | écartée |

**Le fine-tune piper est le seul candidat compatible avec le spectacle.** Il
produit un `.onnx` qui *remplace* la voix actuelle : même code, même latence,
aucune dépendance réseau — ce qui est non négociable en déambulation de rue,
où le réseau n'existe pas. Ordre de grandeur du corpus : 45 min à 1 h de
lecture, même micro, même pièce, **aucun traitement**, segments de 3 à 10 s
avec transcriptions ; fine-tune depuis un checkpoint français existant.

Les autres voies gardent **un** usage, et un seul : le clonage cloud permet
d'**entendre en une heure**, pour quelques centimes, ce que le timbre de David
donnerait une fois cloné — donc de décider *avant* d'investir la séance
d'enregistrement. C'est un instrument de mesure, pas une brique du spectacle.

⚠️ **Licences** : si le spectacle est payant, vérifier la licence de tout
checkpoint utilisé — plusieurs modèles de clonage réputés sont diffusés en
non-commercial. Piper est permissif ; c'est un argument de plus pour lui.

## 5. L'arbitrage artistique — SUSPENDU au lot V0

Deux directions s'excluent, et le choix n'est pas technique :

- **A — rapprocher la machine de David.** On clone, Didier garde sa chair, ses
  nuances, sa chaleur. La continuité reste *approchée* : elle dépend de la
  qualité du clone et se dégrade sur les phrases longues.
- **B — éloigner les deux vers un commun robotique.** On pousse le traitement
  (vocodeur en plus de l'octaver) jusqu'à ce que la source devienne
  indifférente : humain et machine passent au même moule, la continuité est
  garantie **par construction**. Prix : Didier perd en chair.

**Décision reportée après écoute (V0).** C'est le bon ordre : la question
« combien d'écart reste-t-il après l'octaver ? » a une réponse mesurable, et
elle change l'arbitrage.

### Ce qui va mordre avant le timbre

Deux points à garder au chaud, parce qu'aucune des deux directions ne les règle :

- **La prosodie, pas le timbre.** Même clone parfait, une TTS est plate ; David
  joue. Le public lit l'intention avant la couleur. Un timbre identique sur une
  intonation morte ne fera pas illusion plus longtemps qu'un timbre différent.
  **Aucune solution retenue à ce stade** (§8).
- **La latence.** Une réponse LLM met des secondes ; la ventriloquie est
  instantanée. La rupture de *rythme* est un signal aussi fort que la rupture
  de timbre. Déjà traité en partie côté conversation (streaming par phrase,
  piper in-process) — mais c'est le même problème de continuité.

## 6. Le câblage — faire passer le Pi par l'octaver

Trois montages possibles ; le half-duplex (§2) en rend un nettement meilleur.

**Option 1 — commutateur A/B piloté par le relais existant. RECOMMANDÉE.**
Puisque les deux sources ne parlent jamais en même temps, aucun mélange n'est
nécessaire : un simple aiguillage devant l'octaver suffit, et le Pi **sait déjà
piloter des relais** (`relays.py`). L'état du commutateur devient en prime la
lecture fiable du « une source est vivante » qu'appelle overview.md l. 311.

**Option 2 — insert / départ auxiliaire de la mixette.** Si la mixette a un
insert ou un aux send + retour, on y place l'octaver et les deux voies y
passent. Avantage : adaptation de niveau gérée par la console. Inconvénient :
ça **modifie le chemin de la ventriloquie**, qui marche aujourd'hui — on
touche à l'existant qui tourne, pour servir le nouveau. À n'envisager que si
l'option 1 coince.

**Option 3 — refaire l'octaver en logiciel** sur le Pi (sox / rubberband /
LADSPA), câblage inchangé. C'est de loin le plus maintenable : réglable,
versionné, testable sans matériel. Mais ce n'est **pas le même** octaver, donc
l'égalité de timbre n'est plus garantie par construction — elle redevient un
travail d'imitation. Candidat sérieux **après** V0, pas pendant.

### Deux pièges de câblage

- **Adaptation de niveau.** L'octaver attend probablement du niveau instrument
  (il est alimenté par un récepteur HF) ; la sortie du DAC USB est du niveau
  ligne, et stéréo. Il faut sommer en mono et atténuer (pad résistif passif, ou
  boîtier de reamp). Ne pas attaquer une pédale en ligne : ça sature.
- **⚠️ Tous les sons du Pi ne doivent PAS être pitchés.** Klaxon, bruitages,
  musique doivent rester secs. Deux parades : le relais `effect` déjà en place
  (commuté par réplique), ou — plus simple et sans logique — **séparer les bus
  gauche/droite** de la sortie stéréo : voix à gauche → octaver, bruitages à
  droite → mixette en direct. Un seul câble en Y, aucune commande.

## 7. Lots V0 → V4

**V0 — banc d'écoute (atelier, aucune modification permanente).** Un câble, un
pad, la sortie du Pi dans l'entrée de l'octaver existant. Protocole :

1. **6 phrases représentatives**, choisies pour attaquer l'octaver là où il
   décroche : une salutation, une question, une réplique longue, une avec des
   chiffres, une saturée de sifflantes, une à attaques explosives (`p`/`t`/`k`).
2. Chaque phrase enregistrée **au même point** (sortie mixette) en trois
   versions : (a) David en ventriloquie, (b) piper voix 1, (c) piper voix 2 —
   **toutes post-octaver**. Normaliser en sonie avant écoute, sinon on compare
   des volumes.
3. **Le test décisif est l'alternance**, pas l'écoute isolée : monter une
   réplique où David et la machine se répondent phrase à phrase. La rupture ne
   s'entend qu'en juxtaposition — un extrait isolé passe toujours.
4. Écoute **en aveugle** par au moins deux personnes ne connaissant pas
   l'ordre, notation 1–5 sur « est-ce le même personnage ? ».
5. Consigner au §9. **C'est ce lot qui débloque l'arbitrage §5.**

**V1 — câblage permanent** (option 1 du §6) + garde-fou bruitages non pitchés.

**V2 — accordage sans clonage** : choisir la voix piper française dont la
tessiture est la plus proche de celle de David, et **pré-transposer** la sortie
piper pour qu'elle entre dans l'octaver au même F0 que la voix de David (une
ligne de `sox`/`rubberband`) — l'octaver suit le fondamental, donc à F0 égal il
décroche de la même façon sur les deux sources. V1 + V2 sont probablement
l'essentiel du résultat.

**V3 — banque de répliques enregistrées par David** (80 à 150 : accueils,
esquives, « laisse-moi réfléchir », relances). Double intérêt, et c'est ce qui
en fait le meilleur rapport effort/résultat du chantier :
- pendant la phase où l'IA répond mal, ce sont justement ces phrases
  passe-partout qui sortent le plus souvent — elles sortiront dans **la vraie
  voix**, sans aucun clonage ;
- **ce corpus EST le jeu de données du fine-tune** (V4). Un après-midi
  d'enregistrement, deux livrables. Enregistrer donc aux exigences du §4
  (voix sèche, même micro, même pièce, transcriptions).

**V4 — fine-tune piper** sur le corpus V3. À n'engager que si V0→V2 laisse un
écart audible que l'arbitrage §5 refuse d'absorber.

## 8. Points encore ouverts (assumés, pas oubliés)

- **Modèle exact de l'octaver** à relever (analogique ou numérique, niveau
  d'entrée attendu, latence) — conditionne le pad du §6 et l'option 3.
- **La mixette a-t-elle un insert / aux send ?** — conditionne l'option 2.
- **F0 moyen de la voix de ventriloquie de David** à mesurer — c'est la cible
  de la pré-transposition du lot V2.
- **La prosodie** : aucune approche retenue (§5). À rouvrir si V0 montre que le
  timbre n'est pas le facteur limitant.
- **Licences** des checkpoints si le spectacle devient payant (§4).

## 9. Journal des mesures et décisions

- **2026-08-26** — Ouverture. Câblage relevé auprès de David : HF → octaver →
  mixette ; **Pi → mixette en direct** (ne passe pas par l'octaver). Principe
  directeur arrêté (§3 : cloner avant les filtres, unifier après). Arbitrage
  artistique (§5) explicitement suspendu au lot V0.
