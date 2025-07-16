"""
OPERAÇÕES DE BITS - Técnicas Fundamentais
Complexidade: O(1) para a maioria das operações

Intuição:
Operações de bits permitem manipulações eficientes e elegantes:
1. AND (&): Mascaramento e verificação de bits
2. OR (|): Definir bits
3. XOR (^): Flip de bits, detecção de diferenças
4. SHIFT (<<, >>): Multiplicação/divisão por potências de 2
5. NOT (~): Complemento de bits
"""

def operacoes_basicas_demonstracao():
    """
    Demonstra operações básicas de bits com exemplos práticos.
    """
    print("=== OPERAÇÕES BÁSICAS DE BITS ===")
    
    a, b = 12, 10  # 1100 e 1010 em binário
    
    print(f"a = {a} = {bin(a)}")
    print(f"b = {b} = {bin(b)}")
    print(f"a & b = {a & b} = {bin(a & b)}")  # AND: 1000 = 8
    print(f"a | b = {a | b} = {bin(a | b)}")  # OR:  1110 = 14
    print(f"a ^ b = {a ^ b} = {bin(a ^ b)}")  # XOR: 0110 = 6
    print(f"~a = {~a} = {bin(~a & 0xFFFF)}")  # NOT (limitado a 16 bits)
    print(f"a << 1 = {a << 1} = {bin(a << 1)}")  # SHIFT LEFT: 11000 = 24
    print(f"a >> 1 = {a >> 1} = {bin(a >> 1)}")  # SHIFT RIGHT: 110 = 6
    print()

def verificar_bit(num, posicao):
    """
    Verifica se o bit na posição especificada está definido (1).
    
    Args:
        num: Número inteiro
        posicao: Posição do bit (0 = bit menos significativo)
        
    Returns:
        bool: True se bit está definido, False caso contrário
        
    Técnica: num & (1 << posicao) != 0
    """
    return (num & (1 << posicao)) != 0

def definir_bit(num, posicao):
    """
    Define o bit na posição especificada como 1.
    
    Args:
        num: Número inteiro
        posicao: Posição do bit
        
    Returns:
        int: Número com bit definido
        
    Técnica: num | (1 << posicao)
    """
    return num | (1 << posicao)

def limpar_bit(num, posicao):
    """
    Define o bit na posição especificada como 0.
    
    Args:
        num: Número inteiro
        posicao: Posição do bit
        
    Returns:
        int: Número com bit limpo
        
    Técnica: num & ~(1 << posicao)
    """
    return num & ~(1 << posicao)

def flip_bit(num, posicao):
    """
    Inverte o bit na posição especificada.
    
    Args:
        num: Número inteiro
        posicao: Posição do bit
        
    Returns:
        int: Número com bit invertido
        
    Técnica: num ^ (1 << posicao)
    """
    return num ^ (1 << posicao)

def contar_bits_definidos(num):
    """
    Conta quantos bits estão definidos (1) no número.
    
    Args:
        num: Número inteiro
        
    Returns:
        int: Quantidade de bits definidos
        
    Técnica de Brian Kernighan: n & (n-1) remove o bit 1 mais à direita
    """
    count = 0
    while num:
        num &= num - 1  # Remove o bit 1 mais à direita
        count += 1
    return count

def e_potencia_de_dois(num):
    """
    Verifica se um número é potência de 2.
    
    Args:
        num: Número inteiro positivo
        
    Returns:
        bool: True se é potência de 2
        
    Técnica: Potência de 2 tem apenas um bit definido
    num & (num - 1) == 0 para potências de 2
    """
    return num > 0 and (num & (num - 1)) == 0

def encontrar_unico_numero(arr):
    """
    Encontra o número que aparece uma vez em array onde outros aparecem duas vezes.
    
    Args:
        arr: Array onde todos números aparecem 2 vezes, exceto um
        
    Returns:
        int: O número único
        
    Técnica: XOR de todos elementos cancela pares (a ^ a = 0, a ^ 0 = a)
    
    Exemplo:
        arr = [2, 3, 5, 4, 5, 3, 4]
        Retorna: 2
    """
    resultado = 0
    for num in arr:
        resultado ^= num
    return resultado

