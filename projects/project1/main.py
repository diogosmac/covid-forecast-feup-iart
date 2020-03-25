from dataset import Dataset


def main():
    datasetA = Dataset('a_example')
    datasetB = Dataset('b_should_be_easy')
    datasetC = Dataset('c_no_hurry')
    datasetD = Dataset('d_metropolis')
    datasetE = Dataset('e_high_bonus')

    datasetA.first_solve()
    datasetA.print_solution()

    return 0


if __name__ == '__main__':
    main()
