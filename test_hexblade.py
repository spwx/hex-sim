from hexblade import Hexblade
from unittest.mock import patch, MagicMock


def test_hex_curse():
    hexblade = Hexblade(1)
    # verify crit_range is set correctly
    assert hexblade.crit_range == 1
    # turn hex curse on
    hexblade.hex_curse()
    assert hexblade.crit_range == 2
    assert hexblade.options['curse'] == True
    # turn hex curse off
    hexblade.hex_curse(on=False)
    assert hexblade.crit_range == 1
    assert hexblade.options.get('curse', False) == False


@patch("hexblade.randint")
def test_hexed_damage(randint_mock):
    hexblade = Hexblade(1)
    randint_mock.return_value = 3
    assert hexblade.hexed_damage() == 3
    # test crit damage
    assert hexblade.hexed_damage(crit=True) == 6


@patch("hexblade.randint")
def test_eldritch_blast_damage(randint_mock):
    randint_mock.return_value = 5
    hexblade = Hexblade(1)
    # test regular damage.
    assert hexblade.eldritch_blast_damage() == 5 + 3  # 8
    # test crit damage
    assert hexblade.eldritch_blast_damage(crit=True) == 5 + 5 + 3  # 13
    # test damage with hex curse applied to target
    hexblade.hex_curse()
    assert hexblade.eldritch_blast_damage() == 5 + 3 + 2  # 10


def test_eldritch_blast_misses():
    hexblade = Hexblade(1)
    hexblade.attack_roll = MagicMock(return_value=1)
    assert hexblade.eldritch_blast(2) == 0


def test_eldritch_blast_hits():
    hexblade = Hexblade(1)
    hexblade.attack_roll = MagicMock(return_value=15)
    hexblade.eldritch_blast_damage = MagicMock(return_value=5)
    assert hexblade.eldritch_blast(15) == 5


def test_eldritch_blast_hits_with_hex():
    hexblade = Hexblade(1)
    hexblade.attack_roll = MagicMock(return_value=15)
    hexblade.eldritch_blast_damage = MagicMock(return_value=5)
    hexblade.hexed_damage = MagicMock(return_value=4)
    hexblade.hexed()
    assert hexblade.eldritch_blast(15) == 9


def test_eldritch_blast_crits():
    hexblade = Hexblade(1)
    hexblade.attack_roll = MagicMock(return_value=20)
    hexblade.eldritch_blast_damage = MagicMock(return_value=5)
    assert hexblade.eldritch_blast(15) == 5


def test_eldritch_blast_crits_with_hex():
    hexblade = Hexblade(1)
    hexblade.attack_roll = MagicMock(return_value=15)
    hexblade.eldritch_blast_damage = MagicMock(return_value=5)
    hexblade.hexed_damage = MagicMock(return_value=4)
    hexblade.hexed()
    assert hexblade.eldritch_blast(15) == 9

# @patch("hexblade.randint")
# def test_eldritch_blast(randint_mock):
#     # make sure it hits
#     randint_mock.return_value = 5
#     hexblade = Hexblade(1)
#     # should be 5 + 2 (for proficiency)
#     assert hexblade._eldritch_blast(5) == 7
#
#     # make sure it misses
#     assert hexblade._eldritch_blast(4) == 7
