from dataset import Dataset
from solution import Solution
from typing import List


class HillClimbing(object):

    def __init__(self, dataset: Dataset, max_iter: int = 10000):
        self.dataset = dataset
        self.solution = dataset.greedy_solve()
        self.iteration_limit = max_iter

    def write(self):
        self.solution.write()

    def solve(self):

        iteration = 0
        while iteration < self.iteration_limit:

            next_solution = self.choose_next()

            if next_solution is None:
                break

            self.solution = next_solution
            iteration += 1

    def choose_next(self):
        return None
        # gera um sucessor de cada vez, o primeiro que tiver um score melhor é escolhido
