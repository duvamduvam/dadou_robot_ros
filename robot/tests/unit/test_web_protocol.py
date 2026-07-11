"""Tests du protocole pur du pont web W0 (robot_web.web_protocol).

Couvre : whitelist (garantie de sécurité W0 -- pas de roues/e_stop), parsing
des 5 types de message client, auth/écriture exclusive/heartbeat de
SessionManager (horloge injectée, jamais time.time() réel), le contenu exact
de stop_all_commands() et les constructeurs de messages serveur.
"""

import ast
import pathlib

import pytest

from robot_web import web_catalog, web_protocol
from robot_web.web_protocol import (
    HEARTBEAT_PERIOD_S, WHITELIST, WHITELIST_SPECTACLE, WHITELIST_TECHNIQUE,
    WRITE_TIMEOUT_S, ProtocolError, SessionManager, build_ack, build_err,
    build_hb_ack, build_hello, build_state, mode_from_domain_id,
    parse_client_message, stop_all_commands,
)


def imported_roots(module):
    """Racines des paquets réellement importés par un module (via son AST).
    Même motif que test_wheels_payload.py : robot_web doit rester un paquet
    autonome, importable dans le conteneur sim sans rclpy ni dadou_utils_ros."""
    tree = ast.parse(pathlib.Path(module.__file__).read_text())
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


# --- Autonomie (garde-fou AST) ----------------------------------------------

def test_web_protocol_reste_autonome():
    roots = imported_roots(web_protocol)
    assert roots.isdisjoint(("rclpy", "aiohttp", "dadou_utils_ros", "robot")), roots


def test_web_catalog_reste_autonome():
    roots = imported_roots(web_catalog)
    assert roots.isdisjoint(("rclpy", "aiohttp", "dadou_utils_ros", "robot")), roots


# --- Whitelist : contrat de sécurité W0 -------------------------------------

def test_whitelist_n_expose_jamais_les_roues_ni_e_stop():
    """W0 = supervision + contenus + panneau technique. AUCUN accès roues ni
    verrou e_stop -- vérifié explicitement, pas juste "absent par hasard"."""
    interdits = {"wheels", "cmd_vel", "cmd_vel_web", "cmd_vel_remote", "cmd_vel_anim",
                 "cmd_vel_mux", "e_stop"}
    assert interdits.isdisjoint(WHITELIST)


def test_whitelist_est_l_union_spectacle_technique():
    assert WHITELIST == WHITELIST_SPECTACLE | WHITELIST_TECHNIQUE
    assert WHITELIST_SPECTACLE == {"animation", "face", "audio", "robot_lights"}
    assert WHITELIST_TECHNIQUE == {"relay", "neck", "left_eye", "right_eye", "left_arm",
                                    "right_arm", "gaze", "system"}


# --- Parsing des messages client --------------------------------------------

def test_parse_auth_token_present():
    assert parse_client_message('{"type":"auth","token":"secret"}') == {
        "type": "auth", "token": "secret"}


def test_parse_auth_token_null():
    assert parse_client_message('{"type":"auth","token":null}') == {
        "type": "auth", "token": None}


def test_parse_auth_token_invalide_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"type":"auth","token":42}')


def test_parse_hb():
    assert parse_client_message('{"type":"hb","t":1234}') == {"type": "hb", "t": 1234}


def test_parse_hb_sans_t_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"type":"hb"}')


def test_parse_hb_t_booleen_refuse():
    """bool est une sous-classe d'int en Python : un horodatage True/False
    n'a pas de sens, on doit le rejeter explicitement (pas de faux positif)."""
    with pytest.raises(ProtocolError):
        parse_client_message('{"type":"hb","t":true}')


def test_parse_cmd_valide():
    assert parse_client_message('{"type":"cmd","topic":"face","value":"joie","time":500}') == {
        "type": "cmd", "topic": "face", "value": "joie", "time": 500}


def test_parse_cmd_time_defaut_zero():
    assert parse_client_message('{"type":"cmd","topic":"face","value":"joie"}')["time"] == 0


