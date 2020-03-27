from hill_climbing import HillClimbing
from dataset import Dataset


class SimulatedAnnealing(HillClimbing):
    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    def solve(self):
        return self.solution

