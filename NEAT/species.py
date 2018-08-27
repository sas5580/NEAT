from operator import attrgetter
from collections import namedtuple
from random import uniform
from math import sqrt

from NEAT.config import COMPTABILITY_THRESHOLD, SURVIVAL_THRESHOLD, PERCENT_NO_CROSSOVER, MATE_ONLY_PROB
from NEAT.genome import Genome
from NEAT.organism import Organism


class Species:
    def __init__(self, rep_org):
        self.organisms = [rep_org]
        self.max_fitness = None
        self.max_fitness_lifetime = None
        self.average_adjusted_fitness = 0.0
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

    def reproduce(self, generation):
        baby_genome = None
        if uniform(0, 1) < PERCENT_NO_CROSSOVER:
            baby_genome = self._select_org_for_reproduction().genome
            baby_genome.mutate()
        else:
            parent1 = self._select_org_for_reproduction()
            parent2 = self._select_org_for_reproduction()

            if parent1.fitness > parent2.fitness:
                baby_genome = Genome.crossover(parent1.genome, parent2.genome)
            else:
                baby_genome = Genome.crossover(parent2.genome, parent1.genome)

            if parent1 is parent2 or uniform(0, 1) > MATE_ONLY_PROB:
                baby_genome.mutate()

        return Organism(generation, baby_genome)

    def _select_org_for_reproduction(self):
        orgs = len(self.organisms)
        favoured_ind = int(orgs - sqrt(orgs**2 - uniform(0, orgs**2)))
        return self.organisms[favoured_ind]

    def wipe_older_generations(self, generation):
        self.organisms = [org for org in self.organisms if org.generation < generation]