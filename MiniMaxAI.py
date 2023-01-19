import math

import Poddavki
import time
import random


def getTurn(game: Poddavki):
    return move(game, game.getPlayer(), 6, False, True)


def getTurnAB(game: Poddavki):
    turn = move(game, game.getPlayer(), 7, True, True)
    return turn


def move(game, color, depth, alphabeta, rand, verbose=False):
    colors = ('white', 'black')
    time1 = time.perf_counter()
    if alphabeta:
        (eval, move), c = alpha_beta(game, True, 0, depth, -math.inf, math.inf,
                                     colors if color == 'white' else colors[::-1],
                                     rand, 1)
    else:
        (eval, move), c = minimax(game, True, 0, depth, colors if color == 'white' else colors[::-1],
                                  rand, 1)
        # (eval, move), c = minimax(game, True, depth, depth, alphabeta, 0, colors if color == 'white' else colors[::-1],
        #                           rand, 1)
    total_time = time.perf_counter() - time1
    if verbose:
        print(f"Nodes visited: {c}, time elapsed: {total_time}, time per node: {total_time / c}, eval: {eval}")
    return move


def alt_minimax(game, maxPlayer, depth, maxDepth, alphabeta, prevEval, colors, rand, c):
    if depth == 0:
        return (evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]), None), c
    if not game.hasAvailableMoves() and (depth == maxDepth or depth == maxDepth - 1):
        return (70, None) if maxPlayer else (-70, None), c
    if not game.hasAvailableMoves():
        return (50, None) if maxPlayer else (-50, None), c
    if game.draw:
        return (0, None), c

    best = (-100 if maxPlayer else 100, None)
    moves = game.getPossibleMoves(colors[0] if maxPlayer else colors[1])

    if rand:
        random.shuffle(moves)

    for move in moves:
        if best[0] == 70:
            break

        if alphabeta and (maxPlayer and prevEval <= best[0] or not maxPlayer and prevEval >= best[0]):
            break

        gameCopy = game.copyGame()
        gameCopy.applyMove(move)
        eval, c = alt_minimax(gameCopy, not maxPlayer, depth if maxPlayer else depth - 1, maxDepth, alphabeta, best[0],
                              colors, rand, c + 1)

        if maxPlayer and best[0] < eval[0]:
            best = (eval[0], move)
        elif not maxPlayer and best[0] > eval[0]:
            best = (eval[0], move)
    return best, c


def minimax(game, maxPlayer, depth, maxDepth, colors, rand, c):
    if depth == maxDepth:
        if maxPlayer:
            return (evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]) - depth, None), c
        else:
            return (-evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]) + depth, None), c
    if not game.hasAvailableMoves():
        return (50 - depth, None) if maxPlayer else (-50 + depth, None), c
    if game.draw:
        return 0, None

    best = (-100 if maxPlayer else 100, None)
    moves = game.getPossibleMoves(colors[0] if maxPlayer else colors[1])

    if rand:
        random.shuffle(moves)

    if maxPlayer:
        for move in moves:
            gameCopy = game.copyGame()
            gameCopy.applyMove(move)
            score, c = minimax(gameCopy, not maxPlayer, depth + 1, maxDepth, colors, rand, c + 1)
            if score[0] > best[0]:
                best = (score[0], move)
        return best, c
    else:
        for move in moves:
            gameCopy = game.copyGame()
            gameCopy.applyMove(move)
            score, c = minimax(gameCopy, not maxPlayer, depth + 1, maxDepth,  colors, rand, c + 1)
            if score[0] < best[0]:
                best = (score[0], move)
        return best, c


def alpha_beta(game, maxPlayer, depth, maxDepth, alpha, beta, colors, rand, c):
    if depth == maxDepth:
        if maxPlayer:
            return (evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]) - depth, None), c
        else:
            return (-evaluatePosition(game.getBoard(), colors[0] if maxPlayer else colors[1]) + depth, None), c
    if not game.hasAvailableMoves():
        return (50 - depth, None) if maxPlayer else (-50 + depth, None), c
    if game.draw:
        return 0, None

    best = (-100 if maxPlayer else 100, None)
    moves = game.getPossibleMoves(colors[0] if maxPlayer else colors[1])

    if rand:
        random.shuffle(moves)

    if maxPlayer:
        for move in moves:
            gameCopy = game.copyGame()
            gameCopy.applyMove(move)
            score, c = alpha_beta(gameCopy, not maxPlayer, depth + 1, maxDepth, alpha, beta, colors, rand, c + 1)
            if score[0] > best[0]:
                best = (score[0], move)
            if best[0] > beta:
                break
            alpha = max(alpha, best[0])
        return best, c
    else:
        for move in moves:
            gameCopy = game.copyGame()
            gameCopy.applyMove(move)
            score, c = alpha_beta(gameCopy, not maxPlayer, depth + 1, maxDepth, alpha, beta, colors, rand, c + 1)
            if score[0] < best[0]:
                best = (score[0], move)
            if best[0] < alpha:
                break
            beta = max(beta, best[0])
        return best, c


def evaluatePosition(board, playerColor):
    KING_VALUE = 0
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
