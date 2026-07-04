"""Tests d'AnimationManager : temps restant (base du deadman roues) et chargement réel.

Le test de chargement construit le manager avec la vraie config et le vrai
dossier json/sequences/ : il garantit que toutes les séquences du dépôt
restent chargeables par le robot.
"""

import pytest

from dadou_utils_ros.utils.time_utils import TimeUtils
from dadou_utils_ros.utils_static import ANIMATION, DURATION
from robot.robot_config import config
from robot.sequences.animation_manager import AnimationManager

T0 = 1_000_000


@pytest.fixture
def clock(monkeypatch):
    state = {"now": T0}
    monkeypatch.setattr(TimeUtils, "current_milli_time", staticmethod(lambda: state["now"]))
    return state


@pytest.fixture
def bare_manager():
    manager = object.__new__(AnimationManager)
    manager.playing = False
    manager.duration = 0
    manager.last_time = 0
    return manager


def test_remaining_ms_zero_when_not_playing(bare_manager, clock):
    assert bare_manager.remaining_ms() == 0


def test_remaining_ms_counts_down(bare_manager, clock):
    bare_manager.playing = True
    bare_manager.duration = 30000
    bare_manager.last_time = T0

    assert bare_manager.remaining_ms() == 30000
    clock["now"] = T0 + 10000
    assert bare_manager.remaining_ms() == 20000
    clock["now"] = T0 + 40000
    assert bare_manager.remaining_ms() == 0    # jamais négatif


def test_stop_returns_animation_false(bare_manager):
    bare_manager.playing = True
    assert bare_manager.stop() == {ANIMATION: False}
    assert bare_manager.playing is False


@pytest.fixture(scope="module")
def real_manager():
    from robot.files.robot_json_manager import RobotJsonManager
    return AnimationManager(config, RobotJsonManager(config))


def test_all_repo_sequences_load(real_manager):
    assert len(real_manager.sequences_name) >= 40
    assert "moon-walk" in real_manager.sequences_name


def test_start_animation_sets_duration_and_remaining(real_manager, clock):
    real_manager.update({ANIMATION: "moon-walk"})

    assert real_manager.playing is True
    assert real_manager.duration == real_manager.sequences_name["moon-walk"][DURATION]
    clock["now"] = T0 + 5000
    assert real_manager.remaining_ms() == real_manager.duration - 5000
    real_manager.stop()
