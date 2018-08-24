from random import sample, choice, uniform

from NEAT.config import DISABLE_PROB_IF_PARENT_DISABLED
from NEAT.node_gene import NodeGene
from NEAT.connection_gene import ConnectionGene

class Genome:
    def __init__(self):
        self.nodes = set()
        self.connections = dict()
        self.bias_node = NodeGene(NodeGene.Type.BIAS)

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

    def connectionMutation(self):
        if self._isFullyConnected():
            print('Genome fully connected')
            return

        # Find 2 nodes that can have a valid connection and aren't already connected
        node_set = self.nodes.union({self.bias_node})
        node1, node2 = NodeGene.orientNodes(sample(node_set, 1)[0], sample(node_set, 1)[0])
        while node1.type == node2.type or ConnectionGene.getInnovation(node1, node2) in self.connections:
            node1, node2 = NodeGene.orientNodes(sample(node_set, 1)[0], sample(node_set, 1)[0])

        self._addConnection(ConnectionGene(node1, node2))
    
    def nodeMutation(self):
        if not self.connections:
            self.connectionMutation()

        connection = choice(list(self.connections.values()))
        while connection.in_ == self.bias_node:
            connection = choice(list(self.connections.values()))

        connection.enabled = False

        new_node = NodeGene(NodeGene.Type.HIDDEN)
        self._addNode(new_node)

        self._addConnection(ConnectionGene(connection.in_, new_node, 1.0))
        self._addConnection(ConnectionGene(new_node, connection.out, connection.weight))

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