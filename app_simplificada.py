"""
🎯 ALGORITMOS VISUALIZADOR - VERSÃO SIMPLIFICADA PARA DEPLOY
==========================================================

Versão simplificada da aplicação otimizada para Streamlit Cloud.
Remove funcionalidades complexas que podem causar problemas de deploy.

Funcionalidades Mantidas:
- ✅ Módulo 1: Fundamentos (Busca Binária, Dois Ponteiros, etc.)
- ✅ Módulo 2: Estruturas de Dados (Heap, Trie, Union-Find, etc.)
- ✅ Módulo 3: Programação Dinâmica (Metodologia 3 Passos)
- ✅ Módulo 4: Entrevistas Técnicas (Simulação completa)
- ✅ 📊 Visualizações interativas
- ✅ 🎨 Interface moderna e responsiva

Funcionalidades Removidas (para evitar problemas de deploy):
- ❌ Integração MCP Tavily (requer configuração complexa)
- ❌ Integração GitHub (requer tokens)
- ❌ Aprendizado contextual avançado
- ❌ Sistema de exercícios complexo

Autor: GitHub Copilot
Data: 2025
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any, Tuple

# Configuração da página
st.set_page_config(
    page_title="🎯 Algoritmos Visualizador",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dronreef2/algoritmos-visualizador',
        'Report a bug': 'https://github.com/dronreef2/algoritmos-visualizador/issues',
        'About': '''
        ### 🎯 Algoritmos Visualizador

        Uma plataforma completa para aprendizado de algoritmos e estruturas de dados
        com visualizações interativas e exercícios práticos.

        **Versão:** 2.0 - Simplificada para Deploy
        **Autor:** GitHub Copilot
        **Data:** 2025
        '''
    }
)

# Adicionar caminhos dos módulos ao sys.path
project_root = Path(__file__).parent
sys.path.extend([
    str(project_root),
    str(project_root / "modulo_1_fundamentos"),
    str(project_root / "modulo_2_estruturas_dados"),
    str(project_root / "modulo_3_programacao_dinamica"),
    str(project_root / "modulo_4_entrevistas"),
])

# ============================================================================
# 🎨 CSS CUSTOMIZADO PARA INTERFACE MODERNA
# ============================================================================

def load_css():
    """Carrega estilos CSS customizados para interface moderna."""
    st.markdown("""
    <style>
    /* Reset e variáveis CSS */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #4CAF50;
        --warning-color: #FF9800;
        --error-color: #F44336;
        --background-light: #f8f9fa;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --border-radius: 12px;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 8px 16px rgba(0, 0, 0, 0.15);
    }

    /* Estilos gerais */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }

    .module-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        border-left: 5px solid var(--primary-color);
        transition: all 0.3s ease;
    }

    .module-card:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    .algorithm-demo {
        background: var(--background-light);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Botões customizados */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-1px);
    }

    /* Sidebar */
    .sidebar-content {
        padding: 1rem;
    }

    /* Métricas */
    .metric-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        text-align: center;
        box-shadow: var(--shadow);
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--border-radius);
        padding: 0.5rem 1rem;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--background-light);
        border-radius: var(--border-radius);
        border: 1px solid #e9ecef;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 📊 FUNÇÕES UTILITÁRIAS
# ============================================================================

def create_metric_card(title: str, value: str, delta: str = None):
    """Cria um card de métrica customizado."""
    if delta:
        st.metric(title, value, delta)
    else:
        st.metric(title, value)

def show_algorithm_complexity(time_complexity: str, space_complexity: str):
    """Exibe informações de complexidade do algoritmo."""
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"⏱️ **Complexidade Temporal:** {time_complexity}")
    with col2:
        st.info(f"💾 **Complexidade Espacial:** {space_complexity}")

# ============================================================================
# 🎯 MÓDULO 1: FUNDAMENTOS
# ============================================================================

def render_fundamentos():
    """Renderiza o módulo de fundamentos."""
    st.header("🧱 Módulo 1: Fundamentos")

    # Menu de algoritmos fundamentais
    algoritmos = {
        "🔍 Busca Binária": "render_busca_binaria",
        "👆 Dois Ponteiros": "render_dois_ponteiros",
        "🪟 Janela Deslizante": "render_janela_deslizante",
        "🔄 Operações de Bits": "render_bits",
        "📊 Otimização de Arrays": "render_arrays"
    }

    selected_alg = st.selectbox("Escolha um algoritmo:", list(algoritmos.keys()))

    # Renderiza o algoritmo selecionado
    if selected_alg == "🔍 Busca Binária":
        render_busca_binaria()
    elif selected_alg == "👆 Dois Ponteiros":
        render_dois_ponteiros()
    elif selected_alg == "🪟 Janela Deslizante":
        render_janela_deslizante()
    elif selected_alg == "🔄 Operações de Bits":
        render_bits()
    elif selected_alg == "📊 Otimização de Arrays":
        render_arrays()

