"""La chaîne de sécurité matérielle contre le VRAI code Wheels.

Ces tests branchent le code de production Wheels (injection pca9685, comme
test_wheels.py) sur le modèle de la carte main-carrier (safety_chain_model).
Ils prouvent, avant que le cuivre n'existe, les deux scénarios que le deadman
logiciel 400 ms ne peut PAS couvrir :

  1. wheels_node meurt (crash, conteneur tué) → plus personne n'écrit sur le
     bus, le PCA9685 GARDE sa dernière consigne, les roues continuent ;
  2. le bus I2C se fige → stop() lève, l'écriture n'arrive jamais, idem.

Dans les deux cas le deadman logiciel croit avoir freiné et n'a rien freiné.
Seule la coupure MATÉRIELLE (OE) rattrape — c'est ce que ces tests vérifient.

LE CONTRAT LOGICIEL fixé ici (le futur node devra l'implémenter tel quel) :
  - l'impulsion HEARTBEAT (GPIO26) n'est émise qu'APRÈS une écriture I2C
    RÉUSSIE — jamais avant, jamais sur échec (voir drive() et try_stop()) ;
  - au réarmement, remettre les registres à zéro AVANT d'appuyer sur ARM,
    sinon les roues repartent à l'ancienne vitesse (test dédié plus bas).

Convention de lecture :
  - ``.duty_cycle``  = le registre de la puce (ce que le logiciel croit) ;
  - ``.output``      = la broche physique (ce que le SmartDrive reçoit).
La différence entre les deux EST le sujet de ce fichier.
"""

import pytest

from dadou_utils_ros.utils.time_utils import TimeUtils
from robot.robot_config import config
from robot.actions.wheels import Wheels

from robot.tests.unit.safety_chain_model import FakePca9685, I2cBusHungError, SafetyChain

T0 = 1_000_000


@pytest.fixture
def clock(monkeypatch):
    state = {"now": T0}
    monkeypatch.setattr(TimeUtils, "current_milli_time", staticmethod(lambda: state["now"]))
    return state


@pytest.fixture
def rig(clock):
    """Le banc complet : la puce, la carte, et le vrai code Wheels branché dessus."""
    pca = FakePca9685()
    chain = SafetyChain(pca)
    wheels = Wheels(config, pca9685=pca)
    return pca, chain, wheels


def outputs(wheels):
    """Ce que le SmartDrive reçoit VRAIMENT (broches physiques, hors bus I2C)."""
    return wheels.left_pwm.output, wheels.right_pwm.output


def moving_physically(wheels):
    return any(v > 0 for v in outputs(wheels))


# --------------------------------------------------------------------------
# Le contrat logiciel, encodé en 8 lignes : impulsion APRÈS écriture réussie.
# Le futur wheels_node devra faire exactement cela — ces helpers SONT sa spec.
# --------------------------------------------------------------------------

def drive(wheels, chain, linear_x, angular_z):
    try:
        wheels.apply_twist(linear_x, angular_z)
    except OSError:
        return  # écriture ratée -> PAS d'impulsion : le watchdog doit tomber
    chain.heartbeat()


def try_stop(wheels, chain):
    try:
        wheels.stop()
    except OSError:
        return
    chain.heartbeat()


# --------------------------------------------------------------------------
# 1. États de départ et réarmement — la bascule D et son /CLR dominant
# --------------------------------------------------------------------------

def test_mise_sous_tension_desarmee(rig):
    """À la mise sous tension, la chaîne est désarmée : Didier ne peut pas
    partir tout seul, même si le logiciel démarre et écrit du PWM."""
    pca, chain, wheels = rig
    assert not chain.wheels_enabled

    # Le logiciel écrit une consigne (bug, replay, n'importe quoi) : le
    # registre la prend, la broche physique reste à zéro.
    drive(wheels, chain, 0.5, 0.0)
    assert wheels.left_pwm.duty_cycle > 0     # le registre a la consigne...
    assert not moving_physically(wheels)      # ...mais les roues ne bougent pas


