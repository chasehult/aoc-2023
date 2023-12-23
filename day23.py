import networkx as nx
import numpy as np

inp = open('day23.txt').read().strip()

grid = np.array([list(line) for line in inp.split('\n')])
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

graph = nx.DiGraph()

for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x, y] != '#':
            graph.add_node((x, y))

for x in range(len(grid)):
    for y in range(len(grid[0])):
        match grid[x, y]:
            case '.':
                for dir in directions:
                    if 0 <= x + dir[0] < len(grid) \
                            and 0 <= y + dir[1] < len(grid[0]) \
                            and grid[x + dir[0], y + dir[1]] != '#':
                        graph.add_edge((x, y), (x + dir[0], y + dir[1]))
            case '>':
                graph.add_edge((x, y), (x, y+1))
            case '^':
                graph.add_edge((x, y), (x-1, y))
            case 'v':
                graph.add_edge((x, y), (x+1, y))
            case '<':
                graph.add_edge((x, y), (x, y-1))

max_len = 0
for path in nx.all_simple_paths(graph, (0, 1), (len(grid) - 1, len(grid[0]) - 2)):
    max_len = max(max_len, len(path))
print(max_len-1)


graph = nx.Graph()

for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x, y] != '#':
            graph.add_node((x, y))

for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x, y] != '#':
            for dir in directions:
                if 0 <= x + dir[0] < len(grid) \
                        and 0 <= y + dir[1] < len(grid[0]) \
                        and grid[x + dir[0], y + dir[1]] != '#':
                    graph.add_edge((x, y), (x + dir[0], y + dir[1]), weight=1)

for _ in range(100):
    for node in graph.nodes:
        if len(graph[node]) == 2:
            (n1, w1), (n2, w2) = graph[node].items()
            graph.remove_edge(node, n1)
            graph.remove_edge(node, n2)
            graph.add_edge(n1, n2, weight=w1['weight']+w2['weight'])

max_len = 0
for path in nx.all_simple_paths(graph, (0, 1), (len(grid) - 1, len(grid[0]) - 2)):
    weight = 0
    for i in range(1, len(path)):
        weight += graph.edges[path[i-1], path[i]]['weight']
    max_len = max(max_len, weight)
print(max_len)
