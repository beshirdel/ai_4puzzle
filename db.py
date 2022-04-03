from collections import deque
import dbmanager
from time import perf_counter_ns
from puzzle import Puzzle
from multiprocessing import Pool


def visit(puzzle, tiles, tiles_with_blank, visited, db):
    serialized = puzzle.serialize(tiles_with_blank)
    if serialized in visited:
        return False

    visited.add(serialized)
    serialized = puzzle.serialize(tiles)
    if serialized not in db:
        db[serialized] = puzzle.level
    elif db[serialized] > puzzle.level:
        db[serialized] = puzzle.level

    return True


def bfs(puzzle, tiles):
    NANO_TO_SEC = 1000000000
    t1 = perf_counter_ns()

    visited = set()
    open_list = deque()
    open_list.append((puzzle, (0, 0)))
    tiles_with_blank = tiles.copy()
    tiles_with_blank.add(0)
    db = {}

    while open_list:
        p, d = open_list.popleft()

        if not visit(p, tiles, tiles_with_blank, visited, db):
            continue

        for direction in puzzle.DIRECTIONS:
            if d == direction:
                continue

            ok, new_puzzle = p.move_new(direction)
            if not ok:
                continue

            if new_puzzle[p.blankTile[0]][p.blankTile[1]] in tiles:
                new_puzzle.level += 1

            open_list.append((new_puzzle, (-direction[0], -direction[1])))

    return db


def build(size, tiles):
    puzzle = Puzzle(size)
    puzzle.level = 0

    return bfs(puzzle, tiles)


def main():
    size = 4
    groups = [{1, 2, 3, 4, 7}, {5, 6, 9, 10, 13}, {8, 11, 12, 14, 15}]
    result_db = []

    with Pool(processes=10) as pool:
        results = [pool.apply_async(build, (size, group)) for group in groups]
        results = [res.get() for res in results]

        for res in results:
            result_db.append(res)

    dbmanager.save(result_db, groups, size)


if __name__ == "__main__":
    main()
    g,d = dbmanager.load(4)
    print(len(d[0]))
    print(len(d[1]))
    print(len(d[2]))
    # print(len(g) , len(d))