def test_armement_exige_battement_prealable(rig):
    """ARM sans battement = rien : SAFE est bas, le /CLR tient la bascule."""
    pca, chain, wheels = rig
    chain.press_arm()
    assert not chain.wheels_enabled


def test_arm_maintenu_ne_force_pas_le_rearmement(rig, clock):
    """LE test de la bascule D : maintenir ARM enfoncé pendant que la chaîne
    est en défaut ne doit PAS produire un réarmement quand le défaut cesse.
    (C'est la raison d'être du /CLR asynchrone DOMINANT — un simple relais
    auto-maintenu ou une porte ET n'auraient pas cette propriété.)"""
    pca, chain, wheels = rig

    # Battement mort, l'utilisateur s'acharne sur ARM :
    for _ in range(10):
        chain.press_arm()
        assert not chain.wheels_enabled

    # Le battement revient PENDANT que le doigt est resté sur le bouton :
    # pas de nouveau front d'horloge -> toujours désarmé.
    chain.heartbeat()
    assert not chain.wheels_enabled

    # Il faut un VRAI nouvel appui, battement établi :
    chain.press_arm()
    assert chain.wheels_enabled


def test_marche_normale(rig, clock):
    """Vérification de non-nuisance : en fonctionnement nominal (battement à
    chaque écriture, ~20 Hz > période 250 ms du monostable), la chaîne ne
    gêne jamais la conduite."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()

    for step in range(1, 41):                 # 2 s de conduite à 20 Hz
        clock["now"] = T0 + step * 50
        drive(wheels, chain, 0.5, 0.0)
        assert moving_physically(wheels)

    try_stop(wheels, chain)
    assert not moving_physically(wheels)
    assert chain.wheels_enabled               # arrêt volontaire ≠ défaut


# --------------------------------------------------------------------------
# 2. Les deux scénarios que le deadman logiciel ne couvre pas
# --------------------------------------------------------------------------

def test_mort_du_node_coupe_les_roues_registres_intacts(rig, clock):
    """wheels_node meurt en plein mouvement : plus d'écriture, plus de
    battement. Le deadman logiciel 400 ms n'existe plus (le process est
    mort). 250 ms plus tard le monostable tombe, OE monte, les roues
    s'arrêtent — ALORS QUE les registres tiennent toujours l'ancien PWM."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.5, 0.0)
    assert moving_physically(wheels)

    # Le node meurt ici : plus AUCUN appel logiciel à partir de maintenant.
    clock["now"] = T0 + chain.watchdog.PERIOD_MS - 1
    assert moving_physically(wheels)          # juste avant l'échéance : ça roule

    clock["now"] = T0 + chain.watchdog.PERIOD_MS + 1
    assert not moving_physically(wheels)      # le matériel a coupé

    # LA preuve que le logiciel seul ne suffisait pas : le registre de la
    # puce contient TOUJOURS la consigne de marche. Sans OE, le SmartDrive
    # la recevrait encore.
    assert wheels.left_pwm.duty_cycle > 0


def test_bus_i2c_fige_stop_leve_le_materiel_rattrape(rig, clock):
    """Le bus I2C se fige en plein mouvement : stop() LÈVE, l'écriture
    n'arrive jamais, la puce garde sa consigne. Le contrat « impulsion
    seulement après écriture réussie » fait tomber le watchdog — c'est LE
    test qui justifie ce contrat (une impulsion émise avant l'écriture
    entretiendrait le battement d'un node qui n'écrit plus rien)."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.5, 0.0)
    assert moving_physically(wheels)

    pca.hang()                                # SDA bloqué bas, la puce ne répond plus

    # Le node est VIVANT et essaie honnêtement de s'arrêter : ça échoue.
    with pytest.raises(I2cBusHungError):
        wheels.stop()
    # (try_stop, lui, avale l'erreur et n'impulse pas — même effet :)
    try_stop(wheels, chain)

    # Le node continue de tourner et de tenter des écritures : aucune ne
    # réussit, donc aucune impulsion, donc le monostable expire.
    clock["now"] = T0 + chain.watchdog.PERIOD_MS + 1
    drive(wheels, chain, 0.0, 0.0)            # tentative d'arrêt encore : échec silencieux
    assert not moving_physically(wheels)      # OE a coupé, malgré le bus mort


# --------------------------------------------------------------------------
# 3. Le coup-de-poing — catégorie 0, purement électromécanique
# --------------------------------------------------------------------------

def test_coup_de_poing_coupe_tout_immediatement(rig, clock):
    """Appui : le relais 40 A lâche (puissance coupée) ET la logique tombe
    (SAFE bas -> /CLR -> OE haut). Immédiat — pas d'attente des 250 ms du
    monostable, pas de logiciel dans la boucle."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.8, 0.0)

    chain.press_estop()                       # même milliseconde :
    assert not chain.relay_closed             # la puissance moteurs est morte
    assert not moving_physically(wheels)      # et la commande aussi (défense en profondeur)


