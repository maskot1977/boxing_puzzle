import os
import pandas as pd

from boxing_puzzle import boxing2

os.system("mkdir tetromino/")
for i, matrix in enumerate(find_some(
        x_length = 10,
        y_length = 6,
        piece_size = 5,
        same_piece_limit = 1,
        max_trial = 5300000
    )):
    pd.DataFrame(matrix).to_csv("tetromino/{}.csv".format(i))
