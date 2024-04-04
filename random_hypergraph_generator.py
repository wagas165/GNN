import numpy as np
from hypergraph import Hypergraph
import matplotlib.pyplot as plt

class RandomHypergraphGenerator:
    def __init__(self, N, S, p, target_k):
        """
        初始化随机超图生成器。

        参数:
        - N: 节点的总数。
        - S: 子组的总数。
        - p: 选择子组加入超边的概率。
        - target_k: 超图达到的目标平均度。
        """
        self.N = N
        self.S = S
        self.p = p
        self.target_k = target_k

    def generate(self):
        """
        生成随机超图，直到达到期望的平均度k。

        返回:
        - 生成的Hypergraph实例。
        """
        hypergraph = Hypergraph()
        # 子组集合用于避免重复
        subgroups_set = set()
        subgroups = []

        # 生成不重复的子组
        while len(subgroups) < self.S:
            size = np.random.poisson(2)
            if size > 1:
                subgroup = frozenset(np.random.choice(range(self.N), size, replace=False))
                if subgroup not in subgroups_set:
                    subgroups_set.add(subgroup)
                    subgroups.append(subgroup)

        degrees = np.zeros(self.N)  # 节点的度数数组
        current_k = 0  # 当前平均度
        hyperedges_set = set()  # 超边集合用于避免重复

        while current_k < self.target_k:
            if np.random.rand() < self.p and subgroups:
                selected_subgroup = subgroups[np.random.choice(len(subgroups))]
                if selected_subgroup not in hyperedges_set:  # 确保不添加重复超边
                    hyperedges_set.add(selected_subgroup)
                    hypergraph.add_hyperedge(set(selected_subgroup))



                    for node in selected_subgroup:
                        degrees[node] += 1
            else:
                size = np.random.poisson(2)
                if size > 1:
                    selected_nodes = frozenset(np.random.choice(range(self.N), size, replace=False))
                    if selected_nodes not in hyperedges_set:  # 确保不添加重复超边
                        hyperedges_set.add(selected_nodes)
                        hypergraph.add_hyperedge(set(selected_nodes))
                        for node in selected_nodes:
                            degrees[node] += 1

            current_k = np.mean(degrees)  # 更新当前平均度

        return hypergraph

#visualize the hypergraph
# H=RandomHypergraphGenerator(40,4,0.3,1.1)
# hypergraph=H.generate()
# print(hypergraph.get_hyperedges())
# H= hnx.Hypergraph(hypergraph.get_hyperedges())
# hnx.draw(H)
# plt.show()

