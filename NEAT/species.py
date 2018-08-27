from operator import attrgetter
from collections import namedtuple

from NEAT.genome import Genome
from NEAT.config import COMPTABILITY_THRESHOLD, SPECIES_PENALIZE_AGE, STAGNANT_SPECIES_PENALTY, SURVIVAL_THRESHOLD

Organism = namedtuple('Organism', ['id', 'generation', 'genome', 'network', 'fitness', 'adjusted_fitness', 'eliminate', 'champion'])
Organism.__new__.__defaults__ = (None, None, False, False)


class Species:
    def __init__(self, rep_org):
        self.organisms = [rep_org]
        self.max_fitness = None
        self.max_fitness_lifetime = None
        self.average_adjusted_fitness = None
        self.age = 0
        self.last_improved_age = 0

    def add(self, org):
        self.organisms.append(org)

    def compute_max_fitness(self):
        self.max_fitness = max(self.organisms, key=attrgetter('fitness')).fitness

    def compatible(self, organism):
        return Genome.compatibility(self.organisms[0].genome, organism.genome) < COMPTABILITY_THRESHOLD

    def new_gen(self):
        self.age += 1

    def compuate_adjusted_fitness(self):
        size = len(self.organisms)

        for org in self.organisms:
            org.adjusted_fitness = org.fitness

            if org.adjusted_fitness < 0:
                org.adjusted_fitness = 0.0001

            org.adjusted_fitness /= size

            self.average_adjusted_fitness += org.adjusted_fitness

        self.average_adjusted_fitness /= len(self.organisms)

    def sort_and_cull(self):
        self.organisms.sort(key=attrgetter('fitness'), reverse=True)
        best_fitness = self.organisms[0].fitness
        if best_fitness > self.max_fitness_lifetime:
            self.last_improved_age = self.age
            self.max_fitness_lifetime = best_fitness

        new_av_fitness = self.average_adjusted_fitness*len(self.organisms)
        num_parents = int(SURVIVAL_THRESHOLD*(len(self.organisms) + 1))

        for i in range(num_parents, len(self.organisms)):
            new_av_fitness -= self.organisms[i].adjusted_fitness
            del self.organisms[i]

        self.average_adjusted_fitness = new_av_fitness/len(self.organisms)