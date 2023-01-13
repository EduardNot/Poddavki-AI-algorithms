import copy


def move(game, color, depth, alphabeta):
    colors = ['white', 'black']
    _, move = minimax(game, True, depth, alphabeta, colors if color == 'white' else colors[::-1])
    return move
            

def minimax(game, maxPlayer, depth, alphabeta, colors):
    if depth == 0:
        return (evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]), None)
    if not game.hasAvailableMoves():
        return (30, None) if maxPlayer else (-30, None)

    locations = game.getPieceLocations(colors[0] if maxPlayer else colors[1])
    best = (-100 if maxPlayer else 100, None)
    for row, col in locations:
        moves = game.getPossibleMoves(row, col)
        
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
    whiteTotal = 0
    blackTotal = 0
    for rowValues in board:
        for piece in rowValues:
            if piece in ['w', 'wk']:
                whiteTotal += 1
            elif piece in ['b', 'bk']:
                blackTotal += 1
    
    if playerColor == 'white':
        return blackTotal - whiteTotal
    else:
        return whiteTotal - blackTotal
