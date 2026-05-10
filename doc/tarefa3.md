::::::::::::::::::::::::::::: u-flex-row-start__HJsCs
:::::::::::::::::::::::: assignment-details-left-pane__vs74O
# Algoritmos de Dijkstra e de Bellman-Ford {#algoritmos-de-dijkstra-e-de-bellman-ford .assignment-title__ZavFH .assignment-title-large__iDiT2 test="assignment-title"}

### Objetivo {#objetivo data-start="196" end="208"}

Implementar um programa em Python que leia de um arquivo texto a
definição de um grafo ponderado e, dados dois vértices de entrada,
calcule e exiba o menor caminho entre eles utilizando o **Algoritmo de
Dijkstra**. Repita o mesmo processo utilizando o **Algoritmo de
Bellman-Ford **aceitando, neste segundo caso, arestas com peso negativo.

### Especificação {#especificação data-start="425" end="442"}

1.  **Formato de entrada (arquivo texto):**

    -   Primeira linha: G W ou D W

        -   G indica grafo não direcionado

        -   D indica dígrafo

        -   W indica grafo ponderado (pesos inteiros ou reais)

    -   Demais linhas: cada linha representa uma aresta no formato:

        <div>

        <div>

        <div>

        <div>

        </div>

        </div>

        </div>

        <div>

        u v w

        </div>

        </div>

        onde u e v são vértices, e w é o peso da aresta (número inteiro
        ou real).

2.  **Entradas adicionais:**

    -   Após a leitura do arquivo, o programa deve solicitar ao usuário
        dois vértices:

        -   origem

        -   destino

3.  **Saída esperada:**

    -   Os programas devem calcular o **menor caminho** de origem até
        destino pelos algoritmos de **Dijkstra** [e]{data-start="1102"
        end="1114"} **Bellman-Ford.**[ ]{data-start="1102" end="1114"}

    -   Exibir na tela:

        -   O **custo total** do caminho.

        -   A **sequência de vértices** do caminho encontrado.

    -   Caso não exista caminho entre os dois vértices, o programa deve
        informar ao usuário.

    -   ::: {data-start="1243" end="1327" style="margin-top:0px;margin-bottom:0px;"}
        [Caso existam ciclos negativos ao executar o Algoritmo de
        Bellman-Ford, informar ao
        usuário.]{style="display:inline!important"}\
        :::

4.  **Exemplo de arquivo de entrada (grafo_exemplo.txt):**

    <div>

    <div>

    <div>

    <div>

    </div>

    </div>

    </div>

    <div>

    D W A B 4 A C 2 B C 1 B D 5 C D 8 C E 10 D E 2 E F 3

    </div>

    </div>

5.  **Exemplo de execução:**

    <div>

    <div>

    <div>

    <div>

    </div>

    </div>

    </div>

    <div>

    Arquivo lido: grafo_exemplo.txt Grafo criado (dígrafo, ponderado)
    com 6 vértices e 8 arestas. Informe o vértice de origem: A Informe o
    vértice de destino: F Menor caminho de A até F: A -\> C -\> B -\> D
    -\> E -\> F Custo total: 15

    </div>

    </div>

### Requisitos {#requisitos data-start="1775" end="1789"}

-   O código deve seguir a mesma estrutura utilizada nas aulas práticas:

    -   Uso da biblioteca **NetworkX** para representar o grafo.

    -   Funções para leitura do grafo a partir do arquivo, adição de
        vértices/arestas e execução do algoritmo.

    -   Visualização opcional do grafo com o caminho destacado
        (diferenciando arestas do menor caminho em cor, se desejado).

    -   Não poderão ser utilizadas as funções **nx.shortest_path(),
        nx.dijkstra_path(), nx.bellman_ford_path(), nx.astar_path()**, e
        derivações das mesmas.

### Entrega {#entrega data-start="2159" end="2170"}

<div>

-   Código Python documentado.

-   Arquivo(s) de entrada de exemplo.

-   Um arquivo README.md explicando como executar o programa e
    apresentando pelo menos um exemplo de uso para cada algoritmo.

\

</div>

<div>

### Critérios de Avaliação {#critérios-de-avaliação data-start="2159" end="2170" style="box-sizing:border-box;scroll-margin-top:-5rem"}

</div>

-   [Implementação correta (40%)]{data-start="141" end="172"}

-   [Atendimento aos requisitos (20%)]{data-start="271" end="313"}

-   [Saída e clareza dos resultados (20%)]{data-start="392" end="432"}

-   [Organização e Documentação do código (15%)]{data-start="500"
    end="531"}

-   [Testes e exemplos (5%)]{data-start="593" end="619"}
