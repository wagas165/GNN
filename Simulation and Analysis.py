import numpy as np
import matplotlib.pyplot as plt
from contagion_dynamics import ContagionDynamics
from random_hypergraph_generator import RandomHypergraphGenerator
from hypergraph import Hypergraph
import random
from experiment_setup import ExperimentSetup
from hoc_identification import identify_hocs


# 设置模拟参数
lambda_h_values = np.arange(0.28, 0.46, 0.02)
#选择一个在0.25和0.75之间的随机值
gamma_value=0.05
high_order_betas = [lambda_h_value * gamma_value for lambda_h_value in lambda_h_values]

# 准备空列表来收集结果
empirical_results = []
random_results = []


def calculate_relative_outbreak_size(final_status_counts):
    # 计算I和R状态的节点总数
    I_count = final_status_counts.get('I', 0)
    R_count = final_status_counts.get('R', 0)
    total_count = I_count

    # 网络中的总节点数
    total_nodes = sum(final_status_counts.values())

    # 相对爆发规模
    relative_outbreak_size = total_count / total_nodes
    return relative_outbreak_size


# 运行模拟
for high_order_beta in high_order_betas:

    # 运行实证超图模型
    empirical_hypergraph = ExperimentSetup(model='SIS', dataset_paths=[
        'contact-high-school/contact-high-school-nverts.txt',
        'contact-high-school/contact-high-school-simplices.txt'])
    empirical_hypergraph = empirical_hypergraph.build_hypergraph_from_files()

    empirical_hocs = identify_hocs(empirical_hypergraph)
    empirical_contagion_model = ContagionDynamics(empirical_hypergraph, hocs=empirical_hocs, model='SIS', beta=0, gamma=0.05, beta_high_order=[high_order_beta]*8)
    empirical_contagion_model.simulate(steps=80)  # 假设步数足以达到稳态
    final_status_counts = empirical_contagion_model.get_status_counts()  # 获取最后一个时间步的状态计数
    empirical_results.append(calculate_relative_outbreak_size(final_status_counts))

    del empirical_hypergraph
    del empirical_hocs
    del empirical_contagion_model

    # 运行随机超图模型
    random_hypergraph = RandomHypergraphGenerator(N=10000, S=10000, p=0.5, target_k=5).generate()
    random_contagion_model = ContagionDynamics(random_hypergraph, hocs=identify_hocs(random_hypergraph), model='SIS', beta=0, gamma=0.05, beta_high_order=[high_order_beta]*100)
    random_contagion_model.simulate(steps=80)  # 假设步数足以达到稳态
    final_status_counts = random_contagion_model.get_status_counts()  # 获取最后一个时间步的状态计数
    random_results.append(calculate_relative_outbreak_size(final_status_counts))


# 绘制实证和随机模型的结果
plt.figure(figsize=(10, 8))
plt.plot(lambda_h_values, empirical_results, label='Empirical', marker='o')
plt.plot(lambda_h_values, random_results, label='Random',marker='s')
plt.xlabel('λ_h')
plt.ylabel('Relative Outbreak Size')
plt.title('Relative Outbreak Size for SIS Model')
plt.legend()
plt.show()
