# import chess
import random
from math import inf
from time import time
from typing import Tuple
from ChessEngine import GameState, Move
from Evaluation import evaluate_board


def evaluate(board: GameState, for_white: bool) -> int:
    """
        returns an integer score representing current state of the board.
        Higher number is in favour of player given.
    """
    ret = evaluate_board(board.board)
    if not for_white:
        ret *= -1
    return ret


def minimax(board: GameState, alpha: float, beta: float, maximizer: bool, curDepth: int, max_depth: int) -> Tuple[float, Move]:
    """
        returns an integer score and move which is the best current player can get
    """
    if board.is_game_over() or curDepth == max_depth:
        return evaluate(board, board.whiteToMove), None

    # sending inf so that the branch is ignored by parent
    if final_move is not None and time() - stime > timeout:
        return +inf if maximizer else -inf, None

    moves = list(board.getValidMoves())
    assert moves != []
    best_move = None
    if maximizer:
        best_score = -inf

        def is_better_score(curr, currbest):
            return curr > currbest

        def update_AB(score):
            nonlocal alpha
            alpha = max(alpha, score)

    else:
        best_score = +inf

        def is_better_score(curr, currbest):
            return curr < currbest

        def update_AB(score):
            nonlocal beta
            beta = min(beta, score)

    for move in moves:
        board.makeMove(move, by_AI=True)
        curr_score, _ = minimax(
            board, alpha, beta, not maximizer, curDepth+1, max_depth)
        board.undoMove()
        if is_better_score(curr_score, best_score):
            best_score = curr_score
            best_move = move
            update_AB(best_score)
            if alpha >= beta:
                break

    return best_score, best_move


def next_move_restricted(board: GameState, max_depth: int) -> Tuple[float, Move]:
    """
        returns best move calculated till depth given
    """
    score, move = minimax(board, alpha=-inf, beta=+inf,
                          maximizer=True, curDepth=0, max_depth=max_depth)
    if not move:
        return -inf, None
    return score, move


def next_move(board: GameState) -> Move:
    """
        returns best move calculated till timeout
    """
    global timeout, stime, final_move
    initial_depth = 4
    depth_extension_limit = 10
    timeout = .5  # in seconds
    final_move = None
    stime = time()
    assert not board.is_game_over()

    final_score, final_move = next_move_restricted(
        board, max_depth=initial_depth)

    for extension in range(1, depth_extension_limit):
        if time() - stime >= timeout:
            break
        score, move = next_move_restricted(
            board, max_depth=initial_depth+extension)
        if move is not None and score > final_score:
            final_score, final_move = score, move

    return final_move
