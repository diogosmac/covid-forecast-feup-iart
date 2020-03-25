from numpy import *


def manhattan_distance(v1, v2):
    return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])


def first_solve(dataset):
    """
    Compute the first solution for the problem, using a greedy approach.

    For each vehicle, save in a list the ride in progress for each time increment (step).
    Then, for each step, go through all vehicles, and check if there are rides that can be allocated to it.
    If so, choose the best one, and then continue.
    """

    dataset.solution = zeros(shape=(dataset.nvehicles, dataset.nrides))

    step = 0
    rides_allocated = zeros(dataset.nrides)
    vehicle_steps = zeros(shape=(dataset.nvehicles, dataset.steps))
    vehicle_positions = [{'current_position': [0, 0]} for _ in range(dataset.nvehicles)]

    while step < dataset.steps:

        for v_id, car in enumerate(vehicle_positions):

            if vehicle_steps[v_id][step]:
                continue

            priority = zeros(dataset.nrides, int)
            priority[:] = iinfo(int).max

            no_rides = True

            r_pointer = -1
            for ride in dataset.rides:
                r_pointer += 1
                if rides_allocated[r_pointer]:
                    continue
                dist_to_car = manhattan_distance(car['current_position'], ride.orig)
                if step + dist_to_car > dataset.steps:
                    continue

                length = manhattan_distance(ride.orig, ride.dest)
                if step + dist_to_car + length > ride.latest_finish:
                    continue

                earliest_start = ride.earliest_start - step
                priority[v_id] = abs(dist_to_car - earliest_start)
                no_rides = False

            if no_rides:
                continue

            r_id = int(argmin(priority))
            ride = dataset.rides[r_id]
            rides_allocated[r_id] = 1
            dist_to_car = manhattan_distance(car['current_position'], ride.orig)
            length = manhattan_distance(ride.orig, ride.dest)
            ride_start = max([step + dist_to_car, ride.earliest_start])
            vehicle_steps[v_id][step: ride_start + length] = ones(shape=(ride_start + length - step,))
            car['current_position'] = ride.dest
            dataset.solution[v_id][r_id] = 1

        step += 1

    return True


def print_solution(dataset):
    v_id = 0
    while v_id < dataset.nvehicles:
        output = 'Vehicle ' + str(v_id) + ': '
        i = 0
        while i < len(dataset.solution[v_id]):
            if dataset.solution[v_id][i]:
                output += str(i) + ' '
        print(output)
        v_id += 1
