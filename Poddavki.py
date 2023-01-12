import pygame
import sys


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


def getPossibleMoves(board, row, col):
    piece = board[row][col]
    possibleMoves = []
    moves = []
    if piece == 'b':
        moves = [(row + 1, col - 1), (row + 1, col + 1)]
    if piece == 'w':
        moves = [(row - 1, col - 1), (row - 1, col + 1)]
    for r, c in moves:
        # print(r, c, board[r][c])
        if 0 <= r <= 7 and 0 <= c <= 7 and board[r][c] == '':
            possibleMoves.append((r, c))
    return possibleMoves


def isEnd(board, nextplayer):
    pass  # TODO


def getWinner(board):
    pass  # TODO


def getClickedTile(board):
    x, y = pygame.mouse.get_pos()
    if 40 <= x <= 840 and 40 <= y <= 840:
        row = (y - BORDER_WIDTH) // TILE_WIDTH
        col = (x - BORDER_WIDTH) // TILE_WIDTH
        print(f'Clicked: {rowMove[row]}{colMove[col]}', row, col)
        return row, col, board[row][col]
    else:
        print('Clicked border')
        return 'border', 'border', 'border'


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
    possibleMoves = []

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
                    possibleMoves = getPossibleMoves(board, row, col)
                    print(possibleMoves)
        update_display(WINDOW, board, selectedPiece, possibleMoves)


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
