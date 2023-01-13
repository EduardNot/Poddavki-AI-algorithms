import pygame
import sys
from tabulate import tabulate


def getCoords(location):
    row, col = location
    return getX(col), getY(row)


def getX(col):
    return BORDER_WIDTH + col * TILE_WIDTH


def getY(row):
    return BORDER_WIDTH + row * TILE_WIDTH


def getPieceLocations(board):
    positions = []
    for row, rowValues in enumerate(board):
        for col, piece in enumerate(rowValues):
            if piece in ['b', 'bk', 'w', 'wk']:
                positions.append((row, col))
    return positions


def isInBounds(row, col):
    return 0 <= row <= 7 and 0 <= col <= 7


def newBoard(board, moves):
    new_board = list(map(list, board))
    start_row, start_col = moves[0]
    end_row, end_col = moves[-1]
    piece = board[start_row][start_col]

    for row, col in moves:
        if row == 0 and piece == 'w':
            piece = 'wk'
        if row == 7 and piece == 'b':
            piece = 'bk'
        new_board[row][col] = ''

    new_board[end_row][end_col] = piece
    return tuple(map(tuple, new_board))


def getRegularMoves(board, row, col):
    moves = []
    startingLoc = (row, col)
    piece = board[row][col]
    match piece:
        case 'b':
            moves = [(row + 1, col - 1), (row + 1, col + 1)]
        case 'w':
            moves = [(row - 1, col + 1), (row - 1, col - 1)]
        case 'wk' | 'bk':
            moves = [(row + 1, col - 1), (row + 1, col + 1), (row - 1, col + 1), (row - 1, col - 1)]

    possibleMoves = []
    for row, col in moves:
        if isInBounds(row, col) and board[row][col] == '':
            possibleMoves.append((startingLoc, (row, col)))
    return possibleMoves


def printBoard(board):
    print(tabulate(board))


def translateMove(move):
    rowMove = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    colMove = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    result = ''
    if len(move) == 2:
        delimiter = ', '
    else:
        delimiter = ':'
    for row, col in move:
        result += f'{colMove[col]}{rowMove[row]}{delimiter}'
    return result[:-len(delimiter)]


def getNextSkips(board, row, col):
    startPosition = (row, col)
    piece = board[row][col]
    locations = []
    if piece in ['b', 'bk']:
        opponentPieces = ['w', 'wk']
    else:
        opponentPieces = ['b', 'bk']
    match piece:
        case 'b':
            locations = [((row + 1, col - 1), (row + 2, col - 2)), ((row + 1, col + 1), (row + 2, col + 2))]
        case 'w':
            locations = [((row - 1, col + 1), (row - 2, col + 2)), ((row - 1, col - 1), (row - 2, col - 2))]
        case 'wk' | 'bk':
            locations = [((row + 1, col - 1), (row + 2, col - 2)), ((row + 1, col + 1), (row + 2, col + 2)),
                         ((row - 1, col + 1), (row - 2, col + 2)), ((row - 1, col - 1), (row - 2, col - 2))]
    skipMoves = []
    for regular_move, take_piece in locations:
        row, col = regular_move
        if isInBounds(row, col) and board[row][col] in opponentPieces:
            row, col = take_piece
            if isInBounds(row, col) and board[row][col] == '':
                skipMoves.append((startPosition, regular_move, take_piece))
    return skipMoves


def getSkips(board, row, col):
    possibleMoves = []

    skips = getNextSkips(board, row, col)
    while skips:
        move = skips.pop()
        nextSkips = getNextSkips(newBoard(board, move), *move[-1])
        if nextSkips:
            for startingPosition, enemyPiece, nextPosition in nextSkips:
                skips.append(move + (enemyPiece, nextPosition))
        else:
            possibleMoves.append(move)
    return possibleMoves


def getPossibleMoves(board, row, col):
    skips = getSkips(board, row, col)
    if skips:
        return skips
    return getRegularMoves(board, row, col)


