import sys


class State(object):
    def __init__(self, B1=0, B2=0):
        [self.B1, self.B2] = [B1, B2]

    def write(self):
        return '( ' + str(self.B1) + ' ) | ( ' + str(self.B2) + ' )'

    def copy(self):
        return State(self.B1, self.B2)

    def equal(self, state):
        return self.B1 == state.B1 and self.B2 == state.B2


def empty_B1(state):
    if state.B1 > 0:
        state.B1 = 0
        return True
    return False


def empty_B2(state):
    if state.B2 > 0:
        state.B2 = 0
        return True
    return False


def fill_B1(state):
    if state.B1 < C1:
        state.B1 = C1
        return True
    return False


def fill_B2(state):
    if state.B2 < C2:
        state.B2 = C2
        return True
    return False


def transfer_B1_fill_B2(state):
    if state.B1 + state.B2 >= C2 > state.B2:
        state.B1 = state.B1 - (C2 - state.B2)
        state.B2 = C2
        return True
    return False


def transfer_B1_empty_B1(state):
    if state.B1 + state.B2 <= C2 and state.B1 > 0:
        state.B2 = state.B1 + state.B2
        state.B1 = 0
        return True
    return False


def transfer_B2_fill_B1(state):
    if state.B1 + state.B2 >= C1 > state.B1:
        state.B2 = state.B2 - (C2 - state.B1)
        state.B1 = C1
        return True
    return False


def transfer_B2_empty_B2(state):
    if state.B1 + state.B2 <= C1 and state.B2 > 0:
        state.B1 = state.B1 + state.B2
        state.B2 = 0
        return True
    return False


def solve_bfs(operators):
    queue = []
    for op in operators:
        if op(State()):
            queue.append((State(), op, []))

    while True:
        state, op, path = queue.pop(0)

        if check_state(state):
            write_output(path, state, 'BFS')
            return True

        op(state)
        sequence = list(path)
        sequence.append(op)

        for op in operators:
            if op(state.copy()):
                queue.append((state.copy(), op, sequence))


def solve_dfs(operators):
    def state_op_combo(st, oper):
        return st.write(), oper.__name__

    stack = []
    visited = set()
    for op in operators:
        if op(State()):
            stack.append((State(), op, []))
            visited.add(state_op_combo(State(), op))

    while True:
        state, op, path = stack.pop()

        if check_state(state):
            write_output(path, state, 'DFS')
            return True

        op(state)
        sequence = list(path)
        sequence.append(op)

        for op in operators:
            curr = state_op_combo(state, op)
            if curr not in visited:
                visited.add(curr)
                if op(state.copy()):
                    stack.append((state.copy(), op, sequence))


def solve_progressive_dfs(operators):
    def state_op_combo(state, op):
        return state.write(), op.__name__

    def limited_dfs(max_depth):
        stack = []
        visited = set()
        for op in operators:
            if op(State()):
                stack.append((State(), op, [], 0))
                visited.add(state_op_combo(State(), op))

        while not stack == []:
            state, op, path, level = stack.pop()

            if check_state(state):
                write_output(path, state, 'Progressive DFS')
                return True

            if level < max_depth:
                op(state)
                sequence = list(path)
                sequence.append(op)

                for op in operators:
                    curr = state_op_combo(state, op)
                    if curr not in visited:
                        visited.add(curr)
                        if op(state.copy()):
                            stack.append((state.copy(), op, sequence, level + 1))

        return False

    depth = 1
    while not limited_dfs(depth):
        depth += 1

    return False


def check_state(state):
    return state.B1 == N


def write_output(path, final, alg):
    history = State()
    for op in path:
        print(history.write(), '>>', op.__name__)
        op(history)
    print(final.write(), '-- [ Solved with ' + alg + ' in ' + str(len(path)) + ' moves! ]')


C1 = 4
C2 = 3
N = 2


def main():
    if len(sys.argv) != 2:
        print('Usage: python ' + sys.argv[0] + ' <algorithm>')
        return
    alg = sys.argv[1].lower()

    operators = [empty_B1, empty_B2, fill_B1, fill_B2, transfer_B1_fill_B2, transfer_B1_empty_B1, transfer_B2_fill_B1,
                 transfer_B2_empty_B2]

    if alg == 'bfs':
        print('\nUsing Breadth First Search:')
        solve_bfs(operators)
    elif alg == 'dfs':
        print('\nUsing Depth First Search:')
        solve_dfs(operators)
    elif alg == 'progressive':
        print('\nUsing Progressive Depth Search:')
        solve_progressive_dfs(operators)
    else:
        print('\nAlgorithm \'' + sys.argv[1] + '\' is not implemented!')

    print()


if __name__ == '__main__':
    main()
