import networkx as nx
import numpy as np
from tqdm import tqdm
from operator import itemgetter


def assign_probabilities(n):
    # Assigns random number from an exponential distribution with mean 0.03
    # to each node as a starting probability
    F = nx.read_edgelist('./simulation_networks/fb_parsed.edgelist')

    # Assign a random probability
    for node in F.nodes():
        F[node]['probability'] = np.random.exponential(0.03)

    filename = ''.join(['./simulation_networks/fb_parsed_', n, '.edgelist'])
    # Write the edgelist to file
    nx.write_edgelist(F, filename)


def create_parsed_graph():
    F = nx.Graph()

    # Create original network from facebook.txt
    with open('facebook_combined.txt', 'r') as file:
        for line in file:
            if line[0] != '#':
                F.add_edge(int(line.strip().split(' ')[0]),
                           int(line.strip().split(' ')[1]),
                           strength=0)

    strength_dict = {}

    # Add 'strength of connection' as weight to each edge
    for node in tqdm(F.nodes()):
        nbrs = F.neighbors(node)
        for nbr in nbrs:
            nbr_nbrs = F.neighbors(nbr)
            # Strength of connection is determined as ratio of shared neighbors
            strength_dict[(node, nbr)] = (len(
                [i for i in nbrs if i in nbr_nbrs])) / len(nbrs)

    # Assign edge attributes
    nx.set_edge_attributes(F, 'strength', strength_dict)
    filename = './simulation_networks/fb_parsed.edgelist'

    # Write the edgelist to file
    nx.write_edgelist(F, filename)


def read_graph(filename):
    # Read in the parsed Facebook graph (with probabilities and strengths) and
    # construct NetworkX Graph

    G = nx.Graph()

    with open(filename, 'r') as file:
        for line in file:
            node = int(line.split(' ')[0])
            # If the line has probability information:
            if line.split(' ')[1] == 'probability':
                probability = line.split(' ')[2].strip()
                # Add node attributes probability, seen, clicked, seen_last and
                # clicked_last
                G.add_node(node, {'probability': float(probability),
                                  'seen': False, 'clicked': False,
                                  'seen_last': False, 'clicked_last': False})
            else:
                continue

    with open(filename, 'r') as file:
        for line in file:
            node = int(line.split(' ')[0])
            # If the line doesn't have probability information:
            if line.split(' ')[1] != 'probability':
                s = line.split(' ')[3].strip()[:-2]
                # Add edge with strength attribute
                G.add_edge(node, int(line.split(' ')[1]),
                           strength=float(s))
            else:
                continue

    # Return the NetworkX graph
    return G


def increase_prob(strength, probability):
    probability += strength * 0.1

    return probability


def check_stop(G, iteration, clicked, clicked_prev):
    # Check stopping criteria
    seen = 0
    for node in G.nodes():
        if G.node[node]['seen'] is True:
            seen += 1

    # If total ad views is over 2000
    if seen >= 2000:
        return True, 'views upper limit'
    # If no ads were clicked in the last iteration
    elif clicked == clicked_prev:
        return True, 'no progress'
    # If over 100 iterations have been conducted
    elif iteration >= 100:
        return True, 'iteration upper limit'
    else:
        return False, None


def get_nbrs(G, node, strength, threshold):
    # Generate lists of strong, weak or random neighbors for a given node.
    # Strong/weak classification is based on some threshold of shared
    # neighbors.

    if strength == 'strong':
        # Find all neighbors who have edge strength over the threshold
        nbrs = [i for i in G.neighbors(node) if G[node][i][
            'strength'] > threshold]
        # Remove those who have already seen the ad
        return [i for i in nbrs if G.node[i]['seen'] is False]
    elif strength == 'weak':
        # Find all neighbors who have edge strength under the threshold
        nbrs = [i for i in G.neighbors(node) if G[node][i][
            'strength'] <= threshold]
        # Remove those who have already seen the ad
        return [i for i in nbrs if G.node[i]['seen'] is False]
    else:
        # Find all nodes that are not neighbors
        nbrs = [i for i in G.nodes() if i not in G.neighbors(node)]
        # Remove those who have already seen the ad
        return [i for i in nbrs if G.node[i]['seen'] is False]


def update_clicks(G):
    # Generate list of nodes to test based on whether they saw the ad in the
    # last iteration
    to_test = []
    for node in G.nodes():
        if G.node[node]['seen_last'] == True:
            to_test.append(node)

    # For each node, randomly check if their probability results in a click or
    # not
    for node in to_test:
        if np.random.random() < G.node[node]['probability']:
            G.node[node]['clicked'] = True
            G.node[node]['clicked_last'] = True


