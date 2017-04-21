import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import os
import ast
from operator import itemgetter
import seaborn as sns

def distribution_plot():
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

    sns.set_style("white")
    plt.rc('font', family='Raleway')

    plt.scatter(x, y, c='red', s=0.8, edgecolor='red')
    plt.scatter(x, y_1, c='blue', s=0.8, edgecolor='blue')

    plt.legend(labels=["Calculated Influence","Exponential Distribution"],
               bbox_to_anchor=(0.05, .9, 0., 0.), loc=3, mode="expand",
               borderaxespad=0., markerscale=6)

    sns.despine()
    plt.xlabel('Number of instances')
    plt.ylabel('Probability')
    plt.ylim([-0.05, 0.8])
    plt.yticks([i/10 for i in range(0, 9, 1)])
    plt.xlim([0, 4050])
    plt.xticks([0, 1000, 2000, 3000, 4000])
    plt.show()


def read_file(filename):
    data_dict = {10: {}, 12: {}, 14: {}, 16: {}, 18: {}, 20: {}, 22: {},
                 24: {}, 26: {}, 28: {}, 30: {}, 32: {}, 34: {}, 36: {},
                 38: {}, 40: {}}

    with open(filename, 'r') as file:
        for line in file:
            if line[0] != '#' and line[0] != '{' and line[0] != '}':
                test_no = int(line.strip()[:2])

                info = line.strip()[4:-1]
                data_dict[test_no] = ast.literal_eval(info)

    return data_dict


def num_influencers_plot(data):
    x = []
    clicks_y = []
    views_y = []
    clicks_per_view_y = []
    for key in range(10,42,2):
        x.append(key)
        clicks = data[key]['average_clicks'] - key
        views = data[key]['average_views'] - key
        clicks_per_view = clicks / views
        clicks_y.append(clicks)
        views_y.append(views)
        clicks_per_view_y.append(clicks_per_view)

    fig, ax1 = plt.subplots()
    ax1.plot(x, clicks_y, c='black')
    ax1.plot(x, views_y, c='blue')
    ax1.set_xlabel('Number of initial clicks')
    ax1.set_ylabel('Clicks (black) / Views (blue)', color='black')
    ax1.tick_params('y', colors='black')

    ax2 = ax1.twinx()
    ax2.plot(x, clicks_per_view_y, c='red')
    ax2.set_ylabel('Clicks per View', color='r')
    ax2.tick_params('y', colors='r')

    plt.show()


def composition_data(influencers, threshold=False):
    cpvs = []

    if influencers:
        n, m = 0, 28
    else:
        n, m = 28, len(os.listdir("./output_data"))

    for file in os.listdir("./output_data")[n:m]:
        filename = './output_data/' + file
        data = read_file(filename)
        best_cpv = 0
        best_k = 0
        for k, v in data.items():
            cpv = (v['average_clicks'] - k) / (v['average_views'] - k)

            if cpv > best_cpv:
                best_cpv = cpv
                best_k = k
                views = v['average_views'] - k
        if threshold:
            if views > 4000:
                cpvs.append([best_cpv, file, best_k, views])
        else:
            cpvs.append([best_cpv, file, best_k, views])

    return sorted(cpvs, key=itemgetter(0), reverse=True)


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


def degree_distribution_plot():
    G = nx.read_edgelist('./simulation_networks/pa_parsed_4039.edgelist')
    F = nx.Graph()

    # Create original network from facebook.txt
    with open('facebook_combined.txt', 'r') as file:
        for line in file:
            if line[0] != '#':
                F.add_edge(int(line.strip().split(' ')[0]),
                           int(line.strip().split(' ')[1]),
                           strength=0)

    g_x_vals = [n for n in degree_dist(G).keys()]
    g_y_vals = [n for n in degree_dist(G).values()]
    f_x_vals = [n for n in degree_dist(F).keys()]
    f_y_vals = [n for n in degree_dist(F).values()]

    sns.set_style("white")
    plt.rc('font', family='Raleway')

    plt.scatter(g_x_vals, g_y_vals, c='red', s=3, edgecolor='red')
    plt.scatter(f_x_vals, f_y_vals, c='blue', s=3, edgecolor='blue')

    plt.legend(labels=["Preferential Attachment Graph", "Facebook Graph"],
               bbox_to_anchor=(0.6, .9, 0., 0.), loc=3, mode="expand",
               borderaxespad=0., markerscale=2)

    sns.despine()
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes')
    plt.ylim([-5, 400])
    plt.yticks([i for i in range(0, 450, 50)])
    plt.xlim([0, 1100])
    #plt.xticks([0, 1000, 2000, 3000, 4000])
    plt.show()


