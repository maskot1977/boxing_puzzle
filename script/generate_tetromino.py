import os
import pandas as pd

from boxing_puzzle import boxing2

os.system("mkdir tetromino/")
for i, matrix in enumerate(boxing2.find_some(
        x_length = 8,
        y_length = 5,
        piece_size = 4,
        same_piece_limit = 2,
        max_trial = 530000
    )):
    pd.DataFrame(matrix).to_csv("tetromino/{}.csv".format(i))
