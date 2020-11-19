from math import inf
from random import choice
import chess
from chess import BLACK, WHITE


def move_towards_sq(board: chess.BoardT, dest_sq: chess.Square) -> chess.Move:
    def tot_dis_from(board: chess.BoardT, target_sq: chess.Square) -> int:
        tot_dis = 0
        for sq in chess.SQUARES:
            pc = board.piece_at(sq)
            if pc and pc.color == board.turn:
                tot_dis += chess.square_distance(target_sq,
                                                 chess.square_rank(sq))
        return tot_dis

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


def black_sq_move(board: chess.BoardT) -> chess.Move:
    return color_fav_move(board, BLACK)


def white_sq_move(board: chess.BoardT) -> chess.Move:
    return color_fav_move(board, WHITE)

def cccp_strategy(board: chess.BoardT) -> chess.Move:
    moves = list(board.legal_moves)
    ckmate_moves = []
    capture_moves = []
    check_moves = []
    max_pushed_move = None
    max_push_dist = -inf

    def dist_from_homeborder(col: chess.Color) -> int:
        home_row = 0 if col == WHITE else 7
        sum = 0
        for sq in chess.SQUARES:
            pc = board.piece_at(sq)
            if pc and pc.color == col:
                sum += abs(chess.square_rank(sq) - home_row)
        return sum

    for move in moves:
        board.push(move)
        if board.is_checkmate():
            ckmate_moves.append(move)
        elif board.is_check():
            check_moves.append(move)
        board.pop()
        if board.is_capture(move):
            capture_moves.append(move)

        if [] == ckmate_moves == check_moves == capture_moves:
            board.push(move)
            push_dist = dist_from_homeborder(not board.turn)
            if push_dist > max_push_dist:
                max_push_dist = push_dist
                max_pushed_move = move
            board.pop()

    for q in [ckmate_moves, check_moves, capture_moves]:
        if q:
            return choice(q)

    return max_pushed_move


def alphabetic(board: chess.BoardT) -> chess.Move:
    moves = list(board.legal_moves)
    good_moves_checkmate = []
    good_moves_check = []
    good_moves = []
    for move in moves:
        board.push(move)
        if board.is_checkmate():
            good_moves_checkmate.append(move)
        elif board.is_check():
            good_moves_check.append(move)
        board.pop()

    return_val = []
    if good_moves_checkmate!=[] and good_moves_check!=[] :
        return_val.append(good_moves_check[0])
        return_val.append(good_moves_checkmate[0])
        return choice(return_val) 
    elif good_moves_checkmate :
        return good_moves_checkmate[0]
    elif good_moves_check :
        return good_moves_check[0]
    
    return moves[0]


# all these are functions which take parameter 'board' only
# and return the move based in strategy
# thus a generalised strategy function can be called as stragegy(board)
strategies_list = {
    "alphabetic": alphabetic,
    "black_sq": black_sq_move,
    "white_sq": white_sq_move,
    "random": random_next_move,
    "defensive": defensive_move,
    "attacking": attacking_move,
    "cccp": cccp_strategy,
}