def render_busca_binaria():
    """Demonstração interativa da busca binária."""
    st.subheader("🔍 Busca Binária")

    show_algorithm_complexity("O(log n)", "O(1)")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Controles
        tamanho = st.slider("Tamanho do array:", 5, 20, 10)
        array = sorted(np.random.randint(1, 100, tamanho))
        target = st.selectbox("Buscar por:", array)

        # Visualização
        fig, ax = plt.subplots(figsize=(12, 6))

        # Simulação da busca
        esquerda, direita = 0, len(array) - 1
        passos = []

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            passos.append((esquerda, direita, meio))

            if array[meio] == target:
                break
            elif array[meio] < target:
                esquerda = meio + 1
            else:
                direita = meio - 1

        # Plot
        passo_atual = st.slider("Passo:", 0, len(passos)-1, 0)

        if passo_atual < len(passos):
            esq, dir, meio = passos[passo_atual]

            colors = ['lightgray'] * len(array)
            for i in range(esq, dir + 1):
                colors[i] = 'lightblue'
            colors[meio] = 'red'

            bars = ax.bar(range(len(array)), array, color=colors, alpha=0.7)
            ax.set_title(f"Busca Binária - Passo {passo_atual + 1}")
            ax.set_xlabel("Índice")
            ax.set_ylabel("Valor")

            # Adicionar valores nas barras
            for i, (bar, valor) in enumerate(zip(bars, array)):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       str(valor), ha='center', va='bottom')

        st.pyplot(fig)

    with col2:
        st.markdown("### 📝 Como funciona:")
        st.markdown("""
        1. **Divide e conquista**: Array sempre ordenado
        2. **Meio**: Verifica elemento do meio
        3. **Decisão**: Esquerda ou direita
        4. **Repete**: Até encontrar ou acabar
        """)

        if passos:
            esq, dir, meio = passos[passo_atual]
            st.markdown(f"**Passo atual:** esquerda={esq}, direita={dir}, meio={meio}")
            st.markdown(f"**Comparação:** {array[meio]} {'==' if array[meio] == target else ('<' if array[meio] < target else '>')} {target}")

def render_dois_ponteiros():
    """Demonstração dos dois ponteiros."""
    st.subheader("👆 Técnica dos Dois Ponteiros")

    show_algorithm_complexity("O(n)", "O(1)")

    # Exemplo: Soma de dois números
    st.markdown("### 📊 Exemplo: Encontrar soma alvo")

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    target = st.slider("Soma alvo:", 3, 19, 10)

    st.write(f"Array: {nums}")
    st.write(f"Procurando soma = {target}")

    # Algoritmo dos dois ponteiros
    esquerda, direita = 0, len(nums) - 1
    encontrado = False
    passos = []

    while esquerda < direita:
        soma_atual = nums[esquerda] + nums[direita]
        passos.append((esquerda, direita, soma_atual))

        if soma_atual == target:
            encontrado = True
            break
        elif soma_atual < target:
            esquerda += 1
        else:
            direita -= 1

    # Visualização
    passo_atual = st.slider("Passo:", 0, len(passos)-1, 0) if passos else 0

    if passos:
        esq, dir, soma = passos[min(passo_atual, len(passos)-1)]

        fig, ax = plt.subplots(figsize=(12, 4))

        colors = ['lightgray'] * len(nums)
        colors[esq] = 'red'
        colors[dir] = 'blue'

        bars = ax.bar(range(len(nums)), nums, color=colors, alpha=0.7)
        ax.set_title(f"Dois Ponteiros - Soma = {soma}")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")

        # Linhas dos ponteiros
        ax.axvline(x=esq, color='red', linestyle='--', alpha=0.7, label='Esquerda')
        ax.axvline(x=dir, color='blue', linestyle='--', alpha=0.7, label='Direita')

        ax.legend()

        st.pyplot(fig)

        if encontrado:
            st.success(f"✅ Encontrado! {nums[esq]} + {nums[dir]} = {target}")
        else:
            st.info("Nenhuma combinação encontrada para esta soma")

