import random
import Poddavki


def getTurn(game: Poddavki):
    return random.choice(game.getPossibleMoves(game.to_move))
