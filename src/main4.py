import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

from main import GraphService

def kosaraju_scc(graph: nx.DiGraph):
    """
    Implementação do Algoritmo de Kosaraju-Sharir para identificar 
    Componentes Fortemente Conectadas (SCCs) em um dígrafo.
    
    Objetivo:
    O objetivo desta função é retornar uma lista de conjuntos, onde cada conjunto
    contém os vértices de uma Componente Fortemente Conectada.
    
    Estruturas Auxiliares:
    - visited: Conjunto para rastrear os vértices já visitados durante a DFS.
    - stack: Pilha para armazenar os vértices na ordem de finalização
    - transpose_graph: O dígrafo com todas as arestas invertidas
    - current_scc: Lista temporária para armazenar os vértices de uma SCC sendo descoberta
    """
    
    if not isinstance(graph, nx.DiGraph):
        raise ValueError("O algoritmo de Kosaraju-Sharir requer um dígrafo (nx.DiGraph).")

    # Visitamos todos os nós e os empilhamos conforme terminamos de explorar
    # todos os seus descendentes. Isso nos dá uma "ordenação topológica" parcial.
    
    visited = set()
    stack = []

    def fill_order(v):
        """Função recursiva de DFS para preencher a pilha com a ordem de finalização."""
        visited.add(v)
        # Exploramos todos os sucessores de v no grafo original
        for neighbor in graph.neighbors(v):
            if neighbor not in visited:
                fill_order(neighbor)
        # Ao terminar de explorar v e seus descendentes, adicionamos v à pilha
        stack.append(v)

    # Garantimos que todos os nós sejam processados, mesmo em grafos desconexos
    for node in graph.nodes():
        if node not in visited:
            fill_order(node)

    # Invertemos o sentido de todas as arestas. As SCCs em G são as mesmas em G^T.
    
    transpose_graph = nx.DiGraph()
    # Adicionamos todos os nós originais (garante consistência para nós isolados)
    transpose_graph.add_nodes_from(graph.nodes())
    # Invertemos as arestas
    for u, v in graph.edges():
        transpose_graph.add_edge(v, u)

    # Processamos os vértices de acordo com o topo da pilha (maior tempo de finalização).
    # Cada árvore gerada nesta DFS corresponde exatamente a uma SCC.
    
    visited = set()
    sccs = []

    def dfs_transpose(v, current_scc_list):
        """Função recursiva de DFS para identificar os componentes no grafo transposto."""
        visited.add(v)
        current_scc_list.append(v)
        for neighbor in transpose_graph.neighbors(v):
            if neighbor not in visited:
                dfs_transpose(neighbor, current_scc_list)

    # Enquanto houver elementos na pilha de finalização
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            dfs_transpose(node, component)
            # Salvamos a componente encontrada como um conjunto (set)
            sccs.append(set(component))

    return sccs

def main():
    service = GraphService()
    
    # Tentativa de carregar o arquivo digrafo01.txt
    file_path = "digrafo01.txt"
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(__file__), "..", "digrafo01.txt")

    try:
        print(f"Lendo dígrafo de: {file_path}")
        graph = service.load_from_file(file_path)
        
        if not service.is_directed:
            print("Erro: O arquivo não contém um dígrafo. Kosaraju requer um dígrafo.")
            return

        print("\nIniciando algoritmo de Kosaraju-Sharir...")
        sccs = kosaraju_scc(graph)
        
        print(f"\nForam encontradas {len(sccs)} Componentes Fortemente Conectadas:")
        for i, scc in enumerate(sccs, 1):
            print(f" SCC {i}: {sorted(list(scc))}")

        # Verificação com NetworkX para fins de validação
        nx_sccs = list(nx.strongly_connected_components(graph))
        print(f"\nValidação com NetworkX:")
        print(f" SCCs do NetworkX: {[sorted(list(s)) for s in nx_sccs]}")
        
        if len(sccs) == len(nx_sccs):
            print("\nSUCESSO: O número de SCCs coincide com a implementação do NetworkX.")
        else:
            print("\nAVISO: O número de SCCs diverge do NetworkX.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