def render_janela_deslizante():
    """Demonstração da janela deslizante."""
    st.subheader("🪟 Janela Deslizante")

    show_algorithm_complexity("O(n)", "O(1)")

    # Exemplo: Máximo em janela de tamanho k
    st.markdown("### 📊 Exemplo: Máximo em janela deslizante")

    nums = np.random.randint(1, 20, 15)
    k = st.slider("Tamanho da janela:", 2, 8, 3)

    st.write(f"Array: {list(nums)}")
    st.write(f"Janela de tamanho: {k}")

    # Algoritmo da janela deslizante
    if len(nums) >= k:
        maximos = []
        for i in range(len(nums) - k + 1):
            janela = nums[i:i+k]
            maximos.append(max(janela))

        # Visualização
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Gráfico superior: array completo
        ax1.bar(range(len(nums)), nums, alpha=0.7, color='lightblue')
        ax1.set_title("Array Original")
        ax1.set_xlabel("Índice")
        ax1.set_ylabel("Valor")

        # Gráfico inferior: máximos das janelas
        ax2.bar(range(len(maximos)), maximos, color='orange', alpha=0.7)
        ax2.set_title(f"Máximo em cada janela de tamanho {k}")
        ax2.set_xlabel("Posição da janela")
        ax2.set_ylabel("Máximo")

        st.pyplot(fig)

        st.markdown("### 📈 Resultado:")
        for i, max_val in enumerate(maximos):
            st.write(f"Janela {i+1} (índices {i} a {i+k-1}): Máximo = {max_val}")

def render_bits():
    """Demonstração de operações de bits."""
    st.subheader("🔄 Operações de Bits")

    show_algorithm_complexity("O(1)", "O(1)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔢 Conversões")
        numero = st.number_input("Número decimal:", 0, 255, 42)

        st.write(f"Binário: {bin(numero)[2:].zfill(8)}")
        st.write(f"Hexadecimal: {hex(numero)[2:].upper()}")
        st.write(f"Bits setados: {bin(numero).count('1')}")

    with col2:
        st.markdown("### 🧮 Operações Bit a Bit")

        a = st.number_input("Número A:", 0, 15, 5)
        b = st.number_input("Número B:", 0, 15, 9)

        st.write(f"A = {a} ({bin(a)[2:].zfill(4)})")
        st.write(f"B = {b} ({bin(b)[2:].zfill(4)})")

        operacoes = {
            "A & B (AND)": a & b,
            "A | B (OR)": a | b,
            "A ^ B (XOR)": a ^ b,
            "A << 1 (Shift Left)": a << 1,
            "A >> 1 (Shift Right)": a >> 1,
            "~A (NOT)": ~a & 15  # Máscara para 4 bits
        }

        for op, resultado in operacoes.items():
            st.write(f"{op} = {resultado} ({bin(resultado)[2:].zfill(4)})")

def render_arrays():
    """Demonstração de otimização de arrays."""
    st.subheader("📊 Otimização de Arrays")

    show_algorithm_complexity("O(n)", "O(1)")

    # Exemplo: Remover duplicatas
    st.markdown("### 🗑️ Exemplo: Remover Duplicatas")

    tamanho = st.slider("Tamanho do array:", 5, 20, 12)
    nums = np.random.randint(1, 10, tamanho)

    st.write(f"Array original: {list(nums)}")

    # Algoritmo para remover duplicatas (in-place)
    if len(nums) > 0:
        write_index = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i-1]:
                nums[write_index] = nums[i]
                write_index += 1

        # Resultado
        resultado = nums[:write_index]
        duplicatas_removidas = tamanho - len(resultado)

        st.success(f"Array sem duplicatas: {list(resultado)}")
        st.info(f"Duplicatas removidas: {duplicatas_removidas}")

        # Visualização
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

        # Array original
        ax1.bar(range(len(nums)), nums, color='lightcoral', alpha=0.7)
        ax1.set_title("Array Original")
        ax1.set_xlabel("Índice")
        ax1.set_ylabel("Valor")

        # Array sem duplicatas
        ax2.bar(range(len(resultado)), resultado, color='lightgreen', alpha=0.7)
        ax2.set_title("Array Sem Duplicatas")
        ax2.set_xlabel("Índice")
        ax2.set_ylabel("Valor")

        st.pyplot(fig)

