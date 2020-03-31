import math
import random as rd

from dataset import Dataset
from hill_climbing import HillClimbing
from ride import Ride
from typing import List
from tqdm import tqdm


class SimulatedAnnealing(HillClimbing):
    def __init__(self, dataset: Dataset, max_iter: int = 10000, random: bool = False,
                 start_temperature: float = 100, decrease_rate: float = 0.01, limit_temp: float = 1):
        super().__init__(dataset=dataset, max_iter=max_iter, random=random)
        self.start_temperature = start_temperature
        self.decrease_rate = decrease_rate
        self.limit_temp = limit_temp

    def solve(self):

        self.solution.calculate_fitness()
        print('Current Score:', self.solution.fitness)

        iteration = 0
        temperature = self.start_temperature
        progress = tqdm(total=self.iteration_limit, desc='Climbing the Hill')

        while iteration < self.iteration_limit:
            self.cool_down(temperature)
            iteration += 1
            progress.update(1)
            temperature -= temperature * self.decrease_rate
            if temperature < self.limit_temp:
                break

        progress.update(self.iteration_limit - iteration)
        progress.close()

        self.solution.calculate_fitness()
        print('Final Score:', self.solution.fitness)

    def cool_down(self, temperature: float):

        score = self.solution.fitness

        possible_ride_placements: List[int] = list(range(self.dataset.ncars + 1))

        first_order: List[int] = possible_ride_placements.copy()
        if self.random: rd.shuffle(first_order)

        for ride_orig in first_order:
            """
            If there are no rides on the selected list, skip.
            """
            if ride_orig == self.dataset.ncars:
                take_from = self.solution.unallocated_rides
            else:
                take_from = self.solution.cars[ride_orig].allocated_rides

            if not take_from: continue

            second_order: List[int] = possible_ride_placements.copy()
            second_order.remove(ride_orig)
            if self.random: rd.shuffle(second_order)

            for ride_dest in second_order:
                """
                If there are no rides on the selected list, skip.
                """
                if ride_dest == self.dataset.ncars:
                    place_into = self.solution.unallocated_rides
                else:
                    place_into = self.solution.cars[ride_dest].allocated_rides

                third_order = list(range(len(take_from)))
                if self.random: rd.shuffle(third_order)

                for ride_index in third_order:
                    """
                    Move solution to a 'neighboring state'
                    """
                    ride: Ride = take_from.pop(ride_index)
                    place_into.append(ride)

                    if ride_orig != len(self.solution.cars): self.solution.cars[ride_orig].calculate_score()
                    if ride_dest != len(self.solution.cars): self.solution.cars[ride_dest].calculate_score()

                    """
                    Calculate neighbor's fitness, advance if it improves upon the current solution.
                    """
                    self.solution.calculate_fitness()
                    if self.solution.fitness > score:
                        return

                    probability = math.e ** ((self.solution.fitness - score) / temperature)
                    if rd.random() < probability:
                        return

                    """
                    If not, reverse the changes, continue searching.
                    """
                    place_into.remove(ride)
                    take_from.append(ride)

                    if ride_orig != len(self.solution.cars): self.solution.cars[ride_orig].calculate_score()
                    if ride_dest != len(self.solution.cars): self.solution.cars[ride_dest].calculate_score()
