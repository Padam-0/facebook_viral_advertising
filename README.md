## README.md

This repo contains 2 files:
- network.py
- graphs.py

network.py is used for generating networks and running simulations. graphs
.py is availble for generating output graphs.

The aim, output and discussion of results of the simulations is contained in
 submission.pdf.  

#### Code Usage

##### network.py

Can be run from the command line by calling python network.py with no 
additional arguments. Main parameters that are able to be changed in the 
file are:
- Whether to run the base case or graph simulation;
- Whether to use the influencers model of probability assignment;
- If not using the influencers model, how many random probability 
distributions to test;
- Whether to use the Facebook graph or a randomly generated graph 
(preferential attachment);
- If using the randomly generated graph, the name of that graph (should take
 the form './simulation_networks/pa_parsed_n.edgelist' where n is the number
  of nodes). This will set the number of nodes;
- If using the randomly generated graph, the number of edges to connect to 
each new node;
- Strong / weak connection threshold;
- Number and range of starting seeds to test; and
- Whether to create new graphs, or use existing.
 
All of these options can be called set in main().


##### graphs.py