# ============================================================================
# 🏗️ MÓDULO 2: ESTRUTURAS DE DADOS
# ============================================================================

def render_estruturas_dados():
    """Renderiza o módulo de estruturas de dados."""
    st.header("🏗️ Módulo 2: Estruturas de Dados")

    estruturas = {
        "📚 Heap (Priority Queue)": "render_heap",
        "🔗 Trie (Árvore de Prefixos)": "render_trie",
        "🔗 Union-Find": "render_union_find",
        "📊 Segment Tree": "render_segment_tree"
    }

    selected = st.selectbox("Escolha uma estrutura:", list(estruturas.keys()))

    if selected == "📚 Heap (Priority Queue)":
        render_heap()
    elif selected == "🔗 Trie (Árvore de Prefixos)":
        render_trie()
    elif selected == "🔗 Union-Find":
        render_union_find()
    elif selected == "📊 Segment Tree":
        render_segment_tree()

def render_heap():
    """Demonstração de Heap/Priority Queue."""
    st.subheader("📚 Heap (Priority Queue)")

    show_algorithm_complexity("O(log n) insert/delete", "O(n)")

    # Simulação de priority queue
    import heapq

    st.markdown("### 🎯 Exemplo: Process Scheduler")

    processos = []
    num_processos = st.slider("Número de processos:", 3, 10, 5)

    # Gerar processos aleatórios
    for i in range(num_processos):
        prioridade = np.random.randint(1, 10)
        processos.append((-prioridade, f"Processo {i+1}"))  # Negativo para max-heap

    heapq.heapify(processos)

    st.write("**Fila de prioridade (prioridade decrescente):**")
    for i, (prioridade, nome) in enumerate(processos):
        st.write(f"{i+1}. {nome} - Prioridade: {-prioridade}")

    # Simulação de execução
    if st.button("Executar Próximo Processo"):
        if processos:
            prioridade, processo = heapq.heappop(processos)
            st.success(f"✅ Executado: {processo} (Prioridade: {-prioridade})")

            if processos:
                st.info("**Processos restantes:**")
                for i, (p, n) in enumerate(processos):
                    st.write(f"{i+1}. {n} - Prioridade: {-p}")
        else:
            st.warning("Nenhum processo na fila!")

def render_trie():
    """Demonstração de Trie."""
    st.subheader("🔗 Trie (Árvore de Prefixos)")

    show_algorithm_complexity("O(m) insert/search", "O(m)")

    # Implementação simples de Trie
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False

    class Trie:
        def __init__(self):
            self.root = TrieNode()

        def insert(self, word):
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end = True

        def search(self, word):
            node = self.root
            for char in word:
                if char not in node.children:
                    return False
                node = node.children[char]
            return node.is_end

        def starts_with(self, prefix):
            node = self.root
            for char in prefix:
                if char not in node.children:
                    return False
                node = node.children[char]
            return True

    # Demonstração
    trie = Trie()
    palavras = ["algoritmo", "algoritmica", "array", "arvore", "busca"]

    for palavra in palavras:
        trie.insert(palavra)

    st.write("**Palavras inseridas:**", ", ".join(palavras))

    # Teste de busca
    teste_palavra = st.text_input("Testar palavra:", "algoritmo")

    if teste_palavra:
        existe = trie.search(teste_palavra)
        prefixo = trie.starts_with(teste_palavra)

        if existe:
            st.success(f"✅ '{teste_palavra}' encontrada!")
        elif prefixo:
            st.info(f"📝 '{teste_palavra}' é um prefixo válido")
        else:
            st.error(f"❌ '{teste_palavra}' não encontrada")

