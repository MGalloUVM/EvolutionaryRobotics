import constants as c
import copy
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
    
    def Spawn(self):
        self.children = {}
        for i in range(c.populationSize):
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in range(c.populationSize):
            self.children[i].Mutate()
    
    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End()

    def Select(self):
        for i in range(c.populationSize):
            if self.Better_Fitness(self.children[i].fitness, self.parents[i].fitness):
                self.parents[i] = self.children[i]
            
    def Show_Best(self):
        bestIndex = 0
        for i in range(1, c.populationSize):
            if self.Better_Fitness(self.parents[i].fitness, self.parents[bestIndex].fitness):
                bestIndex = i
        self.parents[bestIndex].Start_Simulation("GUI")
        print(f"\n\nBest fitness: {self.parents[bestIndex].fitness}")
    
    # Custom method to make switching fitness easier
    def Better_Fitness(self, leftFitness, rightFitness):
        return leftFitness < rightFitness 
    
    def Print(self):
        print('\n\n')
        for i in range(c.populationSize):
            print(f"Parent Fitness: {self.parents[i].fitness}, Child Fitness: {self.children[i].fitness}")
        print('\n')