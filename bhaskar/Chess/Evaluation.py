
# Global Variables

pawn_value = 100
knight_value = 300
bishop_value = 300
rook_value = 500
queen_value = 900
king_value = 10000

W = 0
B = 1

pawn_phase_val = 0
knight_phase_val = 1
bishop_phase_val = 1
rook_phase_val = 2
queen_phase_val = 4


def initialize(board):
    """
    initialize variables for evaluation
    """
    global p, n, b, r, q, k, pos_p, pos_n, pos_b, pos_r, pos_q, pos_k
    p = [0, 0]
    n = [0, 0]
    b = [0, 0]
    r = [0, 0]
    q = [0, 0]
    k = [0, 0]
    pos_p = [[], []]
    pos_n = [[], []]
    pos_b = [[], []]
    pos_r = [[], []]
    pos_q = [[], []]
    pos_k = [[], []]
    for i in range(8):
        for j in range(8):
            square = board[i][j]
            if square == "wp":
                pos_p[W].append((i, j))
                p[W] += 1
            elif square == "wN":
                pos_n[W].append((i, j))
                n[W] += 1
            elif square == "wB":
                pos_b[W].append((i, j))
                b[W] += 1
            elif square == "wR":
                pos_r[W].append((i, j))
                r[W] += 1
            elif square == "wQ":
                pos_q[W].append((i, j))
                q[W] += 1
            elif square == "wK":
                pos_k[W].append((i, j))
                k[W] += 1
            elif square == "bp":
                pos_p[B].append((7-i, 7-j))
                p[B] += 1
            elif square == "bN":
                pos_n[B].append((7-i, 7-j))
                n[B] += 1
            elif square == "bB":
                pos_b[B].append((7-i, 7-j))
                b[B] += 1
            elif square == "bR":
                pos_r[B].append((7-i, 7-j))
                r[B] += 1
            elif square == "bQ":
                pos_q[B].append((7-i, 7-j))
                q[B] += 1
            elif square == "bK":
                pos_k[B].append((7-i, 7-j))
                k[B] += 1
            else:
                pass


pawn_mg = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-6, -4, 1, 1, 1, 1, -4, -6],
    [-6, -4, 1, 2, 2, 1, -4, -6],
    [-6, -4, 2, 8, 8, 2, -4, -6],
    [-6, -4, 5, 10, 10, 5, -4, -6],
    [-4, -4, 1, 5, 5, 1, -4, -4],
    [-6, -4, 1, -24, -24, 1, -4, -6],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

pawn_eg = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-6, -4, 1, 1, 1, 1, -4, -6],
    [-6, -4, 1, 2, 2, 1, -4, -6],
    [-6, -4, 2, 8, 8, 2, -4, -6],
    [-6, -4, 5, 10, 10, 5, -4, -6],
    [-4, -4, 1, 5, 5, 1, -4, -4],
    [-6, -4, 1, -24, -24, 1, -4, -6],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knight_mg = [
    [-8, -8, -8, -8, -8, -8, -8, -8],
    [-8, 0, 0, 0, 0, 0, 0, -8],
    [-8, 0, 4, 4, 4, 4, 0, -8],
    [-8, 0, 4, 8, 8, 4, 0, -8],
    [-8, 0, 4, 8, 8, 4, 0, -8],
    [-8, 0, 4, 4, 4, 4, 0, -8],
    [-8, 0, 1, 2, 2, 1, 0, -8],
    [-8, -12, -8, -8, -8, -8, -12, -8]
]

knight_eg = [
    [-8, -8, -8, -8, -8, -8, -8, -8],
    [-8, 0, 0, 0, 0, 0, 0, -8],
    [-8, 0, 4, 4, 4, 4, 0, -8],
    [-8, 0, 4, 8, 8, 4, 0, -8],
    [-8, 0, 4, 8, 8, 4, 0, -8],
    [-8, 0, 4, 4, 4, 4, 0, -8],
    [-8, 0, 1, 2, 2, 1, 0, -8],
    [-8, -12, -8, -8, -8, -8, -12, -8]
]

bishop_mg = [
    [-4, -4, -4, -4, -4, -4, -4, -4],
    [-4, 0, 0, 0, 0, 0, 0, -4],
    [-4, 0, 2, 4, 4, 2, 0, -4],
    [-4, 0, 4, 6, 6, 4, 0, -4],
    [-4, 0, 4, 6, 6, 4, 0, -4],
    [-4, 1, 2, 4, 4, 2, 1, -4],
    [-4, 2, 1, 1, 1, 1, 2, -4],
    [-4, -4, -12, -4, -4, -12, -4, -4]
]