def encontrar_dois_unicos(arr):
    """
    Encontra dois números que aparecem uma vez em array onde outros aparecem duas vezes.
    
    Args:
        arr: Array onde todos números aparecem 2 vezes, exceto dois
        
    Returns:
        tuple: Os dois números únicos
        
    Técnica:
    1. XOR todos para obter xor_dois_unicos
    2. Encontrar bit que difere entre os dois números
    3. Dividir array em dois grupos baseado nesse bit
    4. XOR cada grupo separadamente
    """
    xor_todos = 0
    for num in arr:
        xor_todos ^= num
    
    # Encontrar bit mais à direita que é 1 (diferença entre os dois únicos)
    bit_diferente = xor_todos & (-xor_todos)
    
    num1 = num2 = 0
    for num in arr:
        if num & bit_diferente:
            num1 ^= num
        else:
            num2 ^= num
    
    return (num1, num2)

def numero_aparece_uma_vez_em_tres(arr):
    """
    Encontra número que aparece uma vez em array onde outros aparecem três vezes.
    
    Args:
        arr: Array onde números aparecem 3 vezes, exceto um que aparece 1 vez
        
    Returns:
        int: O número único
        
    Técnica: Simular contador de 2 bits para cada posição
    """
    ones = twos = 0
    
    for num in arr:
        # ones armazena bits que apareceram 1 ou 4 ou 7... vezes
        # twos armazena bits que apareceram 2 ou 5 ou 8... vezes
        # Quando bit aparece 3 vezes, ele é removido de ambos
        
        twos |= ones & num  # Se bit estava em ones e aparece em num, vai para twos
        ones ^= num         # Toggle bit em ones
        
        # Se bit aparece 3 vezes, remove de ones e twos
        not_three = ~(ones & twos)
        ones &= not_three
        twos &= not_three
    
    return ones

def trocar_bits_pares_impares(num):
    """
    Troca bits em posições pares com ímpares.
    
    Args:
        num: Número inteiro
        
    Returns:
        int: Número com bits trocados
        
    Exemplo:
        num = 23 (10111) → resultado = 43 (101011)
        Posições: 43210   →            543210
        
    Técnica:
    1. Extrair bits pares: num & 0xAAAAAAAA (10101010...)
    2. Extrair bits ímpares: num & 0x55555555 (01010101...)
    3. Shift e combinar
    """
    # Máscara para bits pares (posições 0, 2, 4, ...)
    bits_pares = num & 0x55555555
    
    # Máscara para bits ímpares (posições 1, 3, 5, ...)
    bits_impares = num & 0xAAAAAAAA
    
    # Shift e combinar
    return (bits_pares << 1) | (bits_impares >> 1)

def reverter_bits(num, num_bits=32):
    """
    Reverte a ordem dos bits em um número.
    
    Args:
        num: Número inteiro
        num_bits: Número de bits a considerar
        
    Returns:
        int: Número com bits revertidos
        
    Exemplo:
        num = 12 (1100), num_bits = 8
        Resultado: 48 (00110000)
    """
    resultado = 0
    for i in range(num_bits):
        if num & (1 << i):
            resultado |= (1 << (num_bits - 1 - i))
    return resultado

def subset_xor_zero(arr):
    """
    Verifica se existe subconjunto com XOR igual a zero.
    
    Args:
        arr: Array de inteiros
        
    Returns:
        bool: True se existe subconjunto com XOR = 0
        
    Usa programação dinâmica com bitmask para rastrear XORs possíveis.
    """
    max_xor = 0
    for num in arr:
        max_xor = max(max_xor, num)
    
    # Se array tem mais de log2(max_valor) elementos, sempre existe subconjunto XOR=0
    # (Princípio da Casa dos Pombos)
    if len(arr) > 20:  # 2^20 > 10^6, suficiente para maioria dos casos
        return True
    
    # DP: dp[i] é True se XOR i é possível
    dp = [False] * (max_xor + 1)
    dp[0] = True  # XOR vazio é 0
    
    for num in arr:
        # Processar de trás para frente para evitar usar mesmo elemento duas vezes
        for xor_val in range(max_xor, -1, -1):
            if dp[xor_val]:
                dp[xor_val ^ num] = True
    
    # Verificar se XOR 0 é possível (excluindo subconjunto vazio)
    return any(dp[num] for num in arr)

