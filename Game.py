from Player import Player


class Game:
    def __init__(self, players: list[Player], should_print: bool = True):
        self.alivePlayers: list[Player] = players
        self.deadPlayers: list[Player] = []
        self.should_print = should_print

    def print(self, *values, sep=' ', end='\n'):
        if self.should_print:
            print(*values, sep=sep, end=end)

    def remove_player_if_dead(self, index):
        if not self.alivePlayers[index].is_alive():
            self.print(f"{self.alivePlayers[index].name} has died :( Well, wasn't good enough I guess ...")
            self.deadPlayers.append(self.alivePlayers.pop(index))

    def damage_player(self, index: int, damage: int):
        assert index in range(len(self.alivePlayers))
        assert damage >= 0

        self.alivePlayers[index].life_points -= damage
        self.remove_player_if_dead(index)

    def check_dead_players(self):
        for i in range(len(self.alivePlayers)):
            self.remove_player_if_dead(i)

    def is_game_finished(self):
        return len(self.alivePlayers) <= 1

    def play(self):
        self.print("Welcome to 30 Berg ab. A german dice game that breaks relationships and separates families. This game is totally based on skill. The skill to roll good. Have fun! \n")

        self.print("The players order is: ")
        for player in self.alivePlayers:
            self.print(f"{player.name}, ", end="")
        self.print("let's go ... \n")

        while not self.is_game_finished():
            for i, player in enumerate(self.alivePlayers):
                if self.is_game_finished():
                    break
                self.print(f"It is {player.name}'s turn!\nYou have {player.life_points} life points.")
                self.print(f"The others have:")
                for p in self.alivePlayers:
                    self.print(f"\t{p.name}: {p.life_points}")

                player_end_roll = player.take_turn()
                self.print(f"And {player.name} rolled a ... ", end='')
                if player_end_roll == 30:
                    self.print(f"whopping {player_end_roll}, wow  . . .  nothing happens.")
                elif player_end_roll < 30:
                    self.print(
                        f"{player_end_roll} ... Can't even roll above 30, smh. In confusion you even damaged yourself, putting you at {player.life_points - (30 - player_end_roll)} lifepoints.")
                    self.damage_player(i, 30 - player_end_roll)
                elif player_end_roll > 30:
                    next_player_index = (i + 1) % len(self.alivePlayers)
                    next_player = self.alivePlayers[next_player_index]
                    self.print(f"{player_end_roll}. Nice finally some damage.")
                    damage = player.roll_damage(player_end_roll - 30, should_print=self.should_print)
                    self.print(
                        f"You damage {next_player.name} with {damage} points, putting him at {next_player.life_points - damage} life points.")
                    self.damage_player(next_player_index, damage)
                player.reset()
                self.print()

        self.print("Nice Game!")
        self.print(f"Players {self.deadPlayers[0].name}", end="")
        if len(self.deadPlayers) > 1:
            for player in self.deadPlayers[1:]:
                self.print(f", {player.name}", end="")
        self.print(
            f" died and lost. All losers, except for {self.alivePlayers[0].name}. The only one with the guts to win. Good job!")

        return self.alivePlayers[0]
