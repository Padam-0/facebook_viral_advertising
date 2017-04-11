To do:

- Create say 100 F graphs and run the simulations (varying 
newsfeed_composition) on them to save time / increase accuracy of comparisons
- Fix hangs
- Fix graph imports
- Extended exercises

The original network facebook_combined.txt had 4,039 nodes and 88,234 edges.

For the purpose of this assignment, nodes that have 7 or less edges are 
ignored. This results in the removal of 654 nodes, resulting in 3385 nodes 
where a 'newsfeed' is able to be constructed. For those nodes ignored, their 
newsfeed takes the form of `n` connections to all of their neighbors in the 
original graph, and then `10 - n` random connections.

For nodes with 8 or more connections, each edge is given a random weight. 
This weight represents the strength of the relationship between the two 
edges, and acts as a proxy for 'probability that an article posted by one is 
seen by the other'.

In the first extended exercise, the weights in the directed graph do not have 
to be equal. This can be thought of as a 'love triangle' situation. 

The function used to generate weights is an exponential decay function, 
which embodies the fact that people in social networks generally have a few 
close friends who they interact with frequently, and a lot of 'unclose' 
friends. In the first example, the strength of the connection between a node 
A and B is independent of the strength of the connections between A and C, 
and B and C.

As a second extended exercise, the strength of existing connections is taken 
into consideration, allowing for more realistic representation of cliques.

Once weights have been assigned for each connection in the network, a new 
graph is constructed and analyzed. This graph begins as a subgraph of the 
original graphs, but also contains some edges which were not present in the 
original.

In this graph, each node has connections to 10 other nodes, made up of some 
combination of 'Strongly Connected' nodes from the original graph, 'Weakly 
Connected' nodes from the original graph, and random connections (that 
didn't exist in the original). These random connections act as an analogy 
for 'suggested' or 'sponsored' posts on Facebook or Twitter.

This new graph is a representation of posts visible on the newsfeed, where 
that newsfeed contains only 10 items. The question to answered is:

"What combination of Strong Connections, Weak Connections and Random 
connections results in fastest possible transmission of data to all nodes."

To answer this question, a number of possible newsfeeds will be tested using 
a simulation, and summary statistics recorded and compared. The simulation 
relies on a number of assumptions:

- Newsfeed composition is fixed throughout the simulation;
- A node may either post or repost an item;
- If an item appears on the newsfeed for a certain node for the first time, 
that node reposts it immediately;
- If two new items appear for the first time together on the newsfeed, only 
the first is reposted;
- Items are posted on the newsfeed descending order of strength of 
connection, with random connections given strength 0;
- Each node checks their newsfeed once per day, all at the same time;
- As such, reposted items appear on newsfeeds of nodes the day after they're 
posted;
- A nodes most recent post appears on newsfeeds that follow it until a it 
posts something new; and
- If a node has not posted or reposted an item yet, nodes that follow it see
 nothing.

Extended exercise 3 relaxes the first constraint, and produces a new 
newsfeed (albeit one constructed with the same composition) for each day of 
the simulation.

Extended exercise 4 relaxes the 5th assumption, and tests whether displaying
 items in an ascending or random order changes results.

The simulation then proceeds as such:

1. 20 random nodes in the network 'post' items on Day 0, so that these items
 are first seen by other nodes on the 1st day.
2. Nodes record which posts they have seen, and repost each item the first 
time they see it
3. The simulation ends when all nodes have seen all 20 posts.

The summary statistic is the number of 'Days' it takes for all nodes in the 
network to see all posts. This is analogous to the Diameter of the network, as 
it is essentially a measure for how long it takes for information to 
disseminate to all nodes.

As this simulation is highly probabilistic (somewhat random newsfeed 
composition and random starting nodes), each simulation is run 10,000 times 
with different seeds for the random number generators. The number of Days 
taken for all nodes to see all posts and the actual Diameter (using `networkx 
nx.diameter(G)`) are recorded and compared.
 
The final step is to decide the composition of the newsfeed. With three 
variables (Strong, Weak and Random connections), there are 120 possible 
newsfeed combinations. However, because Facebook would be a boring place if 
it was completely random posts, we will only consider cases where there are 
3 or fewer random posts. Likewise, people want to see information about 
their best friends, so only cases where 3 or fewer weak connections are 
considered.

This results in 16 cases that will be tested:
- 10 strong, 0 weak, 0 random
- 9 strong, 1 weak, 0 random
- 9 strong, 0 weak, 1 random
- 8 strong, 2 weak, 0 random
- 8 strong, 1 weak, 1 random
- 8 strong, 0 weak, 2 random
- 7 strong, 3 weak, 0 random
- 7 strong, 2 weak, 1 random
- 7 strong, 1 weak, 2 random
- 7 strong, 0 weak, 3 random
- 6 strong, 3 weak, 1 random
- 6 strong, 2 weak, 2 random
- 6 strong, 1 weak, 3 random
- 5 strong, 3 weak, 2 random
- 5 strong, 2 weak, 3 random
- 4 strong, 3 weak, 3 random

This forms the base case. There are 4 extended exercises for comparison as 
features of the simulation are manipulated.

For a given newsfeed composition:
- Generate 100 random graphs based on that composition
- For each graph:
- Run 100 simulations with 20 starting posts
- Return the average number of iterations required to tranverse the entire 
network and diameter