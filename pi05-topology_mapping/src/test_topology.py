import pytest
import networkx as nx
from topology_engine import build_network, analyze_critical_nodes, find_optimized_path

def test_critical_node_detection():
    """Verify the Core Router is identified as the central chokepoint."""
    G = build_network()
    critical = analyze_critical_nodes(G)
    assert "Core" in critical

def test_pathfinding_logic():
    """Verify the optimizer correctly follows the weights."""
    G = build_network()
    # Route to Server_2 should specifically go through Dist_Switch_2
    path = find_optimized_path(G, "Core_Router", "Server_2")
    assert "Dist_Switch_2" in path
    assert path[-1] == "Server_2"

def test_connectivity():
    """Ensure no 'Islands' exist in the graph."""
    G = build_network()
    assert nx.is_connected(G), "Network should be fully connected in base state"