def test_parse_cmd_value_quelconque():
    """value est du JSON quelconque : objet, booléen, null, nombre..."""
    assert parse_client_message('{"type":"cmd","topic":"robot_lights","value":{"brightness":0.2}}'
                                 )["value"] == {"brightness": 0.2}
    assert parse_client_message('{"type":"cmd","topic":"animation","value":false}')["value"] is False


@pytest.mark.parametrize("time_ms", [-1, 2 ** 63])
def test_parse_cmd_time_hors_bornes_leve(time_ms):
    """StringTime.time est un int64 : hors bornes, rclpy lèverait à
    l'affectation dans le node et tuerait la connexion du client au lieu d'un
    refus propre. Négatif refusé aussi (time = durée ms, jamais négative)."""
    with pytest.raises(ProtocolError):
        parse_client_message(
            '{{"type":"cmd","topic":"face","value":"joie","time":{}}}'.format(time_ms))


def test_parse_cmd_sans_value_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"type":"cmd","topic":"face"}')


def test_parse_cmd_topic_hors_whitelist_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"type":"cmd","topic":"inconnu","value":1}')


@pytest.mark.parametrize("topic", ["wheels", "cmd_vel_web", "cmd_vel", "e_stop",
                                    "cmd_vel_remote", "cmd_vel_anim"])
def test_parse_cmd_roues_et_e_stop_toujours_refuses(topic):
    """Vérification EXPLICITE demandée par la spec : ces topics ne doivent
    jamais être acceptés par le pont web W0, quelle que soit la valeur envoyée."""
    with pytest.raises(ProtocolError):
        parse_client_message('{{"type":"cmd","topic":"{}","value":[0.5,0.5]}}'.format(topic))


def test_parse_take_control():
    assert parse_client_message('{"type":"take_control"}') == {"type": "take_control"}


def test_parse_stop_all():
    assert parse_client_message('{"type":"stop_all"}') == {"type": "stop_all"}


def test_parse_json_casse_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"type": "cmd", ')


def test_parse_non_objet_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('[1, 2, 3]')


def test_parse_type_manquant_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"topic":"face","value":"joie"}')


def test_parse_type_inconnu_leve():
    with pytest.raises(ProtocolError):
        parse_client_message('{"type":"boum"}')


# --- stop_all_commands : liste et ordre exacts ------------------------------

def test_stop_all_commands_liste_et_ordre_exacts():
    assert stop_all_commands() == [
        ("animation", False),
        ("audio", "stop"),
        ("face", "stop"),
        ("neck", "stop"),
        ("left_eye", "stop"),
        ("right_eye", "stop"),
        ("left_arm", "stop"),
        ("right_arm", "stop"),
    ]


def test_stop_all_commands_ne_touche_jamais_aux_roues():
    topics = {topic for topic, _value in stop_all_commands()}
    assert "wheels" not in topics
    assert "e_stop" not in topics


# --- Mode robot / sim --------------------------------------------------------

def test_mode_from_domain_id_simulation():
    assert mode_from_domain_id(43) == "SIMULATION"


def test_mode_from_domain_id_robot_reel():
    assert mode_from_domain_id(42) == "ROBOT RÉEL"


@pytest.mark.parametrize("domain_id", [0, 1, -1, 99])
def test_mode_from_domain_id_inconnu(domain_id):
    assert mode_from_domain_id(domain_id) == "INCONNU"


# --- Constructeurs de messages serveur --------------------------------------

def test_build_hello():
    assert build_hello(43, writer=True, token_required=False) == {
        "type": "hello", "domain_id": 43, "mode": "SIMULATION",
        "writer": True, "token_required": False}


def test_build_hb_ack_echo_t():
    assert build_hb_ack(999) == {"type": "hb_ack", "t": 999}


def test_build_ack():
    assert build_ack("face") == {"type": "ack", "topic": "face"}


def test_build_err():
    assert build_err("topic hors whitelist") == {"type": "err", "reason": "topic hors whitelist"}


def test_build_state():
    assert build_state(topics={"face": {"msg": "joie", "age_s": 0.4}}, nodes=["lights_node"],
                        clients=2, writer_present=True) == {
        "type": "state",
        "topics": {"face": {"msg": "joie", "age_s": 0.4}},
        "nodes": ["lights_node"],
        "clients": 2,
        "writer_present": True,
    }


