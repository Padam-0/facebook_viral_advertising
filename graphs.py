import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

F = nx.Graph()

# Create original network from facebook.txt
with open('facebook_combined.txt', 'r') as file:
    for line in file:
        if line[0] != '#':
            F.add_edge(int(line.strip().split(' ')[0]),
                       int(line.strip().split(' ')[1]),
                       strength=0)

probs = []
random_probs = []
max_degree = 0
for node in F.nodes():
    if F.degree(node) > max_degree:
        max_degree = F.degree(node)

for node in F.nodes():
    probs.append(F.degree(node) / max_degree * 0.7)

for node in F.nodes():
    random_probs.append(np.random.exponential(0.03))

y = sorted(probs)
y_1 = sorted(random_probs)
x = range(len(probs))
plt.scatter(x, y, c='red', s=0.2, edgecolor='red')
plt.scatter(x, y_1, c='blue', s=0.2, edgecolor='blue')
plt.show()



