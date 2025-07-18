"""
BACKTRACKING - Template Universal
Complexidade Temporal: Exponencial (depende do problema)
Complexidade Espacial: O(profundidade da recursão)

Intuição:
Backtracking é uma técnica para explorar sistematicamente todas as possibilidades
de uma solução, desfazendo escolhas que não levam a soluções válidas.

Framework Fundamental:
1. Escolha: fazer uma escolha
2. Explorar: recursivamente explorar com essa escolha
3. Desfazer: desfazer a escolha (backtrack)
"""


def template_backtracking(caminho, opcoes, resultado):
    """
    Template genérico para problemas de backtracking.

    Args:
        caminho: Solução parcial atual
        opcoes: Opções disponíveis para a próxima escolha
        resultado: Lista para armazenar todas as soluções

    Estrutura básica:
    if condicao_de_parada(caminho):
        resultado.append(caminho.copy())
        return

    for opcao in opcoes:
        # Fazer escolha
        caminho.append(opcao)

        # Explorar recursivamente
        backtrack(caminho, novas_opcoes, resultado)

        # Desfazer escolha
        caminho.pop()
    """
    pass


def gerar_permutacoes(nums):
    """
    Gera todas as permutações de uma lista de números.

    Args:
        nums: Lista de números únicos

    Returns:
        list: Lista de todas as permutações

    Complexidade: O(n! * n) tempo, O(n) espaço (sem contar output)

    Exemplo:
        nums = [1, 2, 3]
        Retorna: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
    """
    resultado = []

    def backtrack(caminho):
        # Condição de parada: permutação completa
        if len(caminho) == len(nums):
            resultado.append(caminho[:])  # Cópia do caminho
            return

        # Explorar todas as opções
        for num in nums:
            if num not in caminho:  # Evitar duplicatas na permutação
                # Fazer escolha
                caminho.append(num)

                # Explorar recursivamente
                backtrack(caminho)

                # Desfazer escolha
                caminho.pop()

    backtrack([])
    return resultado


def gerar_combinacoes(n, k):
    """
    Gera todas as combinações de k números de 1 a n.

    Args:
        n: Número máximo
        k: Tamanho da combinação

    Returns:
        list: Lista de todas as combinações

    Exemplo:
        n = 4, k = 2
        Retorna: [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
    """
    resultado = []

    def backtrack(inicio, caminho):
        # Condição de parada: combinação do tamanho correto
        if len(caminho) == k:
            resultado.append(caminho[:])
            return

        # Explorar números de inicio até n
        for i in range(inicio, n + 1):
            # Fazer escolha
            caminho.append(i)

            # Explorar recursivamente (i+1 para evitar repetição)
            backtrack(i + 1, caminho)

            # Desfazer escolha
            caminho.pop()

    backtrack(1, [])
    return resultado


def gerar_subconjuntos(nums):
    """
    Gera todos os subconjuntos (power set) de uma lista.

    Args:
        nums: Lista de números únicos

    Returns:
        list: Lista de todos os subconjuntos

    Exemplo:
        nums = [1, 2, 3]
        Retorna: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
    """
    resultado = []

    def backtrack(inicio, caminho):
        # Cada chamada representa um subconjunto válido
        resultado.append(caminho[:])

        # Explorar adicionando cada elemento restante
        for i in range(inicio, len(nums)):
            # Fazer escolha
            caminho.append(nums[i])

            # Explorar recursivamente
            backtrack(i + 1, caminho)

            # Desfazer escolha
            caminho.pop()

    backtrack(0, [])
    return resultado


def resolver_n_rainhas(n):
    """
    Resolve o problema das N-Rainhas.

    Args:
        n: Tamanho do tabuleiro (n x n)

    Returns:
        list: Lista de soluções, cada uma representando posições das rainhas

    Cada solução é uma lista onde o índice i representa a linha
    e o valor representa a coluna da rainha na linha i.

    Exemplo:
        n = 4
        Uma solução: [1, 3, 0, 2] significa:
        - Rainha na linha 0, coluna 1
        - Rainha na linha 1, coluna 3
        - Rainha na linha 2, coluna 0
        - Rainha na linha 3, coluna 2
    """
    resultado = []

    def is_safe(posicoes, linha, coluna):
        """Verifica se é seguro colocar rainha na posição (linha, coluna)"""
        for i in range(linha):
            # Verificar mesma coluna
            if posicoes[i] == coluna:
                return False

            # Verificar diagonais
            if abs(posicoes[i] - coluna) == abs(i - linha):
                return False

        return True

    def backtrack(linha, posicoes):
        # Condição de parada: todas as rainhas colocadas
        if linha == n:
            resultado.append(posicoes[:])
            return

        # Tentar colocar rainha em cada coluna da linha atual
        for coluna in range(n):
            if is_safe(posicoes, linha, coluna):
                # Fazer escolha
                posicoes.append(coluna)

                # Explorar recursivamente
                backtrack(linha + 1, posicoes)

                # Desfazer escolha
                posicoes.pop()

    backtrack(0, [])
    return resultado


