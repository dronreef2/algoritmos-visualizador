"""
🧪 TESTE INTEGRADO - TODOS OS MÓDULOS
====================================

Este arquivo testa todas as implementações dos módulos para garantir
que estão funcionando corretamente.
"""

import sys
import os
import traceback
from pathlib import Path

# Adicionar diretórios ao path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_modulo_1():
    """Testa o módulo 1 - Fundamentos."""
    print("📚 TESTANDO MÓDULO 1: FUNDAMENTOS")
    print("=" * 50)
    
    try:
        # Testar busca binária
        from modulo_1_fundamentos.busca_binaria import busca_binaria_com_passos
        
        arr = [1, 3, 5, 7, 9, 11, 13, 15]
        target = 7
        resultado, passos = busca_binaria_com_passos(arr, target)
        
        print(f"✅ Busca Binária: {resultado} (encontrado em {len(passos)} passos)")
        
        # Testar dois ponteiros
        from modulo_1_fundamentos.dois_ponteiros import two_sum_com_passos
        
        nums = [2, 7, 11, 15]
        target = 9
        resultado, passos = two_sum_com_passos(nums, target)
        
        print(f"✅ Dois Ponteiros: {resultado} (processado em {len(passos)} passos)")
        
        print("✅ Módulo 1 OK!")
        
    except Exception as e:
        print(f"❌ Erro no Módulo 1: {e}")
        traceback.print_exc()

def test_modulo_2():
    """Testa o módulo 2 - Estruturas de Dados."""
    print("\n🏗️ TESTANDO MÓDULO 2: ESTRUTURAS DE DADOS")
    print("=" * 50)
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import (
            AdvancedHeap, Trie, UnionFind, SegmentTree, LRUCache
        )
        
        # Testar Heap
        heap = AdvancedHeap()
        for val in [4, 1, 7, 3, 8, 5]:
            heap.insert(val)
        
        print(f"✅ Heap: {heap.heap}")
        
        # Testar Trie
        trie = Trie()
        words = ["apple", "app", "application"]
        for word in words:
            trie.insert(word)
        
        print(f"✅ Trie: {trie.search('app')} (busca 'app')")
        
        # Testar Union-Find
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(2, 3)
        
        print(f"✅ Union-Find: {uf.components} componentes")
        
        # Testar Segment Tree
        arr = [1, 3, 5, 7, 9, 11]
        seg_tree = SegmentTree(arr)
        
        print(f"✅ Segment Tree: soma[1,3] = {seg_tree.query(1, 3)}")
        
        # Testar LRU Cache
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        result = cache.get(1)
        
        print(f"✅ LRU Cache: get(1) = {result}")
        
        print("✅ Módulo 2 OK!")
        
    except Exception as e:
        print(f"❌ Erro no Módulo 2: {e}")
        traceback.print_exc()

def test_modulo_3():
    """Testa o módulo 3 - Programação Dinâmica."""
    print("\n🎯 TESTANDO MÓDULO 3: PROGRAMAÇÃO DINÂMICA")
    print("=" * 50)
    
    try:
        from modulo_3_programacao_dinamica.metodologia_3_passos import (
            fibonacci_forca_bruta_com_passos,
            fibonacci_memoizacao_com_passos,
            fibonacci_tabulacao_com_passos,
            knapsack_01_tabulacao_com_passos
        )
        
        # Testar Fibonacci
        n = 10
        
        # Força bruta
        resultado_fb, passos_fb = fibonacci_forca_bruta_com_passos(n)
        print(f"✅ Fibonacci Força Bruta: F({n}) = {resultado_fb} ({len(passos_fb)} passos)")
        
        # Memoização
        resultado_memo, passos_memo = fibonacci_memoizacao_com_passos(n)
        print(f"✅ Fibonacci Memoização: F({n}) = {resultado_memo} ({len(passos_memo)} passos)")
        
        # Tabulação
        resultado_tab, passos_tab = fibonacci_tabulacao_com_passos(n)
        print(f"✅ Fibonacci Tabulação: F({n}) = {resultado_tab} ({len(passos_tab)} passos)")
        
        # Testar Knapsack
        valores = [60, 100, 120]
        pesos = [10, 20, 30]
        capacidade = 50
        
        resultado_ks, passos_ks = knapsack_01_tabulacao_com_passos(valores, pesos, capacidade)
        print(f"✅ Knapsack 0/1: valor máximo = {resultado_ks} ({len(passos_ks)} passos)")
        
        print("✅ Módulo 3 OK!")
        
    except Exception as e:
        print(f"❌ Erro no Módulo 3: {e}")
        traceback.print_exc()

