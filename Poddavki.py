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

    def getPieceLocations(self):
        positions = []
        for row, rowValues in enumerate(self.board):
            for col, piece in enumerate(rowValues):
                if piece in ['b', 'bk', 'w', 'wk']:
                    positions.append((row, col))
        return positions

    @staticmethod
    def isInBounds(row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def applyMove(self, moves):
        new_board = list(map(list, self.board))
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
        #self.board = tuple(map(tuple, new_board))
        return tuple(map(tuple, new_board))
    def getRegularMoves(self, row, col):
        moves = []
        startingLoc = (row, col)
        piece = self.board[row][col]
        match piece:
            case 'b':
                moves = [(row + 1, col - 1), (row + 1, col + 1)]
            case 'w':
                moves = [(row - 1, col + 1), (row - 1, col - 1)]
            case 'wk' | 'bk':
                moves = [(row + 1, col - 1), (row + 1, col + 1), (row - 1, col + 1), (row - 1, col - 1)]

        possibleMoves = []
        for row, col in moves:
            if self.isInBounds(row, col) and self.board[row][col] == '':
                possibleMoves.append((startingLoc, (row, col)))
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
            if self.isInBounds(row, col) and board[row][col] in opponentPieces:
                row, col = take_piece
                if self.isInBounds(row, col) and board[row][col] == '':
                    skipMoves.append((startPosition, regular_move, take_piece))
        return skipMoves

    def getSkips(self, row, col):
        possibleMoves = []

        skips = self.getNextSkips(self.board, row, col)
        while skips:
            move = skips.pop()
            nextSkips = self.getNextSkips(self.applyMove(move), *move[-1])
            if nextSkips:
                for startingPosition, enemyPiece, nextPosition in nextSkips:
                    skips.append(move + (enemyPiece, nextPosition))
            else:
                possibleMoves.append(move)
        return possibleMoves

    def getPossibleMoves(self, row, col):
        skips = self.getSkips(row, col)
        if skips:
            return skips
        return self.getRegularMoves(row, col)

    def getAllMoves(self, player):
        availableMoves = []
        if player == 'white':
            pieces = ['w', 'wk']
        else:
            pieces = ['b', 'bk']
        for row, rowValues in enumerate(self.board):
            for col, piece in enumerate(rowValues):
                if piece in pieces:
                    availableMoves.append(self.getPossibleMoves(row, col))
        return availableMoves

    def switchPlayer(self):
        if self.to_move == 'white':
            return 'black'
        else:
            return 'white'
    def hasAvailableMoves(self):
        availableMoves = self.getAllMoves(self.to_move)
        return len(availableMoves) > 0

    def getWinner(self):
        return self.switchPlayer()