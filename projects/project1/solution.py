from typing import List
from car import Car
from ride import Ride

import random as rd


class Solution(object):

    def __init__(self, cars: List[Car], rides: List[Ride]):
        self.cars: List[Car] = cars
        self.unallocated_rides: List[Ride] = rides
        self.fitness: int = 0
        self.nrides = len(rides)

    def copy(self):
        return Solution([car.copy() for car in self.cars], [ride.copy() for ride in self.unallocated_rides])

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
            allocated_rides: List[Ride] = [self.unallocated_rides[ride_index] for ride_index, val in enumerate(binary_list) if val]
            car.allocate_rides(allocated_rides)
            car.calculate_score()
        self.unallocated_rides = []

    def mutate(self):
        possible_ride_positions: List[int] = list(range(len(self.cars)))

        first_choice = possible_ride_positions.copy()
        take_from = None
        ride_orig = None
        while not take_from:
            ride_orig = rd.choice(first_choice)
            first_choice.remove(ride_orig)

            take_from = self.cars[ride_orig]

        second_choice = possible_ride_positions.copy()
        second_choice.remove(ride_orig)
        ride_dest = rd.choice(second_choice)
        place_into = self.cars[ride_dest]

        ride = rd.choice(take_from.allocated_rides)
        take_from.remove_ride(ride.id)
        place_into.allocate_ride(ride)

        self.calculate_fitness()

    def write(self):
        for i, car in enumerate(self.cars):
            print('Car ' + str(i) + ': ' + ' '.join(['%d'] * len(car.allocated_rides))
                  % tuple([ride.id for ride in car.allocated_rides]))


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