import random
import matplotlib.pyplot as plt
import numpy as np

def enumerate(
    x_length = 8,
    y_length = 5,
    piece_size = 4,
    same_piece_limit = 2,
    max_trial = 530000
    ):
    
    best_score = x_length * y_length
    best_matrix = generate(x_length, y_length)

    for trial in range(max_trial):
        matrix = generate(x_length, y_length)
        count = {}
        piece_id = 0
        piece = get_new_piece(matrix, piece_size)
        key = shape_key(piece)
        count[key] = 1

        while len(piece) == piece_size:
            for x, y in piece:
                matrix[y][x] = piece_id

            piece = get_new_piece(matrix, piece_size)
            key = shape_key(piece)
            if key not in count.keys():
                count[key] = 0
            count[key] += 1
            if count[key] > same_piece_limit:
                break

            piece_id += 1

        score = sum([sum([1 if x == -1 else 0 for x in mat]) for mat in matrix])

        if best_score > score:
            best_score = score
            best_matrix = matrix

        if score == 0:
            print(trial, "th trial")
            return best_matrix
            break

def generate(x, y):
    return [[-1 for _ in range(x)] for _ in range(y)]

def get_new_piece(matrix, piece_size):
    x_length = len(matrix[0])
    y_length = len(matrix)
    piece = []

    for x in range(x_length):
        for y in range(y_length):
            if matrix[y][x] == -1:
                piece.append([x, y])
                break
        if len(piece) > 0:
            break

    for i in range(piece_size - 1):
        neighbors = get_rand_neighbor(piece, matrix)
        random.shuffle(neighbors)
        for x, y in neighbors:
            if [x, y] not in piece:
                piece.append([x, y])
                break

    return piece

def get_rand_neighbor(piece, matrix):
    neighbors = []
    for x, y in piece:
        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            if x - dx < 0 or x - dx >= len(matrix[0]):
                pass
            elif y - dy < 0 or y - dy >= len(matrix):
                pass
            elif matrix[y - dy][x - dx] == -1:
                neighbors.append([x - dx, y - dy])

    return neighbors

def shape_key(piece):
    distances = []
    for i in range(len(piece)):
        xy1 = piece[i]
        for j in range(len(piece)):
            if i < j:
                xy2 = piece[j]
                distance = (xy1[0] - xy2[0])**2 + (xy1[1] - xy2[1])**2
                distances.append(distance)
    return "".join(str(sorted(distances)))

def depict(matrix, figname=False):
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.gist_ncar)
    plt.xticks(np.arange(len(matrix[0])), range(len(matrix[0])), rotation=90)
    plt.yticks(np.arange(len(matrix)), range(len(matrix)))
    plt.tight_layout()
    if figname:
        plt.savefig(figname)
    plt.show()
