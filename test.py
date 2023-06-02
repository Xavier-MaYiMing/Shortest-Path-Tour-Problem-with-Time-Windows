#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/30 20:55
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : test.py
# @Statement : Read the benchmarks of the shortest path tour problem with time windows (SPTPTW)
# @Reference : Pugliese L D P, Ferone D, Festa P, et al. Shortest path tour problem with time windows[J]. European Journal of Operational Research, 2020, 282(1): 334-344.
# @Website : https://bit.ly/2H1G8JK


def read_data(file_name):
    # read SPTPTW data
    base_path = './Instances/'
    path = base_path + file_name + '.txt'
    net = {}
    with open(path, 'r') as f:
        data = f.readline().split()
        nn = int(data[0])
        for node in range(nn):
            net[node] = {}
        ns = int(data[-1])
        link_num = []
        for ind in range(nn):
            data = f.readline()
            link_num.append(int(data))
        for i in range(nn):
            for j in range(link_num[i]):
                data = f.readline().split()
                node = int(data[0])
                length = float(data[1])
                time = float(data[2])
                net[i][node - 1] = [length, time]
        source = int(f.readline())
        destination = int(f.readline())
        node_subset = []
        serve_time = {}
        time_window = {}
        for i in range(ns):
            data = f.readline().split()
            temp_num = int(data[0])
            temp_node = []
            for j in range(temp_num):
                node = int(data[j * 4 + 1]) - 1
                serve = float(data[j * 4 + 2])
                start = float(data[j * 4 + 3])
                end = float(data[j * 4 + 4])
                serve_time[node] = serve
                time_window[node] = [start, end]
                temp_node.append(node)
            node_subset.append(temp_node)
    return net, node_subset, time_window, serve_time


if __name__ == '__main__':
    import RSA
    import labeling
    import labeling_v2
    from copy import deepcopy
    import time

    network1, node_subset1, time_window1, serve_time1 = read_data('dmin2max/R3_k5_s29_dmin2max_avg100')
    network2 = deepcopy(network1)
    network3 = deepcopy(network1)
    node_subset2 = deepcopy(node_subset1)
    node_subset3 = deepcopy(node_subset1)
    time_window2 = deepcopy(time_window1)
    time_window3 = deepcopy(time_window1)
    serve_time2 = deepcopy(serve_time1)
    serve_time3 = deepcopy(serve_time1)
    time0 = time.time()
    result1 = RSA.main(network1, node_subset1, time_window1, serve_time1)
    time1 = time.time()
    result2 = labeling.main(network2, node_subset2, time_window2, serve_time2)
    time2 = time.time()
    result3 = labeling_v2.main(network3, node_subset3, time_window3, serve_time3)
    time3 = time.time()
    print('The running time of RSA: ' + str(time1 - time0))
    print('The running time of labeling: ' + str(time2 - time1))
    print('The running time of labeling_2: ' + str(time3 - time2))
    print('The result of RSA: ')
    print(result1)
    print('The result of labeling: ')
    print(result2)
    print('The result of labeling_v2: ')
    print(result3)
