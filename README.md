# Projeto: grafos com `networkx`

- O projeto usa como código base o arquivo `codigobase.py`, mas implementa a versão final em `src/main.py`

## Como rodar

- Instale `uv`:

    - `curl -LsSf https://astral.sh/uv/install.sh | sh`

- Instale as dependências:

    - `uv sync`

- Instale o projeto:

    - `uv pip install -e .`

- Rode o script com `uv run src/main.py` ou os testes com `uv run pytest -s`

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
