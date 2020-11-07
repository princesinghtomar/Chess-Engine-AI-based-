from math import inf
from random import choice
import chess

def tot_dis_from(board: chess.BoardT, target_sq: chess.Square) -> int:
    tot_dis = 0
    for sq in chess.SQUARES:
        pc = board.piece_at(sq)
        if pc and pc.color == board.turn:
            tot_dis += chess.square_distance(target_sq, chess.square_rank(sq))
    return tot_dis


def move_towards_sq(board: chess.BoardT, dest_sq: chess.Square) -> chess.Move:
    moves = list(board.legal_moves)
    min_dist = +inf
    chosen_moves = []
    for move in moves:
        board.push(move)
        dist = tot_dis_from(board, dest_sq)
        if board.is_check():
            dist -= 10
        if board.is_checkmate():
            dist = -inf
        board.pop()
        if dist == min_dist:
            chosen_moves.append(move)
        elif dist < min_dist:
            min_dist = dist
            chosen_moves = [move]
    return choice(chosen_moves)


def defensive_move(board: chess.BoardT) -> chess.Move:
    kingsq = None
    for sq in chess.SQUARES:
        pc = board.piece_at(sq)
        if pc and pc.piece_type == chess.KING and pc.color == board.turn:
            kingsq = sq
            break

    assert kingsq is not None
    return move_towards_sq(board, kingsq)


def attacking_move(board: chess.BoardT) -> chess.Move:
    moves = list(board.legal_moves)
    opp_kingsq = None
    for sq in chess.SQUARES:
        pc = board.piece_at(sq)
        if pc and pc.piece_type == chess.KING and pc.color == board.turn:
            opp_kingsq = sq
            break
    assert opp_kingsq is not None
    return move_towards_sq(board, opp_kingsq)


def random_next_move(board: chess.BoardT) -> chess.Move:
    moves = list(board.legal_moves)
    good_move = None
    for move in moves:
        board.push(move)
        if board.is_check():
            good_move = move
        elif board.is_checkmate():
            board.pop()
            return move
        board.pop()

    if good_move:
        return good_move
    return choice(moves)


def color_fav_move(board: chess.BoardT, fav_color: bool) -> chess.Move:
    moves = list(board.legal_moves)
    good_moves = []
    for move in moves:
        if move.to_square % 2 == fav_color:
            good_moves.append(move)
        board.push(move)
        is_best_move = 0
        if board.is_checkmate():
            is_best_move = 1
        board.pop()
        if is_best_move:
            return move

    if good_moves:
        return choice(good_moves)
    return choice(moves)

def cccp_strategy(board: chess.BoardT) -> chess.Move:
    moves = list(board.legal_moves)
    good_moves = []
    for move in moves:
        board.push(move)
        if board.is_checkmate():
            good_moves.append(move)
        elif board.is_check():
            good_moves.append(move)
        board.pop()
        if good_moves:
            return choice(good_moves)

        if board.is_capture(move):
            return move
        else:
            good_moves.append(move)
    
    return choice(good_moves)

