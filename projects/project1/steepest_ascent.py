import random as rd

from hill_climbing import HillClimbing
from dataset import Dataset
from typing import List
from ride import Ride


class SteepestAscent(HillClimbing):

    def __init__(self, dataset: Dataset, max_iter: int = 10000, random: bool = False):
        super().__init__(dataset=dataset, max_iter=max_iter, random=random)

    def climb_hill(self):

        sol = self.solution
        score = self.solution.fitness
        improved = False

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
                        sol = self.solution.copy()
                        sol.calculate_fitness()
                        score = sol.fitness
                        improved = True

                    """
                    If not, reverse the changes, continue searching.
                    """
                    place_into.remove(ride)
                    take_from.append(ride)

                    if ride_orig != len(self.solution.cars): self.solution.cars[ride_orig].calculate_score()
                    if ride_dest != len(self.solution.cars): self.solution.cars[ride_dest].calculate_score()

        if improved:
            self.solution = sol
            return True

        return False
