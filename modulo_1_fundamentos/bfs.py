"""
BFS (BUSCA EM LARGURA) - Framework Fundamental
Complexidade Temporal: O(V + E) onde V = vértices, E = arestas
Complexidade Espacial: O(V) para a fila

Intuição:
BFS explora o grafo camada por camada, garantindo que encontremos
o caminho mais curto em grafos não ponderados. É ideal para:
1. Menor caminho em grafos não ponderados
2. Exploração por níveis
3. Problemas que requerem distância mínima
"""

from collections import deque


def bfs_basico(grafo, inicio):
    """
    BFS básico para explorar todos os nós alcançáveis.

    Args:
        grafo: Dicionário onde chaves são nós e valores são listas de vizinhos
        inicio: Nó inicial

    Returns:
        list: Lista de nós na ordem de visitação BFS

    Exemplo:
        grafo = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }
        bfs_basico(grafo, 'A') → ['A', 'B', 'C', 'D', 'E', 'F']
    """
    if inicio not in grafo:
        return []

    visitados = set()
    fila = deque([inicio])
    resultado = []

    while fila:
        no_atual = fila.popleft()

        if no_atual not in visitados:
            visitados.add(no_atual)
            resultado.append(no_atual)

            # Adicionar vizinhos não visitados à fila
            for vizinho in grafo.get(no_atual, []):
                if vizinho not in visitados:
                    fila.append(vizinho)

    return resultado


def menor_caminho_bfs(grafo, inicio, destino):
    """
    Encontra o menor caminho entre dois nós usando BFS.

    Args:
        grafo: Dicionário representando o grafo
        inicio: Nó inicial
        destino: Nó destino

    Returns:
        list: Caminho mais curto ou [] se não existe caminho

    Retorna o caminho completo, não apenas a distância.
    """
    if inicio == destino:
        return [inicio]

    if inicio not in grafo or destino not in grafo:
        return []

    visitados = set()
    fila = deque([(inicio, [inicio])])  # (nó_atual, caminho_até_aqui)

    while fila:
        no_atual, caminho = fila.popleft()

        if no_atual in visitados:
            continue

        visitados.add(no_atual)

        for vizinho in grafo.get(no_atual, []):
            if vizinho == destino:
                return caminho + [vizinho]

            if vizinho not in visitados:
                fila.append((vizinho, caminho + [vizinho]))

    return []  # Não existe caminho


def bfs_matriz_grid(matriz, inicio, destino):
    """
    BFS em matriz 2D (grid) para encontrar menor caminho.

    Args:
        matriz: Matriz 2D onde 0 = livre, 1 = bloqueado
        inicio: Tupla (linha, coluna) da posição inicial
        destino: Tupla (linha, coluna) da posição destino

    Returns:
        int: Distância mínima ou -1 se não há caminho

    Movimentos permitidos: cima, baixo, esquerda, direita
    """
    if not matriz or not matriz[0]:
        return -1

    linhas, colunas = len(matriz), len(matriz[0])

    # Verificar se início e destino são válidos
    if (
        inicio[0] < 0
        or inicio[0] >= linhas
        or inicio[1] < 0
        or inicio[1] >= colunas
        or destino[0] < 0
        or destino[0] >= linhas
        or destino[1] < 0
        or destino[1] >= colunas
        or matriz[inicio[0]][inicio[1]] == 1
        or matriz[destino[0]][destino[1]] == 1
    ):
        return -1

    if inicio == destino:
        return 0

    # Direções: cima, baixo, esquerda, direita
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    visitados = set()
    fila = deque([(inicio[0], inicio[1], 0)])  # (linha, coluna, distância)

    while fila:
        linha, coluna, distancia = fila.popleft()

        if (linha, coluna) in visitados:
            continue

        visitados.add((linha, coluna))

        # Explorar vizinhos
        for dx, dy in direcoes:
            nova_linha, nova_coluna = linha + dx, coluna + dy

            # Verificar limites e se é livre
            if (
                0 <= nova_linha < linhas
                and 0 <= nova_coluna < colunas
                and matriz[nova_linha][nova_coluna] == 0
                and (nova_linha, nova_coluna) not in visitados
            ):

                if (nova_linha, nova_coluna) == destino:
                    return distancia + 1

                fila.append((nova_linha, nova_coluna, distancia + 1))

    return -1


def bfs_multi_origem(grafo, origens):
    """
    BFS com múltiplas origens simultaneamente.
    Útil para problemas como propagação de infecção, pintura, etc.

    Args:
        grafo: Dicionário representando o grafo
        origens: Lista de nós iniciais

    Returns:
        dict: Dicionário com distância mínima de cada nó para qualquer origem

    Exemplo:
        Useful para: "tempo mínimo para infectar toda a rede"
    """
    if not origens:
        return {}

    visitados = set()
    fila = deque()
    distancias = {}

    # Inicializar com todas as origens
    for origem in origens:
        if origem in grafo:
            fila.append((origem, 0))
            distancias[origem] = 0

    while fila:
        no_atual, distancia = fila.popleft()

        if no_atual in visitados:
            continue

        visitados.add(no_atual)

        for vizinho in grafo.get(no_atual, []):
            if vizinho not in visitados and vizinho not in distancias:
                distancias[vizinho] = distancia + 1
                fila.append((vizinho, distancia + 1))

    return distancias


