from Game import Game
from Player import Player, HumanPlayer
from Strategies import Strategy, StratSix, StratFiveOrSix, StratSixWithEndLess
from Simulator import Simulator


def compare(strategy1: Strategy, strategy2: Strategy, iterations=10000):
    sim1 = Simulator(strategy1)
    sim1.plot_turn_performance(iterations)
    Simulator(strategy2).plot_turn_performance(iterations)
    sim1.plot_cmp_with_strategy(strategy2, iterations)


def play_test_game():
    names = ["Ben Dover", "Hugh Jazz", "Mike Litoris"]
    playersai = [StratSix('AI'), StratSix("AIGuenther"), StratSix('AI2')]
    players = [HumanPlayer(name) for name in names]
    Game(players).play()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    compare(StratSixWithEndLess(), StratFiveOrSix(), 100000)
    # play_test_game()
