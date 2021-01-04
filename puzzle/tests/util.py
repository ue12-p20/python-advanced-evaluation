"""
WARNING: code for testing - deliberately tedious
NOT suitable for writing a solver
"""

N = 3 # number of rows
M = 3 # number of columns

TARGET = [1, 2, 3, 4, 5, 6, 7, 8, 0]

from itertools import islice

def check_size(b):
    if len(set(b)) != N*M:
        raise ValueError(f"wrong size with input {b}")

def normalize(token):
    def _normalize(token):
        if isinstance(token, int):
            return token
        token = str(token).replace('-', '0').replace('.', '0')
        return int(token) if token else 0
    norm = _normalize(token)
    if 0 <= norm < N*M:
        return norm
    else:
        raise ValueError(f"cannot normalize token {token}")

def build_board_from_tokens(chunk):
    return list(normalize(x) for x in chunk)

def build_board_from_lines(lines):
    return build_board_from_tokens(
        x for line in lines for x in line.replace('  ', ' 0 ').split())

def read_board(filename):
    with open(filename) as feed:
        return build_board_from_lines(islice(feed, N))


def are_neighbours(b1, b2):
    check_size(b1)
    check_size(b2)
    misses = [i for i in range(N*M) if b1[i]!=b2[i]]
    if len(misses) != 2:
        return False
    i1, i2 = misses
    if b1[i1] and b1[i2]:
        return False
    x1, y1 = i1 // M, i1 % M
    x2, y2 = i2 // M, i2 % M
    dx, dy = abs(x1-x2), abs(y1-y2)
    return (dx+dy == 1) and (dx * dy == 0)


def check_chain(input_filename, chain_filename):

    target = build_board_from_tokens(TARGET)
    start = read_board(input_filename)

    print(f"checking chain from {start} to {target}")

    with open(chain_filename) as feed:
        try:
            chain2 = build_board_from_lines(islice(feed, N))
            if chain2 != start:
                print(f"start configuration in {chain_filename} is not correct")
                return False
            assert next(feed).strip() == ""
        except StopIteration:
            print(f"output file {chain_filename} too short")
        reading = True
        while reading:
            try:
                chain1, chain2 = chain2, build_board_from_lines(islice(feed, N))
                next(feed)
                if not are_neighbours(chain1, chain2):
                    return False
            except StopIteration:
                reading = False
        if chain2 != target:
            print(f"end configuration in {chain_filename} is not correct")
            return False
    return True

import os
def run_and_check_filename(filename):
    input_filename = f"puzzle/tests/{filename}.txt"
    chain_filename = f"puzzle/tests/{filename}-chain.txt"
    command = f"python puzzle/solver.py {input_filename} {chain_filename}"
    os.system(command)
    return check_chain(input_filename, chain_filename)