def test_relacher_le_coup_de_poing_ne_rearme_pas(rig, clock):
    """Tourner/relâcher le champignon rend la chaîne READY, pas RUN : il faut
    un appui ARM délibéré. Personne ne redémarre 50 kg par inadvertance."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.5, 0.0)
    chain.press_estop()
    chain.release_estop()

    assert chain.relay_closed                 # la puissance est revenue...
    assert not chain.wheels_enabled           # ...mais les roues restent interdites

    chain.heartbeat()
    chain.press_arm()
    assert chain.wheels_enabled               # réarmement : geste explicite seulement


# --------------------------------------------------------------------------
# 4. Le piège du réarmement — pourquoi le node devra remettre à zéro d'abord
# --------------------------------------------------------------------------

def test_reprise_du_battement_seule_ne_redemarre_pas(rig, clock):
    """Après une chute (node mort puis relancé) : le battement revient, mais
    la bascule reste tombée tant qu'ARM n'est pas pressé. C'est CE test qui
    prouve que le monostable seul ne suffisait pas : sans la bascule, le
    retour du battement ré-abaisserait OE et rejouerait le registre périmé."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.7, 0.0)

    clock["now"] = T0 + chain.watchdog.PERIOD_MS + 1   # le node meurt, la chaîne tombe
    assert not moving_physically(wheels)
    assert wheels.left_pwm.duty_cycle > 0     # ...registre encore chargé (le danger)

    # systemd/docker relance le node : le battement repart.
    clock["now"] = T0 + 5_000
    chain.heartbeat()
    clock["now"] = T0 + 5_050
    chain.heartbeat()

    assert not moving_physically(wheels)      # la bascule tient : toujours coupé


def test_rearmement_sans_remise_a_zero_rejoue_l_ancien_pwm(rig, clock):
    """LE PIÈGE, documenté en test : si on appuie sur ARM alors que les
    registres tiennent encore l'ancienne consigne, les roues REPARTENT à
    l'ancienne vitesse à l'instant du réarmement. Exigence de conception
    pour le futur node : écrire stop() (registres à zéro) AVANT de déclarer
    la reprise possible. La procédure sûre est testée juste en dessous."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.7, 0.0)
    stale = wheels.left_pwm.duty_cycle

    clock["now"] = T0 + chain.watchdog.PERIOD_MS + 1   # chute, registres chargés
    assert not moving_physically(wheels)

    # Réarmement NAÏF : battement + ARM, sans nettoyage.
    chain.heartbeat()
    chain.press_arm()
    assert wheels.left_pwm.output == stale    # les roues repartent seules : INTERDIT


def test_procedure_de_rearmement_sure(rig, clock):
    """La procédure que le node devra suivre : stop() d'abord (registres à
    zéro, battement au passage), ARM ensuite. Aucun mouvement au réarmement."""
    pca, chain, wheels = rig
    chain.heartbeat()
    chain.press_arm()
    drive(wheels, chain, 0.7, 0.0)

    clock["now"] = T0 + chain.watchdog.PERIOD_MS + 1   # chute
    assert not moving_physically(wheels)

    try_stop(wheels, chain)                   # 1. nettoyer les registres (+ impulsion)
    chain.press_arm()                         # 2. réarmer
    assert chain.wheels_enabled
    assert not moving_physically(wheels)      # zéro mouvement : réarmement sûr