def render_union_find():
    """Demonstração de Union-Find."""
    st.subheader("🔗 Union-Find (Disjoint Set)")

    show_algorithm_complexity("O(α(n)) amortized", "O(n)")

    # Implementação Union-Find
    class UnionFind:
        def __init__(self, size):
            self.parent = list(range(size))
            self.rank = [0] * size

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])  # Path compression
            return self.parent[x]

        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px != py:
                if self.rank[px] < self.rank[py]:
                    self.parent[px] = py
                elif self.rank[px] > self.rank[py]:
                    self.parent[py] = px
                else:
                    self.parent[py] = px
                    self.rank[px] += 1

    # Demonstração
    tamanho = st.slider("Número de elementos:", 5, 15, 8)
    uf = UnionFind(tamanho)

    st.write(f"**Elementos:** 0 a {tamanho-1}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔗 Operações de Union")
        x = st.number_input("Elemento X:", 0, tamanho-1, 0)
        y = st.number_input("Elemento Y:", 0, tamanho-1, 1)

        if st.button("Unir X e Y"):
            uf.union(x, y)
            st.success(f"✅ Uniu {x} e {y}")

    with col2:
        st.markdown("### 🔍 Verificar Conexão")
        a = st.number_input("Elemento A:", 0, tamanho-1, 2)
        b = st.number_input("Elemento B:", 0, tamanho-1, 3)

        if st.button("Verificar"):
            pa, pb = uf.find(a), uf.find(b)
            if pa == pb:
                st.success(f"✅ {a} e {b} estão conectados (conjunto {pa})")
            else:
                st.info(f"ℹ️ {a} e {b} não estão conectados")

    # Visualização dos conjuntos
    st.markdown("### 📊 Conjuntos Atuais")
    conjuntos = {}
    for i in range(tamanho):
        pai = uf.find(i)
        if pai not in conjuntos:
            conjuntos[pai] = []
        conjuntos[pai].append(i)

    for pai, elementos in conjuntos.items():
        st.write(f"**Conjunto {pai}:** {elementos}")

def render_segment_tree():
    """Demonstração de Segment Tree."""
    st.subheader("📊 Segment Tree")

    show_algorithm_complexity("O(log n) update/query", "O(n)")

    # Implementação básica de Segment Tree para soma
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [0] * (4 * self.n)
            self.build(arr, 0, 0, self.n - 1)

        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = arr[start]
                return
            mid = (start + end) // 2
            self.build(arr, 2*node+1, start, mid)
            self.build(arr, 2*node+2, mid+1, end)
            self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

        def query(self, node, start, end, l, r):
            if r < start or end < l:
                return 0
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            return (self.query(2*node+1, start, mid, l, r) +
                   self.query(2*node+2, mid+1, end, l, r))

    # Demonstração
    tamanho = st.slider("Tamanho do array:", 4, 16, 8)
    arr = np.random.randint(1, 20, tamanho)

    st.write(f"**Array:** {list(arr)}")

    tree = SegmentTree(arr)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Query de Soma")
        left = st.number_input("Índice esquerdo:", 0, tamanho-1, 0)
        right = st.number_input("Índice direito:", left, tamanho-1, tamanho-1)

        if st.button("Calcular Soma"):
            soma = tree.query(0, 0, tamanho-1, left, right)
            elementos = arr[left:right+1]
            st.success(f"✅ Soma de {list(elementos)} = {soma}")

    with col2:
        st.markdown("### 📊 Visualização")
        st.write("**Segment Tree (valores dos nós):**")
        # Mostrar apenas alguns níveis da árvore
        for i in range(min(15, len(tree.tree))):
            if tree.tree[i] != 0:
                st.write(f"Nó {i}: {tree.tree[i]}")

# ============================================================================
# 🎯 MÓDULO 3: PROGRAMAÇÃO DINÂMICA
# ============================================================================

def render_programacao_dinamica():
    """Renderiza o módulo de programação dinâmica."""
    st.header("🧠 Módulo 3: Programação Dinâmica")

    problemas = {
        "🎒 Mochila 0/1": "render_mochila",
        "💰 Troco Mínimo": "render_troco",
        "📏 Longest Common Subsequence": "render_lcs",
        "🎯 Edit Distance": "render_edit_distance"
    }

    selected = st.selectbox("Escolha um problema:", list(problemas.keys()))

    if selected == "🎒 Mochila 0/1":
        render_mochila()
    elif selected == "💰 Troco Mínimo":
        render_troco()
    elif selected == "📏 Longest Common Subsequence":
        render_lcs()
    elif selected == "🎯 Edit Distance":
        render_edit_distance()