def resolver_sudoku(board):
    """
    Resolve um puzzle de Sudoku 9x9.

    Args:
        board: Matriz 9x9 onde '.' representa células vazias

    Returns:
        bool: True se foi possível resolver, False caso contrário

    Modifica a board in-place com a solução.
    """

    def is_valid(board, linha, coluna, num):
        """Verifica se é válido colocar num na posição (linha, coluna)"""
        # Verificar linha
        for x in range(9):
            if board[linha][x] == num:
                return False

        # Verificar coluna
        for x in range(9):
            if board[x][coluna] == num:
                return False

        # Verificar caixa 3x3
        start_linha = linha - linha % 3
        start_coluna = coluna - coluna % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_linha][j + start_coluna] == num:
                    return False

        return True

    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    for num in "123456789":
                        if is_valid(board, i, j, num):
                            # Fazer escolha
                            board[i][j] = num

                            # Explorar recursivamente
                            if backtrack():
                                return True

                            # Desfazer escolha
                            board[i][j] = "."

                    return False  # Nenhum número funciona nesta posição

        return True  # Todas as células preenchidas

    return backtrack()


def soma_combinacoes(candidates, target):
    """
    Encontra todas as combinações únicas que somam target.
    Números podem ser reutilizados.

    Args:
        candidates: Lista de números candidatos
        target: Valor alvo da soma

    Returns:
        list: Lista de combinações que somam target

    Exemplo:
        candidates = [2,3,6,7], target = 7
        Retorna: [[2,2,3], [7]]
    """
    resultado = []
    candidates.sort()  # Facilita poda

    def backtrack(inicio, caminho, soma_atual):
        # Condição de parada: encontrou target
        if soma_atual == target:
            resultado.append(caminho[:])
            return

        # Poda: se soma excede target, parar
        if soma_atual > target:
            return

        # Explorar candidatos a partir de inicio
        for i in range(inicio, len(candidates)):
            # Fazer escolha
            caminho.append(candidates[i])

            # Explorar recursivamente (mesmo i para permitir reutilização)
            backtrack(i, caminho, soma_atual + candidates[i])

            # Desfazer escolha
            caminho.pop()

    backtrack(0, [], 0)
    return resultado


def particionar_palindromos(s):
    """
    Particiona string em substrings que são palíndromos.

    Args:
        s: String de entrada

    Returns:
        list: Lista de todas as partições válidas

    Exemplo:
        s = "aab"
        Retorna: [["a","a","b"], ["aa","b"]]
    """
    resultado = []

    def is_palindromo(substr):
        return substr == substr[::-1]

    def backtrack(inicio, caminho):
        # Condição de parada: processou toda a string
        if inicio == len(s):
            resultado.append(caminho[:])
            return

        # Tentar todas as substrings a partir de inicio
        for fim in range(inicio + 1, len(s) + 1):
            substr = s[inicio:fim]
            if is_palindromo(substr):
                # Fazer escolha
                caminho.append(substr)

                # Explorar recursivamente
                backtrack(fim, caminho)

                # Desfazer escolha
                caminho.pop()

    backtrack(0, [])
    return resultado


# Exemplos de uso e testes
if __name__ == "__main__":
    # Teste 1: Permutações
    print("Teste 1 - Permutações:")
    nums1 = [1, 2, 3]
    resultado = gerar_permutacoes(nums1)
    print(f"Permutações de {nums1}:")
    for perm in resultado:
        print(f"  {perm}")
    print()

    # Teste 2: Combinações
    print("Teste 2 - Combinações:")
    resultado = gerar_combinacoes(4, 2)
    print(f"Combinações de 4 escolha 2:")
    for comb in resultado:
        print(f"  {comb}")
    print()

    # Teste 3: Subconjuntos
    print("Teste 3 - Subconjuntos:")
    nums2 = [1, 2, 3]
    resultado = gerar_subconjuntos(nums2)
    print(f"Subconjuntos de {nums2}:")
    for subset in resultado:
        print(f"  {subset}")
    print()

    # Teste 4: N-Rainhas
    print("Teste 4 - N-Rainhas (n=4):")
    resultado = resolver_n_rainhas(4)
    print(f"Soluções encontradas: {len(resultado)}")
    for i, solucao in enumerate(resultado):
        print(f"  Solução {i+1}: {solucao}")
    print()

    # Teste 5: Soma de Combinações
    print("Teste 5 - Soma de Combinações:")
    candidates = [2, 3, 6, 7]
    target = 7
    resultado = soma_combinacoes(candidates, target)
    print(f"Candidates: {candidates}, Target: {target}")
    print(f"Combinações que somam {target}:")
    for comb in resultado:
        print(f"  {comb}")
    print()

    # Teste 6: Partição em Palíndromos
    print("Teste 6 - Partição em Palíndromos:")
    s = "aab"
    resultado = particionar_palindromos(s)
    print(f"String: '{s}'")
    print(f"Partições em palíndromos:")
    for part in resultado:
        print(f"  {part}")
