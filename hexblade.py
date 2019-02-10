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

    def attack_roll(self, proficient=True):
        if self.advantage == 1:
            roll = max(randint(1, 20), randint(1, 20))
        elif self.advantage == 2:
            roll = max(randint(1, 20), randint(1, 20), randint(1, 20))
        else:
            roll = randint(1, 20)

        # was the roll a crit?
        if roll >= 20 - self.crit_range:
            crit = True
        else:
            crit = False

        # add proficiency and the stat bonus
        if proficient:
            roll += self.proficiency + self.stat_bonus

        return roll, crit

    def is_hit(self, roll, ac):
        if roll >= ac:
            return True
        else:
            return False


class Hexblade(Character):
    def additional_damage_on_hit(self, crit=False):
        damage = 0
        if self.options.get("hexed", False):
            damage += self.hexed_damage(crit=crit)
        if self.options.get("bestow_curse", False):
            damage += self.bestow_curse_damage(crit=crit)
        if self.options.get("curse", False):
            damage += self.proficiency
        return damage

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

    def bestow_curse(self, on=True):
        if on:
            self.options["bestow_curse"] = True
        else:
            self.options.pop("bestow_curse", None)

    def bestow_curse_damage(self, crit=False):
        if crit:
            return randint(1, 8) + randint(1, 8)
        return randint(1, 8)

    def eldritch_blast_damage(self, crit=False):
        damage = randint(1, 10) + self.stat_bonus
        if crit:
            damage += randint(1, 10)

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
            attack_roll, is_crit = self.attack_roll()

            if attack_roll < ac and not is_crit:
                return 0
            else:
                damage += randint(1, 10) + self.stat_bonus
                if is_crit:
                    damage += randint(1, 10)

                damage += self.additional_damage_on_hit(crit=is_crit)

        return damage

    def spiritual_weapon(self, ac):
        if self.level >= 10:
            d8s = 2
        elif self.level >= 5:
            d8s = 1
        else:
            return 0

        attack_roll, is_crit = self.attack_roll()

        if attack_roll < ac and not is_crit:
            return 0

        damage = 0
        for dice in range(d8s):
            damage += randint(1, 8)
            if is_crit:
                damage += randint(1, 8)

        damage += self.stat_bonus
        damage += self.additional_damage_on_hit(crit=is_crit)

        return damage


def attack(
        level, ac, hexed=False, darkness=False, cursed=False, spiritual_weapon=False, bestow_curse=False,
        foresight=False
):
    hexblade = Hexblade(level)
    if cursed:
        hexblade.hex_curse()
    if hexed:
        hexblade.hexed()
    if bestow_curse:
        hexblade.bestow_curse()
    if darkness or foresight:
        hexblade.advantage = 2

    damage = 0
    for attack_round in range(100_000):
        damage += hexblade.eldritch_blast(ac)
        if spiritual_weapon:
            damage += hexblade.spiritual_weapon(ac)
    return damage / 100_000


def run_trials():
    levels = [3, 5, 9, 13, 17]
    ac = 14

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

        if level >= 9:
            print("")
            damage = attack(level, ac, hexed=True, cursed=True, bestow_curse=True)
            print(f"\thexed, hexblade's curse, bestow curse: {damage}")

            damage = attack(level, ac, darkness=True, cursed=True, bestow_curse=True)
            print(f"\tdarkness, hexblade's curse, bestow curse: {damage}")

        if level >= 17:
            print("")

            damage = attack(level, ac, foresight=True, hexed=True)
            print(f"\thex, foresight: {damage}")

            damage = attack(level, ac, foresight=True, hexed=True, cursed=True)
            print(f"\thex, foresight, hexblade's curse: {damage}")

            damage = attack(level, ac, foresight=True, hexed=True, cursed=True, bestow_curse=True)
            print(f"\thex, foresight, hexblade's curse, bestow curse: {damage}")

        print("")


# TODO stat bonus should increase at different levels for a Hexblade and a Sorlock
# TODO spiritual weapon should increase at different levels for a multi class

if __name__ == '__main__':
    run_trials()