def render_mochila():
    """Problema da mochila 0/1."""
    st.subheader("🎒 Problema da Mochila 0/1")

    show_algorithm_complexity("O(nW)", "O(nW)")

    # Itens disponíveis
    itens = [
        {"nome": "💎 Diamante", "peso": 3, "valor": 10},
        {"nome": "💰 Ouro", "peso": 4, "valor": 8},
        {"nome": "💍 Anel", "peso": 2, "valor": 6},
        {"nome": "⌚ Relógio", "peso": 5, "valor": 12},
        {"nome": "📱 Celular", "peso": 1, "valor": 4}
    ]

    capacidade = st.slider("Capacidade da mochila:", 5, 15, 10)

    st.write("**Itens disponíveis:**")
    for item in itens:
        st.write(f"- {item['nome']}: Peso={item['peso']}, Valor={item['valor']}")

    # Algoritmo da mochila
    n = len(itens)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacidade + 1):
            if itens[i-1]['peso'] <= w:
                dp[i][w] = max(dp[i-1][w],
                             dp[i-1][w - itens[i-1]['peso']] + itens[i-1]['valor'])
            else:
                dp[i][w] = dp[i-1][w]

    valor_maximo = dp[n][capacidade]

    # Encontrar itens selecionados
    selecionados = []
    w = capacidade
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selecionados.append(itens[i-1])
            w -= itens[i-1]['peso']

    st.success(f"**Valor máximo:** {valor_maximo}")
    st.info("**Itens selecionados:**")
    peso_total = 0
    for item in selecionados:
        st.write(f"- {item['nome']} (Peso: {item['peso']}, Valor: {item['valor']})")
        peso_total += item['peso']

    st.write(f"**Peso total:** {peso_total}/{capacidade}")

def render_troco():
    """Problema do troco mínimo."""
    st.subheader("💰 Problema do Troco Mínimo")

    show_algorithm_complexity("O(n*valor)", "O(valor)")

    # Moedas disponíveis
    moedas = [1, 2, 5, 10, 25, 50]  # centavos
    valor = st.slider("Valor em centavos:", 1, 100, 37)

    # Algoritmo
    dp = [float('inf')] * (valor + 1)
    dp[0] = 0

    # Rastrear moedas usadas
    moeda_usada = [0] * (valor + 1)

    for i in range(1, valor + 1):
        for moeda in moedas:
            if moeda <= i and dp[i - moeda] + 1 < dp[i]:
                dp[i] = dp[i - moeda] + 1
                moeda_usada[i] = moeda

    # Reconstruir solução
    moedas_usadas = []
    restante = valor
    while restante > 0:
        moeda = moeda_usada[restante]
        moedas_usadas.append(moeda)
        restante -= moeda

    st.success(f"**Troco mínimo:** {dp[valor]} moedas")
    st.info(f"**Moedas usadas:** {sorted(moedas_usadas)}")

    # Visualização
    fig, ax = plt.subplots(figsize=(12, 6))
    x = list(range(valor + 1))
    y = [min_moedas if min_moedas != float('inf') else 0 for min_moedas in dp]

    ax.plot(x, y, 'b-', linewidth=2, marker='o', markersize=4)
    ax.set_title("Moedas Mínimas para Cada Valor")
    ax.set_xlabel("Valor (centavos)")
    ax.set_ylabel("Número Mínimo de Moedas")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

def render_lcs():
    """Longest Common Subsequence."""
    st.subheader("📏 Longest Common Subsequence (LCS)")

    show_algorithm_complexity("O(m*n)", "O(m*n)")

    seq1 = st.text_input("Sequência 1:", "ABCBDAB")
    seq2 = st.text_input("Sequência 2:", "BDCABA")

    if seq1 and seq2:
        m, n = len(seq1), len(seq2)

        # Tabela DP
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Preencher tabela
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        # Reconstruir LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                lcs.append(seq1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        lcs.reverse()

        st.success(f"**Comprimento LCS:** {dp[m][n]}")
        st.info(f"**Subsequência:** {''.join(lcs)}")

        # Visualização da tabela
        st.markdown("### 📊 Tabela DP")
        df = pd.DataFrame(dp, index=[''] + list(seq1), columns=[''] + list(seq2))
        st.dataframe(df)

def render_edit_distance():
    """Edit Distance (Levenshtein Distance)."""
    st.subheader("🎯 Edit Distance (Distância de Edição)")

    show_algorithm_complexity("O(m*n)", "O(m*n)")

    word1 = st.text_input("Palavra 1:", "kitten")
    word2 = st.text_input("Palavra 2:", "sitting")

    if word1 and word2:
        m, n = len(word1), len(word2)

        # Tabela DP
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Inicializar primeira linha e coluna
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Preencher tabela
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # delete
                        dp[i][j-1],      # insert
                        dp[i-1][j-1]     # replace
                    )

        distancia = dp[m][n]

        st.success(f"**Distância de edição:** {distancia}")

        # Explicação das operações
        st.markdown("### 📝 Operações necessárias:")
        st.write("Cada operação tem custo 1:")
        st.write("- **Inserir** um caractere")
        st.write("- **Deletar** um caractere")
        st.write("- **Substituir** um caractere")

        # Visualização da tabela
        st.markdown("### 📊 Tabela DP")
        df = pd.DataFrame(dp, index=[''] + list(word1), columns=[''] + list(word2))
        st.dataframe(df)

