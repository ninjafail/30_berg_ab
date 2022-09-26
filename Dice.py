import random


class Die:
    def __init__(self, sides):
        self.sides = sides
        self.lastRoll = 0

    def __repr__(self):
        return f"Die(sides: {self.sides}, lastRoll: {self.lastRoll})"

    def roll(self):
        self.lastRoll = random.randint(1, self.sides)
        return self.lastRoll

    def reset(self):
        self.lastRoll = 0


class DiceCup:
    def __init__(self, dice_amount: int, sides: int):
        self.dice = [Die(sides) for _ in range(dice_amount)]
        self.dice_amount = dice_amount
        self.sides = sides

    def __repr__(self):
        return f"DiceCup({self.dice})"

    def take_out(self, indices: list[int]) -> list[Die]:
        if not indices:
            raise IndexError("Please enter valid values.")
        for index in indices:
            if index not in range(len(self.dice)):
                raise IndexError("Please enter a valid value that is shown as an option.")

        return_dice: list[Die] = []
        indices: list[int] = list(dict.fromkeys(indices))
        indices.sort()
        for i, index in enumerate(indices):
            pop_index = index - i
            assert pop_index in range(0, len(self.dice))
            return_dice.append(self.dice.pop(pop_index))
        return return_dice

    def throw_in(self):
        self.dice.append(Die(self.sides))

    def roll(self) -> list[int]:
        return [d.roll() for d in self.dice]

    def reset(self):
        self.dice = [Die(self.sides) for _ in range(self.dice_amount)]

    def is_empty(self):
        return len(self.dice) == 0
