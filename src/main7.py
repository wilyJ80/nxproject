import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
from main import GraphService

def hungarian_algorithm(cost_matrix):
    """
    Implementação manual do Algoritmo Húngaro para encontrar o emparelhamento de custo mínimo.
    Assume que a matriz de custos é quadrada.
    """
    cost_matrix = np.array(cost_matrix, dtype=float)
    n = cost_matrix.shape[0]
    
    # 1. Subtrair o mínimo de cada linha
    matrix = cost_matrix - cost_matrix.min(axis=1)[:, np.newaxis]
    
    # 2. Subtrair o mínimo de cada coluna
    matrix = matrix - matrix.min(axis=0)
    
    def find_min_lines(mat):
        # Encontra o número mínimo de linhas para cobrir todos os zeros
        zeros = np.argwhere(mat == 0)
        n = mat.shape[0]
        
        row_covered = np.zeros(n, dtype=bool)
        col_covered = np.zeros(n, dtype=bool)
        
        # 1. Encontrar um emparelhamento máximo nos zeros
        matching = {} # col -> row
        
        def can_match(u, visited):
            for v in range(n):
                if mat[u, v] == 0 and not visited[v]:
                    visited[v] = True
                    if v not in matching or can_match(matching[v], visited):
                        matching[v] = u
                        return True
            return False

        for i in range(n):
            can_match(i, np.zeros(n, dtype=bool))
            
        # Linhas não emparelhadas
        marked_rows = np.ones(n, dtype=bool)
        for v in matching:
            marked_rows[matching[v]] = False
            
        marked_cols = np.zeros(n, dtype=bool)
        
        changed = True
        while changed:
            changed = False
            # Se uma linha está marcada, marque todas as colunas com zeros nela
            for r in range(n):
                if marked_rows[r]:
                    for c in range(n):
                        if mat[r, c] == 0 and not marked_cols[c]:
                            marked_cols[c] = True
                            changed = True
            
            # se uma coluna está marcada, marque a linha emparelhada com ela
            for c in range(n):
                if marked_cols[c] and c in matching:
                    r = matching[c]
                    if not marked_rows[r]:
                        marked_rows[r] = True
                        changed = True
        
        # Cobertura: linhas NÃO marcadas e colunas marcadas
        rows = np.where(~marked_rows)[0]
        cols = np.where(marked_cols)[0]
        
        return rows, cols, matching

    while True:
        rows, cols, matching = find_min_lines(matrix)
        
        if len(rows) + len(cols) == n:
            # Encontramos o emparelhamento ótimo
            # Re-executar o emparelhamento máximo para garantir que temos n pares
            final_matching = [None] * n
            for col, row in matching.items():
                final_matching[row] = col
            return final_matching
        
        # 3. Ajustar a matriz
        # Encontrar o menor valor não coberto
        mask = np.ones((n, n), dtype=bool)
        mask[rows, :] = False
        mask[:, cols] = False
        
        min_uncovered = np.min(matrix[mask])
        
        # Subtrair de linhas não cobertas
        matrix[~np.isin(np.arange(n), rows), :] -= min_uncovered
        # Adicionar a colunas cobertas
        matrix[:, cols] += min_uncovered

def get_bipartite_sets(graph):
    """
    Identifica os dois conjuntos de vértices de um grafo bipartido.
    """
    if not nx.is_bipartite(graph):
        raise ValueError("O grafo fornecido não é bipartido.")
    
    sets = nx.bipartite.sets(graph)
    # Retornar como listas ordenadas
    u_set = sorted(list(sets[0]))
    v_set = sorted(list(sets[1]))
    
    return u_set, v_set

