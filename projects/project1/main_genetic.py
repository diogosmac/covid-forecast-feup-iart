import sys

from dataset import Dataset
from genetic import Genetic


def main():
    if len(sys.argv) < 2:
        print('Usage:\tpython ' + sys.argv[0] + ' <input file>\n')
        print('\t<input file>   : The file from which the dataset will be extracted')
        print('\t                 Options: a_example\n'
              '\t                          b_should_be_easy\n'
              '\t                          c_no_hurry\n'
              '\t                          d_metropolis\n'
              '\t                          e_high_bonus\n')
        
        return

    entry_file = sys.argv[1]
    dataset = Dataset(entry_file, from_scratch=True)

    genetic_1 = Genetic(dataset)
    print('\n' + genetic_1.write_configuration() + '\n')
    genetic_1.execute()

    return 0


if __name__ == '__main__':
    main()
