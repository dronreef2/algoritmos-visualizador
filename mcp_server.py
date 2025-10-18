# 🔧 MCP Server para Algoritmos

"""
Servidor MCP customizado para integração com VS Code e Streamlit.
Fornece ferramentas dinâmicas para análise e visualização de algoritmos.
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import time
import math


# Simulação de MCP Server (em produção, usaria a biblioteca oficial)
class AlgorithmMCPServer:
    """
    Servidor MCP para análise de algoritmos.

    Fornece ferramentas para:
    - Análise de complexidade
    - Teste de performance
    - Geração de código
    - Otimização de algoritmos
    """

    def __init__(self):
        self.tools = {
            "analyze_algorithm": self.analyze_algorithm,
            "benchmark_performance": self.benchmark_performance,
            "suggest_optimizations": self.suggest_optimizations,
            "generate_code": self.generate_code,
            "complexity_calculator": self.complexity_calculator,
            "visualize_execution": self.visualize_execution,
        }

        self.algorithm_database = {
            "binary_search": {
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
                "category": "search",
                "optimizations": [
                    "Use iterative approach to save stack space",
                    "Consider interpolation search for uniformly distributed data",
                ],
            },
            "quicksort": {
                "time_complexity": "O(n log n) average, O(n²) worst",
                "space_complexity": "O(log n)",
                "category": "sorting",
                "optimizations": [
                    "Use median-of-three pivot selection",
                    "Switch to insertion sort for small subarrays",
                    "Use 3-way partitioning for duplicate keys",
                ],
            },
            "merge_sort": {
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "category": "sorting",
                "optimizations": [
                    "Use in-place merging to reduce space complexity",
                    "Implement bottom-up approach for better cache performance",
                ],
            },
            "dijkstra": {
                "time_complexity": "O((V + E) log V)",
                "space_complexity": "O(V)",
                "category": "graph",
                "optimizations": [
                    "Use Fibonacci heap for better performance",
                    "Implement bidirectional search for single-pair shortest path",
                ],
            },
        }

    async def analyze_algorithm(self, algorithm_name: str, input_params: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa um algoritmo específico."""

        algorithm_name = algorithm_name.lower().replace(" ", "_").replace("-", "_")

        if algorithm_name in self.algorithm_database:
            algo_info = self.algorithm_database[algorithm_name]

            return {
                "algorithm": algorithm_name,
                "analysis": {
                    "time_complexity": algo_info["time_complexity"],
                    "space_complexity": algo_info["space_complexity"],
                    "category": algo_info["category"],
                    "input_size": input_params.get("input_size", "n"),
                    "predicted_operations": self._calculate_operations(
                        algo_info["time_complexity"], input_params.get("input_size", 1000)
                    ),
                },
                "optimizations": algo_info["optimizations"],
                "recommendations": self._generate_recommendations(algorithm_name, input_params),
            }
        else:
            return {
                "error": f"Algorithm '{algorithm_name}' not found in database",
                "available_algorithms": list(self.algorithm_database.keys()),
            }

    async def benchmark_performance(self, algorithm_name: str, test_params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa benchmark de performance."""

        input_size = test_params.get("input_size", 1000)
        iterations = test_params.get("iterations", 10)

        # Simular execução de benchmark
        await asyncio.sleep(0.1)  # Simular processamento

        # Calcular métricas simuladas baseadas no algoritmo
        base_time = self._simulate_execution_time(algorithm_name, input_size)

        results = []
        for i in range(iterations):
            # Adicionar variação realística
            variation = 1 + (0.1 * (0.5 - abs(0.5 - (i / iterations))))
            execution_time = base_time * variation

            memory_usage = self._simulate_memory_usage(algorithm_name, input_size)

            results.append(
                {
                    "iteration": i + 1,
                    "execution_time_ms": round(execution_time, 4),
                    "memory_usage_kb": round(memory_usage, 2),
                    "operations_count": self._calculate_operations(
                        self.algorithm_database.get(algorithm_name, {}).get("time_complexity", "O(n)"), input_size
                    ),
                }
            )

        # Calcular estatísticas
        times = [r["execution_time_ms"] for r in results]
        memory = [r["memory_usage_kb"] for r in results]

        return {
            "algorithm": algorithm_name,
            "test_parameters": test_params,
            "results": results,
            "statistics": {
                "avg_time_ms": round(sum(times) / len(times), 4),
                "min_time_ms": min(times),
                "max_time_ms": max(times),
                "avg_memory_kb": round(sum(memory) / len(memory), 2),
                "total_iterations": iterations,
            },
            "performance_score": self._calculate_performance_score(algorithm_name, input_size, times),
        }

    async def suggest_optimizations(self, algorithm_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Sugere otimizações para um algoritmo."""

        current_complexity = context.get("current_complexity", "unknown")
        input_characteristics = context.get("input_characteristics", {})
        performance_requirements = context.get("performance_requirements", {})

        suggestions = []

        # Sugestões baseadas no algoritmo
        if algorithm_name in self.algorithm_database:
            base_suggestions = self.algorithm_database[algorithm_name]["optimizations"]
            suggestions.extend(
                [{"type": "algorithm_specific", "suggestion": sugg, "impact": "medium"} for sugg in base_suggestions]
            )

        # Sugestões baseadas nas características da entrada
        if input_characteristics.get("is_sorted", False):
            suggestions.append(
                {
                    "type": "input_optimization",
                    "suggestion": "Consider using algorithms optimized for sorted data",
                    "impact": "high",
                }
            )

        if input_characteristics.get("has_duplicates", False):
            suggestions.append(
                {
                    "type": "input_optimization",
                    "suggestion": "Use algorithms with 3-way partitioning for duplicate handling",
                    "impact": "medium",
                }
            )

        # Sugestões baseadas nos requisitos de performance
        if performance_requirements.get("prioritize_memory", False):
            suggestions.append(
                {
                    "type": "memory_optimization",
                    "suggestion": "Consider in-place algorithms to reduce space complexity",
                    "impact": "high",
                }
            )

        if performance_requirements.get("prioritize_speed", False):
            suggestions.append(
                {
                    "type": "speed_optimization",
                    "suggestion": "Use cache-friendly algorithms and data structures",
                    "impact": "high",
                }
            )

        return {
            "algorithm": algorithm_name,
            "context": context,
            "optimizations": suggestions,
            "alternative_algorithms": self._suggest_alternatives(algorithm_name),
            "estimated_improvement": self._estimate_improvement(suggestions),
        }

    async def generate_code(self, algorithm_name: str, language: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Gera código para um algoritmo específico."""

        templates = {
            "binary_search": {
                "python": '''
def binary_search(arr, target):
    """
    Busca binária iterativa.
    Complexidade: O(log n) tempo, O(1) espaço
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
''',
                "javascript": """
function binarySearch(arr, target) {
    /**
     * Busca binária iterativa
     * Complexidade: O(log n) tempo, O(1) espaço
     */
    let left = 0;
    let right = arr.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        
        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}
""",
            },
            "quicksort": {
                "python": '''
def quicksort(arr, low=0, high=None):
    """
    Quick Sort com particionamento Lomuto.
    Complexidade: O(n log n) médio, O(n²) pior caso
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
'''
            },
        }

        if algorithm_name in templates and language in templates[algorithm_name]:
            code = templates[algorithm_name][language]

            # Aplicar opções de customização
            if options.get("add_comments", True):
                # Código já tem comentários
                pass

            if options.get("add_type_hints", False) and language == "python":
                # Adicionar type hints
                code = code.replace(
                    "def binary_search(arr, target):", "def binary_search(arr: List[int], target: int) -> int:"
                )

            return {
                "algorithm": algorithm_name,
                "language": language,
                "code": code.strip(),
                "options_applied": options,
                "complexity_info": self.algorithm_database.get(algorithm_name, {}),
                "test_cases": self._generate_test_cases(algorithm_name),
            }
        else:
            return {
                "error": f"Code template not available for {algorithm_name} in {language}",
                "available_combinations": [f"{alg}:{lang}" for alg in templates.keys() for lang in templates[alg].keys()],
            }

    async def complexity_calculator(self, code: str, language: str) -> Dict[str, Any]:
        """Calcula a complexidade de um código fornecido."""

        # Simulação de análise de complexidade
        # Em produção, usaria AST parsing e análise estática

        complexity_indicators = {
            "for": "O(n)",
            "while": "O(n)",
            "nested_loop": "O(n²)",
            "recursive": "O(2^n) or O(log n)",
            "sort": "O(n log n)",
            "binary_search": "O(log n)",
        }

        detected_patterns = []
        estimated_complexity = "O(1)"

        lines = code.lower().split("\n")
        nested_level = 0

        for line in lines:
            if "for" in line or "while" in line:
                nested_level += 1
                if nested_level == 1:
                    detected_patterns.append("linear_loop")
                    estimated_complexity = "O(n)"
                elif nested_level == 2:
                    detected_patterns.append("nested_loop")
                    estimated_complexity = "O(n²)"

            if "def" in line and line.strip().endswith("():"):
                # Detectar recursão
                func_name = line.split("def")[1].split("(")[0].strip()
                if func_name in code:
                    detected_patterns.append("recursion")

            if "sort(" in line or ".sort()" in line:
                detected_patterns.append("sorting")
                if estimated_complexity == "O(1)" or estimated_complexity == "O(n)":
                    estimated_complexity = "O(n log n)"

        return {
            "analysis": {
                "estimated_time_complexity": estimated_complexity,
                "estimated_space_complexity": "O(1)" if "recursion" not in detected_patterns else "O(n)",
                "detected_patterns": detected_patterns,
                "confidence": "medium",  # Em produção, seria calculado baseado na precisão da análise
            },
            "recommendations": [
                "Consider using iterative approach to reduce space complexity" if "recursion" in detected_patterns else None,
                "Nested loops detected - consider more efficient algorithms" if "nested_loop" in detected_patterns else None,
            ],
            "language": language,
        }

    async def visualize_execution(self, algorithm_name: str, input_data: List[Any]) -> Dict[str, Any]:
        """Gera dados para visualização da execução de um algoritmo."""

        if algorithm_name == "binary_search":
            return self._trace_binary_search(input_data["array"], input_data["target"])
        elif algorithm_name == "bubble_sort":
            return self._trace_bubble_sort(input_data["array"])
        else:
            return {"error": f"Visualization not available for {algorithm_name}"}

    def _calculate_operations(self, complexity: str, n: int) -> int:
        """Calcula número aproximado de operações baseado na complexidade."""
        if "log" in complexity:
            return int(n * math.log2(max(n, 1)))
        elif "n²" in complexity or "n^2" in complexity:
            return n * n
        elif "2^n" in complexity:
            return min(2 ** min(n, 20), 1000000)  # Limitar para evitar overflow
        else:  # O(n) ou O(1)
            return n if "n" in complexity else 1

    def _simulate_execution_time(self, algorithm_name: str, input_size: int) -> float:
        """Simula tempo de execução baseado no algoritmo e tamanho da entrada."""
        base_times = {"binary_search": 0.001, "linear_search": 0.01, "quicksort": 0.1, "merge_sort": 0.12, "bubble_sort": 1.0}

        base_time = base_times.get(algorithm_name, 0.01)

        if algorithm_name == "binary_search":
            return base_time * math.log2(max(input_size, 1))
        elif algorithm_name in ["quicksort", "merge_sort"]:
            return base_time * input_size * math.log2(max(input_size, 1)) / 1000
        elif algorithm_name == "bubble_sort":
            return base_time * input_size * input_size / 1000000
        else:
            return base_time * input_size / 1000

    def _simulate_memory_usage(self, algorithm_name: str, input_size: int) -> float:
        """Simula uso de memória baseado no algoritmo."""
        if algorithm_name in ["binary_search", "bubble_sort"]:
            return 8 + (input_size * 4) / 1024  # O(1) + array space
        elif algorithm_name == "merge_sort":
            return 8 + (input_size * 8) / 1024  # O(n) auxiliary space
        else:
            return 8 + (input_size * 4) / 1024

    def _calculate_performance_score(self, algorithm_name: str, input_size: int, execution_times: List[float]) -> float:
        """Calcula score de performance baseado nos tempos de execução."""
        avg_time = sum(execution_times) / len(execution_times)
        expected_time = self._simulate_execution_time(algorithm_name, input_size)

        # Score baseado na proximidade do tempo esperado
        ratio = expected_time / max(avg_time, 0.001)
        score = min(100, max(0, ratio * 50))

        return round(score, 1)

    def _generate_recommendations(self, algorithm_name: str, input_params: Dict[str, Any]) -> List[str]:
        """Gera recomendações específicas baseadas no contexto."""
        recommendations = []

        input_size = input_params.get("input_size", 0)

        if input_size > 10000:
            recommendations.append("Consider using more efficient algorithms for large datasets")

        if algorithm_name == "bubble_sort" and input_size > 100:
            recommendations.append("Bubble sort is inefficient for large arrays. Consider quicksort or mergesort")

        return recommendations

    def _suggest_alternatives(self, algorithm_name: str) -> List[Dict[str, str]]:
        """Sugere algoritmos alternativos."""
        alternatives = {
            "bubble_sort": [
                {"name": "quicksort", "reason": "Much better average case performance"},
                {"name": "merge_sort", "reason": "Guaranteed O(n log n) performance"},
                {"name": "heapsort", "reason": "In-place with O(n log n) guarantee"},
            ],
            "linear_search": [
                {"name": "binary_search", "reason": "O(log n) if data is sorted"},
                {"name": "hash_table", "reason": "O(1) average case lookup"},
            ],
        }

        return alternatives.get(algorithm_name, [])

    def _estimate_improvement(self, suggestions: List[Dict[str, str]]) -> Dict[str, str]:
        """Estima melhoria potencial das otimizações."""
        high_impact_count = sum(1 for s in suggestions if s.get("impact") == "high")
        medium_impact_count = sum(1 for s in suggestions if s.get("impact") == "medium")

        if high_impact_count > 0:
            return {"potential": "high", "description": "Significant performance gains expected"}
        elif medium_impact_count > 1:
            return {"potential": "medium", "description": "Moderate performance improvement expected"}
        else:
            return {"potential": "low", "description": "Minor optimizations available"}

    def _generate_test_cases(self, algorithm_name: str) -> List[Dict[str, Any]]:
        """Gera casos de teste para um algoritmo."""
        if algorithm_name == "binary_search":
            return [
                {"input": {"array": [1, 3, 5, 7, 9], "target": 5}, "expected": 2},
                {"input": {"array": [1, 3, 5, 7, 9], "target": 1}, "expected": 0},
                {"input": {"array": [1, 3, 5, 7, 9], "target": 10}, "expected": -1},
                {"input": {"array": [], "target": 5}, "expected": -1},
            ]
        elif algorithm_name == "quicksort":
            return [
                {"input": [3, 1, 4, 1, 5], "expected": [1, 1, 3, 4, 5]},
                {"input": [1], "expected": [1]},
                {"input": [], "expected": []},
                {"input": [5, 4, 3, 2, 1], "expected": [1, 2, 3, 4, 5]},
            ]
        return []

    def _trace_binary_search(self, array: List[int], target: int) -> Dict[str, Any]:
        """Rastreia execução da busca binária para visualização."""
        steps = []
        left, right = 0, len(array) - 1

        while left <= right:
            mid = (left + right) // 2
            steps.append(
                {
                    "step": len(steps) + 1,
                    "left": left,
                    "right": right,
                    "mid": mid,
                    "mid_value": array[mid] if mid < len(array) else None,
                    "comparison": "equal" if array[mid] == target else ("less" if array[mid] < target else "greater"),
                    "found": array[mid] == target,
                }
            )

            if array[mid] == target:
                break
            elif array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return {
            "algorithm": "binary_search",
            "input": {"array": array, "target": target},
            "steps": steps,
            "result": steps[-1]["mid"] if steps and steps[-1]["found"] else -1,
        }

    def _trace_bubble_sort(self, array: List[int]) -> Dict[str, Any]:
        """Rastreia execução do bubble sort para visualização."""
        array = array.copy()
        steps = []
        n = len(array)

        for i in range(n):
            for j in range(0, n - i - 1):
                comparison_step = {
                    "step": len(steps) + 1,
                    "type": "comparison",
                    "comparing": [j, j + 1],
                    "values": [array[j], array[j + 1]],
                    "array_state": array.copy(),
                    "will_swap": array[j] > array[j + 1],
                }
                steps.append(comparison_step)

                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    swap_step = {"step": len(steps) + 1, "type": "swap", "swapped": [j, j + 1], "array_state": array.copy()}
                    steps.append(swap_step)

        return {"algorithm": "bubble_sort", "input": array, "steps": steps, "result": array}


# Função principal para inicializar o servidor MCP
async def main():
    """Inicializa e executa o servidor MCP."""
    server = AlgorithmMCPServer()

    print("🚀 Algorithm MCP Server iniciado!")
    print("🔧 Ferramentas disponíveis:")
    for tool_name in server.tools.keys():
        print(f"  - {tool_name}")

    # Exemplo de uso
    print("\n📊 Exemplo de análise:")
    result = await server.analyze_algorithm("binary_search", {"input_size": 1000})
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
