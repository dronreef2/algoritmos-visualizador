"""
BUSCA BINÁRIA - Template Universal
Complexidade Temporal: O(log n)
Complexidade Espacial: O(1)

Intuição:
A busca binária é uma técnica fundamental para encontrar elementos em espaços ordenados.
O framework pode ser adaptado para encontrar:
- Elemento exato
- Primeiro elemento que satisfaz uma condição
- Último elemento que satisfaz uma condição
- Posição de inserção
"""

def busca_binaria_basica(arr, target):
    """
    Busca binária básica para encontrar elemento exato.
    
    Args:
        arr: Lista ordenada
        target: Elemento a ser encontrado
        
    Returns:
        int: Índice do elemento ou -1 se não encontrado
        
    Complexidade: O(log n) tempo, O(1) espaço
    """
    if not arr:
        return -1
    
    esquerda, direita = 0, len(arr) - 1
    
    while esquerda <= direita:
        meio = esquerda + (direita - esquerda) // 2
        
        if arr[meio] == target:
            return meio
        elif arr[meio] < target:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    return -1

def busca_primeiro_elemento(arr, target):
    """
    Encontra o primeiro índice do elemento target.
    
    Args:
        arr: Lista ordenada (pode ter duplicatas)
        target: Elemento a ser encontrado
        
    Returns:
        int: Primeiro índice do elemento ou -1 se não encontrado
        
    Exemplo:
        arr = [1, 2, 2, 2, 3], target = 2
        Retorna: 1
    """
    if not arr:
        return -1
    
    esquerda, direita = 0, len(arr) - 1
    resultado = -1
    
    while esquerda <= direita:
        meio = esquerda + (direita - esquerda) // 2
        
        if arr[meio] == target:
            resultado = meio
            direita = meio - 1  # Continue procurando à esquerda
        elif arr[meio] < target:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    return resultado

def busca_ultimo_elemento(arr, target):
    """
    Encontra o último índice do elemento target.
    
    Args:
        arr: Lista ordenada (pode ter duplicatas)
        target: Elemento a ser encontrado
        
    Returns:
        int: Último índice do elemento ou -1 se não encontrado
        
    Exemplo:
        arr = [1, 2, 2, 2, 3], target = 2
        Retorna: 3
    """
    if not arr:
        return -1
    
    esquerda, direita = 0, len(arr) - 1
    resultado = -1
    
    while esquerda <= direita:
        meio = esquerda + (direita - esquerda) // 2
        
        if arr[meio] == target:
            resultado = meio
            esquerda = meio + 1  # Continue procurando à direita
        elif arr[meio] < target:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    return resultado

def busca_posicao_insercao(arr, target):
    """
    Encontra a posição onde target deveria ser inserido para manter ordem.
    
    Args:
        arr: Lista ordenada
        target: Elemento a ser inserido
        
    Returns:
        int: Posição de inserção
        
    Exemplo:
        arr = [1, 3, 5, 6], target = 4
        Retorna: 2 (posição onde 4 deve ser inserido)
    """
    esquerda, direita = 0, len(arr)
    
    while esquerda < direita:
        meio = esquerda + (direita - esquerda) // 2
        
        if arr[meio] < target:
            esquerda = meio + 1
        else:
            direita = meio
    
    return esquerda

def busca_em_espaco_resposta(condicao, inicio, fim):
    """
    Template para busca binária em espaço de resposta.
    Útil quando você precisa encontrar a resposta ótima em um intervalo.
    
    Args:
        condicao: Função que retorna True se o valor satisfaz a condição
        inicio: Limite inferior do espaço de busca
        fim: Limite superior do espaço de busca
        
    Returns:
        int: Valor ótimo encontrado
        
    Exemplo de uso:
        # Encontrar a menor velocidade para comer todas as bananas em H horas
        def pode_comer_todas(velocidade):
            return calcular_tempo(velocidade) <= H
        
        resultado = busca_em_espaco_resposta(pode_comer_todas, 1, max(pilhas))
    """
    esquerda, direita = inicio, fim
    
    while esquerda < direita:
        meio = esquerda + (direita - esquerda) // 2
        
        if condicao(meio):
            direita = meio  # Procurar por valor menor (se existe)
        else:
            esquerda = meio + 1
    
    return esquerda

