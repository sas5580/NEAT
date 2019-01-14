from copy import copy

from NEAT.neat import random
from NEAT.config import DISABLE_PROB_IF_PARENT_DISABLED, EXCESS_WEIGHT, DISJOINT_WEIGHT, WEIGHT_DIFFERENCE_WEIGHT, \
    ADD_CONNECTION_MUTATION_ATTEMPTS, ADD_NODE_MUTATION_ATTEMPTS, MUTATE_ADD_LINK_PROB, MUTATE_ADD_NODE_PROB, MUTATE_DELETE_LINK_PROB, \
    MUTATE_DELETE_NODE_PROB, MUTATE_TOGGLE_ENABLE_PROB, MUTATE_WEIGHTS_PROB, MUTATE_RENABLE_PROB
from NEAT.node_gene import NodeGene
from NEAT.connection_gene import ConnectionGene
from NEAT.drawing import draw_genome, history


class Genome:
    INPUT_NODES = []
    OUTPUT_NODES = []
    BIAS_NODE = None
    ID = 0

    @classmethod
    def init_io_nodes(cls, n_input, n_ouput):
        cls.BIAS_NODE = NodeGene(NodeGene.Type.BIAS, 0)
        for _ in range(n_input):
            cls.INPUT_NODES.append(NodeGene(NodeGene.Type.INPUT, 0))
        for _ in range(n_ouput):
            cls.OUTPUT_NODES.append(NodeGene(NodeGene.Type.OUTPUT, 1))

    def __init__(self, parents=None):
        self.id = Genome.ID
        Genome.ID += 1
        self.nodes = set(Genome.INPUT_NODES + Genome.OUTPUT_NODES)
        self.connections = dict()
        self.bias_node = Genome.BIAS_NODE

        self.parents = parents

    def basic_init(self):
        for inode in Genome.INPUT_NODES:
            for onode in Genome.OUTPUT_NODES:
                self._addConnection(ConnectionGene(inode, onode))

    def _addNode(self, node):
        if node in self.nodes:
            raise Exception(f'Adding exisitng node {node} to genome')
        self.nodes.add(node)

    def _addConnection(self, connection):
        if connection.innovation in self.connections:
            raise Exception(f'Adding exsting connection')
        # TODO: Remove if not causing problems and slowing down
        if connection.in_ not in self.nodes.union({self.bias_node}) or connection.out not in self.nodes.union({self.bias_node}):
            raise Exception('Attempting to add connection to nodes not in genome')
        self.connections[connection.innovation] = connection

    def _isFullyConnected(self):
        inp = out = hidden = 0
        for node in self.nodes:
            if node.type == NodeGene.Type.INPUT:
                inp += 1
            elif node.type == NodeGene.Type.OUTPUT:
                out += 1
            else:
                hidden += 1
        inp += 1 # bias
        pos_connections = inp*hidden + inp*out + hidden*out + (hidden - 1)*(hidden)//2
        return len(self.connections) == pos_connections

    def addConnectionMutation(self):
        #print('Attempting addConnectionMutation')
        if self._isFullyConnected():
            #print('Genome fully connected')
            return

        # Find 2 nodes that can have a valid connection and aren't already connected
        attempts = 1
        node_set = self.nodes.union({self.bias_node})
        node1, node2 = NodeGene.orientNodes(random.sample(node_set, 1)[0], random.sample(node_set, 1)[0])
        while node1.type == node2.type or node1.depth == node2.depth or ConnectionGene.getInnovation(node1, node2) in self.connections:
            attempts += 1
            if attempts > ADD_CONNECTION_MUTATION_ATTEMPTS:
                #print('addConncetionMutation too many attempts')
                return
            node1, node2 = NodeGene.orientNodes(random.sample(node_set, 1)[0], random.sample(node_set, 1)[0])

        self._addConnection(ConnectionGene(node1, node2))

    def deleteConnectionMutation(self):
        #print('Attempting deleteConnectionMutation')
        if not self.connections:
            return

        connection = random.choice(list(self.connections.values()))
        del self.connections[connection.innovation]

        if connection.in_.type != NodeGene.Type.HIDDEN and connection.out.type != NodeGene.Type.HIDDEN:
            return

        found_in = found_out = False
        for conn in self.connections.values():
            if connection.in_ == conn.in_ or connection.in_ == conn.out:
                found_in = True
            if connection.out == conn.in_ or connection.out == conn.out:
                found_out = True

        if connection.in_.type == NodeGene.Type.HIDDEN and not found_in:
            self.nodes.remove(connection.in_)

        if connection.out.type == NodeGene.Type.HIDDEN and not found_out:
            self.nodes.remove(connection.out)

    def addNodeMutation(self):
        #print('Attempting addNodeMutation')
        # SHouldnt need this since we always do add connection before mutating..
        assert self.connections, 'no connections before add node mutation'

        attempt = 1
        connection = random.choice(list(self.connections.values()))
        while not connection.enabled and connection.in_ == self.bias_node:
            attempt += 1
            if attempt > ADD_NODE_MUTATION_ATTEMPTS:
                #print('addNodeMutation too many attempts')
                return
            connection = random.choice(list(self.connections.values()))

        connection.disable()

        if connection.in_.depth + 1 == connection.out.depth:
            # Adding new depth, increment larger depths to make space
            for node in NodeGene.NODE_MAP.values():
                if node.depth >= connection.out.depth:
                    node.depth += 1

        new_node = NodeGene(NodeGene.Type.HIDDEN, connection.in_.depth + 1)
        self._addNode(new_node)

        self._addConnection(ConnectionGene(connection.in_, new_node, 1.0))
        self._addConnection(ConnectionGene(new_node, connection.out, connection.weight))

    # FIXME: Broken
    def deleteNodeMutation(self):
        #print('Attempting deleteNodeMutation')
        first_non_io_node_ind = 0
        nodes = list(self.nodes)
        for node in nodes:
            if node.type == NodeGene.Type.HIDDEN:
                break
            first_non_io_node_ind += 1

        if first_non_io_node_ind >= len(nodes) - 1:
            return

        node = random.choice(nodes[first_non_io_node_ind:])
        assert(node.type == NodeGene.Type.HIDDEN)

        self.nodes.remove(node)

        self.connections = {
            innov: conn for innov, conn in self.connections.items() if conn.in_ != node and conn.out != node
        }

    def toggleEnableMutation(self):
        #print('Attempting toggleEnableMutation')
        # SHouldnt need this since we always do add connection before mutating..
        if not self.connections:
            self.addConnectionMutation()
            return

        connection = random.choice(list(self.connections.values()))
        if not connection.enabled:
            connection.enable()
        else:
            # make sure another connection exists from in node
            found = False
            for gene in self.connections.values():
                if gene.in_ == connection.in_:
                    found = True
                    break
            if found:
                connection.disable()

    def renenableMutation(self):
        #print('Attempting renenableMutation')
        for connection in self.connections.values():
            if not connection.enabled:
                connection.enable()
                break

    def weightsMutation(self):
        #print('Attempting weightsMutation')
        for connection in self.connections.values():
            connection.mutateWeight()

    def _mutate_one(self):
        if not self.connections:
            self.addConnectionMutation()
        if random.uniform(0, 1) < MUTATE_WEIGHTS_PROB:
            self.weightsMutation()
        elif random.uniform(0, 1) < MUTATE_ADD_LINK_PROB:
            self.addConnectionMutation()
        elif random.uniform(0, 1) < MUTATE_ADD_NODE_PROB:
            self.addNodeMutation()
        elif random.uniform(0, 1) < MUTATE_DELETE_LINK_PROB:
            self.deleteConnectionMutation()
        elif random.uniform(0, 1) < MUTATE_TOGGLE_ENABLE_PROB:
            self.toggleEnableMutation()
        elif random.uniform(0, 1) < MUTATE_RENABLE_PROB:
            self.renenableMutation()

    def _mutate_any(self):
        if not self.connections:
            self.addConnectionMutation()
        if random.uniform(0, 1) < MUTATE_WEIGHTS_PROB:
            self.weightsMutation()
        if random.uniform(0, 1) < MUTATE_ADD_LINK_PROB:
            self.addConnectionMutation()
        if random.uniform(0, 1) < MUTATE_ADD_NODE_PROB:
            self.addNodeMutation()
        if random.uniform(0, 1) < MUTATE_DELETE_LINK_PROB:
            self.deleteConnectionMutation()
        if random.uniform(0, 1) < MUTATE_TOGGLE_ENABLE_PROB:
            self.toggleEnableMutation()
        if random.uniform(0, 1) < MUTATE_RENABLE_PROB:
            self.renenableMutation()

    def mutate(self):
        #print('MUTATING')
        self._mutate_one()
        self.verify()

    def clone(self):
        cl = Genome([self])
        cl.nodes = copy(self.nodes)
        for connection in self.connections.values():
            cl._addConnection(connection.clone())

        return cl

    # Assunes genome1 is fitter than genome2
    @classmethod
    def crossover(cls, genome1, genome2):
        child = cls([genome1, genome2])
        child.nodes = copy(genome1.nodes)

        for innovation, connection in genome1.connections.items():
            disable_prob = 0.0
            weight = None
            if innovation in genome2.connections: # matching case
                if not connection.enabled or not genome2.connections[innovation].enabled:
                    disable_prob = DISABLE_PROB_IF_PARENT_DISABLED

                # TODO: Parameterizing this might improve performance
                if random.uniform(0, 1) < 0.5:
                    weight = connection.weight
                else:
                    weight = genome2.connections[innovation].weight
            else: # excess or disjoint case
                disable_prob = 0.0 if connection.enabled else 1.0
                weight = connection.weight

            child._addConnection(ConnectionGene(
                connection.in_, connection.out, weight, disable_prob
            ))

        return child

    @staticmethod
    def compatibility(genome1, genome2):
        con_ind1 = con_ind2 = 0
        cons1, cons2 = list(genome1.connections.keys()), list(genome2.connections.keys())
        n1, n2 = len(genome1.connections), len(genome2.connections)

        disjoint_count = excess_count = matching_count = weight_diff = 0

        while con_ind1 < n1 or con_ind2 < n2:
            if con_ind1 >= n1:
                excess_count += 1
                con_ind2 += 1
            elif con_ind2 >= n2:
                excess_count += 1
                con_ind1 += 1
            else:
                ino1, ino2 = cons1[con_ind1], cons2[con_ind2]
                if ino1 == ino2:
                    matching_count += 1
                    weight_diff += abs(genome1.connections[ino1].weight - genome2.connections[ino2].weight)
                    con_ind1 += 1
                    con_ind2 += 1
                elif ino1 < ino2:
                    disjoint_count += 1
                    con_ind1 += 1
                elif ino1 > ino2:
                    disjoint_count += 1
                    con_ind2 += 1
        matching_count = matching_count or 1
        return DISJOINT_WEIGHT*disjoint_count + EXCESS_WEIGHT*excess_count + WEIGHT_DIFFERENCE_WEIGHT*weight_diff/matching_count

    def verify(self):
        try:
            for c in self.connections.values():
                assert c.in_ in self.nodes or c.in_ == self.bias_node, f'{c.in_} not in nodes'
                assert c.out in self.nodes or c.out == self.bias_node, f'{c.out} not in nodes'
                assert c.in_.depth < c.out.depth, f'in {c.in_} has depth {c.in_.depth}, out {c.out} has depth {c.out.depth}'
        except AssertionError as e:
            print(e)
            history(self)
            raise
