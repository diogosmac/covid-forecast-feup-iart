N = 3

class State(object):
    def __init__(self, Missionaries=[N,0], Cannibals=[N,0]):
        self.Missionaries = list(Missionaries)
        self.Cannibals = list(Cannibals)
    
    def write(self):
        return '( ' + str(self.Missionaries[0]) + 'M ' + str(self.Cannibals[0]) + 'C ) ' + \
            '~ ~ ( ' + str(self.Missionaries[1]) + 'M ' + str(self.Cannibals[1]) + 'C )'
    
    def check(self):
        return self.Missionaries == [0,N] and self.Cannibals == [0,N]

    def copy(self):
        return State(self.Missionaries, self.Cannibals)
    
    def equal(self, state):
        return self.Missionaries == state.Missionaries \
            and self.Cannibals == state.Cannibals


def move1missAB(state):
    if state.Missionaries[0] >= 1:
        state.Missionaries[0] -= 1
        state.Missionaries[1] += 1
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move2missAB(state):
    if state.Missionaries[0] >= 2:
        state.Missionaries[0] -= 2
        state.Missionaries[1] += 2
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move1cannAB(state):
    if state.Cannibals[0] >= 1:
        state.Cannibals[0] -= 1
        state.Cannibals[1] += 1
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move2cannAB(state):
    if state.Cannibals[0] >= 2:
        state.Cannibals[0] -= 2
        state.Cannibals[1] += 2
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def moveBothAB(state):
    if state.Cannibals[0] >= 1 and state.Missionaries[0] >= 1:
        state.Cannibals[0] -= 1
        state.Cannibals[1] += 1
        state.Missionaries[0] -= 1
        state.Missionaries[1] += 1
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move1missBA(state):
    if state.Missionaries[1] >= 1:
        state.Missionaries[1] -= 1
        state.Missionaries[0] += 1
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move2missBA(state):
    if state.Missionaries[1] >= 2:
        state.Missionaries[1] -= 2
        state.Missionaries[0] += 2
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move1cannBA(state):
    if state.Cannibals[1] >= 1:
        state.Cannibals[1] -= 1
        state.Cannibals[0] += 1
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def move2cannBA(state):
    if state.Cannibals[1] >= 2:
        state.Cannibals[1] -= 2
        state.Cannibals[0] += 2
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def moveBothBA(state):
    if state.Cannibals[1] >= 1 and state.Missionaries[1] >= 1:
        state.Cannibals[1] -= 1
        state.Cannibals[0] += 1
        state.Missionaries[1] -= 1
        state.Missionaries[0] += 1
        return (state.Missionaries[0] >= state.Cannibals[0] or state.Missionaries[0] == 0) and \
            (state.Missionaries[1] >= state.Cannibals[1] or state.Missionaries[1] == 0)
    return False


def solve_bfs(operatorsAB, operatorsBA):

    queue = []
    for op in operatorsAB:
        if op(State()):
            queue.append((State(), op, [], False))
    
    while True:
        state, op, path, A_to_B = queue.pop(0)

        if state.check():
            write_output(path, state, 'BFS')
            return True

        op(state)
        sequence = list(path)
        sequence.append(op)

        operators = operatorsAB if A_to_B else operatorsBA

        for op in operators:
            if op(state.copy()):
                queue.append((state.copy(), op, sequence, not A_to_B))


def solve_dfs(operatorsAB, operatorsBA):

    def state_op_combo(state, op):
        return (state.write(), op.__name__)

    stack = []
    visited = set()
    for op in operatorsAB:
        if op(State()):
            stack.append((State(), op, [], False))
            visited.add(state_op_combo(State(), op))

    while True:
        state, op, path, A_to_B = stack.pop()

        if state.check():
            write_output(path, state, 'DFS')
            return True

        op(state)
        sequence = list(path)
        sequence.append(op)

        operators = operatorsAB if A_to_B else operatorsBA

        for op in operators:
            curr = state_op_combo(state, op)
            if curr not in visited:
                visited.add(curr)
                if op(state.copy()):
                    stack.append((state.copy(), op, sequence, not A_to_B))


def solve_progressive_dfs(operatorsAB, operatorsBA):

    def state_op_combo(state, op):
        return (state.write(), op.__name__)

    def limited_dfs(max_depth):
        stack = []
        visited = set()
        for op in operatorsAB:
            if op(State()):
                stack.append((State(), op, [], False, 0))
                visited.add(state_op_combo(State(), op))
        
        while not stack == []:
            state, op, path, A_to_B, depth = stack.pop()

            if state.check():
                write_output(path, state, 'Progressive DFS')
                return True
            
            if depth < max_depth:
                op(state)
                sequence = list(path)
                sequence.append(op)

                operators = operatorsAB if A_to_B else operatorsBA

                for op in operators:
                    curr = state_op_combo(state, op)
                    if curr not in visited:
                        visited.add(curr)
                        if op(state.copy()):
                            stack.append((state.copy(), op, sequence, not A_to_B, depth + 1))
        
        return False

    depth = 1
    while not limited_dfs(depth):
        depth += 1
    
    return False


def write_output(path, final, alg):
    history = State()
    for op in path:
        print(history.write(), '>>', op.__name__)
        op(history)
    print(final.write(), '-- [ Solved with ' + alg + ' in ' + str(len(path)) + ' moves! ]')


def main():
    
    operatorsAB = [moveBothAB, move1missAB, move2missAB, move1cannAB, move2cannAB]
    operatorsBA = [moveBothBA, move1missBA, move2missBA, move1cannBA, move2cannBA]

    print('\nUsing Breadth First Search:')
    solve_bfs(operatorsAB, operatorsBA)
    print('\nUsing Depth First Search:')
    solve_dfs(operatorsAB, operatorsBA)
    print('\nUsing Progressive Depth Search:')
    solve_progressive_dfs(operatorsAB, operatorsBA)
    print()
    return 0


if __name__ == '__main__':
    main()
