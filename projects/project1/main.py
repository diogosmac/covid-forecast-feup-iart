from dataset import Dataset
from car import Car
from solution import Solution
from hill_climbing import HillClimbing


def main():
    datasetA = Dataset('a_example')
    datasetB = Dataset('b_should_be_easy')
    datasetC = Dataset('c_no_hurry')
    datasetD = Dataset('d_metropolis')
    datasetE = Dataset('e_high_bonus')

    hill_climbing = HillClimbing(datasetA, 10000)
    hill_climbing.write()

    # get_neighbors test
    #Solution([Car() for _ in range(datasetA.ncars)], datasetA.rides.copy()).get_neighbors()[0].get_neighbors()

    return 0


if __name__ == '__main__':
    main()
