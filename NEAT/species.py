from operator import attrgetter
from collections import namedtuple

from NEAT.genome import Genome
from NEAT.config import COMPTABILITY_THRESHOLD, SPECIES_PENALIZE_AGE, SPECIES_STAGNANT_PENALTY, SURVIVAL_THRESHOLD

Organism = namedtuple('Organism', ['id', 'generation', 'genome', 'network', 'fitness', 'adjusted_fitness', 'eliminate', 'champion'])
Organism.__new__.__defaults__ = (None, None, False, False)


class Species:
    def __init__(self, rep_org):
        self.organisms = [rep_org]
        self.max_fitness = None
        self.max_fitness_lifetime = None
        self.age = 1
        self.last_improved_age = 0

    def add(self, org):
        self.organisms.append(org)

    def compute_max_fitness(self):
        self.max_fitness = max(self.organisms, key=attrgetter('fitness')).fitness

    def compatible(self, organism):
        return Genome.compatibility(self.organisms[0].genome, organism.genome) < COMPTABILITY_THRESHOLD

    def compuate_adjusted_fitness(self):
        age_debt = (self.age - self.last_improved_age + 1 - SPECIES_PENALIZE_AGE)
        size = len(self.organisms)

        for org in self.organisms:
            org.adjusted_fitness = org.fitness

            if age_debt >= 0:
                org.adjusted_fitness *= SPECIES_STAGNANT_PENALTY

            if org.adjusted_fitness < 0:
                org.adjusted_fitness = 0.0001

            org.adjusted_fitness /= size


    def sort_and_label(self):
        self.organisms.sort(key=attrgetter('adjusted_fitness'), reverse=True)
        best_fitness = self.organisms[0].adjusted_fitness
        if best_fitness > self.max_fitness_lifetime:
            self.last_improved_age = self.age
            self.max_fitness_lifetime = best_fitness

        num_parents = int(SURVIVAL_THRESHOLD*(len(self.organisms) + 1))

        for org in self.organisms[num_parents:]:
            org.eliminate = True