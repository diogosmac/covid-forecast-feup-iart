from hill_climbing import HillClimbing
from dataset import Dataset


class SteepestAscent(HillClimbing):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    def choose_next(self):

        neighbors = self.solution.get_neighbors()

        score = self.solution.calculate_fitness(self.dataset.bonus)
        next_solution = None

        for neighbor in neighbors:
            new_score = neighbor.calculate_fitness(self.dataset.bonus)
            if new_score > score:
                score = new_score
                next_solution = neighbor

        return next_solution
