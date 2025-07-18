"""
🧠 PROGRAMAÇÃO DINÂMICA - Metodologia dos 3 Passos
================================================================

Este módulo implementa a metodologia dos 3 passos para resolver problemas
de programação dinâmica com visualizações interativas.

Metodologia:
1. 🔴 Força Bruta (Recursive) - Entender o problema
2. 🟡 Memoização (Top-Down) - Otimizar com cache
3. 🟢 Tabulação (Bottom-Up) - Solução iterativa

Intuição:
A programação dinâmica resolve problemas complexos dividindo-os em
subproblemas menores e reutilizando soluções já calculadas.
"""

import time
from functools import lru_cache
from typing import List, Dict, Tuple, Any
import numpy as np

# ============================================================================
# 🔢 FIBONACCI - Problema Clássico
# ============================================================================

def fibonacci_forca_bruta_com_passos(n: int) -> Tuple[int, List[Dict]]:
    """
    Implementação por força bruta do Fibonacci com tracking de passos.
    
    Complexidade: O(2^n) tempo, O(n) espaço (stack)
    
    Args:
        n: Número da sequência de Fibonacci
        
    Returns:
        Tuple com resultado e lista de passos para visualização
    """
    passos = []
    call_count = 0
    
    def fib_recursive(num, depth=0):
        nonlocal call_count
        call_count += 1
        
        passos.append({
            'tipo': 'chamada',
            'n': num,
            'depth': depth,
            'call_id': call_count,
            'action': f'Calculando F({num})'
        })
        
        if num <= 1:
            passos.append({
                'tipo': 'caso_base',
                'n': num,
                'resultado': num,
                'depth': depth,
                'call_id': call_count,
                'action': f'Caso base: F({num}) = {num}'
            })
            return num
        
        # Chamada recursiva
        left = fib_recursive(num - 1, depth + 1)
        right = fib_recursive(num - 2, depth + 1)
        
        resultado = left + right
        passos.append({
            'tipo': 'resultado',
            'n': num,
            'left': left,
            'right': right,
            'resultado': resultado,
            'depth': depth,
            'call_id': call_count,
            'action': f'F({num}) = F({num-1}) + F({num-2}) = {left} + {right} = {resultado}'
        })
        
        return resultado
    
    resultado = fib_recursive(n)
    
    passos.append({
        'tipo': 'final',
        'resultado_final': resultado,
        'total_chamadas': call_count,
        'action': f'Fibonacci({n}) = {resultado} (Total: {call_count} chamadas)'
    })
    
    return resultado, passos

def fibonacci_memoizacao_com_passos(n: int) -> Tuple[int, List[Dict]]:
    """
    Implementação com memoização do Fibonacci com tracking de passos.
    
    Complexidade: O(n) tempo, O(n) espaço
    
    Args:
        n: Número da sequência de Fibonacci
        
    Returns:
        Tuple com resultado e lista de passos para visualização
    """
    passos = []
    memo = {}
    call_count = 0
    
    def fib_memo(num, depth=0):
        nonlocal call_count
        call_count += 1
        
        passos.append({
            'tipo': 'chamada',
            'n': num,
            'depth': depth,
            'call_id': call_count,
            'memo_state': memo.copy(),
            'action': f'Calculando F({num})'
        })
        
        # Verificar cache
        if num in memo:
            passos.append({
                'tipo': 'cache_hit',
                'n': num,
                'resultado': memo[num],
                'depth': depth,
                'call_id': call_count,
                'memo_state': memo.copy(),
                'action': f'Cache hit: F({num}) = {memo[num]}'
            })
            return memo[num]
        
        if num <= 1:
            memo[num] = num
            passos.append({
                'tipo': 'caso_base',
                'n': num,
                'resultado': num,
                'depth': depth,
                'call_id': call_count,
                'memo_state': memo.copy(),
                'action': f'Caso base: F({num}) = {num}, salvando no cache'
            })
            return num
        
        # Chamadas recursivas
        left = fib_memo(num - 1, depth + 1)
        right = fib_memo(num - 2, depth + 1)
        
        resultado = left + right
        memo[num] = resultado
        
        passos.append({
            'tipo': 'resultado',
            'n': num,
            'left': left,
            'right': right,
            'resultado': resultado,
            'depth': depth,
            'call_id': call_count,
            'memo_state': memo.copy(),
            'action': f'F({num}) = {left} + {right} = {resultado}, salvando no cache'
        })
        
        return resultado
    
    resultado = fib_memo(n)
    
    passos.append({
        'tipo': 'final',
        'resultado_final': resultado,
        'total_chamadas': call_count,
        'cache_final': memo.copy(),
        'action': f'Fibonacci({n}) = {resultado} (Total: {call_count} chamadas, Cache: {len(memo)} entradas)'
    })
    
    return resultado, passos

