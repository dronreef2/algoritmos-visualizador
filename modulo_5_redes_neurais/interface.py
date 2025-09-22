"""
INTERFACE PRINCIPAL - Módulo 5: Redes Neurais
===========================================

Interface Streamlit integrada para o módulo de redes neurais,
combinando visualizações, exercícios e integrações MCP.
"""

import streamlit as st
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import time

# Importações do módulo
from .otimizadores import GradienteDescendente, SGD, Adam, otimizar_rede_simples
from .visualizacoes import (
    plot_curva_erro_2d, plot_convergencia, plot_parametros,
    criar_animacao_otimizacao
)
from .exercicios import (
    ExercicioGradienteDescendente, ExercicioFuncaoPerda,
    ExercicioOtimizadorComparacao, criar_interface_exercicio,
    mostrar_dashboard_exercicios
)

# Importações de integrações MCP (se disponíveis)
try:
    from gitmcp_integration import GitMCPIntegration
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


class ModuloRedesNeurais:
    """
    Classe principal para o módulo de redes neurais.
    """

    def __init__(self):
        self.dados_exemplo = self._gerar_dados_exemplo()

    def _gerar_dados_exemplo(self) -> Tuple[np.ndarray, np.ndarray]:
        """Gera dados de exemplo para demonstrações."""
        np.random.seed(42)
        X = np.random.randn(50, 1) * 2
        y = 2 * X.flatten() + 1 + np.random.randn(50) * 0.5
        return X, y

    def mostrar_interface_principal(self):
        """Mostra a interface principal do módulo."""
        st.title("🧠 Redes Neurais: Otimização Visual")
        st.markdown("""
        Explore visualmente como algoritmos de otimização ajustam os parâmetros
        de redes neurais para minimizar funções de perda.
        """)

        # Sidebar com navegação
        with st.sidebar:
            st.header("🎯 Navegação")
            pagina = st.radio(
                "Selecione uma seção:",
                ["📊 Visualização Interativa", "🎮 Exercícios Práticos", "📚 Exemplos do GitHub", "⚙️ Configurações"],
                key="nav_redes"
            )

        # Conteúdo principal baseado na seleção
        if pagina == "📊 Visualização Interativa":
            self._mostrar_visualizacoes()
        elif pagina == "🎮 Exercícios Práticos":
            self._mostrar_exercicios()
        elif pagina == "📚 Exemplos do GitHub":
            self._mostrar_exemplos_github()
        elif pagina == "⚙️ Configurações":
            self._mostrar_configuracoes()

    def _mostrar_visualizacoes(self):
        """Mostra interface de visualizações interativas."""
        st.header("📊 Visualização da Curva de Erro")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("⚙️ Configurações da Otimização")

            # Seleção de otimizador
            otimizador_tipo = st.selectbox(
                "Algoritmo de Otimização:",
                ["Gradiente Descendente", "SGD", "Adam"],
                key="otimizador_select"
            )

            # Parâmetros
            learning_rate = st.slider(
                "Taxa de Aprendizado (lr):",
                min_value=0.001, max_value=1.0, value=0.1, step=0.001,
                format="%.3f", key="lr_slider"
            )

            num_epocas = st.slider(
                "Número de Épocas:",
                min_value=10, max_value=200, value=50, step=10,
                key="epocas_slider"
            )

            # Parâmetros específicos
            momentum = 0.0
            if otimizador_tipo == "SGD":
                momentum = st.slider(
                    "Momentum:",
                    min_value=0.0, max_value=0.9, value=0.0, step=0.1,
                    key="momentum_slider"
                )

            # Botão de execução
            executar = st.button("🚀 Executar Otimização", key="executar_otimizacao")

        with col2:
            st.subheader("📈 Resultados")

            if executar:
                with st.spinner("Executando otimização..."):
                    # Cria otimizador
                    if otimizador_tipo == "Gradiente Descendente":
                        otimizador = GradienteDescendente(learning_rate=learning_rate)
                    elif otimizador_tipo == "SGD":
                        otimizador = SGD(learning_rate=learning_rate, momentum=momentum)
                    else:  # Adam
                        otimizador = Adam(learning_rate=learning_rate)

                    # Executa otimização
                    historico = otimizar_rede_simples(
                        self.dados_exemplo[0], self.dados_exemplo[1],
                        otimizador, num_epocas
                    )

                    # Salva no session_state
                    st.session_state.historico_otimizacao = historico
                    st.session_state.otimizador_usado = otimizador_tipo

                st.success("Otimização concluída!")

            # Mostra resultados se disponíveis
            if 'historico_otimizacao' in st.session_state:
                historico = st.session_state.historico_otimizacao
                otimizador_usado = st.session_state.otimizador_usado

                # Métricas
                perda_inicial = historico['loss'][0]
                perda_final = historico['loss'][-1]
                melhoria = ((perda_inicial - perda_final) / perda_inicial) * 100

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Perda Inicial", f"{perda_inicial:.4f}")
                with col_b:
                    st.metric("Perda Final", f"{perda_final:.4f}")
                with col_c:
                    st.metric("Melhoria", f"{melhoria:.1f}%")

                # Gráficos
                tab1, tab2, tab3, tab4 = st.tabs(["🗻 Curva 3D", "📉 Convergência", "📊 Parâmetros", "🎬 Animação"])

                with tab1:
                    fig_3d = plot_curva_erro_2d(
                        historico, self.dados_exemplo[0], self.dados_exemplo[1],
                        f"Trajetória - {otimizador_usado}"
                    )
                    st.plotly_chart(fig_3d, use_container_width=True)

                with tab2:
                    fig_conv = plot_convergencia(historico, f"Convergência - {otimizador_usado}")
                    st.plotly_chart(fig_conv, use_container_width=True)

                with tab3:
                    fig_params = plot_parametros(historico, f"Parâmetros - {otimizador_usado}")
                    st.plotly_chart(fig_params, use_container_width=True)

                with tab4:
                    fig_anim = criar_animacao_otimizacao(
                        historico, self.dados_exemplo[0], self.dados_exemplo[1],
                        f"Animação - {otimizador_usado}"
                    )
                    st.plotly_chart(fig_anim, use_container_width=True)

    def _mostrar_exercicios(self):
        """Mostra interface de exercícios práticos."""
        st.header("🎮 Exercícios Interativos")

        # Dashboard de progresso
        mostrar_dashboard_exercicios()

        st.divider()

        # Seleção de exercício
        exercicio_opcao = st.selectbox(
            "Escolha um exercício:",
            ["Gradiente Descendente Básico", "Função de Perda MSE", "Comparação de Otimizadores"],
            key="exercicio_select"
        )

        # Cria instância do exercício
        if exercicio_opcao == "Gradiente Descendente Básico":
            exercicio = ExercicioGradienteDescendente()
        elif exercicio_opcao == "Função de Perda MSE":
            exercicio = ExercicioFuncaoPerda()
        else:
            exercicio = ExercicioOtimizadorComparacao()

        # Interface do exercício
        criar_interface_exercicio(exercicio)

    def _mostrar_exemplos_github(self):
        """Mostra exemplos de redes neurais do GitHub."""
        st.header("📚 Exemplos Reais do GitHub")

        if not MCP_AVAILABLE:
            st.warning("Integração MCP não disponível. Instale as dependências necessárias.")
            return

        # Interface de busca
        col1, col2 = st.columns([2, 1])

        with col1:
            query = st.text_input(
                "Buscar exemplos de redes neurais:",
                value="neural network optimization",
                key="github_query"
            )

        with col2:
            buscar = st.button("🔍 Buscar", key="buscar_github")

        if buscar and query:
            with st.spinner("Buscando no GitHub..."):
                git_client = GitMCPIntegration()

                # Busca documentação
                resultado = git_client.buscar_documentacao_algoritmo(query)

                if resultado and resultado.get('status') == 'success':
                    docs = resultado.get('documentacao', [])

                    if docs:
                        st.success(f"Encontrados {len(docs)} exemplos!")

                        for i, doc in enumerate(docs[:5]):  # Mostra top 5
                            with st.expander(f"📄 {doc.get('title', f'Exemplo {i+1}')}"):
                                st.write(doc.get('description', 'Sem descrição'))
                                if 'url' in doc:
                                    st.markdown(f"[Ver no GitHub]({doc['url']})")
                    else:
                        st.info("Nenhum exemplo encontrado. Tente uma busca diferente.")
                else:
                    st.error("Erro na busca. Verifique sua conexão e token do GitHub.")

    def _mostrar_configuracoes(self):
        """Mostra configurações do módulo."""
        st.header("⚙️ Configurações")

        st.subheader("🎨 Visualização")
        tema_grafico = st.selectbox(
            "Tema dos gráficos:",
            ["plotly", "plotly_white", "plotly_dark"],
            key="tema_grafico"
        )

        st.subheader("🎮 Exercícios")
        mostrar_dicas = st.checkbox("Mostrar dicas automaticamente", value=True, key="mostrar_dicas")
        salvar_progresso = st.checkbox("Salvar progresso automaticamente", value=True, key="salvar_progresso")

        st.subheader("🤖 Integrações")
        if MCP_AVAILABLE:
            st.success("✅ Integrações MCP disponíveis")
            usar_cache_mcp = st.checkbox("Usar cache para buscas MCP", value=True, key="cache_mcp")
        else:
            st.warning("❌ Integrações MCP não disponíveis")
            st.info("Para habilitar: pip install -r requirements_mcp.txt")

        # Botão de reset
        if st.button("🔄 Resetar Configurações", key="reset_config"):
            # Reset logic here
            st.success("Configurações resetadas!")


# Função principal para integração com app_integrada.py
def criar_modulo_redes_neurais():
    """Cria instância do módulo de redes neurais."""
    return ModuloRedesNeurais()


# Para execução independente
if __name__ == "__main__":
    modulo = ModuloRedesNeurais()
    modulo.mostrar_interface_principal()