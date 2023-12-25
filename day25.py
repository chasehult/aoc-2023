import random

import networkx as nx

inp = open('day25.txt').read().strip()


class WireGroup:
    def __init__(self, wires: set[str] | frozenset[str]):
        self.wires = frozenset(wires)

    def __add__(self, other: 'WireGroup'):
        return WireGroup(self.wires | other.wires)

    def __contains__(self, other: 'WireGroup'):
        return (self.wires & other.wires)

    def __copy__(self):
        return WireGroup(self.wires)

    def __eq__(self, other):
        return isinstance(other, WireGroup) and self.wires == other.wires

    def __hash__(self):
        return hash(self.wires)


# wgs = []
# for line in inp.split('\n'):
#     wgs.append(WireGroup(set(re.findall(r'\w{3}', line))))


# old = None
# while wgs != old:
#     old = deepcopy(wgs)
#
#     newwgs = []
#     combined = set()
#     for i, wg1 in enumerate(wgs):
#         nwg = copy(wg1)
#         for wg2 in wgs[i+1:]:
#             if wg2 in combined:
#                 continue
#             if wg1 in wg2:
#                 nwg += wg2
#                 combined.add(wg2)
#         newwgs.append(nwg)
#     wgs = newwgs
# print(wgs)

graph = nx.Graph()
for line in inp.split('\n'):
    frm, tos = line.split(': ')
    for to in tos.split(' '):
        graph.add_edge(frm, to)

for f, t in nx.minimum_edge_cut(graph):
    graph.remove_edge(f, t)
c1, c2 = [*nx.connected_components(graph)]  # noqa
print(len(c1) * len(c2))


# edges = [*graph.edges]
# random.shuffle(edges)
#
# print(len(edges))
# for i1, (f1, t1) in enumerate(edges):
#     graph.remove_edge(f1, t1)
#     for i2, (f2, t2) in enumerate(edges[i1+1:]):
#         if f1 == f2 and t1 == t2:
#             continue
#         graph.remove_edge(f2, t2)
#         for i3, (f3, t3) in enumerate(edges[i2+1:]):
#             if f1 == f3 and t1 == t3:
#                 continue
#             if f2 == f3 and t2 == t3:
#                 continue
#             graph.remove_edge(f3, t3)
#             if len([*nx.connected_components(graph)]) == 2:
#                 c1, c2 = [*nx.connected_components(graph)]  # noqa
#                 print(len(c1) * len(c2))
#             graph.add_edge(f3, t3)
#         graph.add_edge(f2, t2)
#     graph.add_edge(f1, t1)
