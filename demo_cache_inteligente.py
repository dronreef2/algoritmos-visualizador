"""
🎯 DEMONSTRAÇÃO DO SISTEMA DE CACHE INTELIGENTE
===============================================

Este arquivo demonstra como usar o sistema de cache inteligente
implementado no projeto de algoritmos visualizador.

Funcionalidades Demonstradas:
- ✅ Cache de visualizações matplotlib/plotly
- ✅ Cache de algoritmos computacionalmente intensos
- ✅ Cache de consultas MCP
- ✅ Métricas de performance em tempo real
- ✅ Interface Streamlit integrada

Autor: GitHub Copilot
Data: 2025
"""

import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
from cache_inteligente import (
    cache_visualizacao,
    cache_algoritmo,
    cache_mcp,
    obter_cache_stats,
    mostrar_estatisticas_cache,
    limpar_cache,
)

# ============================================================================
# 🎯 EXEMPLO 1: CACHE DE VISUALIZAÇÕES
# ============================================================================


@cache_visualizacao(ttl_seconds=1800)  # Cache por 30 minutos
def criar_grafico_complexo(dados, titulo="Gráfico Complexo"):
    """
    Cria um gráfico complexo com cache inteligente.

    Este gráfico simula uma visualização que leva tempo para ser gerada.
    """
    # Simular processamento demorado
    time.sleep(0.5)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Criar dados complexos
    x = np.linspace(0, 10, len(dados))
    y1 = np.sin(x) * dados
    y2 = np.cos(x) * dados

    ax.plot(x, y1, "b-", label="Seno", linewidth=2)
    ax.plot(x, y2, "r--", label="Cosseno", linewidth=2)
    ax.fill_between(x, y1, y2, alpha=0.3, color="gray")

    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


# ============================================================================
# 🎯 EXEMPLO 2: CACHE DE ALGORITMOS
# ============================================================================


@cache_algoritmo(ttl_seconds=3600)  # Cache por 1 hora
def fibonacci_otimizado(n):
    """
    Calcula Fibonacci com memoização e cache inteligente.

    Este algoritmo é computacionalmente intensivo para valores grandes.
    """
    if n <= 1:
        return n

    # Simular processamento
    time.sleep(0.01)

    memo = {0: 0, 1: 1}

    for i in range(2, n + 1):
        memo[i] = memo[i - 1] + memo[i - 2]

    return memo[n]


@cache_algoritmo(ttl_seconds=3600)
def calcular_primos_ate_n(n):
    """
    Calcula todos os números primos até n usando Crivo de Eratóstenes.

    Algoritmo O(n log log n) que se beneficia muito de cache.
    """
    if n < 2:
        return []

    # Simular processamento
    time.sleep(0.1)

    # Crivo de Eratóstenes
    eh_primo = [True] * (n + 1)
    eh_primo[0] = eh_primo[1] = False

    for i in range(2, int(n**0.5) + 1):
        if eh_primo[i]:
            for j in range(i * i, n + 1, i):
                eh_primo[j] = False

    return [i for i in range(2, n + 1) if eh_primo[i]]


# ============================================================================
# 🎯 EXEMPLO 3: CACHE DE CONSULTAS MCP (SIMULAÇÃO)
# ============================================================================


@cache_mcp(ttl_seconds=1800)  # Cache por 30 minutos
def buscar_informacao_algoritmo(algoritmo, profundidade="basic"):
    """
    Simula busca de informação sobre algoritmos com cache.

    Na implementação real, isso faria uma consulta ao Tavily API.
    """
    # Simular consulta demorada
    time.sleep(0.3)

    # Simular resultados baseados no algoritmo
    resultados = {
        "busca_binaria": {
            "titulo": "Busca Binária - Algoritmo Fundamental",
            "conteudo": "A busca binária é um algoritmo de busca eficiente que funciona dividindo repetidamente o espaço de busca pela metade.",
            "complexidade": "O(log n)",
            "aplicacoes": ["Busca em arrays ordenados", "Otimização de consultas"],
        },
        "dois_ponteiros": {
            "titulo": "Técnica dos Dois Ponteiros",
            "conteudo": "A técnica dos dois ponteiros é usada para problemas que envolvem arrays ou listas ligadas.",
            "complexidade": "O(n)",
            "aplicacoes": ["Container With Most Water", "Problema dos três números"],
        },
        "heap": {
            "titulo": "Heap - Estrutura de Dados",
            "conteudo": "Heap é uma estrutura de dados baseada em árvore especializada em encontrar o mínimo ou máximo rapidamente.",
            "complexidade": "O(log n) para operações",
            "aplicacoes": ["Fila de prioridade", "Ordenação heapsort"],
        },
    }

    return resultados.get(algoritmo, {"erro": "Algoritmo não encontrado"})


# ============================================================================
# 🎯 INTERFACE STREAMLIT PARA DEMONSTRAÇÃO
# ============================================================================


