import copy
from tabulate import tabulate


class Poddavki:
    def __init__(self):
        self.board = (
            ('', 'b', '', 'b', '', 'b', '', 'b'),
            ('b', '', 'b', '', 'b', '', 'b', ''),
            ('', 'b', '', 'b', '', 'b', '', 'b'),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('w', '', 'w', '', 'w', '', 'w', ''),
            ('', 'w', '', 'w', '', 'w', '', 'w'),
            ('w', '', 'w', '', 'w', '', 'w', ''),
        )
        self.to_move = 'white'

    def getBoard(self):
        return copy.deepcopy(self.board)

    def getPieceLocations(self, type='all'):
        positions = []
        for row, rowValues in enumerate(self.board):
            for col, piece in enumerate(rowValues):
                if type == 'all' and piece in ['b', 'bk', 'w', 'wk']:
                    positions.append((row, col))
                elif type == 'white' and piece in ['w', 'wk']:
                    positions.append((row, col))
                elif type == 'black' and piece in ['b', 'bk']:
                    positions.append((row, col))
        return positions

    def getPlayer(self):
        return self.to_move

    def copyGame(self):
        new_game = Poddavki()
        new_game.board = self.board
        new_game.to_move = self.to_move
        return new_game

    @staticmethod
    def isInBounds(row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def applyMove(self, moves):
        self.board = self.getNextBoardState(moves)
        self.switchPlayer()

    def getNextBoardState(self, moves):
        new_board = [[*row] for row in self.board]
        start_row, start_col = moves[0]
        end_row, end_col = moves[-1]
        piece = self.board[start_row][start_col]

        for row, col in moves:
            if row == 0 and piece == 'w':
                piece = 'wk'
            if row == 7 and piece == 'b':
                piece = 'bk'
            new_board[row][col] = ''

        new_board[end_row][end_col] = piece
        return tuple(map(tuple, new_board))

    def getRegularMoves(self, row, col):
        moves = []
        directions = []
        startingLoc = (row, col)
        piece = self.board[row][col]
        match piece:
            case 'b':
                moves = [(row + 1, col - 1), (row + 1, col + 1)]
            case 'w':
                moves = [(row - 1, col + 1), (row - 1, col - 1)]
            case 'wk' | 'bk':
                directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        possibleMoves = []
        for row, col in moves:
            if self.isInBounds(row, col) and self.board[row][col] == '':
                possibleMoves.append((startingLoc, (row, col)))
        for r, c in directions:
            for i in range(1, 8):
                new_row = row + i * r
                new_col = col + i * c
                if self.isInBounds(new_row, new_col) and self.board[new_row][new_col] == '':
                    possibleMoves.append((startingLoc, (new_row, new_col)))
                else:
                    break
        return possibleMoves

    def printBoard(self):
        print(tabulate(self.board))

    @staticmethod
    def translateMove(move):
        rowMove = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
        colMove = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        result = ''
        if len(move) == 2:
            for row, col in move:
                result += f'{colMove[col]}{rowMove[row]}-'
        else:
            for row, col in move[::2]:
                result += f'{colMove[col]}{rowMove[row]}:'
        return result[:-1]

    def getNextSkips(self, board, row, col):
        startPosition = (row, col)
        piece = board[row][col]
        locations = []
        directions = []
        if piece in ['b', 'bk']:
            opponentPieces = ['w', 'wk']
            friendlyPieces = ['b', 'bk']
        else:
            opponentPieces = ['b', 'bk']
            friendlyPieces = ['w', 'wk']
        match piece:
            case 'b':
                locations = [((row + 1, col - 1), (row + 2, col - 2)), ((row + 1, col + 1), (row + 2, col + 2))]
            case 'w':
                locations = [((row - 1, col + 1), (row - 2, col + 2)), ((row - 1, col - 1), (row - 2, col - 2))]
            case 'wk' | 'bk':
                directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        skipMoves = []

        for enemyPosition, nextPosition in locations:
            row, col = enemyPosition
            if self.isInBounds(row, col) and board[row][col] in opponentPieces:
                row, col = nextPosition
                if self.isInBounds(row, col) and board[row][col] == '':
                    skipMoves.append((startPosition, enemyPosition, nextPosition))

        for r, c in directions:
            for i in range(1, 8):
                enemyPosition = (row + i * r, col + i * c)
                row_1, col_1 = enemyPosition
                if self.isInBounds(row_1, col_1):
                    if board[row_1][col_1] in friendlyPieces:
                        break
                    if board[row_1][col_1] in opponentPieces:
                        for j in range(i + 1, 7):
                            nextPosition = (row + j * r, col + j * c)
                            row_2, col_2 = nextPosition
                            if self.isInBounds(row_2, col_2):
                                if board[row_2][col_2] == '':
                                    skipMoves.append((startPosition, enemyPosition, nextPosition))
                                else:
                                    break  # can't move past other pieces
                            else:
                                break  # out of bounds
                        break  # took opponent's piece
                else:
                    break  # out of bounds
        return skipMoves

    def getSkips(self, row, col):
        possibleMoves = []

        skips = self.getNextSkips(self.board, row, col)
        while skips:
            move = skips.pop()
            nextSkips = self.getNextSkips(self.getNextBoardState(move), *move[-1])
            if nextSkips:
                for startingPosition, enemyPiece, nextPosition in nextSkips:
                    skips.append(move + (enemyPiece, nextPosition))
            else:
                possibleMoves.append(move)
        return possibleMoves

    def getPossibleMoves(self, player):
        availableMoves = []
        if player == 'white':
            pieces = ['w', 'wk']
        else:
            pieces = ['b', 'bk']
        for row, rowValues in enumerate(self.board):
            for col, piece in enumerate(rowValues):
                if piece in pieces:
                    moveList = self.getSkips(row, col)
                    if moveList:
                        for move in moveList:
                            availableMoves.append(move)
        if not availableMoves:
            for row, rowValues in enumerate(self.board):
                for col, piece in enumerate(rowValues):
                    if piece in pieces:
                        moveList = self.getRegularMoves(row, col)
                        if moveList:
                            for move in moveList:
                                availableMoves.append(move)
        return availableMoves

    def getPossibleBoardStates(self, player):
        boardStates = []
        for move in self.getPossibleMoves(player):
            boardStates.append(self.getNextBoardState(move))
        return boardStates

    def switchPlayer(self):
        if self.to_move == 'white':
            self.to_move = 'black'
        else:
            self.to_move = 'white'

    def hasAvailableMoves(self):
        availableMoves = self.getPossibleMoves(self.to_move)
        return len(availableMoves) > 0

    def getWinner(self):
        return self.to_move

    def get_outcome(self):
        white = self.getPossibleMoves('white')
        black = self.getPossibleMoves('black')
        if len(white) == 0 and len(black) == 0:
            return 'draw'

        return 'white' if len(white) == 0 else 'black'
