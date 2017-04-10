# create original network from facebook.txt

import networkx as nx

def degree_dist(G):
    degree_dist = {}
    for i in G.nodes():
        degree_dist[i] = len(G.neighbors(i))

    dd_plot_data = {}
    for n, d in degree_dist.items():
        if d in dd_plot_data:
            dd_plot_data[d] += 1
        else:
            dd_plot_data[d] = 1

    return dd_plot_data

def get_strength():
    pass


F = nx.Graph()
with open('facebook_combined.txt', 'r') as file:
    for line in file:
        if line[0] != '#':
            F.add_edge(int(line.strip().split(' ')[0]),
                       int(line.strip().split(' ')[1]),
                       strength=0)
list_of_excluded_nodes = []

for i in F.nodes():
    if len(F.neighbors(i)) <= 7:
        list_of_excluded_nodes.append(i)

for i in F.nodes():
    if i in list_of_excluded_nodes:
        continue

    # Add 'strength of connection' as weight to each edge
    for j, k in enumerate(F.neighbors(i)):
        #print(j)
        pass
        #F[i][k]['strength'] = get_strength(j)


G = nx.Graph()
for node in F.nodes():
    # Create 'newsfeed'
    pass