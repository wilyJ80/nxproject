import networkx as nx
import matplotlib.pyplot as plt
import os

class GraphService:
    def __init__(self):
        self.graph = None
        self.is_weighted = False
        self.is_directed = False

    def load_from_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Graph file not found: {file_path}")

        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError(f"File {file_path} is empty.")

        header = lines[0].split()
        if len(header) != 2:
            raise ValueError("Invalid header format. Expected '[G|D] [N|W]'.")

        graph_type, weight_type = header
        self.is_directed = (graph_type == "D")
        self.is_weighted = (weight_type == "W")

        if self.is_directed:
            self.graph = nx.DiGraph()
        elif graph_type == "G":
            self.graph = nx.Graph()
        else:
            raise ValueError(f"Invalid graph type '{graph_type}'. Use 'G' or 'D'.")

        for line in lines[1:]:
            parts = line.split()
            if self.is_weighted:
                if len(parts) != 3:
                    raise ValueError(f"Weighted graph expects 'u v w', got: {line}")
                u, v, w = parts
                self.add_edge(u, v, float(w))
            else:
                if len(parts) != 2:
                    raise ValueError(f"Unweighted graph expects 'u v', got: {line}")
                u, v = parts
                self.add_edge(u, v)

        return self.graph

    def add_vertex(self, v):
        if self.graph is None:
            self.graph = nx.Graph()
        
        self.graph.add_node(v)

    def add_edge(self, u, v, weight=None):
        if self.graph is None:
            self.graph = nx.Graph()

        if self.is_weighted:
            w_val = float(weight) if weight is not None else 0.0
            self.graph.add_edge(u, v, weight=w_val)
        else:
            self.graph.add_edge(u, v)

    def get_adjacency_matrix(self):
        if self.graph is None:
            return [], []

        nodes = sorted(list(self.graph.nodes()))
        size = len(nodes)
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        matrix = [[0.0 if self.is_weighted else 0 for _ in range(size)] for _ in range(size)]

        for u, v, data in self.graph.edges(data=True):
            i, j = node_to_idx[u], node_to_idx[v]
            weight = data.get('weight', 0.0) if self.is_weighted else 1
            matrix[i][j] = weight
            if not self.is_directed:
                matrix[j][i] = weight

        return nodes, matrix

    def get_incidence_matrix(self):
        if self.graph is None:
            return [], [], []
        
        nodes = sorted(list(self.graph.nodes()))
        edges = list(self.graph.edges(data=True))
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        num_nodes = len(nodes)
        num_edges = len(edges)
        
        matrix = [[0.0 for _ in range(num_edges)] for _ in range(num_nodes)]
        
        for e_idx, (u, v, data) in enumerate(edges):
            u_idx, v_idx = node_to_idx[u], node_to_idx[v]
            weight = data.get('weight', 0.0) if self.is_weighted else 1.0
            
            if self.is_directed:
                matrix[u_idx][e_idx] = -weight
                matrix[v_idx][e_idx] = weight
            else:
                matrix[u_idx][e_idx] = weight
                matrix[v_idx][e_idx] = weight
                
        return nodes, edges, matrix

    def get_adjacency_list(self):
        if self.graph is None:
            return {}
            
        adj_list = {}
        for node in sorted(self.graph.nodes()):
            neighbors = []
            for neighbor in sorted(self.graph[node]):
                if self.is_weighted:
                    weight = self.graph[node][neighbor].get('weight', 0.0)
                    neighbors.append((neighbor, weight))
                else:
                    neighbors.append(neighbor)
            adj_list[node] = neighbors
        return adj_list

    def display_adjacency_matrix(self):
        nodes, matrix = self.get_adjacency_matrix()
        if not nodes:
            print("Graph is empty.")
            return

        header = "    " + " ".join(f"{str(n):>3}" for n in nodes)
        print("\nAdjacency Matrix:")
        print(header)
        print("-" * len(header))

        for i, row in enumerate(matrix):
            row_str = f"{str(nodes[i]):<2} | " + " ".join(
                f"{val:3g}" if isinstance(val, float) else f"{val:3}" 
                for val in row
            )
            print(row_str)

    def display_incidence_matrix(self):
        nodes, edges, matrix = self.get_incidence_matrix()
        if not nodes:
            print("Graph is empty.")
            return

        edge_labels = [f"({u},{v})" for u, v, _ in edges]
        header = "    " + " ".join(f"{label:>8}" for label in edge_labels)
        print("\nIncidence Matrix:")
        print(header)
        print("-" * len(header))

        for i, row in enumerate(matrix):
            row_str = f"{str(nodes[i]):<2} | " + " ".join(f"{val:8g}" for val in row)
            print(row_str)

    def display_adjacency_list(self):
        adj_list = self.get_adjacency_list()
        print("\nAdjacency List:")
        for node, neighbors in adj_list.items():
            if self.is_weighted:
                neigh_str = ", ".join([f"({n}, {w:g})" for n, w in neighbors])
            else:
                neigh_str = ", ".join([str(n) for n in neighbors])
            print(f"{node}: [{neigh_str}]")

    def visualize(self, title="Graph Visualization"):
        if self.graph is None or self.graph.number_of_nodes() == 0:
            print("Graph is empty or not loaded.")
            return

        pos = nx.spring_layout(self.graph)
        nx.draw(
            self.graph, pos, with_labels=True, 
            node_color='lightblue', edge_color='gray', 
            node_size=800, font_size=10, 
            arrows=self.is_directed, arrowsize=15
        )

        if self.is_weighted:
            labels = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        plt.title(title)
        plt.show()

def main():
    service = GraphService()
    try:
        print("Attempting to load grafo01.txt...")
        service.load_from_file("grafo01.txt")
        service.display_adjacency_matrix()
        service.display_incidence_matrix()
        service.display_adjacency_list()
        
        print("\nAttempting to load digrafo01.txt...")
        service.load_from_file("digrafo01.txt")
        service.display_adjacency_matrix()
        service.display_incidence_matrix()
        service.display_adjacency_list()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
