# 🌐 Streamlit App Completa para Deploy

import streamlit as st

# import matplotlib.pyplot as plt  # Removido para compatibilidade Streamlit Cloud
import numpy as np
import pandas as pd

# Importações condicionais para Plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    go = None

import time
import json

# import requests  # Removido temporariamente
from typing import List, Tuple, Dict, Any
from collections import deque

# Configuração da página
st.set_page_config(
    page_title="🧠 Visualizador de Algoritmos - MCP Ready", page_icon="🧠", layout="wide", initial_sidebar_state="expanded"
)

# CSS customizado para melhor aparência
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


# Classe para comunicação MCP (simulada)
class MCPConnector:
    """Simulação de connector MCP para demonstração."""

    def __init__(self):
        self.tools_available = ["algorithm_analyzer", "performance_tester", "complexity_calculator", "code_generator"]
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
                "optimizations": ["Use binary search", "Consider iterative approach"],
            }
        elif tool_name == "performance_tester":
            return {
                "execution_time": np.random.uniform(0.001, 0.1),
                "memory_usage": np.random.uniform(10, 100),
                "score": np.random.uniform(80, 100),
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
    st.markdown(
        """
    <div style='text-align: right; padding-top: 1rem;'>
        <span style='background: #4CAF50; color: white; padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem;'>
            🔗 MCP Connected
        </span>
    </div>
    """,
        unsafe_allow_html=True,
    )

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
        "📊 Algoritmos de Ordenação",
        "🌳 Algoritmos de Grafos",
        "👆 Dois Ponteiros",
        "🪟 Janela Deslizante",
        "🔄 Backtracking",
        "🌐 BFS (Busca em Largura)",
        "📊 Análise MCP",
        "🧠 Metodologia 3 Passos",
        "⚡ Performance Testing",
    ],
)

