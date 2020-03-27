from typing import List
from car import Car
from ride import Ride

import random as rd


class Solution(object):

    def __init__(self, cars: List[Car], rides: List[Ride]):
        self.cars: List[Car] = cars
        self.unallocated_rides: List[Ride] = rides
        self.fitness = 0

    def copy(self):
        return Solution([car.copy() for car in self.cars], [ride.copy() for ride in self.unallocated_rides])

    def calculate_fitness(self, bonus: int):
        self.fitness = sum(car.calculate_score(bonus) for car in self.cars)

    def mutate(self):
        rd.choice(self.cars).mutate()

    def write(self):
        for i, car in enumerate(self.cars):
            print('Car ' + str(i) + ': ' + ' '.join(['%d'] * len(car.allocated_rides))
                  % tuple([ride.id for ride in car.allocated_rides]))

    def get_neighbors(self):
        return self
