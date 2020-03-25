from numpy import *
from tqdm import tqdm


def manhattan_distance(v1, v2):
    return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])


def first_solve(dataset):
    """
    Compute the first solution for the problem, using a greedy approach.

    For each vehicle, save in a list the ride in progress for each time increment (step).
    Then, for each step, go through all vehicles, and check if there are rides that can be allocated to it.
    If so, choose the best one, and then continue.
    """

    def print_solution(d):
        """
        For each vehicle, print the rides assigned to it
        """
        v = 0
        while v < d.nvehicles:
            if dataset.output[v]:
                output = 'Vehicle ' + str(v) + ':'
                for r in dataset.output[v]:
                    output += ' ' + str(r)
                print(output)
            v += 1

    dataset.output = [[] for _ in range(dataset.nvehicles)]

    rides_allocated = zeros(dataset.nrides)
    vehicle_taken = zeros((dataset.nvehicles, dataset.steps))
    vehicle_positions = [[0, 0] for _ in range(dataset.nvehicles)]

    print('Solving ' + dataset.name + ' . . .')
    progress = tqdm(total=dataset.steps, desc='Progress')

    step = 0
    while step < dataset.steps:

        for v_id, v_pos in enumerate(vehicle_positions):

            if vehicle_taken[v_id][step]:
                continue

            r_priority = zeros(dataset.nrides, int)
            r_priority[:] = iinfo(int).max

            rides_available = False

            for r_id, ride in enumerate(dataset.rides):

                if rides_allocated[r_id]:
                    continue

                dist_to_car = manhattan_distance(v_pos, ride.orig)

                if step + dist_to_car > dataset.steps:
                    continue

                ride_len = manhattan_distance(ride.orig, ride.dest)
                if step + dist_to_car + ride_len > ride.latest_finish:
                    continue

                earliest_start = ride.earliest_start - step
                r_priority[r_id] = abs(dist_to_car - earliest_start)

                rides_available = True

            if not rides_available:
                continue

            r_id = argmin(r_priority)
            ride = dataset.rides[r_id]
            rides_allocated[r_id] = 1

            dist_to_car = manhattan_distance(v_pos, ride.orig)
            ride_start = max([step + dist_to_car, ride.earliest_start])
            ride_len = manhattan_distance(ride.orig, ride.dest)
            vehicle_taken[v_id][step: ride_start + ride_len] = ones((ride_start + ride_len - step,))

            dataset.output[v_id].append(r_id)
            vehicle_positions[v_id] = ride.dest

        step += 1
        progress.update(1)

    progress.close()
    print("Done!")

    print_solution(dataset)

    return True
