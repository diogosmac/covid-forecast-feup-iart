from dataset import Dataset
from hill_climbing import HillClimbing
from solution_draft import *


def main():
    datasetA = Dataset('a_example')
    datasetB = Dataset('b_should_be_easy')
    datasetC = Dataset('c_no_hurry')
    datasetD = Dataset('d_metropolis')
    datasetE = Dataset('e_high_bonus')

    hill_climbing = HillClimbing(datasetA, 10000)
    hill_climbing.write()

    return 0


if __name__ == '__main__':
    main()
