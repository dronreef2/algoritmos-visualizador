"""
JANELA DESLIZANTE - Template Universal
Complexidade Temporal: O(n)
Complexidade Espacial: O(1) ou O(k) dependendo do problema

Intuição:
A técnica de janela deslizante é eficaz para problemas que envolvem:
1. Substring/sub-array com propriedades específicas
2. Janela de tamanho fixo
3. Janela de tamanho variável que satisfaz uma condição
"""

from collections import defaultdict, deque


def janela_tamanho_fixo_maximo(arr, k):
    """
    Encontra a soma máxima de sub-array de tamanho k.

    Args:
        arr: Lista de inteiros
        k: Tamanho da janela

    Returns:
        int: Soma máxima encontrada

    Complexidade: O(n) tempo, O(1) espaço

    Exemplo:
        arr = [1, 4, 2, 7, 3, 1], k = 3
        Retorna: 13 (sub-array [4, 2, 7])
    """
    if not arr or len(arr) < k:
        return 0

    # Calcular soma da primeira janela
    soma_janela = sum(arr[:k])
    soma_maxima = soma_janela

    # Deslizar a janela
    for i in range(k, len(arr)):
        soma_janela = soma_janela - arr[i - k] + arr[i]
        soma_maxima = max(soma_maxima, soma_janela)

    return soma_maxima


def substring_sem_repeticao(s):
    """
    Encontra o comprimento da maior substring sem caracteres repetidos.

    Args:
        s: String de entrada

    Returns:
        int: Comprimento da maior substring sem repetição

    Estratégia:
    Use janela variável com HashMap para rastrear últimas posições dos caracteres.

    Exemplo:
        s = "abcabcbb"
        Retorna: 3 (substring "abc")
    """
    if not s:
        return 0

    char_index = {}
    max_length = 0
    inicio = 0

    for fim in range(len(s)):
        if s[fim] in char_index and char_index[s[fim]] >= inicio:
            inicio = char_index[s[fim]] + 1

        char_index[s[fim]] = fim
        max_length = max(max_length, fim - inicio + 1)

    return max_length


def minima_janela_cobrindo_substring(s, t):
    """
    Encontra a menor janela em s que contém todos os caracteres de t.

    Args:
        s: String onde buscar
        t: String com caracteres que devem estar na janela

    Returns:
        str: Menor substring que contém todos caracteres de t

    Complexidade: O(|s| + |t|) tempo, O(|s| + |t|) espaço

    Exemplo:
        s = "ADOBECODEBANC", t = "ABC"
        Retorna: "BANC"
    """
    if not s or not t or len(s) < len(t):
        return ""

    # Contar caracteres necessários
    t_count = defaultdict(int)
    for char in t:
        t_count[char] += 1

    required = len(t_count)
    formed = 0
    window_counts = defaultdict(int)

    # Ponteiros da janela
    esquerda, direita = 0, 0

    # Resultado: (comprimento_janela, esquerda, direita)
    ans = float("inf"), None, None

    while direita < len(s):
        # Adicionar caractere da direita à janela
        character = s[direita]
        window_counts[character] += 1

        # Verificar se a frequência do caractere atual atingiu a frequência desejada
        if character in t_count and window_counts[character] == t_count[character]:
            formed += 1

        # Tentar contrair a janela pela esquerda
        while esquerda <= direita and formed == required:
            character = s[esquerda]

            # Atualizar resultado se esta janela é menor
            if direita - esquerda + 1 < ans[0]:
                ans = (direita - esquerda + 1, esquerda, direita)

            # Remover da esquerda
            window_counts[character] -= 1
            if character in t_count and window_counts[character] < t_count[character]:
                formed -= 1

            esquerda += 1

        direita += 1

    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]


def max_consecutivos_com_k_flips(arr, k):
    """
    Encontra o comprimento máximo de 1s consecutivos após flip de no máximo k zeros.

    Args:
        arr: Lista binária (0s e 1s)
        k: Número máximo de zeros que podem ser flipados

    Returns:
        int: Comprimento máximo de 1s consecutivos

    Exemplo:
        arr = [1,1,1,0,0,0,1,1,1,1,0], k = 2
        Retorna: 6 (flipar os zeros nas posições 4 e 5)
    """
    if not arr:
        return 0

    esquerda = 0
    zeros_count = 0
    max_length = 0

    for direita in range(len(arr)):
        # Expandir janela
        if arr[direita] == 0:
            zeros_count += 1

        # Contrair janela se necessário
        while zeros_count > k:
            if arr[esquerda] == 0:
                zeros_count -= 1
            esquerda += 1

        # Atualizar comprimento máximo
        max_length = max(max_length, direita - esquerda + 1)

    return max_length


