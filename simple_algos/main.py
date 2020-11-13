from random import random, seed
import chess
from chess import BLACK, WHITE
from algos import color_fav_move, defensive_move, random_next_move, attacking_move, cccp_strategy, alphabetic
from time import sleep


def main(whiteStrategy=random_next_move, blackStrategy=random_next_move, log: bool = True):
    # seed(0)
    board = chess.Board()
    move_count = 0
    if log:
        print(move_count, ":\n", board)

    while not board.is_game_over():
        next_move = None
        if board.turn == chess.WHITE:
            next_move = whiteStrategy(board)
        else:
            next_move = blackStrategy(board)
        board.push(next_move)
        move_count += 1
        if log:
            print(move_count, ":\n", board)
        # sleep(0.005)
        # input()

    if log:
        print(f"\n\nResult: {move_count}\n", board.result())
    return board


if __name__ == '__main__':
    main()
