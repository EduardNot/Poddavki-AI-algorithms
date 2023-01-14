import copy
import Poddavki

def getTurn(game: Poddavki):
    return move(game, game.getPlayer(), 3, False)


def move(game, color, depth, alphabeta):
    colors = ['white', 'black']
    eval, move = minimax(game, True, depth, alphabeta, colors if color == 'white' else colors[::-1])
    print(eval)
    return move
            

def minimax(game, maxPlayer, depth, alphabeta, colors):
    if depth == 0:
        return (evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]), None)
    if not game.hasAvailableMoves():
        return (30, None) if maxPlayer else (-30, None)

    best = (-100 if maxPlayer else 100, None)
    moves = game.getPossibleMoves(colors[0] if maxPlayer else colors[1])
    
    for move in moves:
        gameCopy = copy.deepcopy(game)
        gameCopy.applyMove(move)
        eval = minimax(gameCopy, not maxPlayer, depth if maxPlayer else depth-1, alphabeta, colors)
        
        if maxPlayer and best[0] < eval[0]:
            best = (eval[0], move)
        elif not maxPlayer and best[0]  > eval[0]:
            best = (eval[0], move)
    return best


def evaluatePosition(board, playerColor):
    KING_VALUE = 0.5
    whiteTotal = 0
    blackTotal = 0
    for rowValues in board:
        for piece in rowValues:
            match piece:
                case 'w':
                    whiteTotal += 1
                case 'wk':
                    whiteTotal += 1 - KING_VALUE
                case 'b':
                    blackTotal += 1
                case 'bk':
                    blackTotal += 1 - KING_VALUE

    if playerColor == 'white':
        return blackTotal - whiteTotal
    else:
        return whiteTotal - blackTotal
