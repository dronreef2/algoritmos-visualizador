"""
🏗️ MÓDULO 2: ESTRUTURAS DE DADOS AVANÇADAS - Advanced Data Structures
=====================================================================

Este módulo implementa estruturas de dados avançadas com visualizações
interativas e análise de performance em tempo real.

Estruturas Implementadas:
- Heap (Min/Max)
- Trie (Árvore de Prefixos)
- Union-Find (Disjoint Set)
- Segment Tree
- Fenwick Tree (Binary Indexed Tree)
- LRU Cache
- Graph (Representações diferentes)

Cada estrutura inclui:
- Implementação otimizada
- Visualização passo a passo
- Análise de complexidade
- Casos de uso práticos
"""

import heapq
import time
from typing import List, Dict, Any, Optional, Set, Tuple, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
import bisect
import math

# ============================================================================
# 🏗️ HEAP (MIN/MAX) - PRIORITY QUEUE
# ============================================================================


class AdvancedHeap:
    """
    Implementação avançada de Heap com rastreamento de operações.

    Suporta tanto Min-Heap quanto Max-Heap com visualização detalhada.
    """

    def __init__(self, is_max_heap: bool = False):
        self.heap = []
        self.is_max_heap = is_max_heap
        self.operations = []
        self.operation_count = 0

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registra operação para visualização."""
        self.operation_count += 1
        self.operations.append(
            {"step": self.operation_count, "operation": operation, "heap_state": self.heap.copy(), "details": details}
        )

    def _compare(self, a: int, b: int) -> bool:
        """Compara elementos baseado no tipo de heap."""
        if self.is_max_heap:
            return a > b
        return a < b

    def _heapify_up(self, index: int):
        """Reorganiza heap para cima (após inserção)."""
        parent_index = (index - 1) // 2

        if index > 0 and self._compare(self.heap[index], self.heap[parent_index]):
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._log_operation(
                "heapify_up",
                {"swapped_indices": [index, parent_index], "swapped_values": [self.heap[parent_index], self.heap[index]]},
            )
            self._heapify_up(parent_index)

    def _heapify_down(self, index: int):
        """Reorganiza heap para baixo (após remoção)."""
        size = len(self.heap)
        largest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < size and self._compare(self.heap[left_child], self.heap[largest]):
            largest = left_child

        if right_child < size and self._compare(self.heap[right_child], self.heap[largest]):
            largest = right_child

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._log_operation(
                "heapify_down", {"swapped_indices": [index, largest], "swapped_values": [self.heap[largest], self.heap[index]]}
            )
            self._heapify_down(largest)

    def insert(self, value: int):
        """
        Insere elemento no heap.

        Complexidade: O(log n)
        """
        self.heap.append(value)
        self._log_operation("insert", {"value": value, "position": len(self.heap) - 1})
        self._heapify_up(len(self.heap) - 1)

    def extract_root(self) -> Optional[int]:
        """
        Remove e retorna o elemento raiz (min ou max).

        Complexidade: O(log n)
        """
        if not self.heap:
            return None

        if len(self.heap) == 1:
            root = self.heap.pop()
            self._log_operation("extract_root", {"extracted_value": root, "heap_size": 0})
            return root

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._log_operation(
            "extract_root", {"extracted_value": root, "moved_value": self.heap[0], "heap_size": len(self.heap)}
        )
        self._heapify_down(0)

        return root

    def peek(self) -> Optional[int]:
        """Retorna o elemento raiz sem removê-lo."""
        return self.heap[0] if self.heap else None

    def build_heap(self, arr: List[int]):
        """
        Constrói heap a partir de array.

        Complexidade: O(n)
        """
        self.heap = arr.copy()
        self._log_operation("build_heap", {"initial_array": arr.copy(), "heap_size": len(arr)})

        # Heapify de baixo para cima
        for i in range(len(arr) // 2 - 1, -1, -1):
            self._heapify_down(i)

    def heap_sort(self, arr: List[int]) -> List[int]:
        """
        Ordena array usando heap sort.

        Complexidade: O(n log n)
        """
        self.build_heap(arr)
        sorted_arr = []

        while self.heap:
            sorted_arr.append(self.extract_root())

        if self.is_max_heap:
            sorted_arr.reverse()

        return sorted_arr

    def get_visualization_data(self) -> Dict[str, Any]:
        """Retorna dados para visualização."""
        return {
            "heap": self.heap.copy(),
            "operations": self.operations.copy(),
            "is_max_heap": self.is_max_heap,
            "size": len(self.heap),
        }


# ============================================================================
# 🌳 TRIE - ÁRVORE DE PREFIXOS
# ============================================================================


class TrieNode:
    """Nó da árvore Trie."""

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False
        self.word_count: int = 0


class Trie:
    """
    Implementação de Trie (Árvore de Prefixos) com visualização.

    Útil para:
    - Autocompletar
    - Verificação de palavras
    - Busca por prefixos
    """

    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0
        self.operations = []

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registra operação para visualização."""
        self.operations.append({"operation": operation, "details": details, "tree_state": self._get_tree_state()})

    def insert(self, word: str):
        """
        Insere palavra na Trie.

        Complexidade: O(m), onde m é o comprimento da palavra
        """
        node = self.root
        path = []

        for char in word:
            path.append(char)
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end_of_word:
            self.total_words += 1

        node.is_end_of_word = True
        node.word_count += 1

        self._log_operation("insert", {"word": word, "path": path, "new_word": node.word_count == 1})

    def search(self, word: str) -> bool:
        """
        Verifica se palavra existe na Trie.

        Complexidade: O(m)
        """
        node = self.root
        path = []

        for char in word:
            path.append(char)
            if char not in node.children:
                self._log_operation("search", {"word": word, "path": path, "found": False, "stopped_at": len(path)})
                return False
            node = node.children[char]

        found = node.is_end_of_word
        self._log_operation(
            "search", {"word": word, "path": path, "found": found, "word_count": node.word_count if found else 0}
        )

        return found

    def starts_with(self, prefix: str) -> bool:
        """
        Verifica se existe palavra com o prefixo dado.

        Complexidade: O(m)
        """
        node = self.root
        path = []

        for char in prefix:
            path.append(char)
            if char not in node.children:
                self._log_operation("starts_with", {"prefix": prefix, "path": path, "found": False})
                return False
            node = node.children[char]

        self._log_operation("starts_with", {"prefix": prefix, "path": path, "found": True})

        return True

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Retorna todas as palavras com o prefixo dado.

        Complexidade: O(p + n), onde p é o comprimento do prefixo e n é o número de nós
        """
        node = self.root

        # Navegar até o nó do prefixo
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Encontrar todas as palavras a partir deste nó
        words = []
        self._dfs_words(node, prefix, words)

        self._log_operation("get_words_with_prefix", {"prefix": prefix, "words_found": words, "count": len(words)})

        return words

    def _dfs_words(self, node: TrieNode, current_word: str, words: List[str]):
        """DFS para encontrar todas as palavras."""
        if node.is_end_of_word:
            words.append(current_word)

        for char, child_node in node.children.items():
            self._dfs_words(child_node, current_word + char, words)

    def delete(self, word: str) -> bool:
        """
        Remove palavra da Trie.

        Complexidade: O(m)
        """

        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            if index == len(word):
                if not node.is_end_of_word:
                    return False

                node.is_end_of_word = False
                node.word_count = 0
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False

            should_delete_child = _delete_helper(node.children[char], word, index + 1)

            if should_delete_child:
                del node.children[char]
                return not node.is_end_of_word and len(node.children) == 0

            return False

        if self.search(word):
            _delete_helper(self.root, word, 0)
            self.total_words -= 1

            self._log_operation("delete", {"word": word, "deleted": True})
            return True

        self._log_operation("delete", {"word": word, "deleted": False})
        return False

    def _get_tree_state(self) -> Dict[str, Any]:
        """Retorna estado atual da árvore."""

        def _serialize_node(node: TrieNode) -> Dict[str, Any]:
            return {
                "is_end_of_word": node.is_end_of_word,
                "word_count": node.word_count,
                "children": {char: _serialize_node(child) for char, child in node.children.items()},
            }

        return {"root": _serialize_node(self.root), "total_words": self.total_words}


# ============================================================================
# 🤝 UNION-FIND (DISJOINT SET)
# ============================================================================


class UnionFind:
    """
    Implementação de Union-Find com path compression e union by rank.

    Útil para:
    - Detecção de ciclos
    - Componentes conectados
    - Algoritmos de grafos (Kruskal)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
        self.operations = []

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registra operação para visualização."""
        self.operations.append(
            {
                "operation": operation,
                "details": details,
                "parent_state": self.parent.copy(),
                "rank_state": self.rank.copy(),
                "components": self.components,
            }
        )

    def find(self, x: int) -> int:
        """
        Encontra representante do conjunto com path compression.

        Complexidade: O(α(n)) - função inversa de Ackermann
        """
        path = []
        original_x = x

        # Encontrar raiz
        while self.parent[x] != x:
            path.append(x)
            x = self.parent[x]

        # Path compression
        root = x
        for node in path:
            self.parent[node] = root

        self._log_operation("find", {"element": original_x, "root": root, "path_compressed": path, "path_length": len(path)})

        return root

    def union(self, x: int, y: int) -> bool:
        """
        Une dois conjuntos com union by rank.

        Complexidade: O(α(n))
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            self._log_operation(
                "union",
                {
                    "element1": x,
                    "element2": y,
                    "root1": root_x,
                    "root2": root_y,
                    "united": False,
                    "reason": "already_in_same_set",
                },
            )
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            new_root = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            new_root = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            new_root = root_x

        self.components -= 1

        self._log_operation(
            "union",
            {
                "element1": x,
                "element2": y,
                "root1": root_x,
                "root2": root_y,
                "new_root": new_root,
                "united": True,
                "rank_increased": self.rank[new_root] > max(self.rank[root_x], self.rank[root_y]),
            },
        )

        return True

    def connected(self, x: int, y: int) -> bool:
        """Verifica se dois elementos estão no mesmo conjunto."""
        connected = self.find(x) == self.find(y)

        self._log_operation("connected", {"element1": x, "element2": y, "connected": connected})

        return connected

    def get_components(self) -> List[List[int]]:
        """Retorna todos os componentes conectados."""
        component_map = defaultdict(list)

        for i in range(len(self.parent)):
            root = self.find(i)
            component_map[root].append(i)

        components = list(component_map.values())

        self._log_operation("get_components", {"total_components": len(components), "components": components})

        return components


