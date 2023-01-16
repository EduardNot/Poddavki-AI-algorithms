import time
from os import environ
from RandomAI import getTurn as randomAiTurn
from MonteCarloAI import getTurn as monteCarloTurn
from MiniMaxAI import getTurn as minMaxTurn


environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # hide pygame welcome message
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
    white_tile = '#FFCE9E'
    black_tile = '#D18B47'
    highlighted_tile = '#EC4136'

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
                WIN.blit(pygame.transform.scale(images['move'], (20, 20)) if SMALL else images['move'],
                         (x + OFFSET_MOVE, y + OFFSET_MOVE))
            # add pieces
            if piece in ['w', 'wk', 'b', 'bk']:
                WIN.blit(pygame.transform.scale(images[piece], (50, 50)) if SMALL else images[piece],
                         (x + OFFSET_PIECE, y + OFFSET_PIECE))
    pygame.display.update()


def getClickedTile(board):
    x, y = pygame.mouse.get_pos()
    if 40 <= x <= BOARD_SIZE - BORDER_WIDTH and 40 <= y <= BOARD_SIZE - BORDER_WIDTH:
        row = (y - BORDER_WIDTH) // TILE_WIDTH
        col = (x - BORDER_WIDTH) // TILE_WIDTH
        return row, col, board[row][col]
    else:
        return 'border', 'border', 'border'


def main():
    v_border = pygame.transform.scale(images['v_border'], (640, 40)) if SMALL else images['v_border']
    h_border = pygame.transform.scale(images['h_border'], (40, 640)) if SMALL else images['h_border']

    WINDOW.blit(v_border, (0, 0))
    WINDOW.blit(v_border, (0, BOARD_SIZE - BORDER_WIDTH))
    WINDOW.blit(h_border, (0, 0))
    WINDOW.blit(h_border, (BOARD_SIZE - BORDER_WIDTH, 0))

    game = Poddavki()
    availableMoves = game.getPossibleMoves(game.to_move)
    selectedPiece = None
    highlightedMoves = dict()
    update_display(WINDOW, game.board, selectedPiece, highlightedMoves)
    while availableMoves:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            if game.to_move == 'white' and PLAYER_WHITE == 'human' or game.to_move == 'black' and PLAYER_BLACK == 'human':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col, piece = getClickedTile(game.board)
                    if game.to_move == 'white' and piece in ['w', 'wk'] or game.to_move == 'black' and piece in ['b','bk']:
                        selectedPiece = (row, col)
                        highlightedMoves = {move[-1]: move for move in availableMoves if move[0] == selectedPiece}
                        update_display(WINDOW, game.board, selectedPiece, highlightedMoves)
                    if (row, col) in highlightedMoves:
                        print(game.to_move, game.translateMove(highlightedMoves[(row, col)]))
                        game.applyMove(highlightedMoves[(row, col)])
                        selectedPiece = None
                        highlightedMoves = dict()
                        availableMoves = game.getPossibleMoves(game.to_move)
                        update_display(WINDOW, game.board, selectedPiece, highlightedMoves)

            else:
                start = time.time()
                if len(availableMoves) == 1:
                    move = availableMoves[0]
                elif game.to_move == 'white':
                    move = aiTurns[PLAYER_WHITE](game)
                else:
                    move = aiTurns[PLAYER_BLACK](game)
                while time.time() - start < 0.2: pass
                if len(move) == 8:
                    for moveList in game.getPossibleMoves(game.to_move):
                        if move == game.getNextBoardState(moveList):
                            move = moveList
                            break
                if move in availableMoves:
                    print(game.to_move, game.translateMove(move))
                    game.applyMove(move)
                    availableMoves = game.getPossibleMoves(game.to_move)
                    update_display(WINDOW, game.board, selectedPiece, highlightedMoves)
                else:
                    print('invalid move')
    print('Winner:', game.getWinner())


images = {val: pygame.image.load(f'assets/{val}.png') for val in ['b', 'bk', 'w', 'wk', 'move', 'v_border', 'h_border']}

SMALL = False

BOARD_SIZE = 640 if SMALL else 880
BORDER_WIDTH = 40
OFFSET_PIECE = 10
OFFSET_MOVE = 25 if SMALL else 35
TILE_WIDTH = 70 if SMALL else 100

pygame.init()
WINDOW = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption('Checkers')

aiTurns = {'random-ai': randomAiTurn, 'minmax-ai': minMaxTurn, 'monteCarlo-ai': monteCarloTurn}

PLAYER_WHITE = 'random-ai'
PLAYER_BLACK = 'monteCarlo-ai'

main()
