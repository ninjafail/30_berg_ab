from Game import Game
from Player import Player, HumanPlayer, AiHighestOrSix, AiFiveOrSix
from Simulator import Simulator


def compare(strategy1: Player, strategy2: Player):
    sim1 = Simulator(strategy1)
    sim1.plot_turn_performance()
    Simulator(strategy2).plot_turn_performance()
    sim1.plot_cmp_with_strategy(strategy2, iterations=100000)


def play_test_game():
    names = ["Ben Dover", "Hugh Jazz", "Mike Litoris"]
    playersai = [AiHighestOrSix('AI'), AiHighestOrSix("AIGuenther"), AiHighestOrSix('AI2')]
    players = [HumanPlayer(name) for name in names]
    Game(playersai).play()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    compare(AiHighestOrSix(), AiFiveOrSix())



