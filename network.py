# create original network from facebook.txt

import networkx as nx
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from operator import itemgetter


def get_strength():
    return np.random.exponential(2)

def check_all_seen(G, items):
    # For each node in the network
    for node in G.nodes():
        # If it has not seen every post
        if node['seen'] != {k + 1:True for k in range(items)}:
            # return false and exit loop
            return False
        # If it has seen every post, move onto next node
        continue
    # If all nodes have seen all posts, return true
    return True

def find_next_post(G, newsfeed, previously_posted):
    # Go down newsfeed
    # If seen before, don't post
    # Post first non-seen item
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
        # Post the last posted item
        return previously_posted[-1]




"""
y_t = []
for j in tqdm(range(1000)):
    y = []
    for i in range(1000):
        y.append(np.random.exponential(2))
    y_t.append(len([k for k in y if k > 2]))

print(sum(y_t)/1000)
"""

F = nx.Graph()
nx.set_node_attributes(F, 'value', {})
with open('facebook_combined.txt', 'r') as file:
    for line in file:
        if line[0] != '#':
            F.add_edge(int(line.strip().split(' ')[0]),
                       int(line.strip().split(' ')[1]),
                       strength=0)

# Start simulation
n = 1
items = 20
newsfeed_composition = [1,5,4]

# Find list of nodes to exclude
list_of_excluded_nodes = []
for i in F.nodes():
    if len(F.neighbors(i)) <= 7:
        list_of_excluded_nodes.append(i)

# Add 'strength of connection' as weight to each edge
for i in F.nodes():
    for k in F.neighbors(i):
        F[i][k]['strength'] = get_strength()

seen_dict = {k + 1:False for k in range(items)}
#seen_dict = [False for k in range(items)]

for i in tqdm(range(n)):
    # Create empty graph

    G = nx.Graph()
    #nx.set_node_attributes(G, 'newsfeed', 0)
    #nx.set_node_attributes(G, 'seen', 0)
    nx.set_node_attributes(G, 'current_post', 0)
    nx.set_node_attributes(G, 'previously_posted', [])

    """
    # Create newsfeed for each node in F
    for node in tqdm(F.nodes()):
        w_edges = []
        # Get edge strength for each edge between the current node and its
        # neighbors
        for j in F.neighbors(node):
            w_edges.append([j, F.get_edge_data(node, j)['strength']])

        # Filter w_edges for the strongest 1/3rd of edges
        strong_nodes = [i for i in w_edges if i[1] > 1.4]
        # Sort strong nodes descending for strength
        strong_nodes = sorted(strong_nodes, key=itemgetter(1), reverse=True)
        # FIlter w_edges for remaining 2/3rd of edges
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
        newsfeed_comp = []

        # If there aren't enough strong nodes to fill the quota
        if len(strong_nodes) < newsfeed_composition[0]:
            newsfeed.extend([i[0] for i in strong_nodes])
            newsfeed_comp.extend(['strong' for i in strong_nodes])
        else:
            # Add a random selection of strong nodes, weighted according to
            # strength
            newsfeed.extend(np.random.choice([i[0] for i in strong_nodes],
                                             size=newsfeed_composition[0],
                                             replace=False, p=strong_proba))
            newsfeed_comp.extend(['strong' for i in range(newsfeed_composition[
                                                            0])])

        # If there aren't enough weak nodes to fill the quota
        if len(weak_nodes) < newsfeed_composition[1]:
            # Add all available weak nodes
            newsfeed.extend([i[0] for i in weak_nodes])
            newsfeed_comp.extend(['weak' for i in weak_nodes])
        else:
            # Add a random selection of weak nodes, weighted according to
            # strength
            newsfeed.extend(np.random.choice([i[0] for i in weak_nodes],
                            size=newsfeed_composition[1],
                            replace=False, p=weak_proba))
            newsfeed_comp.extend(['weak' for i in range(newsfeed_composition[
                1])])

        # For remaining spots in the newsfeed, populate with random
        for j in range(10 - len(newsfeed)):
            newsfeed.append(np.random.choice(random_nodes))
            newsfeed_comp.append('random')

        # Test newsfeed composition. Remove for production
        # print(newsfeed_comp)

        # Add the newsfeed edges to the new graph
        for j in newsfeed:
            G.add_edge(node, j)
        G[node]['newsfeed'] = newsfeed
        G[node]['seen'] = seen_dict

    nx.write_edgelist(G, "test.edgelist")
    """

    # Use this to avoid generating the graph during testing. Remove for
    # production

    with open('test.edgelist', 'r') as file:
        for line in file:
            node = int(line.split(' ')[0])
            if line.split(' ')[1] == 'newsfeed':
                newsfeed = [int(i) for i in ''.join(line.split(
                    ' ')[2:])[1:-2].split(',')]
                G.add_node(node, {'newsfeed': newsfeed, 'seen':
                    {k + 1:False for k in range(items)}, 'current_post': 0,
                                  'previously_posted': []})
            else:
                continue

    with open('test.edgelist', 'r') as file:
        for line in file:
            node = int(line.split(' ')[0])
            if line.split(' ')[1] == 'newsfeed':
                continue
            elif line.split(' ')[1] == 'seen':
                continue
            else:
                G.add_edge(node, int(line.split(' ')[1]))

    # Generate 20 random posts at nodes
    generators = np.random.choice(G.nodes(), size=items, replace=False)

    for post, node in enumerate(generators):
        G.node[node]['seen'][post + 1] = True
        G.node[node]['current_post'] = post + 1
        G.node[node]['previously_posted'] = [post + 1]

    all_seen_all = False
    while not all_seen_all:

        # For every node
        for node in G.nodes():
            # Check posts it can see:
            newsfeed = G.node[node]['newsfeed']
            for post in newsfeed:
                if G.node[post]['current_post'] == 0:
                    continue
                else:
                    G.node[node]['seen'][G.node[post]['current_post']] = True

            G.node[node]['current_post'] = find_next_post(G, newsfeed,
                                                G.node[node]['previously_posted'])

            G.node[node]['previously_posted'].append(G.node[node]['current_post'])







        # Update




        # Check stopping criteria
        #all_seen_all = check_all_seen(G, items)
        all_seen_all = True
