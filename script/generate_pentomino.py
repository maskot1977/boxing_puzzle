import os
from boxing_puzzle import boxing2

os.system("mkdir pentomino/")
for i, matrix in enumerate(find_some()):
    pd.DataFrame(matrix).to_csv("pentomino/{}.csv".format(i))
