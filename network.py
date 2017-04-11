import networkx as nx
import numpy as np
from tqdm import tqdm
from operator import itemgetter

def get_strength():
    return np.random.exponential(2)


def check_all_seen(G, items):
    complete = 0
    # For each node in the network
    for node in G.nodes():
        # If it has not seen every post
        if G.node[node]['seen'] != {k + 1:True for k in range(items)}:
            # return false and exit loop
            return False, round(complete/len(G.nodes()),0)
        # If it has seen every post, move onto next node
        complete += 1
        continue
    # If all nodes have seen all posts, return true
    return True, 100


def find_next_post(G, newsfeed, previously_posted):
    # For each post in the newsfeed
    for post in newsfeed:
        # If its post number is 0, skip it
        if G.node[post]['current_post'] == 0:
            continue

        # If its post number isn't 0, and it hasn't already been posted
        if G.node[post]['current_post'] not in previously_posted:
            # Repost that item
            return G.node[post]['current_post']

    # If nothing has been posted
    if len(previously_posted) == 0:
        # Continue to post nothing
        return 0
    # Otherwise
    else:
        # Post a random item that has previously been posted
        return np.random.choice(previously_posted)


def create_graphs(n_graphs, newsfeed_composition):
    F = nx.Graph()

    # Create original network from facebook.txt
    nx.set_node_attributes(F, 'value', {})
    with open('facebook_combined.txt', 'r') as file:
        for line in file:
            if line[0] != '#':
                F.add_edge(int(line.strip().split(' ')[0]),
                           int(line.strip().split(' ')[1]),
                           strength=0)

    # Add 'strength of connection' as weight to each edge
    for i in F.nodes():
        for k in F.neighbors(i):
            F[i][k]['strength'] = get_strength()

    for z in range(n_graphs):
        # Create empty graph
        G = nx.Graph()

        # Create newsfeed for each node in F
        for node in F.nodes():
            w_edges = []
            # Get edge strength for each edge between the current node and its
            # neighbors
            for j in F.neighbors(node):
                w_edges.append([j, F.get_edge_data(node, j)['strength']])

            # Filter w_edges for the strongest 1/3rd of edges
            strong_nodes = [i for i in w_edges if i[1] > 1.4]
            # Sort strong nodes descending for strength
            strong_nodes = sorted(strong_nodes, key=itemgetter(1), reverse=True)
            # Filter w_edges for remaining 2/3rd of edges
            weak_nodes = [i for i in w_edges if i[1] <= 1.4]
            # Sort weak nodes descending for strength
            weak_nodes = sorted(weak_nodes, key=itemgetter(1), reverse=True)
            # Set all other non-neighbor nodes as random
            random_nodes = [i for i in F.nodes() if i not in F.neighbors(node)]

            # Calculate probabilities for each strong and weak node based on
            # relative strength
            strong_tot = sum([i[1] for i in strong_nodes])
            weak_tot = sum([i[1] for i in weak_nodes])

            strong_proba = []
            for j in strong_nodes:
                strong_proba.append(j[1]/strong_tot)
            weak_proba = []
            for j in weak_nodes:
                weak_proba.append(j[1] / weak_tot)

            # Construct news feed
            newsfeed = []

            # If there aren't enough strong nodes to fill the quota
            if len(strong_nodes) < newsfeed_composition[0]:
                newsfeed.extend([i[0] for i in strong_nodes])
            else:
                # Add a random selection of strong nodes, weighted according to
                # strength
                newsfeed.extend(np.random.choice([i[0] for i in strong_nodes],
                                                 size=newsfeed_composition[0],
                                                 replace=False, p=strong_proba))

            # If there aren't enough weak nodes to fill the quota
            if len(weak_nodes) == 0:
                pass
            elif len(weak_nodes) < newsfeed_composition[1]:
                # Add all available weak nodes
                newsfeed.extend([i[0] for i in weak_nodes])
            else:
                # Add a random selection of weak nodes, weighted according to
                # strength
                newsfeed.extend(np.random.choice([i[0] for i in weak_nodes],
                                size=newsfeed_composition[1],
                                replace=False, p=weak_proba))

            # For remaining spots in the newsfeed, populate with random
            for j in range(sum(newsfeed_composition) - len(newsfeed)):
                newsfeed.append(np.random.choice(random_nodes))

            # Add the newsfeed edges to the new graph
            for j in newsfeed:
                G.add_edge(node, j)
            G[node]['newsfeed'] = newsfeed
        filename = './simulation_networks/graph_' + str(z) + '.edgelist'
        nx.write_edgelist(G, filename)


