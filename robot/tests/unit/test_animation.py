"""Tests de la logique de timing d'Animation (robot/sequences/animation.py).

L'horloge est contrôlée en remplaçant TimeUtils.current_milli_time, dont
dépendent à la fois Animation et TimeUtils.is_time.
"""

import pytest

from dadou_utils_ros.utils.time_utils import TimeUtils
from robot.sequences.animation import Animation

T0 = 1_000_000


@pytest.fixture
def clock(monkeypatch):
    state = {"now": T0}
    monkeypatch.setattr(TimeUtils, "current_milli_time", staticmethod(lambda: state["now"]))
    return state


def test_keyframes_fire_at_fraction_of_duration(clock):
    animation = Animation({"neck": [[0, 0.1], [0.5, 0.9], [1, 0.5]]}, 1000, "neck")

    assert animation.next() is None            # t=0 : le seuil est strictement dépassé, pas encore
    clock["now"] = T0 + 1
    assert animation.next() == 0.1             # premier keyframe (départ immédiat)
    clock["now"] = T0 + 400
    assert animation.next() is None            # avant 50% de 1000 ms
    clock["now"] = T0 + 502
    assert animation.next() == 0.9             # keyframe à 50%
    clock["now"] = T0 + 1002
    assert animation.next() == 0.5             # keyframe final à 100%
    clock["now"] = T0 + 2000
    assert animation.next() is None            # plus rien après le dernier


def test_first_keyframe_waits_for_start_delay(clock):
    animation = Animation({"neck": [[0.5, 0.9]]}, 1000, "neck")

    clock["now"] = T0 + 100
    assert animation.next() is None            # 0.5 * 1000 ms pas encore atteint
    clock["now"] = T0 + 501
    assert animation.next() == 0.9
    clock["now"] = T0 + 5000
    assert animation.next() is None            # piste épuisée


def test_empty_track_has_no_data(clock):
    assert Animation({}, 1000, "neck").has_data is False
    assert Animation({"neck": []}, 1000, "neck").has_data is False
    assert Animation({"wheels": [[0, [0.5, 0.5]]]}, 1000, "neck").has_data is False


def test_wheels_values_pass_through(clock):
    animation = Animation({"wheels": [[0, [0.6, -0.6]], [1, [0, 0]]]}, 30000, "wheels")

    clock["now"] = T0 + 1
    assert animation.next() == [0.6, -0.6]
    clock["now"] = T0 + 30001
    assert animation.next() == [0, 0]