def composition_plot(data):
    order = ['4_6', '5_5', '6_4', '7_3', '8_2', '9_1', '10_0',
             '8_12', '10_10', '12_8', '14_6', '16_4', '18_2', '20_0',
             '12_18', '15_15', '18_12', '21_9', '24_6', '27_3', '30_0',
             '16_24', '20_20', '24_16', '28_12', '32_8', '36_4', '40_0']
    values = []
    for o in order:
        for item in data:
            if o == item[1][12:-4]:
                values.append([item[1][12:-4], float(item[0]), int(item[3])])

    criteria = []
    for item in values:
        if item[2] > 4000:
            criteria.append(False)
        else:
            criteria.append(True)

    clicks = []
    for item in values:
        clicks.append(int(item[1] * item[2]))

    plot_labels = []
    for item in values:
        sw = item[0].split('_')
        plot_labels.extend([str(sw[0]) + ' strong / ' + str(sw[1]) + ' weak'])

    sns.set_style("white")
    plt.rc('font', family='Raleway')
    fig, ax1 = plt.subplots(figsize=(20,10))
    plt.subplots_adjust(bottom=0.15)

    fig.canvas.draw()
    plt.xticks([i for i in range(len(plot_labels))])
    labels = [item.get_text() for item in ax1.get_xticklabels()]
    for i in range(len(plot_labels)):
        labels[i] = plot_labels[i]
    ax1.set_xticklabels(labels, rotation=-45)

    x = [i for i in range(len(values))]
    y = [i[1] for i in values]

    ax2 = ax1.twinx()

    use_colors = {True: 'red', False: 'blue'}
    ax1.scatter(x, y, s=30, c=[use_colors[x] for x in criteria])
    ax1.scatter(x, [None for i in range(len(x))], c='red', s=30,
                edgecolor='black')
    ax1.plot(x, [None for i in range(len(x))], c='black')
    ax1.yaxis.tick_left()

    ax1.legend(labels=["Additional Clicks Generated",
                       "Clicks per View Above views threshold",
                       "Clicks per view Below views threshold"],
               bbox_to_anchor=(0.05, .9, 0., 0.), loc=3, mode="expand",
               borderaxespad=0., markerscale=1)

    ax2.plot(x, clicks, c='black')
    sns.despine()

    ax1.set_xlabel('Structure of Ad-Serve')
    ax1.set_ylabel('Clicks per View')
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Total Additional Clicks Generated')
    ax2.tick_params('y')
    ax2.yaxis.tick_right()
    plt.xlim([-1, len(values)+1])

    plt.show()


def large_composition_data(k, threshold):
    k10_files = os.listdir("./additional_output_data")[:28]
    k20_files = os.listdir("./additional_output_data")[28:56]
    k4_files = os.listdir("./additional_output_data")[56:]

    if k == 4:
        k_files = k4_files
        thres = 4000
    elif k == 10:
        k_files = k10_files
        thres = 9750
    else:
        k_files = k20_files
        thres = 19500

    cpvs = []

    for file in k_files:
        filename = './additional_output_data/' + file
        data = read_file(filename)
        best_cpv = 0
        best_k = 0
        for k, v in data.items():
            cpv = (v['average_clicks'] - k) / (v['average_views'] - k)

            if cpv > best_cpv:
                best_cpv = cpv
                best_k = k
                views = v['average_views'] - k
        if threshold:
            if views > thres:
                cpvs.append([best_cpv, file, best_k, views])
        else:
            cpvs.append([best_cpv, file, best_k, views])

    return sorted(cpvs, key=itemgetter(0), reverse=True)


