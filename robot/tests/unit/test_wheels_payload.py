"""Tests du parsing pur du payload roues (robot_drive.wheels_payload).

Couvre toutes les formes acceptées par la branche WHEELS de
robot/actions/wheels.py (voir wheels_payload.py pour la correspondance).
"""

from dadou_utils_ros.utils_static import ANIMATION, BACKWARD, FORWARD, LEFT, RIGHT, SPEED, STOP, WHEELS
from robot_drive.wheels_payload import payload_to_pair


def test_no_wheels_key_returns_none():
    assert payload_to_pair({}) is None
    assert payload_to_pair({ANIMATION: True}) is None


def test_stop():
    assert payload_to_pair({WHEELS: STOP}) == STOP


def test_dict_left_right_is_converted_from_percent():
    assert payload_to_pair({WHEELS: {LEFT: 50, RIGHT: -100}}) == (0.5, -1.0)
    assert payload_to_pair({WHEELS: {LEFT: 0, RIGHT: 0}}) == (0.0, 0.0)


def test_pair_list_used_as_is():
    assert payload_to_pair({WHEELS: [0.3, -0.4]}) == (0.3, -0.4)
    assert payload_to_pair({WHEELS: (0.3, -0.4)}) == (0.3, -0.4)


def test_pair_list_is_clamped_to_unit_range():
    assert payload_to_pair({WHEELS: [2.0, -3.0]}) == (1.0, -1.0)


def test_string_forward():
    assert payload_to_pair({WHEELS: FORWARD}) == (0.5, 0.5)


def test_string_backward():
    assert payload_to_pair({WHEELS: BACKWARD}) == (-0.5, -0.5)


def test_string_left():
    assert payload_to_pair({WHEELS: LEFT}) == (-0.5, 0.5)


def test_string_right():
    assert payload_to_pair({WHEELS: RIGHT}) == (0.5, -0.5)


def test_speed_key_returns_none():
    assert payload_to_pair({WHEELS: {SPEED: 80}}) is None


def test_unrecognized_form_returns_none():
    assert payload_to_pair({WHEELS: {"unknown": 1}}) is None
    assert payload_to_pair({WHEELS: 42}) is None
    assert payload_to_pair({WHEELS: [0.1, 0.2, 0.3]}) is None


def test_constantes_alignees_avec_utils_static():
    """Anti-dérive : les constantes du protocole sont dupliquées dans
    robot_drive (autonomie du conteneur sim, qui n'a pas dadou_utils_ros) ;
    elles doivent rester identiques aux originales."""
    from dadou_utils_ros import utils_static
    from robot_drive import wheels_payload
    for name in ("WHEELS", "STOP", "FORWARD", "BACKWARD", "LEFT", "RIGHT", "SPEED"):
        assert getattr(wheels_payload, name) == getattr(utils_static, name), name
