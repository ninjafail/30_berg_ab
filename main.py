from dice import Player, PlayBergAb

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    names = ["Ben Dover", "Hugh Jazz", "Mike Litoris"]
    players = [Player(name) for name in names]
    PlayBergAb(players).play()

