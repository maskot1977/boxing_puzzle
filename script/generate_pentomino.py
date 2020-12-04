import os
import pandas as pd

from boxing_puzzle import boxing2

os.system("mkdir pentomino/")
for i, matrix in enumerate(boxing2.find_some(
        x_length = 10,
        y_length = 6,
        piece_size = 5,
        same_piece_limit = 1,
        max_trial = 530000
    )):
    pd.DataFrame(matrix).to_csv("pentomino/{}.csv".format(i))