bishop_eg = [
    [-4, -4, -4, -4, -4, -4, -4, -4],
    [-4, 0, 0, 0, 0, 0, 0, -4],
    [-4, 0, 2, 4, 4, 2, 0, -4],
    [-4, 0, 4, 6, 6, 4, 0, -4],
    [-4, 0, 4, 6, 6, 4, 0, -4],
    [-4, 1, 2, 4, 4, 2, 1, -4],
    [-4, 2, 1, 1, 1, 1, 2, -4],
    [-4, -4, -12, -4, -4, -12, -4, -4]
]

rook_mg = [
    [5, 5, 5, 5, 5, 5, 5, 5],
    [20, 20, 20, 20, 20, 20, 20, 20],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 2, 2, 0, 0, 0]
]

rook_eg = [
    [5, 5, 5, 5, 5, 5, 5, 5],
    [20, 20, 20, 20, 20, 20, 20, 20],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 2, 2, 0, 0, 0]
]

queen_mg = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 2, 3, 3, 2, 0, 0],
    [0, 0, 2, 3, 3, 2, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [-5, -5, -5, -5, -5, -5, -5, -5]
]

queen_eg = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 2, 3, 3, 2, 0, 0],
    [0, 0, 2, 3, 3, 2, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [-5, -5, -5, -5, -5, -5, -5, -5]
]

king_mg = [
    [-40, -30, -50, -70, -70, -50, -30, -40],
    [-30, -20, -40, -60, -60, -40, -20, -30],
    [-20, -10, -30, -50, -50, -30, -10, -20],
    [-10, 0, -20, -40, -40, -20, 0, -10],
    [0, 10, -10, -30, -30, -10, 10, 0],
    [10, 20, 0, -20, -20, 0, 20, 10],
    [30, 40, 20, 0, 0, 20, 40, 30],
    [40, 50, 30, 10, 10, 30, 50, 40]
]

king_eg = [
    [-72, -48, -36, -24, -24, -36, -48, -72],
    [-48, -24, -12, 0, 0, -12, -24, -48],
    [-36, -12, 0, 12, 12, 0, -12, -36],
    [-24, 0, 12, 24, 24, 12, 0, -24],
    [-24, 0, 12, 24, 24, 12, 0, -24],
    [-36, -12, 0, 12, 12, 0, -12, -36],
    [-48, -24, -12, 0, 0, -12, -24, -48],
    [-72, -48, -36, -24, -24, -36, -48, -72]
]

weak_pawn_pcsq = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-10, -12, -14, -16, -16, -14, -12, -10],
    [-10, -12, -14, -16, -16, -14, -12, -10],
    [-10, -12, -14, -16, -16, -14, -12, -10],
    [-10, -12, -14, -16, -16, -14, -12, -10],
    [-8, -12, -14, -16, -16, -14, -12, -10],
    [-8, -12, -14, -16, -16, -14, -12, -10],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

passed_pawn_pcsq = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [80, 80, 80, 80, 80, 80, 80, 80],
    [60, 60, 60, 60, 60, 60, 60, 60],
    [40, 40, 40, 40, 40, 40, 40, 40],
    [20, 20, 20, 20, 20, 20, 20, 20],
    [20, 20, 20, 20, 20, 20, 20, 20],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


def material(c):
    """
    Calculate and return material value for given color
    """
    eval = p[c] * pawn_value + n[c]*knight_value + b[c] * \
        bishop_value + r[c]*rook_phase_val + q[c]*queen_value + k[c]*king_value
    return eval


def pawn_structure_mg(c):
    """
    Calculate midgame pawn evaluation on basis of structure for color c
    """
    eval = p[c] * pawn_value
    for pos in pos_p[c]:
        eval += pawn_mg[pos[0]][pos[1]]
    return eval


def eval_knight_mg(c):
    """
    Calculate midgame knight evaluation for color c
    """
    eval = n[c] * knight_value
    for pos in pos_n[c]:
        eval += knight_mg[pos[0]][pos[1]]
    return eval


def eval_bishop_mg(c):
    """
    Calculate midgame bishop evaluation for color c
    """
    eval = b[c] * bishop_value
    for pos in pos_b[c]:
        eval += bishop_mg[pos[0]][pos[1]]
    return eval


