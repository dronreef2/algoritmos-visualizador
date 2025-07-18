# 🧪 Teste dos Prompts Customizados MCP
# Este arquivo demonstra como usar os prompts do GitHub Copilot integrado com MCP

def busca_linear(arr, target):
    """
    Implementação básica de busca linear
    
    Args:
        arr: Lista de elementos
        target: Elemento a ser encontrado
        
    Returns:
        int: Índice do elemento ou -1 se não encontrado
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def busca_binaria(arr, target):
    """
    Implementação de busca binária (versão recursiva)
    
    Args:
        arr: Lista ordenada de elementos
        target: Elemento a ser encontrado
        
    Returns:
        int: Índice do elemento ou -1 se não encontrado
    """
    def busca_recursiva(inicio, fim):
        if inicio > fim:
            return -1
        
        meio = (inicio + fim) // 2
        
        if arr[meio] == target:
            return meio
        elif arr[meio] > target:
            return busca_recursiva(inicio, meio - 1)
        else:
            return busca_recursiva(meio + 1, fim)
    
    return busca_recursiva(0, len(arr) - 1)


def ordenacao_bolha(arr):
    """
    Implementação de bubble sort
    
    Args:
        arr: Lista de elementos para ordenar
        
    Returns:
        list: Lista ordenada
    """
    n = len(arr)
    arr_copia = arr.copy()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr_copia[j] > arr_copia[j + 1]:
                arr_copia[j], arr_copia[j + 1] = arr_copia[j + 1], arr_copia[j]
    
    return arr_copia


def fibonacci_recursivo(n):
    """
    Implementação recursiva (ineficiente) de Fibonacci
    
    Args:
        n: Número da sequência de Fibonacci
        
    Returns:
        int: n-ésimo número de Fibonacci
    """
    if n <= 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def fibonacci_iterativo(n):
    """
    Implementação iterativa (eficiente) de Fibonacci
    
    Args:
        n: Número da sequência de Fibonacci
        
    Returns:
        int: n-ésimo número de Fibonacci
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


# 🧪 Função de teste para demonstrar os algoritmos
def testar_algoritmos():
    """
    Função para testar e comparar os algoritmos implementados
    """
    # Dados de teste
    dados_ordenados = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    dados_desordenados = [64, 34, 25, 12, 22, 11, 90]
    target = 7
    
    print("🔍 Testando Busca Linear:")
    resultado_linear = busca_linear(dados_ordenados, target)
    print(f"Elemento {target} encontrado no índice: {resultado_linear}")
    
    print("\n🔍 Testando Busca Binária:")
    resultado_binario = busca_binaria(dados_ordenados, target)
    print(f"Elemento {target} encontrado no índice: {resultado_binario}")
    
    print("\n📊 Testando Ordenação Bolha:")
    dados_ordenados_resultado = ordenacao_bolha(dados_desordenados)
    print(f"Array original: {dados_desordenados}")
    print(f"Array ordenado: {dados_ordenados_resultado}")
    
    print("\n🔢 Testando Fibonacci:")
    n = 10
    print(f"Fibonacci({n}) recursivo: {fibonacci_recursivo(n)}")
    print(f"Fibonacci({n}) iterativo: {fibonacci_iterativo(n)}")


# 🎯 INSTRUÇÕES PARA TESTAR OS PROMPTS MCP:
"""
Agora você pode testar os prompts customizados! 

1. POSICIONE O CURSOR em qualquer função acima
2. DIGITE UM DOS PROMPTS ABAIXO no chat do Copilot:

   /analyze-complexity
   - Analisa a complexidade temporal e espacial da função

   /optimize-algorithm  
   - Sugere otimizações para melhorar performance

   /generate-visualization
   - Gera código para visualizar a execução do algoritmo

   /benchmark-performance
   - Cria código de benchmark para testar performance

3. O MCP SERVER IRÁ FORNECER:
   - Análise detalhada de complexidade
   - Sugestões específicas de otimização
   - Código para visualização
   - Comparações de performance

4. EXPERIMENTE COM DIFERENTES ALGORITMOS:
   - Compare busca_linear vs busca_binaria
   - Analise fibonacci_recursivo vs fibonacci_iterativo
   - Otimize ordenacao_bolha

5. EXECUTE O TESTE:
   - Digite: python teste.py
   - Ou use o prompt: /benchmark-performance
"""

if __name__ == "__main__":
    testar_algoritmos()