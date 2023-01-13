import random
import Poddavki


def getTurn(game: Poddavki):
    return random.choice(game.getPossibleBoardStates(game.to_move))
    # return random.choice(game.getPossibleMoves(game.to_move))
