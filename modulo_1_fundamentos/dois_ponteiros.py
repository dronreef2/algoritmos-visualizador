"""
DOIS PONTEIROS - Templates Fundamentais
Complexidade Temporal: O(n)
Complexidade Espacial: O(1)

Intuição:
A técnica de dois ponteiros é eficaz para resolver problemas que envolvem:
1. Detecção de ciclos (ponteiros rápido e lento)
2. Busca em arrays ordenados (ponteiros esquerda e direita)
3. Janela variável em arrays/strings
"""

def dois_ponteiros_opostos(arr, target):
    """
    Template para busca usando ponteiros nas extremidades.
    Útil para encontrar pares que somam um valor específico.
    
    Args:
        arr: Lista ordenada
        target: Valor alvo da soma
        
    Returns:
        tuple: Índices do par encontrado ou (-1, -1)
        
    Complexidade: O(n) tempo, O(1) espaço
    
    Exemplo:
        arr = [1, 2, 3, 4, 6], target = 6
        Retorna: (1, 3) pois arr[1] + arr[3] = 2 + 4 = 6
    """
    if not arr or len(arr) < 2:
        return (-1, -1)
    
    esquerda, direita = 0, len(arr) - 1
    
    while esquerda < direita:
        soma_atual = arr[esquerda] + arr[direita]
        
        if soma_atual == target:
            return (esquerda, direita)
        elif soma_atual < target:
            esquerda += 1
        else:
            direita -= 1
    
    return (-1, -1)

def remover_duplicatas_ordenado(arr):
    """
    Remove duplicatas de array ordenado usando dois ponteiros.
    Modifica o array in-place e retorna novo comprimento.
    
    Args:
        arr: Lista ordenada com possíveis duplicatas
        
    Returns:
        int: Novo comprimento sem duplicatas
        
    Exemplo:
        arr = [1, 1, 2, 2, 3] → arr = [1, 2, 3, ?, ?], retorna 3
    """
    if not arr:
        return 0
    
    # Ponteiro lento: posição para próximo elemento único
    # Ponteiro rápido: explora o array
    lento = 0
    
    for rapido in range(1, len(arr)):
        if arr[rapido] != arr[lento]:
            lento += 1
            arr[lento] = arr[rapido]
    
    return lento + 1

def detectar_ciclo_lista_ligada(head):
    """
    Detecta ciclo em lista ligada usando algoritmo de Floyd.
    
    Args:
        head: Nó cabeça da lista ligada
        
    Returns:
        bool: True se há ciclo, False caso contrário
        
    Complexidade: O(n) tempo, O(1) espaço
    """
    if not head or not head.next:
        return False
    
    lento = head
    rapido = head
    
    # Fase 1: Detectar se há ciclo
    while rapido and rapido.next:
        lento = lento.next
        rapido = rapido.next.next
        
        if lento == rapido:
            return True
    
    return False

def encontrar_inicio_ciclo(head):
    """
    Encontra o nó onde o ciclo começa em uma lista ligada.
    
    Args:
        head: Nó cabeça da lista ligada
        
    Returns:
        Node: Nó onde o ciclo começa ou None se não há ciclo
        
    Algoritmo:
    1. Use ponteiros rápido/lento para detectar ciclo
    2. Quando se encontrarem, mova um ponteiro para head
    3. Mova ambos um passo até se encontrarem novamente
    """
    if not head or not head.next:
        return None
    
    # Fase 1: Detectar ciclo
    lento = head
    rapido = head
    
    while rapido and rapido.next:
        lento = lento.next
        rapido = rapido.next.next
        
        if lento == rapido:
            break
    else:
        return None  # Não há ciclo
    
    # Fase 2: Encontrar início do ciclo
    lento = head
    while lento != rapido:
        lento = lento.next
        rapido = rapido.next
    
    return lento

