from operator import attrgetter

from NEAT.config import STAGNANT_SPECIES_AGE_DIFF
from NEAT.network import Network
from NEAT.species import Organism, Species


class Population:
    def __init__(self, seed_genomes):
        self.generation = 1
        self.max_fitness = 0
        self.organisms = []
        for i, genome in enumerate(seed_genomes):
            net = Network(genome.nodes, genome.bias, genome.connections)
            self.organisms.append(
                Organism(i, 1, genome, net)
            )

        self.species = []
        self.speciate(self.organisms)

    def calculate_fitness(self):
        pass

    def speciate(self, organisms):
        for org in organisms:
            specie = None
            for sp in self.species:
                if sp.compatible(org):
                    specie = sp
                    sp.add(org)
                    break

            if specie is None:
                specie = Species(org)
                self.species.append(specie)


    def next_generation(self):
        self.calculate_fitness()

        # Adjust fitness based on species size and stagnance
        # Kill off bottom of species (param for amount)
        # Calculate average fitnesses of each species
        # Kill stagnant species
        # Kill crappy species
        # give children to species based on how much they contribute to the entire sum of average fitnesses
        # If not enough children, create more from best species
        # Speciate based on old organsisms
        # delete old organisms from population and species
        population_size = len(self.organisms)
        average_fitness_sum = 0.0


        for sp in self.species:
            sp.new_gen()
            sp.compute_adjusted_fitness()
            sp.sort_and_cull()
            average_fitness_sum += sp.average_adjusted_fitness

        sp_index = len(self.species)
        ave_fit_sum_copy = average_fitness_sum
        while sp_index > 0:
            sp_index -= 1
            sp = self.species[sp_index]
            if sp.age - sp.last_improved_age >= STAGNANT_SPECIES_AGE_DIFF:
                average_fitness_sum -= sp.average_adjusted_fitness
                del self.species[sp_index]
            elif sp.average_adjusted_fitness/ave_fit_sum_copy*population_size < 1:
                average_fitness_sum -= sp.average_adjusted_fitness
                del self.species[sp_index]

        children = []
        for sp in self.species:

            num_children = 0

        self.generation += 1