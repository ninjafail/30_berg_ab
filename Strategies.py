from Player import Player
from abc import abstractmethod

class Strategy(Player):
    def __init__(self, name):
        super().__init__(name)

    def strategy(self, roll: list[int]) -> list[int]:
        res = []
        for i, r in enumerate(roll):
            self.take_dice(res, i, r, roll)

        if not res:
            res.append(roll.index(max(roll)))
        return res

    @abstractmethod
    def take_dice(self, res: list[int], i: int, r: int, roll: list[int]):
        pass


class StratSix(Strategy):
    def __init__(self, name="StratSix"):
        super().__init__(name)

    def take_dice(self, res: list[int], i: int, r: int, roll: list[int]):
        if r == 6:
            res.append(i)


class StratFiveOrSix(Strategy):
    def __init__(self, name="StratSix"):
        super().__init__(name)

    def take_dice(self, res: list[int], i: int, r: int, roll: list[int]):
        if r == 5 or r == 6:
            res.append(i)