# Exemplos de uso e testes
if __name__ == "__main__":
    # Teste 1: Busca básica
    arr1 = [1, 3, 5, 7, 9, 11]
    print("Teste 1 - Busca Básica:")
    print(f"Buscar 5 em {arr1}: {busca_binaria_basica(arr1, 5)}")  # Esperado: 2
    print(f"Buscar 6 em {arr1}: {busca_binaria_basica(arr1, 6)}")  # Esperado: -1
    print()
    
    # Teste 2: Primeiro e último elemento
    arr2 = [1, 2, 2, 2, 3, 4, 4, 5]
    print("Teste 2 - Primeiro e Último:")
    print(f"Array: {arr2}")
    print(f"Primeiro 2: {busca_primeiro_elemento(arr2, 2)}")  # Esperado: 1
    print(f"Último 2: {busca_ultimo_elemento(arr2, 2)}")     # Esperado: 3
    print(f"Primeiro 4: {busca_primeiro_elemento(arr2, 4)}")  # Esperado: 5
    print(f"Último 4: {busca_ultimo_elemento(arr2, 4)}")     # Esperado: 6
    print()
    
    # Teste 3: Posição de inserção
    arr3 = [1, 3, 5, 6]
    print("Teste 3 - Posição de Inserção:")
    print(f"Array: {arr3}")
    print(f"Inserir 2: posição {busca_posicao_insercao(arr3, 2)}")  # Esperado: 1
    print(f"Inserir 4: posição {busca_posicao_insercao(arr3, 4)}")  # Esperado: 2
    print(f"Inserir 7: posição {busca_posicao_insercao(arr3, 7)}")  # Esperado: 4
    print()
    
    # Teste 4: Casos extremos
    print("Teste 4 - Casos Extremos:")
    print(f"Array vazio: {busca_binaria_basica([], 5)}")      # Esperado: -1
    print(f"Um elemento (encontrado): {busca_binaria_basica([5], 5)}")  # Esperado: 0
    print(f"Um elemento (não encontrado): {busca_binaria_basica([5], 3)}")  # Esperado: -1

class BuscaBinaria:
    """
    Classe wrapper para busca binária com interface unificada.
    """
    
    def __init__(self):
        """Inicializa a classe de busca binária."""
        pass
    
    def buscar(self, arr, target):
        """
        Método principal para busca binária.
        
        Args:
            arr: Lista ordenada
            target: Elemento a ser encontrado
            
        Returns:
            int: Índice do elemento ou -1 se não encontrado
        """
        return busca_binaria_basica(arr, target)
    
    def buscar_com_passos(self, arr, target):
        """
        Busca binária que retorna os passos intermediários.
        
        Args:
            arr: Lista ordenada
            target: Elemento a ser encontrado
            
        Returns:
            tuple: (índice, lista de passos)
        """
        if not arr:
            return -1, []
        
        esquerda, direita = 0, len(arr) - 1
        passos = []
        
        while esquerda <= direita:
            meio = esquerda + (direita - esquerda) // 2
            passos.append({
                'esquerda': esquerda,
                'direita': direita,
                'meio': meio,
                'valor_meio': arr[meio]
            })
            
            if arr[meio] == target:
                return meio, passos
            elif arr[meio] < target:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        return -1, passos

# Teste da classe
if __name__ == "__main__":
    busca = BuscaBinaria()
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    alvo = 7
    
    resultado = busca.buscar(arr, alvo)
    print(f"Resultado da busca: {resultado}")  # Esperado: 3
