from typing import List
from dataset import Dataset
from solution import Solution
from car import Car

import random as rd

class Genetic(object):

    def __init__(self, dataset: Dataset, max_population_size: int = 1000, polling_size: int = 200, mutation_rate: float = 0.01, constant_generations_num: int = 5):
        """
        """
        self.dataset = dataset

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
                children = self.reproduce(parent_a, parent_b)
                # slight chance of mutation
                if rd.random() < self.mutation_rate:
                    children[0].mutate()
                if rd.random() < self.mutation_rate:
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
            cars: List[Car] = [Car(self.dataset.bonus) for _ in range(self.dataset.ncars)]
            random_solution: Solution = Solution(cars, self.dataset.rides.copy())
            random_solution.randomize_allocation()
            self.population.append(random_solution)

    def constant_generations(self):
        return len(set(self.best_fit_queue)) == 1

    def queue_best_fit(self):
        if len(self.best_fit_queue) == self.constant_generations_num:
            self.best_fit_queue.pop(0)
        self.best_fit_queue.append(self.best_fit)

    def reproduce(self, parent_a: Solution, parent_b: Solution) -> List[Solution]:
        parent_a_matrix = self.solution_to_matrix(parent_a)
        parent_b_matrix = self.solution_to_matrix(parent_b)
        child_a_matrix: List[List[bool]] = []
        child_b_matrix: List[List[bool]] = []

        crossover_index: int = rd.randint(1, self.dataset.nrides - 1)
        for parent_a_car, parent_b_car in zip(parent_a_matrix, parent_b_matrix):
            child_a_matrix.append(parent_a_car[0:crossover_index] + parent_b_car[crossover_index:self.dataset.nrides])
            child_b_matrix.append(parent_b_car[0:crossover_index] + parent_a_car[crossover_index:self.dataset.nrides])

        child_a = self.matrix_to_solution(child_a_matrix)
        child_a.calculate_fitness()
        child_b = self.matrix_to_solution(child_b_matrix)
        child_b.calculate_fitness()

        return [child_a, child_b]

    def solution_to_matrix(self, solution: Solution) -> List[List[bool]]:
        matrix: List[List[bool]] = []
        for car in solution.cars:
            binary_list: List[bool] = [False] * self.dataset.nrides
            for ride in car.allocated_rides:
                binary_list[ride.id] = True
            matrix.append(binary_list)
        return matrix

    def matrix_to_solution(self, matrix: List[List[bool]]) -> Solution:
        cars: List[Car] = [Car(self.dataset.bonus) for _ in range(self.dataset.ncars)]
        solution: Solution = Solution(cars, self.dataset.rides.copy())
        solution.matrix_allocation(matrix)
        return solution

    def write(self):
        print('Generation {} best fit: {}'.format(self.generation, self.best_fit.fitness))

from car import Car
from ride import Ride
# testing :) :-]
if __name__ == "__main__":
    dataset = Dataset('a_example')
    gen = Genetic(dataset)
    gen.execute()
    """
    rides = [Ride(0, [0, 1, 2, 3, 3, 5]), Ride(1, [2, 1, 5, 6, 2, 6]), Ride(2, [5, 2, 6, 3, 1, 7])]
    cars = [Car(2), Car(2), Car(2)]
    dataset.rides = rides
    dataset.ncars = 3
    
    solution_1 = Solution([car.copy() for car in cars], rides.copy())
    # solution_2 = Solution([car.copy() for car in cars], rides.copy())
    
    solution_1.randomize_allocation()
    solution_1.calculate_fitness()
    solution_1.write()
    solution_1.mutate()
    solution_1.write()

    solution_2.randomize_allocation()
    solution_2.calculate_fitness()

    solution_2.write()

    children = gen.reproduce(solution_1, solution_2)
    children[0].write()
    children[1].write()
    """
