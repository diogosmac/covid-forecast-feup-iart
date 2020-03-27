from typing import List
from car import Car

import random as rd

class Solution(object):

    def __init__(self, cars: List[Car]):
        self.cars = cars
        self.fitness = 0

    def calculate_fitness(self):
        self.fitness = sum(car.score for car in self.cars)

    def mutate(self):
        rd.choice(self.cars).mutate()
                
