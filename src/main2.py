import networkx as nx
import os
from main import GraphService

def modified_dfs_all_paths(graph, u, v, k):
    all_paths = []
    
    def dfs(current_node, target, max_depth, path):
        current_len = len(path) - 1
        
        if current_node == target:
            all_paths.append(list(path))
            return
            
        if current_len >= max_depth:
            return
            
        for neighbor in graph.neighbors(current_node):
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, target, max_depth, path)
                path.pop()

    if u not in graph or v not in graph:
        return 0
        
    dfs(u, v, k, [u])
    
    if all_paths:
        print(f"Caminhos de '{u}' até '{v}' com comprimento <= {k}:")
        for i, p in enumerate(all_paths, 1):
            path_str = " -> ".join(map(str, p))
            print(f"  {i}. {path_str} (comprimento: {len(p)-1})")
    else:
        print(f"Nenhum caminho de '{u}' até '{v}' com comprimento <= {k} encontrado.")
        
    return len(all_paths)

def main():
    service = GraphService()
    
    if os.path.exists("grafo01.txt"):
        print("\n--- Testando com grafo01.txt (Não-direcionado) ---")
        service.load_from_file("grafo01.txt")
        count = modified_dfs_all_paths(service.graph, "A", "D", 2)
        print(f"Total de caminhos encontrados: {count}")
        
        count = modified_dfs_all_paths(service.graph, "A", "C", 3)
        print(f"Total de caminhos encontrados: {count}")

    if os.path.exists("digrafo01.txt"):
        print("\n--- Testando com digrafo01.txt (Direcionado) ---")
        service.load_from_file("digrafo01.txt")
        count = modified_dfs_all_paths(service.graph, "A", "D", 3)
        print(f"Total de caminhos encontrados: {count}")

if __name__ == "__main__":
    main()
