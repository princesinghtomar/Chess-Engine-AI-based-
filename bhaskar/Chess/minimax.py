from multiprocessing import Process, Pipe, connection
from multiprocessing.connection import Connection
import random
from math import inf
from time import time
from typing import Tuple, List
from ChessEngine import GameState, Move
from Evaluation import evaluate_board


def evaluate(board: GameState, for_white: bool) -> int:
    """
        returns an integer score representing current state of the board.
        Higher number is in favour of player given.
    """
    eval_stime = time()
    ret = (1 if for_white else -1) * evaluate_board(board.board)
    duration = time()-eval_stime
    global eval_time, evals_cnt
    eval_time += duration
    evals_cnt += 1
    # print(f"eval time {duration}")
    return ret


def minimax(board: GameState, moves: List[Move], alpha: float, beta: float, maximizer: bool, curDepth: int, max_depth: int) -> Tuple[float, Move]:
    """
        returns an integer score and move which is the best current player can get
    """
    if board.is_game_over():
        if board.staleMate:
            return 0, None
        if board.checkMate:
            return (-inf if maximizer else +inf), None
    if curDepth == max_depth:
        return evaluate(board, not(board.whiteToMove ^ maximizer)), None

    # sending inf so that the branch is ignored by parent
    if final_move is not None and time() - stime > timeout:
        return +inf if maximizer else -inf, None

    # moves = list(board.getValidMoves())
    assert moves != []
    best_move = None
    if maximizer:
        best_score = -inf

        def is_better_score(curr, currbest):
            return curr >= currbest

        def update_AB(score):
            nonlocal alpha
            alpha = max(alpha, score)

    else:
        best_score = +inf

        def is_better_score(curr, currbest):
            return curr <= currbest

        def update_AB(score):
            nonlocal beta
            beta = min(beta, score)

    for move in moves:
        board.makeMove(move, by_AI=True)
        global moves_cnt
        moves_cnt += 1
        curr_score, _ = minimax(
            board, board.getValidMoves(), alpha, beta, not maximizer, curDepth+1, max_depth)
        board.undoMove()
        if is_better_score(curr_score, best_score):
            best_score = curr_score
            best_move = move
            update_AB(best_score)
            if alpha >= beta:
                break

    return best_score, best_move

def minimax_handler(conn:Connection ,board:GameState,moves_set:List[Move], max_depth:int):
    score, move = minimax(board, moves=moves_set, alpha=-inf, beta=+inf,
                          maximizer=True, curDepth=0, max_depth=max_depth)
    conn.send(score)
    conn.send(move)

def next_move_restricted(board: GameState, max_depth: int) -> Tuple[float, Move]:
    """
        returns best move calculated till depth given
    """
    depth_stime = time()
    global eval_time, moves_cnt, evals_cnt
    eval_time = 0
    moves_cnt = 0
    evals_cnt = 0
    moves = board.getValidMoves()
    length = len(moves)
    step_size = max(1, length//6)
    moves_sets:List[List[Move]] = []
    procs_list:List[Process] = []
    conn_list:List[Connection] = []

    for start in range(0, length, step_size):
        end = start+step_size
        if length-end < step_size:
            end = length
        moves_sets.append(moves[start: end])

    for moves_sb_set in moves_sets:
        par_conn, ch_conn = Pipe()
        p = Process(target=minimax_handler, args=(ch_conn, board,moves_sb_set, max_depth))
        p.start()
        procs_list.append(p)
        conn_list.append(par_conn)
    
    score, move = -inf, None
    for conn in conn_list:
        curr_score:int = conn.recv()
        curr_move:Move = conn.recv()
        if curr_score >= score:
            score, move = curr_score, curr_move

    for p in procs_list:
        p.join()
    

    print(
        f"depth [{max_depth}] done in {time()-depth_stime} score: {score}"
        # f"evals_time : {eval_time}, eval_cnt: {evals_cnt}, moves_cnt: {moves_cnt}"
        )
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
    timeout = 20  # in seconds
    final_move = None
    stime = time()
    assert not board.is_game_over()

    final_score, final_move = next_move_restricted(
        board, max_depth=initial_depth)
    print(f"depth ({initial_depth}) chosen")

    for extension in range(1, depth_extension_limit):
        if time() - stime >= timeout:
            break
        score, move = next_move_restricted(
            board, max_depth=initial_depth+extension)
        if move is not None and score >= final_score:
            final_score, final_move = score, move
            print(f"depth ({initial_depth+extension}) chosen")

    return final_move
