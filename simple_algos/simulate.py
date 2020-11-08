import main
from algos import strategies_list

matches_per_pair = 200

scores = {name: 0 for name in strategies_list}

for wname, wway in strategies_list.items():
    for bname, bway in strategies_list.items():
        print(f"{wname} vs {bname}")
        for _ in range(matches_per_pair):
            final_board = main.main(wway, bway, False)
            if final_board.result() == '0-1':
                scores[bname] += 1
            elif final_board.result() == '1-0':
                scores[wname] += 1


for name, score in scores.items():
    print(name, score)

"""
writing an output here to avoid running again and again for analysis
(max score): 1400
defensive 768
attacking 790
random 350
alphabetic 82
cccp 863
black_sq 688
white_sq 524
"""