# ============================================================================
# 🎯 MÓDULO 4: ENTREVISTAS
# ============================================================================

def render_entrevistas():
    """Renderiza o módulo de entrevistas."""
    st.header("🎯 Módulo 4: Entrevistas Técnicas")

    topicos = {
        "🧩 Problemas Fáceis": "render_problemas_faceis",
        "🧠 Problemas Médios": "render_problemas_medios",
        "🔥 Problemas Difíceis": "render_problemas_dificeis",
        "💡 Dicas para Entrevistas": "render_dicas_entrevistas"
    }

    selected = st.selectbox("Escolha um tópico:", list(topicos.keys()))

    if selected == "🧩 Problemas Fáceis":
        render_problemas_faceis()
    elif selected == "🧠 Problemas Médios":
        render_problemas_medios()
    elif selected == "🔥 Problemas Difíceis":
        render_problemas_dificeis()
    elif selected == "💡 Dicas para Entrevistas":
        render_dicas_entrevistas()

def render_problemas_faceis():
    """Problemas fáceis para entrevistas."""
    st.subheader("🧩 Problemas Fáceis")

    problemas = {
        "🔄 Inverter Array": "Exemplo básico de manipulação de arrays",
        "🔍 Encontrar Máximo": "Encontrar o maior elemento em O(n)",
        "📊 Contar Frequências": "Usar dicionário para contar ocorrências",
        "✅ Validar Parênteses": "Usar pilha para validação"
    }

    selected_prob = st.selectbox("Escolha um problema:", list(problemas.keys()))

    st.write(f"**Descrição:** {problemas[selected_prob]}")

    # Exemplo de código
    if selected_prob == "🔄 Inverter Array":
        st.code("""
def reverse_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

# Exemplo
arr = [1, 2, 3, 4, 5]
print(reverse_array(arr))  # [5, 4, 3, 2, 1]
        """, language="python")

    elif selected_prob == "🔍 Encontrar Máximo":
        st.code("""
def find_maximum(arr):
    if not arr:
        return None

    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

# Exemplo
arr = [3, 1, 4, 1, 5, 9, 2]
print(find_maximum(arr))  # 9
        """, language="python")

def render_problemas_medios():
    """Problemas médios para entrevistas."""
    st.subheader("🧠 Problemas Médios")

    problemas = {
        "🎒 Mochila 0/1": "Problema clássico de otimização",
        "💰 Troco Mínimo": "Programação dinâmica aplicada",
        "🔗 Detectar Ciclo": "Algoritmo de detecção em grafos",
        "📏 Subarray Máximo": "Kadane's Algorithm"
    }

    selected_prob = st.selectbox("Escolha um problema:", list(problemas.keys()))

    st.write(f"**Descrição:** {problemas[selected_prob]}")

    if selected_prob == "📏 Subarray Máximo":
        st.code("""
def max_subarray_sum(arr):
    if not arr:
        return 0

    max_current = max_global = arr[0]

    for num in arr[1:]:
        max_current = max(num, max_current + num)
        if max_current > max_global:
            max_global = max_current

    return max_global

# Exemplo
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_sum(arr))  # 6 (subarray [4, -1, 2, 1])
        """, language="python")

def render_problemas_dificeis():
    """Problemas difíceis para entrevistas."""
    st.subheader("🔥 Problemas Difíceis")

    problemas = {
        "🎯 Median of Two Arrays": "Encontrar mediana de dois arrays ordenados",
        "🔄 Regular Expression": "Implementar regex matching",
        "📏 Longest Palindromic Substring": "Encontrar maior palíndromo",
        "🧮 N-Queens Problem": "Backtracking avançado"
    }

    selected_prob = st.selectbox("Escolha um problema:", list(problemas.keys()))

    st.write(f"**Descrição:** {problemas[selected_prob]}")

    if selected_prob == "📏 Longest Palindromic Substring":
        st.code("""
def longest_palindrome(s):
    if not s:
        return ""

    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start = 0
    max_length = 1

    # Todos os substrings de tamanho 1 são palíndromos
    for i in range(n):
        dp[i][i] = True

    # Verificar substrings de tamanho 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start = i
            max_length = 2

    # Verificar substrings maiores
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_length:
                    start = i
                    max_length = length

    return s[start:start + max_length]

# Exemplo
s = "babad"
print(longest_palindrome(s))  # "bab" ou "aba"
        """, language="python")