def fibonacci_tabulacao_com_passos(n: int) -> Tuple[int, List[Dict]]:
    """
    Implementação com tabulação do Fibonacci com tracking de passos.
    
    Complexidade: O(n) tempo, O(n) espaço (pode ser O(1))
    
    Args:
        n: Número da sequência de Fibonacci
        
    Returns:
        Tuple com resultado e lista de passos para visualização
    """
    passos = []
    
    if n <= 1:
        passos.append({
            'tipo': 'caso_base',
            'n': n,
            'resultado': n,
            'dp_table': [n] if n == 1 else [0],
            'action': f'Caso base: F({n}) = {n}'
        })
        return n, passos
    
    # Inicializar tabela DP
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    passos.append({
        'tipo': 'inicializacao',
        'dp_table': dp.copy(),
        'action': 'Inicializando tabela DP: dp[0] = 0, dp[1] = 1'
    })
    
    # Preencher tabela
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
        
        passos.append({
            'tipo': 'calculo',
            'i': i,
            'dp_i_1': dp[i-1],
            'dp_i_2': dp[i-2],
            'resultado': dp[i],
            'dp_table': dp.copy(),
            'action': f'dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i-1]} + {dp[i-2]} = {dp[i]}'
        })
    
    passos.append({
        'tipo': 'final',
        'resultado_final': dp[n],
        'dp_table_final': dp.copy(),
        'action': f'Fibonacci({n}) = {dp[n]} (Tabela completa)'
    })
    
    return dp[n], passos

# ============================================================================
# 🎒 PROBLEMA DA MOCHILA (KNAPSACK)
# ============================================================================

def knapsack_forca_bruta_com_passos(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[Dict]]:
    """
    Solução por força bruta do problema da mochila.
    
    Complexidade: O(2^n) tempo, O(n) espaço
    
    Args:
        weights: Lista de pesos dos itens
        values: Lista de valores dos itens
        capacity: Capacidade da mochila
        
    Returns:
        Tuple com valor máximo e lista de passos
    """
    passos = []
    n = len(weights)
    call_count = 0
    
    def knapsack_recursive(i, remaining_capacity, current_items):
        nonlocal call_count
        call_count += 1
        
        passos.append({
            'tipo': 'chamada',
            'item_index': i,
            'remaining_capacity': remaining_capacity,
            'current_items': current_items.copy(),
            'call_id': call_count,
            'action': f'Considerando item {i}, capacidade restante: {remaining_capacity}'
        })
        
        # Caso base
        if i == n or remaining_capacity == 0:
            current_value = sum(values[j] for j in current_items)
            passos.append({
                'tipo': 'caso_base',
                'item_index': i,
                'remaining_capacity': remaining_capacity,
                'current_items': current_items.copy(),
                'current_value': current_value,
                'call_id': call_count,
                'action': f'Caso base: valor atual = {current_value}'
            })
            return current_value
        
        # Opção 1: Não incluir o item atual
        not_include = knapsack_recursive(i + 1, remaining_capacity, current_items)
        
        # Opção 2: Incluir o item atual (se couber)
        include = 0
        if weights[i] <= remaining_capacity:
            new_items = current_items + [i]
            include = values[i] + knapsack_recursive(i + 1, remaining_capacity - weights[i], new_items)
        
        resultado = max(not_include, include)
        
        passos.append({
            'tipo': 'resultado',
            'item_index': i,
            'remaining_capacity': remaining_capacity,
            'not_include': not_include,
            'include': include,
            'resultado': resultado,
            'call_id': call_count,
            'action': f'Item {i}: max({not_include}, {include}) = {resultado}'
        })
        
        return resultado
    
    resultado = knapsack_recursive(0, capacity, [])
    
    passos.append({
        'tipo': 'final',
        'resultado_final': resultado,
        'total_chamadas': call_count,
        'action': f'Valor máximo da mochila: {resultado} (Total: {call_count} chamadas)'
    })
    
    return resultado, passos

