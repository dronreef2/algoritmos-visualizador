"""
OTIMIZAÇÃO DE ARRAYS - Técnicas Fundamentais
Soma de Prefixos: O(1) para consultas de soma de intervalo
Array de Diferenças: O(1) para modificações de intervalo

Intuição:
Estas técnicas transformam operações custosas em operações O(1):
1. Soma de Prefixos: Responder rapidamente "qual a soma de arr[i] até arr[j]?"
2. Array de Diferenças: Aplicar rapidamente "adicione x a todos elementos de i até j"
"""

class SomaPrefixos:
    """
    Classe para calcular somas de intervalos em O(1).
    
    Pré-processamento: O(n)
    Consulta: O(1)
    Espaço: O(n)
    
    Uso típico: Múltiplas consultas de soma de intervalo
    """
    
    def __init__(self, arr):
        """
        Inicializa o array de soma de prefixos.
        
        Args:
            arr: Array original
            
        Exemplo:
            arr = [1, 2, 3, 4, 5]
            prefixos = [0, 1, 3, 6, 10, 15]
            
        prefixos[i] = soma de arr[0] até arr[i-1]
        """
        self.prefixos = [0]  # Começar com 0 para facilitar cálculos
        
        for num in arr:
            self.prefixos.append(self.prefixos[-1] + num)
    
    def soma_intervalo(self, inicio, fim):
        """
        Calcula soma do intervalo [inicio, fim] (inclusivo).
        
        Args:
            inicio: Índice inicial (0-indexado)
            fim: Índice final (0-indexado)
            
        Returns:
            int: Soma dos elementos no intervalo
            
        Fórmula: soma[i:j] = prefixos[j+1] - prefixos[i]
        """
        if inicio < 0 or fim >= len(self.prefixos) - 1 or inicio > fim:
            return 0
        
        return self.prefixos[fim + 1] - self.prefixos[inicio]

class SomaPrefixos2D:
    """
    Soma de prefixos para matrizes 2D.
    Permite consultas de soma de sub-retângulos em O(1).
    """
    
    def __init__(self, matriz):
        """
        Inicializa matriz de soma de prefixos 2D.
        
        Args:
            matriz: Matriz 2D original
        """
        if not matriz or not matriz[0]:
            self.prefixos = []
            return
        
        linhas, colunas = len(matriz), len(matriz[0])
        
        # Criar matriz de prefixos com padding de 0s
        self.prefixos = [[0] * (colunas + 1) for _ in range(linhas + 1)]
        
        for i in range(1, linhas + 1):
            for j in range(1, colunas + 1):
                self.prefixos[i][j] = (matriz[i-1][j-1] + 
                                     self.prefixos[i-1][j] + 
                                     self.prefixos[i][j-1] - 
                                     self.prefixos[i-1][j-1])
    
    def soma_retangulo(self, linha1, coluna1, linha2, coluna2):
        """
        Calcula soma do retângulo definido pelos cantos opostos.
        
        Args:
            linha1, coluna1: Canto superior esquerdo
            linha2, coluna2: Canto inferior direito
            
        Returns:
            int: Soma dos elementos no retângulo
        """
        if not self.prefixos:
            return 0
        
        # Ajustar para coordenadas da matriz de prefixos (1-indexada)
        linha1 += 1
        coluna1 += 1
        linha2 += 1
        coluna2 += 1
        
        return (self.prefixos[linha2][coluna2] - 
                self.prefixos[linha1-1][coluna2] - 
                self.prefixos[linha2][coluna1-1] + 
                self.prefixos[linha1-1][coluna1-1])

class ArrayDiferenca:
    """
    Array de diferenças para modificações de intervalo em O(1).
    
    Construção: O(n)
    Modificação de intervalo: O(1)
    Reconstrução: O(n)
    
    Uso típico: Múltiplas modificações de intervalo seguidas de consulta final
    """
    
    def __init__(self, arr):
        """
        Inicializa array de diferenças.
        
        Args:
            arr: Array original
            
        Array de diferenças d[i] = arr[i] - arr[i-1]
        Propriedade: arr[i] = d[0] + d[1] + ... + d[i] (soma de prefixos de d)
        """
        self.tamanho = len(arr)
        self.dif = [0] * (self.tamanho + 1)  # Padding extra para facilitar
        
        if arr:
            self.dif[0] = arr[0]
            for i in range(1, self.tamanho):
                self.dif[i] = arr[i] - arr[i-1]
    
    def adicionar_intervalo(self, inicio, fim, valor):
        """
        Adiciona valor a todos elementos no intervalo [inicio, fim].
        
        Args:
            inicio: Índice inicial
            fim: Índice final
            valor: Valor a ser adicionado
            
        Complexidade: O(1)
        
        Truque: Para adicionar valor ao intervalo [i, j]:
        - dif[i] += valor (afeta arr[i] até o final)
        - dif[j+1] -= valor (cancela o efeito após arr[j])
        """
        if 0 <= inicio <= fim < self.tamanho:
            self.dif[inicio] += valor
            if fim + 1 < len(self.dif):
                self.dif[fim + 1] -= valor
    
    def obter_array_final(self):
        """
        Reconstrói o array final após todas as modificações.
        
        Returns:
            list: Array com todas as modificações aplicadas
            
        Complexidade: O(n)
        """
        resultado = [0] * self.tamanho
        if self.tamanho > 0:
            resultado[0] = self.dif[0]
            for i in range(1, self.tamanho):
                resultado[i] = resultado[i-1] + self.dif[i]
        
        return resultado

