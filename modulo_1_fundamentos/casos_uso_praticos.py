"""
📋 CASOS DE USO PRÁTICOS - MÓDULO 1: FUNDAMENTOS
===============================================

Esta coleção apresenta implementações concisas e práticas dos algoritmos
fundamentais, focando em casos de uso que você encontrará em entrevistas
técnicas e desenvolvimento real.

Cada algoritmo inclui:
- Template reutilizável
- Caso de uso real
- Análise de complexidade
- Dicas de otimização
"""

from typing import List, Optional, Tuple, Dict
import bisect
from collections import deque, defaultdict

# ============================================================================
# 🔍 BUSCA BINÁRIA - Templates Práticos
# ============================================================================

def busca_binaria_template(arr: List[int], target: int) -> int:
    """
    Template universal de busca binária
    
    Caso de Uso: Busca padrão para qualquer elemento
    Complexidade: O(log n)
    Retorna: posição se encontrado, -1 se não encontrado
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def busca_elemento_exato(arr: List[int], target: int) -> int:
    """
    Template básico: encontrar elemento exato
    
    Caso de Uso: Verificar se usuário existe em sistema
    Complexidade: O(log n)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def encontrar_primeiro_ocorrencia(arr: List[int], target: int) -> int:
    """
    Template: primeira ocorrência em array com duplicatas
    
    Caso de Uso: Primeira entrada de usuário em logs ordenados
    Complexidade: O(log n)
    """
    left, right = 0, len(arr) - 1
    resultado = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            resultado = mid  # Salvar posição
            right = mid - 1  # Continuar buscando à esquerda
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return resultado

def encontrar_ponto_insercao(arr: List[int], target: int) -> int:
    """
    Template: posição de inserção para manter ordem
    
    Caso de Uso: Inserir nova tarefa em lista ordenada por prioridade
    Complexidade: O(log n)
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left

def buscar_em_array_rotacionado(arr: List[int], target: int) -> int:
    """
    Template: busca em array rotacionado ordenado
    
    Caso de Uso: Busca em cache circular ou buffer rotativo
    Complexidade: O(log n)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        
        # Verificar qual metade está ordenada
        if arr[left] <= arr[mid]:  # Metade esquerda ordenada
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Metade direita ordenada
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

def encontrar_pico_em_array(arr: List[int]) -> int:
    """
    Template: encontrar elemento pico (maior que vizinhos)
    
    Caso de Uso: Encontrar máximo local em dados de sensor
    Complexidade: O(log n)
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] < arr[mid + 1]:
            left = mid + 1  # Pico está à direita
        else:
            right = mid     # Pico está à esquerda ou é o mid
    
    return left

# ============================================================================
# 👥 DOIS PONTEIROS - Templates Práticos
# ============================================================================

def dois_ponteiros_soma_alvo(arr: List[int], target: int) -> Tuple[int, int]:
    """
    Template clássico: encontrar par que soma valor específico
    
    Caso de Uso: Encontrar dois produtos com desconto que totalizam budget
    Complexidade: O(n) - requer array ordenado
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        soma_atual = arr[left] + arr[right]
        
        if soma_atual == target:
            return (left, right)
        elif soma_atual < target:
            left += 1
        else:
            right -= 1
    
    return (-1, -1)

def remover_duplicatas_inplace(arr: List[int]) -> int:
    """
    Template: remover duplicatas mantendo ordem
    
    Caso de Uso: Limpar lista de emails únicos
    Complexidade: O(n)
    """
    if not arr:
        return 0
    
    slow = 0  # Ponteiro para posição de escrita
    
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    
    return slow + 1  # Novo tamanho

def detectar_ciclo_lista_ligada(head) -> bool:
    """
    Template Floyd: detectar ciclo com dois ponteiros
    
    Caso de Uso: Detectar loops infinitos em estruturas de dados
    Complexidade: O(n) tempo, O(1) espaço
    """
    if not head or not head.next:
        return False
    
    slow = fast = head
    
    # Fase 1: Detectar se há ciclo
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False

def tres_elementos_soma_zero(arr: List[int]) -> List[List[int]]:
    """
    Template: encontrar triplas que somam zero
    
    Caso de Uso: Balanceamento de débitos/créditos em contabilidade
    Complexidade: O(n²)
    """
    arr.sort()
    resultado = []
    
    for i in range(len(arr) - 2):
        # Evitar duplicatas no primeiro elemento
        if i > 0 and arr[i] == arr[i-1]:
            continue
        
        left, right = i + 1, len(arr) - 1
        
        while left < right:
            soma = arr[i] + arr[left] + arr[right]
            
            if soma == 0:
                resultado.append([arr[i], arr[left], arr[right]])
                
                # Evitar duplicatas
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif soma < 0:
                left += 1
            else:
                right -= 1
    
    return resultado

