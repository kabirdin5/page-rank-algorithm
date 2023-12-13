import random
import sys
import os
import time
import argparse
from progress import Progress

def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    # Iterate through the file line by line
    graph = {}
    for line in args.datafile:
        # And split each line into two URLs
        try:
            node, target = line.split()
        except:
            print("Error")
            continue

        if node not in graph:
            graph[node] = []
        graph[node].append(target)

        if target not in graph:
            graph[target] = []

    return graph

def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    number_of_nodes = len(graph)
    number_of_edges = sum(len(edges) for edges in graph.values())
    print(f"Number of nodes: {number_of_nodes}")
    print(f"Number of edges: {number_of_edges}")

def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """

    hit_count = {node: 0 for node in graph}
    for x in range(args.repeats):
        current_node = random.choice(list(graph.keys()))
        current_node = random.choice(graph[current_node])
        hit_count[current_node] += 1

    ranking = {value: count / args.steps for value, count in hit_count.items()}

    return ranking


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """

    nodes = list(graph.keys())
    number_of_nodes = len(nodes)

    node_prob = {node: 1 / number_of_nodes
                 for node in nodes}

    for x in range(args.steps):
        next_prob = {node: 0
                     for node in nodes}

        for node in nodes:
            if len(graph[node]) > 0:
                p = node_prob[node] / len(graph[node])
            else:
                p = 0

            for target in graph[node]:
                next_prob[target] += p

        node_prob = next_prob

    return node_prob


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
