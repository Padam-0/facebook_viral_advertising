import numpy as np
import networkx as nx

def get_strength():
    return np.random.exponential(2)

F = nx.Graph()

# Create original network from facebook.txt
nx.set_node_attributes(F, 'value', {})
with open('facebook_combined.txt', 'r') as file:
    for line in file:
        if line[0] != '#':
            F.add_edge(int(line.strip().split(' ')[0]),
                       int(line.strip().split(' ')[1]),
                       strength=0)

a = []
# Add 'strength of connection' as weight to each edge
for node in F.nodes():
    nbrs = F.neighbors(node)
    for nbr in nbrs:
        nbr_nbrs = F.neighbors(nbr)
        a.append((len([i for i in nbrs if i in nbr_nbrs])) / len(nbrs))

print(max(a))
print(np.mean(a))
print(min(a))


        #F[node][nbr]['strength'] = get_strength()