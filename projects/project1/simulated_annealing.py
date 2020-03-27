from hill_climbing import HillClimbing
from dataset import Dataset
from solution import Solution
import math, random


class SimulatedAnnealing(HillClimbing):
    def __init__(self, dataset: Dataset, max_iter: int = 10000,
                 start_temperature: float = 100, decrease_rate: float = 0.01, limit_temp: float = 1):
        super().__init__(dataset, max_iter)
        self.start_temperature = start_temperature
        self.decrease_rate = decrease_rate
        self.limit_temp = limit_temp

    def solve(self):

        iteration = 0
        temperature = self.start_temperature
        while iteration < self.iteration_limit:
            next_solution = self.choose_next(temperature)
            if next_solution is not None:
                self.solution = next_solution
            iteration += 1
            temperature -= temperature * self.decrease_rate
            if temperature < self.limit_temp:
                break

        return self.solution

    def choose_next(self, temperature: float):

        score = self.solution.calculate_fitness(self.dataset.bonus)

        while True:

            neighbor: Solution = self.solution.copy()         # TODO: self.solution.get_random_neighbor()

            new_score = neighbor.calculate_fitness(self.dataset.bonus)
            if new_score > score:
                return neighbor

            probability = math.e ** ((new_score - score) / temperature)
            if random.random() < probability:
                return neighbor
