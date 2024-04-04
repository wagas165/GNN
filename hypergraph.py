class Hypergraph:
    def __init__(self):
        #H=(V, E)
        self.nodes = set()
        self.hyperedges = []

    def add_node(self, node):
        self.nodes.add(node)

    def add_hyperedge(self, hyperedge):
        self.hyperedges.append(hyperedge)
        self.nodes.update(hyperedge)

    def get_nodes(self):
        return list(self.nodes)

    def get_hyperedges(self):
        return self.hyperedges