def random_graph_test(items, threshold, composition, filename):

    G = read_graph(filename)

    node_list = []
    for i in G.nodes(data=True):
        node_list.append([i[0], i[1]['probability']])

    # Pick `items` number of nodes with the highest probability
    generators = [i[0] for i in sorted(node_list, key=itemgetter(1),
                                       reverse=True)[:items]]

    # For each node in the generators, set node characteristics
    for node in generators:
        G.node[node]['seen'] = True
        G.node[node]['clicked'] = True
        G.node[node]['seen_last'] = True
        G.node[node]['clicked_last'] = True

    stop = False
    iteration = 0
    clicked_prev = items

    # While stopping condition is not met
    while not stop:
        # Create list of nodes where an ad was clicked in the previous
        # iteration
        latest_clicks = [i for i in G.nodes() if G.node[i][
            'clicked_last'] == True]

        # For all nodes, reset characteristics
        for node in G.nodes():
            G.node[node]['seen_last'] = False
            G.node[node]['clicked_last'] = False

        # For each node that clicked the ad in the previous iteration
        for node in latest_clicks:
            # For each neighbor of this node
            for nbr in G.neighbors(node):
                # Increase probability according to edge strength
                p = increase_prob(G[node][nbr]['strength'], G.node[nbr][
                    'probability'])

                G.node[nbr]['probablity'] = p

            # Create lists of strong, weak and random nodes for each node
            strong_nbrs = get_nbrs(G, node, 'strong', threshold)
            weak_nbrs = get_nbrs(G, node, 'weak', threshold)
            random_nbrs = get_nbrs(G, node, 'random', threshold)

            to_show = []
            leftovers = 0

            # Find 10 nodes to show the ads to based on Ad-Serve composition:
            if composition[0] < len(strong_nbrs):
                to_show.extend(np.random.choice(strong_nbrs,
                                size=composition[0], replace=False))
            else:
                to_show.extend(strong_nbrs)
                leftovers += composition[0] - len(strong_nbrs)

            if composition[1] < len(weak_nbrs):
                to_show.extend(np.random.choice(weak_nbrs,
                                size=composition[1],replace=False))
            else:
                to_show.extend(weak_nbrs)
                leftovers += composition[1] - len(weak_nbrs)
            if leftovers > 0:
                to_show.extend(np.random.choice(random_nbrs,
                                size=leftovers, replace=False))

            # Update node characteristics for nodes that are shown the ad
            for node in to_show:
                G.node[node]['seen_last'] = True
                G.node[node]['seen'] = True

        # Test each node to see if it clicked the ad or not based on
        # adjusted probabilities
        update_clicks(G)

        # Generate summary statistics
        clicked_list = []
        seen_list = []
        for node in G.nodes():
            if G.node[node]['clicked'] == True:
                clicked_list.append(node)
            if G.node[node]['seen'] == True:
                seen_list.append(node)

        clicked = len(clicked_list)
        # Check stopping condition
        stop, condition = check_stop(G, iteration, clicked, clicked_prev)
        clicked_prev = clicked
        iteration += 1

    # Return output statistics
    return iteration, clicked, len(seen_list), condition


def base_case():
    F = nx.Graph()

    # Create original network from facebook.txt
    nx.set_node_attributes(F, 'probability', {})
    with open('facebook_combined.txt', 'r') as file:
        for line in file:
            if line[0] != '#':
                F.add_edge(int(line.strip().split(' ')[0]),
                           int(line.strip().split(' ')[1]),
                           strength=0)

    click_list = []
    for i in tqdm(range(1000)):
        clicks = 0
        for node in F.nodes():
            # Fix this line if gunna do anything with it
            # F.node[node]['probability'] = get_strength()
            if F.node[node]['probability'] > np.random.random():
                clicks += 1
        click_list.append(clicks)

    print(np.mean(click_list))
    print(np.std(click_list))


def simulation(composition, threshold, items, n_graphs):
    # List of possible newsfeed item breakdowns (strong, weak, random) to be
    # tested

    iterations = []
    clicks = []
    views = []
    conditions = []

    for graph in tqdm(range(n_graphs)):
        filename = ''.join(['./simulation_networks/fb_parsed_', str(graph),
                            '.edgelist'])

        iteration, clicked, seen, condition = \
            random_graph_test(items, threshold, composition, filename)
        iterations.append(iteration)
        clicks.append(clicked)
        views.append(seen)
        conditions.append(condition)

    condition_dict = {'views upper limit': 0,
                      'no progress': 0,
                      'iteration upper limit': 0
                      }

    for condition in conditions:
        condition_dict[condition] += 1

    output_data = {
        'average_iterations': np.mean(iterations),
        'average_clicks': np.mean(clicks),
        'average_views': np.mean(views),
        'stopping_conditions': condition_dict
    }

    return output_data


def write_header_information(composition, filename):
    # Write file header information
    with open(filename, 'w') as file:
        file.write('# Output data for newsfeed composition:\n')
        file.write('# Strong connections: ' + str(composition[0]) + '\n')
        file.write('# Weak connections: ' + str(composition[1]) + '\n')
        file.write('{\n')


def write_output_data(filename, items, data, final_line):
    with open(filename, 'a') as file:
        if final_line is False:
            file.write('\t' + str(items) + ': ' + str(data) + ',\n')
        else:
            file.write('\t' + str(items) + ': ' + str(data) + '\n')


def write_footer_information(filename):
    with open(filename, 'a') as file:
        file.write('}')


def main():
    np.random.seed(123)

    number_of_graphs = 20
    strong_weak_threshold = 0.5

    """
    create_parsed_graph()


    for graph in tqdm(range(number_of_graphs)):
        assign_probabilities(str(graph))
    """

    possible_compositions = [
        [20, 0],
        [18, 2],
        [16, 4],
        [14, 6],
        [12, 8]]

    for ad_serve in possible_compositions[:3]:
        print("Current composition:", str(ad_serve))
        filename = './output_data/output_data_' + \
                   str(ad_serve[0]) + '_' + \
                   str(ad_serve[1]) + '.txt'
        write_header_information(ad_serve, filename)

        for items in range(20, 42, 2):
            print("Current number of starting items:", str(items))
            data = simulation(ad_serve, strong_weak_threshold, items,
                              number_of_graphs)
            if items != 2:
                write_output_data(filename, items, data, False)
            else:
                write_output_data(filename, items, data, True)
        write_footer_information(filename)


if __name__ == '__main__':
    main()
