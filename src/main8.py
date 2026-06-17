import networkx as nx
import matplotlib.pyplot as plt
import os
from main import GraphService

def check_planarity_boyer_myrvold(G):
    """
    Realiza o teste de planaridade utilizando o algoritmo de Boyer-Myrvold.
    A função retorna (is_planar, result).
    is_planar True, result objeto PlanarEmbedding.
    is_planar False, result subgrafo de Kuratowski (K5 ou K3,3).
    """
    is_planar, result = nx.check_planarity(G, counterexample=True)
    return is_planar, result

def visualize_planar_embedding(G, embedding, output_path):
    # Converte o embedding combinatório em coordenadas (posições) para desenho
    pos = nx.combinatorial_embedding_to_pos(embedding)
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', 
            edge_color='gray', node_size=800, font_size=12, font_weight='bold')
    
    plt.title("Embedding Planar (Boyer-Myrvold)")
    
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    plt.savefig(output_path)
    plt.close()
    print(f"Embedding planar salvo em: {output_path}")

def main():
    service = GraphService()
    
    input_file = input("Informe o caminho do arquivo de grafo: ").strip()
    if not input_file:
        input_file = "grafo01.txt"
        
    if not os.path.exists(input_file):
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        return

    try:
        G = service.load_from_file(input_file)
        print(f"Grafo carregado: {G.number_of_nodes()} vértices e {G.number_of_edges()} arestas.")
        
        is_planar, result = check_planarity_boyer_myrvold(G)
        
        if is_planar:
            print("O grafo é planar.")
            
            output_image = input("Informe o nome do arquivo de imagem de saída (ex: output/planar.png): ").strip()
            if not output_image:
                output_image = "output/planar_embedding.png"
                
            # extração de embedding
            visualize_planar_embedding(G, result, output_image)
        else:
            print("O grafo NÃO é planar.")
            
            # extração de Kuratowski
            print("\nSubgrafo de Kuratowski identificado:")
            print(f"Vértices: {sorted(list(result.nodes()))}")
            print(f"Arestas: {list(result.edges())}")
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
