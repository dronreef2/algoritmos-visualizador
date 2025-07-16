# 📊 Algoritmos de Ordenação
# Implementações completas com análise de complexidade

import time
import random
import matplotlib.pyplot as plt
import numpy as np

def bubble_sort_com_passos(arr):
    """
    Bubble Sort com tracking de passos para visualização
    
    Complexidade: O(n²)
    Espaço: O(1)
    """
    n = len(arr)
    passos = []
    arr_copy = arr.copy()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            # Registra o estado atual
            passos.append({
                'array': arr_copy.copy(),
                'comparando': [j, j + 1],
                'i': i,
                'j': j
            })
            
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                
    passos.append({
        'array': arr_copy.copy(),
        'comparando': [],
        'final': True
    })
    
    return arr_copy, passos


def quick_sort_com_passos(arr, start=0, end=None):
    """
    Quick Sort com tracking de passos
    
    Complexidade: O(n log n) médio, O(n²) pior caso
    Espaço: O(log n)
    """
    if end is None:
        end = len(arr) - 1
        
    passos = []
    
    def partition(arr, low, high, passos):
        pivot = arr[high]
        i = low - 1
        
        passos.append({
            'array': arr.copy(),
            'pivot': high,
            'range': [low, high],
            'action': f'Escolhendo pivot: {pivot}'
        })
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                
                passos.append({
                    'array': arr.copy(),
                    'pivot': high,
                    'trocou': [i, j],
                    'action': f'Trocou {arr[j]} com {arr[i]}'
                })
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        passos.append({
            'array': arr.copy(),
            'pivot_final': i + 1,
            'action': f'Pivot {pivot} na posição final'
        })
        
        return i + 1
    
    def quick_sort_recursive(arr, low, high, passos):
        if low < high:
            pi = partition(arr, low, high, passos)
            quick_sort_recursive(arr, low, pi - 1, passos)
            quick_sort_recursive(arr, pi + 1, high, passos)
    
    arr_copy = arr.copy()
    quick_sort_recursive(arr_copy, start, end, passos)
    
    return arr_copy, passos


def merge_sort_com_passos(arr):
    """
    Merge Sort com tracking de passos
    
    Complexidade: O(n log n)
    Espaço: O(n)
    """
    passos = []
    
    def merge(left, right, start_idx):
        result = []
        i = j = 0
        
        passos.append({
            'merging': True,
            'left': left,
            'right': right,
            'start_idx': start_idx,
            'action': f'Mergeando {left} e {right}'
        })
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        
        passos.append({
            'merged': result,
            'start_idx': start_idx,
            'action': f'Resultado: {result}'
        })
        
        return result
    
    def merge_sort_recursive(arr, start_idx=0):
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        
        passos.append({
            'dividing': True,
            'array': arr,
            'mid': mid,
            'start_idx': start_idx,
            'action': f'Dividindo em {arr[:mid]} e {arr[mid:]}'
        })
        
        left = merge_sort_recursive(arr[:mid], start_idx)
        right = merge_sort_recursive(arr[mid:], start_idx + mid)
        
        return merge(left, right, start_idx)
    
    resultado = merge_sort_recursive(arr.copy())
    return resultado, passos


def heap_sort_com_passos(arr):
    """
    Heap Sort com tracking de passos
    
    Complexidade: O(n log n)
    Espaço: O(1)
    """
    passos = []
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    def heapify(arr, n, i, passos):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
            
        if right < n and arr[right] > arr[largest]:
            largest = right
            
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            passos.append({
                'array': arr.copy(),
                'trocou': [i, largest],
                'heap_size': n,
                'action': f'Heapify: trocou posições {i} e {largest}'
            })
            heapify(arr, n, largest, passos)
    
    # Construir heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr_copy, n, i, passos)
    
    passos.append({
        'array': arr_copy.copy(),
        'heap_construido': True,
        'action': 'Max heap construído'
    })
    
    # Extrair elementos
    for i in range(n - 1, 0, -1):
        arr_copy[0], arr_copy[i] = arr_copy[i], arr_copy[0]
        passos.append({
            'array': arr_copy.copy(),
            'extraiu': arr_copy[i],
            'heap_size': i,
            'action': f'Extraiu máximo: {arr_copy[i]}'
        })
        heapify(arr_copy, i, 0, passos)
    
    return arr_copy, passos


