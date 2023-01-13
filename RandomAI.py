import random
import Poddavki


def getTurn(game: Poddavki):
    return random.choice(game.getAllMoves(game.to_move))
