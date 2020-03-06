import random

class State(object):

    def __init__(self, N, Numbers=None):
        def generate_puzzle_nums(N):
            def split_list(values):
                for i in range(0, N*N, N):
                    yield values[i:i + N]
            starting_sequence = [i for i in range(N*N)]
            random.shuffle(starting_sequence)
            return split_list(starting_sequence)

        self.N = N
        if Numbers is None:
            self.Numbers = list(generate_puzzle_nums(N))
        else:
            self.Numbers = Numbers
    
    def copy(self):
        return State(self.N, self.Numbers)
    
    def equal(self, state):
        if self.N != state.N:
            return False
        for i in range(len(self.Numbers)):
            if self.Numbers[i] != state.Numbers[i]:
                return False
        return True

    def write(self):
        for row in self.Numbers:
            row_out = '[\t'
            for i in row:
                row_out += str(i) + '\t'
            row_out += ']'
            print(row_out)



def main():
    return 0


if __name__ == '__main__':
    main()
