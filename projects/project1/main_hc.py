import sys

from src.dataset import Dataset
from src.hill_climbing import HillClimbing
from src.steepest_ascent import SteepestAscent
from src.simulated_annealing import SimulatedAnnealing


def main():
    if len(sys.argv) < 3:
        print('Usage:\tpython ' + sys.argv[0] + ' <from scratch> <input file>\n')
        print('\t<from scratch> : Determines whether the solution will be calculated')
        print('\t                 from scratch or from a greedy starting point')
        print('\t                 Options: 0 | 1\n')
        print('\t<input file>   : The file from which the dataset will be extracted')
        print('\t                 Options: a_example\n'
              '\t                          b_should_be_easy\n'
              '\t                          c_no_hurry\n'
              '\t                          d_metropolis\n'
              '\t                          e_high_bonus\n')
        return

    from_scratch = bool(int(sys.argv[1]))
    entry_file = sys.argv[2]

    dataset = Dataset(entry_file, from_scratch)

    print('\nHill Climbing - Standard')
    hc_standard = HillClimbing(dataset)
    hc_standard.solve()

    print('\nHill Climbing - Random')
    hc_random = HillClimbing(dataset, random=True)
    hc_random.solve()

    print('\nHill Climbing (Steepest Ascent) - Standard')
    hc_sa_standard = SteepestAscent(dataset)
    hc_sa_standard.solve()

    print('\nHill Climbing (Steepest Ascent) - Random')
    hc_sa_random = SteepestAscent(dataset, random=True)
    hc_sa_random.solve()

    print('\nSimulated Annealing - Standard')
    sa_standard = SimulatedAnnealing(dataset)
    sa_standard.solve()

    print('\nSimulated Annealing - Random')
    sa_random = SimulatedAnnealing(dataset, random=True)
    sa_random.solve()

    print()

    return 0


if __name__ == '__main__':
    main()
