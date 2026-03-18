import networkx as nx
import matplotlib.pyplot as plt

def build_network():
    """
    Creates a Graph representation of a multi-layer network.
    """
    G = nx.Graph()

    # Define nodes: Core, Distribution, and Access layers
    # Edges include 'weight' representing latency in milliseconds
    G.add_edge("Core_Router", "Dist_Switch_1", weight=1)
    G.add_edge("Core_Router", "Dist_Switch_2", weight=1)
    
    # Path A is congested (Weight 10)
    G.add_edge("Dist_Switch_1", "Access_Switch_A", weight=10) 
    # Path B is clear (Weight 2)
    G.add_edge("Dist_Switch_2", "Access_Switch_B", weight=2)
    
    G.add_edge("Access_Switch_A", "Server_1", weight=1)
    G.add_edge("Access_Switch_B", "Server_2", weight=1)

    return G

def analyze_critical_nodes(G):
    """
    Uses Betweenness Centrality to identify network chokepoints.
    """
    centrality = nx.betweenness_centrality(G)
    return max(centrality, key=centrality.get)

def find_optimized_path(G, start, end):
    """
    Finds the path based on weights (latency) rather than just hop count.
    """
    return nx.shortest_path(G, source=start, target=end, weight='weight')

if __name__ == "__main__":
    net = build_network()
    critical = analyze_critical_nodes(net)
    
    # Find the best path to Server_1
    # Even if Dist_Switch_2 is "further" in hops, it might be faster if weights are lower
    path = find_optimized_path(net, "Core_Router", "Server_1")
    
    print(f"Critical Node (Chokepoint): {critical}")
    print(f"AI Optimized Path to Server 1: {' -> '.join(path)}")
    
    # Visualization for the README
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(net)
    nx.draw(net, pos, with_labels=True, node_color='skyblue', node_size=2500, font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(net, 'weight')
    nx.draw_networkx_edge_labels(net, pos, edge_labels=labels)
    
    plt.title("AI-Driven Network Topology Map")
    plt.savefig("topology_map.png")
    print("Map saved as topology_map.png")