def update_display(WIN, board, selectedPiece, possibleMoves):
    for row, rowValues in enumerate(board):
        for col, piece in enumerate(rowValues):
            x, y = getCoords((row, col))
            # color tiles
            if (row, col) == selectedPiece:
                color = highlighted_tile
            elif (row % 2 + col) % 2:
                color = black_tile
            else:
                color = white_tile
            pygame.draw.rect(WINDOW, color, (x, y, TILE_WIDTH, TILE_WIDTH))
            # show move locations
            if (row, col) in possibleMoves:
                WIN.blit(images['move'], (x + OFFSET_MOVE, y + OFFSET_MOVE))
            # add pieces
            if piece in ['w', 'wk', 'b', 'bk']:
                WIN.blit(images[piece], (x + OFFSET_PIECE, y + OFFSET_PIECE))
    pygame.display.update()


def getAllMoves(board, player):
    availableMoves = []
    if player == 'white':
        pieces = ['w', 'wk']
    else:
        pieces = ['b', 'bk']
    for row, rowValues in enumerate(board):
        for col, piece in enumerate(rowValues):
            if piece in pieces:
                availableMoves.append(getPossibleMoves(board, row, col))
    return availableMoves


def switchPlayer(currentPlayer):
    if currentPlayer == 'white':
        return 'black'
    else:
        return 'white'


def isEnd(board, player):
    availableMoves = getAllMoves(board, player)
    return len(availableMoves) > 0


def getClickedTile(board):
    x, y = pygame.mouse.get_pos()
    if 40 <= x <= 840 and 40 <= y <= 840:
        row = (y - BORDER_WIDTH) // TILE_WIDTH
        col = (x - BORDER_WIDTH) // TILE_WIDTH
        return row, col, board[row][col]
    else:
        return 'border', 'border', 'border'


def main():
    WINDOW.blit(images['v_border'], (0, 0))
    WINDOW.blit(images['v_border'], (0, 840))
    WINDOW.blit(images['h_border'], (0, 0))
    WINDOW.blit(images['h_border'], (840, 0))

    board = (
        ('', 'b', '', 'b', '', 'b', '', 'b'),
        ('b', '', 'b', '', 'b', '', 'b', ''),
        ('', 'b', '', 'b', '', 'b', '', 'b'),
        ('', '', '', '', '', '', '', ''),
        ('', '', '', '', '', '', '', ''),
        ('w', '', 'w', '', 'w', '', 'w', ''),
        ('', 'w', '', 'w', '', 'w', '', 'w'),
        ('w', '', 'w', '', 'w', '', 'w', ''),
    )

    selectedPiece = None
    highlightedMoves = dict()
    player = 'white'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col, piece = getClickedTile(board)
                # TODO fix mandatory capture
                if player == 'white' and piece in ['w', 'wk'] or player == 'black' and piece in ['b', 'bk']:
                    selectedPiece = (row, col)
                    possibleMoves = getPossibleMoves(board, row, col)
                    highlightedMoves = {move[-1]: move for move in possibleMoves}
                if (row, col) in highlightedMoves:
                    print(player, translateMove(highlightedMoves[(row, col)]))
                    board = move(board, highlightedMoves[(row, col)])
                    player = switchPlayer(player)
                    selectedPiece = None
                    highlightedMoves = dict()
        update_display(WINDOW, board, selectedPiece, highlightedMoves)


images = {val: pygame.image.load(f'assets/{val}.png') for val in ['b', 'bk', 'w', 'wk', 'move', 'v_border', 'h_border']}

BOARD_SIZE = 880
BORDER_WIDTH = 40
OFFSET_PIECE = 10
OFFSET_MOVE = 35
TILE_WIDTH = 100

white_tile = '#FFCE9E'
black_tile = '#D18B47'
highlighted_tile = '#EC4136'

pygame.init()
WINDOW = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption('Checkers')

priorMoves = []
main()
