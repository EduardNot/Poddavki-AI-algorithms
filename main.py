import pygame
import sys
from Poddavki import Poddavki


def getCoords(location):
    row, col = location
    return getX(col), getY(row)


def getX(col):
    return BORDER_WIDTH + col * TILE_WIDTH


def getY(row):
    return BORDER_WIDTH + row * TILE_WIDTH


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

    # board = (
    #     ('', 'b', '', 'b', '', 'b', '', 'b'),
    #     ('b', '', 'b', '', 'b', '', 'b', ''),
    #     ('', 'b', '', 'b', '', 'b', '', 'b'),
    #     ('', '', '', '', '', '', '', ''),
    #     ('', '', '', '', '', '', '', ''),
    #     ('w', '', 'w', '', 'w', '', 'w', ''),
    #     ('', 'w', '', 'w', '', 'w', '', 'w'),
    #     ('w', '', 'w', '', 'w', '', 'w', ''),
    # )
    game = Poddavki()
    selectedPiece = None
    highlightedMoves = dict()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col, piece = getClickedTile(game.board)
                # TODO fix mandatory capture
                if game.to_move == 'white' and piece in ['w', 'wk'] or game.to_move == 'black' and piece in ['b', 'bk']:
                    selectedPiece = (row, col)
                    possibleMoves = game.getPossibleMoves(row, col)
                    # possibleMoves = getPossibleMoves(board, row, col)
                    highlightedMoves = {move[-1]: move for move in possibleMoves}
                if (row, col) in highlightedMoves:
                    print(game.to_move, game.translateMove(highlightedMoves[(row, col)]))
                    # print(player, translateMove(highlightedMoves[(row, col)]))
                    game.board = game.applyMove(highlightedMoves[(row, col)])
                    # board = apply_move(board, highlightedMoves[(row, col)])
                    game.switchPlayer()
                    # player = switchPlayer(player)
                    selectedPiece = None
                    highlightedMoves = dict()
        update_display(WINDOW, game.board, selectedPiece, highlightedMoves)


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