# --- SessionManager : auth ---------------------------------------------------

def test_auth_libre_quand_token_serveur_vide():
    sessions = SessionManager(token=None)
    assert sessions.token_required is False
    assert sessions.authenticate("c1", token=None, now_s=0.0) is True
    assert sessions.authenticate("c2", token="n'importe quoi", now_s=0.0) is True


def test_auth_avec_bon_token():
    sessions = SessionManager(token="secret")
    assert sessions.token_required is True
    assert sessions.authenticate("c1", token="secret", now_s=0.0) is True


def test_auth_avec_mauvais_token_rejetee():
    sessions = SessionManager(token="secret")
    assert sessions.authenticate("c1", token="faux", now_s=0.0) is False
    assert sessions.is_writer("c1") is False


# --- SessionManager : écriture exclusive ------------------------------------

def test_premier_client_authentifie_prend_l_ecriture():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    assert sessions.is_writer("c1") is True
    assert sessions.writer_present() is True


def test_second_client_est_lecteur():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    sessions.authenticate("c2", None, now_s=0.0)
    assert sessions.is_writer("c1") is True
    assert sessions.is_writer("c2") is False


def test_take_control_reprend_l_ecriture_explicitement():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    sessions.authenticate("c2", None, now_s=0.0)
    assert sessions.take_control("c2", now_s=1.0) is True
    assert sessions.is_writer("c2") is True
    assert sessions.is_writer("c1") is False


def test_take_control_refuse_si_non_authentifie():
    sessions = SessionManager(token="secret")
    assert sessions.take_control("inconnu", now_s=0.0) is False


def test_deconnexion_du_writer_libere_l_ecriture_sans_reprise_automatique():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    sessions.authenticate("c2", None, now_s=0.0)
    was_writer = sessions.remove_client("c1")
    assert was_writer is True
    assert sessions.writer_present() is False
    # c2 était lecteur, il ne récupère PAS l'écriture automatiquement.
    assert sessions.is_writer("c2") is False


def test_deconnexion_d_un_lecteur_ne_touche_pas_l_ecriture():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    sessions.authenticate("c2", None, now_s=0.0)
    was_writer = sessions.remove_client("c2")
    assert was_writer is False
    assert sessions.is_writer("c1") is True


# --- SessionManager : heartbeat / timeout -----------------------------------

def test_heartbeat_rearme_l_horloge_writer():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    assert sessions.heartbeat("c1", now_s=2.0) is True
    # Juste avant le timeout depuis le dernier battement (2.0 + 2.9 < 2.0 + WRITE_TIMEOUT_S) :
    assert sessions.check_timeouts(now_s=2.0 + WRITE_TIMEOUT_S - 0.1) is None
    assert sessions.is_writer("c1") is True


def test_heartbeat_ignore_pour_un_non_writer():
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    sessions.authenticate("c2", None, now_s=0.0)
    assert sessions.heartbeat("c2", now_s=1.0) is False


def test_timeout_libere_l_ecriture_horloge_avancee_a_la_main():
    """Le coeur du test : aucune horloge réelle, on avance now_s à la main."""
    sessions = SessionManager(token=None)
    sessions.authenticate("c1", None, now_s=0.0)
    assert sessions.is_writer("c1") is True

    # Silence total au-delà de WRITE_TIMEOUT_S depuis l'auth (qui arme l'horloge) :
    released = sessions.check_timeouts(now_s=WRITE_TIMEOUT_S + 0.01)
    assert released == "c1"
    assert sessions.writer_present() is False
    assert sessions.is_writer("c1") is False


def test_timeout_ne_libere_rien_si_pas_de_writer():
    sessions = SessionManager(token=None)
    assert sessions.check_timeouts(now_s=1000.0) is None


def test_constante_heartbeat_period_inferieure_au_timeout():
    """Sanity check du couple de constantes exportées : le client doit battre
    plusieurs fois avant expiration, sinon la moindre latence réseau ferait
    perdre l'écriture en continu."""
    assert HEARTBEAT_PERIOD_S < WRITE_TIMEOUT_S
