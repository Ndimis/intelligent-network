# Concept Explainer: Graph-Based Network Topology Discovery

### 🧠 The Core Concept
Modern networks are too complex for manual mapping. **Graph Theory** provides a mathematical framework to visualize and optimize these connections. In this project, we represent the network as a **Directed Graph** using the `NetworkX` library.

- **Nodes (Vertices):** Represent Hardware (Routers, Switches, Servers).
- **Edges (Links):** Represent Connections (Ethernet, Fiber, VPN).
- **Weights:** Represent Metrics (Latency, Bandwidth, Congestion).



### 🛠️ Lessons Learned
1.  **Critical Path Analysis:** By calculating **Betweenness Centrality**, we can identify which router is the most significant "chokepoint" in the infrastructure. If this node fails, the network fractures.
2.  **Resilience Testing:** We can mathematically simulate "What happens if Router B fails?" and see if the network remains connected or breaks into "Islands".
3.  **AI-Driven Pathfinding:** Unlike static routing tables, graph-based routing allows an AI controller to find the "Cheapest" path based on real-time link weights (latency/load).

### 📝 Key Takeaway
> **A network is only as strong as its most central node.** Understanding the topology allows us to prioritize hardware upgrades on the nodes that carry the most logical weight, rather than just the nodes with the most physical connections.

### 🚀 How to Run
1. **Install Dependencies**:
   ```bash
   pip install networkx matplotlib pytest