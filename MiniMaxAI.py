import Poddavki


def getTurn(game: Poddavki):
    return move(game, game.getPlayer(), 4, False)


def getTurnAB(game: Poddavki):
    return move(game, game.getPlayer(), 4, True)


def move(game, color, depth, alphabeta):
    colors = ('white', 'black')
    _, move = minimax(game, True, depth, alphabeta, 0, colors if color == 'white' else colors[::-1])
    return move
            

def minimax(game, maxPlayer, depth, alphabeta, prevEval, colors):
    if depth == 0:
        return (evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]), None)
    if not game.hasAvailableMoves():
        return (30, None) if maxPlayer else (-30, None)

    best = (-100 if maxPlayer else 100, None)
    moves = game.getPossibleMoves(colors[0] if maxPlayer else colors[1])
    
    for move in moves:
        if alphabeta and (maxPlayer and prevEval <= best[0] or not maxPlayer and prevEval >= best[0]):
            break

        gameCopy = game.copyGame()
        gameCopy.applyMove(move)
        eval = minimax(gameCopy, not maxPlayer, depth if maxPlayer else depth-1, alphabeta, best[0], colors)
        
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
