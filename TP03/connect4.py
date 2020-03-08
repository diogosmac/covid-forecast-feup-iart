import random

HEIGHT = 6
WIDTH = 7


class State(object):
    def __init__(self, board=None, lastMoveX=None, lastMoveY=None, player=1, nmoves=0):
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)] if board is None else board
        self.board = board
        [self.lastMoveX, self.lastMoveY] = [lastMoveX, lastMoveY]
        self.player = player
        self.nmoves = nmoves

    def copy(self):
        board_copy = [[col for col in row] for row in self.board]
        return State(board_copy, self.lastMoveX, self.lastMoveY, self.player, self.nmoves)

    def draw(self):
        ind = lin = ''
        for i in range(WIDTH):
            ind += str(i) + ' '
            lin += '--'
        print(lin)
        print(ind)
        print(lin)
        i = HEIGHT - 1
        while i >= 0:
            st = ''
            for j in range(WIDTH):
                st += str(self.board[i][j]) + ' '
            print(st)
            i += 1
        print(lin)

    def switch_player(self):
        self.player = 3 - self.player  # if 1 then 2, if 2 then 1 (stonks)

    def valid_move(self, move):
        return not (move < 1 or move > WIDTH or self.board[HEIGHT - 1][move] != 0)

    def execute_move(self, move):
        move = move - 1
        for i in range(HEIGHT):
            if self.board[i][move] == 0:
                self.board[i][move] = self.player
                self.lastMoveY = i
                self.lastMoveX = move
                self.switch_player()
                self.nmoves += 1


def line(number, st, player):
    def count(n, pl, p1, p2, p3, p4):
        pec = (p1 == pl) + (p2 == pl) + (p3 == pl) + (p4 == pl)
        if n == 4: return pec == 4
        vaz = (p1 == 0) + (p2 == 0) + (p3 == 0) + (p4 == 0)
        if n == 3: return pec == 3 and vaz == 1

    lin = 0
    i = 0
    while i < HEIGHT:

        j = 0
        while j < WIDTH:

            if j < WIDTH - 3 and \
                    count(number, player,
                          st.board[i][j], st.board[i][j + 1], st.board[i][j + 2], st.board[i][j + 3]):
                lin += 1
            if i < HEIGHT - 3 and \
                    count(number, player,
                          st.board[i][j], st.board[i + 1][j], st.board[i + 2][j], st.board[i + 3][j]):
                lin += 1
            if j < WIDTH - 3 and i < HEIGHT - 3 and \
                    count(number, player,
                          st.board[i][j], st.board[i + 1][j + 1], st.board[i + 2][j + 2], st.board[i + 3][j + 3]):
                lin += 1
            if j > 3 and i < HEIGHT - 3 and \
                    count(number, player,
                          st.board[i][j], st.board[i + 1][j - 1], st.board[i + 2][j - 2], st.board[i + 3][j - 3]):
                lin += 1

            j += 1

        i += 1

    return lin


def check_winner(state):
    if line(4, state, 1) > 0:
        return 1
    if line(4, state, 2) > 0:
        return 2
    if state.nmoves == 42:
        return 0
    return -1


def evaluate(state: State, player: int) -> int:
    def posit(st, pl):
        v = 0
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if st.board[i][j] == pl:
                    if j == 3:
                        v += 2
                    elif j == 2 or j == 4:
                        v += 1
        return v

    pos = posit(state, player) - posit(state, 3 - player)
    lin3 = line(3, state, player) - line(3, state, 3 - player)
    lin4 = line(4, state, player) - line(4, state, 3 - player)
    val = lin4 * 100 + lin3 * 5 + pos
    # print('Val: ' + str(val) + ' = Pos: ' + str(pos) + ' Lin3: ' + str(lin3) + ' Lin4: ' + str(lin4))
    return val


def get_human_move(state: State) -> int:
    while True:
        move = int(input("Please Select Move (1-7):"))
        if state.valid_move(move):
            break
    return move


def get_PC_random_move(state: State) -> int:
    while True:
        move = random.randint(1, 7)
        if state.valid_move(move):
            break
    return move


def get_PC_greedy_move(state: State) -> int:
    val = -1000
    move = 0
    for i in range(WIDTH):
        if state.valid_move(i):
            state2 = state.copy()
            state2.execute_move(i)
            curr_val = evaluate(state2, state.player)
            if curr_val > val:
                val = curr_val
                move = i
    return move


def get_PC_minimax_move(state: State, depth: int) -> int:
    move = 0
    # TODO: Minimax with alpha-beta cuts
    return move


def main():
    game = State()
    game.draw()

    while True:
        mov = get_PC_greedy_move(game) if game.player == 1 else get_human_move(game)
        game.execute_move(mov)
        game.draw()
        if check_winner(game) != -1:
            break

    print("End of Game! Winner: " + str(check_winner(game)))


if __name__ == '__main__':
    main()