def solve_assignment(graph):
    """
    Prepara a matriz de custos e resolve usando o algoritmo húngaro.
    """
    u_set, v_set = get_bipartite_sets(graph)
    
    n = max(len(u_set), len(v_set))
    # Para o algoritmo húngaro clássico, precisamos de uma matriz quadrada.
    cost_matrix = np.full((n, n), 1e9) # Valor alto para arestas inexistentes
    
    u_map = {node: i for i, node in enumerate(u_set)}
    v_map = {node: i for i, node in enumerate(v_set)}
    
    for u, v, data in graph.edges(data=True):
        if u in u_map and v in v_map:
            cost_matrix[u_map[u], v_map[v]] = data.get('weight', 0)
        elif v in u_map and u in v_map:
            cost_matrix[u_map[v], v_map[u]] = data.get('weight', 0)
            
    assignment = hungarian_algorithm(cost_matrix)
    
    matching_edges = []
    total_cost = 0
    
    for u_idx, v_idx in enumerate(assignment):
        if u_idx < len(u_set) and v_idx < len(v_set):
            u_node = u_set[u_idx]
            v_node = v_set[v_idx]
            if graph.has_edge(u_node, v_node):
                weight = graph[u_node][v_node]['weight']
                matching_edges.append((u_node, v_node, weight))
                total_cost += weight
                
    return matching_edges, total_cost

def visualize_hungarian(graph, matching_edges, output_path="hungarian_result.png"):
    plt.figure(figsize=(12, 10))
    
    u_set, v_set = get_bipartite_sets(graph)
    pos = {}
    
    # Posicionamento bipartido
    for i, node in enumerate(u_set):
        pos[node] = (0, -i)
    for i, node in enumerate(v_set):
        pos[node] = (1, -i)
        
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color='lightblue', alpha=0.9)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif', font_weight='bold')
    
    matching_set = set()
    for u, v, w in matching_edges:
        matching_set.add(tuple(sorted((u, v))))
        
    normal_edges = []
    blue_edges = []
    
    for u, v in graph.edges():
        if tuple(sorted((u, v))) in matching_set:
            blue_edges.append((u, v))
        else:
            normal_edges.append((u, v))
            
    nx.draw_networkx_edges(graph, pos, edgelist=normal_edges, edge_color='lightgray', width=1, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, edgelist=blue_edges, edge_color='blue', width=4, alpha=1.0)
    
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    
    plt.title("Emparelhamento Ótimo (Algoritmo Húngaro)")
    plt.axis('off')
    
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    plt.savefig(output_path)
    print(f"Imagem salva em: {output_path}")
    plt.close()

def main():
    service = GraphService()
    
    input_file = input("Informe o caminho do arquivo de grafo bipartido: ").strip()
    if not input_file:
        input_file = "test/hungarian_test_input.txt"
        
    output_image = input("Informe o nome do arquivo de imagem de saída (ex: matching.png): ").strip()
    if not output_image:
        output_image = "output/hungarian_matching.png"

    if not os.path.exists(input_file):
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        return

    try:
        graph = service.load_from_file(input_file)
        
        print(f"Processando grafo bipartido com {graph.number_of_nodes()} vértices e {graph.number_of_edges()} arestas.")
        
        matching_edges, total_cost = solve_assignment(graph)
        
        print("\n--- Emparelhamento Ótimo (Algoritmo Húngaro Manual) ---")
        for u, v, w in matching_edges:
            print(f"Aresta: {u} - {v}, Peso: {w}")
        print(f"Custo total: {total_cost}")
        
        # Validar com NetworkX
        u_set, v_set = get_bipartite_sets(graph)
        try:
            nx_matching = nx.bipartite.matching.minimum_weight_full_matching(graph, top_nodes=u_set)
            nx_total_cost = sum(graph[u][v]['weight'] for u, v in nx_matching.items()) / 2
            print(f"\nValidação NetworkX - Custo total: {nx_total_cost}")
            
            if abs(total_cost - nx_total_cost) < 1e-9:
                print("Sucesso! A implementação manual coincide com o resultado do NetworkX.")
            else:
                print("Atenção: Os custos totais divergem.")
        except Exception as e:
            print(f"\nNão foi possível validar com NetworkX: {e}")
            
        visualize_hungarian(graph, matching_edges, output_image)
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
