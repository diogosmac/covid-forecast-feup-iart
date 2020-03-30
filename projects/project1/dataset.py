from car import Car
from ride import Ride
from solution import Solution
from tqdm import tqdm
import numpy as np


class Dataset(object):

    def __init__(self, filename, from_scratch: bool = False):
        """
        A Dataset is composed of:
            A map, defined by the number of rows and columns, as a grid;
            A fleet of vehicles, for which we receive the size;
            A set of scheduled rides;
            A bonus value, which is added to the "score" for each ride that
                starts exactly on time;
            A number of steps, which serves the purpose of counting the passage
                of time as the rides are scheduled and executed.
        """
        self.extracted_rides = 0

        self.name = filename
        self.input_str = 'inputs/' + filename + '.in'
        self.output_str = 'outputs/' + filename + '.out'

        with open(self.input_str, 'r') as f:
            """
            The first line holds the dataset values relative to
            the map, number of vehicles, bonus score and amount
            of steps.
            """
            [self.rows, self.cols, self.ncars,
             self.nrides, self.bonus, self.steps] = \
                [int(n) for n in f.readline().split()]

            """
            After the initial line, each following line represents
            a scheduled ride.
            """
            self.rides = []
            for ride in range(self.nrides):
                self.rides.append(Ride(self.extracted_rides, [int(n) for n in f.readline().split()]))
                self.extracted_rides += 1

        if from_scratch:
            self.solution = self.empty_solution()
        else:
            self.solution = self.greedy_solve()

    def empty_solution(self) -> Solution:
        return Solution([Car(self.bonus) for _ in range(self.ncars)], self.rides.copy())

    def greedy_solve(self) -> Solution:

        def manhattan_distance(v1, v2):
            return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])

        solution = Solution([Car(self.bonus) for _ in range(self.ncars)], self.rides.copy())

        step = 0
        progress = tqdm(total=self.steps, desc='Building initial solution')

        while step < self.steps:

            for car in solution.cars:

                if car.step > step:
                    continue

                ride_priority = np.zeros(len(solution.unallocated_rides), int)
                ride_priority[:] = np.iinfo(int).max

                rides_available: bool = False

                for ride_id, ride in enumerate(solution.unallocated_rides):

                    distance_to_car = manhattan_distance(car.position, ride.orig)

                    if step + distance_to_car > self.steps:
                        continue

                    if step + distance_to_car + ride.distance > ride.latest_finish:
                        continue

                    earliest_start = ride.earliest_start - step
                    ride_priority[ride_id] = abs(distance_to_car - earliest_start)

                    rides_available = True

                if not rides_available:
                    continue

                ride_id = np.argmin(ride_priority)
                ride = solution.unallocated_rides[int(ride_id)]

                distance_to_car = manhattan_distance(car.position, ride.orig)
                ride_start = max([step + distance_to_car, ride.earliest_start])
                car.step = ride_start + ride.distance

                car.allocate_ride(ride)
                car.position = ride.dest
                solution.unallocated_rides.remove(ride)

            step += 1
            progress.update(1)

        progress.close()

        return solution
