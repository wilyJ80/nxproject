# Projeto: grafos com `networkx`

- O projeto usa como código base o arquivo `codigobase.py`, mas implementa as versões finais no diretório `src/`

## Como rodar

- Instale `uv`:

    - `curl -LsSf https://astral.sh/uv/install.sh | sh`

- Instale as dependências:

    - `uv sync`

- Instale o projeto:

    - `uv pip install -e .`

- Rode o script da primeira tarefa com `uv run src/main.py` 

    - segunda tarefa (parte 1): `uv run src/main2.py`

    - segunda tarefa (parte 2): `uv run src/main3.py`

    - terceira tarefa: `uv run src/main4.py`

    - quarta tarefa (Dijkstra e Bellman-Ford): `uv run src/main5.py`

    - quinta tarefa (Kruskal): `uv run src/main6.py`

- ou os testes com `uv run pytest -s`

## Algoritmo de Kruskal (Tarefa 5)

O script `src/main6.py` implementa o **Algoritmo de Kruskal** para encontrar a Árvore Geradora Mínima (MST) de um grafo ponderado não-direcionado.

### Como usar

1. Execute o script: `uv run src/main6.py`
2. Informe o caminho do arquivo de grafo (ex: `test/kruskal_test_input.txt`).
3. Informe o caminho do arquivo de imagem de saída (ex: `output/mst.png`).

## Algoritmos de Menor Caminho (Tarefa 4)

O script `src/main5.py` implementa os algoritmos de **Dijkstra** e **Bellman-Ford** para encontrar o menor caminho entre dois vértices em um grafo ponderado.

### Como usar

1. Execute o script: `uv run src/main5.py`
2. Informe o caminho do arquivo de grafo (ex: `grafo_exemplo.txt`).
3. Informe o vértice de origem.
4. Informe o vértice de destino.

### Exemplo de Uso

Utilizando o arquivo `grafo_exemplo.txt`:
```
D W
A B 4
A C 2
B C 1
B D 5
C D 8
C E 10
D E 2
E F 3
```

**Execução:**
- Origem: `A`
- Destino: `F`
- **Resultado esperado:**
    - Menor caminho: `A -> B -> D -> E -> F` (pode variar se houver caminhos de mesmo custo, mas este é um deles)
    - Custo total: `14.0`

### Diferenças entre os Algoritmos

- **Dijkstra:** Mais eficiente, porém não suporta arestas com pesos negativos.
- **Bellman-Ford:** Suporta pesos negativos e é capaz de detectar ciclos negativos no grafo.

## Complexidade de Representações de Grafos

### 1. Matriz de Adjacência: $O(V^2)$
A matriz de adjacência é uma tabela $V \times V$ onde cada entrada `[i][j]` indica a presença (e o peso) de uma aresta entre os vértices $i$ e $j$.
- **Vantagem:** Verificação instantânea — complexidade $O(1)$ — para saber se existe uma conexão entre dois vértices específicos.
- **Desvantagem:** Ocupa sempre $O(V^2)$ de memória, independentemente do número de arestas. É ideal para **grafos densos** (onde o número de arestas $E$ se aproxima de $V^2$).

### 2. Lista de Adjacência: $O(V + E)$
Nesta representação, cada vértice mantém uma lista (ou dicionário) de seus vizinhos diretos.
- **Vantagem:** Extremamente eficiente em termos de memória, ocupando apenas $O(V + E)$. É a escolha padrão para a maioria dos algoritmos de travessia (como BFS e DFS).
- **Desvantagem:** Verificar a existência de uma aresta específica pode levar até $O(V)$ no pior caso. É a melhor escolha para **grafos esparsos**.

### 3. Matriz de Incidência: $O(V \cdot E)$
Uma matriz de dimensão $V \times E$ que relaciona cada vértice a cada aresta do grafo.
- **Vantagem:** Facilita a análise de propriedades estruturais onde a relação direta entre vértices e arestas é o foco (como em problemas de fluxo ou circuitos).
- **Desvantagem:** Pode consumir muita memória ($O(V \cdot E)$) em grafos grandes, tornando-se menos prática que a lista de adjacência para uso geral.
