from random import sample, choice, uniform

from NEAT.config import DISABLE_PROB_IF_PARENT_DISABLED, EXCESS_WEIGHT, DISJOINT_WEIGHT, WEIGHT_DIFFERENCE_WEIGHT, \
    ADD_CONNECTION_MUTATION_ATTEMPTS, ADD_NODE_MUTATION_ATTEMPTS
from NEAT.node_gene import NodeGene
from NEAT.connection_gene import ConnectionGene

class Genome:
    def __init__(self):
        self.nodes = set()
        self.connections = dict()
        self.bias_node = NodeGene(NodeGene.Type.BIAS, 0)

    def _addNode(self, node):
        if node in self.nodes:
            raise Exception(f'Adding exisitng node {node} to genome')
        self.nodes.add(node)
    
    def _addConnection(self, connection):
        if connection.innovation in self.connections:
            raise Exception(f'Adding exsting connection')
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
        if self._isFullyConnected():
            print('Genome fully connected')
            return

        # Find 2 nodes that can have a valid connection and aren't already connected
        attempts = 1
        node_set = self.nodes.union({self.bias_node})
        node1, node2 = NodeGene.orientNodes(sample(node_set, 1)[0], sample(node_set, 1)[0])
        while node1.type == node2.type or node1.depth == node2.depth or ConnectionGene.getInnovation(node1, node2) in self.connections:
            attempts += 1
            if attempts > ADD_CONNECTION_MUTATION_ATTEMPTS:
                print('addConncetionMutation too many attempts')
                return
            node1, node2 = NodeGene.orientNodes(sample(node_set, 1)[0], sample(node_set, 1)[0])

        self._addConnection(ConnectionGene(node1, node2))

    def deleteConnectionMutation(self):
        if not self.connections:
            return

        connection = choice(list(self.connections.values()))
        del self.connections[connection.innovation]

        if connection.in_ != NodeGene.Type.HIDDEN and connection.out != NodeGene.Type.HIDDEN:
            return

        found_in = found_out = False
        for conn in self.connections.values():
            if connection.in_ == conn.in_ or connection.in_ == conn.out:
                found_in = True
            if connection.out == conn.in_ or connection.out == conn.out:
                found_out = True

        if connection.in_ == NodeGene.Type.HIDDEN and not found_in:
            self.nodes.remove(connection.in_)

        if connection.out == NodeGene.Type.HIDDEN and not found_out:
            self.nodes.remove(connection.out)

    def addNodeMutation(self):
        attempt = 1
        connection = choice(list(self.connections.values()))
        while not connection.enabled and connection.in_ == self.bias_node:
            attempt += 1
            if attempt > ADD_NODE_MUTATION_ATTEMPTS:
                print('addNodeMutation too many attempts')
                return
            connection = choice(list(self.connections.values()))

        connection.disable()

        if connection.in_.depth + 1 == connection.out.depth:
            # Adding new depth, increment larger depths to make space
            for node in self.nodes:
                if node.depth >= connection.out.depth:
                    node.depth += 1

        new_node = NodeGene(NodeGene.Type.HIDDEN, connection.in_.depth + 1)
        self._addNode(new_node)

        self._addConnection(ConnectionGene(connection.in_, new_node, 1.0))
        self._addConnection(ConnectionGene(new_node, connection.out, connection.weight))

    def deleteNodeMutation(self):
        first_non_io_node_ind = 0
        nodes = list(self.nodes)
        for node in nodes:
            if node.type == NodeGene.Type.HIDDEN:
                break
            first_non_io_node_ind += 1

        if first_non_io_node_ind >= len(nodes) - 1:
            return

        node = choice(nodes[first_non_io_node_ind:])
        assert(node.type_ == NodeGene.Type.HIDDEN)

        self.nodes.remove(node)

        self.connections = {
            innov: conn for innov, conn in self.connections.items() if
            conn.in_ != node or conn.out != node
        }

    def toggleEnableMutation(self):
        connection = choice(self.connections.values())
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
        for connection in self.connections.values():
            if not connection.enabled:
                connection.enable()
                break

    def weightsMutation(self):
        for connection in self.connections.values():
            if not connection.frozen:
                connection.mutateWeight()

    # Assunes genome1 is fitter than genome 2
    @classmethod
    def crossover(cls, genome1, genome2):
        child = cls()
        for innovation, connection in genome1.connections.items():
            disable_prob = 0.0
            weight = None
            if innovation in genome2.connections: # matching case
                if not connection.enabled or not genome2.connections[innovation].enabled:
                    disable_prob = DISABLE_PROB_IF_PARENT_DISABLED

                # TODO: Parameterizing this prob might improve performance
                if uniform(0, 1) < 0.5:
                    weight = connection.weight
                else:
                    weight = genome2.connections[innovation].weight
            else: # excess or disjoint case
                disable_prob = 0.0 if connection.enabled else 1.0
                weight = connection.weight

            try:
                child._addNode(connection.in_)
            except:
                pass
            try:
                child._addNode(connection.out)
            except:
                pass

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

        return DISJOINT_WEIGHT*disjoint_count + EXCESS_WEIGHT*excess_count + WEIGHT_DIFFERENCE_WEIGHT*weight_diff/matching_count