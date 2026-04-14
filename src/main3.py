import networkx as nx
import os
from main import GraphService

def verify_sequence(graph, S):
    results = {
        "is_walk": False,
        "is_path": False,
        "is_trail": False,
        "is_circuit": False
    }
    
    if not S:
        return results
        
    if len(S) == 1:
        if S[0] in graph:
            results["is_walk"] = True
            results["is_path"] = True
            results["is_trail"] = True
            results["is_circuit"] = False 
        return results

    edges_used = []
    for i in range(len(S) - 1):
        u, v = S[i], S[i+1]
        if not graph.has_edge(u, v):
            return results 
            
        if graph.is_directed():
            edges_used.append((u, v))
        else:
            edges_used.append(tuple(sorted((u, v))))
            
    results["is_walk"] = True
    
    if len(S) == len(set(S)):
        results["is_path"] = True
        
    if len(edges_used) == len(set(edges_used)):
        results["is_trail"] = True
        
    if results["is_trail"] and S[0] == S[-1] and len(S) > 1:
        results["is_circuit"] = True
        
    return results

def display_results(sequence, results):
    print(f"\nSequência: {sequence}")
    if not results["is_walk"]:
        print("  - Não é um passeio válido (arestas faltando).")
        return
        
    status = []
    if results["is_walk"]: status.append("Passeio")
    if results["is_path"]: status.append("Caminho (Simples)")
    if results["is_trail"]: status.append("Trilha")
    if results["is_circuit"]: status.append("Circuito")
    
    print(f"  - Resultados: {', '.join(status)}")

def main():
    service = GraphService()
    
    if os.path.exists("grafo01.txt"):
        print("\n--- Testando com grafo01.txt (Não-direcionado) ---")
        service.load_from_file("grafo01.txt")
        
        sequences = [
            ["A", "B", "C", "D"],       
            ["A", "B", "D", "A"],      
            ["A", "B", "C", "B", "D"],
            ["A", "B", "A"],         
            ["A", "E", "C"]         
        ]
        
        for s in sequences:
            res = verify_sequence(service.graph, s)
            display_results(s, res)

    if os.path.exists("digrafo01.txt"):
        print("\n--- Testando com digrafo01.txt (Direcionado) ---")
        service.load_from_file("digrafo01.txt")
        
        sequences = [
            ["A", "B", "C", "D"],       
            ["D", "A", "B", "D"],       
            ["B", "D", "A", "B", "C"]   
        ]
        
        for s in sequences:
            res = verify_sequence(service.graph, s)
            display_results(s, res)

if __name__ == "__main__":
    main()
