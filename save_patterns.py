import numpy as np


def save_pattern(pattern, path='patterns/pattern1.txt'):
    with open(path, 'w') as file:
        for i in range(pattern.shape[0]):
            for j in range(pattern.shape[1]):
                file.write(str(int(pattern[i, j])))
            file.write('\n')


def load_pattern(path):
    lines = []
    with open(path, 'r') as file:
        for line in file.readlines():
            lines.append([int(c) for c in line.replace('\n', '')])
    return np.asarray(lines)
