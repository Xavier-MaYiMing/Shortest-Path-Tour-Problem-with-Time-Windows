### Shortest Path Tour Problem with Time Windows 

##### Reference: Pugliese L D P, Ferone D, Festa P, et al. Shortest path tour problem with time windows[J]. European Journal of Operational Research, 2020, 282(1): 334-344.

The shortest path tour problem (SPTP) aims to find the shortest path that traverses multiple disjoint node subsets in a given order. The SPTP with time windows (SPTPTW) takes the time window constraints into account.

- labeling.py: The labeling method from the SPTPTW
- labeling_v2.py: The labeling method for the SPTPTW with upper bound initialization strategy
- RSA.py: The ripple-spreading algorithm (RSA) for the SPTPTW
- Instances: The test cases of the SPTPTW (https://bit.ly/2H1G8JK)
- test.py: Read test cases and compare algorithms of the SPTPTW

----

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node1: {node2: [cost, time], ...}, ...}         |
| node_subset   | List, [[subset1], [subset2], ...]                            |
| source        | The source node                                              |
| destination   | The destination node                                         |
| nn            | The number of nodes                                          |
| ns            | The number of node subsets                                   |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the ith ripple is epicenter_set[i] |
| radius_set    | List, the radius of the ith ripple is radius_set[i]          |
| path_set      | List, the path of the ith ripple from the source node to node i is path_set[i] |
| length_set    | List, the length of path_set[i]                              |
| time_set      | List, the time of path_set[i]                                |
| level_set     | List, the level of path_set[i]                               |
| active_set    | List, active_set contains all active ripples                 |
| Omega         | Dictionary, Omega[n] = i denotes that ripple i is generated at node n |
| label_set     | All generated labels                                         |
| label         | label[n] denotes all labels of node n                        |
| best_solution | The best solution ever found                                 |
| delta         | The length of best_solution                                  |

----

#### Example

##### Run the test.py (The test case is dmin2max/R3_k5_s29_dmin2max_avg100).

##### Output:

```python
The running time of RSA: 43.04834604263306
The running time of labeling: 6.481421232223511
The running time of labeling_2: 6.684788942337036
The result of RSA: 
{
  'cost': 65030.0, 
  'time': 1547.9999999999998, 
  'level': 7, 
  'path': [0, 85, 115, 35, 156, 14, 34, 264, 174, 96, 278, 258, 120, 206, 299]
}
The result of labeling: 
{
  'cost': 65030.0, 
  'time': 1547.9999999999998, 
  'level': 7, 
  'path': [0, 85, 115, 35, 156, 14, 34, 264, 174, 96, 278, 258, 120, 206, 299]
}
The result of labeling_v2: 
{
  'cost': 65030.0, 
  'time': 1547.9999999999998, 
  'level': 7, 
  'path': [0, 85, 115, 35, 156, 14, 34, 264, 174, 96, 278, 258, 120, 206, 299]
}
```

