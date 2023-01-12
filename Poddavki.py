import pygame
import sys
from copy import deepcopy


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
    new_board = deepcopy(board)
    start_row, start_col = moves[0]
    end_row, end_col = moves[-1]
    new_board[end_row][end_col] = new_board[start_row][start_col]
    for row, col in moves[:-1]:
        new_board[row][col] = ''
    return new_board


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
            move = (startingLoc, (row, col))
            possibleMoves.append({'board': newBoard(board, move), 'moves': move})
    return possibleMoves


def getSkips(board, row, col):
    pass  # TODO


def getAllMoves(board, player):
    pass  # TODO


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


def isEnd(board, nextplayer):
    pass  # TODO


def getWinner(board):
    pass  # TODO


def getClickedTile(board):
    x, y = pygame.mouse.get_pos()
    if 40 <= x <= 840 and 40 <= y <= 840:
        row = (y - BORDER_WIDTH) // TILE_WIDTH
        col = (x - BORDER_WIDTH) // TILE_WIDTH
        print(f'Clicked: {rowMove[row]}{colMove[col]} ({row}, {col})')
        return row, col, board[row][col]
    else:
        print('Clicked border')
        return 'border', 'border', 'border'


def getHighlightedTiles(moves):
    return {val['moves'][-1]: val['board'] for val in moves}


def main():
    WINDOW.blit(images['v_border'], (0, 0))
    WINDOW.blit(images['v_border'], (0, 840))
    WINDOW.blit(images['h_border'], (0, 0))
    WINDOW.blit(images['h_border'], (840, 0))

    board = [
        ['', 'b', '', 'b', '', 'b', '', 'b'],
        ['b', '', 'b', '', 'b', '', 'b', ''],
        ['', 'b', '', 'b', '', 'b', '', 'b'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['w', '', 'w', '', 'w', '', 'w', ''],
        ['', 'w', '', 'w', '', 'w', '', 'w'],
        ['w', '', 'w', '', 'w', '', 'w', ''],
    ]

    selectedPiece = None
    highlightedMoves = dict()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col, piece = getClickedTile(board)
                if piece in ['w', 'b', 'bk', 'wk']:
                    selectedPiece = (row, col)
                    possibleMoves = getRegularMoves(board, row, col)
                    highlightedMoves = getHighlightedTiles(possibleMoves)
                if (row, col) in highlightedMoves:
                    board = highlightedMoves[(row, col)]
                    selectedPiece = None
                    highlightedMoves = dict()
        update_display(WINDOW, board, selectedPiece, highlightedMoves)


colMove = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
rowMove = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
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
