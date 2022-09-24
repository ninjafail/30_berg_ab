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
        assert indices

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


class Player:
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

    def take_turn(self) -> int:
        self.reset()
        while True:
            if self.dice_cup.is_empty():
                break
            roll = self.roll()
            err = True
            while err:
                try:
                    print(f"{self.name} rolled: ")
                    print("\t", end='')
                    for j, r in enumerate(roll):
                        print(f"{chr(ord('a') + j)}: {r}, ", end='')
                    print("\nChoose the dice you want to take out by typing the letters and press enter to submit:")
                    letters = input()
                    numbers = [ord(l) - ord('a') for l in letters]
                    self.take_out(numbers)
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


class PlayBergAb:
    def __init__(self, players: list[Player]):
        self.alivePlayers: list[Player] = players
        self.deadPlayers: list[Player] = []

    def remove_player_if_dead(self, index):
        if not self.alivePlayers[index].is_alive():
            print(f"{self.alivePlayers[index].name} has died :( Well, wasn't good enough I guess ...")
            self.deadPlayers.append(self.alivePlayers.pop(index))

    def damage_player(self, index: int, damage: int):
        assert index in range(len(self.alivePlayers))
        assert damage >= 0

        self.alivePlayers[index].life_points -= damage
        self.remove_player_if_dead(index)

    def check_dead_players(self):
        for i in range(len(self.alivePlayers)):
            self.remove_player_if_dead(i)

    def play(self):
        print("Welcome to 30 Berg ab. A german dice game that breaks relationships and separates families. This game is totally based on skill. The skill to roll good. Have fun! \n")

        print("The players order is: ")
        for player in self.alivePlayers:
            print(f"{player.name}, ", end="")
        print("let's go ... \n")

        while len(self.alivePlayers) > 1:
            for i, player in enumerate(self.alivePlayers):
                self.check_dead_players()
                print(f"It is {player.name}'s turn!\nYou have {player.life_points} life points.")
                print(f"The others have:")
                for p in self.alivePlayers:
                    print(f"\t{p.name}: {p.life_points}")

                player_end_roll = player.take_turn()
                print(f"And {player.name} rolled a ... ")
                if player_end_roll == 30:
                    print(f"... whopping {player_end_roll}, wow ...\n\tnothing happens.")
                elif player_end_roll < 30:
                    print(f"... {player_end_roll} ... Can't even roll above 30, smh. In confusion you even damaged yourself, putting you at {player.life_points - (30 - player_end_roll)} lifepoints.")
                    self.damage_player(i, 30 - player_end_roll)
                elif player_end_roll > 30:
                    next_player_index = (i + 1) % len(self.alivePlayers)
                    next_player = self.alivePlayers[next_player_index]
                    print(f"... {player_end_roll}. Nice finally some damage.")
                    damage = player.roll_damage(player_end_roll - 30)
                    print(f"You damage {next_player.name} with {damage} points, putting him at {next_player.life_points - damage} life points.")
                    self.damage_player(next_player_index, damage)
                player.reset()
                print()

        print("Nice Game!")
        print(f"Players {self.deadPlayers[0].name}", end="")
        for player in self.deadPlayers[1:]:
            print(f", {player.name}", end="")
        print(f" died and lost. All losers, except for {self.alivePlayers[0].name}. The only one with the guts to win. Good job!")


def test():
    PlayBergAb([Player(name) for name in ["Ben Dover", "Hugh Jazz", "Mike Litoris"]]).play()


test()
