from Poddavki import Poddavki
from RandomAI import getTurn as randomAiTurn
from MonteCarloAI import getTurn as monteCarloTurn
from MiniMaxAI import getTurn as minMaxTurn
from MiniMaxAI import getTurnAB as minMaxABTurn


def main(PLAYER_WHITE, PLAYER_BLACK):
    aiTurns = {'random-ai': randomAiTurn, 'minimax-ai': minMaxTurn, 'minimaxab-ai': minMaxABTurn,
               'monteCarlo-ai': monteCarloTurn}
    game = Poddavki()
    availableMoves = game.getPossibleMoves(game.to_move)
    print(f'(white) {PLAYER_WHITE} vs {PLAYER_BLACK} (black)')
    while availableMoves and not game.draw:
        if len(availableMoves) == 1:
            move = availableMoves[0]
        elif game.to_move == 'white':
            move = aiTurns[PLAYER_WHITE](game)
        else:
            move = aiTurns[PLAYER_BLACK](game)
        if len(move) == 8:
            for moveList in game.getPossibleMoves(game.to_move):
                if move == game.getNextBoardState(moveList):
                    move = moveList
                    break
        if move in availableMoves:
            print(game.to_move, game.translateMove(move))
            game.applyMove(move)
            availableMoves = game.getPossibleMoves(game.to_move)
        else:
            print('invalid move')
    winner = game.getWinner()
    print(f'(white) {PLAYER_WHITE} vs {PLAYER_BLACK} (black)')
    if winner == 'white':
        print(f'Winner: {PLAYER_WHITE}')
    elif winner == 'black':
        print(f'Winner: {PLAYER_BLACK}')
    else:
        print('Draw')