# ============================================================================
# 🎯 SEGMENT TREE
# ============================================================================


class SegmentTree:
    """
    Implementação de Segment Tree para consultas de intervalo.

    Suporta:
    - Consulta de soma/min/max em intervalo
    - Atualização de elemento
    - Atualização de intervalo (lazy propagation)
    """

    def __init__(self, arr: List[int], operation: str = "sum"):
        self.n = len(arr)
        self.operation = operation
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.arr = arr.copy()
        self.operations = []

        self._build(arr, 0, 0, self.n - 1)

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registra operação para visualização."""
        self.operations.append({"operation": operation, "details": details, "tree_state": self._get_tree_state()})

    def _get_identity(self):
        """Retorna elemento neutro da operação."""
        if self.operation == "sum":
            return 0
        elif self.operation == "min":
            return float("inf")
        elif self.operation == "max":
            return float("-inf")

    def _combine(self, a: int, b: int) -> int:
        """Combina dois valores baseado na operação."""
        if self.operation == "sum":
            return a + b
        elif self.operation == "min":
            return min(a, b)
        elif self.operation == "max":
            return max(a, b)

    def _build(self, arr: List[int], node: int, start: int, end: int):
        """Constrói a árvore de segmento."""
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            self._build(arr, left_child, start, mid)
            self._build(arr, right_child, mid + 1, end)

            self.tree[node] = self._combine(self.tree[left_child], self.tree[right_child])

    def _push_lazy(self, node: int, start: int, end: int):
        """Propaga lazy updates."""
        if self.lazy[node] != 0:
            if self.operation == "sum":
                self.tree[node] += self.lazy[node] * (end - start + 1)
            else:
                self.tree[node] += self.lazy[node]

            if start != end:
                left_child = 2 * node + 1
                right_child = 2 * node + 2
                self.lazy[left_child] += self.lazy[node]
                self.lazy[right_child] += self.lazy[node]

            self.lazy[node] = 0

    def query(self, left: int, right: int) -> int:
        """
        Consulta valor em intervalo [left, right].

        Complexidade: O(log n)
        """
        result = self._query_helper(0, 0, self.n - 1, left, right)

        self._log_operation("query", {"left": left, "right": right, "result": result, "operation": self.operation})

        return result

    def _query_helper(self, node: int, start: int, end: int, left: int, right: int) -> int:
        """Helper para consulta recursiva."""
        if start > right or end < left:
            return self._get_identity()

        self._push_lazy(node, start, end)

        if start >= left and end <= right:
            return self.tree[node]

        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        left_result = self._query_helper(left_child, start, mid, left, right)
        right_result = self._query_helper(right_child, mid + 1, end, left, right)

        return self._combine(left_result, right_result)

    def update(self, index: int, value: int):
        """
        Atualiza elemento no índice.

        Complexidade: O(log n)
        """
        old_value = self.arr[index]
        self.arr[index] = value

        self._update_helper(0, 0, self.n - 1, index, value)

        self._log_operation("update", {"index": index, "old_value": old_value, "new_value": value})

    def _update_helper(self, node: int, start: int, end: int, index: int, value: int):
        """Helper para atualização recursiva."""
        if start == end:
            self.tree[node] = value
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            if index <= mid:
                self._update_helper(left_child, start, mid, index, value)
            else:
                self._update_helper(right_child, mid + 1, end, index, value)

            self.tree[node] = self._combine(self.tree[left_child], self.tree[right_child])

    def range_update(self, left: int, right: int, value: int):
        """
        Atualiza todos os elementos em [left, right].

        Complexidade: O(log n) com lazy propagation
        """
        self._range_update_helper(0, 0, self.n - 1, left, right, value)

        self._log_operation("range_update", {"left": left, "right": right, "value": value})

    def _range_update_helper(self, node: int, start: int, end: int, left: int, right: int, value: int):
        """Helper para atualização de intervalo."""
        self._push_lazy(node, start, end)

        if start > right or end < left:
            return

        if start >= left and end <= right:
            self.lazy[node] += value
            self._push_lazy(node, start, end)
            return

        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        self._range_update_helper(left_child, start, mid, left, right, value)
        self._range_update_helper(right_child, mid + 1, end, left, right, value)

        self._push_lazy(left_child, start, mid)
        self._push_lazy(right_child, mid + 1, end)

        self.tree[node] = self._combine(self.tree[left_child], self.tree[right_child])

    def _get_tree_state(self) -> Dict[str, Any]:
        """Retorna estado atual da árvore."""
        return {
            "tree": self.tree[: 4 * self.n],
            "lazy": self.lazy[: 4 * self.n],
            "array": self.arr.copy(),
            "operation": self.operation,
        }


# ============================================================================
# 💾 LRU CACHE
# ============================================================================


class LRUNode:
    """Nó para implementação de LRU Cache."""

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional["LRUNode"] = None
        self.next: Optional["LRUNode"] = None


class LRUCache:
    """
    Implementação de LRU Cache com visualização.

    Complexidade: O(1) para get e put
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, LRUNode] = {}
        self.operations = []

        # Criar nós dummy para head e tail
        self.head = LRUNode()
        self.tail = LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registra operação para visualização."""
        self.operations.append({"operation": operation, "details": details, "cache_state": self._get_cache_state()})

    def _add_to_head(self, node: LRUNode):
        """Adiciona nó logo após head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: LRUNode):
        """Remove nó da lista."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: LRUNode):
        """Move nó para head (usado recentemente)."""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> LRUNode:
        """Remove último nó antes de tail."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node

    def get(self, key: int) -> int:
        """
        Obtém valor da chave.

        Complexidade: O(1)
        """
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)

            self._log_operation("get", {"key": key, "value": node.value, "hit": True})

            return node.value

        self._log_operation("get", {"key": key, "value": -1, "hit": False})

        return -1

    def put(self, key: int, value: int):
        """
        Adiciona ou atualiza chave-valor.

        Complexidade: O(1)
        """
        if key in self.cache:
            # Atualizar valor existente
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)

            self._log_operation("put", {"key": key, "value": value, "action": "update"})
        else:
            # Adicionar novo nó
            new_node = LRUNode(key, value)

            if len(self.cache) >= self.capacity:
                # Remover LRU
                tail_node = self._remove_tail()
                del self.cache[tail_node.key]

                self._log_operation(
                    "put", {"key": key, "value": value, "action": "add_with_eviction", "evicted_key": tail_node.key}
                )
            else:
                self._log_operation("put", {"key": key, "value": value, "action": "add"})

            self.cache[key] = new_node
            self._add_to_head(new_node)

    def _get_cache_state(self) -> Dict[str, Any]:
        """Retorna estado atual do cache."""
        # Construir ordem da lista
        order = []
        current = self.head.next
        while current != self.tail:
            order.append({"key": current.key, "value": current.value})
            current = current.next

        return {"capacity": self.capacity, "size": len(self.cache), "order": order, "keys": list(self.cache.keys())}


