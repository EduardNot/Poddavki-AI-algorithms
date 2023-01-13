from Poddavki import Poddavki
from RandomAI import getTurn as randomAiTurn

# from MonteCarloAI import getTurn as monteCarloTurn
# from MiniMaxAI import getTurn as minMaxTurn

def main():
    game = Poddavki()
    availableMoves = game.getPossibleMoves(game.to_move)
    while availableMoves:
        if game.to_move == 'white':
            move = aiTurns[PLAYER_WHITE](game)
        else:
            move = aiTurns[PLAYER_BLACK](game)
        if len(move) == 8:
            for moves in game.getPossibleMoves(game.to_move):
                if move == game.getNextBoardState(moves):
                    print(game.to_move, game.translateMove(moves))
            game.switchPlayer()
            game.board = move
        else:
            print(game.to_move, game.translateMove(move))
            game.applyMove(move)
        availableMoves = game.getPossibleMoves(game.to_move)

    print('Winner:', game.getWinner())


aiTurns = {'random-ai': randomAiTurn, 'minmax-ai': None, 'monteCarlo-ai': None, 'minmax-ab-ai': None}

PLAYER_WHITE = 'random-ai'
PLAYER_BLACK = 'random-ai'

main()