def read_edge_list(z, items):
    filename = './simulation_networks/graph_' + str(z) + '.edgelist'

    G = nx.Graph()
    connected = False
    while connected != True:

        with open(filename, 'r') as file:
            for line in file:
                node = int(line.split(' ')[0])
                if line.split(' ')[1] == 'newsfeed':
                    newsfeed = [int(i) for i in ''.join(line.split(
                        ' ')[2:])[1:-2].split(',')]
                    G.add_node(node, {'newsfeed': newsfeed, 'seen':
                        {k + 1: False for k in range(items)},
                                      'current_post': 0,
                                      'previously_posted': []})
                else:
                    continue

        with open(filename, 'r') as file:
            for line in file:
                node = int(line.split(' ')[0])
                if line.split(' ')[1] == 'newsfeed':
                    continue
                else:
                    G.add_edge(node, int(line.split(' ')[1]))

        if nx.is_connected(G):
            connected = True
        else:
            continue

    return G


def random_graph_test(r, q, items):
    iterations = []
    # Use this to avoid generating the graph during testing. Remove for
    # production
    for z in range(r):
        G = read_edge_list(q, items)
        # Generate random posts at nodes
        generators = np.random.choice(G.nodes(), size=items, replace=False)

        for post, node in enumerate(generators):
            G.node[node]['seen'][post + 1] = True
            G.node[node]['current_post'] = post + 1
            G.node[node]['previously_posted'] = [post + 1]

        all_seen_all = False

        i = 0
        while not all_seen_all:

            # For every node
            for node in G.nodes():
                # Check each post that it can see on its newsfeed
                newsfeed = G.node[node]['newsfeed']
                for post in newsfeed:
                    # If that post number is 0, ignore it
                    if G.node[post]['current_post'] == 0:
                        continue
                    # Otherwise
                    else:
                        # Update the 'seen' dictionary to reflect that the post
                        # has been seen
                        G.node[node]['seen'][G.node[post]['current_post']] = True

                # When all posts have been scanned, find which one of them to
                # repost
                G.node[node]['current_post'] = find_next_post(G, newsfeed,
                                                    G.node[node]['previously_posted'])

                # Add the posted item to the 'previously_posted' list
                G.node[node]['previously_posted'].append(G.node[node]['current_post'])

            # Check stopping criteria
            all_seen_all, perc_complete = check_all_seen(G, items)
            i += 1
            if i > 1000:
                all_seen_all = True

        print("Iteration " + str(z + 1) + "/" + str(r) + " of loop " + str(q
                + 1) + " complete.")
        if i != 1001:
            print("  Iterations: ", i)
            iterations.append(i)
        else:
            print("Timed out. Max iterations reached.")


    ave_iterations = np.mean(iterations)
    try:
        diameter = nx.diameter(G)
        return ave_iterations, diameter
    except:
        return ave_iterations, 0


def main():
    possible_compositions = [
        [10, 0, 0],
        [9, 1, 0],
        [9, 0, 1],
        [8, 2, 0],
        [8, 1, 1],
        [8, 0, 2],
        [7, 3, 0],
        [7, 2, 1],
        [7, 1, 2],
        [7, 0, 3],
        [6, 3, 1],
        [6, 2, 2],
        [6, 1, 3],
        [5, 3, 2],
        [5, 2, 3],
        [4, 3, 3]]

    composition = 1
    n = 1
    r = 10
    items = 20

    create_graphs(n, possible_compositions[composition])
    iterations = []
    diameters = []

    for i in range(n):
        ave_iterations, diameter = random_graph_test(r, i, items)
        iterations.append(ave_iterations)
        diameters.append(diameter)
        print("Iteration " + str(i + 1) + "/" + str(n) + " complete.")
    print('' + str(n) + " iterations complete.\n")
    print('Newsfeed composition: ' + str(possible_compositions[composition]))
    ai = np.mean(iterations)
    ad = np.mean(diameters)
    print("Average iterations: " + ai)
    print("Average Diameter: " + ad)


if __name__ == '__main__':
    main()