from typing import List
from car import Car

import random as rd


class Solution(object):

    def __init__(self, cars: List[Car]):
        self.cars = cars
        self.fitness = 0

    def calculate_fitness(self, bonus: int):
        self.fitness = sum(car.calculate_score(bonus) for car in self.cars)

    def mutate(self):
        rd.choice(self.cars).mutate()