def container_com_mais_agua(heights: List[int]) -> int:
    """
    Template: maximizar área entre dois pontos
    
    Caso de Uso: Otimizar capacidade de containers/tanques
    Complexidade: O(n)
    """
    left, right = 0, len(heights) - 1
    max_area = 0
    
    while left < right:
        # Área = largura × altura_minima
        largura = right - left
        altura = min(heights[left], heights[right])
        area_atual = largura * altura
        
        max_area = max(max_area, area_atual)
        
        # Mover ponteiro da menor altura
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area

# ============================================================================
# 🌐 BFS - Templates Práticos
# ============================================================================

def bfs_caminho_mais_curto(grafo: Dict, inicio: str, fim: str) -> List[str]:
    """
    Template: caminho mais curto em grafo não-ponderado
    
    Caso de Uso: Navegação GPS, roteamento de rede
    Complexidade: O(V + E)
    """
    if inicio == fim:
        return [inicio]
    
    visitados = {inicio}
    fila = deque([(inicio, [inicio])])
    
    while fila:
        no_atual, caminho = fila.popleft()
        
        for vizinho in grafo.get(no_atual, []):
            if vizinho == fim:
                return caminho + [vizinho]
            
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
    
    return []  # Caminho não encontrado

def bfs_nivel_por_nivel(grafo: Dict, inicio: str) -> Dict[str, int]:
    """
    Template: processar nós por nível de distância
    
    Caso de Uso: Análise de influência em rede social
    Complexidade: O(V + E)
    """
    distancias = {inicio: 0}
    fila = deque([inicio])
    
    while fila:
        no_atual = fila.popleft()
        
        for vizinho in grafo.get(no_atual, []):
            if vizinho not in distancias:
                distancias[vizinho] = distancias[no_atual] + 1
                fila.append(vizinho)
    
    return distancias

