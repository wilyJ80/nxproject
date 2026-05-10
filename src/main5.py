import networkx as nx
import heapq
import os
import sys
from main import GraphService

def dijkstra(graph, start, end):
    """
    Implementação do Algoritmo de Dijkstra para encontrar o menor caminho.
    Não aceita pesos negativos.
    """
    # Inicialização
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes()}
    
    # Fila de prioridade (distância, nó)
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Se já encontramos um caminho menor, ignoramos
        if current_distance > distances[current_node]:
            continue
            
        # Se chegamos ao destino, poderíamos parar, mas vamos processar normalmente
        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor].get('weight', 1.0)
            
            if weight < 0:
                raise ValueError("Dijkstra não suporta arestas com peso negativo.")
                
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    # Reconstrução do caminho
    path = []
    current = end
    if distances[end] == float('infinity'):
        return None, float('infinity')
        
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    
    return path[::-1], distances[end]

def bellman_ford(graph, start, end):
    """
    Implementação do Algoritmo de Bellman-Ford.
    Suporta pesos negativos e detecta ciclos negativos.
    """
    # Inicialização
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes()}
    
    nodes = list(graph.nodes())
    edges = list(graph.edges(data=True))
    
    # Relaxamento das arestas |V| - 1 vezes
    for _ in range(len(nodes) - 1):
        for u, v, data in edges:
            weight = data.get('weight', 1.0)
            if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                previous_nodes[v] = u
            
            # Se for não-direcionado, também relaxamos no outro sentido
            if not graph.is_directed():
                if distances[v] != float('infinity') and distances[v] + weight < distances[u]:
                    distances[u] = distances[v] + weight
                    previous_nodes[u] = v

    # Verificação de ciclos negativos
    for u, v, data in edges:
        weight = data.get('weight', 1.0)
        if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
            raise ValueError("O grafo contém um ciclo negativo.")
        if not graph.is_directed():
            if distances[v] != float('infinity') and distances[v] + weight < distances[u]:
                raise ValueError("O grafo contém um ciclo negativo.")

    # Reconstrução do caminho
    path = []
    current = end
    if distances[end] == float('infinity'):
        return None, float('infinity')
        
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
        
    return path[::-1], distances[end]

def main():
    service = GraphService()
    
    # Solicitar nome do arquivo
    file_path = input("Informe o caminho do arquivo de grafo: ").strip()
    if not file_path:
        # Fallback para exemplo se o usuário não digitar nada
        file_path = "grafo_exemplo.txt"
        
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return

    try:
        graph = service.load_from_file(file_path)
        print(f"Arquivo lido: {file_path}")
        print(f"Grafo criado ({'dígrafo' if service.is_directed else 'grafo'}, "
              f"{'ponderado' if service.is_weighted else 'não ponderado'}) com "
              f"{graph.number_of_nodes()} vértices e {graph.number_of_edges()} arestas.")
        
        origin = input("Informe o vértice de origem: ").strip()
        destination = input("Informe o vértice de destino: ").strip()
        
        if origin not in graph or destination not in graph:
            print("Erro: Vértice de origem ou destino não existe no grafo.")
            return

        print("\n--- Executando Dijkstra ---")
        try:
            path_d, cost_d = dijkstra(graph, origin, destination)
            if path_d:
                print(f"Menor caminho de {origin} até {destination}: {' -> '.join(path_d)}")
                print(f"Custo total: {cost_d}")
            else:
                print(f"Não existe caminho entre {origin} e {destination}.")
        except ValueError as e:
            print(f"Erro no Dijkstra: {e}")

        print("\n--- Executando Bellman-Ford ---")
        try:
            path_bf, cost_bf = bellman_ford(graph, origin, destination)
            if path_bf:
                print(f"Menor caminho de {origin} até {destination}: {' -> '.join(path_bf)}")
                print(f"Custo total: {cost_bf}")
            else:
                print(f"Não existe caminho entre {origin} e {destination}.")
        except ValueError as e:
            print(f"Erro no Bellman-Ford: {e}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