def demo_cache_visualizacoes():
    """Demonstra cache de visualizações."""
    st.markdown("### 📊 Cache de Visualizações")

    st.markdown(
        """
    **Como funciona:**
    - As visualizações são cacheadas automaticamente
    - Mesmo dados geram o mesmo gráfico instantaneamente
    - Cache expira em 30 minutos
    """
    )

    # Controles
    col1, col2 = st.columns(2)

    with col1:
        tamanho = st.slider("Tamanho dos dados:", 10, 100, 50, key="viz_tamanho")
        titulo = st.text_input("Título do gráfico:", "Demonstração de Cache", key="viz_titulo")

    with col2:
        seed = st.number_input("Seed para dados:", 0, 1000, 42, key="viz_seed")

    # Gerar dados
    np.random.seed(seed)
    dados = np.random.randn(tamanho) * 10

    # Botão para gerar visualização
    if st.button("🎨 Gerar Visualização", key="gerar_viz"):
        start_time = time.time()

        with st.spinner("Gerando visualização..."):
            fig = criar_grafico_complexo(dados, titulo)

        end_time = time.time()

        st.pyplot(fig)
        st.success(".3f")

        # Mostrar se foi cacheado
        st.info("💡 Na segunda execução com os mesmos parâmetros, será instantâneo!")


def demo_cache_algoritmos():
    """Demonstra cache de algoritmos."""
    st.markdown("### ⚡ Cache de Algoritmos")

    st.markdown(
        """
    **Como funciona:**
    - Resultados de algoritmos são cacheados
    - Cálculos complexos são executados apenas uma vez
    - Cache expira em 1 hora
    """
    )

    # Fibonacci
    st.markdown("#### 🌀 Fibonacci Otimizado")
    n_fib = st.slider("Calcular Fibonacci de:", 5, 50, 20, key="fib_n")

    if st.button("🔢 Calcular Fibonacci", key="calc_fib"):
        start_time = time.time()
        resultado = fibonacci_otimizado(n_fib)
        end_time = time.time()

        st.success(f"Fibonacci({n_fib}) = {resultado}")
        st.info(".3f")

    # Números primos
    st.markdown("#### 🔢 Números Primos")
    n_primos = st.slider("Calcular primos até:", 10, 200, 50, key="primos_n")

    if st.button("🔍 Calcular Primos", key="calc_primos"):
        start_time = time.time()
        primos = calcular_primos_ate_n(n_primos)
        end_time = time.time()

        st.success(f"Encontrados {len(primos)} números primos até {n_primos}")
        st.write("Primos:", primos[:20], "..." if len(primos) > 20 else "")
        st.info(".3f")


def demo_cache_mcp():
    """Demonstra cache de consultas MCP."""
    st.markdown("### 🔍 Cache de Consultas MCP")

    st.markdown(
        """
    **Como funciona:**
    - Consultas de busca são cacheadas
    - Mesmo termo retorna resultado instantaneamente
    - Cache expira em 30 minutos
    """
    )

    # Seleção de algoritmo
    algoritmos = ["busca_binaria", "dois_ponteiros", "heap"]
    algoritmo = st.selectbox("Algoritmo:", algoritmos, key="mcp_algoritmo")

    profundidade = st.selectbox("Profundidade:", ["basic", "advanced"], key="mcp_profundidade")

    if st.button("🔍 Buscar Informação", key="buscar_mcp"):
        start_time = time.time()
        resultado = buscar_informacao_algoritmo(algoritmo, profundidade)
        end_time = time.time()

        if "erro" not in resultado:
            st.success(f"✅ Informação sobre {algoritmo.replace('_', ' ').title()}")
            st.markdown(f"**Título:** {resultado['titulo']}")
            st.markdown(f"**Conteúdo:** {resultado['conteudo']}")
            st.markdown(f"**Complexidade:** {resultado['complexidade']}")
            st.markdown(f"**Aplicações:** {', '.join(resultado['aplicacoes'])}")
        else:
            st.error(resultado["erro"])

        st.info(".3f")


# ============================================================================
# 🎯 FUNÇÃO PRINCIPAL
# ============================================================================


def main():
    """Função principal da demonstração."""
    st.set_page_config(page_title="🎯 Cache Inteligente Demo", page_icon="🎯", layout="wide")

    st.title("🚀 Sistema de Cache Inteligente")
    st.markdown("---")

    # Abas para diferentes demonstrações
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualizações", "⚡ Algoritmos", "🔍 MCP", "📈 Estatísticas"])

    with tab1:
        demo_cache_visualizacoes()

    with tab2:
        demo_cache_algoritmos()

    with tab3:
        demo_cache_mcp()

    with tab4:
        st.markdown("### 📊 Estatísticas do Sistema de Cache")

        # Botões de controle
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Atualizar Estatísticas", key="atualizar_stats"):
                st.rerun()

        with col2:
            if st.button("🧹 Limpar Cache", key="limpar_cache_demo"):
                limpar_cache()
                st.success("✅ Cache limpo!")
                st.rerun()

        # Mostrar estatísticas
        mostrar_estatisticas_cache()

        # Informações adicionais
        st.markdown("---")
        st.markdown(
            """
        ### 💡 Dicas de Uso

        **Para Visualizações:**
        - Use `@cache_visualizacao()` em funções que criam gráficos matplotlib/plotly
        - Ideal para dados que não mudam frequentemente

        **Para Algoritmos:**
        - Use `@cache_algoritmo()` em funções computacionalmente intensas
        - Perfeito para cálculos recursivos ou iterativos complexos

        **Para Consultas MCP:**
        - Use `@cache_mcp()` em funções que fazem buscas na web
        - Evita chamadas desnecessárias à API

        **Configurações:**
        - TTL padrão: 30 minutos para visualizações, 1 hora para algoritmos
        - Memória máxima: 200MB
        - Compressão automática para dados grandes
        """
        )


if __name__ == "__main__":
    main()
