import game_CLI
import game_GUI
from enum import Enum


class Board(Enum):
    GUI = game_GUI.main
    CLI = game_CLI.main


class PlayerType(Enum):
    Human = 'human'
    RandomAI = 'random-ai'
    MiniMaxAI = 'minimax-ai'
    MiniMaxAlphaBetaAI = 'minimaxab-ai'
    MonteCarloAI = 'monteCarlo-ai'


# These values should be changed
selectedGameType = Board.CLI
playerWhite = PlayerType.RandomAI
playerBlack = PlayerType.MiniMaxAlphaBetaAI
# Launch the game
selectedGameType(playerWhite.value, playerBlack.value)
