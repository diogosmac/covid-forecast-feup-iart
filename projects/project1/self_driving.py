from ride import Ride
from dataset import Dataset


def main():
    datasetA = Dataset('a_example')
    for ride in datasetA.rides:
        ride.write()
    # datasetB = Dataset('b_should_be_easy')
    # datasetC = Dataset('c_no_hurry')
    # datasetD = Dataset('d_metropolis')
    # datasetE = Dataset('e_high_bonus')

    return 0


if __name__ == '__main__':
    main()