def large_composition_plot():
    k4_data = large_composition_data(4, False)
    k10_data = large_composition_data(10, False)
    k20_data = large_composition_data(20, False)

    order = ['4_6', '5_5', '6_4', '7_3', '8_2', '9_1', '10_0',
             '8_12', '10_10', '12_8', '14_6', '16_4', '18_2', '20_0',
             '12_18', '15_15', '18_12', '21_9', '24_6', '27_3', '30_0',
             '16_24', '20_20', '24_16', '28_12', '32_8', '36_4', '40_0']

    k4_val = []
    k10_val = []
    k20_val = []

    for o in order:
        for item in k4_data:
            if o == item[1][15:-4]:
                k4_val.append([item[1][15:-4], float(item[0]), int(item[3])])

    for o in order:
        for item in k10_data:
            if o == item[1][16:-4]:
                k10_val.append([item[1][12:-4], float(item[0]), int(item[3])])

    for o in order:
        for item in k20_data:
            if o == item[1][16:-4]:
                k20_val.append([item[1][12:-4], float(item[0]), int(item[3])])

    k4_criteria = []
    k10_criteria = []
    k20_criteria = []
    for item in k4_val:
        if item[2] > 4000:
            k4_criteria.append(True)
        else:
            k4_criteria.append(False)


    for item in k10_val:
        if item[2] > 9750:
            k10_criteria.append(True)
        else:
            k10_criteria.append(False)

    for item in k20_val:
        if item[2] > 19500:
            k20_criteria.append(True)
        else:
            k20_criteria.append(False)

    plot_labels = []
    for item in k4_val:
        sw = item[0].split('_')
        plot_labels.extend([str(sw[0]) + ' strong / ' + str(sw[1]) + ' weak'])

    sns.set_style("white")
    plt.rc('font', family='Raleway')
    fig, ax1 = plt.subplots(figsize=(20, 10))
    plt.subplots_adjust(bottom=0.15)

    plt.xticks([i for i in range(len(plot_labels))])
    labels = [item.get_text() for item in ax1.get_xticklabels()]
    for i in range(len(plot_labels)):
        labels[i] = plot_labels[i]
    ax1.set_xticklabels(labels, rotation=-45)

    x = [i for i in range(len(k4_val))]
    k4_y = [i[1] for i in k4_val]
    k10_y = [i[1] for i in k10_val]
    k20_y = [i[1] for i in k20_val]

    red = (226/255, 160/255, 160/255, 0.8)
    blue = (163/255, 158/255, 229/255, 0.8)
    green = (206/255, 165/255, 93/255, 0.8)

    use_colors = {True: 'blue', False: 'red'}
    ax1.scatter(x, k4_y, s=30, c=[use_colors[x] for x in k4_criteria])
    ax1.plot(x, k4_y, c=red)

    ax1.scatter(x, k10_y, s=30, c=[use_colors[x] for x in k4_criteria])
    ax1.plot(x, k10_y, c=blue)

    ax1.scatter(x, k20_y, s=30, c=[use_colors[x] for x in k4_criteria])
    ax1.plot(x, k20_y, c=green)

    ax1.scatter(x, [None for i in range(len(x))], c='blue', edgecolor='black')

    ax1.legend(labels=["4,039 node preferential attachment graph",
                       "10,000 node preferential attachment graph",
                       "20,000 node preferential attachment graph",
                       "Clicks per View Above views threshold",
                       "Clicks per view Below views threshold"],
               bbox_to_anchor=(0.65, .8, 0., 0.), loc=3, mode="expand",
               borderaxespad=0., markerscale=1)

    sns.despine()
    #plt.ylim([0,0.1])
    ax1.set_xlabel('Structure of Ad-Serve')
    ax1.set_ylabel('Clicks per View')
    plt.xlim([-1, len(plot_labels) + 1])

    plt.show()


def main():
    #distribution_plot()
    #degree_distribution_plot()
    #data = read_file('./additional_output_data/influencers_4_6.txt')
    #num_influencers_plot(data)
    #sorted_data = composition_data(True, True)
    #composition_plot(sorted_data)
    large_composition_plot()

if __name__ == '__main__':
    main()
