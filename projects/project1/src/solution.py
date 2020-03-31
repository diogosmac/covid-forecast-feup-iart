import random as rd

from typing import List
from src.car import Car
from src.ride import Ride


class Solution(object):
    """
    A class that saves any given solution to the Self Driving Rides problem

    ...

    Attributes
    ----------
    cars : List[Car]
        list of available cars, relative to the dataset
    unallocated_rides : List[Ride]
        list of rides that are not allocated to any car
    fitness : int
        the score for a given solution
    nrides : int
        the total number of rides, relative to the dataset

    Methods
    -------
    copy()
        generates a copy of the solution, which can be manipulated independently
    calculate_fitness()
        calculates the solution's score
    randomize_allocation()
        allocates all rides on the solution to cars, randomly
    matrix_allocation()
        allocates the rides to cars based on a binary matrix
    mutate()
        transforms a solution into a random neighbor
    write()
        prints the solution to the console
    """

    def __init__(self, cars: List[Car], rides: List[Ride]):
        """
        Parameters
        ----------
        cars : List[Car]
            list of cars belonging to the solution
        rides : List[Ride]
            
        """
        self.cars: List[Car] = cars
        self.unallocated_rides: List[Ride] = rides
        self.fitness: int = 0
        self.nrides = len(rides)

    def copy(self):
        return Solution([car.copy() for car in self.cars], self.unallocated_rides.copy())

    def calculate_fitness(self):
        self.fitness = sum(car.score for car in self.cars)

    def randomize_allocation(self):
        rides_per_car: int = len(self.unallocated_rides) // len(self.cars)
        # allocate random rides to cars
        for car_index in range(len(self.cars) - 1):
            allocated_rides: List[Ride] = rd.sample(self.unallocated_rides, rides_per_car)
            self.cars[car_index].allocate_rides(allocated_rides)
            self.cars[car_index].calculate_score()
            self.unallocated_rides = list(set(self.unallocated_rides) - set(allocated_rides))
        # last car is allocated the rest of unallocated rides
        self.cars[len(self.cars) - 1].allocate_rides(self.unallocated_rides)
        self.cars[len(self.cars) - 1].calculate_score()
        self.unallocated_rides = []

    def matrix_allocation(self, binary_matrix: List[List[bool]]):
        for car, binary_list in zip(self.cars, binary_matrix):
            # get indexes of True elements in binary list
            allocated_rides: List[Ride] = \
                [self.unallocated_rides[ride_index] for ride_index, val in enumerate(binary_list) if val]
            car.allocate_rides(allocated_rides)
            car.calculate_score()
        self.unallocated_rides = []

    def mutate(self):
        possible_ride_positions: List[int] = list(range(len(self.cars)))

        first_choice = possible_ride_positions.copy()
        ride_orig = None
        take_from = None
        while not take_from:
            if not first_choice:
                return
            ride_orig = rd.choice(first_choice)
            first_choice.remove(ride_orig)

            take_from = self.cars[ride_orig].allocated_rides

        second_choice = possible_ride_positions.copy()
        second_choice.remove(ride_orig)
        ride_dest = rd.choice(second_choice)

        ride = rd.choice(self.cars[ride_orig].allocated_rides)
        self.cars[ride_orig].remove_ride(ride.id)
        self.cars[ride_dest].allocate_ride(ride)

        self.calculate_fitness()

    def write(self):
        for i, car in enumerate(self.cars):
            print('Car ' + str(i) + ': ' + ' '.join(['%d'] * len(car.allocated_rides))
                  % tuple([ride.id for ride in car.allocated_rides]))