def eval_rook_mg(c):
    """
    Calculate midgame rook evaluation for color c
    """
    eval = r[c] * rook_value
    for pos in pos_r[c]:
        eval += rook_mg[pos[0]][pos[1]]
    return eval


def eval_queen_mg(c):
    """
    Calculate midgame queen evaluation for color c
    """
    eval = q[c] * queen_value
    for pos in pos_q[c]:
        eval += queen_mg[pos[0]][pos[1]]
    return eval


def eval_king_mg(c):
    """
    Calculate midgame king evaluation for color c
    """
    eval = k[c] * king_value
    for pos in pos_k[c]:
        eval += king_mg[pos[0]][pos[1]]
    return eval


def mid_game():
    """
    Returns Mid game evaluation for the current board state
    """
    eval = (pawn_structure_mg(W) - pawn_structure_mg(B)) + \
        (eval_knight_mg(W) - eval_knight_mg(B)) + \
        (eval_bishop_mg(W) - eval_bishop_mg(B)) + \
        (eval_rook_mg(W) - eval_rook_mg(B)) + \
        (eval_queen_mg(W) - eval_queen_mg(B)) + \
        (eval_king_mg(W) - eval_king_mg(B))
    return eval


def pawn_structure_eg(c):
    """
    Calculate endgame pawn evaluation on basis of structure for color c
    """
    eval = p[c] * pawn_value
    for pos in pos_p[c]:
        eval += pawn_eg[pos[0]][pos[1]]
    return eval


def eval_knight_eg(c):
    """
    Calculate endgame knight evaluation for color c
    """
    eval = n[c] * knight_value
    for pos in pos_n[c]:
        eval += knight_eg[pos[0]][pos[1]]
    return eval


def eval_bishop_eg(c):
    """
    Calculate endgame bishop evaluation for color c
    """
    eval = b[c] * bishop_value
    for pos in pos_b[c]:
        eval += bishop_eg[pos[0]][pos[1]]
    return eval


def eval_rook_eg(c):
    """
    Calculate endgame rook evaluation for color c
    """
    eval = r[c] * rook_value
    for pos in pos_r[c]:
        eval += rook_eg[pos[0]][pos[1]]
    return eval


def eval_queen_eg(c):
    """
    Calculate endgame queen evaluation for color c
    """
    eval = q[c] * queen_value
    for pos in pos_q[c]:
        eval += queen_eg[pos[0]][pos[1]]
    return eval


def eval_king_eg(c):
    """
    Calculate endgame king evaluation for color c
    """
    eval = k[c] * king_value
    for pos in pos_k[c]:
        eval += king_eg[pos[0]][pos[1]]
    return eval


def end_game():
    """
    Returns end game evaluation for the current board state
    """
    eval = (pawn_structure_eg(W) - pawn_structure_eg(B)) + \
        (eval_knight_eg(W) - eval_knight_eg(B)) + \
        (eval_bishop_eg(W) - eval_bishop_eg(B)) + \
        (eval_rook_eg(W) - eval_rook_eg(B)) + \
        (eval_queen_eg(W) - eval_queen_eg(B)) + \
        (eval_king_eg(W) - eval_king_eg(B))
    return eval


def calc_phase():
    """
    Calculates a number between 1 and 128 representing the phase of the game
    """
    tmax = 4 * (bishop_phase_val + knight_phase_val +
                rook_phase_val) + 2 * queen_phase_val
    tmin = 0
    phase = 0
    for i in range(2):
        phase += b[i] * bishop_phase_val + n[i] * knight_phase_val + \
            r[i] * rook_phase_val + q[i] * queen_phase_val
    ret = (phase * 128 + 8) // (tmax - tmin)
    return ret


def evaluate_board(board):
    """
    Gives an integer that tells the evaluation of the current board state
    """
    initialize(board)
    # print(p, n, b, r, q, k)
    # print(pos_p, pos_n, pos_b, pos_r, pos_q, pos_k)
    phase = calc_phase()
    mid_val = mid_game()
    end_val = end_game()
    # print(phase, mid_val, end_val)
    # ks = king_safety()
    ret = (mid_val * phase + (128 - phase) * end_val) / 128
    return ret


# For testing
# board = [
#     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
#     ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
#     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
# print(evaluate(board))
