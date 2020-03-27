from typing import List
from dataset import Dataset
from solution import Solution

import random as rd

class Genetic(object):

    def __init__(self, dataset: Dataset, max_population_size: int = 10000, polling_size: int = 2500, mutation_rate: float = 0.01, constant_generations_num: int = 5):
        """
        """
        self.dataset = Dataset

        self.generation: int = 1
        self.population: List[Solution] = []
        self.max_population_size: int = max_population_size
        self.polling_size: int = polling_size
        self.mutation_rate: float = mutation_rate
        self.constant_generations_num: int = constant_generations_num
        self.best_fit: Solution
        self.best_fit_queue: List[int] = [i for i in range(5)]

    def execute(self):
        # create first population
        self.create_random_population()
        # calculate new population's fitness
        for solution in self.population:
            solution.calculate_fitness()
        # sort from best to worst
        self.sort_population()
        self.best_fit = self.population[0]
        self.write()

        while not self.constant_generations():
            # create new population
            new_population: List[Solution] = []
            while len(new_population) < self.max_population_size:
                # choose the best n (polling size) of population
                parent_a = self.population[rd.randint(0, self.polling_size - 1)]
                parent_b = self.population[rd.randint(0, self.polling_size - 1)]
                children = parent_a.reproduce(parent_b)
                children[0].mutate()
                children[1].mutate()
                new_population.append(children[0])
                new_population.append(children[1])

            self.population = new_population
            self.generation += 1
            # calculate new population's fitness
            for solution in self.population:
                solution.calculate_fitness()
            # sort from best to worst
            self.sort_population()
            # new best might not be better than the old best
            if self.population[0].fitness > self.best_fit.fitness:
                self.best_fit = self.population[0]
            # enqueue best solution in current population
            self.queue_best_fit()
            self.write()

    def sort_population(self):
        self.population.sort(key=lambda solution: solution.fitness, reverse=True)

    def create_random_population(self):
        while len(self.population) < self.max_population_size:
            random_solution: Solution = Solution(self.dataset.nrides, self.dataset.rides.copy())
            self.population.append(random_solution)

    def constant_generations(self):
        return len(set(self.best_fit_queue)) == 1

    def queue_best_fit(self):
        if len(self.best_fit_queue) == self.constant_generations_num:
            self.best_fit_queue.pop(0)
        self.best_fit_queue.append(self.best_fit)

    def write(self):
        print('Generation {} best fit: {}'.format(self.generation, self.best_fit.fitness))


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