def substring_com_k_caracteres_distintos(s, k):
    """
    Encontra o comprimento da maior substring com exatamente k caracteres distintos.

    Args:
        s: String de entrada
        k: Número exato de caracteres distintos

    Returns:
        int: Comprimento da maior substring válida

    Exemplo:
        s = "araaci", k = 2
        Retorna: 4 (substring "araa")
    """
    if not s or k == 0:
        return 0

    char_count = defaultdict(int)
    esquerda = 0
    max_length = 0

    for direita in range(len(s)):
        # Expandir janela
        char_count[s[direita]] += 1

        # Contrair janela se temos mais de k caracteres distintos
        while len(char_count) > k:
            char_count[s[esquerda]] -= 1
            if char_count[s[esquerda]] == 0:
                del char_count[s[esquerda]]
            esquerda += 1

        # Atualizar resultado se temos exatamente k caracteres distintos
        if len(char_count) == k:
            max_length = max(max_length, direita - esquerda + 1)

    return max_length


def maximo_janela_deslizante(arr, k):
    """
    Encontra o máximo em cada janela de tamanho k.

    Args:
        arr: Lista de inteiros
        k: Tamanho da janela

    Returns:
        list: Lista com o máximo de cada janela

    Usa deque para manter elementos em ordem decrescente.

    Exemplo:
        arr = [1,3,-1,-3,5,3,6,7], k = 3
        Retorna: [3,3,5,5,6,7]
    """
    if not arr or k == 0:
        return []

    if k == 1:
        return arr

    deq = deque()  # Armazena índices em ordem decrescente de valores
    resultado = []

    for i in range(len(arr)):
        # Remover elementos fora da janela atual
        while deq and deq[0] <= i - k:
            deq.popleft()

        # Remover elementos menores que o atual (não podem ser máximo)
        while deq and arr[deq[-1]] < arr[i]:
            deq.pop()

        deq.append(i)

        # Se já processamos pelo menos k elementos, adicionar máximo
        if i >= k - 1:
            resultado.append(arr[deq[0]])

    return resultado


def template_janela_variavel(arr, is_valid):
    """
    Template genérico para janela deslizante variável.

    Args:
        arr: Array de entrada
        is_valid: Função que determina se a janela atual é válida

    Returns:
        int: Comprimento da maior janela válida

    Este é um template que pode ser adaptado para vários problemas.
    """
    if not arr:
        return 0

    esquerda = 0
    max_length = 0

    for direita in range(len(arr)):
        # Expandir janela adicionando arr[direita]

        # Contrair janela enquanto inválida
        while not is_valid():
            # Remover arr[esquerda] da janela
            esquerda += 1

        # Atualizar resultado
        max_length = max(max_length, direita - esquerda + 1)

    return max_length


# Exemplos de uso e testes
if __name__ == "__main__":
    # Teste 1: Janela de tamanho fixo
    print("Teste 1 - Janela Tamanho Fixo:")
    arr1 = [2, 1, 5, 1, 3, 2]
    k1 = 3
    resultado = janela_tamanho_fixo_maximo(arr1, k1)
    print(f"Array: {arr1}, k: {k1}")
    print(f"Soma máxima: {resultado}")  # Esperado: 9
    print()

    # Teste 2: Substring sem repetição
    print("Teste 2 - Substring Sem Repetição:")
    s1 = "abcabcbb"
    resultado = substring_sem_repeticao(s1)
    print(f"String: {s1}")
    print(f"Comprimento máximo: {resultado}")  # Esperado: 3
    print()

    # Teste 3: Mínima janela cobrindo
    print("Teste 3 - Mínima Janela Cobrindo:")
    s2, t2 = "ADOBECODEBANC", "ABC"
    resultado = minima_janela_cobrindo_substring(s2, t2)
    print(f"S: {s2}, T: {t2}")
    print(f"Mínima janela: {resultado}")  # Esperado: "BANC"
    print()

    # Teste 4: Máximo com k flips
    print("Teste 4 - Máximo com K Flips:")
    arr2 = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    k2 = 2
    resultado = max_consecutivos_com_k_flips(arr2, k2)
    print(f"Array: {arr2}, k: {k2}")
    print(f"Máximo 1s consecutivos: {resultado}")  # Esperado: 6
    print()

    # Teste 5: Máximo em janela deslizante
    print("Teste 5 - Máximo Janela Deslizante:")
    arr3 = [1, 3, -1, -3, 5, 3, 6, 7]
    k3 = 3
    resultado = maximo_janela_deslizante(arr3, k3)
    print(f"Array: {arr3}, k: {k3}")
    print(f"Máximos: {resultado}")  # Esperado: [3, 3, 5, 5, 6, 7]
