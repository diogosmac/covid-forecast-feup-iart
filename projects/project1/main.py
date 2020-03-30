import sys

from dataset import Dataset
from hill_climbing import HillClimbing
from steepest_ascent import SteepestAscent
from simulated_annealing import SimulatedAnnealing


def main():
    if len(sys.argv) != 2:
        print('Usage: python ' + sys.argv[0] + ' <from_scratch: 0 | 1>')
        return

    from_scratch = bool(int(sys.argv[1]))

    datasetA = Dataset('a_example')
    datasetB = Dataset('b_should_be_easy')
    datasetC = Dataset('c_no_hurry')
    datasetD = Dataset('d_metropolis')
    datasetE = Dataset('e_high_bonus')

    print('\nHill Climbing - Standard')
    hc_standard = HillClimbing(datasetB, from_scratch=from_scratch)
    hc_standard.solve()

    print('\nHill Climbing - Random')
    hc_random = HillClimbing(datasetB, from_scratch=from_scratch, random=True)
    hc_random.solve()

    print('\nHill Climbing (Steepest Ascent) - Standard')
    hc_sa_standard = SteepestAscent(datasetB, from_scratch=from_scratch)
    hc_sa_standard.solve()

    print('\nHill Climbing (Steepest Ascent) - Random')
    hc_sa_random = SteepestAscent(datasetB, from_scratch=from_scratch, random=True)
    hc_sa_random.solve()

    print('\nSimulated Annealing - Standard')
    sa_standard = SimulatedAnnealing(datasetB, from_scratch=from_scratch)
    sa_standard.solve()

    print('\nSimulated Annealing - Random')
    sa_random = SimulatedAnnealing(datasetB, from_scratch=from_scratch, random=True)
    sa_random.solve()


    return 0


if __name__ == '__main__':
    main()
