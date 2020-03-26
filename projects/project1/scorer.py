import numpy as np


class Scorer(object):

    @staticmethod
    def calculate(rides: np.array, solution: np.array):
        """
        Calculates solution score based on dataset

        Parameters
        ----------
        rides : Dataset
            Problem's information.
        solution: np.array
            2 dimensional array that contains boolean values

        Returns
        -------
        total_score : int
            solution's score.
        """
        total_score = 0

        for car, ride in zip(solution, rides):
            np.mul()

        return total_score


if __name__ == "__main__":
    print(np.sum(np.multiply([1, 2, 3], [0, 1, 1])))
