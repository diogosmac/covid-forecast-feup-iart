from src.ride import Ride
from typing import List


class Car(object):
    """
    A class that keeps all information relative to a ride

    ...

    Attributes
    ----------
    position : List[int]
        stores the position of the car, during the calculations of the greedy solution and of the car's score
    step : int
        stores the current step of the car, during the calculations of the greedy solution and of the car's score
    bonus : int
        the bonus applied to all rides that start as early as possible, related to the dataset
    allocated_rides : List[Ride]
        the list of rides allocated to the car, in the order that they will be done
    score : int
        the score associated to a car, to prevent the global recalculation of the score for each new solution

    Methods
    -------
    copy()
        generates a different Ride object, with the same characteristics as the one for which it is called
    allocate_ride()
        allocates a ride to the car, and updates the car's score
    allocate_rides()
        sets a car's allocated rides list to the argument passed
    remove_ride()
        removes a ride from the car, and updates the car's score
    has_ride()
        checks whether a given ride is allocated to the car
    sort_rides()
        uses heuristics to define the order in which the rides will be done
    move_to_ride_orig()
        moves the car to the starting point of a ride
    move_to_ride_dest()
        moves the car to the finish point of a ride
    calculate_score()
        calculates the car's score, based on the allocated rides and their order
    write()
        prints the ride's information to the console
    """

    def __init__(self, bonus: int):
        """
        Parameters
        ----------
        bonus : int
            the bonus score associated to all rides that start as early as possible
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

