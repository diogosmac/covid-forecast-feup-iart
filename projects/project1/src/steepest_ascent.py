import random as rd

from src.hill_climbing import HillClimbing
from src.dataset import Dataset
from typing import List
from src.ride import Ride


class SteepestAscent(HillClimbing):
    """
    A specific implementation of the Hill Climbing algorithm to solve the Self
    Driving Rides problem, given the dataset and algorithm related attributes,
    which always advances to the most advantageous of all neighbors

    ...

    Attributes
    ----------
    dataset : Dataset
        a Dataset instance containing information about the problem
    max_iter : int
        the maximum number of iterations
    random : bool
        determines whether the neighbors will be visited in random order
    solution : Solution
        the starting point for the algorithm to solve from

    Methods
    -------
    climb_hill()
        advances to the best possible neighbor which improves on the current solution
    """

    def __init__(self, dataset: Dataset, max_iter: int = 10000, random: bool = False):
        """
        Parameters
        ----------
        dataset : Dataset
            a Dataset instance containing information about the problem
        max_iter : int
            the maximum number of iterations
        random : bool
            determines whether the neighbors will be visited in random order
        """
        super().__init__(dataset=dataset, max_iter=max_iter, random=random)

    def climb_hill(self):
        # Stores the current solution and score
        sol = self.solution
        score = self.solution.fitness
        # Indicates whether a better neighbor has been found
        improved = False
        # A ride can be present in each of the cars, or in the unallocated ride list
        possible_ride_placements: List[int] = list(range(self.dataset.ncars + 1))
        # A first decision will be made, which is where to take a ride from
        first_order: List[int] = possible_ride_placements.copy()
        if self.random: rd.shuffle(first_order)
        # Tries for each of the cars, because there may not be rides to be removed from some of them
        for ride_orig in first_order:
            # Specifies where to take the ride from
            if ride_orig == self.dataset.ncars:
                take_from = self.solution.unallocated_rides
            else:
                take_from = self.solution.cars[ride_orig].allocated_rides
            # If there are no rides on the selected list, skip
            if not take_from: continue
            # A second decision will be made, which is where to place the ride into
            second_order: List[int] = possible_ride_placements.copy()
            # A ride can not be placed in the same car it was taken from (duh)
            second_order.remove(ride_orig)
            if self.random: rd.shuffle(second_order)
            # Tries for each of the cars, because it will probably not be advantageous for all of them
            for ride_dest in second_order:
                # Specifies where to place the ride
                if ride_dest == self.dataset.ncars:
                    place_into = self.solution.unallocated_rides
                else:
                    place_into = self.solution.cars[ride_dest].allocated_rides
                # A third decision will be made, which is what ride should be moved
                third_order = list(range(len(take_from)))
                if self.random: rd.shuffle(third_order)
                # Tries for each of the rides, because not all may be good rides to move
                for ride_index in third_order:
                    # Moves solution to a 'neighboring' state
                    ride: Ride = take_from.pop(ride_index)
                    place_into.append(ride)
                    # Updates the score where needed
                    if ride_orig != len(self.solution.cars): self.solution.cars[ride_orig].calculate_score()
                    if ride_dest != len(self.solution.cars): self.solution.cars[ride_dest].calculate_score()
                    # Calculate neighbor's fitness, record the neighbor if it is the best one found
                    self.solution.calculate_fitness()
                    if self.solution.fitness > score:
                        # Stores a copy of the better neighbor, as well as its score
                        sol = self.solution.copy()
                        sol.calculate_fitness()
                        score = sol.fitness
                        # At least one better neighbor has been found! :)
                        improved = True
                    # Reverses the changes, to continue searching
                    place_into.remove(ride)
                    take_from.append(ride)
                    # Restores the score to where it was before the attempted changes
                    if ride_orig != len(self.solution.cars): self.solution.cars[ride_orig].calculate_score()
                    if ride_dest != len(self.solution.cars): self.solution.cars[ride_dest].calculate_score()

        # If a better neighbor was found, update solution and continue execution
        if improved:
            self.solution = sol
            return True
        # If no better neighbor was found, terminate execution
        return False
