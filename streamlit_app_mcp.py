# 🌐 Streamlit App Completa para Deploy

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import json
import requests
from typing import List, Tuple, Dict, Any
from collections import deque

# Configuração da página
st.set_page_config(
    page_title="🧠 Visualizador de Algoritmos - MCP Ready",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhor aparência
st.markdown("""
<style>
.main > div {
    padding-top: 1rem;
}
.stSelectbox > div > div > select {
    font-size: 16px;
}
.algorithm-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
.metric-card {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# Classe para comunicação MCP (simulada)
class MCPConnector:
    """Simulação de connector MCP para demonstração."""
    
    def __init__(self):
        self.tools_available = [
            "algorithm_analyzer", 
            "performance_tester", 
            "complexity_calculator",
            "code_generator"
        ]
        self.session_data = {}
    
    def discover_tools(self) -> List[str]:
        """Simula dynamic tool discovery."""
        return self.tools_available
    
    def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simula chamada de tool via MCP."""
        if tool_name == "algorithm_analyzer":
            return {
                "complexity": "O(log n)",
                "space": "O(1)",
                "optimizations": ["Use binary search", "Consider iterative approach"]
            }
        elif tool_name == "performance_tester":
            return {
                "execution_time": np.random.uniform(0.001, 0.1),
                "memory_usage": np.random.uniform(10, 100),
                "score": np.random.uniform(80, 100)
            }
        return {"status": "Tool not found"}

# Inicializar connector MCP
@st.cache_resource
def init_mcp():
    return MCPConnector()

mcp = init_mcp()

# Título principal com badge MCP
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🧠 Visualizador Interativo de Algoritmos")
    st.markdown("**Integrado com MCP + Streamlit Cloud**")
with col2:
    st.markdown("""
    <div style='text-align: right; padding-top: 1rem;'>
        <span style='background: #4CAF50; color: white; padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem;'>
            🔗 MCP Connected
        </span>
    </div>
    """, unsafe_allow_html=True)

# Sidebar com MCP Tools
st.sidebar.title("🛠️ MCP Tools")
st.sidebar.markdown("**Dynamic Tool Discovery:**")

# Descobrir tools disponíveis
available_tools = mcp.discover_tools()
for tool in available_tools:
    st.sidebar.markdown(f"✅ {tool}")

st.sidebar.markdown("---")

# Seleção de algoritmo
st.sidebar.title("📚 Algoritmos")
algoritmo_selecionado = st.sidebar.selectbox(
    "🔍 Escolha um algoritmo:",
    [
        "🏠 Dashboard",
        "🔍 Busca Binária",
        "👆 Dois Ponteiros",
        "🪟 Janela Deslizante", 
        "🔄 Backtracking",
        "🌐 BFS (Busca em Largura)",
        "📊 Análise MCP",
        "🧠 Metodologia 3 Passos",
        "⚡ Performance Testing"
    ]
)

# Informações na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Metodologia dos 3 Passos")
st.sidebar.markdown("""
1. **🔴 Força Bruta** - Entender o problema
2. **🟡 Memoização** - Otimizar redundâncias
3. **🟢 Tabulação** - Solução iterativa
""")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh MCP Tools"):
    st.rerun()

# Conteúdo principal baseado na seleção
if algoritmo_selecionado == "🏠 Dashboard":
    st.header("🎯 Dashboard - Plano de Estudo Algorítmico")
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Módulos", "4", "Completos")
    with col2:
        st.metric("🔍 Algoritmos", "25+", "Implementados")
    with col3:
        st.metric("⏱️ Duração", "12", "Semanas")
    with col4:
        st.metric("🎯 Progresso", "35%", "Módulo 1 ✅")
    
    st.markdown("---")
    
    # Cards dos módulos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="algorithm-card">
            <h3>📁 Módulo 1: Fundamentos ✅</h3>
            <p><strong>Status:</strong> Completo</p>
            <p><strong>Algoritmos:</strong> Busca Binária, Dois Ponteiros, BFS, Backtracking</p>
            <p><strong>Complexidades:</strong> O(log n), O(n), O(V+E)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="algorithm-card">
            <h3>📁 Módulo 3: Programação Dinâmica</h3>
            <p><strong>Status:</strong> Planejado</p>
            <p><strong>Foco:</strong> Metodologia 3 Passos</p>
            <p><strong>Problemas:</strong> Knapsack, LCS, Edit Distance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="algorithm-card">
            <h3>📁 Módulo 2: Estruturas de Dados</h3>
            <p><strong>Status:</strong> Em Desenvolvimento</p>
            <p><strong>Estruturas:</strong> BST, Heaps, Union-Find</p>
            <p><strong>Próximo:</strong> Implementação visual</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="algorithm-card">
            <h3>📁 Módulo 4: Entrevistas</h3>
            <p><strong>Status:</strong> Planejado</p>
            <p><strong>Foco:</strong> Problemas clássicos</p>
            <p><strong>Meta:</strong> Preparação para entrevistas</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de progresso
    st.markdown("### 📈 Progresso do Estudo")
    
    progress_data = {
        'Módulo': ['Módulo 1', 'Módulo 2', 'Módulo 3', 'Módulo 4'],
        'Progresso': [100, 25, 0, 0],
        'Algoritmos': [7, 2, 0, 0]
    }
    
    fig = px.bar(progress_data, x='Módulo', y='Progresso', 
                title="Progresso por Módulo (%)",
                color='Progresso',
                color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

elif algoritmo_selecionado == "🔍 Busca Binária":
    st.header("🔍 Busca Binária com Análise MCP")
    
    # Controles
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tamanho_array = st.slider("Tamanho do array:", 5, 30, 15)
    with col2:
        array_ordenado = sorted(np.random.randint(1, 100, tamanho_array).tolist())
        target = st.selectbox("Procurar por:", array_ordenado)
    with col3:
        analyze_with_mcp = st.checkbox("🔗 Analisar com MCP", value=True)
    
    # Executar busca binária
    def busca_binaria_visual(array, target):
        esquerda, direita = 0, len(array) - 1
        passos = []
        
        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            passos.append({
                'esquerda': esquerda,
                'direita': direita,
                'meio': meio,
                'valor_meio': array[meio]
            })
            
            if array[meio] == target:
                return meio, passos
            elif array[meio] < target:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        return -1, passos
    
    resultado, passos = busca_binaria_visual(array_ordenado, target)
    
    # Análise MCP
    if analyze_with_mcp:
        with st.spinner("🔄 Analisando com MCP..."):
            mcp_analysis = mcp.call_tool("algorithm_analyzer", {
                "algorithm": "binary_search",
                "input_size": len(array_ordenado),
                "target": target
            })
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>⏱️ Complexidade Temporal</h4>
                    <h2>{mcp_analysis['complexity']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>💾 Complexidade Espacial</h4>
                    <h2>{mcp_analysis['space']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                performance = mcp.call_tool("performance_tester", {
                    "algorithm": "binary_search",
                    "array_size": len(array_ordenado)
                })
                st.markdown(f"""
                <div class="metric-card">
                    <h4>⚡ Performance Score</h4>
                    <h2>{performance['score']:.1f}/100</h2>
                </div>
                """, unsafe_allow_html=True)
    
    # Visualização
    st.markdown("### 🎬 Visualização Passo a Passo")
    passo_atual = st.slider("Passo da busca:", 0, len(passos)-1, 0)
    
    if passo_atual < len(passos):
        passo = passos[passo_atual]
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(14, 8))
        
        cores = ['lightgray'] * len(array_ordenado)
        for i in range(passo['esquerda'], passo['direita'] + 1):
            cores[i] = 'lightblue'
        cores[passo['meio']] = 'red' if passo['valor_meio'] != target else 'green'
        
        bars = ax.bar(range(len(array_ordenado)), array_ordenado, color=cores, 
                     edgecolor='black', linewidth=1.5)
        
        for i, val in enumerate(array_ordenado):
            ax.text(i, val + 1, str(val), ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(f"Passo {passo_atual + 1}: Verificando posição {passo['meio']} (valor={passo['valor_meio']})", 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel("Índice", fontsize=12)
        ax.set_ylabel("Valor", fontsize=12)
        
        st.pyplot(fig)
        plt.close()
    
    # Resultado
    if resultado != -1:
        st.success(f"✅ Target {target} encontrado na posição {resultado}!")
    else:
        st.error(f"❌ Target {target} não encontrado!")
    
    st.info(f"📊 Total de passos: {len(passos)} | Teórico máximo: {int(np.log2(len(array_ordenado))) + 1}")

elif algoritmo_selecionado == "📊 Análise MCP":
    st.header("📊 Análise Avançada com MCP Integration")
    
    st.markdown("""
    ### 🔗 MCP (Model Context Protocol) Integration
    
    Esta seção demonstra como o **MCP** pode expandir as capacidades da aplicação Streamlit:
    """)
    
    # Demonstração de MCP Tools
    st.markdown("#### 🛠️ Available MCP Tools:")
    
    for tool in available_tools:
        with st.expander(f"🔧 {tool}"):
            if tool == "algorithm_analyzer":
                st.markdown("""
                **Funcionalidade:** Análise automática de complexidade
                - Detecta padrões de complexidade temporal
                - Sugere otimizações
                - Compara com algoritmos similares
                """)
                
                if st.button(f"Test {tool}"):
                    result = mcp.call_tool(tool, {"algorithm": "quicksort"})
                    st.json(result)
            
            elif tool == "performance_tester":
                st.markdown("""
                **Funcionalidade:** Teste de performance em tempo real
                - Medição de tempo de execução
                - Análise de uso de memória
                - Benchmarking automático
                """)
                
                if st.button(f"Test {tool}"):
                    result = mcp.call_tool(tool, {"input_size": 1000})
                    st.json(result)
            
            elif tool == "complexity_calculator":
                st.markdown("""
                **Funcionalidade:** Cálculo preciso de complexidade
                - Big O analysis
                - Worst/average/best case
                - Space complexity
                """)
            
            elif tool == "code_generator":
                st.markdown("""
                **Funcionalidade:** Geração automática de código
                - Templates de algoritmos
                - Otimizações sugeridas
                - Multi-language support
                """)
    
    # Demonstração de integração
    st.markdown("### 🔄 Real-time MCP Communication")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Request to MCP Server:**")
        sample_request = {
            "tool": "algorithm_analyzer",
            "params": {
                "algorithm": "merge_sort",
                "input_size": 1000,
                "optimize": True
            }
        }
        st.json(sample_request)
    
    with col2:
        st.markdown("**Response from MCP Server:**")
        if st.button("🚀 Send Request"):
            with st.spinner("Calling MCP server..."):
                time.sleep(1)  # Simular latência
                response = {
                    "complexity": {
                        "time": "O(n log n)",
                        "space": "O(n)"
                    },
                    "optimizations": [
                        "Use in-place sorting for space optimization",
                        "Consider quicksort for average case performance"
                    ],
                    "benchmark": {
                        "execution_time": "0.045ms",
                        "memory_usage": "24KB"
                    }
                }
                st.json(response)

elif algoritmo_selecionado == "⚡ Performance Testing":
    st.header("⚡ Performance Testing com MCP")
    
    # Seletor de algoritmo para teste
    algoritmo_teste = st.selectbox(
        "Algoritmo para testar:",
        ["Busca Binária", "Busca Linear", "Quick Sort", "Merge Sort", "Bubble Sort"]
    )
    
    # Parâmetros do teste
    col1, col2, col3 = st.columns(3)
    with col1:
        min_size = st.number_input("Tamanho mínimo:", 100, 10000, 1000)
    with col2:
        max_size = st.number_input("Tamanho máximo:", 1000, 100000, 10000)
    with col3:
        num_tests = st.number_input("Número de testes:", 3, 20, 10)
    
    if st.button("🚀 Executar Benchmark"):
        with st.spinner("Executando testes de performance..."):
            # Simular execução de testes
            sizes = np.linspace(min_size, max_size, num_tests, dtype=int)
            results = []
            
            progress_bar = st.progress(0)
            for i, size in enumerate(sizes):
                # Simular chamada MCP para teste
                result = mcp.call_tool("performance_tester", {
                    "algorithm": algoritmo_teste.lower().replace(" ", "_"),
                    "input_size": size
                })
                
                results.append({
                    "Tamanho": size,
                    "Tempo (ms)": result["execution_time"],
                    "Memória (KB)": result["memory_usage"],
                    "Score": result["score"]
                })
                
                progress_bar.progress((i + 1) / num_tests)
                time.sleep(0.1)  # Simular processamento
        
        # Mostrar resultados
        df_results = pd.DataFrame(results)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_time = px.line(df_results, x="Tamanho", y="Tempo (ms)", 
                              title=f"Performance: {algoritmo_teste}")
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            fig_memory = px.line(df_results, x="Tamanho", y="Memória (KB)", 
                                title="Uso de Memória")
            st.plotly_chart(fig_memory, use_container_width=True)
        
        st.dataframe(df_results, use_container_width=True)

else:
    st.header(f"{algoritmo_selecionado}")
    st.info("🚧 Esta seção demonstra a flexibilidade da arquitetura MCP + Streamlit. Novos algoritmos podem ser adicionados dinamicamente!")
    
    # Demonstrar tool discovery dinâmico
    st.markdown("### 🔍 Dynamic Tool Discovery")
    st.markdown("Com MCP, novas ferramentas podem ser descobertas automaticamente:")
    
    discovered_tools = mcp.discover_tools()
    for tool in discovered_tools:
        st.markdown(f"- 🛠️ **{tool}**: Disponível para este contexto")

# Footer com informações MCP
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🌐 Streamlit Cloud**")
    st.markdown("Deploy automático do GitHub")

with col2:
    st.markdown("**🔗 MCP Integration**")
    st.markdown("Dynamic tool discovery")

with col3:
    st.markdown("**🧠 VS Code Ready**")
    st.markdown("Compatible with Copilot")

st.markdown("""
---
**🎯 Arquitetura:** Streamlit Cloud + MCP + VS Code | **📚 Projeto:** Dominando o Pensamento Algorítmico
""")
