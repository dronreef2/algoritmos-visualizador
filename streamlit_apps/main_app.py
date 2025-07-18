"""
🎮 STREAMLIT APPS - COMPONENTES MODULARES
=========================================

Este diretório contém aplicações Streamlit modulares para visualização
de algoritmos e estruturas de dados.

Estrutura:
- components/: Componentes reutilizáveis
- pages/: Páginas individuais por módulo
- utils/: Utilitários compartilhados
- config/: Configurações globais

Padrão de Arquitetura:
- Player: Controles de interação (sliders, botões)
- Renderer: Visualizações (gráficos, animações)
- Controller: Lógica de negócio
- Model: Dados e estado
"""

import streamlit as st
from pathlib import Path
import sys

# Adicionar diretórios dos módulos ao path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "modulo_1_fundamentos"))
sys.path.append(str(project_root / "modulo_2_estruturas_dados"))
sys.path.append(str(project_root / "modulo_3_programacao_dinamica"))
sys.path.append(str(project_root / "modulo_4_entrevistas"))

# ============================================================================
# 📋 CONFIGURAÇÃO PRINCIPAL
# ============================================================================

def setup_page_config():
    """Configura a página principal do Streamlit."""
    st.set_page_config(
        page_title="🎯 Algoritmos Visualizador",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #2E86AB;
        margin-bottom: 2rem;
    }
    
    .module-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        margin: 0.5rem 0;
    }
    
    .algorithm-step {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #1976d2;
    }
    
    .complexity-badge {
        background: #4caf50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    
    .warning-badge {
        background: #ff9800;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    
    .error-badge {
        background: #f44336;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Função principal da aplicação."""
    setup_page_config()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        🎯 Algoritmos Visualizador
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para navegação
    st.sidebar.title("🧭 Navegação")
    
    # Seleção de módulo
    module = st.sidebar.selectbox(
        "Selecione o Módulo",
        [
            "🏠 Home",
            "📚 Módulo 1: Fundamentos",
            "🏗️ Módulo 2: Estruturas de Dados",
            "🎯 Módulo 3: Programação Dinâmica",
            "💼 Módulo 4: Entrevistas"
        ]
    )
    
    # Roteamento baseado na seleção
    if module == "🏠 Home":
        render_home_page()
    elif module == "📚 Módulo 1: Fundamentos":
        render_module_1()
    elif module == "🏗️ Módulo 2: Estruturas de Dados":
        render_module_2()
    elif module == "🎯 Módulo 3: Programação Dinâmica":
        render_module_3()
    elif module == "💼 Módulo 4: Entrevistas":
        render_module_4()

def render_home_page():
    """Renderiza a página inicial."""
    st.markdown("""
    ## 🎉 Bem-vindo ao Algoritmos Visualizador!
    
    Uma plataforma interativa para aprender algoritmos e estruturas de dados
    através de visualizações dinâmicas e exercícios práticos.
    """)
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Módulos", "4", "Completos")
    
    with col2:
        st.metric("🎯 Algoritmos", "50+", "Implementados")
    
    with col3:
        st.metric("🏗️ Estruturas", "15+", "Visualizadas")
    
    with col4:
        st.metric("💼 Problemas", "25+", "de Entrevista")
    
    # Cards dos módulos
    st.markdown("### 📋 Módulos Disponíveis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="module-card">
            <h3>📚 Módulo 1: Fundamentos</h3>
            <p>Algoritmos fundamentais como busca binária, dois ponteiros, 
            janela deslizante e operações com bits.</p>
            <ul>
                <li>🔍 Busca Binária</li>
                <li>👥 Dois Ponteiros</li>
                <li>🪟 Janela Deslizante</li>
                <li>🔢 Operações com Bits</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
            <h3>🎯 Módulo 3: Programação Dinâmica</h3>
            <p>Metodologia de 3 passos para resolver problemas de programação dinâmica.</p>
            <ul>
                <li>💪 Força Bruta</li>
                <li>🧠 Memoização</li>
                <li>📊 Tabulação</li>
                <li>🎯 Otimização</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="module-card">
            <h3>🏗️ Módulo 2: Estruturas de Dados</h3>
            <p>Estruturas de dados avançadas com visualizações detalhadas.</p>
            <ul>
                <li>🔺 Heap (Min/Max)</li>
                <li>🌳 Trie</li>
                <li>🤝 Union-Find</li>
                <li>📊 Segment Tree</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
            <h3>💼 Módulo 4: Entrevistas</h3>
            <p>Simulação de entrevistas técnicas com feedback em tempo real.</p>
            <ul>
                <li>🎯 Problemas Clássicos</li>
                <li>📊 Análise de Código</li>
                <li>⏱️ Simulação de Tempo</li>
                <li>📝 Feedback Detalhado</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de recursos
    st.markdown("### ⚡ Recursos Principais")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🎮 Player Interativo
        - Controles de velocidade
        - Navegação por passos
        - Personalização de entrada
        - Comparação de algoritmos
        """)
    
    with col2:
        st.markdown("""
        #### 🎨 Visualizações Dinâmicas
        - Gráficos em tempo real
        - Animações passo a passo
        - Múltiplas representações
        - Análise de complexidade
        """)
    
    with col3:
        st.markdown("""
        #### 🤖 Integração MCP
        - Análise automática
        - Otimizações sugeridas
        - Feedback inteligente
        - Benchmarking avançado
        """)

def render_module_1():
    """Renderiza o módulo 1 - Fundamentos."""
    st.markdown("## 📚 Módulo 1: Fundamentos")
    
    # Importar componentes do módulo 1
    try:
        from modulo_1_fundamentos import busca_binaria, dois_ponteiros, janela_deslizante
        
        # Seleção de algoritmo
        algorithm = st.selectbox(
            "Escolha o Algoritmo",
            [
                "🔍 Busca Binária",
                "👥 Dois Ponteiros", 
                "🪟 Janela Deslizante",
                "🔢 Operações com Bits"
            ]
        )
        
        if algorithm == "🔍 Busca Binária":
            render_binary_search()
        elif algorithm == "👥 Dois Ponteiros":
            render_two_pointers()
        elif algorithm == "🪟 Janela Deslizante":
            render_sliding_window()
        elif algorithm == "🔢 Operações com Bits":
            render_bit_operations()
            
    except ImportError as e:
        st.error(f"Erro ao importar módulo 1: {e}")
        st.info("Certifique-se de que todos os arquivos do módulo 1 estão presentes.")

def render_binary_search():
    """Renderiza a visualização de busca binária."""
    st.markdown("### 🔍 Busca Binária")
    
    # Player controls
    st.markdown("#### 🎮 Controles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        array_size = st.slider("Tamanho do Array", 5, 50, 20)
        
    with col2:
        target = st.number_input("Valor a Buscar", value=25)
        
    with col3:
        speed = st.slider("Velocidade", 1, 10, 5)
    
    # Gerar array ordenado
    import numpy as np
    arr = sorted(np.random.randint(1, 100, array_size))
    
    # Visualização
    st.markdown("#### 📊 Visualização")
    
    # Implementar busca binária com passos
    def binary_search_steps(arr, target):
        steps = []
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            steps.append({
                'left': left,
                'right': right,
                'mid': mid,
                'comparison': arr[mid],
                'found': arr[mid] == target
            })
            
            if arr[mid] == target:
                break
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return steps
    
    steps = binary_search_steps(arr, target)
    
    # Controles de navegação
    step = st.slider("Passo", 0, len(steps) - 1, 0) if steps else 0
    
    if steps:
        current_step = steps[step]
        
        # Mostrar array com destaque
        colors = ['lightblue'] * len(arr)
        
        # Destacar região atual
        for i in range(current_step['left'], current_step['right'] + 1):
            colors[i] = 'lightgreen'
        
        # Destacar mid
        colors[current_step['mid']] = 'red'
        
        # Gráfico de barras
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        bars = ax.bar(range(len(arr)), arr, color=colors)
        ax.set_title(f"Busca Binária - Passo {step + 1}")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        
        # Adicionar anotações
        ax.axvline(current_step['left'], color='green', linestyle='--', alpha=0.7, label='Left')
        ax.axvline(current_step['right'], color='green', linestyle='--', alpha=0.7, label='Right')
        ax.axvline(current_step['mid'], color='red', linestyle='-', alpha=0.7, label='Mid')
        
        ax.legend()
        st.pyplot(fig)
        
        # Informações do passo
        st.markdown(f"""
        <div class="algorithm-step">
            <strong>Passo {step + 1}:</strong><br>
            Left: {current_step['left']}, Right: {current_step['right']}, Mid: {current_step['mid']}<br>
            Comparando: {current_step['comparison']} vs {target}<br>
            {"✅ Encontrado!" if current_step['found'] else "⏭️ Continuando..."}
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Array Size", len(arr))
    
    with col2:
        st.metric("Passos", len(steps))
    
    with col3:
        complexity = "O(log n)"
        st.markdown(f'<span class="complexity-badge">{complexity}</span>', unsafe_allow_html=True)

def render_two_pointers():
    """Renderiza a visualização de dois ponteiros."""
    st.markdown("### 👥 Dois Ponteiros")
    st.info("Implementação em desenvolvimento...")

def render_sliding_window():
    """Renderiza a visualização de janela deslizante."""
    st.markdown("### 🪟 Janela Deslizante")
    st.info("Implementação em desenvolvimento...")

def render_bit_operations():
    """Renderiza operações com bits."""
    st.markdown("### 🔢 Operações com Bits")
    st.info("Implementação em desenvolvimento...")

def render_module_2():
    """Renderiza o módulo 2 - Estruturas de Dados."""
    st.markdown("## 🏗️ Módulo 2: Estruturas de Dados")
    st.info("Implementação em desenvolvimento...")

def render_module_3():
    """Renderiza o módulo 3 - Programação Dinâmica."""
    st.markdown("## 🎯 Módulo 3: Programação Dinâmica")
    st.info("Implementação em desenvolvimento...")

def render_module_4():
    """Renderiza o módulo 4 - Entrevistas."""
    st.markdown("## 💼 Módulo 4: Entrevistas")
    st.info("Implementação em desenvolvimento...")

if __name__ == "__main__":
    main()
