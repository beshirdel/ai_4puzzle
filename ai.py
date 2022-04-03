import dbmanager


class AI:
    def __init__(self, size):
        self.inf = 99999999999
        groups, db = dbmanager.load(size)
        self.groups = groups
        self.db = db

    def ida_star(self, puzzle):
        if puzzle.goal_test():
            return []
        bound = self.h_db(puzzle)
        path = [puzzle]
        directions = []
        while True:
            result = self.ids(path, 0, bound, directions)

            if result == True:
                return directions

            if result == self.inf:
                return None


            bound = result

    def ids(self, path, g, bound, directions):
        p = path[-1]
        f = g + self.h_db(p)

        if f > bound:
            return f

        if p.goal_test():
            return True

        min = self.inf

        for direction in p.DIRECTIONS:
            if directions and (-direction[0], -direction[1]) == directions[-1]:
                continue
            ok, new_puzzle = p.move_new(direction)

            if not ok or new_puzzle in path:
                continue

            path.append(new_puzzle)
            directions.append(direction)

            result = self.ids(path, g + 1, bound, directions)
            if result == True:
                return True
            if result < min:
                min = result

            path.pop()
            directions.pop()

        return min

    def h_db(self, puzzle):
        h = 0
        for i in range(len(self.groups)):
            grp_hash = puzzle.serialize(self.groups[i])
            if grp_hash in self.db[i]:
                h += self.db[i][grp_hash]
            else:
                h += self.h_md(puzzle, self.groups[i])
        return h

    def h_md(self, puzzle, group):
        h = 0
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                if puzzle[i][j] != 0 and puzzle[i][j] in group:
                    real_pos = ((puzzle[i][j] - 1) // puzzle.size,
                                (puzzle[i][j] - 1) % puzzle.size)
                    h += abs(real_pos[0] - i)
                    h += abs(real_pos[1] - j)
        return h
