from copy import copy

class Organism:
    def __init__(self, generation, genome):
        self.generation = generation
        self.genome = genome
        self.fitness = None
        self.adjusted_fitness = None
