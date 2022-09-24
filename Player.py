from Dice import DiceCup
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.life_points = 30
        self.dice_cup = DiceCup(6, 6)
        self.rolled = False
        self.results = []

    def __repr__(self):
        return f"Player(name: {self.name}, lp: {self.life_points}, activeDie: {self.dice_cup}, results: {self.results})"

    def roll(self) -> list[int]:
        assert not self.rolled

        self.rolled = True
        return self.dice_cup.roll()

    def take_out(self, indices: list[int]) -> list[int]:
        assert self.rolled

        res_dice = self.dice_cup.take_out(indices)
        res = [d.lastRoll for d in res_dice]
        self.results.extend(res)
        self.rolled = False
        return res

    def get_end_result(self) -> int:
        return sum(self.results, 0)

    def is_alive(self) -> bool:
        return self.life_points > 0

    def reset(self):
        self.dice_cup.reset()
        self.rolled = False
        self.results = []

    def attack_once(self, factor: int) -> int:
        assert factor in range(1, 7)

        if self.dice_cup.is_empty():
            self.reset()
        results = self.roll()
        print(f"Your damage roll: {results}")
        attack_amount = results.count(factor)
        to_take_out = [*range(attack_amount)]

        if not to_take_out:
            self.rolled = False
            return 0

        self.take_out(to_take_out)
        return attack_amount * factor

    """Defines which indexes should be taken out from the roll and returns them
    
    :param roll the list of results that got rolled in this turn
    :returns list of indexes from the argument roll
    """
    @abstractmethod
    def strategy(self, roll: list[int]) -> list[int]:
        pass

    def take_turn(self) -> int:
        self.reset()
        while True:
            if self.dice_cup.is_empty():
                break
            roll = self.roll()
            err = True
            while err:
                try:
                    self.take_out(self.strategy(roll))
                    err = False
                except Exception as e:
                    print(e)
                    err = True
        return self.get_end_result()

    def roll_damage(self, factor: int) -> int:
        self.reset()
        last_damage = self.attack_once(factor)
        attack_damage = last_damage
        while last_damage != 0 or self.dice_cup.is_empty():
            last_damage = self.attack_once(factor)
            attack_damage += last_damage
        return attack_damage


class HumanPlayer(Player):
    def strategy(self, roll: list[int]) -> list[int]:
        print(f"{self.name} rolled: ")
        print("\t", end='')
        for j, r in enumerate(roll):
            print(f"{chr(ord('a') + j)}: {r}, ", end='')
        print("\nChoose the dice you want to take out by typing the letters and press enter to submit:")
        letters = input()
        return [ord(l) - ord('a') for l in letters]


class HighestOrSixAi(Player):
    def strategy(self, roll: list[int]) -> list[int]:
        res = []
        for i, r in roll:
            if r == 6:
                res.append(i)
        if not res:
            res.append(max(roll))
        return res