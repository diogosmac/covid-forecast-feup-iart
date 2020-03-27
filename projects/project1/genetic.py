from typing import List
from dataset import Dataset
from solution import Solution

import random as rd

class Genetic(object):

    def __init__(self, dataset: Dataset, population_size: int = 10000, polling_size: int = 2500, mutation_rate: int = 0.01, constant_generations_num: int = 5):
        """
        """
        self.dataset = Dataset

        self.population: List[Solution] = []
        self.population_size = population_size
        self.polling_size = polling_size
        self.mutation_rate = mutation_rate
        self.constant_generations_num = constant_generations_num
        self.best_fit_queue = [i for i in range(5)]

    def execute(self):
        return 0

    def create_random_population(self):
        while len(self.population) < self.population_size:
            self.population.append(Solution())

    def constant_generations(self):
        return len(set(self.best_fit_queue)) == 1

    def queue_best_fit(self, generation):
        if len(self.best_fit_queue) == self.constant_generations_num:
            self.best_fit_queue.pop(0)
        self.best_fit_queue.append(generation)

    def reproduce(self, parent_a, parent_b):
        return

    def mutate(self, chromosome):
        return


class Test(object):

    def __init__(self, ident):
        self.id = ident


# testing :) :-]
if __name__ == "__main__":
    arr = [Test(1), Test(2), Test(3), Test(2)]

    print([t.id for t in arr])

    for t in arr:
        if t.id == 2:
            arr.remove(t)

    print([t.id for t in arr])