def knapsack_tabulacao_com_passos(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[Dict]]:
    """
    Solução com tabulação do problema da mochila.
    
    Complexidade: O(n*W) tempo, O(n*W) espaço
    
    Args:
        weights: Lista de pesos dos itens
        values: Lista de valores dos itens
        capacity: Capacidade da mochila
        
    Returns:
        Tuple com valor máximo e lista de passos
    """
    passos = []
    n = len(weights)
    
    # Inicializar tabela DP
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    passos.append({
        'tipo': 'inicializacao',
        'dp_table': [row[:] for row in dp],
        'weights': weights,
        'values': values,
        'capacity': capacity,
        'action': 'Inicializando tabela DP com zeros'
    })
    
    # Preencher tabela
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Não incluir o item atual
            dp[i][w] = dp[i-1][w]
            
            # Incluir o item atual (se couber)
            if weights[i-1] <= w:
                include_value = values[i-1] + dp[i-1][w - weights[i-1]]
                dp[i][w] = max(dp[i][w], include_value)
                
                passos.append({
                    'tipo': 'calculo',
                    'item_index': i-1,
                    'weight': weights[i-1],
                    'value': values[i-1],
                    'capacity': w,
                    'not_include': dp[i-1][w],
                    'include': include_value,
                    'resultado': dp[i][w],
                    'dp_table': [row[:] for row in dp],
                    'action': f'dp[{i}][{w}] = max({dp[i-1][w]}, {values[i-1]} + {dp[i-1][w - weights[i-1]]}) = {dp[i][w]}'
                })
            else:
                passos.append({
                    'tipo': 'nao_cabe',
                    'item_index': i-1,
                    'weight': weights[i-1],
                    'capacity': w,
                    'resultado': dp[i][w],
                    'dp_table': [row[:] for row in dp],
                    'action': f'Item {i-1} não cabe (peso {weights[i-1]} > capacidade {w})'
                })
    
    # Rastrear itens selecionados
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
    
    passos.append({
        'tipo': 'final',
        'resultado_final': dp[n][capacity],
        'selected_items': selected_items[::-1],
        'dp_table_final': [row[:] for row in dp],
        'action': f'Valor máximo: {dp[n][capacity]}, Itens selecionados: {selected_items[::-1]}'
    })
    
    return dp[n][capacity], passos

# ============================================================================
# 📏 LONGEST COMMON SUBSEQUENCE (LCS)
# ============================================================================