def tres_soma_zero(arr):
    """
    Encontra todos os triplets únicos que somam zero.
    
    Args:
        arr: Lista de inteiros
        
    Returns:
        list: Lista de triplets que somam zero
        
    Estratégia:
    1. Ordene o array
    2. Para cada elemento, use dois ponteiros para encontrar pares
    3. Evite duplicatas pulando elementos iguais
    """
    if not arr or len(arr) < 3:
        return []
    
    arr.sort()
    resultado = []
    
    for i in range(len(arr) - 2):
        # Pular duplicatas para o primeiro elemento
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        
        esquerda, direita = i + 1, len(arr) - 1
        
        while esquerda < direita:
            soma = arr[i] + arr[esquerda] + arr[direita]
            
            if soma == 0:
                resultado.append([arr[i], arr[esquerda], arr[direita]])
                
                # Pular duplicatas
                while esquerda < direita and arr[esquerda] == arr[esquerda + 1]:
                    esquerda += 1
                while esquerda < direita and arr[direita] == arr[direita - 1]:
                    direita -= 1
                
                esquerda += 1
                direita -= 1
            elif soma < 0:
                esquerda += 1
            else:
                direita -= 1
    
    return resultado

def container_com_mais_agua(heights):
    """
    Encontra o container que pode armazenar mais água.
    
    Args:
        heights: Lista de alturas das paredes
        
    Returns:
        int: Área máxima de água que pode ser armazenada
        
    Estratégia:
    Use dois ponteiros nas extremidades e mova o ponteiro da menor altura.
    A intuição é que mover o ponteiro maior nunca resultará em área maior.
    """
    if not heights or len(heights) < 2:
        return 0
    
    esquerda, direita = 0, len(heights) - 1
    area_maxima = 0
    
    while esquerda < direita:
        # Calcular área atual
        largura = direita - esquerda
        altura = min(heights[esquerda], heights[direita])
        area_atual = largura * altura
        area_maxima = max(area_maxima, area_atual)
        
        # Mover o ponteiro da menor altura
        if heights[esquerda] < heights[direita]:
            esquerda += 1
        else:
            direita -= 1
    
    return area_maxima

def reverter_string(s):
    """
    Reverte string usando dois ponteiros (in-place).
    
    Args:
        s: Lista de caracteres
        
    Returns:
        None: Modifica a lista in-place
    """
    if not s:
        return
    
    esquerda, direita = 0, len(s) - 1
    
    while esquerda < direita:
        s[esquerda], s[direita] = s[direita], s[esquerda]
        esquerda += 1
        direita -= 1

# Exemplo de classe para lista ligada (para testes)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Exemplos de uso e testes
if __name__ == "__main__":
    # Teste 1: Dois ponteiros opostos
    print("Teste 1 - Soma de Dois Números:")
    arr1 = [2, 7, 11, 15]
    target = 9
    resultado = dois_ponteiros_opostos(arr1, target)
    print(f"Array: {arr1}, Target: {target}")
    print(f"Índices: {resultado}")  # Esperado: (0, 1)
    print()
    
    # Teste 2: Remover duplicatas
    print("Teste 2 - Remover Duplicatas:")
    arr2 = [1, 1, 2, 2, 3, 3, 3, 4]
    print(f"Array original: {arr2}")
    novo_tamanho = remover_duplicatas_ordenado(arr2)
    print(f"Novo tamanho: {novo_tamanho}")
    print(f"Array modificado: {arr2[:novo_tamanho]}")  # Esperado: [1, 2, 3, 4]
    print()
    
    # Teste 3: Três soma zero
    print("Teste 3 - Três Soma Zero:")
    arr3 = [-1, 0, 1, 2, -1, -4]
    resultado = tres_soma_zero(arr3)
    print(f"Array: {arr3}")
    print(f"Triplets que somam zero: {resultado}")  # Esperado: [[-1, -1, 2], [-1, 0, 1]]
    print()
    
    # Teste 4: Container com mais água
    print("Teste 4 - Container com Mais Água:")
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    area = container_com_mais_agua(heights)
    print(f"Alturas: {heights}")
    print(f"Área máxima: {area}")  # Esperado: 49
    print()
    
    # Teste 5: Reverter string
    print("Teste 5 - Reverter String:")
    s = list("hello")
    print(f"String original: {''.join(s)}")
    reverter_string(s)
    print(f"String revertida: {''.join(s)}")  # Esperado: "olleh"
