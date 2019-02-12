from hexblade import Hexblade

def test_additional_damage_on_hit(mocker):
    hexblade = Hexblade(1)
    assert hexblade.additional_damage_on_hit() == 0
    # test with hex, bestow curse, hex curse
    hexblade.hexed_damage = mocker.MagicMock(return_value=5)
    hexblade.bestow_curse_damage = mocker.MagicMock(return_value=5)
    hexblade.hexed()
    hexblade.bestow_curse()
    hexblade.hex_curse()
    # hexed (5) + bestow curse (5) + proficiency (2)
    assert hexblade.additional_damage_on_hit() == 12



def test_hex_curse():
    hexblade = Hexblade(1)
    # verify crit_range is set correctly
    assert hexblade.crit_range == 1
    # turn hex curse on
    hexblade.hex_curse()
    assert hexblade.crit_range == 2
    assert hexblade.options['curse'] is True
    # turn hex curse off
    hexblade.hex_curse(on=False)
    assert hexblade.crit_range == 1
    assert hexblade.options.get('curse', False) is False


def test_hexed_damage(mocker):
    hexblade = Hexblade(1)
    mocker.patch('hexblade.randint', return_value=3)
    assert hexblade.hexed_damage() == 3
    # test crit damage
    assert hexblade.hexed_damage(crit=True) == 6


def test_eldritch_blast_damage(mocker):
    hexblade = Hexblade(1)
    mocker.patch('hexblade.randint', return_value=5)
    # test regular damage.
    assert hexblade.eldritch_blast_damage() == 5 + 3  # 8
    # test crit damage
    assert hexblade.eldritch_blast_damage(crit=True) == 5 + 5 + 3  # 13


def test_eldritch_blast_misses(mocker):
    hexblade = Hexblade(1)
    hexblade.attack_roll = mocker.MagicMock(return_value=(1, False))
    assert hexblade.eldritch_blast(2) == 0


def test_eldritch_blast_hits(mocker):
    hexblade = Hexblade(1)
    hexblade.attack_roll = mocker.MagicMock(return_value=(15, False))
    mocker.patch('hexblade.randint', return_value=5)
    # roll + stat bonus
    assert hexblade.eldritch_blast(15) == 5 + 3


def test_eldritch_blast_crits(mocker):
    hexblade = Hexblade(1)
    mocker.patch('hexblade.randint', return_value=5)
    hexblade.attack_roll = mocker.MagicMock(return_value=(20, True))
    # damage dice (5 + 5) + stat bonus (3)
    assert hexblade.eldritch_blast(15) == 13


def test_eldritch_blast_level_17(mocker):
    hexblade = Hexblade(17)
    hexblade.attack_roll = mocker.MagicMock(return_value=(15, False))
    mocker.patch('hexblade.randint', return_value=5)
    # damage dice x4 (5, 5, 5, 5) + stat bonus x4 (5, 5, 5, 5)
    assert hexblade.eldritch_blast(15) == 40


def test_spiritual_weapon_level_1():
    hexblade = Hexblade(1)
    assert hexblade.spiritual_weapon(15) == 0


def test_spiritual_weapon_level_5(mocker):
    mocker.patch('hexblade.randint', return_value=5)
    hexblade = Hexblade(5)
    hexblade.attack_roll = mocker.MagicMock(return_value=(15, False))
    assert hexblade.spiritual_weapon(14) == 5 + 4  # 9


def test_spiritual_weapon_level_10(mocker):
    mocker.patch("hexblade.randint", return_value=5)
    hexblade = Hexblade(10)
    hexblade.attack_roll = mocker.MagicMock(return_value=(15, False))
    assert hexblade.spiritual_weapon(14) == 5 + 5 + 5  # 14


def test_spiritual_weapon_level_5_crit(mocker):
    hexblade = Hexblade(5)
    mocker.patch("hexblade.randint", return_value=5)
    hexblade.attack_roll = mocker.MagicMock(return_value=(20, True))
    assert hexblade.spiritual_weapon(14) == 5 + 5 + 4  # 14


def test_spiritual_weapon_level_10_crit(mocker):
    hexblade = Hexblade(10)
    mocker.patch("hexblade.randint", return_value=5)
    hexblade.attack_roll = mocker.MagicMock(return_value=(20, True))
    assert hexblade.spiritual_weapon(14) == 5 + 5 + 5 + 5 + 5  # 25


def test_spiritual_weapon_level_10_with_curse(mocker):
    hexblade = Hexblade(10)
    hexblade.hex_curse()
    mocker.patch("hexblade.randint", return_value=5)
    hexblade.attack_roll = mocker.MagicMock(return_value=(20, True))
    # 4d8 damage die + prof + spell ability modifier
    assert hexblade.spiritual_weapon(14) == 5 + 5 + 5 + 5 + 5 + 4  # 29


def test_spiritual_weapon_level_10_with_hex(mocker):
    hexblade = Hexblade(10)
    hexblade.hexed()
    mocker.patch("hexblade.randint", return_value=5)
    hexblade.attack_roll = mocker.MagicMock(return_value=(15, False))
    assert hexblade.spiritual_weapon(14) == 5 + 5 + 5 + 5  # 25
