"""
🎯 ALGORITMOS VISUALIZADOR - VERSÃO ULTRA SIMPLIFICADA
=====================================================

Versão ultra simplificada otimizada para deploy no Streamlit Cloud.
Remove todas as funcionalidades complexas que podem causar problemas.

Funcionalidades Mantidas:
- ✅ Interface básica do Streamlit
- ✅ Alguns algoritmos fundamentais simples
- ✅ Visualizações básicas
- ✅ Navegação entre seções

Funcionalidades Removidas (para evitar problemas):
- ❌ Integração MCP Tavily (requer API key)
- ❌ Integração GitHub (requer tokens)
- ❌ Módulos complexos de estruturas de dados
- ❌ Programação dinâmica avançada
- ❌ Exercícios interativos complexos
- ❌ Aprendizado contextual
- ❌ Sistema de progresso

Autor: GitHub Copilot
Data: 2025
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuração da página
st.set_page_config(page_title="🎯 Algoritmos Visualizador", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

# ============================================================================
# 🎨 CSS SIMPLIFICADO
# ============================================================================

st.markdown(
    """
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}
.algorithm-demo {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    font-weight: 600;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# 🏠 PÁGINA INICIAL
# ============================================================================


def render_home():
    st.markdown(
        """
    <div class="main-header">
        <h1>🎯 Algoritmos Visualizador</h1>
        <p>Uma plataforma simplificada para aprendizado de algoritmos</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Algoritmos", "5+", "Simples")
    with col2:
        st.metric("📊 Visualizações", "10+", "Interativas")
    with col3:
        st.metric("👥 Usuários", "Online", "Funcionando")

    st.markdown("---")

    st.subheader("🎯 Algoritmos Disponíveis")

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown("### 🔍 Busca Binária")
            st.markdown("Algoritmo de busca eficiente em arrays ordenados")
            if st.button("Ver Demonstração", key="busca"):
                st.session_state.current_page = "busca_binaria"

        with st.container():
            st.markdown("### 📊 Ordenação")
            st.markdown("Algoritmos de ordenação: Bubble Sort, Quick Sort")
            if st.button("Ver Demonstração", key="ordenacao"):
                st.session_state.current_page = "ordenacao"

    with col2:
        with st.container():
            st.markdown("### 🧮 Fibonacci")
            st.markdown("Sequência de Fibonacci com múltiplas abordagens")
            if st.button("Ver Demonstração", key="fibonacci"):
                st.session_state.current_page = "fibonacci"

        with st.container():
            st.markdown("### 📈 Fatorial")
            st.markdown("Cálculo de fatorial com recursão e iteração")
            if st.button("Ver Demonstração", key="fatorial"):
                st.session_state.current_page = "fatorial"


# ============================================================================
# 🔍 BUSCA BINÁRIA
# ============================================================================


def render_busca_binaria():
    st.header("🔍 Busca Binária")

    st.markdown(
        """
    ### 📝 Como funciona:
    1. **Array ordenado**: O algoritmo requer um array previamente ordenado
    2. **Divisão**: Divide o array ao meio a cada iteração
    3. **Comparação**: Compara o elemento do meio com o alvo
    4. **Decisão**: Vai para esquerda ou direita baseado na comparação
    """
    )

    # Controles
    col1, col2 = st.columns(2)

    with col1:
        tamanho = st.slider("Tamanho do array:", 5, 20, 10)
        array = sorted(np.random.randint(1, 100, tamanho))
        target = st.selectbox("Buscar por:", array)

    with col2:
        st.write("**Array atual:**")
        st.write(array)
        st.write(f"**Procurando:** {target}")

    # Algoritmo
    esquerda, direita = 0, len(array) - 1
    passos = []
    encontrado = False

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        passos.append((esquerda, direita, meio, array[meio]))

        if array[meio] == target:
            encontrado = True
            break
        elif array[meio] < target:
            esquerda = meio + 1
        else:
            direita = meio - 1

    # Visualização
    if passos:
        passo_atual = st.slider("Passo:", 0, len(passos) - 1, 0)

        if passo_atual < len(passos):
            esq, dir, meio, valor_meio = passos[passo_atual]

            fig, ax = plt.subplots(figsize=(12, 6))

            colors = ["lightgray"] * len(array)
            for i in range(esq, dir + 1):
                colors[i] = "lightblue"
            colors[meio] = "red"

            bars = ax.bar(range(len(array)), array, color=colors, alpha=0.7)
            ax.set_title(f"Busca Binária - Passo {passo_atual + 1}")
            ax.set_xlabel("Índice")
            ax.set_ylabel("Valor")

            # Adicionar valores
            for i, (bar, valor) in enumerate(zip(bars, array)):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(valor), ha="center", va="bottom")

            st.pyplot(fig)

            # Status
            if encontrado and passo_atual == len(passos) - 1:
                st.success(f"✅ Encontrado! {target} está na posição {meio}")
            else:
                st.info(f"🔍 Procurando... Comparando {valor_meio} com {target}")


# ============================================================================
# 📊 ORDENAÇÃO
# ============================================================================


def render_ordenacao():
    st.header("📊 Algoritmos de Ordenação")

    algoritmo = st.selectbox("Escolha o algoritmo:", ["Bubble Sort", "Selection Sort", "Insertion Sort"])

    # Gerar array
    tamanho = st.slider("Tamanho do array:", 5, 15, 8)
    array = np.random.randint(1, 50, tamanho).tolist()

    st.write("**Array original:**", array)

    if algoritmo == "Bubble Sort":
        st.markdown("### 🫧 Bubble Sort")
        st.markdown("Compara elementos adjacentes e troca se estiverem na ordem errada.")

        # Implementação simplificada
        arr = array.copy()
        passos = [arr.copy()]

        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    passos.append(arr.copy())

        # Visualização
        if passos:
            passo_atual = st.slider("Passo:", 0, len(passos) - 1, 0)

            fig, ax = plt.subplots(figsize=(10, 5))
            colors = ["lightblue"] * len(passos[passo_atual])
            bars = ax.bar(range(len(passos[passo_atual])), passos[passo_atual], color=colors, alpha=0.7)
            ax.set_title(f"Bubble Sort - Passo {passo_atual + 1}")
            ax.set_xlabel("Índice")
            ax.set_ylabel("Valor")

            st.pyplot(fig)

            if passo_atual == len(passos) - 1:
                st.success("✅ Array ordenado!")

    elif algoritmo == "Selection Sort":
        st.markdown("### 🎯 Selection Sort")
        st.markdown("Encontra o menor elemento e coloca na posição correta.")

        # Implementação simplificada
        arr = array.copy()
        passos = [arr.copy()]

        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j

            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                passos.append(arr.copy())

        # Visualização
        if passos:
            passo_atual = st.slider("Passo:", 0, len(passos) - 1, 0)

            fig, ax = plt.subplots(figsize=(10, 5))
            colors = ["lightgreen"] * len(passos[passo_atual])
            bars = ax.bar(range(len(passos[passo_atual])), passos[passo_atual], color=colors, alpha=0.7)
            ax.set_title(f"Selection Sort - Passo {passo_atual + 1}")
            ax.set_xlabel("Índice")
            ax.set_ylabel("Valor")

            st.pyplot(fig)

            if passo_atual == len(passos) - 1:
                st.success("✅ Array ordenado!")


# ============================================================================
# 🧮 FIBONACCI
# ============================================================================


def render_fibonacci():
    st.header("🧮 Sequência de Fibonacci")

    st.markdown(
        """
    ### 📝 Sobre Fibonacci:
    - **Definição**: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
    - **Aplicações**: Análise de algoritmos, teoria dos grafos, finanças
    - **Complexidade**: O(2^n) recursivo, O(n) iterativo
    """
    )

    n = st.slider("Calcular até:", 5, 20, 10)

    # Abordagem iterativa (eficiente)
    st.subheader("🔢 Abordagem Iterativa (O(n))")

    fib_sequence = [0, 1]
    for i in range(2, n + 1):
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])

    st.write("**Sequência:**", fib_sequence[: n + 1])

    # Visualização
    fig, ax = plt.subplots(figsize=(12, 6))
    x = list(range(len(fib_sequence)))
    y = fib_sequence

    ax.plot(x, y, "bo-", linewidth=2, markersize=8)
    ax.set_title("Sequência de Fibonacci")
    ax.set_xlabel("n")
    ax.set_ylabel("F(n)")
    ax.grid(True, alpha=0.3)

    # Adicionar valores
    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.annotate(f"F({i})={yi}", (xi, yi), textcoords="offset points", xytext=(0, 10), ha="center")

    st.pyplot(fig)

    # Comparação de crescimento
    st.subheader("📈 Comparação de Crescimento")

    ratios = []
    for i in range(2, len(fib_sequence)):
        ratio = fib_sequence[i] / fib_sequence[i - 1]
        ratios.append(ratio)

    if ratios:
        st.write(".4f")
        st.write("**Razão áurea aproximada:**", ratios[-1])


# ============================================================================
# 📈 FATORIAL
# ============================================================================


def render_fatorial():
    st.header("📈 Cálculo de Fatorial")

    st.markdown(
        """
    ### 📝 Sobre Fatorial:
    - **Definição**: n! = n × (n-1) × (n-2) × ... × 1
    - **Aplicações**: Permutações, combinações, probabilidade
    - **Complexidade**: O(n) iterativo, O(2^n) recursivo ineficiente
    """
    )

    n = st.slider("Calcular fatorial de:", 1, 15, 5)

    # Abordagem iterativa
    st.subheader("🔢 Abordagem Iterativa (O(n))")

    resultado = 1
    passos = []

    for i in range(1, n + 1):
        resultado *= i
        passos.append((i, resultado))

    st.write(f"**Resultado:** {n}! = {resultado}")

    # Mostrar cálculo passo a passo
    st.write("**Cálculo passo a passo:**")
    calculo = " × ".join([str(i) for i in range(1, n + 1)])
    st.code(f"{n}! = {calculo} = {resultado}")

    # Visualização
    fig, ax = plt.subplots(figsize=(12, 6))

    x = [p[0] for p in passos]
    y = [p[1] for p in passos]

    ax.plot(x, y, "ro-", linewidth=2, markersize=8)
    ax.set_title("Crescimento do Fatorial")
    ax.set_xlabel("n")
    ax.set_ylabel("n!")
    ax.set_yscale("log")  # Escala logarítmica
    ax.grid(True, alpha=0.3)

    # Adicionar valores
    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.annotate(f"{xi}!={yi}", (xi, yi), textcoords="offset points", xytext=(0, 10), ha="center")

    st.pyplot(fig)

    # Comparação com exponencial
    st.subheader("📊 Comparação com Funções")

    valores_n = list(range(1, 11))
    fatoriais = [np.math.factorial(i) for i in valores_n]
    exponenciais = [2**i for i in valores_n]
    lineares = [i for i in valores_n]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(valores_n, fatoriais, "ro-", label="n!", linewidth=2)
    ax.plot(valores_n, exponenciais, "bs-", label="2^n", linewidth=2)
    ax.plot(valores_n, lineares, "g^-", label="n", linewidth=2)

    ax.set_title("Comparação: n! vs 2^n vs n")
    ax.set_xlabel("n")
    ax.set_ylabel("Valor")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)


# ============================================================================
# 🎯 FUNÇÃO PRINCIPAL
# ============================================================================


def main():
    # Inicializar estado da sessão
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # Sidebar
    st.sidebar.title("🎯 Algoritmos")
    st.sidebar.markdown("---")

    # Menu de navegação
    pages = {
        "🏠 Início": "home",
        "🔍 Busca Binária": "busca_binaria",
        "📊 Ordenação": "ordenacao",
        "🧮 Fibonacci": "fibonacci",
        "📈 Fatorial": "fatorial",
    }

    selected_page = st.sidebar.selectbox("Navegar para:", list(pages.keys()))

    # Atualizar página atual
    st.session_state.current_page = pages[selected_page]

    # Renderizar página
    if st.session_state.current_page == "home":
        render_home()
    elif st.session_state.current_page == "busca_binaria":
        render_busca_binaria()
    elif st.session_state.current_page == "ordenacao":
        render_ordenacao()
    elif st.session_state.current_page == "fibonacci":
        render_fibonacci()
    elif st.session_state.current_page == "fatorial":
        render_fatorial()

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🎯 <strong>Algoritmos Visualizador</strong> |
        Versão Ultra Simplificada |
        Desenvolvido com ❤️ usando Streamlit
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