# ============================================================================
# 📊 GRAPH - REPRESENTAÇÕES E ALGORITMOS
# ============================================================================


class Graph:
    """
    Implementação de grafo com múltiplas representações e algoritmos.

    Suporta:
    - Lista de adjacência
    - Matriz de adjacência
    - DFS, BFS
    - Detecção de ciclos
    - Componentes conectados
    """

    def __init__(self, vertices: int, directed: bool = False):
        self.vertices = vertices
        self.directed = directed
        self.adj_list = defaultdict(list)
        self.adj_matrix = [[0] * vertices for _ in range(vertices)]
        self.operations = []

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registra operação para visualização."""
        self.operations.append({"operation": operation, "details": details, "graph_state": self._get_graph_state()})

    def add_edge(self, u: int, v: int, weight: int = 1):
        """
        Adiciona aresta ao grafo.

        Complexidade: O(1)
        """
        self.adj_list[u].append((v, weight))
        self.adj_matrix[u][v] = weight

        if not self.directed:
            self.adj_list[v].append((u, weight))
            self.adj_matrix[v][u] = weight

        self._log_operation("add_edge", {"from": u, "to": v, "weight": weight, "directed": self.directed})

    def dfs(self, start: int, visited: Optional[Set[int]] = None) -> List[int]:
        """
        Depth-First Search.

        Complexidade: O(V + E)
        """
        if visited is None:
            visited = set()

        result = []
        stack = [start]
        path = []

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                path.append(vertex)

                # Adicionar vizinhos na ordem reversa para manter ordem
                neighbors = [v for v, _ in self.adj_list[vertex]]
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)

        self._log_operation("dfs", {"start": start, "path": path, "visited_order": result})

        return result

    def bfs(self, start: int) -> List[int]:
        """
        Breadth-First Search.

        Complexidade: O(V + E)
        """
        visited = set()
        queue = deque([start])
        result = []
        levels = {start: 0}

        while queue:
            vertex = queue.popleft()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                for neighbor, _ in self.adj_list[vertex]:
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        levels[neighbor] = levels[vertex] + 1

        self._log_operation("bfs", {"start": start, "visited_order": result, "levels": levels})

        return result

    def has_cycle(self) -> bool:
        """
        Detecta se o grafo possui ciclo.

        Complexidade: O(V + E)
        """
        if self.directed:
            return self._has_cycle_directed()
        else:
            return self._has_cycle_undirected()

    def _has_cycle_directed(self) -> bool:
        """Detecta ciclo em grafo direcionado usando DFS."""
        color = ["WHITE"] * self.vertices

        def dfs_cycle(vertex):
            color[vertex] = "GRAY"

            for neighbor, _ in self.adj_list[vertex]:
                if color[neighbor] == "GRAY":
                    return True
                if color[neighbor] == "WHITE" and dfs_cycle(neighbor):
                    return True

            color[vertex] = "BLACK"
            return False

        for vertex in range(self.vertices):
            if color[vertex] == "WHITE":
                if dfs_cycle(vertex):
                    self._log_operation("has_cycle", {"has_cycle": True, "type": "directed"})
                    return True

        self._log_operation("has_cycle", {"has_cycle": False, "type": "directed"})
        return False

    def _has_cycle_undirected(self) -> bool:
        """Detecta ciclo em grafo não-direcionado usando Union-Find."""
        uf = UnionFind(self.vertices)

        edges = []
        for u in range(self.vertices):
            for v, weight in self.adj_list[u]:
                if u < v:  # Evitar duplicatas
                    edges.append((u, v))

        for u, v in edges:
            if uf.connected(u, v):
                self._log_operation("has_cycle", {"has_cycle": True, "type": "undirected", "cycle_edge": (u, v)})
                return True
            uf.union(u, v)

        self._log_operation("has_cycle", {"has_cycle": False, "type": "undirected"})
        return False

    def connected_components(self) -> List[List[int]]:
        """
        Encontra componentes conectados.

        Complexidade: O(V + E)
        """
        visited = set()
        components = []

        for vertex in range(self.vertices):
            if vertex not in visited:
                component = []
                stack = [vertex]

                while stack:
                    v = stack.pop()
                    if v not in visited:
                        visited.add(v)
                        component.append(v)

                        for neighbor, _ in self.adj_list[v]:
                            if neighbor not in visited:
                                stack.append(neighbor)

                components.append(component)

        self._log_operation("connected_components", {"components": components, "count": len(components)})

        return components

    def _get_graph_state(self) -> Dict[str, Any]:
        """Retorna estado atual do grafo."""
        return {
            "vertices": self.vertices,
            "directed": self.directed,
            "adj_list": dict(self.adj_list),
            "edge_count": sum(len(neighbors) for neighbors in self.adj_list.values()),
        }


# ============================================================================
# 🧪 FUNÇÕES DE TESTE
# ============================================================================


def test_advanced_structures():
    """Testa todas as estruturas avançadas."""
    print("🏗️ TESTANDO ESTRUTURAS AVANÇADAS")
    print("=" * 50)

    # Teste 1: Heap
    print("\n🔺 Teste 1: Heap")
    print("-" * 30)

    heap = AdvancedHeap(is_max_heap=False)
    values = [4, 1, 7, 3, 8, 5]

    for val in values:
        heap.insert(val)

    print(f"Heap construído: {heap.heap}")
    print(f"Operações registradas: {len(heap.operations)}")

    # Teste 2: Trie
    print("\n🌳 Teste 2: Trie")
    print("-" * 30)

    trie = Trie()
    words = ["apple", "app", "application", "apply", "banana"]

    for word in words:
        trie.insert(word)

    print(f"Palavras inseridas: {words}")
    print(f"Busca 'app': {trie.search('app')}")
    print(f"Prefixo 'app': {trie.get_words_with_prefix('app')}")

    # Teste 3: Union-Find
    print("\n🤝 Teste 3: Union-Find")
    print("-" * 30)

    uf = UnionFind(6)
    edges = [(0, 1), (1, 2), (3, 4)]

    for u, v in edges:
        uf.union(u, v)

    components = uf.get_components()
    print(f"Componentes: {components}")
    print(f"Total de componentes: {uf.components}")

    # Teste 4: Segment Tree
    print("\n🎯 Teste 4: Segment Tree")
    print("-" * 30)

    arr = [1, 3, 5, 7, 9, 11]
    seg_tree = SegmentTree(arr, "sum")

    print(f"Array: {arr}")
    print(f"Soma [1, 3]: {seg_tree.query(1, 3)}")

    seg_tree.update(2, 10)
    print(f"Após update(2, 10) - Soma [1, 3]: {seg_tree.query(1, 3)}")

    # Teste 5: LRU Cache
    print("\n💾 Teste 5: LRU Cache")
    print("-" * 30)

    cache = LRUCache(3)
    operations = [
        ("put", 1, 1),
        ("put", 2, 2),
        ("get", 1),
        ("put", 3, 3),
        ("get", 2),
        ("put", 4, 4),
        ("get", 1),
        ("get", 3),
        ("get", 4),
    ]

    for op in operations:
        if op[0] == "put":
            cache.put(op[1], op[2])
            print(f"PUT({op[1]}, {op[2]})")
        else:
            result = cache.get(op[1])
            print(f"GET({op[1]}) = {result}")

    # Teste 6: Graph
    print("\n📊 Teste 6: Graph")
    print("-" * 30)

    graph = Graph(5, directed=False)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

    for u, v in edges:
        graph.add_edge(u, v)

    print(f"DFS from 0: {graph.dfs(0)}")
    print(f"BFS from 0: {graph.bfs(0)}")
    print(f"Has cycle: {graph.has_cycle()}")
    print(f"Components: {graph.connected_components()}")


if __name__ == "__main__":
    test_advanced_structures()
