"""
Exemplo de implementação de algoritmo seguindo as instruções customizadas do projeto.
Este arquivo demonstra como o GitHub Copilot deve gerar código baseado nas instruções definidas.
"""

def busca_binaria(lista, target):
    """
    Implementa busca binária em uma lista ordenada.
    
    Complexidade Temporal: O(log n) - onde n é o tamanho da lista
    Complexidade Espacial: O(1) - usa apenas variáveis auxiliares
    
    Args:
        lista (list): Lista ordenada onde buscar
        target: Elemento a ser encontrado
        
    Returns:
        int: Índice do elemento se encontrado, -1 caso contrário
        
    Raises:
        TypeError: Se lista não for uma lista
        ValueError: Se lista estiver vazia
    """
    # Validação de entrada
    if not isinstance(lista, list):
        raise TypeError("Parâmetro 'lista' deve ser uma lista")
    
    if len(lista) == 0:
        raise ValueError("Lista não pode estar vazia")
    
    # Inicialização dos ponteiros
    esquerda = 0
    direita = len(lista) - 1
    
    # Loop principal da busca binária
    while esquerda <= direita:
        # Calcula meio evitando overflow
        meio = esquerda + (direita - esquerda) // 2
        
        # Elemento encontrado
        if lista[meio] == target:
            return meio
        # Target está na metade direita
        elif lista[meio] < target:
            esquerda = meio + 1
        # Target está na metade esquerda
        else:
            direita = meio - 1
    
    # Elemento não encontrado
    return -1


# Exemplos de uso
if __name__ == "__main__":
    # Caso básico
    numeros = [1, 3, 5, 7, 9, 11, 13, 15]
    resultado = busca_binaria(numeros, 7)
    print(f"Busca por 7: índice {resultado}")  # Saída: 3
    
    # Elemento não existe
    resultado = busca_binaria(numeros, 6)
    print(f"Busca por 6: índice {resultado}")  # Saída: -1
    
    # Caso extremo - um elemento
    resultado = busca_binaria([5], 5)
    print(f"Lista com um elemento: índice {resultado}")  # Saída: 0
    
    # Tratamento de erro
    try:
        busca_binaria([], 5)
    except ValueError as e:
        print(f"Erro esperado: {e}")
