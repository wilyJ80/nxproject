Descrição
Implemente um programa em Python que leia de um arquivo de entrada um grafo ponderado e determine sua árvore geradora mínima (MST) utilizando o algoritmo de Kruskal.
O programa deve gerar uma imagem do grafo, destacando em azul as arestas pertencentes à MST.

Requisitos
O programa deve ler o grafo a partir de um arquivo texto com o seguinte formato:

Primeira linha: dois caracteres

'G' ou 'D' → indica se é grafo ou dígrafo (para esta tarefa, apenas 'G' será considerado);

'W' → indica que o grafo é ponderado.

Linhas seguintes: arestas no formato

u v w
onde u e v são vértices e w é o peso da aresta.

O programa deve:

Construir o grafo em Python usando networkx;

Calcular a árvore geradora mínima com o algoritmo de Kruskal;

Exibir e salvar a figura do grafo com:

Arestas da MST em azul;

Demais arestas em cinza;

Pesos das arestas visíveis no gráfico.

O nome do arquivo de entrada e o nome da imagem de saída devem ser informados pelo usuário.

Exemplo de entrada
G W A B 4 A C 3 B C 2 B D 5 C D 7
Saída esperada
Exibição gráfica do grafo, com as arestas da MST destacadas em azul;

Critérios de Avaliação
(4 pts) Correção da implementação do algoritmo de Kruskal

(1 pts) Leitura correta do arquivo de entrada

(2 pts) Visualização gráfica adequada (arestas da MST destacadas)

(3 pts) Clareza, organização, e comentários no código
