To do:

- Create graph where probability is related to the degree of the node 
'influencers'
- Do simulations for 10s and 40s
- Generate graphs, writeup


Advertisers on Facebook want to reach the most number of people who are 
likely to click on their ad and buy their product. Facebook has ways to 
target ads to users based on likes and interests, but it is unclear if 
Facebook utilizes friendship information to optimize who is shown specific ads.

Based on the assumption that users are more likely to click on an ad that a
connection of theirs has already clicked on, can the user network be used 
to 'spread' the ad in a viral manner to achieve similar numbers of clicks, 
while showing the ad to fewer people?

Two metrics are important, total number of clicks, and clicks per view. To 
maximise total clicks, the ad should be shown to all users. If each user has
an existing probably of clicking on the ad (which is related to other 
factors), what is the expected number of clicks per view based on this 
strategy. This forms the base case for our analysis.

If a users underlying probability of clicking on an ad is influenced by 
connections that have clicked on the ad, then it may make more sense to 
disseminate the ad throughout the network slowly, in order to target users 
when their probability of clicking is higher than in the base case.

This method could optimize clicks per view, by only showing the ad to users 
when they are more likely to click on it.

`Due to cost constraints, if a user clicks on an ad, that ad is only shown 
to 10 of their connections`. These connections can be selected from one of 
three lists:
 - Strong connections of the user;
 - Weak connection of the user; or
 - Random user in the network.
 
This distribution of connections is hence referred to as Ad-Serve.

For this simulation, it is assumed that:
 - A user has a 10% greater chance of clicking on an ad that a strong 
 connection of theirs has clicked on over their base case probability;
 - A user has a 5% greater chance of clicking on an ad that a weak 
 connection of theirs has clicked on over their base case probability.

If 10 users are selected, how many from each list should be selected to 
maximize the number of overall clicks without showing the ad to too many users.

The original network facebook_combined.txt had 4,039 nodes and 88,234 edges.

All users were given an underlying probability of clicking on an ad based on
an exponential distribution, and the base case number of clicks calculated 
using a independent Bernoulli trial on each user.

In the base case, 80.538 users clicked on the ad (1000 trials, std=8.78)

In the simulation, users begin with the same base case probability of 
clicking on the ad, and the 20 users in the network with the highest 
underlying probabilty of clicking on the ad are deemed to have 
'clicked on' that ad. 

All users who have a relationship (connection) with those users have their 
underlying probability adjusted based on the strength of that connection.

In the each iteration, for each user who has clicked on the ad, the ad is 
shown to more 10 users who are 'linked' to each of that user based on the 
Ad-Serve composition.

That is, in the first iteration, 20 people see the ad. In the second, that 
number grows to (approximately) 200, and so on.

Each user who sees the ad has a probability of clicking on it (base case 
plus any probability increase due to their connections having clicked on the
ad)

The simulation ends after the 3000 users have 'seen' the ad, as this is the 
ad agency's cost constraint. At this stage, the number of clicks is 
recorded, and compared to the base case and other Ad-Serve compositions.



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
- Generate 32 random graphs based on that composition
- For each graph:
- Run 32 simulations with 20 starting posts
- Return the average number of iterations required to tranverse the entire 
network and diameter