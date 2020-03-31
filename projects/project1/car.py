from ride import Ride
from typing import List


class Car(object):

    def __init__(self, bonus: int):
        """
        A car is composed of:
            A position on the map;
            A current step;
            A list of allocated rides (Object).
        """
        self.position = [0, 0]
        self.step = 0
        self.bonus = bonus

        self.allocated_rides: List[Ride] = []

        self.score = 0

    def copy(self):
        new = Car(self.bonus)
        new.position = self.position
        new.step = self.step
        new.allocated_rides = [ride.copy() for ride in self.allocated_rides]
        new.score = self.score

        return new

    def allocate_ride(self, ride: Ride):
        self.allocated_rides.append(ride)
        self.sort_rides()
        self.calculate_score()

    def allocate_rides(self, rides: List[Ride]):
        self.allocated_rides = rides
        self.sort_rides()

    def remove_ride(self, ride_index: int):
        for ride in self.allocated_rides:
            if ride.id == ride_index:
                self.allocated_rides.remove(ride)
                self.sort_rides()
                self.calculate_score()
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

    def calculate_score(self):
        self.position = [0, 0]
        self.step = 0
        self.sort_rides()

        score = 0
        for ride in self.allocated_rides:
            self.move_to_ride_orig(ride)
            # bonus if ride is started on earliest_start step
            if self.step <= ride.earliest_start:
                score += self.bonus
                self.step = ride.earliest_start
            self.move_to_ride_orig(ride)
            # if ride is made on time calculate score
            if self.step <= ride.latest_finish:
                score = ride.distance

        self.score = score

    def write(self, num):
        print('Car {}'.format(num))
        for ride in self.allocated_rides:
            ride.write()