def lcs_tabulacao_com_passos(text1: str, text2: str) -> Tuple[int, List[Dict]]:
    """
    Solução com tabulação do LCS.
    
    Complexidade: O(m*n) tempo, O(m*n) espaço
    
    Args:
        text1: Primeira string
        text2: Segunda string
        
    Returns:
        Tuple com comprimento do LCS e lista de passos
    """
    passos = []
    m, n = len(text1), len(text2)
    
    # Inicializar tabela DP
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    passos.append({
        'tipo': 'inicializacao',
        'text1': text1,
        'text2': text2,
        'dp_table': [row[:] for row in dp],
        'action': f'Comparando "{text1}" e "{text2}"'
    })
    
    # Preencher tabela
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                passos.append({
                    'tipo': 'match',
                    'i': i-1,
                    'j': j-1,
                    'char1': text1[i-1],
                    'char2': text2[j-1],
                    'resultado': dp[i][j],
                    'dp_table': [row[:] for row in dp],
                    'action': f'Match: "{text1[i-1]}" == "{text2[j-1]}", dp[{i}][{j}] = {dp[i][j]}'
                })
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                passos.append({
                    'tipo': 'no_match',
                    'i': i-1,
                    'j': j-1,
                    'char1': text1[i-1],
                    'char2': text2[j-1],
                    'from_top': dp[i-1][j],
                    'from_left': dp[i][j-1],
                    'resultado': dp[i][j],
                    'dp_table': [row[:] for row in dp],
                    'action': f'No match: "{text1[i-1]}" != "{text2[j-1]}", dp[{i}][{j}] = max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}'
                })
    
    # Reconstruir LCS
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i-1] == text2[j-1]:
            lcs_chars.append(text1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    lcs_string = ''.join(reversed(lcs_chars))
    
    passos.append({
        'tipo': 'final',
        'lcs_length': dp[m][n],
        'lcs_string': lcs_string,
        'dp_table_final': [row[:] for row in dp],
        'action': f'LCS length: {dp[m][n]}, LCS: "{lcs_string}"'
    })
    
    return dp[m][n], passos

# ============================================================================
# 🪙 COIN CHANGE
# ============================================================================

def coin_change_tabulacao_com_passos(coins: List[int], amount: int) -> Tuple[int, List[Dict]]:
    """
    Solução com tabulação do Coin Change.
    
    Complexidade: O(amount * len(coins)) tempo, O(amount) espaço
    
    Args:
        coins: Lista de denominações de moedas
        amount: Valor alvo
        
    Returns:
        Tuple com número mínimo de moedas e lista de passos
    """
    passos = []
    
    # Inicializar tabela DP
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    passos.append({
        'tipo': 'inicializacao',
        'coins': coins,
        'amount': amount,
        'dp_table': dp[:],
        'action': f'Inicializando: dp[0] = 0, resto = inf'
    })
    
    # Preencher tabela
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                new_value = dp[a - coin] + 1
                if new_value < dp[a]:
                    dp[a] = new_value
                    passos.append({
                        'tipo': 'atualizacao',
                        'amount': a,
                        'coin': coin,
                        'prev_value': dp[a - coin],
                        'new_value': new_value,
                        'dp_table': dp[:],
                        'action': f'dp[{a}] = min(dp[{a}], dp[{a - coin}] + 1) = min({dp[a]}, {new_value}) = {dp[a]}'
                    })
    
    resultado = dp[amount] if dp[amount] != float('inf') else -1
    
    passos.append({
        'tipo': 'final',
        'resultado_final': resultado,
        'dp_table_final': dp[:],
        'action': f'Número mínimo de moedas para {amount}: {resultado}'
    })
    
    return resultado, passos

# ============================================================================
# 🧪 FUNÇÕES DE TESTE E BENCHMARK
# ============================================================================

def benchmark_dp_approaches(problem_type: str, problem_size: int) -> Dict[str, Any]:
    """
    Benchmark das três abordagens para um problema de DP.
    
    Args:
        problem_type: Tipo do problema ('fibonacci', 'knapsack', etc.)
        problem_size: Tamanho do problema
        
    Returns:
        Dicionário com resultados do benchmark
    """
    results = {}
    
    if problem_type == 'fibonacci':
        # Fibonacci
        if problem_size <= 30:  # Força bruta só para tamanhos pequenos
            start_time = time.time()
            result_fb, steps_fb = fibonacci_forca_bruta_com_passos(problem_size)
            time_fb = time.time() - start_time
            results['forca_bruta'] = {
                'tempo': time_fb,
                'resultado': result_fb,
                'passos': len(steps_fb),
                'complexidade': f'O(2^{problem_size})'
            }
        
        start_time = time.time()
        result_memo, steps_memo = fibonacci_memoizacao_com_passos(problem_size)
        time_memo = time.time() - start_time
        results['memoizacao'] = {
            'tempo': time_memo,
            'resultado': result_memo,
            'passos': len(steps_memo),
            'complexidade': f'O({problem_size})'
        }
        
        start_time = time.time()
        result_tab, steps_tab = fibonacci_tabulacao_com_passos(problem_size)
        time_tab = time.time() - start_time
        results['tabulacao'] = {
            'tempo': time_tab,
            'resultado': result_tab,
            'passos': len(steps_tab),
            'complexidade': f'O({problem_size})'
        }
    
    return results

# ============================================================================
# 📊 EXEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("🧠 TESTANDO PROGRAMAÇÃO DINÂMICA - METODOLOGIA DOS 3 PASSOS")
    print("=" * 70)
    
    # Teste 1: Fibonacci
    print("\n🔢 Teste 1: Fibonacci(10)")
    print("-" * 40)
    
    n = 10
    resultado_fb, passos_fb = fibonacci_forca_bruta_com_passos(n)
    resultado_memo, passos_memo = fibonacci_memoizacao_com_passos(n)
    resultado_tab, passos_tab = fibonacci_tabulacao_com_passos(n)
    
    print(f"Força Bruta: F({n}) = {resultado_fb} ({len(passos_fb)} passos)")
    print(f"Memoização:  F({n}) = {resultado_memo} ({len(passos_memo)} passos)")
    print(f"Tabulação:   F({n}) = {resultado_tab} ({len(passos_tab)} passos)")
    
    # Teste 2: Knapsack
    print("\n🎒 Teste 2: Problema da Mochila")
    print("-" * 40)
    
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    resultado_knap_fb, passos_knap_fb = knapsack_forca_bruta_com_passos(weights, values, capacity)
    resultado_knap_tab, passos_knap_tab = knapsack_tabulacao_com_passos(weights, values, capacity)
    
    print(f"Força Bruta: Valor máximo = {resultado_knap_fb} ({len(passos_knap_fb)} passos)")
    print(f"Tabulação:   Valor máximo = {resultado_knap_tab} ({len(passos_knap_tab)} passos)")
    
    # Teste 3: LCS
    print("\n📏 Teste 3: Longest Common Subsequence")
    print("-" * 40)
    
    text1 = "ABCDGH"
    text2 = "AEDFHR"
    
    resultado_lcs, passos_lcs = lcs_tabulacao_com_passos(text1, text2)
    print(f'LCS("{text1}", "{text2}") = {resultado_lcs} ({len(passos_lcs)} passos)')
    
    # Teste 4: Coin Change
    print("\n🪙 Teste 4: Coin Change")
    print("-" * 40)
    
    coins = [1, 3, 4]
    amount = 6
    
    resultado_coin, passos_coin = coin_change_tabulacao_com_passos(coins, amount)
    print(f"Coin Change({coins}, {amount}) = {resultado_coin} ({len(passos_coin)} passos)")
    
    # Benchmark
    print("\n📊 Benchmark: Fibonacci(20)")
    print("-" * 40)
    
    benchmark_results = benchmark_dp_approaches('fibonacci', 20)
    for approach, results in benchmark_results.items():
        print(f"{approach.title()}: {results['tempo']:.6f}s, {results['passos']} passos, {results['complexidade']}")
    
    print("\n✅ Todos os testes completados!")
