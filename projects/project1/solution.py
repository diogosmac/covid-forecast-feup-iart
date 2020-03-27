from typing import List
from car import Car
from ride import Ride

import random as rd


class Solution(object):

    def __init__(self, nvehicles: int, rides: List[Ride]):
        self.cars: List[Car] = [Car() for _ in range(nvehicles)]
        self.unallocated_rides: List[Ride] = rides
        self.fitness = 0

    def calculate_fitness(self, bonus: int):
        self.fitness = sum(car.calculate_score(bonus) for car in self.cars)

    def mutate(self):
        rd.choice(self.cars).mutate()

    def write(self):
        for i, car in enumerate(self.cars):
            output = 'Car ' + str(i) + ':'
            for ride in car.allocated_rides:
                output += ' ' + str(ride.id)
            print(output)
