class Ride(object):

    def __init__(self, ident, line):
        """
        A Ride is composed of:
            - a start point (orig), which is a position on the map [x, y]
            - a finish point (dest), which is a position on the map [x, y]
            - an earliest start time (min_start)
            - a latest finish time (max_end)
        """
        # each ride has an ID, for assignment in the end
        self.id = ident

        # first two values in the line are the coordinates of the origin
        self.orig = list(line[0:2])

        # the next two values are the coordinates of the destination
        self.dest = list(line[2:4])

        # with orig and dest we can calculate the distance (score) of the ride
        self.distance = abs(self.orig[0] - self.dest[0]) + abs(self.orig[1] - self.dest[1])

        # the next value is the minimum (and ideal) start time for the ride
        self.earliest_start = line[4]

        # the next, and last, value is the maximum end time for the ride
        self.latest_finish = line[5]

        # the next value is the minimum (and ideal) start time for the ride
        self.latest_start = self.latest_finish - self.distance

    def copy(self):
        return Ride(self.id,
                    [self.orig[0], self.orig[1], self.dest[0], self.dest[1], self.earliest_start, self.latest_finish])

    def write(self):
        output = 'ride ' + str(self.id) + ': '
        output += 'from ' + str(self.orig)
        output += ' to ' + str(self.dest) + ', '
        output += ' total distance ' + str(self.dest) + ', '
        output += 'earliest start ' + str(self.earliest_start) + ', '
        output += 'latest finish ' + str(self.latest_finish)
        print(output)
