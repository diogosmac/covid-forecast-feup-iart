import random
import time

class Solution(object):
    def __init__(self, init):
        self.solution = init
        with open('timetabling.in', 'r') as f:
            self.turmas = []
            [self.nSlots, self.nDisciplinas] = \
                [int(n) for n in f.readline().split()]
            for _ in range(self.nDisciplinas):
                self.turmas.append([int(n) for n in f.readline().split()])
    
    def calc_incompats(self):
        for i in range(self.nDisciplinas):
            turma1 = self.turmas[i]
            for j in range(i+1, self.nDisciplinas):
                turma2 = self.turmas[j]
                inter = list(set(turma1).intersection(turma2))
                if not len(inter) == 0:
                    print('Turmas ' + str(i+1) + '-' + str(j+1))
                    print(list(set(turma1).intersection(turma2)))


    def eval(self, solution):

        def get_incompats(t1, t2):
            turma1 = self.turmas[t1]
            turma2 = self.turmas[t2]
            return list(set(turma1).intersection(turma2))

        sobrepostos = set()
        for i in range(self.nDisciplinas):
            for j in range(i+1, self.nDisciplinas):
                if solution[i] != solution[j]:
                    continue
                for aluno in get_incompats(i, j):
                    sobrepostos.add(aluno)

        return len(list(sobrepostos))


    def solve_hillclimb(self):

        def improve_with_neighbours():
            neigh = []
            min_eval = self.eval(self.solution)
            for i in range(self.nDisciplinas):
                for j in range(1, self.nSlots + 1):
                    if j != self.solution[i]:
                        new_sol = self.solution.copy()
                        new_sol[i] = j
                        val = self.eval(new_sol)
                        if val < min_eval:
                            neigh = new_sol
                            min_eval = val
                        elif val == min_eval:
                            if bool(random.getrandbits(1)):
                                neigh = new_sol
            return neigh

        print('\tStarting!', str(self.solution) + ' -> ' + str(self.eval(self.solution)))

        start = time.time()

        count = 0
        while time.time() - start < 1:
            new_sol = improve_with_neighbours()
            if new_sol == []:
                break
            self.solution = new_sol
            count += 1

        elapsed = time.time() - start

        print('\t-> After ' + str(count) + ' iterations in ' + str(round(elapsed, 2)) + ' seconds ...')
        print('\tDone!\t ', str(self.solution) + ' -> ' + str(self.eval(self.solution)))

        return count


def test_hillclimb():

    sol_final = []
    score = 13
    count = 0

    for i in range(10):

        print('Iteration ' + str(i+1))
        sol = Solution([1,1,1,1,1,1,1,1,1,1,1,1])     # valores todos iguais
        # sol = Solution([1,1,1,2,2,2,3,3,3,4,4,1])     # muito perto da solução ótima
        # sol = Solution([1,1,4,2,2,2,3,3,3,4,4,1])     # mínimo local
        # sol = Solution([1,2,3,4,1,2,3,4,1,2,3,4])     # mínimo local II: electric boogaloo

        new_c = sol.solve_hillclimb()
        new_score = sol.eval(sol.solution)

        if new_score < score:
            sol_final = sol.solution
            score = new_score
            count = new_c
            print('Updated Data!')

        elif new_score == score:
            if new_c < count:
                sol_final = sol.solution
                count = new_c
                print('Updated Data!')
    

    print('\nDone! Final Solution: ' + str(sol_final))
    print('Number of iterations: ' + str(count))
    print('Number of overlaps: ' + str(score) + '\n')




def main():

    print('\nTimetabling Problem!')
    test_hillclimb()





if __name__ == '__main__':
    main()