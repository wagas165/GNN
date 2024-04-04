from hypergraph import Hypergraph
from hoc_identification import identify_hocs
import matplotlib.pyplot as plt
import networkx as nx
from contagion_dynamics import ContagionDynamics

# 创建一个超图实例
hypergraph = Hypergraph()
hypergraph.add_hyperedge({'A', 'B', 'C', 'D'})
hypergraph.add_hyperedge({'C', 'D', 'E'})
hypergraph.add_hyperedge({'E', 'F', 'G'})
hypergraph.add_hyperedge({'F','G','H', 'I'})
hypergraph.add_hyperedge({'J', 'K', 'L', 'M'})
hypergraph.add_hyperedge({'M', 'N', 'O'})

# 步骤2: 识别高阶组件
hocs = identify_hocs(hypergraph, 2)  # 假设我们关注的是2阶组件

# 步骤3: 初始化ContagionDynamics对象
contagion_model = ContagionDynamics(hypergraph, hocs, model='SIR', beta=0.5, gamma=0.05, beta_high_order=[0, 0.1])

# 步骤4: 运行模拟
contagion_model.status['A'] = 'I'  # 将节点A标记为初始感染者
contagion_model.simulate(steps=100)

# 绘制状态变化
status_counts_over_time = contagion_model.status_counts_over_time
time_steps = list(range(len(status_counts_over_time)))

# 对于每种状态，获取每个时间步的人数
for status in ['S', 'I', 'R']:
    counts = [step_counts.get(status, 0) for step_counts in status_counts_over_time]
    plt.plot(time_steps, counts, label=status)

plt.xlabel('Time Step')
plt.ylabel('Number of People')
plt.title('Contagion Dynamics Over Time')
plt.legend()
plt.show()