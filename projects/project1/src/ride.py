from typing import List


class Ride(object):
    """
    A class that keeps all information relative to a ride

    ...

    Attributes
    ----------
    id : int
        the id of the ride, relative to the dataset
    orig : List[int]
        the coordinates of the starting point for the ride
    dest : List[int]
        the coordinates of the finish point for the ride
    distance : int
        the Manhattan distance between the ride's starting and finish points
    earliest_start : int
        the earliest step in the problem at which the ride can be started
    latest_finish : int
        the latest step at which the ride must be finished in order to be scored
    latest_start : int
        the latest time at which a ride can be started in order to still finish on time

    Methods
    -------
    copy()
        generates a different Ride object, with the same characteristics as the one for which it is called
    write()
        prints the ride's information to the console
    """

    def __init__(self, ident: int, line: List[int]):
        """
        Parameters
        ----------
        ident : int
            the id for the ride
        line : List[int]
            the numerical inputs used to generate the ride
        """
        self.id = ident
        self.orig = list(line[0:2])
        self.dest = list(line[2:4])
        self.earliest_start = line[4]
        self.latest_finish = line[5]
        # with orig and dest we can calculate the distance (score) of the ride
        self.distance = abs(self.orig[0] - self.dest[0]) + abs(self.orig[1] - self.dest[1])
        # the next value is the minimum (and ideal) start time for the ride
        self.latest_start = self.latest_finish - self.distance

    def copy(self):
        return Ride(self.id,
                    [self.orig[0], self.orig[1], self.dest[0], self.dest[1], self.earliest_start, self.latest_finish])

    def write(self):
        print('ride {}: from {} to {}, total distance {}, earliest start {}, latest finish {}'.format(
            self.id, self.orig, self.dest, self.distance, self.earliest_start, self.latest_finish))
