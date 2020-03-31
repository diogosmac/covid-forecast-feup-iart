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
            self.unallocated_rides = list(set(self.unallocated_rides) - set(allocated_rides))
        # last car is allocated the rest of unallocated rides
        self.cars[len(self.cars) - 1].allocate_rides(self.unallocated_rides)
        self.unallocated_rides = []

    def matrix_allocation(self, binary_matrix: List[List[bool]]):
        for car, binary_list in zip(self.cars, binary_matrix):
            # get indexes of True elements in binary list
            allocated_rides: List[Ride] = [self.unallocated_rides[ride_index] for ride_index, val in enumerate(binary_list) if val]
            car.allocate_rides(allocated_rides)
        self.unallocated_rides = []

    def mutate(self):
        possible_ride_placements: List[int] = list(range(len(self.cars) + 1))

        first_choice = possible_ride_placements.copy()
        take_from = None
        ride_orig = None
        while not take_from:
            ride_orig = rd.choice(first_choice)
            first_choice.remove(ride_orig)

            if ride_orig == len(self.cars):
                take_from = self.unallocated_rides
            else:
                take_from = self.cars[ride_orig].allocated_rides

        second_choice = possible_ride_placements.copy()
        second_choice.remove(ride_orig)
        ride_dest = rd.choice(first_choice)
        if ride_dest == len(self.cars):
            place_into = self.unallocated_rides
        else:
            place_into = self.cars[ride_orig].allocated_rides

        ride = rd.choice(take_from)
        take_from.remove(ride)
        place_into.append(ride)

        if ride_orig != len(self.cars): self.cars[ride_orig].calculate_score()
        if ride_dest != len(self.cars): self.cars[ride_dest].calculate_score()

    def write(self):
        for i, car in enumerate(self.cars):
            print('Car ' + str(i) + ': ' + ' '.join(['%d'] * len(car.allocated_rides))
                  % tuple([ride.id for ride in car.allocated_rides]))

    # Progressively allocates rides
    def get_neighbors(self):

        sol_list = []
        ride_starting_index = 0

        while ride_starting_index < len(self.unallocated_rides):

            ride_index = ride_starting_index

            # generate a new solution
            new_car_list = []
            new_ride_list = self.unallocated_rides.copy()

            for car_index in range(0, len(self.cars)):
                current_car = self.cars[car_index].copy()
                current_ride = self.unallocated_rides[ride_index]

                if current_ride in new_ride_list:
                    current_car.allocate_ride(current_ride)  # add the ride to the car
                    new_ride_list.remove(current_ride)  # remove the ride from the list

                new_car_list.append(current_car)  # add the car to the list

                ride_index = (ride_index + 1) % (len(self.unallocated_rides))

            # Add the solution
            sol = Solution(new_car_list, new_ride_list)
            sol_list.append(sol)

            ride_starting_index += 1

        return sol_list

    def write(self):
        print('Fitness: {}'.format(self.fitness))
        for car_index in range(len(self.cars)):
            self.cars[car_index].write(car_index)

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