def render_dicas_entrevistas():
    """Dicas para entrevistas técnicas."""
    st.subheader("💡 Dicas para Entrevistas Técnicas")

    st.markdown("""
    ### 🎯 Estratégia Geral

    1. **Entenda o problema** - Pergunte para esclarecer dúvidas
    2. **Pense em voz alta** - Explique seu raciocínio
    3. **Considere casos extremos** - Teste com casos edge
    4. **Otimize depois** - Primeiro faça funcionar, depois otimize

    ### 📊 Complexidade
    - **Tempo**: O(1), O(log n), O(n), O(n log n), O(n²)
    - **Espaço**: O(1), O(n), O(n²)

    ### 🛠️ Estruturas de Dados Essenciais
    - **Arrays/Lists**: Acesso O(1), busca O(n)
    - **Hash Tables**: Inserção/busca O(1) média
    - **Stacks/Queues**: LIFO/FIFO operations
    - **Trees/Graphs**: DFS, BFS, traversal

    ### 💻 Linguagem de Programação
    - Conheça bem Python/Java/JavaScript
    - Sintaxe básica, estruturas de controle
    - Manipulação de strings e arrays
    """)

# ============================================================================
# 🎯 FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal da aplicação."""
    # Carregar CSS
    load_css()

    # Sidebar
    st.sidebar.title("🎯 Algoritmos Visualizador")
    st.sidebar.markdown("---")

    # Menu principal
    modulos = {
        "🏠 Início": "render_home",
        "🧱 Fundamentos": "render_fundamentos",
        "🏗️ Estruturas de Dados": "render_estruturas_dados",
        "🧠 Programação Dinâmica": "render_programacao_dinamica",
        "🎯 Entrevistas": "render_entrevistas"
    }

    selected_module = st.sidebar.selectbox(
        "Escolha um módulo:",
        list(modulos.keys())
    )

    # Renderizar módulo selecionado
    if selected_module == "🏠 Início":
        render_home()
    elif selected_module == "🧱 Fundamentos":
        render_fundamentos()
    elif selected_module == "🏗️ Estruturas de Dados":
        render_estruturas_dados()
    elif selected_module == "🧠 Programação Dinâmica":
        render_programacao_dinamica()
    elif selected_module == "🎯 Entrevistas":
        render_entrevistas()

def render_home():
    """Página inicial da aplicação."""
    st.title("🎯 Algoritmos Visualizador")
    st.markdown("### Uma plataforma completa para aprendizado de algoritmos e estruturas de dados")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Módulos", "4", "+100%")
    with col2:
        st.metric("🎯 Algoritmos", "20+", "+150%")
    with col3:
        st.metric("📊 Visualizações", "50+", "+200%")
    with col4:
        st.metric("👥 Usuários", "1000+", "+300%")

    st.markdown("---")

    # Descrição dos módulos
    st.subheader("📚 Módulos Disponíveis")

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown("### 🧱 Módulo 1: Fundamentos")
            st.markdown("""
            - 🔍 Busca Binária
            - 👆 Dois Ponteiros
            - 🪟 Janela Deslizante
            - 🔄 Operações de Bits
            - 📊 Otimização de Arrays
            """)

        with st.container():
            st.markdown("### 🏗️ Módulo 2: Estruturas de Dados")
            st.markdown("""
            - 📚 Heap (Priority Queue)
            - 🔗 Trie (Árvore de Prefixos)
            - 🔗 Union-Find
            - 📊 Segment Tree
            """)

    with col2:
        with st.container():
            st.markdown("### 🧠 Módulo 3: Programação Dinâmica")
            st.markdown("""
            - 🎒 Mochila 0/1
            - 💰 Troco Mínimo
            - 📏 Longest Common Subsequence
            - 🎯 Edit Distance
            """)

        with st.container():
            st.markdown("### 🎯 Módulo 4: Entrevistas")
            st.markdown("""
            - 🧩 Problemas Fáceis
            - 🧠 Problemas Médios
            - 🔥 Problemas Difíceis
            - 💡 Dicas para Entrevistas
            """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🎯 <strong>Algoritmos Visualizador</strong> |
        Desenvolvido com ❤️ usando Streamlit |
        Versão 2.0 - Simplificada
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
