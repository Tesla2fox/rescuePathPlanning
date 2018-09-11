from platypus import NSGAIII, DTLZ2
#from platypus.algorithms





import platypus as ps
import random

perm = ps.Permutation([1,2,3,4])
wtf = perm.__str__

#perm.__str__
#perm.
print(perm.encode(1))
print(perm.elements)


class MyProblem(ps.Problem):
    def __init__(self, nobjs = 2):
        super(MyProblem,self).__init__(nvars = 2,nobjs =2)
#        self.types [:] = Real*
        self.types[:] = ps.Real(-5,5)
    def evaluate(self,solution):        
        solution.objectives[:] = solution.variables[:]
#        print(solution.objectives[:])
    def random(self):
        solution = ps.Solution(self)
        solution.variables[:] = [random.uniform(0,5) for _ in range(self.types)]
        solution.evaluate()
        return solution
        
# define the problem definition
problem = MyProblem()

# instantiate the optimization algorithm
algorithm = NSGAIII(problem,20)

# optimize the problem using 10,000 function evaluations
algorithm.run(10000)

# plot the results using matplotlib
import matplotlib.pyplot as plt

plt.scatter([s.objectives[0] for s in algorithm.result],
            [s.objectives[1] for s in algorithm.result])
plt.xlim([-5.1, 5.1])
plt.ylim([-5.1, 5.1])
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_2(x)$")
plt.show()


import numpy