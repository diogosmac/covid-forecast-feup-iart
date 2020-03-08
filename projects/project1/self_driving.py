class Ride(object):

# a Ride is composed of:
#   - a start point (orig), which is a position on the map [x, y]
#   - a finish point (dest), which is a position on the map [x, y]
#   - an earliest start time (min_start)
#   - a latest finish time (max_end)

    def __init__(self, line):

        # first two values in the line are the coordinates of the origin
        self.orig = list(line[0:2])

        # the next two values are the coordinates of the destination
        self.dest = list(line[2:4])

        # the next value is the minimum (and ideal) start time for the ride
        self.min_start = line[4]

        # the next, and last, value is the maximum end time for the ride
        self.max_end = line[5]
    
    def write(self):
        output = 'ride from ' + str(self.orig)
        output += ' to ' + str(self.dest) + ', '
        output += 'earliest start ' + str(self.min_start) + ', '
        output += 'latest finish ' + str(self.max_end)
        print(output)

class Dataset(object):

# a Dataset is composed of:
#   - a map, defined by the number of rows and columns, as a grid
#   - a fleet of vehicles, for which we receive the size
#   - a set of scheduled rides
#   - a bonus value, which is added to the "score" for each ride that
#       starts exactly on time
#   - a number of steps, which serves the purpose of counting the passage
#       of time as the rides are scheduled and executed

    def __init__(self, filename):

        path = 'inputs/' + filename + '.in'
        with open(path, 'r') as f:

            # the first line holds the dataset values relative to
            # the map, number of vehicles, bonus score and amount
            # of steps 
            [self.rows, self.cols, self.nvehicles,
            self.nrides, self.bonus, self.steps] = \
                [int(n) for n in f.readline().split()]

            # after the initial line, each following line represents
            # a scheduled ride
            self.rides = []
            for ride in range(self.nrides):
                self.rides.append(Ride(f.readline().split()))


def main():

    datasetA = Dataset('a_example')
    datasetB = Dataset('b_should_be_easy')
    datasetC = Dataset('c_no_hurry')
    datasetD = Dataset('d_metropolis')
    datasetE = Dataset('e_high_bonus')

    return 0


if __name__ == '__main__':
    main()
