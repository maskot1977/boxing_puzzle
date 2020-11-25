from boxing_puzzle import boxing

for trial in range(10):
    matrix = boxing.find_one(
        x_length = 10,
        y_length = 6,
        piece_size = 5,
        same_piece_limit = 1,
        max_trial = 53000000000
    )
    boxing.depict(matrix, "tetramino_{}.png".format(trial))
