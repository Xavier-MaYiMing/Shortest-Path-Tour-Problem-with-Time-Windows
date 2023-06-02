#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 09:06
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA.py
# @Statement : The ripple-spreading algorithm for the shortest path tour problem with time windows (SPTPTW)
from numpy import inf, array


def find_neighbors(network):
    # find the neighbors of each node
    neighbor = []
    for i in network.keys():
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    # find the ripple-spreading speed
    v = inf
    for i in network.keys():
        for j in neighbor[i]:
            v = min(v, network[i][j][0])
    return v


def dominate(length1, time1, level1, length2, time2, level2):
    # judge whether ripple1 dominates ripple2
    arr1 = array([length1, time1, -level1])
    arr2 = array([length2, time2, -level2])
    return all(arr1 <= arr2) and any(arr1 != arr2)


def find_POR(incoming_ripples, omega_node, length_set, time_set, level_set):
    # find the Pareto-Optimal ripples
    new_ripples = []
    flag = [False for _ in range(len(incoming_ripples))]
    for i in range(len(incoming_ripples)):
        for j in range(len(incoming_ripples)):
            if i != j and not flag[j] and dominate(incoming_ripples[i]['length'], incoming_ripples[i]['time'], incoming_ripples[i]['level'], incoming_ripples[j]['length'], incoming_ripples[j]['time'], incoming_ripples[j]['level']):
                flag[j] = True
    for r in range(len(incoming_ripples) - 1, -1, -1):
        if flag[r]:
            incoming_ripples.pop(r)
            flag.pop(r)
    for i in range(len(incoming_ripples)):
        length = incoming_ripples[i]['length']
        time = incoming_ripples[i]['time']
        level = incoming_ripples[i]['level']
        for j in omega_node:
            if dominate(length_set[j], time_set[j], level_set[j], length, time, level):
                flag[i] = True
                break
        if not flag[i]:
            new_ripples.append(incoming_ripples[i])
    return new_ripples


def main(network, node_subset, time_window, serve_time):
    """
    The Ripple-Spreading Algorithm for the Shortest Path Problem main function
    :param network: {node1: {node2: [cost, time], ...}, ...}
    :param node_subset: node subset
    :param time_window: the time window associated with each served node
    :param serve_time: the serve time associated with each served node
    :return:
    """
    # Step 1. Initialization
    neighbor = find_neighbors(network)
    v = find_speed(network, neighbor)  # ripple-spreading speed
    nn = len(network)  # node number
    ns = len(node_subset)  # subset number
    nr = 0  # the number of ripples  - 1
    serve_node = []  # the node in the node subset
    for nodes in node_subset:
        serve_node.extend(nodes)
    source = node_subset[0][0]
    destination = node_subset[-1][0]
    node_subset.append([])
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    path_set = []  # path set
    length_set = []  # length set
    time_set = []  # time set
    level_set = []  # level set
    active_set = []  # the set containing all active ripples
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = []

    # Step 2. Initialize the first ripple
    epicenter_set.append(source)
    radius_set.append(0)
    path_set.append([source])
    length_set.append(0)
    time_set.append(0)
    level_set.append(1)
    active_set.append(nr)
    omega[source].append(nr)
    nr += 1

    # Step 3. The Ripple-Spreading Algorithm for the Shortest Path Problem main loop
    while active_set:

        # Step 3.1. Termination judgment
        flag = False
        for ripple in omega[destination]:
            if level_set[ripple] == ns:
                flag = False
                break
        if flag:
            break

        # Step 3.2. Active ripples spread out
        incoming_ripples = {}
        remove_ripples = []
        for ripple in active_set:
            flag_inactive = True
            radius_set[ripple] += v

            # Step 3.3. New incoming ripples
            epicenter = epicenter_set[ripple]
            radius = radius_set[ripple]
            path = path_set[ripple]
            length = length_set[ripple]
            time = time_set[ripple]
            level = level_set[ripple]
            for node in neighbor[epicenter]:
                temp_length = network[epicenter][node][0]
                if temp_length <= radius < temp_length + v:
                    new_path = path.copy()
                    new_path.append(node)
                    new_length = length + network[epicenter][node][0]
                    new_time = time + network[epicenter][node][1]
                    if node in incoming_ripples.keys():
                        incoming_ripples[node].append({
                            'path': new_path,
                            'radius': radius - temp_length,
                            'length': new_length,
                            'time': new_time,
                            'level': level,
                        })
                    else:
                        incoming_ripples[node] = [{
                            'path': new_path,
                            'radius': radius - temp_length,
                            'length': new_length,
                            'time': new_time,
                            'level': level,
                        }]
                    if node in node_subset[level] and new_time <= time_window[node][1]:
                        incoming_ripples[node].append({
                            'path': new_path,
                            'radius': radius - temp_length,
                            'length': new_length,
                            'time': max(new_time, time_window[node][0]) + serve_time[node],
                            'level': level + 1,
                        })

                # Step 3.4. Active -> inactive
                if radius < temp_length:
                    flag_inactive = False
            if flag_inactive:
                remove_ripples.append(ripple)
        for ripple in remove_ripples:
            active_set.remove(ripple)

        # Step 3.5. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripples = find_POR(incoming_ripples[node], omega[node], length_set, time_set, level_set)
            for ripple in new_ripples:
                epicenter_set.append(node)
                radius_set.append(ripple['radius'])
                path_set.append(ripple['path'])
                length_set.append(ripple['length'])
                time_set.append(ripple['time'])
                level_set.append(ripple['level'])
                if node != destination:
                    active_set.append(nr)
                omega[node].append(nr)
                nr += 1

    # Step 3.6. Sort the results
    best_ripple = -1
    min_length = inf
    for ripple in omega[destination]:
        if level_set[ripple] == ns and length_set[ripple] < min_length:
            best_ripple = ripple
            min_length = length_set[ripple]
    return {
        'cost': length_set[best_ripple],
        'time': time_set[best_ripple],
        'level': level_set[best_ripple],
        'path': path_set[best_ripple],
    }