# Informações na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Metodologia dos 3 Passos")
st.sidebar.markdown(
    """
1. **🔴 Força Bruta** - Entender o problema
2. **🟡 Memoização** - Otimizar redundâncias
3. **🟢 Tabulação** - Solução iterativa
"""
)

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
        st.markdown(
            """
        <div class="algorithm-card">
            <h3>📁 Módulo 1: Fundamentos ✅</h3>
            <p><strong>Status:</strong> Completo</p>
            <p><strong>Algoritmos:</strong> Busca Binária, Dois Ponteiros, BFS, Backtracking</p>
            <p><strong>Complexidades:</strong> O(log n), O(n), O(V+E)</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="algorithm-card">
            <h3>📁 Módulo 3: Programação Dinâmica</h3>
            <p><strong>Status:</strong> Planejado</p>
            <p><strong>Foco:</strong> Metodologia 3 Passos</p>
            <p><strong>Problemas:</strong> Knapsack, LCS, Edit Distance</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="algorithm-card">
            <h3>📁 Módulo 2: Estruturas de Dados</h3>
            <p><strong>Status:</strong> Em Desenvolvimento</p>
            <p><strong>Estruturas:</strong> BST, Heaps, Union-Find</p>
            <p><strong>Próximo:</strong> Implementação visual</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="algorithm-card">
            <h3>📁 Módulo 4: Entrevistas</h3>
            <p><strong>Status:</strong> Planejado</p>
            <p><strong>Foco:</strong> Problemas clássicos</p>
            <p><strong>Meta:</strong> Preparação para entrevistas</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Gráfico de progresso
    st.markdown("### 📈 Progresso do Estudo")

    progress_data = {
        "Módulo": ["Módulo 1", "Módulo 2", "Módulo 3", "Módulo 4"],
        "Progresso": [100, 25, 0, 0],
        "Algoritmos": [7, 2, 0, 0],
    }

    if PLOTLY_AVAILABLE:
        fig = px.bar(
            progress_data,
            x="Módulo",
            y="Progresso",
            title="Progresso por Módulo (%)",
            color="Progresso",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback para tabela simples quando Plotly não está disponível
        df = pd.DataFrame(progress_data)
        st.bar_chart(df.set_index("Módulo")["Progresso"])
        st.dataframe(df, use_container_width=True)

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
            passos.append({"esquerda": esquerda, "direita": direita, "meio": meio, "valor_meio": array[meio]})

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
            mcp_analysis = mcp.call_tool(
                "algorithm_analyzer", {"algorithm": "binary_search", "input_size": len(array_ordenado), "target": target}
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <h4>⏱️ Complexidade Temporal</h4>
                    <h2>{mcp_analysis['complexity']}</h2>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <h4>💾 Complexidade Espacial</h4>
                    <h2>{mcp_analysis['space']}</h2>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col3:
                performance = mcp.call_tool(
                    "performance_tester", {"algorithm": "binary_search", "array_size": len(array_ordenado)}
                )
                st.markdown(
                    f"""
                <div class="metric-card">
                    <h4>⚡ Performance Score</h4>
                    <h2>{performance['score']:.1f}/100</h2>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # Visualização
    st.markdown("### 🎬 Visualização Passo a Passo")
    passo_atual = st.slider("Passo da busca:", 0, len(passos) - 1, 0)

    if passo_atual < len(passos):
        passo = passos[passo_atual]

        if PLOTLY_AVAILABLE:
            # Criar gráfico com Plotly
            cores = ["lightgray"] * len(array_ordenado)
            for i in range(passo["esquerda"], passo["direita"] + 1):
                cores[i] = "lightblue"
            cores[passo["meio"]] = "red" if passo["valor_meio"] != target else "green"

            fig = go.Figure()
            fig.add_bar(
                x=list(range(len(array_ordenado))),
                y=array_ordenado,
                marker_color=cores,
                text=array_ordenado,
                textposition="auto",
                name="Array",
            )

            fig.update_layout(
                title=f"Passo {passo_atual + 1}: Verificando posição {passo['meio']} (valor={passo['valor_meio']})",
                xaxis_title="Índice",
                yaxis_title="Valor",
                showlegend=False,
                height=400,
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback simples quando Plotly não está disponível
            st.write(f"**Passo {passo_atual + 1}:** Verificando posição {passo['meio']} (valor={passo['valor_meio']})")

            # Mostrar array visualmente
            array_visual = ""
            for i, val in enumerate(array_ordenado):
                if i == passo["meio"]:
                    if passo["valor_meio"] == target:
                        array_visual += f"🎯**{val}** "
                    else:
                        array_visual += f"🔍**{val}** "
                elif passo["esquerda"] <= i <= passo["direita"]:
                    array_visual += f"📍{val} "
                else:
                    array_visual += f"⬜{val} "

            st.write(f"Array: {array_visual}")
            st.write(f"Área de busca: [{passo['esquerda']}, {passo['direita']}]")

    # Resultado
    if resultado != -1:
        st.success(f"✅ Target {target} encontrado na posição {resultado}!")
    else:
        st.error(f"❌ Target {target} não encontrado!")

    st.info(f"📊 Total de passos: {len(passos)} | Teórico máximo: {int(np.log2(len(array_ordenado))) + 1}")

elif algoritmo_selecionado == "📊 Análise MCP":
    st.header("📊 Análise Avançada com MCP Integration")

    st.markdown(
        """
    ### 🔗 MCP (Model Context Protocol) Integration
    
    Esta seção demonstra como o **MCP** pode expandir as capacidades da aplicação Streamlit:
    """
    )

    # Demonstração de MCP Tools
    st.markdown("#### 🛠️ Available MCP Tools:")

    for tool in available_tools:
        with st.expander(f"🔧 {tool}"):
            if tool == "algorithm_analyzer":
                st.markdown(
                    """
                **Funcionalidade:** Análise automática de complexidade
                - Detecta padrões de complexidade temporal
                - Sugere otimizações
                - Compara com algoritmos similares
                """
                )

                if st.button(f"Test {tool}"):
                    result = mcp.call_tool(tool, {"algorithm": "quicksort"})
                    st.json(result)

            elif tool == "performance_tester":
                st.markdown(
                    """
                **Funcionalidade:** Teste de performance em tempo real
                - Medição de tempo de execução
                - Análise de uso de memória
                - Benchmarking automático
                """
                )

                if st.button(f"Test {tool}"):
                    result = mcp.call_tool(tool, {"input_size": 1000})
                    st.json(result)

            elif tool == "complexity_calculator":
                st.markdown(
                    """
                **Funcionalidade:** Cálculo preciso de complexidade
                - Big O analysis
                - Worst/average/best case
                - Space complexity
                """
                )

            elif tool == "code_generator":
                st.markdown(
                    """
                **Funcionalidade:** Geração automática de código
                - Templates de algoritmos
                - Otimizações sugeridas
                - Multi-language support
                """
                )

    # Demonstração de integração
    st.markdown("### 🔄 Real-time MCP Communication")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Request to MCP Server:**")
        sample_request = {
            "tool": "algorithm_analyzer",
            "params": {"algorithm": "merge_sort", "input_size": 1000, "optimize": True},
        }
        st.json(sample_request)

    with col2:
        st.markdown("**Response from MCP Server:**")
        if st.button("🚀 Send Request"):
            with st.spinner("Calling MCP server..."):
                time.sleep(1)  # Simular latência
                response = {
                    "complexity": {"time": "O(n log n)", "space": "O(n)"},
                    "optimizations": [
                        "Use in-place sorting for space optimization",
                        "Consider quicksort for average case performance",
                    ],
                    "benchmark": {"execution_time": "0.045ms", "memory_usage": "24KB"},
                }
                st.json(response)

elif algoritmo_selecionado == "⚡ Performance Testing":
    st.header("⚡ Performance Testing com MCP")

    # Seletor de algoritmo para teste
    algoritmo_teste = st.selectbox(
        "Algoritmo para testar:", ["Busca Binária", "Busca Linear", "Quick Sort", "Merge Sort", "Bubble Sort"]
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
                result = mcp.call_tool(
                    "performance_tester", {"algorithm": algoritmo_teste.lower().replace(" ", "_"), "input_size": size}
                )

                results.append(
                    {
                        "Tamanho": size,
                        "Tempo (ms)": result["execution_time"],
                        "Memória (KB)": result["memory_usage"],
                        "Score": result["score"],
                    }
                )

                progress_bar.progress((i + 1) / num_tests)
                time.sleep(0.1)  # Simular processamento

        # Mostrar resultados
        df_results = pd.DataFrame(results)

        col1, col2 = st.columns(2)

        with col1:
            if PLOTLY_AVAILABLE:
                fig_time = px.line(df_results, x="Tamanho", y="Tempo (ms)", title=f"Performance: {algoritmo_teste}")
                st.plotly_chart(fig_time, use_container_width=True)
            else:
                st.subheader(f"Performance: {algoritmo_teste}")
                st.line_chart(df_results.set_index("Tamanho")["Tempo (ms)"])

        with col2:
            if PLOTLY_AVAILABLE:
                fig_memory = px.line(df_results, x="Tamanho", y="Memória (KB)", title="Uso de Memória")
                st.plotly_chart(fig_memory, use_container_width=True)
            else:
                st.subheader("Uso de Memória")
                st.line_chart(df_results.set_index("Tamanho")["Memória (KB)"])

        st.dataframe(df_results, use_container_width=True)

# 📊 Seção de Algoritmos de Ordenação
elif algoritmo_selecionado == "📊 Algoritmos de Ordenação":
    st.header("📊 Algoritmos de Ordenação")
    st.markdown("Compare diferentes algoritmos de ordenação com visualização em tempo real")

    # Importar algoritmos de ordenação (simulação - na implementação real seria import)
    def simulate_sorting_algorithm(algorithm, data, steps):
        """Simula execução de algoritmo de ordenação"""
        result = sorted(data)
        example_steps = [
            {"array": data.copy(), "comparing": [0, 1], "action": f"Iniciando {algorithm}"},
            {
                "array": result[: len(result) // 2] + data[len(result) // 2 :],
                "comparing": [2, 3],
                "action": "Comparando elementos",
            },
            {"array": result, "comparing": [], "action": "Ordenação completa"},
        ]
        return result, example_steps[:steps]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("⚙️ Configurações")

        # Seleção do algoritmo
        algoritmo_ord = st.selectbox(
            "Escolha o algoritmo:", ["Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort", "Counting Sort"]
        )

        # Configuração dos dados
        tamanho_array = st.slider("Tamanho do array:", 5, 50, 15)

        tipo_dados = st.radio("Tipo de dados:", ["Aleatório", "Quase Ordenado", "Inversamente Ordenado", "Custom"])

        if tipo_dados == "Custom":
            dados_custom = st.text_input("Digite os números (separados por vírgula):")
            if dados_custom:
                try:
                    dados = [int(x.strip()) for x in dados_custom.split(",")]
                except:
                    dados = list(range(1, tamanho_array + 1))
                    st.warning("Formato inválido. Usando dados padrão.")
            else:
                dados = list(range(1, tamanho_array + 1))
        else:
            dados = list(range(1, tamanho_array + 1))
            if tipo_dados == "Aleatório":
                np.random.shuffle(dados)
            elif tipo_dados == "Inversamente Ordenado":
                dados = dados[::-1]
            elif tipo_dados == "Quase Ordenado":
                # Fazer apenas algumas trocas
                for _ in range(max(1, len(dados) // 5)):
                    i, j = np.random.choice(len(dados), 2, replace=False)
                    dados[i], dados[j] = dados[j], dados[i]

        st.write(f"**Array inicial:** {dados}")

        # Análise de complexidade
        complexidades = {
            "Bubble Sort": {"melhor": "O(n)", "médio": "O(n²)", "pior": "O(n²)", "espaço": "O(1)"},
            "Quick Sort": {"melhor": "O(n log n)", "médio": "O(n log n)", "pior": "O(n²)", "espaço": "O(log n)"},
            "Merge Sort": {"melhor": "O(n log n)", "médio": "O(n log n)", "pior": "O(n log n)", "espaço": "O(n)"},
            "Heap Sort": {"melhor": "O(n log n)", "médio": "O(n log n)", "pior": "O(n log n)", "espaço": "O(1)"},
            "Counting Sort": {"melhor": "O(n+k)", "médio": "O(n+k)", "pior": "O(n+k)", "espaço": "O(k)"},
        }

        if algoritmo_ord in complexidades:
            comp = complexidades[algoritmo_ord]
            st.markdown("### 📈 Análise de Complexidade")
            st.markdown(f"**Melhor caso:** {comp['melhor']}")
            st.markdown(f"**Caso médio:** {comp['médio']}")
            st.markdown(f"**Pior caso:** {comp['pior']}")
            st.markdown(f"**Espaço:** {comp['espaço']}")

    with col2:
        st.subheader("🎬 Visualização")

        if st.button("▶️ Executar Algoritmo"):
            # Placeholder para progresso
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Simular execução
            resultado, passos = simulate_sorting_algorithm(algoritmo_ord, dados, 8)

            # Container para visualização
            chart_container = st.empty()

            # Animar os passos
            for i, passo in enumerate(passos):
                progress_bar.progress((i + 1) / len(passos))
                status_text.text(passo["action"])

                if PLOTLY_AVAILABLE:
                    # Criar gráfico do estado atual
                    fig = go.Figure()

                    colors = ["lightblue"] * len(passo["array"])
                    if "comparing" in passo and passo["comparing"]:
                        for idx in passo["comparing"]:
                            if idx < len(colors):
                                colors[idx] = "red"

                    fig.add_bar(
                        x=list(range(len(passo["array"]))),
                        y=passo["array"],
                        marker_color=colors,
                        text=passo["array"],
                        textposition="auto",
                    )

                    fig.update_layout(
                        title=f"{algoritmo_ord} - {passo['action']}",
                        xaxis_title="Posição",
                        yaxis_title="Valor",
                        showlegend=False,
                        height=400,
                    )

                    chart_container.plotly_chart(fig, use_container_width=True)
                else:
                    # Fallback visual simples
                    array_visual = ""
                    for idx, val in enumerate(passo["array"]):
                        if "comparing" in passo and idx in passo.get("comparing", []):
                            array_visual += f"🔴**{val}** "
                        else:
                            array_visual += f"🔵{val} "

                    chart_container.write(f"**{passo['action']}**")
                    chart_container.write(f"Array: {array_visual}")

                time.sleep(0.8)

            st.success(f"✅ Ordenação completa! Array final: {resultado}")
            progress_bar.progress(1.0)
            status_text.text("Algoritmo concluído")

# 🌳 Seção de Algoritmos de Grafos
elif algoritmo_selecionado == "🌳 Algoritmos de Grafos":
    st.header("🌳 Algoritmos de Grafos")
    st.markdown("Explore algoritmos fundamentais de grafos com visualização interativa")

    # Simulação de grafo
    def create_sample_graph():
        """Cria um grafo de exemplo"""
        return {
            "vertices": ["A", "B", "C", "D", "E"],
            "arestas": [
                ("A", "B", 4),
                ("A", "C", 2),
                ("B", "C", 1),
                ("B", "D", 5),
                ("C", "D", 8),
                ("C", "E", 10),
                ("D", "E", 2),
            ],
        }

    def simulate_graph_algorithm(algorithm, graph, start="A"):
        """Simula execução de algoritmo de grafo"""
        if algorithm == "BFS":
            return ["A", "B", "C", "D", "E"], [
                {"visitados": ["A"], "fila": ["B", "C"], "atual": "A", "action": "Iniciando BFS"},
                {"visitados": ["A", "B"], "fila": ["C", "D"], "atual": "B", "action": "Processando B"},
                {"visitados": ["A", "B", "C"], "fila": ["D", "E"], "atual": "C", "action": "Processando C"},
            ]
        elif algorithm == "Dijkstra":
            return {"A": 0, "B": 4, "C": 2, "D": 6, "E": 8}, [
                {
                    "distancias": {"A": 0, "B": float("inf"), "C": float("inf"), "D": float("inf"), "E": float("inf")},
                    "atual": "A",
                    "action": "Início",
                },
                {
                    "distancias": {"A": 0, "B": 4, "C": 2, "D": float("inf"), "E": float("inf")},
                    "atual": "A",
                    "action": "Relaxando vizinhos de A",
                },
                {"distancias": {"A": 0, "B": 3, "C": 2, "D": 10, "E": 12}, "atual": "C", "action": "Relaxando vizinhos de C"},
            ]

    tab1, tab2, tab3 = st.tabs(["🔍 Busca", "🛣️ Caminhos Mínimos", "🌲 Árvore Geradora"])

    with tab1:
        st.subheader("Algoritmos de Busca")

        col1, col2 = st.columns([1, 2])

        with col1:
            algoritmo_busca = st.selectbox("Algoritmo:", ["BFS (Busca em Largura)", "DFS (Busca em Profundidade)"])

            vertice_inicio = st.selectbox("Vértice inicial:", ["A", "B", "C", "D", "E"])

            if st.button("🔍 Executar Busca"):
                grafo = create_sample_graph()
                resultado, passos = simulate_graph_algorithm(
                    "BFS" if "BFS" in algoritmo_busca else "DFS", grafo, vertice_inicio
                )

                st.success(f"Ordem de visita: {' → '.join(resultado)}")

                # Mostrar passos
                for passo in passos:
                    st.info(f"**{passo['action']}**")
                    st.write(f"Visitados: {passo.get('visitados', [])}")
                    if "fila" in passo:
                        st.write(f"Fila: {passo['fila']}")

        with col2:
            # Visualização do grafo
            st.subheader("Estrutura do Grafo")

            # Criar visualização simples do grafo
            grafo_data = create_sample_graph()

            # Matriz de adjacência para visualização
            vertices = grafo_data["vertices"]
            matriz = pd.DataFrame(0, index=vertices, columns=vertices)

            for u, v, peso in grafo_data["arestas"]:
                matriz.loc[u, v] = peso
                matriz.loc[v, u] = peso  # Grafo não-dirigido

            st.write("**Matriz de Adjacência (com pesos):**")
            st.dataframe(matriz)

            st.write("**Arestas:**")
            for u, v, peso in grafo_data["arestas"]:
                st.write(f"• {u} ↔ {v} (peso: {peso})")

    with tab2:
        st.subheader("Algoritmo de Dijkstra")

        col1, col2 = st.columns([1, 1])

        with col1:
            vertice_dijkstra = st.selectbox("Vértice inicial (Dijkstra):", ["A", "B", "C", "D", "E"], key="dijkstra_start")

            if st.button("🛣️ Calcular Caminhos Mínimos"):
                grafo = create_sample_graph()
                distancias, passos = simulate_graph_algorithm("Dijkstra", grafo, vertice_dijkstra)

                st.success("Distâncias mínimas calculadas!")

                # Mostrar distâncias
                for vertice, dist in distancias.items():
                    if dist == float("inf"):
                        st.write(f"**{vertice}:** ∞ (não alcançável)")
                    else:
                        st.write(f"**{vertice}:** {dist}")

        with col2:
            st.subheader("Análise de Complexidade")
            st.markdown(
                """
            **Dijkstra:**
            - **Temporal:** O((V + E) log V)
            - **Espacial:** O(V)
            - **Uso:** Caminhos mínimos com pesos positivos
            
            **Características:**
            - ✅ Garante solução ótima
            - ❌ Não funciona com pesos negativos
            - 🔧 Usa heap para eficiência
            """
            )

    with tab3:
        st.subheader("Árvore Geradora Mínima")

        st.markdown(
            """
        **Algoritmo de Kruskal** para encontrar a Árvore Geradora Mínima (MST):
        
        1. Ordenar arestas por peso
        2. Para cada aresta, verificar se forma ciclo
        3. Se não formar ciclo, adicionar à MST
        4. Repetir até ter V-1 arestas
        """
        )

        if st.button("🌲 Gerar MST (Kruskal)"):
            grafo = create_sample_graph()

            # Simular Kruskal
            arestas_ordenadas = sorted(grafo["arestas"], key=lambda x: x[2])
            mst = []
            peso_total = 0

            st.write("**Arestas ordenadas por peso:**")
            for u, v, peso in arestas_ordenadas:
                st.write(f"• {u}-{v}: {peso}")

            st.write("**Construindo MST:**")
            for u, v, peso in arestas_ordenadas[:4]:  # Simular algumas arestas
                mst.append((u, v, peso))
                peso_total += peso
                st.success(f"✅ Adicionada: {u}-{v} (peso: {peso})")

            st.write(f"**MST Final:** {mst}")
            st.write(f"**Peso Total:** {peso_total}")

else:
    st.header(f"{algoritmo_selecionado}")
    st.info(
        "🚧 Esta seção demonstra a flexibilidade da arquitetura MCP + Streamlit. Novos algoritmos podem ser adicionados dinamicamente!"
    )

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

st.markdown(
    """
---
**🎯 Arquitetura:** Streamlit Cloud + MCP + VS Code | **📚 Projeto:** Dominando o Pensamento Algorítmico
"""
)
