import math
import random as rd
import time as tm

from dataset import Dataset
from hill_climbing import HillClimbing
from ride import Ride
from typing import List
from tqdm import tqdm


class SimulatedAnnealing(HillClimbing):
    """
    A different approach to the Hill Climbing algorithm, which sometimes tolerates worse solutions
    in an attempt to avoid being trapped in local minima/maxima.

    ...

    Attributes
    ----------
    dataset : Dataset
        a Dataset instance containing information about the problem
    max_iter : int
        the maximum number of iterations
    random : bool
        determines whether the neighbors will be visited in random order
    start_temperature : float
        starting temperature for the Simulated Annealing algorithm
    decrease rate : float
        rate at which the temperature drops (percentage per each iteration)
    limit_temp : float
        minimum temperature at which the annealing will stop (effectively
        becoming a regular Hill Climbing algorithm)

    Methods
    -------
    solve()
        executes the algorithm to solve the problem
    cool_down()
        advances to a suitable neighbor, based on the current temperature
    """

    def __init__(self, dataset: Dataset, max_iter: int = 10000, random: bool = False,
                 start_temperature: float = 100, decrease_rate: float = 0.01, limit_temp: float = 1):
        """
        Parameters
        ----------
        dataset : Dataset
            a Dataset instance containing information about the problem
        max_iter : int
            the maximum number of iterations
        random : bool
            determines whether the neighbors will be visited in random order
        start_temperature : float
            starting temperature for the Simulated Annealing algorithm
        decrease rate : float
            rate at which the temperature drops (percentage per each iteration)
        limit_temp : float
            minimum temperature at which the annealing will stop (effectively
            becoming a regular Hill Climbing algorithm)
        """
        super().__init__(dataset=dataset, max_iter=max_iter, random=random)
        self.start_temperature = start_temperature
        self.decrease_rate = decrease_rate
        self.limit_temp = limit_temp

    def solve(self):
        # Starts by calculating the score before the algorithm execution
        self.solution.calculate_fitness()
        initial_score = self.solution.fitness
        print('Initial Score: {}'.format(self.solution.fitness))
        # Progress bar will give a visual indication of the work being done
        iteration = 0
        progress = tqdm(total=self.iteration_limit, desc='Climbing the Hill (with Simulated Annealing)')
        # Temperature takes its starting value
        temperature = self.start_temperature
        # Time will be recorded for statistical purposes
        start = time = tm.time()
        # Executes until it reaches the limit of iterations (or until it reaches an end condition)
        while iteration < self.iteration_limit:
            improved = self.cool_down(temperature)
            # Advances the iteration counter, updates the progress bar (for clarity)
            iteration += 1
            progress.update(1)
            # Decrease temperature until it reaches its limit value
            if temperature >= self.limit_temp:
                temperature -= temperature * self.decrease_rate
            else:
                # Ends if limit temperature has been reached and no better neighbors have been found
                if not improved:
                    break
            # Displays the current score after an iteration
            progress.set_postfix_str('Current Score = {}, Time Elapsed = {:.2f} seconds'.format(
                self.solution.fitness, tm.time() - start
            ))

        # Records the elapsed time, for statistical purposes
        elapsed = tm.time() - start
        progress.update(self.iteration_limit - iteration)
        progress.set_postfix_str('Final Score = {}, Time Elapsed = {:.2f} seconds'.format(
            self.solution.fitness, tm.time() - start
        ))
        progress.close()
        print('Final Score: {}, Gain in Score: {}, Time Elapsed = {:.2f} seconds'.format(
            self.solution.fitness, self.solution.fitness - initial_score, elapsed))


    def cool_down(self, temperature: float) -> bool:
        # Stores the initial score, for comparison purposes
        score = self.solution.fitness
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
                    # Calculate neighbor's fitness, advance if it improves upon the current solution.
                    self.solution.calculate_fitness()
                    if self.solution.fitness > score:
                        return True
                    # A worse neighbor an still be accepted, depending on the temperature
                    probability = math.e ** ((self.solution.fitness - score) / temperature)
                    if rd.random() < probability:
                        return True
                    # If the neighbor was still not accepted, reverse the changes and continue searching
                    place_into.remove(ride)
                    take_from.append(ride)
                    # Restores the score to where it was before the attempted changes
                    if ride_orig != len(self.solution.cars): self.solution.cars[ride_orig].calculate_score()
                    if ride_dest != len(self.solution.cars): self.solution.cars[ride_dest].calculate_score()

        # No neighbors were accepted :(
        return False
