import numpy as np
import random
import hoc_identification
from tqdm import tqdm

class ContagionDynamics:
    def __init__(self, hypergraph, hocs, model, beta=0.1, gamma=0.05, beta_high_order=None):
        """
        初始化传播动态模拟。

        参数:
        - hypergraph: 超图实例。
        - hocs: 高阶组件的列表，每个组件是一组超边。
        - model: 使用的模型类型，'SIR' 或 'SIS'。
        - beta: 基础感染率（一阶传播率）。
        - gamma: 康复率，仅在SIR模型中使用。
        - beta_high_order: 高阶传播率的列表，列表的第i个元素代表(i+2)阶传播的感染率。
        """
        self.hypergraph = hypergraph
        self.hocs = hocs
        self.model = model
        self.beta = beta
        self.gamma = gamma
        self.beta_high_order = beta_high_order if beta_high_order is not None else []
        self.status = {node: 'S' for node in hypergraph.get_nodes()}

        # 随机选择一条超边并将其所有节点标记为感染
        if hypergraph.get_hyperedges():
            initial_infected_edge = random.choice(list(hypergraph.get_hyperedges()))
            for node in initial_infected_edge:
                self.status[node] = 'I'

    def step(self):
        """
        执行模拟的一个时间步。
        """
        new_status = self.status.copy()

        # 超边内部直接以一阶感染率传播
        for hyperedge in self.hypergraph.get_hyperedges():
            self._spread_infection_within_hyperedge(hyperedge, new_status)

        # 利用 hocs 信息进行高阶传播
        if self.beta_high_order:
            for order, hocs in self.hocs.items():
                # 确保不会因为索引问题而导致错误
                if order - 2 < len(self.beta_high_order):
                    beta = self.beta_high_order[order - 2]  # 安全地获取beta值
                    for hoc in hocs:
                        self._spread_infection_among_hyperedges(hoc, new_status, beta)
                else:
                    # 处理索引越界的情况，比如通过打印警告
                    print(f"Warning: No beta value provided for order {order}. Skipping...")

        # 根据模型类型更新感染者状态
        if self.model == 'SIR':
                for node, status in self.status.items():
                    if status == 'I' and random.random() < self.gamma:
                        new_status[node] = 'R'
        elif self.model == 'SIS':
                for node, status in self.status.items():
                    if status == 'I' and random.random() < self.gamma:
                        new_status[node] = 'S'

        self.status = new_status

    def _spread_infection_within_hyperedge(self, hyperedge, new_status):
        infected = [node for node in hyperedge if self.status[node] == 'I']
        if infected:
            for node in hyperedge:
                if self.status[node] == 'S' and random.random() < self.beta:
                    new_status[node] = 'I'

    def _spread_infection_among_hyperedges(self, hoc, new_status, beta):
        """
        在给定的高阶组件内模拟高阶传播，要求超边之间至少共享一个节点。

        参数:
        - hoc: 当前处理的高阶组件，是一个包含多个超边的集合。
        - new_status: 用于记录状态更新的字典。
        - beta: 高阶传播的感染率。
        """
        # 检查并标记每个超边的感染状态
        # if len(hoc) > 100:
        #     loop = tqdm(hoc, desc="Spreading infection among hyperedges")
        # else:
        #     loop = hoc  # 直接遍历，不使用tqdm
        for hyperedge in hoc:
            if any(self.status[node] == 'I' for node in hyperedge):  # 如果超边内有感染者
                for adjacent_hyperedge in hoc:
                    if adjacent_hyperedge != hyperedge and hoc_identification.find_shared_nodes(hyperedge,
                                                                                                adjacent_hyperedge) > 0:
                        # 以beta的概率感染相邻超边的易感节点
                        for node in adjacent_hyperedge:
                            if self.status[node] == 'S' and random.random() < beta:
                                new_status[node] = 'I'
    def simulate(self, steps=10):
        # 初始化存储每个时间步状态计数的列表
        self.status_counts_over_time = []
        for _ in tqdm(range(steps),desc="Running simulation"):
            self.step()
            self.status_counts_over_time.append(self.get_status_counts())

    def get_status_counts(self):
        return {status: list(self.status.values()).count(status) for status in set(self.status.values())}

