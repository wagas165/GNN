from random_hypergraph_generator import RandomHypergraphGenerator
from hypergraph import Hypergraph
from hoc_identification import identify_hocs
from contagion_dynamics import ContagionDynamics
import matplotlib.pyplot as plt
import numpy as np




class ExperimentSetup():
    def __init__(self, N=None, S=None, p=None, target_k=None, model='SIR', beta=0.1, gamma=0.05, beta_high_order=None,
                 dataset_paths=None):
        """
        初始化实验设置。

        参数:
        - N, S, p, target_k: 用于随机超图生成的参数。
        - model, beta, gamma, beta_high_order: 传染模型的参数。
        - dataset_paths: 包含nverts文件路径、simplices文件路径的元组。如果提供了dataset_paths，则从数据集构建超图。
        """
        self.N = N
        self.S = S
        self.p = p
        self.target_k = target_k
        self.model = model
        self.beta = beta
        self.gamma = gamma
        self.beta_high_order = beta_high_order
        self.dataset_paths = dataset_paths

    def build_hypergraph_from_files(self):
        """
        从文件构建超图。
        """

        hypergraph = Hypergraph()
        dataset_paths = self.dataset_paths
        nverts_path= dataset_paths[0]
        simplices_path=dataset_paths[1]
        added_hyperedges = set()

        # 读取每个单纯形的顶点数
        with open(nverts_path, 'r') as file:
            nverts = [int(line.strip()) for line in file.readlines()]

        # 读取构成单纯形的节点列表
        with open(simplices_path, 'r') as file:
            simplices_nodes = [int(line.strip()) for line in file.readlines()]

        # 构建超边
        start = 0
        for nvert in nverts:
            hyperedge = set(simplices_nodes[start:start + nvert])
            # 将超边转换为元组以便在集合中进行唯一性检查
            hyperedge_tuple = tuple(sorted(hyperedge))

            if hyperedge_tuple not in added_hyperedges:
                hypergraph.add_hyperedge(hyperedge)
                added_hyperedges.add(hyperedge_tuple)

            start += nvert

        print('hypergraph successfully built')
        return hypergraph

    def run(self, steps=50):
        """
        运行实验。
        """
        # 根据是否提供了数据集路径来构建超图
        if self.dataset_paths:
            hypergraph = self.build_hypergraph_from_files(self.dataset_paths)
            # H = hnx.Hypergraph(hypergraph.get_hyperedges())
            # hnx.draw(H)
            # plt.show()
        else:
            generator = RandomHypergraphGenerator(self.N, self.S, self.p, self.target_k)
            hypergraph = generator.generate()


        # 识别高阶组件
        hocs = identify_hocs(hypergraph)  # 示例中关注2阶组件
        # hoc_hypergraph = Hypergraph()
        # for hoc in hocs:
        #     for hyperedge in hoc:
        #         hoc_hypergraph.add_hyperedge(set(hyperedge))
        # H = hnx.Hypergraph(hoc_hypergraph.get_hyperedges())
        # hnx.draw(H)
        # plt.show()

        # 设置传染动态模拟
        contagion_model = ContagionDynamics(hypergraph, hocs, self.model, self.beta, self.gamma, self.beta_high_order)
        contagion_model.simulate(steps)

        # 可视化结果
        self.visualize(contagion_model.status_counts_over_time, steps)



    def visualize(self, status_counts_over_time, steps):
        """
        可视化传染动态模拟结果。

        参数:
        - status_counts_over_time: 每个时间步的状态计数列表。
        - steps: 模拟的时间步数。
        """
        time_steps = range(steps)
        S_counts = [status_counts.get('S', 0) for status_counts in status_counts_over_time]
        I_counts = [status_counts.get('I', 0) for status_counts in status_counts_over_time]
        R_counts = [status_counts.get('R', 0) for status_counts in status_counts_over_time]

        def calculate_relative_outbreak_size():
            # 稳态时的感染者和恢复者总数
            infected_count = I_counts[-1]
            recovered_count = R_counts[-1]
            total_count = infected_count + recovered_count

            # 网络中的总节点数
            total_nodes = self.N

            # 相对爆发规模
            relative_outbreak_size = total_count / total_nodes
            self.relative_outbreak_size = relative_outbreak_size
            print(f"Relative outbreak size: {relative_outbreak_size:.2f}")

        calculate_relative_outbreak_size()


        plt.figure(figsize=(10, 6))
        plt.plot(time_steps, S_counts, label='Susceptible')
        plt.plot(time_steps, I_counts, label='Infected')
        plt.plot(time_steps, R_counts, label='Recovered', linestyle='--')
        plt.xlabel('Time Step')
        plt.ylabel('Count')
        plt.title('Contagion Dynamics Over Time')
        plt.legend()
        plt.show()

# Hypergraph_highschool = ExperimentSetup(model='SIR', beta=0.8, gamma=0.05, beta_high_order=[0.5, 0.3, 0.1],
#                                         dataset_paths=['/Users/alphazhang/Desktop/pythonproject/HOC dynamics/contact-high-school/contact-high-school-nverts.txt',
#                                                   '/Users/alphazhang/Desktop/pythonproject/HOC dynamics/contact-high-school/contact-high-school-simplices.txt'])
# Hypergraph_highschool.run(steps=100)

# RandomH=ExperimentSetup(N=10000,S=10000,p=0.5,target_k=5,model='SIS',beta=0.1,gamma=0.2,beta_high_order=[0.12,0.1])
# RandomH.run(steps=100)
