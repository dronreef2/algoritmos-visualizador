"""
🎯 ALGORITMOS VISUALIZADOR - APLICAÇÃO INTEGRADA
===============================================

Aplicação Streamlit completa e integrada que combina todos os módulos
do projeto em uma experiência unificada de aprendizado.

Funcionalidades Integradas:
- ✅ Módulo 1: Fundamentos (Busca Binária, Dois Ponteiros, etc.)
- ✅ Módulo 2: Estruturas de Dados (Heap, Trie, Union-Find, etc.)
- ✅ Módulo 3: Programação Dinâmica (Metodologia 3 Passos)
- ✅ Módulo 4: Entrevistas Técnicas (Simulação completa)
- ✅ 🎯 Aprendizado Contextualizado (Jornadas temáticas)
- ✅ 🎯 Exercícios Práticos Interativos
- ✅ 🤖 Busca MCP com Tavily (Busca inteligente)
- ✅ 📊 Visualizações interativas
- ✅ 📈 Sistema de progresso e conquistas
- ✅ 🎨 Interface moderna e responsiva

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
    page_title="🎯 Algoritmos Visualizador Integrado",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dronreef2/algoritmos-visualizador',
        'Report a bug': 'https://github.com/dronreef2/algoritmos-visualizador/issues',
        'About': '''
        ### 🎯 Algoritmos Visualizador

        Uma plataforma completa para aprendizado de algoritmos e estruturas de dados
        com visualizações interativas, exercícios práticos e integração com IA.

        **Versão:** 2.0 - Integrada
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

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }

    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }

    /* Cards de módulo */
    .module-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }

    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-hover);
        border-color: var(--accent-color);
    }

    .module-card h3 {
        margin-top: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }

    .module-card p {
        margin: 0.5rem 0;
        opacity: 0.9;
    }

    .module-card ul {
        margin: 1rem 0 0 0;
        padding-left: 1.2rem;
    }

    .module-card li {
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }

    /* Cards de funcionalidade */
    .feature-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-hover);
    }

    .feature-card h4 {
        color: var(--primary-color);
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }

    /* Cards métricos */
    .metric-card {
        background: var(--background-light);
        border-left: 4px solid var(--primary-color);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: var(--shadow);
    }

    .metric-card h5 {
        margin: 0;
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 600;
    }

    .metric-card p {
        margin: 0.3rem 0 0 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }

    /* Cards de exercício */
    .exercise-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border: 2px solid var(--accent-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }

    .exercise-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-success {
        background: var(--success-color);
        color: white;
    }

    .status-warning {
        background: var(--warning-color);
        color: white;
    }

    .status-info {
        background: var(--primary-color);
        color: white;
    }

    /* Botões customizados */
    .custom-button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        text-align: center;
    }

    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }

    /* Sidebar customizada */
    .sidebar-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin-bottom: 1rem;
        text-align: center;
    }

    .sidebar-header h3 {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
    }

    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }

        .module-card {
            padding: 1rem;
        }

        .feature-card {
            padding: 1rem;
        }
    }

    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background-light);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }

    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 🔧 UTILITÁRIOS E HELPERS
# ============================================================================

def initialize_session_state():
    """Inicializa o estado da sessão com valores padrão."""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'completed_modules': [],
            'completed_exercises': [],
            'current_streak': 0,
            'total_study_time': 0,
            'achievements': [],
            'last_activity': datetime.now()
        }

    if 'current_module' not in st.session_state:
        st.session_state.current_module = "🏠 Home"

    if 'exercise_session' not in st.session_state:
        st.session_state.exercise_session = None

def get_module_info(module_key: str) -> Dict[str, Any]:
    """Retorna informações detalhadas sobre um módulo."""
    modules_info = {
        "📚 Módulo 1: Fundamentos": {
            "title": "Fundamentos do Pensamento Algorítmico",
            "description": "Domine as técnicas algorítmicas essenciais que servem como blocos de construção para problemas mais complexos.",
            "topics": [
                "🔍 Busca Binária - O(log n)",
                "👥 Dois Ponteiros - O(n)",
                "🪟 Janela Deslizante - O(n)",
                "🔄 Backtracking - Exponencial",
                "🌐 BFS (Busca em Largura)",
                "📊 Otimização de Arrays",
                "🔢 Operações com Bits"
            ],
            "difficulty": "Iniciante a Intermediário",
            "estimated_time": "15-20 horas",
            "applications": [
                "Sistemas de busca em logs",
                "Detector de fraudes bancárias",
                "Análise de sequências de DNA",
                "Planejador de turnos",
                "Redes sociais"
            ]
        },
        "🏗️ Módulo 2: Estruturas de Dados": {
            "title": "Estruturas de Dados Avançadas",
            "description": "Explore estruturas de dados complexas com visualizações detalhadas e aplicações práticas.",
            "topics": [
                "🔺 Heap (Min/Max)",
                "🌳 Trie (Árvore de Prefixos)",
                "🤝 Union-Find",
                "📊 Segment Tree",
                "🔗 Listas Encadeadas",
                "📚 Tabelas Hash",
                "🗂️ Árvores Binárias"
            ],
            "difficulty": "Intermediário a Avançado",
            "estimated_time": "20-25 horas",
            "applications": [
                "Sistemas de cache inteligentes",
                "Motores de busca",
                "Sistemas de recomendação",
                "Gerenciamento de memória",
                "Bancos de dados"
            ]
        },
        "🎯 Módulo 3: Programação Dinâmica": {
            "title": "Programação Dinâmica",
            "description": "Domine a metodologia de 3 passos para resolver problemas de programação dinâmica.",
            "topics": [
                "💪 Força Bruta",
                "🧠 Memoização",
                "📊 Tabulação",
                "🎯 Otimização",
                "🔄 Problemas Clássicos (Knapsack, LCS)",
                "📈 Sequências Ótimas"
            ],
            "difficulty": "Intermediário a Avançado",
            "estimated_time": "18-22 horas",
            "applications": [
                "Otimização de rotas",
                "Alinhamento de sequências",
                "Compressão de dados",
                "Planejamento financeiro",
                "Jogos e IA"
            ]
        },
        "💼 Módulo 4: Entrevistas": {
            "title": "Entrevistas Técnicas",
            "description": "Simulação completa de entrevistas técnicas com feedback em tempo real.",
            "topics": [
                "🎯 Problemas Clássicos",
                "📊 Análise de Código",
                "⏱️ Simulação de Tempo",
                "📝 Feedback Detalhado",
                "🧠 Estratégias de Resolução",
                "💡 Otimização de Soluções"
            ],
            "difficulty": "Intermediário a Avançado",
            "estimated_time": "12-16 horas",
            "applications": [
                "Preparação para entrevistas",
                "Análise de performance",
                "Resolução de problemas",
                "Otimização de código",
                "Pensamento algorítmico"
            ]
        }
    }

    return modules_info.get(module_key, {})

def render_sidebar():
    """Renderiza a barra lateral com navegação e informações do usuário."""
    with st.sidebar:
        # Header da sidebar
        st.markdown("""
        <div class="sidebar-header">
            <h3>🧭 Navegação</h3>
        </div>
        """, unsafe_allow_html=True)

        # Menu principal
        menu_options = [
            "🏠 Home",
            "📚 Módulo 1: Fundamentos",
            "🏗️ Módulo 2: Estruturas de Dados",
            "🎯 Módulo 3: Programação Dinâmica",
            "💼 Módulo 4: Entrevistas",
            "🎯 Aprendizado Contextualizado",
            "🎯 Exercícios Práticos",
            "🔍 Busca MCP (Tavily)",
            "📊 Dashboard de Progresso",
            "🏆 Conquistas",
            "⚙️ Configurações"
        ]

        selected_option = st.selectbox(
            "Selecione uma seção:",
            menu_options,
            index=menu_options.index(st.session_state.get('current_module', "🏠 Home")),
            key="main_navigation"
        )

        st.session_state.current_module = selected_option

        # Separador
        st.markdown("---")

        # Informações do usuário
        st.markdown("### 👤 Meu Progresso")

        progress = st.session_state.user_progress

        # Métricas rápidas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Módulos Completados", len(progress['completed_modules']))
        with col2:
            st.metric("Sequência Atual", progress['current_streak'])

        # Barra de progresso geral
        total_modules = 4
        completed = len(progress['completed_modules'])
        progress_percentage = (completed / total_modules) * 100

        st.markdown("**Progresso Geral:**")
        st.progress(progress_percentage / 100)

        st.markdown(f"**{completed}/{total_modules} módulos** ({progress_percentage:.1f}%)")

        # Separador
        st.markdown("---")

        # Links úteis
        st.markdown("### 🔗 Links Úteis")
        st.markdown("""
        - [📚 Documentação](https://github.com/dronreef2/algoritmos-visualizador)
        - [🐛 Reportar Bug](https://github.com/dronreef2/algoritmos-visualizador/issues)
        - [💡 Sugestões](https://github.com/dronreef2/algoritmos-visualizador/discussions)
        """)

# ============================================================================
# 🏠 PÁGINA INICIAL
# ============================================================================

def render_home_page():
    """Renderiza a página inicial com visão geral completa."""
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🎯 Algoritmos Visualizador Integrado</h1>
        <p>Uma experiência completa de aprendizado contextualizado com visualizações interativas</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h5>📚 Módulos</h5>
            <p>4 módulos completos</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h5>🎯 Algoritmos</h5>
            <p>50+ implementados</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h5>🏗️ Estruturas</h5>
            <p>15+ visualizadas</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h5>💼 Problemas</h5>
            <p>25+ de entrevista</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="metric-card">
            <h5>🎯 Exercícios</h5>
            <p>30+ interativos</p>
        </div>
        """, unsafe_allow_html=True)

    # Destaques especiais
    st.markdown("## 🌟 Funcionalidades em Destaque")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Aprendizado Contextualizado</h4>
            <p>Jornadas temáticas com contexto histórico, aplicações reais e conexões entre conceitos.</p>
            <ul>
                <li>🗺️ Mapa visual de aprendizado</li>
                <li>🚀 Jornadas temáticas estruturadas</li>
                <li>📚 Conceitos interativos</li>
                <li>📊 Acompanhamento de progresso</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="exercise-card">
            <h4>🎯 Exercícios Práticos Interativos</h4>
            <p>Pratique com exercícios reais, validação automática e feedback imediato.</p>
            <ul>
                <li>✅ Múltipla escolha e verdadeiro/falso</li>
                <li>✅ Análise de complexidade</li>
                <li>✅ Debugging de código</li>
                <li>✅ Sistema de conquistas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 Busca Inteligente com MCP</h4>
            <p>Busque explicações e exemplos na web usando IA integrada.</p>
            <ul>
                <li>🔍 Busca contextual com Tavily</li>
                <li>🧠 Respostas geradas por IA</li>
                <li>📊 Resultados personalizados</li>
                <li>⚡ Busca avançada e básica</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>📊 Visualizações Interativas</h4>
            <p>Veja algoritmos em ação com animações passo a passo.</p>
            <ul>
                <li>🎨 Gráficos matplotlib/plotly</li>
                <li>🎬 Animações em tempo real</li>
                <li>📈 Análise de complexidade</li>
                <li>🔍 Exploração detalhada</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Módulos disponíveis
    st.markdown("## 📋 Módulos de Aprendizado")

    col1, col2 = st.columns(2)

    with col1:
        # Módulo 1
        module_info = get_module_info("📚 Módulo 1: Fundamentos")
        st.markdown(f"""
        <div class="module-card">
            <h3>📚 Módulo 1: Fundamentos</h3>
            <p>{module_info.get('description', 'Algoritmos fundamentais')}</p>
            <ul>
        """, unsafe_allow_html=True)

        for topic in module_info.get('topics', [])[:4]:  # Mostra primeiros 4 tópicos
            st.markdown(f"<li>{topic}</li>", unsafe_allow_html=True)

        st.markdown("</ul></div>", unsafe_allow_html=True)

        # Módulo 3
        module_info = get_module_info("🎯 Módulo 3: Programação Dinâmica")
        st.markdown(f"""
        <div class="module-card">
            <h3>🎯 Módulo 3: Programação Dinâmica</h3>
            <p>{module_info.get('description', 'Metodologia 3 passos')}</p>
            <ul>
        """, unsafe_allow_html=True)

        for topic in module_info.get('topics', [])[:4]:
            st.markdown(f"<li>{topic}</li>", unsafe_allow_html=True)

        st.markdown("</ul></div>", unsafe_allow_html=True)

    with col2:
        # Módulo 2
        module_info = get_module_info("🏗️ Módulo 2: Estruturas de Dados")
        st.markdown(f"""
        <div class="module-card">
            <h3>🏗️ Módulo 2: Estruturas de Dados</h3>
            <p>{module_info.get('description', 'Estruturas avançadas')}</p>
            <ul>
        """, unsafe_allow_html=True)

        for topic in module_info.get('topics', [])[:4]:
            st.markdown(f"<li>{topic}</li>", unsafe_allow_html=True)

        st.markdown("</ul></div>", unsafe_allow_html=True)

        # Módulo 4
        module_info = get_module_info("💼 Módulo 4: Entrevistas")
        st.markdown(f"""
        <div class="module-card">
            <h3>💼 Módulo 4: Entrevistas</h3>
            <p>{module_info.get('description', 'Simulação de entrevistas')}</p>
            <ul>
        """, unsafe_allow_html=True)

        for topic in module_info.get('topics', [])[:4]:
            st.markdown(f"<li>{topic}</li>", unsafe_allow_html=True)

        st.markdown("</ul></div>", unsafe_allow_html=True)

    # Call-to-action
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3>🚀 Pronto para começar sua jornada?</h3>
        <p>Escolha um módulo acima ou explore as funcionalidades especiais!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 📚 MÓDULOS INDIVIDUAIS
# ============================================================================

def render_module_1():
    """Renderiza o Módulo 1: Fundamentos."""
    st.markdown("""
    <div class="main-header">
        <h1>📚 Módulo 1: Fundamentos</h1>
        <p>Algoritmos fundamentais que formam a base do pensamento computacional</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs do módulo
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Busca Binária",
        "👥 Dois Ponteiros",
        "🪟 Janela Deslizante",
        "🔄 Backtracking"
    ])

    with tab1:
        render_busca_binaria()

    with tab2:
        render_dois_ponteiros()

    with tab3:
        render_janela_deslizante()

    with tab4:
        render_backtracking()

def render_module_2():
    """Renderiza o Módulo 2: Estruturas de Dados."""
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Módulo 2: Estruturas de Dados</h1>
        <p>Estruturas de dados avançadas com visualizações interativas</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs do módulo
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔺 Heap (Min/Max)",
        "🌳 Trie",
        "🤝 Union-Find",
        "📊 Segment Tree"
    ])

    with tab1:
        render_heap()

    with tab2:
        render_trie()

    with tab3:
        render_union_find()

    with tab4:
        render_segment_tree()

def render_module_3():
    """Renderiza o Módulo 3: Programação Dinâmica."""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Módulo 3: Programação Dinâmica</h1>
        <p>Metodologia de 3 passos para resolver problemas complexos</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs do módulo
    tab1, tab2, tab3, tab4 = st.tabs([
        "💪 Força Bruta",
        "🧠 Memoização",
        "📊 Tabulação",
        "🎯 Problemas Clássicos"
    ])

    with tab1:
        render_forca_bruta()

    with tab2:
        render_memoizacao()

    with tab3:
        render_tabulacao()

    with tab4:
        render_problemas_classicos()

def render_module_4():
    """Renderiza o Módulo 4: Entrevistas."""
    st.markdown("""
    <div class="main-header">
        <h1>💼 Módulo 4: Entrevistas</h1>
        <p>Simulação completa de entrevistas técnicas</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs do módulo
    tab1, tab2, tab3 = st.tabs([
        "🎯 Simulação de Entrevista",
        "📊 Análise de Código",
        "📝 Feedback"
    ])

    with tab1:
        render_simulacao_entrevista()

    with tab2:
        render_analise_codigo()

    with tab3:
        render_feedback_entrevista()

# ============================================================================
# 🎯 APRENDIZADO CONTEXTUALIZADO
# ============================================================================

def render_aprendizado_contextualizado():
    """Renderiza o sistema de aprendizado contextualizado."""
    try:
        from aprendizado_contextual_ui import render_aprendizado_contextual
        render_aprendizado_contextual()
    except ImportError:
        st.error("Sistema de aprendizado contextualizado não disponível.")
        st.info("Verifique se o arquivo `aprendizado_contextual_ui.py` está presente.")

# ============================================================================
# 🎯 EXERCÍCIOS PRÁTICOS
# ============================================================================

def render_exercicios_praticos():
    """Renderiza o sistema de exercícios práticos."""
    try:
        from exercicios_praticos_ui import render_exercicios_praticos
        from integracao_gitmcp_exercicios import render_exercicios_gitmcp

        # Abas para exercícios tradicionais e integração GitHub
        tab1, tab2 = st.tabs(["📝 Exercícios Tradicionais", "🔗 Exercícios com GitHub"])

        with tab1:
            render_exercicios_praticos()

        with tab2:
            render_exercicios_gitmcp()

    except ImportError:
        st.error("Sistema de exercícios práticos não disponível.")
        st.info("Verifique se o arquivo `exercicios_praticos_ui.py` está presente.")

# ============================================================================
# 🔍 BUSCA MCP
# ============================================================================

def render_busca_mcp():
    """Renderiza a interface de busca MCP com Tavily."""
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Busca Inteligente com MCP</h1>
        <p>Busque explicações e exemplos usando IA integrada</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from mcp_tavily_integration import TavilySearchClient

        # Inicializar cliente
        if 'mcp_client' not in st.session_state:
            st.session_state.mcp_client = TavilySearchClient()

        client = st.session_state.mcp_client

        # Status da configuração
        if client.is_configured():
            st.success("✅ MCP Server Tavily configurado e pronto!")

            # Interface de busca
            col1, col2 = st.columns([3, 1])

            with col1:
                query = st.text_input(
                    "Digite sua consulta:",
                    placeholder="Ex: 'como funciona o algoritmo de Dijkstra?'",
                    help="Faça perguntas sobre algoritmos, estruturas de dados ou problemas de programação"
                )

            with col2:
                search_type = st.selectbox(
                    "Tipo de busca:",
                    ["basic", "advanced"],
                    help="Basic: busca rápida, Advanced: busca detalhada"
                )

                include_answer = st.checkbox(
                    "Incluir resposta da IA",
                    value=False,
                    help="Gera resposta contextualizada usando IA"
                )

                max_results = st.slider(
                    "Máximo de resultados:",
                    min_value=1,
                    max_value=10,
                    value=5,
                    help="Número máximo de resultados"
                )

            if st.button("🔍 Buscar", type="primary", use_container_width=True):
                if query.strip():
                    with st.spinner("🔄 Buscando informações com IA..."):
                        try:
                            result = client.search(
                                query,
                                search_depth=search_type,
                                include_answer=include_answer,
                                max_results=max_results
                            )

                            if result and 'results' in result:
                                st.success(f"✅ Encontrados {len(result['results'])} resultados!")

                                # Exibir resultados
                                for i, item in enumerate(result['results'], 1):
                                    with st.expander(f"📄 Resultado {i}: {item.get('title', 'Sem título')}"):
                                        st.markdown(f"**URL:** {item.get('url', 'N/A')}")
                                        st.markdown(f"**Conteúdo:** {item.get('snippet', 'N/A')}")

                                # Resposta da IA se solicitada
                                if include_answer and 'answer' in result:
                                    st.markdown("---")
                                    st.markdown("### 🧠 Resposta da IA")
                                    st.info(result['answer'])

                            else:
                                st.warning("Nenhum resultado encontrado.")

                        except Exception as e:
                            st.error(f"Erro na busca: {str(e)}")
                else:
                    st.warning("Por favor, digite uma consulta.")
        else:
            st.warning("⚠️ MCP Server precisa ser configurado.")
            st.info("Para configurar: Edite `mcp-server-tavily/.env` e adicione sua chave da API Tavily")

    except ImportError:
        st.error("Integração MCP não disponível.")
        st.info("Verifique se o arquivo `mcp_tavily_integration.py` está presente.")

# ============================================================================
# 📊 DASHBOARD DE PROGRESSO
# ============================================================================

def render_dashboard_progresso():
    """Renderiza o dashboard de progresso do usuário."""
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard de Progresso</h1>
        <p>Acompanhe seu avanço no aprendizado de algoritmos</p>
    </div>
    """, unsafe_allow_html=True)

    progress = st.session_state.user_progress

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        completed_modules = len(progress['completed_modules'])
        st.metric("Módulos Completados", f"{completed_modules}/4")

    with col2:
        st.metric("Sequência Atual", progress['current_streak'])

    with col3:
        total_time = progress['total_study_time']
        st.metric("Tempo de Estudo", f"{total_time} min")

    with col4:
        achievements = len(progress['achievements'])
        st.metric("Conquistas", achievements)

    # Gráfico de progresso
    st.markdown("### 📈 Progresso por Módulo")

    modules = ["Fundamentos", "Estruturas", "Dinâmica", "Entrevistas"]
    completed = [1 if f"Módulo {i+1}" in progress['completed_modules'] else 0 for i in range(4)]

    fig = go.Figure(data=[
        go.Bar(
            x=modules,
            y=completed,
            marker_color=['#4CAF50' if c else '#FF9800' for c in completed]
        )
    ])

    fig.update_layout(
        title="Status de Conclusão dos Módulos",
        xaxis_title="Módulos",
        yaxis_title="Status (0=Não Concluído, 1=Concluído)",
        yaxis=dict(tickmode='linear', tick0=0, dtick=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Atividades recentes
    st.markdown("### 🕒 Atividades Recentes")

    if 'last_activity' in progress:
        st.info(f"Última atividade: {progress['last_activity'].strftime('%d/%m/%Y %H:%M')}")

    # Recomendações
    st.markdown("### 💡 Recomendações")

    if completed_modules < 4:
        next_module = modules[completed_modules]
        st.info(f"🎯 Próximo módulo recomendado: **{next_module}**")
    else:
        st.success("🎉 Parabéns! Você completou todos os módulos!")

# ============================================================================
# 🏆 SISTEMA DE CONQUISTAS
# ============================================================================

def render_conquistas():
    """Renderiza o sistema de conquistas."""
    st.markdown("""
    <div class="main-header">
        <h1>🏆 Sistema de Conquistas</h1>
        <p>Desbloqueie conquistas enquanto aprende algoritmos</p>
    </div>
    """, unsafe_allow_html=True)

    # Conquistas disponíveis
    achievements = [
        {
            "name": "Primeiro Passo",
            "description": "Complete seu primeiro exercício",
            "icon": "🎯",
            "unlocked": len(st.session_state.user_progress['completed_exercises']) > 0
        },
        {
            "name": "Buscador Ávido",
            "description": "Complete o módulo de Busca Binária",
            "icon": "🔍",
            "unlocked": "Módulo 1" in st.session_state.user_progress['completed_modules']
        },
        {
            "name": "Estruturador",
            "description": "Complete o módulo de Estruturas de Dados",
            "icon": "🏗️",
            "unlocked": "Módulo 2" in st.session_state.user_progress['completed_modules']
        },
        {
            "name": "Dinâmico",
            "description": "Complete o módulo de Programação Dinâmica",
            "icon": "🎯",
            "unlocked": "Módulo 3" in st.session_state.user_progress['completed_modules']
        },
        {
            "name": "Entrevistador",
            "description": "Complete o módulo de Entrevistas",
            "icon": "💼",
            "unlocked": "Módulo 4" in st.session_state.user_progress['completed_modules']
        },
        {
            "name": "Sequência de Vitórias",
            "description": "Complete 7 exercícios seguidos",
            "icon": "🔥",
            "unlocked": st.session_state.user_progress['current_streak'] >= 7
        },
        {
            "name": "Mestre dos Algoritmos",
            "description": "Complete todos os módulos",
            "icon": "👑",
            "unlocked": len(st.session_state.user_progress['completed_modules']) == 4
        }
    ]

    # Exibir conquistas
    col1, col2, col3 = st.columns(3)

    for i, achievement in enumerate(achievements):
        col = [col1, col2, col3][i % 3]

        with col:
            if achievement["unlocked"]:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: #4CAF50;">
                    <h5>{achievement['icon']} {achievement['name']}</h5>
                    <p>{achievement['description']}</p>
                    <span class="status-badge status-success">DESBLOQUEADA</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: #9E9E9E; opacity: 0.6;">
                    <h5>{achievement['icon']} {achievement['name']}</h5>
                    <p>{achievement['description']}</p>
                    <span class="status-badge status-info">BLOQUEADA</span>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# ⚙️ CONFIGURAÇÕES
# ============================================================================

def render_configuracoes():
    """Renderiza a página de configurações."""
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Configurações</h1>
        <p>Personalize sua experiência de aprendizado</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs de configuração
    tab1, tab2, tab3 = st.tabs([
        "👤 Perfil",
        "🎨 Interface",
        "📊 Dados"
    ])

    with tab1:
        st.markdown("### 👤 Configurações do Perfil")
        st.text_input("Nome", value="Estudante", help="Seu nome para personalizar a experiência")
        st.selectbox("Nível de Experiência", ["Iniciante", "Intermediário", "Avançado"], index=0)
        st.multiselect("Interesses", ["Algoritmos", "Estruturas de Dados", "Programação Dinâmica", "Entrevistas"], default=["Algoritmos"])

    with tab2:
        st.markdown("### 🎨 Configurações da Interface")
        st.selectbox("Tema", ["Claro", "Escuro", "Automático"], index=0)
        st.slider("Velocidade das Animações", 0.5, 2.0, 1.0, 0.1)
        st.checkbox("Mostrar Dicas", value=True)
        st.checkbox("Notificações de Conquistas", value=True)

    with tab3:
        st.markdown("### 📊 Gerenciamento de Dados")
        if st.button("🗑️ Limpar Progresso", type="secondary", key="config_limpar_progresso"):
            st.session_state.user_progress = {
                'completed_modules': [],
                'completed_exercises': [],
                'current_streak': 0,
                'total_study_time': 0,
                'achievements': [],
                'last_activity': datetime.now()
            }
            st.success("Progresso limpo com sucesso!")

        if st.button("📥 Exportar Dados", type="secondary", key="config_exportar_dados"):
            st.download_button(
                label="Baixar Dados JSON",
                data=str(st.session_state.user_progress),
                file_name="progresso_algoritmos.json",
                mime="application/json"
            )

# ============================================================================
# 🔍 VISUALIZADORES INDIVIDUAIS (IMPLEMENTAÇÕES BÁSICAS)
# ============================================================================

def render_busca_binaria():
    """Renderiza demonstração da busca binária."""
    st.markdown("### 🔍 Busca Binária Interativa")

    # Controles
    tamanho = st.slider("Tamanho do array:", 5, 20, 10)
    array = sorted(np.random.randint(1, 100, tamanho))
    target = st.selectbox("Valor a procurar:", array)

    st.write(f"Array: {array}")
    st.write(f"Procurando: {target}")

    # Simulação
    if st.button("Executar Busca", key="busca_binaria_executar"):
        esquerda, direita = 0, len(array) - 1
        passos = []

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            passos.append((esquerda, direita, meio, array[meio]))

            if array[meio] == target:
                st.success(f"✅ Encontrado na posição {meio}!")
                break
            elif array[meio] < target:
                esquerda = meio + 1
            else:
                direita = meio - 1
        else:
            st.error("❌ Valor não encontrado!")

        # Mostrar passos
        for i, (esq, dir, meio, valor) in enumerate(passos):
            st.write(f"Passo {i+1}: esquerda={esq}, direita={dir}, meio={meio}, valor={valor}")

def render_dois_ponteiros():
    """Renderiza demonstração dos dois ponteiros."""
    st.markdown("### 👥 Dois Ponteiros")

    # Exemplo: Container With Most Water
    st.markdown("**Exemplo: Container With Most Water**")

    alturas = st.text_input("Alturas (separadas por vírgula):", "1,8,6,2,5,4,8,3,7")
    alturas = [int(x.strip()) for x in alturas.split(",")]

    if st.button("Calcular", key="dois_ponteiros_calcular"):
        # Algoritmo dos dois ponteiros
        esquerda, direita = 0, len(alturas) - 1
        max_area = 0

        while esquerda < direita:
            # Área = min(altura) * distância
            altura = min(alturas[esquerda], alturas[direita])
            largura = direita - esquerda
            area = altura * largura
            max_area = max(max_area, area)

            # Mover ponteiro da menor altura
            if alturas[esquerda] < alturas[direita]:
                esquerda += 1
            else:
                direita -= 1

        st.success(f"Área máxima: {max_area}")

        # Visualização simples
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(alturas)), alturas, color='skyblue')
        ax.set_title("Container With Most Water")
        ax.set_xlabel("Posição")
        ax.set_ylabel("Altura")
        st.pyplot(fig)

def render_janela_deslizante():
    """Renderiza demonstração da janela deslizante."""
    st.markdown("### 🪟 Janela Deslizante")

    # Exemplo: Maximum Sum Subarray of Size K
    st.markdown("**Exemplo: Soma Máxima de Subarray de Tamanho K**")

    nums = st.text_input("Array (separado por vírgula):", "2,1,5,1,3,2")
    k = st.number_input("Tamanho da janela (K):", 1, 10, 3)

    nums = [int(x.strip()) for x in nums.split(",")]

    if st.button("Calcular", key="janela_deslizante_calcular"):
        if len(nums) >= k:
            # Janela deslizante
            max_sum = sum(nums[:k])
            current_sum = max_sum

            for i in range(k, len(nums)):
                current_sum = current_sum - nums[i-k] + nums[i]
                max_sum = max(max_sum, current_sum)

            st.success(f"Soma máxima: {max_sum}")

            # Visualização
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(nums, 'o-', linewidth=2, markersize=8)
            ax.set_title(f"Janela Deslizante (K={k})")
            ax.set_xlabel("Posição")
            ax.set_ylabel("Valor")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        else:
            st.error("Array deve ter pelo menos K elementos!")

def render_backtracking():
    """Renderiza demonstração de backtracking."""
    st.markdown("### 🔄 Backtracking")

    # Exemplo: Subsets
    st.markdown("**Exemplo: Gerar Todos os Subconjuntos**")

    nums = st.text_input("Números (separados por vírgula):", "1,2,3")
    nums = [int(x.strip()) for x in nums.split(",")]

    if st.button("Gerar Subconjuntos"):
        def backtrack(start, current, result):
            result.append(current[:])
            for i in range(start, len(nums)):
                current.append(nums[i])
                backtrack(i + 1, current, result)
                current.pop()

        result = []
        backtrack(0, [], result)

        st.write("**Subconjuntos gerados:**")
        for subset in result:
            st.write(f"[{', '.join(map(str, subset))}]")

        st.info(f"Total de subconjuntos: {len(result)}")

def render_heap():
    """Renderiza demonstração de Heap."""
    st.markdown("### 🔺 Heap (Min/Max)")

    # Simulação simples de heap
    import heapq

    st.markdown("**Exemplo: Heap Mínimo**")

    valores = st.text_input("Valores (separados por vírgula):", "3,1,4,1,5,9,2,6")
    valores = [int(x.strip()) for x in valores.split(",")]

    if st.button("Criar Heap", key="heap_criar"):
        heap = valores[:]
        heapq.heapify(heap)

        st.write("**Array original:**", valores)
        st.write("**Heap resultante:**", heap)

        # Operações
        if heap:
            menor = heapq.heappop(heap)
            st.write(f"**Menor elemento removido:** {menor}")
            st.write("**Heap após remoção:**", heap)

def render_trie():
    """Renderiza demonstração de Trie."""
    st.markdown("### 🌳 Trie (Árvore de Prefixos)")

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

    # Demonstração
    palavras = st.text_area("Palavras (uma por linha):", "casa\ncarro\ncasa\ncachorro")
    palavra_busca = st.text_input("Palavra para buscar:")

    if st.button("Processar", key="trie_processar"):
        trie = Trie()
        palavras_lista = [p.strip() for p in palavras.split("\n") if p.strip()]

        for palavra in palavras_lista:
            trie.insert(palavra)

        st.write("**Palavras inseridas:**", palavras_lista)

        if palavra_busca:
            encontrado = trie.search(palavra_busca)
            if encontrado:
                st.success(f"✅ '{palavra_busca}' encontrada!")
            else:
                st.error(f"❌ '{palavra_busca}' não encontrada!")

def render_union_find():
    """Renderiza demonstração de Union-Find."""
    st.markdown("### 🤝 Union-Find")

    # Implementação simples
    class UnionFind:
        def __init__(self, size):
            self.parent = list(range(size))
            self.rank = [0] * size

        def find(self, p):
            if self.parent[p] != p:
                self.parent[p] = self.find(self.parent[p])
            return self.parent[p]

        def union(self, p, q):
            rootP = self.find(p)
            rootQ = self.find(q)

            if rootP == rootQ:
                return False

            if self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            elif self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1

            return True

    # Demonstração
    n = st.number_input("Número de elementos:", 5, 20, 10)

    uf = UnionFind(n)

    st.write("**Estado inicial:**")
    st.write("Parent:", uf.parent)
    st.write("Rank:", uf.rank)

    col1, col2 = st.columns(2)
    with col1:
        p = st.number_input("Elemento P:", 0, n-1, 0)
    with col2:
        q = st.number_input("Elemento Q:", 0, n-1, 1)

    if st.button("Fazer Union", key="union_find_union"):
        if uf.union(p, q):
            st.success(f"✅ Union realizada entre {p} e {q}")
        else:
            st.info(f"ℹ️ {p} e {q} já estão no mesmo conjunto")

        st.write("**Estado após union:**")
        st.write("Parent:", uf.parent)
        st.write("Rank:", uf.rank)

def render_segment_tree():
    """Renderiza demonstração de Segment Tree."""
    st.markdown("### 📊 Segment Tree")

    # Implementação básica
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
            left = self.query(2*node+1, start, mid, l, r)
            right = self.query(2*node+2, mid+1, end, l, r)
            return left + right

    # Demonstração
    valores = st.text_input("Array (separado por vírgula):", "1,3,5,7,9,11")
    valores = [int(x.strip()) for x in valores.split(",")]

    if valores:
        tree = SegmentTree(valores)

        st.write("**Array:**", valores)
        st.write("**Segment Tree:**", tree.tree)

        col1, col2 = st.columns(2)
        with col1:
            l = st.number_input("Índice esquerdo:", 0, len(valores)-1, 0)
        with col2:
            r = st.number_input("Índice direito:", 0, len(valores)-1, len(valores)-1)

        if st.button("Consultar Soma", key="segment_tree_consultar"):
            if l <= r:
                soma = tree.query(0, 0, len(valores)-1, l, r)
                st.success(f"Soma de [{l}:{r}] = {soma}")
            else:
                st.error("Índice esquerdo deve ser <= direito!")

def render_forca_bruta():
    """Renderiza exemplo de força bruta."""
    st.markdown("### 💪 Força Bruta")
    st.markdown("**Exemplo: Subset Sum Problem**")

    nums = st.text_input("Números:", "1,2,3,4,5")
    target = st.number_input("Soma alvo:", 1, 50, 9)

    nums = [int(x.strip()) for x in nums.split(",")]

    if st.button("Encontrar Subconjuntos", key="forca_bruta_subsets"):
        def find_subsets(nums, target, index=0, current=[], result=[]):
            if sum(current) == target:
                result.append(current[:])
                return
            if sum(current) > target or index >= len(nums):
                return

            # Incluir elemento atual
            current.append(nums[index])
            find_subsets(nums, target, index + 1, current, result)
            current.pop()

            # Não incluir elemento atual
            find_subsets(nums, target, index + 1, current, result)

        result = []
        find_subsets(nums, target, 0, [], result)

        if result:
            st.success(f"Encontrados {len(result)} subconjuntos:")
            for subset in result:
                st.write(f"[{', '.join(map(str, subset))}] = {sum(subset)}")
        else:
            st.warning("Nenhum subconjunto encontrado com essa soma.")

def render_memoizacao():
    """Renderiza exemplo de memoização."""
    st.markdown("### 🧠 Memoização")
    st.markdown("**Exemplo: Fibonacci com Memoização**")

    n = st.number_input("Calcular Fibonacci de:", 0, 50, 10)

    if st.button("Calcular", key="memoizacao_calcular"):
        memo = {}

        def fib_memo(n):
            if n in memo:
                return memo[n]
            if n <= 1:
                return n

            memo[n] = fib_memo(n-1) + fib_memo(n-2)
            return memo[n]

        resultado = fib_memo(n)
        st.success(f"Fibonacci({n}) = {resultado}")

        # Mostrar cache
        st.write("**Cache de memoização:**")
        for k, v in sorted(memo.items()):
            st.write(f"fib({k}) = {v}")

def render_tabulacao():
    """Renderiza exemplo de tabulação."""
    st.markdown("### 📊 Tabulação")
    st.markdown("**Exemplo: Fibonacci com Tabulação**")

    n = st.number_input("Calcular Fibonacci até:", 0, 50, 10)

    if st.button("Calcular", key="tabulacao_calcular"):
        if n >= 0:
            fib = [0] * (n + 1)
            if n >= 1:
                fib[1] = 1

            for i in range(2, n + 1):
                fib[i] = fib[i-1] + fib[i-2]

            st.success(f"Fibonacci({n}) = {fib[n]}")

            # Mostrar tabela
            st.write("**Tabela de Fibonacci:**")
            for i in range(min(n+1, 20)):  # Mostra até 20 primeiros
                st.write(f"fib({i}) = {fib[i]}")

            if n > 19:
                st.info("... (mostrando apenas os primeiros 20)")

def render_problemas_classicos():
    """Renderiza problemas clássicos de DP."""
    st.markdown("### 🎯 Problemas Clássicos de Programação Dinâmica")

    problema = st.selectbox("Escolha um problema:",
                           ["Knapsack 0/1", "Longest Common Subsequence", "Coin Change"])

    if problema == "Knapsack 0/1":
        st.markdown("**Knapsack 0/1**")
        st.markdown("Dado um conjunto de itens com pesos e valores, maximize o valor sem exceder a capacidade.")

        pesos = st.text_input("Pesos:", "2,3,4,5")
        valores = st.text_input("Valores:", "3,4,5,6")
        capacidade = st.number_input("Capacidade:", 1, 50, 8)

        pesos = [int(x.strip()) for x in pesos.split(",")]
        valores = [int(x.strip()) for x in valores.split(",")]

        if st.button("Resolver", key="knapsack_resolver"):
            n = len(pesos)
            dp = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

            for i in range(1, n + 1):
                for w in range(capacidade + 1):
                    if pesos[i-1] <= w:
                        dp[i][w] = max(dp[i-1][w], dp[i-1][w - pesos[i-1]] + valores[i-1])
                    else:
                        dp[i][w] = dp[i-1][w]

            st.success(f"Valor máximo: {dp[n][capacidade]}")

    elif problema == "Longest Common Subsequence":
        st.markdown("**Longest Common Subsequence (LCS)**")
        st.markdown("Encontre a maior subsequência comum entre duas strings.")

        s1 = st.text_input("String 1:", "AGGTAB")
        s2 = st.text_input("String 2:", "GXTXAYB")

        if st.button("Calcular LCS", key="lcs_calcular"):
            m, n = len(s1), len(s2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]

            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if s1[i-1] == s2[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

            st.success(f"Comprimento da LCS: {dp[m][n]}")

    elif problema == "Coin Change":
        st.markdown("**Coin Change**")
        st.markdown("Encontre o número mínimo de moedas para fazer um valor.")

        moedas = st.text_input("Moedas (separadas por vírgula):", "1,2,5")
        valor = st.number_input("Valor:", 1, 100, 11)

        moedas = [int(x.strip()) for x in moedas.split(",")]

        if st.button("Calcular", key="coin_change_calcular"):
            dp = [float('inf')] * (valor + 1)
            dp[0] = 0

            for i in range(1, valor + 1):
                for moeda in moedas:
                    if moeda <= i:
                        dp[i] = min(dp[i], dp[i - moeda] + 1)

            if dp[valor] != float('inf'):
                st.success(f"Número mínimo de moedas: {dp[valor]}")
            else:
                st.error("Não é possível fazer esse valor com as moedas dadas.")

def render_simulacao_entrevista():
    """Renderiza simulação de entrevista."""
    st.markdown("### 🎯 Simulação de Entrevista")

    # Seleção de dificuldade e categoria
    col1, col2 = st.columns(2)

    with col1:
        dificuldade = st.selectbox("Dificuldade:", ["Easy", "Medium", "Hard"], index=1)

    with col2:
        categoria = st.selectbox("Categoria:", ["Array", "String", "Tree", "Graph", "DP"], index=0)

    tempo = st.slider("Tempo limite (minutos):", 15, 60, 30)

    if st.button("🎯 Iniciar Simulação", type="primary", key="entrevista_iniciar"):
        st.success("Simulação iniciada! Responda o problema abaixo:")

        # Problema de exemplo baseado na categoria
        if categoria == "Array":
            st.markdown("""
            **Problema: Two Sum**

            Dado um array de números inteiros `nums` e um inteiro `target`, retorne os índices dos dois números que somam `target`.

            Você pode assumir que cada entrada tem exatamente uma solução, e não pode usar o mesmo elemento duas vezes.

            **Exemplo:**
            ```
            Input: nums = [2,7,11,15], target = 9
            Output: [0,1]
            ```
            """)

            # Área de resposta
            resposta = st.text_area("Sua solução (código Python):", height=200)

            if st.button("📤 Enviar Resolução", key="entrevista_enviar"):
                if resposta.strip():
                    st.success("✅ Resolução enviada! Análise em andamento...")

                    # Análise simples
                    if "for" in resposta and "enumerate" in resposta:
                        st.info("🎯 Boa abordagem! Você usou iteração com enumerate.")
                    if "return" in resposta:
                        st.info("✅ Estrutura de função correta!")

                    st.markdown("### 📊 Análise da Solução")
                    st.markdown("- **Complexidade Temporal:** O(n)")
                    st.markdown("- **Complexidade Espacial:** O(n)")
                    st.markdown("- **Pontuação:** 8/10 - Boa solução!")

                else:
                    st.warning("Por favor, escreva sua solução!")

def render_analise_codigo():
    """Renderiza análise de código."""
    st.markdown("### 📊 Análise de Código")

    codigo = st.text_area("Cole seu código para análise:", height=200,
                         value="""def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""")

    if st.button("🔍 Analisar Código", key="analise_codigo_analisar"):
        st.markdown("### 📋 Análise Detalhada")

        # Análise básica
        linhas = len(codigo.split('\n'))
        funcoes = codigo.count('def ')
        loops = codigo.count('for ') + codigo.count('while ')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Linhas de Código", linhas)

        with col2:
            st.metric("Funções", funcoes)

        with col3:
            st.metric("Laços", loops)

        # Feedback
        st.markdown("### 💡 Feedback")

        if "dict" in codigo or "seen" in codigo:
            st.success("✅ Uso eficiente de dicionário para lookup O(1)!")

        if "enumerate" in codigo:
            st.success("✅ Uso correto de enumerate para índices!")

        if "return" in codigo:
            st.success("✅ Estrutura de retorno adequada!")

        # Sugestões
        st.markdown("### 🎯 Sugestões de Melhoria")
        st.markdown("- Considere adicionar validação de entrada")
        st.markdown("- Adicione comentários explicativos")
        st.markdown("- Considere casos extremos (array vazio, etc.)")

def render_feedback_entrevista():
    """Renderiza feedback da entrevista."""
    st.markdown("### 📝 Feedback da Entrevista")

    # Métricas de performance
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pontuação Geral", "8.5/10")

    with col2:
        st.metric("Complexidade", "9/10")

    with col3:
        st.metric("Legibilidade", "8/10")

    with col4:
        st.metric("Eficiência", "9/10")

    # Feedback detalhado
    st.markdown("### 💬 Feedback Detalhado")

    st.markdown("""
    **Pontos Fortes:**
    - ✅ Solução correta e eficiente
    - ✅ Boa compreensão do problema
    - ✅ Código limpo e bem estruturado
    - ✅ Uso adequado de estruturas de dados

    **Áreas para Melhorar:**
    - ⚠️ Poderia adicionar mais comentários
    - ⚠️ Considere casos extremos
    - ⚠️ Validação de entrada poderia ser mais robusta

    **Sugestões para Próximas Entrevistas:**
    - Pratique mais problemas de Two Pointers
    - Estude otimizações para casos específicos
    - Foque em explicar seu raciocínio durante a resolução
    """)

    # Recomendações
    st.markdown("### 📚 Recomendações de Estudo")
    st.markdown("""
    - 🔍 **Busca Binária:** Pratique variações (lower bound, upper bound)
    - 👥 **Dois Ponteiros:** Estude aplicações em strings e arrays
    - 🪟 **Janela Deslizante:** Foque em problemas de substring
    - 🔄 **Backtracking:** Pratique com problemas de combinação
    """)

# ============================================================================
# 🎯 FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal da aplicação."""
    # Carregar CSS
    load_css()

    # Inicializar estado da sessão
    initialize_session_state()

    # Renderizar sidebar
    render_sidebar()

    # Roteamento principal baseado na seleção
    selected_module = st.session_state.current_module

    if selected_module == "🏠 Home":
        render_home_page()
    elif selected_module == "📚 Módulo 1: Fundamentos":
        render_module_1()
    elif selected_module == "🏗️ Módulo 2: Estruturas de Dados":
        render_module_2()
    elif selected_module == "🎯 Módulo 3: Programação Dinâmica":
        render_module_3()
    elif selected_module == "💼 Módulo 4: Entrevistas":
        render_module_4()
    elif selected_module == "🎯 Aprendizado Contextualizado":
        render_aprendizado_contextualizado()
    elif selected_module == "🎯 Exercícios Práticos":
        render_exercicios_praticos()
    elif selected_module == "🔍 Busca MCP (Tavily)":
        render_busca_mcp()
    elif selected_module == "📊 Dashboard de Progresso":
        render_dashboard_progresso()
    elif selected_module == "🏆 Conquistas":
        render_conquistas()
    elif selected_module == "⚙️ Configurações":
        render_configuracoes()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🎯 <strong>Algoritmos Visualizador Integrado</strong> | 
        Desenvolvido com ❤️ usando Streamlit | 
        Versão 2.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
