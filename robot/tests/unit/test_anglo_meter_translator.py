"""Tests de la cinématique différentielle joystick/inclinomètre -> roues."""

import pytest

from robot.move.anglo_meter_translator import AngloMeterTranslator


@pytest.fixture
def translator():
    return AngloMeterTranslator()


def test_neutral_is_stopped(translator):
    assert translator.translate(forward=0, turn=0) == (0, 0)


def test_full_forward_and_backward(translator):
    assert translator.translate(forward=99, turn=0) == (100, 100)
    assert translator.translate(forward=-99, turn=0) == (-100, -100)


def test_half_forward_is_proportional(translator):
    assert translator.translate(forward=50, turn=0) == (50, 50)


def test_pure_turn_spins_in_place(translator):
    assert translator.translate(forward=0, turn=99) == (100, -100)
    assert translator.translate(forward=0, turn=-99) == (-100, 100)


def test_diagonal_pivots_on_one_wheel(translator):
    assert translator.translate(forward=99, turn=99) == (100, 0)


def test_output_always_bounded(translator):
    for forward in range(-99, 100, 33):
        for turn in range(-99, 100, 33):
            left, right = translator.translate(forward=forward, turn=turn)
            assert -100 <= left <= 100 and -100 <= right <= 100