def bfs_por_niveis(grafo, inicio):
    """
    BFS que processa nós nível por nível.
    Útil quando você precisa saber exatamente em qual nível cada nó está.

    Args:
        grafo: Dicionário representando o grafo
        inicio: Nó inicial

    Returns:
        list: Lista de listas, onde cada sublista contém nós de um nível

    Exemplo:
        Resultado: [[nível_0], [nível_1], [nível_2], ...]
    """
    if inicio not in grafo:
        return []

    visitados = set()
    fila = deque([inicio])
    resultado = []

    while fila:
        nivel_atual = []
        tamanho_nivel = len(fila)

        # Processar todos os nós do nível atual
        for _ in range(tamanho_nivel):
            no_atual = fila.popleft()

            if no_atual not in visitados:
                visitados.add(no_atual)
                nivel_atual.append(no_atual)

                # Adicionar vizinhos para o próximo nível
                for vizinho in grafo.get(no_atual, []):
                    if vizinho not in visitados:
                        fila.append(vizinho)

        if nivel_atual:
            resultado.append(nivel_atual)

    return resultado


def labirinto_menor_caminho(labirinto):
    """
    Encontra o menor caminho em um labirinto de 'S' (start) para 'E' (end).

    Args:
        labirinto: Matriz de caracteres onde:
                  'S' = início, 'E' = fim, '.' = livre, '#' = parede

    Returns:
        int: Número mínimo de passos ou -1 se impossível
    """
    if not labirinto or not labirinto[0]:
        return -1

    linhas, colunas = len(labirinto), len(labirinto[0])
    inicio = fim = None

    # Encontrar posições de início e fim
    for i in range(linhas):
        for j in range(colunas):
            if labirinto[i][j] == "S":
                inicio = (i, j)
            elif labirinto[i][j] == "E":
                fim = (i, j)

    if not inicio or not fim:
        return -1

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visitados = set()
    fila = deque([(inicio[0], inicio[1], 0)])

    while fila:
        linha, coluna, passos = fila.popleft()

        if (linha, coluna) == fim:
            return passos

        if (linha, coluna) in visitados:
            continue

        visitados.add((linha, coluna))

        for dx, dy in direcoes:
            nova_linha, nova_coluna = linha + dx, coluna + dy

            if (
                0 <= nova_linha < linhas
                and 0 <= nova_coluna < colunas
                and (nova_linha, nova_coluna) not in visitados
                and labirinto[nova_linha][nova_coluna] != "#"
            ):

                fila.append((nova_linha, nova_coluna, passos + 1))

    return -1


def ilhas_conectadas(grid):
    """
    Conta o número de ilhas em um grid binário.
    Uma ilha é formada por 1s conectados horizontalmente ou verticalmente.

    Args:
        grid: Matriz binária onde 1 = terra, 0 = água

    Returns:
        int: Número de ilhas
    """
    if not grid or not grid[0]:
        return 0

    linhas, colunas = len(grid), len(grid[0])
    visitados = set()
    num_ilhas = 0

    def bfs_ilha(start_linha, start_coluna):
        """BFS para marcar toda a ilha como visitada"""
        fila = deque([(start_linha, start_coluna)])
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while fila:
            linha, coluna = fila.popleft()

            if (linha, coluna) in visitados:
                continue

            visitados.add((linha, coluna))

            for dx, dy in direcoes:
                nova_linha, nova_coluna = linha + dx, coluna + dy

                if (
                    0 <= nova_linha < linhas
                    and 0 <= nova_coluna < colunas
                    and grid[nova_linha][nova_coluna] == 1
                    and (nova_linha, nova_coluna) not in visitados
                ):

                    fila.append((nova_linha, nova_coluna))

    # Procurar por ilhas
    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j] == 1 and (i, j) not in visitados:
                bfs_ilha(i, j)
                num_ilhas += 1

    return num_ilhas


# Exemplos de uso e testes
if __name__ == "__main__":
    # Teste 1: BFS básico
    print("Teste 1 - BFS Básico:")
    grafo1 = {"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"], "D": ["B"], "E": ["B", "F"], "F": ["C", "E"]}
    resultado = bfs_basico(grafo1, "A")
    print(f"BFS a partir de 'A': {resultado}")
    print()

    # Teste 2: Menor caminho
    print("Teste 2 - Menor Caminho:")
    caminho = menor_caminho_bfs(grafo1, "A", "F")
    print(f"Caminho de A para F: {caminho}")
    print()

    # Teste 3: BFS em matriz
    print("Teste 3 - BFS em Matriz:")
    matriz = [[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0]]
    distancia = bfs_matriz_grid(matriz, (0, 0), (3, 3))
    print(f"Matriz:")
    for linha in matriz:
        print(f"  {linha}")
    print(f"Distância de (0,0) para (3,3): {distancia}")
    print()

    # Teste 4: Labirinto
    print("Teste 4 - Labirinto:")
    labirinto = [["S", ".", "#", "."], [".", "#", ".", "."], [".", ".", ".", "#"], ["#", ".", ".", "E"]]
    passos = labirinto_menor_caminho(labirinto)
    print(f"Labirinto:")
    for linha in labirinto:
        print(f"  {linha}")
    print(f"Menor caminho S → E: {passos} passos")
    print()

    # Teste 5: Contar ilhas
    print("Teste 5 - Contar Ilhas:")
    grid_ilhas = [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]]
    num_ilhas = ilhas_conectadas(grid_ilhas)
    print(f"Grid:")
    for linha in grid_ilhas:
        print(f"  {linha}")
    print(f"Número de ilhas: {num_ilhas}")  # Esperado: 3
