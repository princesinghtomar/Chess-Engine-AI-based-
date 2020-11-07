from random import seed
import chess
from chess import BLACK, WHITE
from algos import color_fav_move, defensive_move, random_next_move, attacking_move, cccp_strategy, alphabetic
from time import sleep

board = chess.Board()

# seed(0)
move_count = 0
print(move_count, ":")
print(board)
while not board.is_game_over():
    if board.turn == chess.WHITE:
        board.push(alphabetic(board))
    else:
        board.push(attacking_move(board))
    move_count += 1
    print(move_count, ":")
    print(board)
    # sleep(0.005)
    # input()

print(f"\n\nResult: {move_count}")
print(board.result())
