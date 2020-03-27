class Genetic(object):

    def __init__(self, population_size, polling_size, mutation_rate, max_generation_size: int):
        self.population_size = population_size
        self.polling_size = polling_size
        self.mutation_rate = mutation_rate
        self.max_generation_size = max_generation_size
        self.best_fit_queue = []

    def constant_generations(self):
        return len(set(self.best_fit_queue)) == 1

    def queue_best_fit(self, generation):
        if len(self.best_fit_queue) == self.max_generation_size:
            self.best_fit_queue.pop(0)

        self.best_fit_queue.append(generation)

    def reproduce(self, parent_a, parent_b):
        return

    def mutate(self, chromosome):
        return


class Test(object):

    def __init__(self, id):
        self.id = id


# testing :) :-]
if __name__ == "__main__":
    arr = [Test(1), Test(2), Test(3), Test(2)]

    print([t.id for t in arr])

    for t in arr:
        if t.id == 2:
            arr.remove(t)

    print([t.id for t in arr])
