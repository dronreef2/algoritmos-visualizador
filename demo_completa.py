"""
🎯 DEMONSTRAÇÃO FINAL - SISTEMA COMPLETO
========================================

Esta demonstração mostra todas as funcionalidades implementadas
do sistema de visualização de algoritmos.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Configurar paths
project_root = Path(__file__).parent
sys.path.append(str(project_root))


def demo_modulo_2():
    """Demonstra o módulo 2 - Estruturas de Dados."""
    print("🏗️ DEMONSTRAÇÃO MÓDULO 2: ESTRUTURAS DE DADOS")
    print("=" * 60)

    from modulo_2_estruturas_dados.estruturas_avancadas import AdvancedHeap, Trie, UnionFind, SegmentTree, LRUCache, Graph

    # 1. Heap
    print("\n🔺 Heap (Min-Heap)")
    print("-" * 30)

    heap = AdvancedHeap(is_max_heap=False)
    values = [15, 10, 20, 8, 25, 3, 12]

    print(f"Inserindo valores: {values}")
    for val in values:
        heap.insert(val)

    print(f"Heap resultante: {heap.heap}")
    print(f"Operações registradas: {len(heap.operations)}")

    # Extrair alguns elementos
    print("\nExtraindo elementos:")
    for _ in range(3):
        extracted = heap.extract_root()
        print(f"  Extraído: {extracted}, Heap: {heap.heap}")

    # 2. Trie
    print("\n🌳 Trie (Árvore de Prefixos)")
    print("-" * 30)

    trie = Trie()
    words = ["programação", "programa", "programar", "dinâmica", "dinâmico"]

    print(f"Inserindo palavras: {words}")
    for word in words:
        trie.insert(word)

    print(f"Total de palavras: {trie.total_words}")

    # Buscar palavras
    test_words = ["programa", "programação", "algoritmo"]
    for word in test_words:
        found = trie.search(word)
        print(f"  '{word}': {'✅ encontrada' if found else '❌ não encontrada'}")

    # Buscar por prefixo
    prefix = "program"
    words_with_prefix = trie.get_words_with_prefix(prefix)
    print(f"  Palavras com prefixo '{prefix}': {words_with_prefix}")

    # 3. Union-Find
    print("\n🤝 Union-Find")
    print("-" * 30)

    uf = UnionFind(8)
    connections = [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7)]

    print(f"Conectando: {connections}")
    for u, v in connections:
        uf.union(u, v)
        print(f"  União({u}, {v}) -> {uf.components} componentes")

    components = uf.get_components()
    print(f"Componentes finais: {components}")

    # 4. Segment Tree
    print("\n🎯 Segment Tree")
    print("-" * 30)

    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    seg_tree = SegmentTree(arr, "sum")

    print(f"Array: {arr}")

    # Consultas
    queries = [(0, 2), (1, 4), (3, 6)]
    for left, right in queries:
        result = seg_tree.query(left, right)
        print(f"  Soma[{left}, {right}] = {result}")

    # Atualização
    seg_tree.update(3, 100)
    print(f"  Após update(3, 100): Soma[1, 4] = {seg_tree.query(1, 4)}")

    # 5. LRU Cache
    print("\n💾 LRU Cache")
    print("-" * 30)

    cache = LRUCache(3)
    operations = [
        ("put", 1, 10),
        ("put", 2, 20),
        ("get", 1),
        ("put", 3, 30),
        ("get", 2),
        ("put", 4, 40),  # Deve remover 1
        ("get", 1),  # Deve retornar -1
        ("get", 3),
        ("get", 4),
    ]

    for op in operations:
        if op[0] == "put":
            cache.put(op[1], op[2])
            print(f"  PUT({op[1]}, {op[2]})")
        else:
            result = cache.get(op[1])
            print(f"  GET({op[1]}) = {result}")

    # 6. Graph
    print("\n📊 Graph")
    print("-" * 30)

    graph = Graph(6, directed=False)
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)]

    print(f"Adicionando arestas: {edges}")
    for u, v in edges:
        graph.add_edge(u, v)

    print(f"DFS a partir de 0: {graph.dfs(0)}")
    print(f"BFS a partir de 0: {graph.bfs(0)}")
    print(f"Tem ciclo: {graph.has_cycle()}")
    print(f"Componentes conectados: {graph.connected_components()}")


def demo_modulo_3():
    """Demonstra o módulo 3 - Programação Dinâmica."""
    print("\n🎯 DEMONSTRAÇÃO MÓDULO 3: PROGRAMAÇÃO DINÂMICA")
    print("=" * 60)

    from modulo_3_programacao_dinamica.metodologia_3_passos import (
        fibonacci_forca_bruta_com_passos,
        fibonacci_memoizacao_com_passos,
        fibonacci_tabulacao_com_passos,
        lcs_tabulacao_com_passos,
    )

    # Fibonacci
    print("\n🔢 Fibonacci - Metodologia 3 Passos")
    print("-" * 40)

    n = 8

    # Força Bruta
    resultado_fb, passos_fb = fibonacci_forca_bruta_com_passos(n)
    print(f"Força Bruta: F({n}) = {resultado_fb} ({len(passos_fb)} chamadas)")

    # Memoização
    resultado_memo, passos_memo = fibonacci_memoizacao_com_passos(n)
    print(f"Memoização: F({n}) = {resultado_memo} ({len(passos_memo)} passos)")

    # Tabulação
    resultado_tab, passos_tab = fibonacci_tabulacao_com_passos(n)
    print(f"Tabulação: F({n}) = {resultado_tab} ({len(passos_tab)} passos)")

    # Comparação de eficiência
    print(f"\nComparação de eficiência:")
    print(f"  Força Bruta: {len(passos_fb)} operações")
    print(f"  Memoização: {len(passos_memo)} operações")
    print(f"  Tabulação: {len(passos_tab)} operações")

    # LCS
    print("\n📝 Longest Common Subsequence (LCS)")
    print("-" * 40)

    texto1 = "ABCDGH"
    texto2 = "AEDFHR"

    resultado_lcs, passos_lcs = lcs_tabulacao_com_passos(texto1, texto2)
    print(f"LCS('{texto1}', '{texto2}') = {resultado_lcs} ({len(passos_lcs)} passos)")

    # Mostrar alguns passos
    print("\nPrimeiros 5 passos:")
    for i, passo in enumerate(passos_lcs[:5]):
        print(f"  {i+1}. {passo['acao']}")


def demo_modulo_4():
    """Demonstra o módulo 4 - Entrevistas."""
    print("\n💼 DEMONSTRAÇÃO MÓDULO 4: ENTREVISTAS")
    print("=" * 60)

    from modulo_4_entrevistas.problem_playground import InterviewSession, SolutionVisualizer, TWO_SUM_PROBLEM

    # Sistema de Entrevistas
    print("\n🎯 Sistema de Entrevistas")
    print("-" * 30)

    session = InterviewSession()

    # Problema: Two Sum
    problem = session.start_session("two_sum")
    print(f"Problema: {problem.title}")
    print(f"Dificuldade: {problem.difficulty}")

    # Solução do usuário
    user_code = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""

    print("\nCódigo submetido:")
    print(user_code)

    # Avaliar solução
    result = session.submit_solution(user_code)

    print(f"\nResultados:")
    print(f"  Testes: {result['test_results']['passed']}/{result['test_results']['total']} ✅")
    print(f"  Tempo: {result['test_results']['execution_time']:.4f}s")
    print(f"  Complexidade: {result['code_analysis']['complexity']['time']}")
    print(f"  Padrões: {result['code_analysis']['patterns']}")
    print(f"  Pontuação: {result['final_score']}/100")

    # Visualização
    print("\n📊 Visualização da Solução")
    print("-" * 30)

    visualizer = SolutionVisualizer(problem)
    test_input = {"nums": [2, 7, 11, 15], "target": 9}
    steps = visualizer.generate_steps(test_input)

    print(f"Passos da visualização: {len(steps)}")
    for i, step in enumerate(steps[:3]):  # Mostrar primeiros 3 passos
        print(f"  {i+1}. {step['action']}")


def demo_visualizacao():
    """Demonstra as visualizações."""
    print("\n🎨 DEMONSTRAÇÃO DE VISUALIZAÇÕES")
    print("=" * 60)

    # Criar algumas visualizações simples
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("🎯 Algoritmos Visualizador - Demonstração", fontsize=16, fontweight="bold")

    # 1. Heap Visualization
    ax1 = axes[0, 0]
    heap_data = [1, 3, 5, 4, 8, 7, 6, 9]
    positions = range(len(heap_data))

    bars = ax1.bar(positions, heap_data, color="skyblue", alpha=0.8)
    ax1.set_title("🔺 Min-Heap", fontweight="bold")
    ax1.set_xlabel("Índice")
    ax1.set_ylabel("Valor")

    # Adicionar valores nas barras
    for bar, value in zip(bars, heap_data):
        ax1.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(value), ha="center", va="bottom", fontweight="bold"
        )

    # 2. Busca Binária
    ax2 = axes[0, 1]
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    colors = ["lightgreen" if i in [3, 4, 5] else "lightblue" for i in range(len(arr))]
    colors[4] = "red"  # Mid element

    bars = ax2.bar(range(len(arr)), arr, color=colors, alpha=0.8)
    ax2.set_title("🔍 Busca Binária", fontweight="bold")
    ax2.set_xlabel("Índice")
    ax2.set_ylabel("Valor")

    # Adicionar setas
    ax2.axvline(3, color="green", linestyle="--", alpha=0.7, label="Left")
    ax2.axvline(5, color="green", linestyle="--", alpha=0.7, label="Right")
    ax2.axvline(4, color="red", linestyle="-", alpha=0.7, label="Mid")
    ax2.legend()

    # 3. Fibonacci DP
    ax3 = axes[1, 0]
    n = 8
    fib_values = [0, 1, 1, 2, 3, 5, 8, 13, 21]

    ax3.plot(range(n + 1), fib_values[: n + 1], "o-", color="orange", linewidth=2, markersize=8)
    ax3.set_title("🔢 Fibonacci - Tabulação", fontweight="bold")
    ax3.set_xlabel("n")
    ax3.set_ylabel("F(n)")
    ax3.grid(True, alpha=0.3)

    # Adicionar valores
    for i, val in enumerate(fib_values[: n + 1]):
        ax3.text(i, val + 0.5, str(val), ha="center", va="bottom", fontweight="bold")

    # 4. LRU Cache
    ax4 = axes[1, 1]
    cache_order = ["Key4", "Key3", "Key1"]  # MRU to LRU
    cache_values = [40, 30, 10]

    bars = ax4.barh(range(len(cache_order)), [1, 1, 1], color=["red", "orange", "yellow"])
    ax4.set_title("💾 LRU Cache", fontweight="bold")
    ax4.set_yticks(range(len(cache_order)))
    ax4.set_yticklabels(cache_order)
    ax4.set_xlabel("Ordem (MRU → LRU)")

    # Adicionar valores
    for i, (key, val) in enumerate(zip(cache_order, cache_values)):
        ax4.text(0.5, i, f"{key}:{val}", ha="center", va="center", fontweight="bold")

    plt.tight_layout()

    # Salvar visualização
    output_path = project_root / "demo_visualization.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"📊 Visualização salva em: {output_path}")

    # Mostrar por alguns segundos
    plt.show(block=False)
    plt.pause(3)
    plt.close()


def main():
    """Executa demonstração completa."""
    print("🎯 DEMONSTRAÇÃO COMPLETA - ALGORITMOS VISUALIZADOR")
    print("=" * 70)

    print(
        """
    Este sistema implementa uma plataforma completa para aprendizado
    de algoritmos e estruturas de dados através de visualizações
    interativas e simulações de entrevistas técnicas.
    """
    )

    try:
        demo_modulo_2()
        demo_modulo_3()
        demo_modulo_4()
        demo_visualizacao()
    except Exception as e:
        print(f"❌ Erro durante demonstração: {e}")
        import traceback

        traceback.print_exc()

    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 70)

    print("\n📋 RESUMO DAS FUNCIONALIDADES:")
    print("✅ Estruturas de Dados: Heap, Trie, Union-Find, Segment Tree, LRU Cache, Graph")
    print("✅ Programação Dinâmica: Metodologia 3 passos (Força Bruta → Memoização → Tabulação)")
    print("✅ Sistema de Entrevistas: Simulação com feedback automático e análise de código")
    print("✅ Visualizações: Matplotlib com animações interativas")
    print("✅ Interface Web: Streamlit com Player/Renderer architecture")
    print("✅ Integração MCP: Análise e otimização automática de código")

    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Execute: streamlit run streamlit_apps/main_app.py")
    print("2. Teste módulos individuais com os arquivos de exemplo")
    print("3. Explore visualizações interativas na interface web")
    print("4. Pratique problemas de entrevista no módulo 4")


if __name__ == "__main__":
    main()
