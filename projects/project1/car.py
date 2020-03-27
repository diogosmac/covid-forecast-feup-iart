from ride import Ride
from typing import List
import random as rd


class Car(object):

    def __init__(self, total_rides: int):
        """
        A car is composed of:
            - a position on the map
            - a current step
            - a list of allocated rides (Object)
        """
        self.position = [0, 0]
        self.step = 0

        self.allocated_rides: List[Ride] = []

    def allocate_ride(self, ride: Ride):
        self.allocated_rides.append(ride)

    def remove_ride(self, ride_index: int):
        for ride in self.allocated_rides:
            if ride.id == ride_index:
                self.allocated_rides.remove(ride)
                return

    def has_ride(self, ride_index: int):
        for ride in self.allocated_rides:
            if ride.id == ride_index:
                return True
        return False

    def sort_rides(self):
        self.allocated_rides.sort(key=lambda ride: ride.earliest_start + ride.latest_start)

    def move_to_ride_orig(self, ride: Ride):
        self.step += abs(self.position[0] - ride.orig[0]) + \
                     abs(self.position[1] - ride.orig[1])
        self.position = ride.orig

    def move_to_ride_dest(self, ride: Ride):
        self.step += abs(self.position[0] - ride.dest[0]) + \
                     abs(self.position[1] - ride.dest[1])
        self.position = ride.dest

    def calculate_score(self, bonus: int) -> int:
        self.position = [0, 0]
        self.step = 0
        self.sort_rides()

        score = 0
        for ride in self.allocated_rides:
            self.move_to_ride_orig(ride)
            # bonus if ride is started on earliest_start step
            if self.step <= ride.earliest_start:
                score += bonus
                self.step = ride.earliest_start
            self.move_to_ride_orig(ride)
            # if ride is made on time calculate score
            if self.step <= ride.latest_finish:
                score = ride.distance

        return score

    def mutate(self) -> int:
        return 0
