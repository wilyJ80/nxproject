Emparelhamento pelo Algoritmo Húngaro
Data de conclusão 29 de junho de 2026 às 23:59
•
Fecha 29 de junho de 2026 às 23:59
Instruções
Implemente um programa em Python que resolva o problema de emparelhamento ótimo em grafos bipartidos ponderados utilizando o Algoritmo Húngaro (Hungarian Algorithm).
O programa deve ler uma grafo bipartido ponderado, e retornar o emparelhamento de custo mínimo, exibindo também o custo total da solução.

Requisitos
O programa deve ler o grafo a partir de um arquivo texto com o seguinte formato:

Linhas: arestas no formato u v w; onde u e v são vértices e w é o peso da aresta.

O programa deve:

Construir o grafo em Python usando networkx;

Construir a matriz de custos;

Aplicar o Algoritmo Húngaro para encontrar o emparelhamento ótimo (mínimo custo total);

Exibir e salvar a figura do grafo com:

Arestas do emparelhamento em azul;

Demais arestas em cinza;

Pesos das arestas visíveis no gráfico.

É permitido o uso da biblioteca scipy (scipy.optimize.linear_sum_assignment) ou a implementação manual do algoritmo.


Critérios de Avaliação
(4 pts) Implementação correta do algoritmo Húngaro (ou uso apropriado da função equivalente)

(3 pts) Visualização final clara, com emparelhamentos e custo total

(2 pts) Organização, clareza e modularização do código

(1 pt) Comentários