def counting_sort_com_passos(arr):
    """
    Counting Sort com tracking de passos
    
    Complexidade: O(n + k) onde k é o range dos elementos
    Espaço: O(k)
    """
    if not arr:
        return arr, []
    
    passos = []
    arr_copy = arr.copy()
    
    # Encontrar range
    max_val = max(arr_copy)
    min_val = min(arr_copy)
    range_val = max_val - min_val + 1
    
    passos.append({
        'array': arr_copy.copy(),
        'min_val': min_val,
        'max_val': max_val,
        'range': range_val,
        'action': f'Range: {min_val} a {max_val}'
    })
    
    # Counting array
    count = [0] * range_val
    
    # Contar elementos
    for num in arr_copy:
        count[num - min_val] += 1
        
    passos.append({
        'count_array': count.copy(),
        'action': f'Contagem: {count}'
    })
    
    # Reconstruir array
    result = []
    for i, freq in enumerate(count):
        result.extend([i + min_val] * freq)
    
    passos.append({
        'resultado': result,
        'action': f'Array ordenado: {result}'
    })
    
    return result, passos


def benchmark_algoritmos(tamanhos=[100, 500, 1000]):
    """
    Benchmark de performance dos algoritmos de ordenação
    """
    algoritmos = {
        'Bubble Sort': bubble_sort_com_passos,
        'Quick Sort': quick_sort_com_passos, 
        'Merge Sort': merge_sort_com_passos,
        'Heap Sort': heap_sort_com_passos,
        'Counting Sort': counting_sort_com_passos
    }
    
    resultados = {}
    
    for tamanho in tamanhos:
        resultados[tamanho] = {}
        
        # Gerar dados aleatórios
        dados = [random.randint(1, 1000) for _ in range(tamanho)]
        
        for nome, algoritmo in algoritmos.items():
            try:
                start_time = time.time()
                _, _ = algoritmo(dados.copy())
                end_time = time.time()
                
                resultados[tamanho][nome] = end_time - start_time
                
            except Exception as e:
                resultados[tamanho][nome] = float('inf')
    
    return resultados


def analisar_complexidade(algoritmo_nome):
    """
    Análise teórica de complexidade dos algoritmos
    """
    complexidades = {
        'Bubble Sort': {
            'temporal_melhor': 'O(n)',
            'temporal_medio': 'O(n²)',
            'temporal_pior': 'O(n²)',
            'espacial': 'O(1)',
            'estavel': True,
            'in_place': True,
            'adaptativo': True
        },
        'Quick Sort': {
            'temporal_melhor': 'O(n log n)',
            'temporal_medio': 'O(n log n)',
            'temporal_pior': 'O(n²)',
            'espacial': 'O(log n)',
            'estavel': False,
            'in_place': True,
            'adaptativo': False
        },
        'Merge Sort': {
            'temporal_melhor': 'O(n log n)',
            'temporal_medio': 'O(n log n)',
            'temporal_pior': 'O(n log n)',
            'espacial': 'O(n)',
            'estavel': True,
            'in_place': False,
            'adaptativo': False
        },
        'Heap Sort': {
            'temporal_melhor': 'O(n log n)',
            'temporal_medio': 'O(n log n)',
            'temporal_pior': 'O(n log n)',
            'espacial': 'O(1)',
            'estavel': False,
            'in_place': True,
            'adaptativo': False
        },
        'Counting Sort': {
            'temporal_melhor': 'O(n + k)',
            'temporal_medio': 'O(n + k)',
            'temporal_pior': 'O(n + k)',
            'espacial': 'O(k)',
            'estavel': True,
            'in_place': False,
            'adaptativo': False
        }
    }
    
    return complexidades.get(algoritmo_nome, {})


if __name__ == "__main__":
    # Exemplo de uso
    dados_teste = [64, 34, 25, 12, 22, 11, 90]
    
    print("🧪 Testando algoritmos de ordenação:")
    print(f"Array original: {dados_teste}")
    
    # Testar cada algoritmo
    algoritmos = [
        ('Bubble Sort', bubble_sort_com_passos),
        ('Quick Sort', quick_sort_com_passos),
        ('Merge Sort', merge_sort_com_passos),
        ('Heap Sort', heap_sort_com_passos),
        ('Counting Sort', counting_sort_com_passos)
    ]
    
    for nome, func in algoritmos:
        resultado, passos = func(dados_teste.copy())
        print(f"\n{nome}:")
        print(f"  Resultado: {resultado}")
        print(f"  Passos: {len(passos)}")
        
        # Análise de complexidade
        analise = analisar_complexidade(nome)
        print(f"  Complexidade: {analise.get('temporal_medio', 'N/A')}")
