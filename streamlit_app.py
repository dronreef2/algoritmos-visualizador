# 📊 Visualizador de Algoritmos - Exemplo com Streamlit

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from typing import List

# Importar seus algoritmos existentes
import sys
sys.path.append('modulo_1_fundamentos')

def visualizar_busca_binaria():
    """Demonstração interativa da busca binária"""
    st.header("🔍 Busca Binária Interativa")
    
    # Controles da interface
    tamanho = st.slider("Tamanho do array:", 5, 20, 10)
    array = sorted(np.random.randint(1, 100, tamanho))
    target = st.selectbox("Procurar por:", array)
    
    # Visualização
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Simular busca binária com visualização
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
    
    # Plotar cada passo
    passo_atual = st.slider("Passo:", 0, len(passos)-1, 0)
    
    if passo_atual < len(passos):
        esq, dir, meio = passos[passo_atual]
        
        colors = ['lightgray'] * len(array)
        for i in range(esq, dir + 1):
            colors[i] = 'lightblue'
        colors[meio] = 'red'
        
        ax.bar(range(len(array)), array, color=colors)
        ax.set_title(f"Passo {passo_atual + 1}: Verificando posição {meio} (valor {array[meio]})")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        
        # Adicionar anotações
        for i, val in enumerate(array):
            ax.text(i, val + 1, str(val), ha='center')
    
    st.pyplot(fig)
    
    # Mostrar complexidade
    st.info(f"✅ Complexidade: O(log n) - Máximo {int(np.log2(len(array))) + 1} passos")

def demonstrar_metodologia_3_passos():
    """Demonstração da metodologia dos 3 passos"""
    st.header("🧠 Metodologia dos 3 Passos")
    
    problema = st.selectbox("Escolha um problema:", 
                          ["Fibonacci", "Climbing Stairs", "House Robber"])
    
    if problema == "Fibonacci":
        n = st.slider("Calcular F(n):", 1, 40, 10)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("1️⃣ Força Bruta")
            if n <= 30:  # Evitar travamento
                start = time.time()
                # Implementação da força bruta aqui
                resultado = f"F({n}) = resultado"
                tempo = time.time() - start
                st.code(f"""
def fibonacci_bruta(n):
    if n <= 1: return n
    return fibonacci_bruta(n-1) + fibonacci_bruta(n-2)
                """)
                st.success(f"Resultado: {resultado}")
                st.error(f"Tempo: {tempo:.4f}s")
            else:
                st.warning("Muito lento para n > 30")
        
        with col2:
            st.subheader("2️⃣ Memoização")
            st.code(f"""
@lru_cache(maxsize=None)
def fibonacci_memo(n):
    if n <= 1: return n
    return fibonacci_memo(n-1) + fibonacci_memo(n-2)
            """)
            st.success("Tempo: ~0.001s")
            st.info("Melhoria: 1000x+")
        
        with col3:
            st.subheader("3️⃣ Tabulação")
            st.code(f"""
def fibonacci_tab(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b
            """)
            st.success("Tempo: ~0.001s")
            st.info("Espaço: O(1)")

def main():
    """Aplicação principal do Streamlit"""
    st.set_page_config(
        page_title="🧠 Algoritmos Interativos",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Plano de Estudo: Algoritmos Interativos")
    st.sidebar.title("📚 Módulos")
    
    modulo = st.sidebar.selectbox("Escolha um módulo:", [
        "🔍 Busca Binária",
        "🧠 Metodologia 3 Passos",
        "👆 Dois Ponteiros",
        "🪟 Janela Deslizante",
        "🔄 Backtracking",
        "🌐 BFS"
    ])
    
    if modulo == "🔍 Busca Binária":
        visualizar_busca_binaria()
    elif modulo == "🧠 Metodologia 3 Passos":
        demonstrar_metodologia_3_passos()
    else:
        st.info(f"Módulo {modulo} em desenvolvimento...")
    
    # Sidebar com informações
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Objetivos")
    st.sidebar.markdown("""
    - ✅ Visualizar algoritmos
    - ✅ Entender complexidade
    - ✅ Comparar abordagens
    - ✅ Praticar interativamente
    """)

if __name__ == "__main__":
    main()
