from random import randint


class Character:
    def __init__(self, level, advantage=0, ability_modifier=0, crit_range=1):
        self.level = level
        self.advantage = advantage
        self.ability_modifier = ability_modifier
        self.crit_range = crit_range
        self.options = {}

        if level >= 17:
            self.proficiency = 6
        elif level >= 13:
            self.proficiency = 5
        elif level >= 9:
            self.proficiency = 4
        elif level >= 5:
            self.proficiency = 3
        else:
            self.proficiency = 2

        if level >= 8:
            self.stat_bonus = 5
        elif level >= 4:
            self.stat_bonus = 4
        else:
            self.stat_bonus = 3

    def attack_roll(self, add_proficiency=True):
        if self.advantage == 1:
            roll = max(randint(1, 20), randint(1, 20))
        elif self.advantage == 2:
            roll = max(randint(1, 20), randint(1, 20), randint(1, 20))
        else:
            roll = randint(1, 20)

        if add_proficiency:
            return roll + self.proficiency + self.stat_bonus
        else:
            return roll

    def is_crit(self, roll):
        if roll >= 20 - self.crit_range:
            return True
        return False

    def is_hit(self, roll, ac):
        if roll >= ac:
            return True
        else:
            return False


class Hexblade(Character):
    def hex_curse(self, on=True):
        if on:
            self.crit_range = 2
            self.options["curse"] = True
        else:
            self.crit_range = 1
            self.options.pop("curse", None)

    def hexed(self, on=True):
        if on:
            self.options["hexed"] = True
        else:
            self.options.pop("hexed", None)

    def hexed_damage(self, crit=False):
        if crit:
            return randint(1, 6) + randint(1, 6)
        return randint(1, 6)

    def eldritch_blast_damage(self, crit=False):
        damage = randint(1, 10) + self.stat_bonus
        if crit:
            damage += randint(1, 10)

        if self.options.get("curse", False):
            damage += self.proficiency

        return damage

    def eldritch_blast(self, ac):

        # add blasts at level 5, 11, 17
        if self.level >= 17:
            blasts = 4
        elif self.level >= 11:
            blasts = 3
        elif self.level >= 5:
            blasts = 2
        else:
            blasts = 1

        damage = 0
        for blast in range(blasts):
            attack_roll = self.attack_roll()

            if self.is_crit(attack_roll):
                damage += self.eldritch_blast_damage(crit=True)
                if self.options.get("hexed", False):
                    damage += self.hexed_damage(crit=True)

            elif attack_roll >= ac:
                damage += self.eldritch_blast_damage(ac)
                if self.options.get("hexed", False):
                    damage += self.hexed_damage()
        return damage

    def spiritual_weapon(self, ac):
        if self.level >= 10:
            d8s = 2
        elif self.level >= 5:
            d8s = 1
        else:
            return 0

        roll = self.attack_roll()

        if roll < ac:
            return 0

        damage = 0
        for dice in range(d8s):
            damage += randint(1, 8)

        if self.is_crit(roll):
            for dice in range(d8s):
                damage += randint(1, 8)

        damage += self.stat_bonus

        if self.options.get("curse", False):
            damage += self.proficiency

        if self.options.get("hexed", False):
            if self.is_crit(roll):
                damage += self.hexed_damage(crit=True)
            else:
                damage += self.hexed_damage()

        return damage


def attack(
        level, ac, hexed=False, darkness=False, cursed=False, spiritual_weapon=False
):
    hexblade = Hexblade(level)
    if cursed:
        hexblade.hex_curse()
    if darkness:
        hexblade.advantage = 2
    if hexed:
        hexblade.hexed()

    damage = 0
    for attack_round in range(100_000):
        if spiritual_weapon:
            damage += hexblade.spiritual_weapon(ac)
        if hexed:
            damage += hexblade.eldritch_blast(ac)
        else:
            damage += hexblade.eldritch_blast(ac)
    return damage / 100_000


def run_trials():
    levels = [3, 5, 9, 13, 17]
    ac = 20

    for level in levels:
        print(f"level: {level}")

        damage = attack(level, ac, hexed=True)
        print(f"\thexed: {damage}")

        damage = attack(level, ac, darkness=True)
        print(f"\tdarkness: {damage}")

        print("")

        damage = attack(level, ac, hexed=True, cursed=True)
        print(f"\thexed, hexblade's curse: {damage}")

        damage = attack(level, ac, darkness=True, cursed=True)
        print(f"\tdarkness, hexblade's curse: {damage}")

        print("")

        damage = attack(level, ac, hexed=True, spiritual_weapon=True)
        print(f"\thexed, spiritual weapon: {damage}")

        damage = attack(level, ac, darkness=True, spiritual_weapon=True)
        print(f"\tdarkness, spiritual weapon: {damage}")

        print("")

        damage = attack(level, ac, hexed=True, cursed=True, spiritual_weapon=True)
        print(f"\thexed, hexblade's curse, spiritual weapon: {damage}")

        damage = attack(level, ac, darkness=True, cursed=True, spiritual_weapon=True)
        print(f"\tdarkness, hexblade's curse, spiritual weapon: {damage}")

        if level >= 17:
            print("")

            damage = attack(level, ac, darkness=True, hexed=True)
            print(f"\thex, foresight: {damage}")

            damage = attack(level, ac, darkness=True, hexed=True, cursed=True)
            print(f"\thex, foresight, hexblade's curse: {damage}")

        print("")


# TODO stat bonus should increase at different levels for a Hexblade and a Sorlock
# TODO spiritual weapon should increase at different levels for a multi class

if __name__ == '__main__':
    run_trials()
