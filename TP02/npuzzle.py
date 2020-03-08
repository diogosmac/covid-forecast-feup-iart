import random
import sys
import time


def get_row(pos):
    return pos[0]


def get_col(pos):
    return pos[1]


class State(object):

    def __init__(self, N, Numbers=None):

        def generate_puzzle_nums(size):
            def split_list(values):
                for i in range(0, size * size, size):
                    yield values[i:i + size]

            starting_sequence = [i for i in range(size * size)]
            random.shuffle(starting_sequence)
            return split_list(starting_sequence)

        self.N = N
        self.Numbers = list(generate_puzzle_nums(N)) \
            if Numbers is None \
            else [[c for c in row] for row in Numbers]

    def copy(self):
        return State(self.N, list(self.Numbers))

    def write(self):
        num_width = len(str(self.N ** 2))
        for row in self.Numbers:
            row_out = '[ '
            for i in row:
                row_out += str(i).rjust(num_width) + ' '
            row_out += ']'
            print(row_out)
        print('')

    def hash(self):
        st = ''
        for i in self.Numbers:
            for j in i:
                st += str(j) + ','
        return st[:-1]

    def check(self):
        i = 1
        for row in self.Numbers:
            for num in row:
                if i == self.N ** 2 and num == 0:
                    return True
                elif i != num:
                    break
                i += 1
        return False

    def find(self, val):
        if val >= self.N ** 2:
            return [-1, -1]

        row = 0
        while row < len(self.Numbers):
            r = self.Numbers[row]
            col = 0
            while col < len(r):
                num = r[col]
                if num == val:
                    return [row, col]
                col += 1
            row += 1
        return [-1, -1]

    def findEmpty(self):
        return self.find(0)

    def swap(self, pos1, pos2):
        [self.Numbers[get_row(pos1)][get_col(pos1)], self.Numbers[get_row(pos2)][get_col(pos2)]] = \
            [self.Numbers[get_row(pos2)][get_col(pos2)], self.Numbers[get_row(pos1)][get_col(pos1)]]

    def getOutOfPlaceCount(self):
        count = 0
        i = 1
        for row in self.Numbers:
            for num in row:
                if i == self.N ** 2:
                    if num != 0:
                        count += 1
                elif i != num:
                    count += 1
                i += 1
        return count

    def getManhattanSum(self):

        def manhattanDist(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        def getCorrectPos(val):
            if val == 0:
                return [self.N - 1, self.N - 1]
            return [(val - 1) // self.N, (val - 1) % self.N]

        total = 0
        row = 0
        while row < len(self.Numbers):
            col = 0
            while col < len(self.Numbers):
                num = self.Numbers[row][col]
                corr = getCorrectPos(num)
                total += manhattanDist([row, col], corr)
                col += 1
            row += 1

        return total


def move_left(state):
    empty = state.findEmpty()
    if get_col(empty) < state.N - 1:
        state.swap(empty, [get_row(empty), get_col(empty) + 1])
        return True
    return False


def move_right(state):
    empty = state.findEmpty()
    if get_col(empty) > 0:
        state.swap(empty, [get_row(empty), get_col(empty) - 1])
        return True
    return False


def move_up(state):
    empty = state.findEmpty()
    if get_row(empty) < state.N - 1:
        state.swap(empty, [get_row(empty) + 1, get_col(empty)])
        return True
    return False


def move_down(state):
    empty = state.findEmpty()
    if get_row(empty) > 0:
        state.swap(empty, [get_row(empty) - 1, get_col(empty)])
        return True
    return False


def solve_bfs(init, operators, timeout):
    print('Using Breadth First Search:')
    start = time.time()

    queue = []
    for op in operators:
        if op(init.copy()):
            queue.append((init.copy(), op, []))

    while time.time() - start < timeout:
        state, op, path = queue.pop(0)

        if state.check():
            elapsed = time.time() - start
            print('Solved in:\t' + str(elapsed) + ' seconds\n')
            return True

        op(state)
        sequence = list(path)
        sequence.append(op)

        for op in operators:
            if op(state.copy()):
                queue.append((state.copy(), op, sequence))

    print('Timeout!!\t(' + str(timeout) + ' seconds)\n')
    return False


def solve_aStar(init, operators, timeout):
    class Item(object):
        def __init__(self, st, operator, p):
            self.state = st
            self.op = operator
            self.path = p

        def eval(self):
            st = self.state.copy()
            op(st)
            return st.getOutOfPlaceCount() * 1000 + st.getManhattanSum()

        def extract(self):
            return [self.state, self.op, self.path]

    def state_op_combo(st, oper):
        return st.hash(), oper.__name__

    print('Using A*:')
    start = time.time()

    priority_queue = []
    visited = set()
    for op in operators:
        if op(init.copy()):
            curr = Item(init.copy(), op, [])
            i = 0
            while i < len(priority_queue):
                item = priority_queue[i]
                if curr.eval() < item.eval():
                    break
                i += 1
            priority_queue.insert(i, curr)
            visited.add(state_op_combo(init.copy(), op))

    while not priority_queue == [] and time.time() - start < timeout:
        item = priority_queue.pop(0)
        [state, op, path] = item.extract()

        if state.check():
            elapsed = time.time() - start
            print('Solved in:\t' + str(elapsed) + ' seconds\n')
            return True

        op(state)
        sequence = list(path)
        sequence.append(op)

        for op in operators:
            curr = state_op_combo(state, op)
            if curr not in visited:
                visited.add(state_op_combo(init.copy(), op))
                if op(state.copy()):
                    curr = Item(state.copy(), op, sequence)
                    i = 0
                    while i < len(priority_queue):
                        item = priority_queue[i]
                        if curr.eval() < item.eval():
                            break
                        i += 1
                    priority_queue.insert(i, curr)

    print('Timeout!!\t(' + str(timeout) + ' seconds)\n')
    return False


def main():
    if len(sys.argv) != 2:
        print('\nUsage: python ' + sys.argv[0] + ' <timeout - seconds>\n')
        return 0

    timeout = int(sys.argv[1])
    operators = [move_left, move_right, move_up, move_down]

    print('\nPuzzle 1:')
    puzzle1 = State(3, [[1, 2, 3], [5, 0, 6], [4, 7, 8]])
    puzzle1.write()
    solve_bfs(puzzle1, operators, timeout)
    solve_aStar(puzzle1, operators, timeout)

    print('\nPuzzle 2:')
    puzzle2 = State(3, [[1, 3, 6], [5, 2, 0], [4, 7, 8]])
    puzzle2.write()
    solve_bfs(puzzle2, operators, timeout)
    solve_aStar(puzzle2, operators, timeout)

    print('\nPuzzle 3:')
    puzzle3 = State(3, [[1, 6, 2], [5, 7, 3], [0, 4, 8]])
    puzzle3.write()
    solve_bfs(puzzle3, operators, timeout)
    solve_aStar(puzzle3, operators, timeout)

    print('\nPuzzle 4:')
    puzzle4 = State(4, [[5, 1, 3, 4], [2, 0, 7, 8], [10, 6, 11, 12], [9, 13, 14, 15]])
    puzzle4.write()
    solve_bfs(puzzle4, operators, timeout)
    solve_aStar(puzzle4, operators, timeout)

    return 0


if __name__ == '__main__':
    main()
