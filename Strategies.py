from Player import Player
from abc import abstractmethod


class Strategy(Player):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def get_all_n(number: int, roll: list[int]):
        return [i for i, r in enumerate(roll) if r == number]

    def strategy(self, roll: list[int]) -> list[int]:
        res = []
        self.take_dice(res, roll)

        if not res:
            res.append(roll.index(max(roll)))
        return res

    @abstractmethod
    def take_dice(self, res: list[int], roll: list[int]):
        pass


class StratSix(Strategy):
    def __init__(self, name="StratSix"):
        super().__init__(name)

    def take_dice(self, res: list[int], roll: list[int]):
        res += self.get_all_n(6, roll)


class StratFiveOrSix(Strategy):
    def __init__(self, name="StratFiveOrSix"):
        super().__init__(name)

    def take_dice(self, res: list[int], roll: list[int]):
        res += self.get_all_n(6, roll)
        res += self.get_all_n(5, roll)


class StratSixWithEndLess(Strategy):
    def __init__(self, name="StratSixWithEndLess"):
        super().__init__(name)

    def take_dice(self, res: list[int], roll: list[int]):
        res += self.get_all_n(6, roll)
        if len(roll) - len(res) < 3:
            res += self.get_all_n(5, roll)
        if len(roll) - len(res) < 2:
            res += self.get_all_n(4, roll)
