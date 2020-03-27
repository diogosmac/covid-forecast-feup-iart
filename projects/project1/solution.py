from typing import List
from car import Car
from ride import Ride

import random as rd


class Solution(object):

    def __init__(self, cars: List[Car]):
        self.cars = cars

    def calculate_fitness(self, bonus: int):
        return sum(car.calculate_score(bonus) for car in self.cars)


    def mutate(self):
        rd.choice(self.cars).mutate()


# testing :)
if __name__ == "__main__":
    car1: Car = Car()
    car1.allocate_ride(Ride(0, [0, 1, 2, 3, 4, 5]))
    car1.allocate_ride(Ride(1, [0, 1, 2, 3, 4, 5]))
    car1.allocate_ride(Ride(2, [0, 1, 2, 3, 4, 5]))

    car2: Car = Car()
    car2.allocate_ride(Ride(3, [0, 1, 2, 3, 4, 5]))
    car2.allocate_ride(Ride(4, [0, 1, 2, 3, 4, 5]))
    car2.allocate_ride(Ride(5, [0, 1, 2, 3, 4, 5]))

    list_1 = [car1, car2]
    list_2 = list_1.copy()

    list_2.pop(0)

    for car in list_1:
        print(car.allocated_rides)

    print()
    for car in list_2:
        print(car.allocated_rides)
