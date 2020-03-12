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

        # the next value is the minimum (and ideal) start time for the ride
        self.min_start = line[4]

        # the next, and last, value is the maximum end time for the ride
        self.max_end = line[5]

    def write(self):
        output = 'ride ' + str(self.id) + ': '
        output += 'from ' + str(self.orig)
        output += ' to ' + str(self.dest) + ', '
        output += 'earliest start ' + str(self.min_start) + ', '
        output += 'latest finish ' + str(self.max_end)
        print(output)