def bfs_matriz_ilhas(grid: List[List[str]]) -> int:
    """
    Template: contar componentes conectados em matriz
    
    Caso de Uso: Análise de clusters em dados geográficos
    Complexidade: O(m × n)
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    visitados = set()
    ilhas = 0
    
    def bfs_ilha(linha, coluna):
        fila = deque([(linha, coluna)])
        visitados.add((linha, coluna))
        
        while fila:
            r, c = fila.popleft()
            
            # Verificar 4 direções
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < m and 0 <= nc < n and 
                    (nr, nc) not in visitados and grid[nr][nc] == '1'):
                    visitados.add((nr, nc))
                    fila.append((nr, nc))
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1' and (i, j) not in visitados:
                bfs_ilha(i, j)
                ilhas += 1
    
    return ilhas

def bfs_menor_caminho_matriz(grid: List[List[int]], inicio: Tuple, fim: Tuple) -> int:
    """
    Template: menor caminho em matriz com obstáculos
    
    Caso de Uso: Pathfinding em jogos, robótica
    Complexidade: O(m × n)
    """
    m, n = len(grid), len(grid[0])
    
    if grid[inicio[0]][inicio[1]] == 1 or grid[fim[0]][fim[1]] == 1:
        return -1  # Início ou fim bloqueados
    
    visitados = set([inicio])
    fila = deque([(inicio[0], inicio[1], 0)])  # (linha, coluna, distância)
    
    while fila:
        r, c, dist = fila.popleft()
        
        if (r, c) == fim:
            return dist
        
        # Verificar 4 direções
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            
            if (0 <= nr < m and 0 <= nc < n and 
                (nr, nc) not in visitados and grid[nr][nc] == 0):
                visitados.add((nr, nc))
                fila.append((nr, nc, dist + 1))
    
    return -1  # Caminho não encontrado

# ============================================================================
# 🔄 BACKTRACKING - Templates Práticos
# ============================================================================

def gerar_permutacoes(nums: List[int]) -> List[List[int]]:
    """
    Template: gerar todas as permutações
    
    Caso de Uso: Testear todas as ordenações possíveis
    Complexidade: O(n! × n)
    """
    resultado = []
    
    def backtrack(permutacao_atual):
        if len(permutacao_atual) == len(nums):
            resultado.append(permutacao_atual[:])  # Fazer cópia
            return
        
        for num in nums:
            if num not in permutacao_atual:
                permutacao_atual.append(num)
                backtrack(permutacao_atual)
                permutacao_atual.pop()  # Backtrack
    
    backtrack([])
    return resultado

def gerar_combinacoes(nums: List[int], k: int) -> List[List[int]]:
    """
    Template: gerar combinações de tamanho k
    
    Caso de Uso: Formar equipes, selecionar amostras
    Complexidade: O(C(n,k) × k)
    """
    resultado = []
    
    def backtrack(inicio, combinacao_atual):
        if len(combinacao_atual) == k:
            resultado.append(combinacao_atual[:])
            return
        
        for i in range(inicio, len(nums)):
            combinacao_atual.append(nums[i])
            backtrack(i + 1, combinacao_atual)
            combinacao_atual.pop()
    
    backtrack(0, [])
    return resultado

def resolver_sudoku(board: List[List[str]]) -> bool:
    """
    Template: resolver sudoku com backtracking
    
    Caso de Uso: Resolução de puzzles, satisfação de restrições
    Complexidade: O(9^(células_vazias))
    """
    def eh_valido(linha, coluna, num):
        # Verificar linha
        for j in range(9):
            if board[linha][j] == num:
                return False
        
        # Verificar coluna
        for i in range(9):
            if board[i][coluna] == num:
                return False
        
        # Verificar quadrante 3x3
        start_row, start_col = 3 * (linha // 3), 3 * (coluna // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def resolver():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for num in '123456789':
                        if eh_valido(i, j, num):
                            board[i][j] = num
                            
                            if resolver():
                                return True
                            
                            board[i][j] = '.'  # Backtrack
                    
                    return False
        return True
    
    return resolver()

def n_rainhas(n: int) -> List[List[str]]:
    """
    Template clássico: problema das N rainhas
    
    Caso de Uso: Planejamento sem conflitos, alocação de recursos
    Complexidade: O(n!)
    """
    resultado = []
    tabuleiro = ['.' * n for _ in range(n)]
    
    def eh_seguro(linha, coluna):
        # Verificar coluna
        for i in range(linha):
            if tabuleiro[i][coluna] == 'Q':
                return False
        
        # Verificar diagonal superior esquerda
        i, j = linha - 1, coluna - 1
        while i >= 0 and j >= 0:
            if tabuleiro[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # Verificar diagonal superior direita
        i, j = linha - 1, coluna + 1
        while i >= 0 and j < n:
            if tabuleiro[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(linha):
        if linha == n:
            resultado.append(tabuleiro[:])  # Fazer cópia
            return
        
        for coluna in range(n):
            if eh_seguro(linha, coluna):
                # Colocar rainha
                tabuleiro[linha] = tabuleiro[linha][:coluna] + 'Q' + tabuleiro[linha][coluna+1:]
                
                backtrack(linha + 1)
                
                # Remover rainha (backtrack)
                tabuleiro[linha] = tabuleiro[linha][:coluna] + '.' + tabuleiro[linha][coluna+1:]
    
    backtrack(0)
    return resultado

# ============================================================================
# 🧪 TESTADORES DE PERFORMANCE
# ============================================================================

def testar_busca_binaria():
    """Testa performance dos templates de busca binária."""
    import random
    import time
    
    # Gerar dados de teste
    arr = sorted(random.randint(1, 10000) for _ in range(10000))
    target = random.choice(arr)
    
    # Testar busca básica
    start = time.time()
    resultado = busca_elemento_exato(arr, target)
    tempo = time.time() - start
    
    print(f"Busca Binária: encontrou {target} na posição {resultado} em {tempo:.6f}s")

def testar_dois_ponteiros():
    """Testa performance dos templates de dois ponteiros."""
    import random
    import time
    
    # Gerar dados de teste
    arr = sorted(random.randint(1, 1000) for _ in range(5000))
    target = random.randint(100, 1900)
    
    start = time.time()
    resultado = dois_ponteiros_soma_alvo(arr, target)
    tempo = time.time() - start
    
    print(f"Dois Ponteiros: encontrou par {resultado} somando {target} em {tempo:.6f}s")

def testar_bfs():
    """Testa performance do BFS."""
    import time
    
    # Criar grafo de teste
    grafo = {}
    for i in range(1000):
        grafo[str(i)] = [str((i+1) % 1000), str((i+2) % 1000)]
    
    start = time.time()
    caminho = bfs_caminho_mais_curto(grafo, "0", "500")
    tempo = time.time() - start
    
    print(f"BFS: encontrou caminho de tamanho {len(caminho)} em {tempo:.6f}s")

def benchmark_completo():
    """Executa benchmark completo de todos os algoritmos."""
    print("🚀 BENCHMARK - ALGORITMOS FUNDAMENTAIS")
    print("=" * 50)
    
    testar_busca_binaria()
    testar_dois_ponteiros()
    testar_bfs()
    
    print("\n✅ Benchmark concluído!")

if __name__ == "__main__":
    benchmark_completo()
