from hypergraph import Hypergraph
from itertools import combinations
from collections import defaultdict
from tqdm import tqdm
import sys
sys.setrecursionlimit(10000)
def find_shared_nodes(hyperedge1, hyperedge2):
    """计算两个超边共享的节点数"""
    return len(set(hyperedge1) & set(hyperedge2))


def build_high_order_connectivity(hypergraph, m_order):
    """
    使用节点索引来优化构建m阶连通性的过程，并显示处理进度。
    """
    # 节点到超边的映射
    node_to_hyperedges = defaultdict(list)
    for index, hyperedge in enumerate(hypergraph.get_hyperedges()):
        for node in hyperedge:
            node_to_hyperedges[node].append(index)

    # 初始化连通性字典
    connectivity = defaultdict(set)

    total_nodes = len(node_to_hyperedges)  # 总节点数
    processed_nodes = 0  # 已处理节点数

    # 使用tqdm显示进度条
    for node, hyperedges in tqdm(node_to_hyperedges.items(), desc="Building connectivity"):
        for hyperedge1_index, hyperedge2_index in combinations(hyperedges, 2):
            hyperedge1 = hypergraph.get_hyperedges()[hyperedge1_index]
            hyperedge2 = hypergraph.get_hyperedges()[hyperedge2_index]

            hyperedge1_tuple = tuple(sorted(hyperedge1))
            hyperedge2_tuple = tuple(sorted(hyperedge2))

            if find_shared_nodes(hyperedge1, hyperedge2) >= m_order:
                connectivity[hyperedge1_tuple].add(hyperedge2_tuple)
                connectivity[hyperedge2_tuple].add(hyperedge1_tuple)

        processed_nodes += 1
        # 可选：每处理一定比例的节点后打印一次进度
        # if processed_nodes % (total_nodes // 10) == 0:  # 例如，每处理10%的节点时更新一次进度
        #     print(f"Processed {processed_nodes} / {total_nodes} nodes.")

    return connectivity

def find_hocs(connectivity):
    """根据m阶连通性信息识别HOCs。这里使用的是简化的逻辑，更复杂的场景可能需要更复杂的图遍历算法。"""
    visited = set()
    hocs = []

    def dfs(hyperedge, current_hoc):
        """深度优先搜索识别HOC"""
        if hyperedge in visited:
            return
        visited.add(hyperedge)
        current_hoc.add(hyperedge)
        for neighbor in connectivity.get(hyperedge, []):
            dfs(neighbor, current_hoc)

    for hyperedge in connectivity:
        if hyperedge not in visited:
            current_hoc = set()
            dfs(hyperedge, current_hoc)
            hocs.append(current_hoc)

    return hocs


def identify_hocs(hypergraph):
    all_hocs = {}
    m_order = 2  # 从二阶连通性开始搜索

    while True:
        connectivity = build_high_order_connectivity(hypergraph, m_order)
        hocs = find_hocs(connectivity)
        if not hocs:  # 如果这个阶数的HOCs为空，停止搜索
            break
        all_hocs[m_order] = hocs
        m_order += 1  # 移动到下一个阶数

    return all_hocs


