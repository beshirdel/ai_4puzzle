from random import choice
from copy import deepcopy


class Puzzle:
    #     x   y
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, size):
        self.size = size
        self.board = [[1 + i + x * size for i in range(size)] for x in range(size)]
        self.board[size - 1][size - 1] = 0
        self.blankTile = (size - 1, size - 1)

    def __getitem__(self, key):
        return self.board[key]

    def move_blank(self, direction):
        next_pos = [self.blankTile[0] + direction[0], self.blankTile[1] + direction[1]]
        if 0 <= next_pos[0] < self.size and 0 <= next_pos[1] < self.size:
            self[self.blankTile[0]][self.blankTile[1]] = self[next_pos[0]][next_pos[1]]
            self[next_pos[0]][next_pos[1]] = 0
            self.blankTile = next_pos
            return True
        return False

    def goal_test(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != i * self.size + j + 1 and self.board[i][j] != 0:
                    return False

        return True

    def shuffle(self):
        for i in range(1000):
            self.move_blank(choice(self.DIRECTIONS))

    def move_new(self, direction):
        cloned_puzzle = deepcopy(self)
        return cloned_puzzle.move_blank(direction), cloned_puzzle

    def serialize(self, tiles=None):
        if not tiles:
            tiles = [i for i in range(self.size ** 2)]

        indexes = ['x'] * 2 * (self.size ** 2)

        for i in range(self.size):
            for j in range(self.size):
                if self[i][j] in tiles:
                    indexes[self[i][j] * 2] = str(i)
                    indexes[self[i][j] * 2 + 1] = str(j)

        return "".join(indexes).replace("x", "")



