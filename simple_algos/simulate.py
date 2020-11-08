import main
from algos import strategies_list
import random

matches_per_pair = 50

scores = {name: 0 for name in strategies_list}

elo_ratings = {name: 1400 for name in strategies_list}

elo_k = 24

# random.seed(1)


def update_elo(player1: str, player2: str, p1_won: bool):
    rate_diff = elo_ratings[player2] - elo_ratings[player1]
    p1_win_prob = 1 / (1 + 10**(rate_diff/400))
    p1_gain = int(elo_k*(p1_won - p1_win_prob))
    elo_ratings[player1] += p1_gain
    elo_ratings[player2] -= p1_gain


for wname, wway in strategies_list.items():
    for bname, bway in strategies_list.items():
        print(f"{wname} vs {bname}")
        for _ in range(matches_per_pair):
            final_board = main.main(wway, bway, False)
            if final_board.result() == '0-1':
                scores[bname] += 2
                update_elo(wname, bname, 0)
            elif final_board.result() == '1-0':
                scores[wname] += 2
                update_elo(wname, bname, 1)
            else:
                scores[wname] += 1
                scores[bname] += 1
                update_elo(wname, bname, 0.5)


print()
for name, score in sorted(scores.items(), key=lambda tup: tup[1]):
    print(name, score)

print()
for name, elo in sorted(elo_ratings.items(), key=lambda tup: tup[1]):
    print(name, elo)
