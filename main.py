from Game import Game
from Player import HumanPlayer, AiHighestOrSix

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    names = ["Ben Dover", "Hugh Jazz", "Mike Litoris"]
    playersai = [AiHighestOrSix('AI'), AiHighestOrSix("AIGuenther"), AiHighestOrSix('AI2')]
    players = [HumanPlayer(name) for name in names]
    Game(playersai).play()
