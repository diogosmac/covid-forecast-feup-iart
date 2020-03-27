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

    # Progressively allocates rides
    def get_neighbors(self):
        sol_list = []

        ride_starting_index = 0

        while ride_starting_index < (len(self.unallocated_rides)):
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
            sol.write()

            ride_starting_index += 1

        return sol_list
