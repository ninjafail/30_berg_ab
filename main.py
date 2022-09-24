from Game import Game
from Player import HumanPlayer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    names = ["Ben Dover", "Hugh Jazz", "Mike Litoris"]
    players = [HumanPlayer(name) for name in names]
    Game(players).play()

