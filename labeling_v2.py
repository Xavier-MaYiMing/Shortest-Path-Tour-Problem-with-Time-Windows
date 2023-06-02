#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 15:31
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling_v2.py
# @Statement : The labeling method for the shortest path tour problem with time windows (SPTPTW) with upper bound initialization strategy
# @Reference : Pugliese L D P, Ferone D, Festa P, et al. Shortest path tour problem with time windows[J]. European Journal of Operational Research, 2020, 282(1): 334-344.
import DP4SPTP as DP
from copy import deepcopy


def find_neighbors(network):
    # find the neighbors of each node
    neighbor = []
    for i in network.keys():
        neighbor.append(list(network[i].keys()))
    return neighbor


def dominate(obj1, obj2):
    # judge whether obj1 dominates obj2
    sum_less = 0
    for i in range(len(obj1)):
        if obj1[i] > obj2[i]:
            return False
        elif obj1[i] != obj2[i]:
            sum_less += 1
    return sum_less != 0


def domination(label1, label2):
    # label1 dominates label2, return 0; label2 dominates label1, return 1
    obj1 = [label1['cost'], label1['time'], -label1['level']]
    obj2 = [label2['cost'], label2['time'], -label2['level']]
    if dominate(obj1, obj2):
        return 0
    if dominate(obj2, obj1):
        return 1


def extract1(label_set):
    # Dijkstra-like (DR) rule
    label_set = sorted(label_set, key=lambda x: x['cost'])
    new_label = label_set.pop(0)
    return new_label, label_set


def extract2(label_set):
    # first-in first-out (FIFO) rule
    new_label = label_set.pop(0)
    return new_label, label_set


def extract3(label_set):
    # last-in first-out (LIFO) rule
    new_label = label_set.pop()
    return new_label, label_set


def add_label(label_set, label, new_label, node):
    # the procedure to add a new label
    flag = True
    remove_dominated = []
    for temp_label in label[node]:
        flag_domination = domination(new_label, temp_label)
        if flag_domination == 1:
            flag = False
            break
        elif flag_domination == 0:
            remove_dominated.append(temp_label)
    if flag:
        for item in remove_dominated:
            if item in label_set:
                label_set.remove(item)
            label[node].remove(item)
        label_set.append(new_label)
        label[node].append(new_label)
    return label_set, label


def main(network, node_subset, time_window, serve_time):
    """
    The main function
    :param network: {node1: {node2: [cost, time], ...}, ...}
    :param node_subset: node subset
    :param time_window: the time window associated with each served node
    :param serve_time: the serve time associated with each served node
    :return:
    """
    # Step 1. Initialization
    neighbor = find_neighbors(network)
    nn = len(network)  # node number
    ns = len(node_subset)  # subset number
    temp_network = deepcopy(network)
    temp_node_subset = deepcopy(node_subset)
    serve_node = []  # the node in the node subset
    for nodes in node_subset:
        serve_node.extend(nodes)
    best_solution = {}
    source = node_subset[0][0]
    destination = node_subset[-1][0]
    node_subset.append([])
    label_set = []  # L
    label = {}  # D
    for node in range(nn):
        label[node] = []

    # Step 2. Add the first label
    first_label = {
        'cost': 0,
        'time': 0,
        'level': 1,
        'path': [source],
    }
    label_set.append(first_label)
    label[source].append(first_label)

    # Step 3. Determine the upper bound
    for i in network.keys():
        for j in neighbor[i]:
            temp_network[i][j] = network[i][j][1]
    temp_result = DP.main(temp_network, temp_node_subset, serve_time)
    temp_path = temp_result['path']
    temp_serve_node = temp_result['serve node']
    time = 0
    delta = 0

    for i in range(len(temp_path) - 1):
        time += temp_network[temp_path[i]][temp_path[i + 1]]
        delta += network[temp_path[i]][temp_path[i + 1]][0]
        if temp_path[i + 1] in temp_serve_node:
            if time > time_window[temp_path[i + 1]][1]:
                return {}
            time += serve_time[temp_path[i + 1]]

    # Step 4. The main loop
    while label_set:
        temp_label, label_set = extract1(label_set)
        temp_cost = temp_label['cost']
        temp_time = temp_label['time']
        temp_level = temp_label['level']
        temp_path = temp_label['path']
        temp_node = temp_path[-1]
        if temp_cost <= delta:
            if temp_node == destination and temp_level == ns:
                delta = temp_cost
                best_solution = temp_label
            else:
                for node in neighbor[temp_node]:
                    new_cost = temp_cost + network[temp_node][node][0]
                    new_time = temp_time + network[temp_node][node][1]
                    new_path = temp_path.copy()
                    new_path.append(node)
                    new_label = {
                        'cost': new_cost,
                        'time': new_time,
                        'level': temp_level,
                        'path': new_path,
                    }
                    label_set, label = add_label(label_set, label, new_label, node)
                    if node in node_subset[temp_level] and new_time <= time_window[node][1]:
                        new_label = {
                            'cost': new_cost,
                            'time': max(new_time, time_window[node][0]) + serve_time[node],
                            'level': temp_level + 1,
                            'path': new_path,
                        }
                        label_set, label = add_label(label_set, label, new_label, node)

    return best_solution