def subarray_soma_k(arr, k):
    """
    Conta quantos sub-arrays têm soma igual a k.
    Usa soma de prefixos com HashMap.
    
    Args:
        arr: Array de inteiros
        k: Soma alvo
        
    Returns:
        int: Número de sub-arrays com soma k
        
    Complexidade: O(n) tempo, O(n) espaço
    
    Intuição: Se prefixo[j] - prefixo[i] = k, então subarray[i+1:j] tem soma k
    """
    if not arr:
        return 0
    
    # Mapa: soma_prefixo -> quantidade de vezes que apareceu
    prefixo_count = {0: 1}  # Soma 0 aparece uma vez (array vazio)
    soma_atual = 0
    resultado = 0
    
    for num in arr:
        soma_atual += num
        
        # Se existe uma soma de prefixo tal que soma_atual - prefixo = k
        # então o subarray entre essa posição e a atual tem soma k
        if soma_atual - k in prefixo_count:
            resultado += prefixo_count[soma_atual - k]
        
        # Adicionar soma atual ao mapa
        prefixo_count[soma_atual] = prefixo_count.get(soma_atual, 0) + 1
    
    return resultado

def matriz_soma_zero(matriz):
    """
    Conta sub-matrizes com soma zero usando soma de prefixos 2D.
    
    Args:
        matriz: Matriz 2D de inteiros
        
    Returns:
        int: Número de sub-matrizes com soma zero
        
    Estratégia:
    1. Para cada par de linhas, reduza para problema 1D
    2. Use técnica de subarray_soma_k para cada coluna
    """
    if not matriz or not matriz[0]:
        return 0
    
    linhas, colunas = len(matriz), len(matriz[0])
    resultado = 0
    
    # Para cada par de linhas
    for linha_inicio in range(linhas):
        temp = [0] * colunas
        
        for linha_fim in range(linha_inicio, linhas):
            # Adicionar linha atual ao array temporário
            for col in range(colunas):
                temp[col] += matriz[linha_fim][col]
            
            # Contar subarrays com soma zero no array temporário
            resultado += subarray_soma_k(temp, 0)
    
    return resultado

def range_update_queries(arr, queries):
    """
    Aplica múltiplas atualizações de intervalo eficientemente.
    
    Args:
        arr: Array original
        queries: Lista de (inicio, fim, valor) para adicionar
        
    Returns:
        list: Array final após todas as atualizações
        
    Exemplo:
        arr = [1, 2, 3, 4, 5]
        queries = [(0, 2, 1), (1, 3, 2)]
        Resultado: [2, 5, 6, 6, 5]
    """
    diff_array = ArrayDiferenca(arr)
    
    # Aplicar todas as queries
    for inicio, fim, valor in queries:
        diff_array.adicionar_intervalo(inicio, fim, valor)
    
    return diff_array.obter_array_final()

def produto_array_exceto_self(arr):
    """
    Calcula produto de todos elementos exceto o atual, sem usar divisão.
    
    Args:
        arr: Array de inteiros
        
    Returns:
        list: Array onde resultado[i] = produto de todos exceto arr[i]
        
    Usa soma de prefixos adaptada para produto.
    
    Exemplo:
        arr = [1, 2, 3, 4]
        Retorna: [24, 12, 8, 6]
    """
    if not arr:
        return []
    
    n = len(arr)
    resultado = [1] * n
    
    # Produto de prefixos (elementos à esquerda)
    for i in range(1, n):
        resultado[i] = resultado[i-1] * arr[i-1]
    
    # Produto de sufixos (elementos à direita)
    produto_direita = 1
    for i in range(n-1, -1, -1):
        resultado[i] *= produto_direita
        produto_direita *= arr[i]
    
    return resultado

# Exemplos de uso e testes
if __name__ == "__main__":
    # Teste 1: Soma de Prefixos 1D
    print("Teste 1 - Soma de Prefixos 1D:")
    arr1 = [1, 2, 3, 4, 5]
    sp = SomaPrefixos(arr1)
    print(f"Array: {arr1}")
    print(f"Soma [1, 3]: {sp.soma_intervalo(1, 3)}")  # Esperado: 9 (2+3+4)
    print(f"Soma [0, 4]: {sp.soma_intervalo(0, 4)}")  # Esperado: 15 (toda soma)
    print()
    
    # Teste 2: Soma de Prefixos 2D
    print("Teste 2 - Soma de Prefixos 2D:")
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    sp2d = SomaPrefixos2D(matriz)
    print("Matriz:")
    for linha in matriz:
        print(f"  {linha}")
    print(f"Soma retângulo (0,0) a (1,1): {sp2d.soma_retangulo(0, 0, 1, 1)}")  # Esperado: 12
    print()
    
    # Teste 3: Array de Diferenças
    print("Teste 3 - Array de Diferenças:")
    arr2 = [1, 2, 3, 4, 5]
    ad = ArrayDiferenca(arr2)
    print(f"Array original: {arr2}")
    
    # Adicionar 2 ao intervalo [1, 3]
    ad.adicionar_intervalo(1, 3, 2)
    # Adicionar 1 ao intervalo [0, 2]
    ad.adicionar_intervalo(0, 2, 1)
    
    resultado = ad.obter_array_final()
    print(f"Após modificações: {resultado}")  # Esperado: [2, 5, 6, 6, 5]
    print()
    
    # Teste 4: Subarray soma K
    print("Teste 4 - Subarray Soma K:")
    arr3 = [1, 1, 1]
    k = 2
    count = subarray_soma_k(arr3, k)
    print(f"Array: {arr3}, K: {k}")
    print(f"Subarrays com soma {k}: {count}")  # Esperado: 2
    print()
    
    # Teste 5: Produto exceto self
    print("Teste 5 - Produto Exceto Self:")
    arr4 = [1, 2, 3, 4]
    produto = produto_array_exceto_self(arr4)
    print(f"Array: {arr4}")
    print(f"Produto exceto self: {produto}")  # Esperado: [24, 12, 8, 6]
