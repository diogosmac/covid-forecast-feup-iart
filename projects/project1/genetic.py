from typing import List
from dataset import Dataset
from solution import Solution
from tqdm import tqdm
from car import Car
import time as tm
import random as rd


class Genetic(object):
    """
    A class used to perform a genetic algorithm given a dataset and
    regular algorithm related attributes

    ...

    Attributes
    ----------
    dataset : Dataset
        a Dataset instance containing information about the problem
    generation : int
        the current generation number
    population : List[Solution]
        a list containing the population, i.e list of chromosomes
    max_population_size : int
        the max number of chromosomes (population size) in each generation
    polling_size : int
        the number of chromosomes in a population that will be used to reproduce
    mutation_rate : float
        the chance of a chromosome being mutated
    constant_generations_num: int
        the number of in a row generations of constant best fit chromosome
        when this happens execution stops
    max_generations: int
        the number of max generations before the algorithm stops
    best_fit : Solution
        the current generation's best chromosome
    best_fit_queue : List[int]
        a list containing the fitness of the last best chromosomes

    Methods
    -------
    execute()
        executes the algorithm
    sort_population()
        sorts chromosomes in population from best fit to worst fit
    create_random_population()
        creates random population with size equal to max_population_size
    constant_generations() -> bool
        returns true if the last generations had no improvement in the last best_fit
    queue_best_fit()
        places the current's generation best fit in the best_fit queue
    reproduce(parent_a : Solution, parent_b : Solution) -> List[Solution]
        returns two chromosomes which were the result of crossing over parent_a and parent_b
    solution_to_matrix(solution : Solution) -> List[Solution]
        transforms the chromosome in a two-dimensional binary list representation
    matrix_to_solution(matrix: List[List[bool]]) -> Solution
        transforms a two-dimensional binary list into a chromosome
    write() -> str
        returns a string containing the information about the current generation
    write_configuration() -> str
        returns a string containing information about algorithm options
    """

    def __init__(self, dataset: Dataset, max_population_size: int = 500, polling_size: int = 50,
                 mutation_rate: float = 0.01, constant_generations_num: int = 10, max_generations: int = 200):
        """
        Parameters
        ----------
        dataset : Dataset
            a Dataset instance containing information about the problem
        max_population_size : int
            the number of chromosomes (population) in each generation
        polling_size : int
            the number of chromosomes in a population that will be used to reproduce
        mutation_rate : float
            the chance of a chromosome being mutated
        constant_generations_num: int
            the number of in a row generations of constant best fit chromosome
            when this happens execution stops
        max_generations: int
            the number of max generations before the algorithm stops
        """
        self.dataset = dataset
        self.generation: int = 1
        self.population: List[Solution] = []
        self.max_population_size: int = max_population_size
        self.polling_size: int = polling_size
        self.mutation_rate: float = mutation_rate
        self.constant_generations_num: int = constant_generations_num
        self.max_generations: int = max_generations

        self.best_fit: Solution
        self.best_fit_queue: List[int] = [i for i in range(5)]

    def execute(self):
        """
        executes the algorithm
        """
        progress = tqdm(total=self.max_generations, desc='Applying genetic algorithm')
        start = tm.time()
        # create first population
        self.create_random_population()
        # calculate new population's fitness
        for solution in self.population:
            solution.calculate_fitness()
        # sort from best to worst
        self.sort_population()
        self.best_fit = self.population[0]
        initial_best = self.best_fit.fitness
        progress.write(self.write())

        progress_new_population = tqdm(total=self.max_population_size, desc='Creating new population')
        while not self.constant_generations():
            # create new population
            new_population: List[Solution] = []
            progress_new_population.reset()
            pop_start = tm.time()
            while len(new_population) < self.max_population_size:
                # choose the best n (polling size) of population
                parent_a = self.population[rd.randint(0, self.polling_size - 1)]
                parent_b = self.population[rd.randint(0, self.polling_size - 1)]
                children = self.reproduce(parent_a, parent_b)
                # slight chance of mutation
                if rd.random() < self.mutation_rate:
                    children[0].mutate()
                if rd.random() < self.mutation_rate:
                    children[1].mutate()
                new_population.append(children[0])
                new_population.append(children[1])
                # update population progress bar
                progress_new_population.update(2)
                # updates time elapsed
                progress_new_population.set_postfix_str(
                    'Generated Chromosomes = {}, Time Elapsed = {:.2f} seconds'.format(
                        len(new_population), tm.time() - pop_start))
                progress.set_postfix_str(
                    'Current Score = {}, New Generation Count = {}, Time Elapsed = {:.2f} seconds'.format(
                        self.best_fit.fitness, self.generation - 1, tm.time() - start
                    ))

            self.population = new_population
            self.generation += 1
            progress.update(1)
            # calculate new population's fitness
            for solution in self.population:
                solution.calculate_fitness()
            # sort from best to worst
            self.sort_population()
            # new best might not be better than the old best
            if self.population[0].fitness > self.best_fit.fitness:
                self.best_fit = self.population[0]
            # enqueue best solution in current population
            self.queue_best_fit()
            progress.write(self.write())
            # Displays the current score after an iteration
            progress.set_postfix_str(
                'Current Score = {}, Generation Count = {}, Time Elapsed = {:.2f} seconds'.format(
                    self.best_fit.fitness, self.generation, tm.time() - start
                ))

        elapsed = tm.time() - start
        progress.update(self.max_population_size)
        progress.set_postfix_str('Current Score = {}, Time Elapsed = {:.2f} seconds'.format(
            self.best_fit, tm.time() - start
        ))
        progress.write('\n')
        progress.write('Initial Score: {}'.format(initial_best))
        progress.write('Final Score: {}'.format(self.best_fit.fitness))
        progress.write('Gain in Score: {}'.format(self.best_fit.fitness - initial_best))
        progress.write('Time elapsed: {} seconds'.format(elapsed))
        progress.close()

    def sort_population(self):
        """
        sorts chromosomes in population from best fit to worst fit
        """
        self.population.sort(key=lambda solution: solution.fitness, reverse=True)

    def create_random_population(self):
        """
        creates random population with size equal to max_population_size
        """
        start = tm.time()
        progress = tqdm(total=self.max_population_size, desc='Creating first random population')
        while len(self.population) < self.max_population_size:
            cars: List[Car] = [Car(self.dataset.bonus) for _ in range(self.dataset.ncars)]
            random_solution: Solution = Solution(cars, self.dataset.rides.copy())
            random_solution.randomize_allocation()
            self.population.append(random_solution)
            progress.update(1)
            progress.set_postfix_str(
                'Generated Chromosomes = {}, Time Elapsed = {:.2f} seconds'.format(
                    len(self.population), tm.time() - start))
        progress.close()
        progress.clear()

    def constant_generations(self) -> bool:
        """
        returns true if the last generations had no improvement in the last best_fit
        """
        return len(set(self.best_fit_queue)) == 1

    def queue_best_fit(self):
        """
        places the current's generation best fit in the best_fit queue
        """
        if len(self.best_fit_queue) == self.constant_generations_num:
            self.best_fit_queue.pop(0)
        self.best_fit_queue.append(self.best_fit)

    def reproduce(self, parent_a: Solution, parent_b: Solution) -> List[Solution]:
        """
        returns two chromosomes which were the result of crossing over parent_a and parent_b
        """
        parent_a_matrix = self.solution_to_matrix(parent_a)
        parent_b_matrix = self.solution_to_matrix(parent_b)
        child_a_matrix: List[List[bool]] = []
        child_b_matrix: List[List[bool]] = []

        crossover_index: int = rd.randint(1, self.dataset.nrides - 1)
        for parent_a_car, parent_b_car in zip(parent_a_matrix, parent_b_matrix):
            child_a_matrix.append(parent_a_car[0:crossover_index] + parent_b_car[crossover_index:self.dataset.nrides])
            child_b_matrix.append(parent_b_car[0:crossover_index] + parent_a_car[crossover_index:self.dataset.nrides])

        child_a = self.matrix_to_solution(child_a_matrix)
        child_a.calculate_fitness()
        child_b = self.matrix_to_solution(child_b_matrix)
        child_b.calculate_fitness()

        return [child_a, child_b]

    def solution_to_matrix(self, solution: Solution) -> List[List[bool]]:
        """
        transforms a two-dimensional binary list into a chromosome
        """
        matrix: List[List[bool]] = []
        for car in solution.cars:
            binary_list: List[bool] = [False] * self.dataset.nrides
            for ride in car.allocated_rides:
                binary_list[ride.id] = True
            matrix.append(binary_list)
        return matrix

    def matrix_to_solution(self, matrix: List[List[bool]]) -> Solution:
        """
        transforms a two-dimensional binary list into a chromosome
        """
        cars: List[Car] = [Car(self.dataset.bonus) for _ in range(self.dataset.ncars)]
        solution: Solution = Solution(cars, self.dataset.rides.copy())
        solution.matrix_allocation(matrix)
        return solution

    def write(self) -> str:
        """
        returns a string containing information about the current generation
        """
        return 'Generation {} best fit: {}'.format(self.generation, self.best_fit.fitness)

    def write_configuration(self) -> str:
        """
        returns a string containing information about algorithm options
        """
        return 'Max Generations: {}\nMax Population Size: {}\nPolling Size: {}\nMutation Chance: {}\nConstant Generation Size: {}'.format(
            self.max_generations, self.max_population_size, self.polling_size, self.mutation_rate,
            self.constant_generations_num)
