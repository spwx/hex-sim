from hexblade import Hexblade
from unittest.mock import patch


def test_hex_curse():
    hexblade = Hexblade(1)
    assert hexblade.crit_range == 1
    hexblade.hex_curse()
    assert hexblade.crit_range == 2


@patch("hexblade.randint")
def test_eldritch_blast(randint_mock):
    # make sure it hits
    randint_mock.return_value = 5
    hexblade = Hexblade(1)
    # should be 5 + 2 (for proficiency)
    assert hexblade._eldritch_blast(5) == 7

    # make sure it misses
    assert hexblade._eldritch_blast(4) == 7

