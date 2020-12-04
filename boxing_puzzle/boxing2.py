# -*- coding: utf-8 -*-
import copy
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate(x, y):
    return [[0 for _ in range(x)] for _ in range(y)]


def get_new_piece(matrix, piece_size):
    piece = []

    for x in range(x_length):
        for y in range(y_length):
            if matrix[y][x] == 0:
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
            elif matrix[y - dy][x - dx] == 0:
                neighbors.append([x - dx, y - dy])

    return neighbors


def depict(matrix):
    plt.imshow(matrix, interpolation="nearest", cmap=plt.cm.gist_ncar)
    plt.xticks(np.arange(len(matrix[0])), range(len(matrix[0])), rotation=90)
    plt.yticks(np.arange(len(matrix)), range(len(matrix)))
    plt.tight_layout()
    plt.show()


def shape_key(piece):
    distances = []
    adjacents = {}
    for i in range(len(piece)):
        xy1 = piece[i]
        for j in range(len(piece)):
            if i < j:
                xy2 = piece[j]
                distance = (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2
                distances.append(distance)

                if distance == 1:
                    if i not in adjacents.keys():
                        adjacents[i] = []
                    adjacents[i].append(j)
                    if j not in adjacents.keys():
                        adjacents[j] = []
                    adjacents[j].append(i)

    return (
        "".join(str(sorted(distances)))
        + "_"
        + "".join(str(sorted([len(adjacents[k]) for k in adjacents.keys()])))
    )


def get_new_pieces(matrix, x_length, y_length, piece_size):
    piece = []

    for x in range(x_length):
        for y in range(y_length):
            if matrix[y][x] == 0:
                piece.append([x, y])
                break
        if len(piece) > 0:
            break

    result_pieces = []
    waiting = []
    waiting.append(piece)
    while len(waiting) > 0:
        piece = waiting.pop()
        neighbors = get_rand_neighbor(piece, matrix)
        for x, y in neighbors:
            if [x, y] not in piece:
                new_piece = copy.deepcopy(piece)
                new_piece.append([x, y])
                if len(new_piece) == piece_size:
                    new_piece = sorted(new_piece)
                    if new_piece not in result_pieces:
                        result_pieces.append(new_piece)
                else:
                    waiting.append(new_piece)

    return sorted(result_pieces)


def get_connected_subgraphs(matrix):
    neigh = {}
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 0:
                neigh[",".join([str(x), str(y)])] = []
                for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    if x - dx < 0 or x - dx >= len(matrix[0]):
                        pass
                    elif y - dy < 0 or y - dy >= len(matrix):
                        pass
                    elif matrix[y - dy][x - dx] == 0:
                        neigh[",".join([str(x), str(y)])].append([x - dx, y - dy])

    connected_subgraphs = []
    found = []
    for k, v in neigh.items():
        if k in found:
            continue
        connected_subgraph = [k]
        waiting = list(v)
        found.append(k)
        while len(waiting):
            x, y = waiting.pop()
            n = ",".join([str(x), str(y)])
            if n in found:
                continue
            connected_subgraph.append(n)
            found.append(n)
            if n in neigh.keys():
                waiting += neigh[n]
        connected_subgraphs.append(connected_subgraph)

    return connected_subgraphs


def get_face(piece, matrix):
    interface = 0
    surface = 0
    for x, y in piece:
        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            if x - dx < 0 or x - dx >= len(matrix[0]):
                pass
            elif y - dy < 0 or y - dy >= len(matrix):
                pass
            elif matrix[y - dy][x - dx] == 0:
                surface += 1
            else:
                interface += 1
    return interface, surface


def half_puzzle(x_length, y_length, piece_size, same_piece_limit):
    best_score = x_length * y_length
    best_matrix = generate(x_length, y_length)
    n_depict = 0
    n_pieces = int(x_length * y_length / piece_size)
    waiting = []
    piece_id = 1
    matrix = generate(x_length, y_length)
    for new_piece in get_new_pieces(matrix, x_length, y_length, piece_size):
        pieces2count = {}
        key = shape_key(new_piece)
        pieces2count[key] = 1
        new_matrix = copy.deepcopy(matrix)
        for x, y in new_piece:
            new_matrix[y][x] = piece_id
        pieces = [new_piece]
        waiting.append([0, piece_id + 1, pieces, new_matrix, pieces2count])

    trial = 0
    random.shuffle(waiting)
    while len(waiting) > 0:
        trial += 1
        if trial > 530000:
            break

        delta, piece_id, pieces, matrix, pieces2count = waiting.pop()
        score = sum([sum([1 if x == 0 else 0 for x in mat]) for mat in matrix])
        if len(get_connected_subgraphs(matrix)) > 1:
            continue

        if best_score >= score:
            best_score = score
            best_matrix = matrix

        if score == (x_length * y_length) / 2:
            yield (best_matrix)
            continue

        new_pieces = get_new_pieces(matrix, x_length, y_length, piece_size)
        for new_piece in new_pieces:
            new_pieces2count = copy.deepcopy(pieces2count)
            key = shape_key(new_piece)
            if key not in new_pieces2count.keys():
                new_pieces2count[key] = 0
            new_pieces2count[key] += 1
            if new_pieces2count[key] > same_piece_limit:
                continue

            new_pieces = copy.deepcopy(pieces)
            new_pieces.append(new_piece)
            new_matrix = copy.deepcopy(matrix)
            for x, y in new_piece:
                new_matrix[y][x] = piece_id

            face = get_face(new_piece, matrix)

            if len(get_connected_subgraphs(matrix)) > 1:
                continue
            waiting.append(
                [face[0], piece_id + 1, new_pieces, new_matrix, new_pieces2count]
            )

        if random.random() < 0.05:
            random.shuffle(waiting)
        elif random.random() < 0.95:
            waiting = sorted(waiting)
    return matrix


def same_piece_within_limit(matrix, same_piece_limit):
    id2piece = {}
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] not in id2piece.keys():
                id2piece[matrix[y][x]] = []
            id2piece[matrix[y][x]].append([x, y])

    key2count = {}
    for id, piece in id2piece.items():
        key = shape_key(piece)
        if key not in key2count.keys():
            key2count[key] = 0
        key2count[key] += 1
        if key2count[key] > same_piece_limit:
            return False

    return True


def find_some(x_length=8, y_length=5, piece_size=4, same_piece_limit=2, max_trial=5):

    index = 0
    matrix_history = []
    keta = int(x_length * y_length / piece_size)
    for matrix in half_puzzle(x_length, y_length, piece_size, same_piece_limit):
        for prev_matrix in matrix_history:
            matrix3 = np.flipud(np.fliplr(np.array(matrix)))

            if (prev_matrix + matrix3).min().min() > 0:
                matrix3 += keta
                matrix3 = np.where(matrix3 == keta, 0, matrix3)
                combined_matrix = prev_matrix + matrix3
                if same_piece_within_limit(combined_matrix, same_piece_limit):
                    yield combined_matrix
                    index += 1

        matrix_history.append(matrix)
        if index > max_trial:
            break

    return True
