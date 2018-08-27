from operator import attrgetter

from NEAT.network import Network
from NEAT.species import Organism, Species


class Population:
    def __init__(self, seed_genomes):
        self.generation = 0
        self.max_fitness = 0
        self.organisms = []
        for i, genome in enumerate(seed_genomes):
            net = Network(genome.nodes, genome.bias, genome.connections)
            self.organisms.append(
                Organism(i, 1, genome, net)
            )

        self.species = []
        self.speciate(self.organisms)

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
        self.generation += 1

        #for sp in self.species: sp.compute_max_fitness()
        #self.species.sort(key=attrgetter('max_fitness'), reverse=True)



