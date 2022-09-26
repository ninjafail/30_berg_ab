from Game import Game
from Player import Player, AiHighestOrSix
import pandas as pd
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self, strategy: Player):
        self.strategy = strategy
        self.turn_performance = []
        self.winner_list = []

    def simulate_turn_performance(self, iteration: int):
        result = []
        for _ in range(iteration):
            result.append(self.strategy.take_turn())
        self.turn_performance = result
        return self.turn_performance

    def plot_turn_performance(self, iterations=10000, bin_range: list[int] = None):
        if bin_range is None:
            bin_range = [*range(18, 38)]
        if not self.turn_performance:
            self.simulate_turn_performance(iterations)
        series = pd.Series(data=self.turn_performance)
        ax = plt.hist(series, bins=bin_range)
        plt.title(f"Turn performance of {self.strategy.name} with n={iterations}")
        plt.xticks(bin_range)
        plt.figtext(0.5, 0.01, f"Variance = {series.var()}, Median = {series.median()}, Mean = {series.mean()}", size=12, ha="center")
        plt.show()

    def cmp_with_strategy(self, enemy_strategy: Player, iterations: int):
        winner_list = []
        for _ in range(iterations):
            game = Game([self.strategy, enemy_strategy], should_print=False)
            winner_list.append(game.play().name)
        self.winner_list = winner_list
        return self.winner_list

    def plot_cmp_with_strategy(self, enemy_strategy: Player = None, iterations=10000):
        if not self.winner_list:
            assert enemy_strategy
            self.cmp_with_strategy(enemy_strategy, iterations)
        series = pd.Series(data=self.winner_list)
        plt.hist(series)
        plt.title(f"Comparison of wins with n={iterations}")
        plt.show()