def maior_xor_subarray(arr):
    """
    Encontra o maior XOR de qualquer subarray.
    
    Args:
        arr: Array de inteiros
        
    Returns:
        int: Maior XOR possível
        
    Usa Trie para armazenar prefixos XOR e encontrar máximo eficientemente.
    """
    class TrieNode:
        def __init__(self):
            self.children = {}
    
    def insert_trie(root, num):
        curr = root
        for i in range(31, -1, -1):  # 32 bits, MSB primeiro
            bit = (num >> i) & 1
            if bit not in curr.children:
                curr.children[bit] = TrieNode()
            curr = curr.children[bit]
    
    def query_max_xor(root, num):
        curr = root
        max_xor = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            # Tentar ir para o bit oposto para maximizar XOR
            toggled_bit = 1 - bit
            if toggled_bit in curr.children:
                max_xor |= (1 << i)
                curr = curr.children[toggled_bit]
            else:
                curr = curr.children[bit]
        return max_xor
    
    root = TrieNode()
    insert_trie(root, 0)  # XOR de prefixo vazio
    
    max_xor = 0
    xor_prefix = 0
    
    for num in arr:
        xor_prefix ^= num
        max_xor = max(max_xor, query_max_xor(root, xor_prefix))
        insert_trie(root, xor_prefix)
    
    return max_xor

# Exemplos de uso e testes
if __name__ == "__main__":
    # Demonstração das operações básicas
    operacoes_basicas_demonstracao()
    
    # Teste 1: Manipulação de bits
    print("Teste 1 - Manipulação de Bits:")
    num = 12  # 1100 em binário
    print(f"Número: {num} = {bin(num)}")
    print(f"Bit 2 definido? {verificar_bit(num, 2)}")  # True
    print(f"Definir bit 1: {definir_bit(num, 1)} = {bin(definir_bit(num, 1))}")  # 14 = 1110
    print(f"Limpar bit 3: {limpar_bit(num, 3)} = {bin(limpar_bit(num, 3))}")   # 4 = 0100
    print()
    
    # Teste 2: Contar bits
    print("Teste 2 - Contar Bits:")
    nums = [7, 8, 15, 16]
    for n in nums:
        print(f"{n} = {bin(n)} tem {contar_bits_definidos(n)} bits definidos")
    print()
    
    # Teste 3: Potência de 2
    print("Teste 3 - Potência de 2:")
    for n in [1, 2, 3, 4, 8, 15, 16]:
        print(f"{n} é potência de 2? {e_potencia_de_dois(n)}")
    print()
    
    # Teste 4: Número único
    print("Teste 4 - Número Único:")
    arr1 = [2, 3, 5, 4, 5, 3, 4]
    resultado = encontrar_unico_numero(arr1)
    print(f"Array: {arr1}")
    print(f"Número único: {resultado}")  # 2
    print()
    
    # Teste 5: Dois números únicos
    print("Teste 5 - Dois Números Únicos:")
    arr2 = [1, 2, 3, 2, 1, 4]
    resultado = encontrar_dois_unicos(arr2)
    print(f"Array: {arr2}")
    print(f"Dois números únicos: {resultado}")  # (3, 4) ou (4, 3)
    print()
    
    # Teste 6: Trocar bits pares/ímpares
    print("Teste 6 - Trocar Bits Pares/Ímpares:")
    num = 23  # 10111
    resultado = trocar_bits_pares_impares(num)
    print(f"Original: {num} = {bin(num)}")
    print(f"Trocado: {resultado} = {bin(resultado)}")
    print()
    
    # Teste 7: Maior XOR subarray
    print("Teste 7 - Maior XOR Subarray:")
    arr3 = [8, 1, 2, 12]
    resultado = maior_xor_subarray(arr3)
    print(f"Array: {arr3}")
    print(f"Maior XOR: {resultado}")  # 15