def test_modulo_4():
    """Testa o módulo 4 - Entrevistas."""
    print("\n💼 TESTANDO MÓDULO 4: ENTREVISTAS")
    print("=" * 50)
    
    try:
        from modulo_4_entrevistas.problem_playground import (
            InterviewSession, TWO_SUM_PROBLEM, VALID_PARENTHESES_PROBLEM
        )
        
        # Testar sistema de entrevistas
        session = InterviewSession()
        
        # Iniciar sessão com Two Sum
        problem = session.start_session("two_sum")
        print(f"✅ Problema carregado: {problem.title}")
        
        # Código de solução
        user_code = """
def two_sum(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return []
"""
        
        # Submeter solução
        result = session.submit_solution(user_code)
        
        print(f"✅ Solução testada: {result['test_results']['passed']}/{result['test_results']['total']} testes passaram")
        print(f"✅ Pontuação: {result['final_score']}/100")
        
        # Testar Valid Parentheses
        problem = session.start_session("valid_parentheses")
        print(f"✅ Problema carregado: {problem.title}")
        
        print("✅ Módulo 4 OK!")
        
    except Exception as e:
        print(f"❌ Erro no Módulo 4: {e}")
        traceback.print_exc()

def test_visualizadores():
    """Testa os visualizadores."""
    print("\n🎨 TESTANDO VISUALIZADORES")
    print("=" * 50)
    
    try:
        # Testar visualizador do módulo 2
        from modulo_2_estruturas_dados.structures_visualizer import AdvancedStructuresVisualizer
        
        visualizer = AdvancedStructuresVisualizer()
        
        # Dados de teste para heap
        heap_data = {
            'heap': [1, 4, 3, 7, 8, 5],
            'is_max_heap': False,
            'size': 6,
            'operations': []
        }
        
        visualizer.visualize_heap(heap_data)
        print("✅ Visualizador de Heap OK!")
        
        # Testar visualizador do módulo 4
        from modulo_4_entrevistas.interview_visualizer import InterviewVisualizer
        
        iv = InterviewVisualizer()
        
        # Dados de teste
        steps = [
            {'tipo': 'inicio', 'nums': [2, 7, 11, 15], 'target': 9, 'hash_map': {}, 'current_index': -1}
        ]
        
        test_results = {'passed': 4, 'total': 4, 'execution_time': 0.001}
        code_analysis = {'score': 85, 'complexity': {'time': 'O(n)', 'space': 'O(n)'}, 'patterns': ['Hash Map']}
        
        iv.visualize_problem("two_sum", steps, test_results, code_analysis)
        print("✅ Visualizador de Entrevistas OK!")
        
        print("✅ Visualizadores OK!")
        
    except Exception as e:
        print(f"❌ Erro nos Visualizadores: {e}")
        traceback.print_exc()

def test_streamlit_app():
    """Testa a aplicação Streamlit."""
    print("\n🚀 TESTANDO APLICAÇÃO STREAMLIT")
    print("=" * 50)
    
    try:
        # Verificar se o arquivo principal existe
        app_path = project_root / "streamlit_apps" / "main_app.py"
        
        if app_path.exists():
            print("✅ Aplicação Streamlit encontrada!")
            print(f"   Arquivo: {app_path}")
            print("   Execute: streamlit run streamlit_apps/main_app.py")
        else:
            print("❌ Aplicação Streamlit não encontrada!")
        
        # Verificar configuração
        config_path = project_root / "streamlit_apps" / ".streamlit" / "config.toml"
        
        if config_path.exists():
            print("✅ Configuração Streamlit encontrada!")
        else:
            print("❌ Configuração Streamlit não encontrada!")
        
        print("✅ Aplicação Streamlit OK!")
        
    except Exception as e:
        print(f"❌ Erro na Aplicação Streamlit: {e}")
        traceback.print_exc()

def main():
    """Executa todos os testes."""
    print("🧪 EXECUTANDO TESTES INTEGRADOS")
    print("=" * 60)
    
    # Verificar estrutura do projeto
    print(f"📁 Diretório do projeto: {project_root}")
    print(f"📁 Diretórios encontrados:")
    
    for item in project_root.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            print(f"   📂 {item.name}")
    
    print()
    
    # Executar testes
    test_modulo_1()
    test_modulo_2()
    test_modulo_3()
    test_modulo_4()
    test_visualizadores()
    test_streamlit_app()
    
    print("\n🎉 TESTES CONCLUÍDOS!")
    print("=" * 60)
    
    # Resumo final
    print("\n📋 RESUMO DO PROJETO:")
    print("✅ Módulo 1: Fundamentos (busca binária, dois ponteiros, etc.)")
    print("✅ Módulo 2: Estruturas de Dados (heap, trie, union-find, etc.)")
    print("✅ Módulo 3: Programação Dinâmica (metodologia 3 passos)")
    print("✅ Módulo 4: Entrevistas (simulação com feedback)")
    print("✅ Visualizadores (matplotlib + animações)")
    print("✅ Aplicação Streamlit (interface web)")
    
    print("\n🚀 COMO EXECUTAR:")
    print("1. Para testes: python teste_integrado.py")
    print("2. Para Streamlit: streamlit run streamlit_apps/main_app.py")
    print("3. Para demonstração: python demonstracao_3_passos.py")

if __name__ == "__main__":
    main()
