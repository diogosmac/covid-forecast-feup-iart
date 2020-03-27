from dataset import Dataset


class HillClimbing(object):

    def __init__(self, dataset: Dataset, max_iter: int = 10000):
        self.solution = dataset.greedy_solve()
        self.iteration_limit = max_iter

    def write(self):
        self.solution.write()
