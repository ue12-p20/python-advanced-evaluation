# it is required to install separately the pytest-timeout plugin
# pip install pytest-timeout

import pytest

"""
WARNING: code for testing - deliberately tedious
NOT suitable for writing a solver
"""

import json
import subprocess

N = 3 # number of rows
M = 3 # number of columns

TARGET = [1, 2, 3, 4, 5, 6, 7, 8, 0]

MAX_MOVES = 36

def is_empty_line(line):
    return line.strip() == ''
def is_sep_line(line):
    return set(line.strip()) == set('-')

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


def check_summary(line, reachable, nb_moves, max_moves):
    d = json.loads(line)
    if not reachable:
        # summary should say target is unreachable
        assert d['reachable'] is False
    else:
        # check number of moves declared in summary
        assert d['nb_moves'] == nb_moves
        # maximum number of moves
        assert nb_moves <= max_moves
    return True


def check_chain(input_filename, chain_filename, reachable, max_moves):

    target = build_board_from_tokens(TARGET)
    start = read_board(input_filename)

    #print(f"checking chain from {start} to {target} - reachable={reachable}")

    with open(chain_filename) as feed:
        try:
            chain2 = build_board_from_lines(islice(feed, N))
            # first board in chain should match initial board
            assert chain2 == start
            first_extra_line = next(feed)
            if not reachable:
                # expecting sep line after unreachable board
                assert is_sep_line(first_extra_line)
                assert check_summary(next(feed), False, None, max_moves)
                # unreachable ends here
                return True
            else:
                # expecting an empty line after initial board
                assert is_empty_line(first_extra_line)

            reading = True
            nb_moves = 0

            while reading:
                chain1, chain2 = chain2, build_board_from_lines(islice(feed, N))
                nb_moves += 1
                # check move chain consistency
                assert are_neighbours(chain1, chain2)
                if chain2 != target:
                    sep_line = next(feed)
                    # expect an empty line between moves in the chain
                    assert is_empty_line(sep_line)
                else:
                    # chain is complete
                    reading = False
                    sep_line = next(feed)
                    # at the end of the chain a separator line is expected
                    assert is_sep_line(sep_line)
            return check_summary(next(feed), True, nb_moves, max_moves)
        except StopIteration:
            raise ValueError(f"output file {chain_filename} too short")
    return True


def run_and_check_filename(filename, *, reachable, max_moves):
    input_filename = f"samples/{filename}.txt"
    chain_filename = f"samples/{filename}.chain"
    # invoking your program
    subprocess.run(
        [
            "python",
            "puzzle8/cli.py",
            input_filename,
            chain_filename
        ]
    )
    # checking the output is correct
    assert check_chain(input_filename, chain_filename, reachable, max_moves)


# range of inputs, e.g. r30-00 .. r30-09
# call run_and_check_range("r30", 0, 10)
def run_and_check_range(prefix, beg, end, reachable=True, max_moves=MAX_MOVES):
    for index in range(beg, end):
        stem = f"{prefix}-{index:02}"
        run_and_check_filename(stem, reachable=reachable, max_moves=max_moves)


####################

# unreachables

@pytest.mark.timeout(timeout=10, method='thread')
def test_unreachable_0():
    run_and_check_range("u30", 0, 20, reachable=False)

@pytest.mark.timeout(timeout=10, method='thread')
def test_unreachable_1():
    run_and_check_range("u30", 20, 40, reachable=False)

# reachables

# 1 - 6 moves
@pytest.mark.timeout(timeout=6, method='thread')
def regular_06():
    run_and_check_range("r06", 0, 10, reachable=True, max_moves=9)

# .. 09 moves
@pytest.mark.timeout(timeout=9, method='thread')
def test_regular_09():
    run_and_check_range("r09", 0, 10, reachable=True, max_moves=12)

# .. 12 moves
@pytest.mark.timeout(timeout=12, method='thread')
def regular_12():
    run_and_check_range("r12", 0, 10, reachable=True, max_moves=16)

# .. 15 moves
@pytest.mark.timeout(timeout=15, method='thread')
def test_regular_15():
    run_and_check_range("r15", 0, 10, reachable=True, max_moves=19)

# .. 18 moves
@pytest.mark.timeout(timeout=18, method='thread')
def regular_18():
    run_and_check_range("r18", 0, 10, reachable=True, max_moves=22)

# .. 21 moves
@pytest.mark.timeout(timeout=21, method='thread')
def test_regular_21():
    run_and_check_range("r21", 0, 10, reachable=True, max_moves=26)

# .. 24 moves
@pytest.mark.timeout(timeout=24, method='thread')
def regular_24():
    run_and_check_range("r24", 0, 10, reachable=True, max_moves=29)

# .. 27 moves
@pytest.mark.timeout(timeout=27, method='thread')
def test_regular_27():
    run_and_check_range("r27", 0, 10, reachable=True, max_moves=32)


# faster and faster

# r30-00 .. r30-09
@pytest.mark.timeout(timeout=30, method='thread')
def test_speed_30():
    run_and_check_range("r30", 0, 10)

@pytest.mark.timeout(timeout=25, method='thread')
def test_speed_25():
    run_and_check_range("r30", 0, 10)

@pytest.mark.timeout(timeout=20, method='thread')
def test_speed_20():
    run_and_check_range("r30", 0, 10)

@pytest.mark.timeout(timeout=15, method='thread')
def test_speed_15():
    run_and_check_range("r30", 0, 10)
