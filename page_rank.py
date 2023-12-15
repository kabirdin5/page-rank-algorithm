import random  # Imports random module
import sys  # Imports sys module
import os  # Imports os module
import time  # Imports time module
import argparse  # Imports argparse module
from progress import Progress  # Imports the Progress class from progress.py file


def load_graph(args):  # Defines the load_graph(args) function
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A graph dictionary mapling a URL (str) to a list of target URLs (str).
    """
    # Initialises an empty graph using a dictionary
    graph = {}
    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        try:
            node, target = line.split()
        # Prints if splitting the line between the node and target does not work
        except ValueError:
            print(f"Error found on line: {line}")
            continue

        # If the node is not found in the graph, it adds to an empty list of nodes
        if node not in graph:
            graph[node] = []
        # Adds the target to the list of targets linking to the nodes
        graph[node].append(target)
        # If the target is not found in the graph, it adds to an empty list of targets
        if target not in graph:
            graph[target] = []

    return graph  # Graph is returned containing the nodes and targets


def print_stats(graph):  # Defines the print_stats(graph) function
    """Print number of nodes and edges in the given graph"""
    # Creates a variable that contains the calculated number of nodes in the graph
    number_of_nodes = len(graph)
    # Creates a variable that contains the total number of edges in the graph, using the sum of out edges for each node
    number_of_edges = sum(len(edges) for edges in graph.values())
    # Prints the number of nodes and edges
    print(f"Number of nodes: {number_of_nodes}")
    print(f"Number of edges: {number_of_edges}")


def stochastic_page_rank(graph, args):  # Defines the stochastic_page_rank(graph, args) function
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A ranking variable that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_repeats end
    on each node of the given graph.
    """

    # Initialises a dictionary that stores the hit counts of each node
    hit_count = {node: 0 for node in graph}

    # Creates a variable that contains a randomly selected node
    current_node = random.choice(list(graph.keys()))

    # Completes random walks according to the specified number of repetitions
    for x in range(args.repeats):
        # If the current node has an outer edge,
        if graph[current_node]:
            # Creates a variable which randomly chooses one out edge of current node
            current_node = random.choice(graph[current_node])
        # If the current node does not have an outer edge,
        else:
            # Another node is randomly selected
            current_node = random.choice(list(graph.keys()))

        # Increments the hit count of the chosen node
        hit_count[current_node] += 1

    # Creates a variable that calculates the page ranking, based on the frequency of hitting the page
    ranking = {value: count / args.repeats for value, count in hit_count.items()}

    return ranking  # Returns the ranking variable





def distribution_page_rank(graph, args):  # Defines the distribution_page_rank(graph, args) function
    """
    Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """

    # Creates a variable that gets a list of all nodes in the graph
    nodes = list(graph.keys())
    # Creates a variable that gets the total number of nodes in the graph
    number_of_nodes = len(nodes)
    # Creates a dictionary that initialises a probability distribution of each node
    node_prob = {node: 1 / number_of_nodes
                 for node in nodes}

    # Completes random walks according to the specified number of steps
    for _ in range(args.steps):
        # Creates a dictionary that initialises the next iteration of probability distribution
        next_prob = {node: 0
                     for node in nodes}

        # For each and every node in the graph
        for node in nodes:
            # If the length of the specific node is more than 0,
            if len(graph[node]) > 0:
                # A variable is created that calculates the probability to move from the current node to its outer edges
                p = node_prob[node] / len(graph[node])
            # If the length of the specified node is equal to 0
            else:
                # A variable is created that sets the probability to 0
                p = 0

            # For each target of every node in the graph,
            for target in graph[node]:
                # The probability distribution is updated for each target node
                next_prob[target] += p

        # The current probability distribution is updated for the next iteration
        node_prob = next_prob
    return node_prob  # The probability for each node is returned

""" Argument Parser """
# Creates a variable sets up the argument parser
parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
# Defines the positional argument of the datafile (school_web.txt)
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
# Defines the positional argument of the page rank method (stochastic or distribution)
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
# Defines the positional argument of the number of repetitions in the algorithm
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
# Defines the positional argument of the number of steps a walker takes
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
# Defines the positional argument of the number of results shown
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

# Checks if the python script is able to run as the main program,
if __name__ == '__main__':
    # Creates a variable that contains the parse arguments
    args = parser.parse_args()
    # Creates a variable to select the preferred algorithm based on the positional argument "method"
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    # Creates a variable that contains the specified datafile given from the load_graph(args) function
    graph = load_graph(args)

    # Runs the print_stats(graph function
    print_stats(graph)

    # Creates a variable that records the start time for calculating the execution time of the algorithm
    start = time.time()
    # Creates a variable that runs the selected page rank algorithm
    ranking = algorithm(graph, args)
    # Creates a variable that records the stop time for calculating the execution time of the algorithm
    stop = time.time()
    # Creates a variable that contains the total execution time of the algorithm
    time = stop - start

    # Displays the websites that are top ranked with also their page rank values
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100 * v:.2f}\t{k}' for k, v in top[:args.number]))

    # Displays the total time taken for the completion of the algorithm in 2 d.p
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")