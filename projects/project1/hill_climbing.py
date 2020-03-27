from dataset import Dataset
from solution import Solution
from typing import List
import random as rd


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
            next_solution = self.climb_hill()
            if next_solution is None:
                break
            self.solution = next_solution
            iteration += 1

    def climb_hill(self):

        score = self.solution.calculate_fitness(self.dataset.bonus)

        neighbors: List[Solution] = self.solution.get_neighbors()       # TODO: get all neighbors from solution

        while neighbors:
            neighbor: Solution = rd.choice(neighbors)

            new_score = neighbor.calculate_fitness(self.dataset.bonus)
            if new_score > score:
                return neighbor

            neighbors.remove(neighbor)

        return None
