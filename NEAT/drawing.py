import matplotlib.pyplot as plt

from NEAT.network import Network

def draw_genome(genome, name):
    SIZE = (50, 50)
    Y_DIST = 10
    X_DIST = 10
    RAD = 3

    plt.cla()
    plt.ylim([0, SIZE[0]])
    plt.xlim([0, SIZE[1]])
    plt.axis('off')

    net = Network(genome.nodes, genome.bias_node, genome.connections)
    net.node_depths = [nodes for nodes in net.node_depths if nodes]
    depths = len(net.node_depths)

    x = (SIZE[0] - X_DIST*(depths - 1))/2

    node_locs = {}

    for nodes in net.node_depths:
        num_nodes = len(nodes)
        y = (SIZE[1] - Y_DIST*(num_nodes - 1))/2
        for node in nodes:
            node_locs[node] = (x, y)
            plt.annotate(
                str(node.id),
                (x, y),
                bbox={'boxstyle' : 'circle', 'color':'blue'}
            )
            y += Y_DIST
        x += X_DIST if num_nodes else 0

    for connection in genome.connections.values():
        n1, n2 = node_locs[connection.in_], node_locs[connection.out]
        plt.plot((n1[0], n2[0]), (n1[1], n2[1]), 'k-', lw=2, color='green' if connection.enabled else 'red')
        mid_point = ((n1[0] + n2[0])/2, (n1[1] + n2[1])/2)
        plt.text(mid_point[0] - 2, mid_point[1], str(round(connection.weight, 2)))

    plt.savefig(f'pics/{name}.png')

def history(genome):
    draw_genome(genome, f'{genome.id}')
    print(genome.nodes)
    if genome.parents:
        for i in range(len(genome.parents)):
            draw_genome(genome.parents[i], f'parent {i} of {genome.id} ({genome.parents[i].id})')
        input()
        for parent in genome.parents:
            history(parent)
