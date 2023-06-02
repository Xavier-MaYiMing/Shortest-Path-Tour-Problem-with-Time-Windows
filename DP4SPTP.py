#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 21:48
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : DP4SPTP.py
# @Statement : The dynamic programming algorithm for the shortest path tour problem (SPTP)
# @Reference : Festa P, Guerriero F, Laganà D, et al. Solving the shortest path tour problem[J]. European Journal of Operational Research, 2013, 230(3): 464-474.
from numpy import inf
from copy import deepcopy


def find_neighbors(network):
    # find the neighbors of each node
    neighbor = {}
    for i in network.keys():
        neighbor[i] = list(network[i].keys())
    return neighbor


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


def dominate(obj1, obj2):
    # judge whether obj1 dominates obj2
    return (obj1[0] <= obj2[0] and obj1[1] > obj2[1]) or (obj1[0] < obj2[0] and obj1[1] >= obj2[1])


def domination(label1, label2):
    # label1 dominates label2, return 0; label2 dominates label1, return 1
    obj1 = [label1['cost'], label1['level']]
    obj2 = [label2['cost'], label2['level']]
    if dominate(obj1, obj2):
        return 0
    elif dominate(obj2, obj1):
        return 1


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


def main(network, node_subset, serve_time):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param node_subset: the disjoint subsets of nodes
    :param serve_time: the serve time associated with each served node
    :return:
    """
    # Step 1. Initialization
    neighbor = find_neighbors(network)
    nn = len(network)  # node number
    ns = len(node_subset)  # subset number
    delta = inf
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
        'level': 1,
        'path': [source],
        'serve node': [source],
    }
    label_set.append(first_label)
    label[source].append(first_label)

    # Step 4. The main loop
    while label_set:
        temp_label, label_set = extract1(label_set)
        temp_cost = temp_label['cost']
        temp_level = temp_label['level']
        temp_path = temp_label['path']
        temp_serve_node = temp_label['serve node']
        temp_node = temp_path[-1]
        if temp_cost < delta:
            if temp_node == destination and temp_level == ns:
                delta = temp_cost
                best_solution = temp_label
            else:
                for node in neighbor[temp_node]:
                    new_cost = temp_cost + network[temp_node][node]
                    new_path = temp_path.copy()
                    new_path.append(node)
                    new_label = {
                        'cost': new_cost,
                        'level': temp_level,
                        'path': new_path,
                        'serve node': temp_serve_node,
                    }
                    label_set, label = add_label(label_set, label, new_label, node)
                    if node in node_subset[temp_level]:
                        new_serve_node = temp_serve_node.copy()
                        new_serve_node.append(node)
                        new_label = {
                            'cost': new_cost + serve_time[node],
                            'level': temp_level + 1,
                            'path': new_path,
                            'serve node': new_serve_node,
                        }
                        label_set, label = add_label(label_set, label, new_label, node)

    return {'path': best_solution['path'], 'length': best_solution['cost'], 'serve node': best_solution['serve node']}
