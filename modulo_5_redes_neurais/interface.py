"""
INTERFACE PRINCIPAL - Módulo 5: Redes Neurais
===========================================

Interface Streamlit integrada para o módulo de redes neurais,
combinando visualizações, exercícios e integrações MCP.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# Importação Netron (se disponível)
try:
    import netron
    NETRON_AVAILABLE = True
except ImportError:
    NETRON_AVAILABLE = False

# Importação PyTorch (se disponível)
try:
    import torch
    import torch.nn as nn
    from .pytorch_utils import UtilitariosPyTorch, RedeNeuralPyTorch
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False


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
                ["📖 Explicação Visual", "📊 Visualização Interativa", "🔍 Visualização de Modelos", "🔍 Buscar Modelos no GitHub", "🎮 Exercícios Práticos", "🧠 Demonstrações PyTorch", "📚 Exemplos do GitHub", "⚙️ Configurações"],
                key="nav_redes"
            )

        # Conteúdo principal baseado na seleção
        if pagina == "📖 Explicação Visual":
            self._mostrar_explicacao_visual()
        elif pagina == "📊 Visualização Interativa":
            self._mostrar_visualizacoes()
        elif pagina == "🔍 Visualização de Modelos":
            self._mostrar_visualizacao_modelos()
        elif pagina == "🔍 Buscar Modelos no GitHub":
            self._mostrar_busca_github()
        elif pagina == "🎮 Exercícios Práticos":
            self._mostrar_exercicios()
        elif pagina == "🧠 Demonstrações PyTorch":
            self._mostrar_demonstracoes_pytorch()
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

    def _mostrar_visualizacao_modelos(self):
        """Mostra interface para visualização de modelos neurais com Netron."""
        st.header("🔍 Visualização de Modelos Neurais")

        if not NETRON_AVAILABLE:
            st.warning("Netron não está instalado. Instale com: pip install netron")
            return

        st.markdown("""
        Visualize a arquitetura de modelos de redes neurais usando Netron.
        Suporte para formatos: ONNX, TensorFlow Lite, Core ML, Keras, PyTorch, etc.
        """)

        # Opções de modelo
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📁 Selecionar Modelo")

            # Upload de arquivo
            uploaded_file = st.file_uploader(
                "Faça upload de um modelo neural:",
                type=['onnx', 'pb', 'tflite', 'h5', 'pt', 'pth', 'caffemodel', 'pkl'],
                key="model_upload"
            )

            # Modelos de exemplo
            st.subheader("🎯 Modelos de Exemplo")
            modelo_exemplo = st.selectbox(
                "Ou selecione um modelo de exemplo:",
                ["Nenhum", "SqueezeNet (ONNX)", "ResNet50 (ONNX)", "YAMNet (TFLite)"],
                key="modelo_exemplo"
            )

            if modelo_exemplo != "Nenhum":
                st.info("💡 Para usar modelos de exemplo, baixe-os primeiro e coloque na pasta models/")
                if modelo_exemplo == "SqueezeNet (ONNX)":
                    st.code("wget https://github.com/onnx/models/raw/main/vision/classification/squeezenet/model/squeezenet1.0-12.onnx -O models/squeezenet.onnx")
                elif modelo_exemplo == "ResNet50 (ONNX)":
                    st.code("wget https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v2-7.onnx -O models/resnet50.onnx")
                elif modelo_exemplo == "YAMNet (TFLite)":
                    st.code("wget https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1?lite-format=tflite -O models/yamnet.tflite")

            # Lista arquivos locais na pasta models
            import os
            models_dir = os.path.join(os.path.dirname(__file__), "models")
            if os.path.exists(models_dir):
                local_models = [f for f in os.listdir(models_dir) if f.endswith(('.onnx', '.pb', '.tflite', '.h5', '.pt', '.pth'))]
                if local_models:
                    st.subheader("📂 Modelos Locais")
                    modelo_local = st.selectbox(
                        "Modelos disponíveis localmente:",
                        ["Nenhum"] + local_models,
                        key="modelo_local"
                    )

        with col2:
            st.subheader("🚀 Visualização")

            # Botão para visualizar
            modelo_selecionado = uploaded_file is not None or modelo_exemplo != "Nenhum" or ( 'modelo_local' in locals() and modelo_local != "Nenhum")

            if modelo_selecionado:
                if st.button("🔍 Visualizar Modelo", key="visualizar_modelo"):
                    with st.spinner("Iniciando Netron..."):
                        try:
                            if uploaded_file is not None:
                                # Salva arquivo temporário
                                import tempfile
                                import os

                                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                                    tmp_file.write(uploaded_file.getvalue())
                                    model_path = tmp_file.name

                                st.info(f"Arquivo salvo temporariamente: {uploaded_file.name}")

                            elif 'modelo_local' in locals() and modelo_local != "Nenhum":
                                model_path = os.path.join(models_dir, modelo_local)
                                st.info(f"Usando modelo local: {modelo_local}")

                            elif modelo_exemplo == "SqueezeNet (ONNX)":
                                model_path = os.path.join(models_dir, "squeezenet.onnx")
                                if not os.path.exists(model_path):
                                    st.error("Modelo não encontrado. Baixe primeiro usando o comando acima.")
                                    return
                                st.info("Usando SqueezeNet (ONNX)")

                            elif modelo_exemplo == "ResNet50 (ONNX)":
                                model_path = os.path.join(models_dir, "resnet50.onnx")
                                if not os.path.exists(model_path):
                                    st.error("Modelo não encontrado. Baixe primeiro usando o comando acima.")
                                    return
                                st.info("Usando ResNet50 (ONNX)")

                            elif modelo_exemplo == "YAMNet (TFLite)":
                                model_path = os.path.join(models_dir, "yamnet.tflite")
                                if not os.path.exists(model_path):
                                    st.error("Modelo não encontrado. Baixe primeiro usando o comando acima.")
                                    return
                                st.info("Usando YAMNet (TFLite)")

                            # Inicia Netron
                            netron.start(model_path, browse=False)

                            # Mostra link para acessar
                            st.success("✅ Netron iniciado!")
                            st.markdown("""
                            **Para visualizar o modelo:**
                            1. Netron está rodando em segundo plano
                            2. Acesse: [http://localhost:8080](http://localhost:8080)
                            3. Ou clique no botão abaixo para abrir em nova aba
                            """)

                            # Botão para abrir no browser
                            if st.button("🌐 Abrir Netron no Browser", key="abrir_netron"):
                                import webbrowser
                                webbrowser.open("http://localhost:8080")

                        except Exception as e:
                            st.error(f"Erro ao iniciar Netron: {str(e)}")
            else:
                st.info("Selecione um modelo para visualizar.")

    def _mostrar_busca_github(self):
        """Mostra interface para buscar modelos de ML no GitHub."""
        st.header("🔍 Buscar Modelos no GitHub")

        if not MCP_AVAILABLE:
            st.warning("Integração MCP não disponível. Instale as dependências necessárias.")
            return

        st.markdown("""
        Busque e baixe modelos de redes neurais diretamente do GitHub.
        Suporte para todos os formatos compatíveis com Netron.
        """)

        # Formulário de busca
        col1, col2 = st.columns([2, 1])

        with col1:
            with st.form("form_busca_github"):
                st.subheader("🔍 Buscar Modelos")

                # Termo de busca
                query = st.text_input(
                    "Termo de busca:",
                    placeholder="Ex: resnet, yolov5, mobilenet...",
                    help="Nome do modelo ou arquitetura (ex: resnet50, yolov5, efficientnet)"
                )

                # Formato específico
                formatos = ["Todos", "ONNX", "TensorFlow Lite", "Keras", "PyTorch", "Core ML", "Darknet", "TensorFlow", "Caffe"]
                formato_selecionado = st.selectbox(
                    "Formato do modelo:",
                    formatos,
                    help="Filtrar por formato específico do modelo"
                )

                # Número máximo de resultados
                max_results = st.slider(
                    "Máximo de resultados:",
                    min_value=5, max_value=50, value=20, step=5,
                    help="Número máximo de modelos a buscar"
                )

                # Botão de busca
                buscar = st.form_submit_button("🔍 Buscar Modelos", type="primary", use_container_width=True)

        with col2:
            st.subheader("📋 Formatos Suportados")
            st.markdown("""
            **🤖 Modelos Suportados:**
            - **ONNX** (.onnx)
            - **TensorFlow Lite** (.tflite)
            - **Keras** (.h5, .keras)
            - **PyTorch** (.pt, .pth, .pkl)
            - **Core ML** (.mlmodel)
            - **Darknet** (.cfg + .weights)
            - **TensorFlow** (.pb, .meta)
            - **Caffe** (.caffemodel)
            """)

            st.info("💡 **Dica:** Modelos grandes podem demorar para baixar. Verifique o tamanho antes!")

        # Executa busca se formulário foi submetido
        if buscar and query.strip():
            with st.spinner("🔍 Buscando modelos no GitHub..."):
                try:
                    git_client = GitMCPIntegration()

                    # Mapeia formato selecionado
                    formato_map = {
                        "Todos": None,
                        "ONNX": "onnx",
                        "TensorFlow Lite": "tflite",
                        "Keras": "keras",
                        "PyTorch": "pytorch",
                        "Core ML": "coreml",
                        "Darknet": "darknet",
                        "TensorFlow": "tensorflow",
                        "Caffe": "caffe"
                    }

                    formato = formato_map.get(formato_selecionado)

                    # Busca modelos
                    resultado = git_client.buscar_modelos_ml(
                        query=query.strip(),
                        formato=formato,
                        max_results=max_results
                    )

                    if resultado and resultado.get("status") == "success":
                        modelos = resultado.get("modelos", [])

                        if modelos:
                            st.success(f"✅ Encontrados {len(modelos)} modelos!")

                            # Mostra resultados
                            for i, modelo in enumerate(modelos, 1):
                                with st.expander(f"🤖 {i}. {modelo['nome']} ({modelo['formato']})"):
                                    col1, col2 = st.columns([2, 1])

                                    with col1:
                                        st.markdown(f"**📁 Nome:** {modelo['nome']}")
                                        st.markdown(f"**📂 Caminho:** {modelo['caminho']}")
                                        st.markdown(f"**🏢 Repositório:** {modelo['repositorio']}")
                                        if modelo.get('stars', 0) > 0:
                                            st.markdown(f"**⭐ Stars:** {modelo['stars']}")
                                        if modelo.get('descricao'):
                                            st.markdown(f"**📝 Descrição:** {modelo['descricao'][:200]}...")

                                    with col2:
                                        # Botão para visualizar no GitHub
                                        st.markdown(f"[🔗 Ver no GitHub]({modelo['url']})")

                                        # Botão para baixar modelo
                                        if st.button(f"📥 Baixar Modelo", key=f"download_{i}"):
                                            self._baixar_modelo_github(modelo)

                                        # Botão para visualizar diretamente (se Netron disponível)
                                        if NETRON_AVAILABLE:
                                            if st.button(f"🔍 Visualizar", key=f"visualizar_{i}"):
                                                self._visualizar_modelo_url(modelo['download_url'], modelo['nome'])

                            # Estatísticas da busca
                            st.markdown("---")
                            st.subheader("📊 Estatísticas da Busca")
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric("Modelos Encontrados", len(modelos))

                            with col2:
                                st.metric("Formato Buscado", formato_selecionado)

                            with col3:
                                st.metric("Query", f'"{query}"')

                        else:
                            st.warning("Nenhum modelo encontrado com os critérios especificados.")
                            st.info("💡 **Dicas:**\n- Tente termos mais gerais (ex: 'resnet' ao invés de 'resnet50')\n- Verifique se o formato está correto\n- Alguns modelos podem estar em repositórios privados")

                    else:
                        st.error("Erro na busca. Verifique sua conexão e token do GitHub.")

                except Exception as e:
                    st.error(f"Erro inesperado: {str(e)}")
                    st.info("Verifique se a integração MCP está funcionando corretamente.")

        elif buscar:
            st.warning("Por favor, digite um termo de busca.")

    def _baixar_modelo_github(self, modelo: dict):
        """Baixa um modelo do GitHub e salva na pasta models."""
        try:
            import requests
            import os
            from pathlib import Path

            # Cria diretório se não existir
            models_dir = Path(__file__).parent / "models"
            models_dir.mkdir(exist_ok=True)

            # Caminho do arquivo
            filename = modelo['nome']
            filepath = models_dir / filename

            # Verifica se arquivo já existe
            if filepath.exists():
                overwrite = st.checkbox(f"Arquivo {filename} já existe. Sobrescrever?", key=f"overwrite_{filename}")
                if not overwrite:
                    st.info(f"Download cancelado. Arquivo {filename} já existe.")
                    return

            # Download do arquivo
            with st.spinner(f"📥 Baixando {filename}..."):
                response = requests.get(modelo['download_url'], timeout=60)
                response.raise_for_status()

                # Salva arquivo
                with open(filepath, 'wb') as f:
                    f.write(response.content)

                tamanho_mb = len(response.content) / (1024 * 1024)
                st.success(f"✅ Download concluído! Tamanho: {tamanho_mb:.1f} MB")
                st.info(f"📁 Salvo em: {filepath}")

                # Botão para visualizar imediatamente
                if NETRON_AVAILABLE:
                    if st.button("🔍 Visualizar Agora", key=f"view_now_{filename}"):
                        self._visualizar_modelo_arquivo(str(filepath))

        except requests.exceptions.RequestException as e:
            st.error(f"Erro no download: {str(e)}")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")

    def _visualizar_modelo_url(self, url: str, nome: str):
        """Visualiza um modelo diretamente de uma URL."""
        try:
            if NETRON_AVAILABLE:
                with st.spinner(f"Iniciando Netron para {nome}..."):
                    netron.start(url, browse=False)
                    st.success("✅ Netron iniciado!")
                    st.markdown(f"""
                    **Visualizando:** {nome}
                    - Acesse: [http://localhost:8080](http://localhost:8080)
                    - Ou clique no botão abaixo para abrir no browser
                    """)

                    if st.button("🌐 Abrir Netron", key=f"open_netron_{nome}"):
                        import webbrowser
                        webbrowser.open("http://localhost:8080")
            else:
                st.error("Netron não está disponível.")
        except Exception as e:
            st.error(f"Erro ao iniciar Netron: {str(e)}")

    def _visualizar_modelo_arquivo(self, filepath: str):
        """Visualiza um modelo de um arquivo local."""
        try:
            if NETRON_AVAILABLE:
                with st.spinner("Iniciando Netron..."):
                    netron.start(filepath, browse=False)
                    st.success("✅ Netron iniciado!")
                    st.markdown("""
                    **Modelo carregado com sucesso!**
                    - Acesse: [http://localhost:8080](http://localhost:8080)
                    - Ou clique no botão abaixo para abrir no browser
                    """)

                    if st.button("🌐 Abrir Netron", key="open_netron_local"):
                        import webbrowser
                        webbrowser.open("http://localhost:8080")
            else:
                st.error("Netron não está disponível.")
        except Exception as e:
            st.error(f"Erro ao iniciar Netron: {str(e)}")
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

    def _mostrar_explicacao_visual(self):
        """Mostra explicação visual e interativa de conceitos de redes neurais."""
        st.header("📖 Explicação Visual: Redes Neurais")

        st.markdown("""
        **Bem-vindo à jornada visual pelas Redes Neurais!** 🎨

        Aqui você aprenderá os conceitos fundamentais de forma interativa e visual,
        desde neurônios básicos até arquiteturas complexas de deep learning.
        """)

        # Abas principais para organizar o conteúdo
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🧠 Neurônio Artificial",
            "🏗️ Arquiteturas",
            "⚡ Funções de Ativação",
            "🔄 Propagação",
            "🎯 Aplicações"
        ])

        with tab1:
            self._explicar_neuronio()

        with tab2:
            self._explicar_arquiteturas()

        with tab3:
            self._explicar_funcoes_ativacao()

        with tab4:
            self._explicar_propagacao()

        with tab5:
            self._explicar_aplicacoes()

    def _explicar_neuronio(self):
        """Explica visualmente o conceito de neurônio artificial."""
        st.subheader("🧠 Neurônio Artificial")

        st.markdown("""
        ### O que é um Neurônio Artificial?

        Um **neurônio artificial** é a unidade básica de uma rede neural, inspirado
        no funcionamento dos neurônios biológicos do cérebro humano.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            ### 📊 Componentes de um Neurônio

            **1. Entradas (Inputs)**: Dados que chegam ao neurônio
            - Cada entrada tem um **peso** associado
            - Pesos determinam a importância de cada entrada

            **2. Soma Ponderada**: Combinação linear das entradas
            ```
            z = w₁×x₁ + w₂×x₂ + ... + wₙ×xₙ + b
            ```

            **3. Função de Ativação**: Decide se o neurônio "dispara"
            - Transforma a soma em uma saída não-linear

            **4. Saída (Output)**: Resultado final do neurônio
            """)

        with col2:
            # Visualização interativa de um neurônio
            st.markdown("### 🎮 Simulação Interativa")

            # Sliders para pesos e bias
            w1 = st.slider("Peso w₁", -2.0, 2.0, 0.5, 0.1, key="w1_neuronio")
            w2 = st.slider("Peso w₂", -2.0, 2.0, -0.8, 0.1, key="w2_neuronio")
            bias = st.slider("Bias (b)", -1.0, 1.0, 0.1, 0.1, key="bias_neuronio")

            # Seleção de função de ativação
            ativacao = st.selectbox(
                "Função de Ativação:",
                ["Step", "Sigmoid", "ReLU", "Tanh"],
                key="ativacao_neuronio"
            )

            # Entradas fixas para demonstração
            x1, x2 = 1.0, 0.5

            # Cálculo da soma ponderada
            z = w1 * x1 + w2 * x2 + bias

            # Aplicação da função de ativação
            if ativacao == "Step":
                output = 1 if z >= 0 else 0
                formula = "output = 1 if z ≥ 0 else 0"
            elif ativacao == "Sigmoid":
                output = 1 / (1 + np.exp(-z))
                formula = "output = 1 / (1 + e^(-z))"
            elif ativacao == "ReLU":
                output = max(0, z)
                formula = "output = max(0, z)"
            else:  # Tanh
                output = np.tanh(z)
                formula = "output = tanh(z)"

            # Exibição dos cálculos
            st.markdown("### 🔢 Cálculos")
            st.latex(f"z = {w1:.1f} \\times {x1} + {w2:.1f} \\times {x2} + {bias:.1f} = {z:.3f}")
            st.latex(f"\\text{{{formula}}}")
            st.latex(f"\\text{{output}} = {output:.3f}")

            # Visualização gráfica
            st.markdown("### 📈 Visualização")

            # Gráfico da função de ativação
            x_range = np.linspace(-3, 3, 100)

            if ativacao == "Step":
                y_range = [1 if x >= 0 else 0 for x in x_range]
            elif ativacao == "Sigmoid":
                y_range = 1 / (1 + np.exp(-x_range))
            elif ativacao == "ReLU":
                y_range = [max(0, x) for x in x_range]
            else:  # Tanh
                y_range = np.tanh(x_range)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x_range, y_range, 'b-', linewidth=2, label=f'Função {ativacao}')
            ax.axvline(x=z, color='r', linestyle='--', alpha=0.7, label=f'z = {z:.2f}')
            ax.axhline(y=output, color='g', linestyle='--', alpha=0.7, label=f'output = {output:.2f}')
            ax.scatter([z], [output], color='red', s=100, zorder=5)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_xlabel('Entrada (z)')
            ax.set_ylabel('Saída')
            ax.set_title(f'Função de Ativação: {ativacao}')

            st.pyplot(fig)

    def _explicar_arquiteturas(self):
        """Explica diferentes arquiteturas de redes neurais."""
        st.subheader("🏗️ Arquiteturas de Redes Neurais")

        st.markdown("""
        ### Camadas e Arquiteturas

        As redes neurais são organizadas em **camadas** conectadas, formando
        arquiteturas que resolvem diferentes tipos de problemas.
        """)

        # Seleção de arquitetura
        arquitetura = st.selectbox(
            "Escolha uma arquitetura para explorar:",
            ["Perceptron Simples", "MLP (Multi-Layer Perceptron)", "CNN (Convolutional Neural Network)", "RNN (Recurrent Neural Network)"],
            key="arquitetura_select"
        )

        if arquitetura == "Perceptron Simples":
            self._explicar_perceptron()
        elif arquitetura == "MLP (Multi-Layer Perceptron)":
            self._explicar_mlp()
        elif arquitetura == "CNN (Convolutional Neural Network)":
            self._explicar_cnn()
        else:  # RNN
            self._explicar_rnn()

    def _explicar_perceptron(self):
        """Explica o perceptron simples."""
        st.markdown("### 🔸 Perceptron Simples")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            **Conceito:**
            O **Perceptron** é a rede neural mais simples, capaz de resolver
            problemas linearmente separáveis.

            **Características:**
            - Uma única camada de neurônios
            - Função de ativação step
            - Aprendizado supervisionado
            - Classificação binária

            **Aplicações:**
            - Porta lógica AND/OR
            - Classificação simples
            - Base para redes maiores
            """)

        with col2:
            # Diagrama ASCII do perceptron
            st.code("""
Entrada 1 ── w₁ ──┐
                    ├── Somador ── Função Step ── Saída
Entrada 2 ── w₂ ──┘
         Bias ── b ──┘
            """, language="text")

            # Exemplo interativo
            st.markdown("### 🎮 Exemplo: Porta Lógica AND")

            # Dados da porta AND
            dados_and = [
                ([0, 0], 0),
                ([0, 1], 0),
                ([1, 0], 0),
                ([1, 1], 1)
            ]

            # Sliders para pesos
            w1 = st.slider("Peso w₁", -2.0, 2.0, 0.5, 0.1, key="w1_and")
            w2 = st.slider("Peso w₂", -2.0, 2.0, 0.5, 0.1, key="w2_and")
            bias = st.slider("Bias", -2.0, 2.0, -0.8, 0.1, key="bias_and")

            st.markdown("### 📊 Resultados")

            resultados = []
            correto = 0

            for entrada, esperado in dados_and:
                z = w1 * entrada[0] + w2 * entrada[1] + bias
                predicao = 1 if z >= 0 else 0
                acerto = "✅" if predicao == esperado else "❌"
                resultados.append(f"{entrada} → {predicao} (esperado: {esperado}) {acerto}")
                if predicao == esperado:
                    correto += 1

            for resultado in resultados:
                st.write(resultado)

            accuracy = correto / len(dados_and) * 100
            if accuracy == 100:
                st.success(f"Acurácia: {accuracy:.1f}% - Perfeito! Todos os exemplos classificados corretamente.")
            else:
                st.warning(f"Acurácia: {accuracy:.1f}% - Ajuste os pesos para melhorar a classificação.")
    def _explicar_mlp(self):
        """Explica Multi-Layer Perceptron."""
        st.markdown("### 🔸 Multi-Layer Perceptron (MLP)")

        st.markdown("""
        **O que é um MLP?**

        O **Multi-Layer Perceptron** é uma rede neural feedforward composta por
        múltiplas camadas de neurônios, capaz de aprender representações complexas.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            **Arquitetura Típica:**

            **1. Camada de Entrada (Input Layer)**
            - Recebe os dados brutos
            - Número de neurônios = número de features

            **2. Camadas Ocultas (Hidden Layers)**
            - Processam informações intermediárias
            - Podem ter diferentes números de neurônios
            - Funções de ativação não-lineares

            **3. Camada de Saída (Output Layer)**
            - Produz o resultado final
            - Número de neurônios depende do problema

            **4. Conexões**
            - Totalmente conectadas (fully connected)
            - Cada neurônio conectado a todos da camada seguinte
            """)

        with col2:
            # Diagrama visual da arquitetura
            st.markdown("### 🏗️ Diagrama da Arquitetura")

            # Criar diagrama simples com matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))

            # Camadas
            camadas = [4, 6, 6, 3]  # input, hidden1, hidden2, output
            nomes = ['Entrada', 'Oculta 1', 'Oculta 2', 'Saída']

            # Posições das camadas
            x_pos = np.linspace(0.1, 0.9, len(camadas))
            y_centers = [0.5] * len(camadas)

            # Desenhar neurônios
            for i, (x, neurons, nome) in enumerate(zip(x_pos, camadas, nomes)):
                y_pos = np.linspace(0.2, 0.8, neurons)
                ax.scatter([x] * neurons, y_pos, s=200, c='lightblue', edgecolors='blue', zorder=3)
                ax.text(x, 0.9, nome, ha='center', va='bottom', fontsize=10, fontweight='bold')

                # Conexões para a próxima camada (exceto última)
                if i < len(camadas) - 1:
                    next_x = x_pos[i + 1]
                    next_y = np.linspace(0.2, 0.8, camadas[i + 1])
                    for y1 in y_pos:
                        for y2 in next_y:
                            ax.plot([x, next_x], [y1, y2], 'gray', alpha=0.3, linewidth=1)

            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.set_title('Arquitetura MLP Típica')

            st.pyplot(fig)

        # Demonstração interativa
        st.markdown("### 🎮 Demonstração Interativa")

        st.markdown("""
        **Problema:** Classificação de pontos em um plano 2D

        Os pontos azuis devem ser classificados como classe 0, os vermelhos como classe 1.
        Uma linha reta (decisão linear) não consegue separar essas classes.
        """)

        # Gerar dados não-linearmente separáveis
        np.random.seed(42)

        # Classe 0: círculo interno
        theta0 = np.random.uniform(0, 2*np.pi, 50)
        r0 = np.random.uniform(0, 0.7, 50)
        x0 = r0 * np.cos(theta0)
        y0 = r0 * np.sin(theta0)

        # Classe 1: círculo externo
        theta1 = np.random.uniform(0, 2*np.pi, 50)
        r1 = np.random.uniform(0.8, 1.2, 50)
        x1 = r1 * np.cos(theta1)
        y1 = r1 * np.sin(theta1)

        # Plotar dados
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x0, y0, c='blue', label='Classe 0', alpha=0.7)
        ax.scatter(x1, y1, c='red', label='Classe 1', alpha=0.7)
        ax.set_xlabel('Feature 1')
        ax.set_ylabel('Feature 2')
        ax.set_title('Dados Não-Linearmente Separáveis')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Adicionar círculo de decisão teórico
        circle = plt.Circle((0, 0), 0.75, fill=False, color='green', linestyle='--', linewidth=2, label='Fronteira de decisão ideal')
        ax.add_patch(circle)
        ax.legend()

        st.pyplot(fig)

        st.info("""
        💡 **Por que MLP consegue resolver isso?**

        As camadas ocultas com funções de ativação não-lineares permitem que a rede
        aprenda **representações não-lineares** dos dados, criando fronteiras de decisão
        complexas que separam as classes de forma não-linear.
        """)

    def _explicar_cnn(self):
        """Explica Convolutional Neural Networks."""
        st.markdown("### 🔸 Convolutional Neural Networks (CNN)")

        st.markdown("""
        **Para que servem as CNNs?**

        As **Redes Neurais Convolucionais** são especializadas no processamento de
        dados com estrutura de grade, como imagens, vídeos e sinais.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            **Componentes Principais:**

            **1. Camada Convolucional**
            - Extrai features locais da imagem
            - Filtros aprendíveis (kernels)
            - Reduz dimensionalidade

            **2. Pooling**
            - Redução de dimensionalidade
            - Max Pooling ou Average Pooling
            - Invariância a pequenas translações

            **3. Camadas Fully Connected**
            - Classificação final
            - Combinam features globais

            **4. Dropout**
            - Regularização
            - Previne overfitting
            """)

        with col2:
            # Demonstração de convolução
            st.markdown("### 🔍 Demonstração: Convolução")

            # Criar uma imagem simples 5x5
            imagem = np.array([
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]
            ])

            # Filtro vertical
            filtro = np.array([
                [-1, 0, 1],
                [-1, 0, 1],
                [-1, 0, 1]
            ])

            # Aplicar convolução manual
            resultado = np.zeros((3, 3))
            for i in range(3):
                for j in range(3):
                    patch = imagem[i:i+3, j:j+3]
                    resultado[i, j] = np.sum(patch * filtro)

            # Mostrar resultado
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Imagem Original**")
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.imshow(imagem, cmap='gray')
                ax.axis('off')
                st.pyplot(fig)

            with col2:
                st.markdown("**Filtro Vertical**")
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.imshow(filtro, cmap='RdBu', vmin=-1, vmax=1)
                ax.axis('off')
                st.pyplot(fig)

            with col3:
                st.markdown("**Resultado**")
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.imshow(resultado, cmap='RdBu')
                ax.axis('off')
                st.pyplot(fig)

    def _explicar_rnn(self):
        """Explica Recurrent Neural Networks."""
        st.markdown("### 🔸 Recurrent Neural Networks (RNN)")

        st.markdown("""
        **Para que servem as RNNs?**

        As **Redes Neurais Recorrentes** são projetadas para processar sequências
        de dados, mantendo um estado interno que captura dependências temporais.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            **Características:**

            **1. Estado Interno (Memory)**
            - Mantém informação sobre passos anteriores
            - Permite processar sequências

            **2. Compartilhamento de Pesos**
            - Mesmos pesos para cada timestep
            - Eficiência computacional

            **3. Backpropagation Through Time**
            - Algoritmo de treinamento especial
            - Lida com dependências temporais

            **4. Aplicações**
            - Processamento de linguagem natural
            - Previsão de séries temporais
            - Reconhecimento de fala
            """)

        with col2:
            # Diagrama de RNN desenrolada
            st.markdown("### ⏰ RNN Desenrolada no Tempo")

            fig, ax = plt.subplots(figsize=(12, 4))

            # Desenhar a RNN desenrolada
            timesteps = 5
            x_positions = np.linspace(0.1, 0.9, timesteps)

            # Neurônios da RNN
            for i, x in enumerate(x_positions):
                # Círculo do neurônio
                circle = plt.Circle((x, 0.5), 0.08, fill=True, color='lightblue', ec='blue', linewidth=2)
                ax.add_patch(circle)

                # Estado interno
                ax.text(x, 0.5, f'h{timesteps-1-i}', ha='center', va='center', fontweight='bold')

                # Entrada
                ax.arrow(x-0.05, 0.7, 0, -0.1, head_width=0.02, head_length=0.02, fc='green', ec='green')
                ax.text(x, 0.75, f'x{timesteps-1-i}', ha='center', va='bottom', color='green')

                # Saída
                ax.arrow(x, 0.42, 0, -0.1, head_width=0.02, head_length=0.02, fc='red', ec='red')
                ax.text(x, 0.35, f'y{timesteps-1-i}', ha='center', va='top', color='red')

                # Conexão para o próximo timestep
                if i < len(x_positions) - 1:
                    ax.arrow(x+0.08, 0.5, 0.14, 0, head_width=0.03, head_length=0.02, fc='orange', ec='orange')

            ax.set_xlim(0, 1)
            ax.set_ylim(0.2, 0.8)
            ax.axis('off')
            ax.set_title('RNN Desenrolada - Processamento Sequencial')

            st.pyplot(fig)

        # Demonstração de problema de vanishing gradient
        st.markdown("### ⚠️ Problema do Gradiente Desvanecente")

        st.markdown("""
        **Por que RNNs têm problemas?**

        Durante o backpropagation, os gradientes podem "desvanecer" ou "explodir"
        ao serem propagados através de muitos timesteps, dificultando o aprendizado
        de dependências longas.
        """)

        # Simulação do vanishing gradient
        timesteps_range = st.slider("Número de timesteps", 5, 50, 20, key="timesteps_vanishing")

        # Simular decaimento exponencial do gradiente
        gradiente_inicial = 1.0
        decay_rate = 0.95  # Taxa de decaimento

        gradientes = [gradiente_inicial]
        for t in range(1, timesteps_range):
            gradiente = gradientes[-1] * decay_rate
            gradientes.append(gradiente)

        # Plotar
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(range(timesteps_range), gradientes, 'r-', linewidth=2, marker='o')
        ax.set_xlabel('Timestep')
        ax.set_ylabel('Magnitude do Gradiente')
        ax.set_title('Vanishing Gradient Problem')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)

        # Linha de referência
        ax.axhline(y=0.01, color='orange', linestyle='--', alpha=0.7, label='Threshold crítico')
        ax.legend()

        st.pyplot(fig)

        st.info("""
        💡 **Soluções para Vanishing Gradient:**
        - **LSTM** (Long Short-Term Memory)
        - **GRU** (Gated Recurrent Unit)
        - **Residual Connections**
        - **Gradient Clipping**
        """)

    def _explicar_funcoes_ativacao(self):
        """Explica funções de ativação."""
        st.markdown("## ⚡ Funções de Ativação")

        st.markdown("""
        **Por que precisamos de funções de ativação?**

        As **funções de ativação** introduzem não-linearidade nas redes neurais,
        permitindo que aprendam representações complexas dos dados.
        """)

        # Seleção de função para explorar
        funcao = st.selectbox(
            "Escolha uma função de ativação:",
            ["Sigmoid", "Tanh", "ReLU", "Leaky ReLU", "ELU", "Softmax"],
            key="funcao_ativacao"
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            # Descrição da função
            descricoes = {
                "Sigmoid": {
                    "formula": "σ(x) = 1 / (1 + e^(-x))",
                    "range": "(0, 1)",
                    "vantagens": ["Saída probabilística", "Suave e diferenciável"],
                    "desvantagens": ["Vanishing gradient", "Não centrada em zero", "Computacionalmente cara"],
                    "usos": ["Classificação binária", "Camada de saída"]
                },
                "Tanh": {
                    "formula": "tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))",
                    "range": "(-1, 1)",
                    "vantagens": ["Centrada em zero", "Mais forte que sigmoid"],
                    "desvantagens": ["Vanishing gradient", "Computacionalmente cara"],
                    "usos": ["Camadas ocultas", "RNNs"]
                },
                "ReLU": {
                    "formula": "ReLU(x) = max(0, x)",
                    "range": "[0, ∞)",
                    "vantagens": ["Resolve vanishing gradient", "Computacionalmente eficiente", "Converge rápido"],
                    "desvantagens": ["Dying ReLU problem", "Não centrada em zero"],
                    "usos": ["Camadas ocultas em CNNs", "Redes profundas"]
                },
                "Leaky ReLU": {
                    "formula": "LeakyReLU(x) = max(αx, x) onde α=0.01",
                    "range": "(-∞, ∞)",
                    "vantagens": ["Resolve dying ReLU", "Não saturada"],
                    "desvantagens": ["Parâmetro extra α", "Resultados inconsistentes"],
                    "usos": ["Substituto do ReLU", "Quando ReLU morre"]
                },
                "ELU": {
                    "formula": "ELU(x) = x se x > 0 senão α(e^x - 1)",
                    "range": "(-α, ∞)",
                    "vantagens": ["Suave em zero", "Resolve dying ReLU", "Centrada em zero"],
                    "desvantagens": ["Computacionalmente cara", "Parâmetro extra"],
                    "usos": ["Redes profundas", "Quando precisão importa"]
                },
                "Softmax": {
                    "formula": "Softmax(x_i) = e^(x_i) / Σ e^(x_j)",
                    "range": "(0, 1), soma = 1",
                    "vantagens": ["Probabilidades normalizadas", "Usada em classificação multiclasse"],
                    "desvantagens": ["Sensível a outliers", "Não para regressão"],
                    "usos": ["Camada de saída", "Classificação multiclasse"]
                }
            }

            info = descricoes[funcao]

            st.markdown(f"### Fórmula: {funcao}")
            st.latex(info["formula"])
            st.markdown(f"**Range:** {info['range']}")

            st.markdown("**✅ Vantagens:**")
            for v in info["vantagens"]:
                st.markdown(f"- {v}")

            st.markdown("**❌ Desvantagens:**")
            for d in info["desvantagens"]:
                st.markdown(f"- {d}")

            st.markdown("**🎯 Usos:**")
            for u in info["usos"]:
                st.markdown(f"- {u}")

        with col2:
            # Gráfico da função
            x = np.linspace(-3, 3, 200)

            if funcao == "Sigmoid":
                y = 1 / (1 + np.exp(-x))
            elif funcao == "Tanh":
                y = np.tanh(x)
            elif funcao == "ReLU":
                y = np.maximum(0, x)
            elif funcao == "Leaky ReLU":
                alpha = 0.1
                y = np.where(x > 0, x, alpha * x)
            elif funcao == "ELU":
                alpha = 1.0
                y = np.where(x > 0, x, alpha * (np.exp(x) - 1))
            else:  # Softmax (exemplo com 3 classes)
                # Exemplo com valores diferentes
                x_softmax = np.array([x, x*0.5, x*0.3]).T
                exp_x = np.exp(x_softmax - np.max(x_softmax, axis=1, keepdims=True))
                y = exp_x / np.sum(exp_x, axis=1, keepdims=True)
                # Plotar apenas a primeira classe para visualização
                y = y[:, 0]

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, y, 'b-', linewidth=2, label=funcao)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Entrada (x)')
            ax.set_ylabel('Saída')
            ax.set_title(f'Função de Ativação: {funcao}')
            ax.legend()

            # Adicionar linhas de referência
            if funcao in ["Sigmoid", "Tanh"]:
                ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
            if funcao == "Sigmoid":
                ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='y=0.5')
                ax.legend()

            st.pyplot(fig)

    def _explicar_propagacao(self):
        """Explica forward e backward propagation."""
        st.markdown("## 🔄 Propagação: Forward e Backward")

        st.markdown("""
        **Como as Redes Neurais Aprendem?**

        O aprendizado em redes neurais acontece através de dois processos principais:
        **propagação para frente (forward)** e **retropropagação (backward)**.
        """)

        tab1, tab2 = st.tabs(["⬆️ Forward Propagation", "⬇️ Backward Propagation"])

        with tab1:
            self._explicar_forward_propagation()

        with tab2:
            self._explicar_backward_propagation()

    def _explicar_forward_propagation(self):
        """Explica forward propagation."""
        st.markdown("### ⬆️ Forward Propagation")

        st.markdown("""
        **O que é Forward Propagation?**

        A **propagação para frente** é o processo de calcular as saídas da rede
        neural a partir das entradas, passando pelos pesos e funções de ativação.
        """)

        # Exemplo interativo
        st.markdown("### 🎮 Exemplo Interativo: Rede de 2 Camadas")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            **Arquitetura:**
            - Entrada: 2 neurônios
            - Oculta: 3 neurônios (ReLU)
            - Saída: 1 neurônio (Sigmoid)

            **Pesos e Bias:**
            - W1: 2×3 matriz
            - b1: 3 valores
            - W2: 3×1 matriz
            - b2: 1 valor
            """)

        with col2:
            # Inputs fixos
            x1 = st.slider("Entrada x₁", -2.0, 2.0, 1.0, 0.1, key="x1_forward")
            x2 = st.slider("Entrada x₂", -2.0, 2.0, 0.5, 0.1, key="x2_forward")

            X = np.array([[x1], [x2]])

            # Pesos fixos para demonstração
            W1 = np.array([[0.5, -0.3, 0.8], [0.2, 0.9, -0.1]])
            b1 = np.array([[0.1], [0.2], [0.05]])
            W2 = np.array([[0.7, -0.5, 0.3]])
            b2 = np.array([[0.1]])

            # Forward pass
            Z1 = np.dot(W1.T, X) + b1  # W1.T @ X + b1
            A1 = np.maximum(0, Z1)  # ReLU
            Z2 = np.dot(W2, A1) + b2  # W2 @ A1 + b2
            A2 = 1 / (1 + np.exp(-Z2))  # Sigmoid

            st.markdown("### 🔢 Cálculos Passo a Passo")

            st.latex(f"\\mathbf{{X}} = \\begin{{pmatrix}} {x1:.1f} \\\\ {x2:.1f} \\end{{pmatrix}}")

            st.latex(f"\\mathbf{{Z1}} = \\mathbf{{W1}}^T \\mathbf{{X}} + \\mathbf{{b1}} = \\begin{{pmatrix}} {Z1[0,0]:.3f} \\\\ {Z1[1,0]:.3f} \\\\ {Z1[2,0]:.3f} \\end{{pmatrix}}")

            st.latex(f"\\mathbf{{A1}} = \\text{{ReLU}}(\\mathbf{{Z1}}) = \\begin{{pmatrix}} {A1[0,0]:.3f} \\\\ {A1[1,0]:.3f} \\\\ {A1[2,0]:.3f} \\end{{pmatrix}}")

            st.latex(f"\\mathbf{{Z2}} = \\mathbf{{W2}} \\mathbf{{A1}} + \\mathbf{{b2}} = {Z2[0,0]:.3f}")

            st.latex(f"\\mathbf{{A2}} = \\sigma(\\mathbf{{Z2}}) = {A2[0,0]:.3f}")

            # Interpretar resultado
            probabilidade = A2[0, 0]
            classe = "Classe 1" if probabilidade > 0.5 else "Classe 0"

            if probabilidade > 0.7:
                st.success(f"🎯 Predição: {classe} (confiança alta: {probabilidade:.1%})")
            elif probabilidade > 0.5:
                st.warning(f"🤔 Predição: {classe} (confiança média: {probabilidade:.1%})")
            else:
                st.error(f"❓ Predição: {classe} (confiança baixa: {probabilidade:.1%})")

    def _explicar_backward_propagation(self):
        """Explica backward propagation."""
        st.markdown("### ⬇️ Backward Propagation")

        st.markdown("""
        **O que é Backward Propagation?**

        A **retropropagação** é o algoritmo usado para treinar redes neurais,
        calculando os gradientes dos pesos em relação ao erro e atualizando-os.
        """)

        # Exemplo simplificado
        st.markdown("### 🎮 Exemplo: Gradiente Descendente Simples")

        # Função de perda simples
        st.latex("\\mathcal{L}(w) = (w - 2)^2")

        # Slider para peso
        w = st.slider("Peso w", -1.0, 5.0, 4.0, 0.1, key="w_gradient")

        # Calcular perda
        loss = (w - 2)**2

        # Gradiente
        grad = 2 * (w - 2)

        st.markdown("### 📊 Cálculos")

        st.latex(f"\\mathcal{{L}}(w) = ({w:.1f} - 2)^2 = {loss:.3f}")

        st.latex(f"\\frac{{d\\mathcal{{L}}}}{{dw}} = 2(w - 2) = {grad:.3f}")

        # Visualização
        w_range = np.linspace(-1, 5, 100)
        loss_range = (w_range - 2)**2

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Função de perda
        ax1.plot(w_range, loss_range, 'b-', linewidth=2)
        ax1.scatter([w], [loss], color='red', s=100, zorder=5)
        ax1.axvline(x=2, color='green', linestyle='--', alpha=0.7, label='Mínimo (w=2)')
        ax1.set_xlabel('Peso w')
        ax1.set_ylabel('Perda L(w)')
        ax1.set_title('Função de Perda')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Gradiente
        grad_range = 2 * (w_range - 2)
        ax2.plot(w_range, grad_range, 'r-', linewidth=2)
        ax2.scatter([w], [grad], color='red', s=100, zorder=5)
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax2.axvline(x=2, color='green', linestyle='--', alpha=0.7, label='Gradiente = 0')
        ax2.set_xlabel('Peso w')
        ax2.set_ylabel('Gradiente dL/dw')
        ax2.set_title('Gradiente')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        st.pyplot(fig)

        # Explicação do algoritmo
        st.markdown("### 🔄 Algoritmo de Gradient Descent")

        learning_rate = st.slider("Taxa de Aprendizado (η)", 0.01, 1.0, 0.1, 0.01, key="lr_gd")

        # Simulação de algumas iterações
        w_history = [w]
        loss_history = [loss]

        for i in range(10):
            grad = 2 * (w_history[-1] - 2)
            w_new = w_history[-1] - learning_rate * grad
            w_history.append(w_new)
            loss_history.append((w_new - 2)**2)

        st.markdown("**Iterações do Gradient Descent:**")
        for i, (w_val, loss_val) in enumerate(zip(w_history[:6], loss_history[:6])):
            if i == 0:
                st.write(f"**Inicial:** w = {w_val:.3f}, Loss = {loss_val:.3f}")
            else:
                st.write(f"**Passo {i}:** w = {w_val:.3f}, Loss = {loss_val:.3f}")

        # Plotar convergência
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(range(len(loss_history)), loss_history, 'b-o', linewidth=2, markersize=4)
        ax.set_xlabel('Iteração')
        ax.set_ylabel('Perda')
        ax.set_title('Convergência do Gradient Descent')
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')

        st.pyplot(fig)

    def _explicar_aplicacoes(self):
        """Explica aplicações práticas de redes neurais."""
        st.markdown("## 🎯 Aplicações Práticas")

        st.markdown("""
        **Onde as Redes Neurais são usadas?**

        As redes neurais revolucionaram diversos campos da tecnologia e ciência,
        resolvendo problemas complexos que eram difíceis para métodos tradicionais.
        """)

        # Grid de aplicações
        col1, col2 = st.columns(2)

        aplicacoes = [
            {
                "titulo": "🖼️ Visão Computacional",
                "arquitetura": "CNNs",
                "exemplos": ["Classificação de imagens", "Detecção de objetos", "Segmentação", "Reconhecimento facial"],
                "exemplo_pratico": "Redes como ResNet e YOLO conseguem identificar objetos em imagens com precisão sobre-humana."
            },
            {
                "titulo": "🎤 Processamento de Linguagem",
                "arquitetura": "Transformers/RNNs",
                "exemplos": ["Tradução automática", "Análise de sentimento", "Geração de texto", "Chatbots"],
                "exemplo_pratico": "Modelos como GPT e BERT entendem e geram linguagem natural de forma impressionante."
            },
            {
                "titulo": "🎵 Reconhecimento de Áudio",
                "arquitetura": "CNNs/RNNs",
                "exemplos": ["Reconhecimento de fala", "Identificação de música", "Análise de emoções", "Separação de fontes"],
                "exemplo_pratico": "Assistentes virtuais como Siri e Alexa usam redes neurais para entender comandos de voz."
            },
            {
                "titulo": "🏥 Saúde e Medicina",
                "arquitetura": "CNNs/MLP",
                "exemplos": ["Diagnóstico por imagem", "Descoberta de fármacos", "Predição de doenças", "Análise genômica"],
                "exemplo_pratico": "Redes neurais ajudam radiologistas a detectar câncer em exames de imagem com maior precisão."
            },
            {
                "titulo": "🚗 Veículos Autônomos",
                "arquitetura": "CNNs/RNNs",
                "exemplos": ["Detecção de obstáculos", "Planejamento de rota", "Controle de direção", "Previsão de movimento"],
                "exemplo_pratico": "Carros autônomos usam múltiplas câmeras e sensores processados por redes neurais profundas."
            },
            {
                "titulo": "📈 Finanças",
                "arquitetura": "RNNs/LSTMs",
                "exemplos": ["Previsão de preços", "Detecção de fraudes", "Trading algorítmico", "Avaliação de risco"],
                "exemplo_pratico": "Bancos usam redes neurais para detectar transações fraudulentas em tempo real."
            }
        ]

        for i, app in enumerate(aplicacoes):
            col = col1 if i % 2 == 0 else col2

            with col:
                with st.expander(f"{app['titulo']} ({app['arquitetura']})"):
                    st.markdown(f"**Arquitetura principal:** {app['arquitetura']}")

                    st.markdown("**Aplicações:**")
                    for exemplo in app['exemplos']:
                        st.markdown(f"- {exemplo}")

                    st.markdown(f"**💡 Exemplo:** {app['exemplo_pratico']}")

        # Demonstração prática
        st.markdown("### 🎮 Demonstração: Classificação de Dígitos")

        st.markdown("""
        **MNIST Dataset:** Um dos problemas clássicos de visão computacional.

        A rede neural aprende a reconhecer dígitos handwritten (0-9) a partir de imagens 28×28 pixels.
        """)

        # Simulação de uma predição
        st.markdown("### 🧠 Simulação de Predição")

        # Criar uma imagem simples de dígito (exemplo do "1")
        digit_image = np.zeros((28, 28))
        # Desenhar um "1" simples
        digit_image[5:20, 12:16] = 1  # Linha vertical
        digit_image[5:9, 8:20] = 1    # Topo do 1

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(digit_image, cmap='gray')
        ax.axis('off')
        ax.set_title('Imagem de Entrada (28×28)')
        st.pyplot(fig)

        # Simular predições da rede
        predicoes = np.array([0.01, 0.85, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])

        st.markdown("### 📊 Saída da Rede Neural (Softmax)")

        # Criar gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 4))
        digits = [str(i) for i in range(10)]
        bars = ax.bar(digits, predicoes, color=['lightblue']*10)
        bars[1].set_color('darkblue')  # Destaque para o dígito 1

        ax.set_xlabel('Dígito')
        ax.set_ylabel('Probabilidade')
        ax.set_title('Predições da Rede Neural')
        ax.set_ylim(0, 1)

        # Adicionar valores nas barras
        for bar, pred in zip(bars, predicoes):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   '.2f', ha='center', va='bottom')

        st.pyplot(fig)

        st.success("🎯 **Predição correta:** Dígito 1 com 85% de confiança!")

        st.markdown("""
        ### 🏆 Por que isso é impressionante?

        - **Antes das CNNs:** Algoritmos tradicionais conseguiam ~95% de acurácia
        - **Com CNNs modernas:** Redes como ResNet alcançam ~99.8% de acurácia
        - **Aplicações reais:** Reconhecimento de cheques, leitura de placas, OCR

        **Isso representa uma melhoria de 4.8x na taxa de erro!**
        """)

    def _mostrar_demonstracoes_pytorch(self):
        """Mostra demonstrações práticas com PyTorch."""
        st.header("🧠 Demonstrações PyTorch")

        if not PYTORCH_AVAILABLE:
            st.warning("PyTorch não está instalado. Instale com: pip install torch torchvision torchaudio")
            st.info("""
            **PyTorch** é uma biblioteca de deep learning que fornece:

            - **Tensores**: Arrays multidimensionais similares ao NumPy, mas com suporte GPU
            - **Autograd**: Sistema automático de diferenciação para backpropagation
            - **nn.Module**: Classes para construir redes neurais
            - **Otimizadores**: Algoritmos como Adam, SGD, etc.
            - **Aceleração GPU**: Computação paralela massiva
            """)
            return

        st.markdown("""
        **Bem-vindo às Demonstrações PyTorch!** 🚀

        Aqui você aprenderá na prática como usar PyTorch para criar, treinar e
        avaliar redes neurais. PyTorch combina flexibilidade com performance excepcional.
        """)

        # Inicializa utilitários PyTorch
        if not hasattr(self, 'pytorch_utils'):
            self.pytorch_utils = UtilitariosPyTorch()

        # Abas de demonstração
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Tensores Básicos",
            "🔄 Autograd",
            "🧠 Rede Neural",
            "🎨 CNN Simples",
            "⚡ GPU Acceleration"
        ])

        with tab1:
            self._demonstrar_tensores()

        with tab2:
            self._demonstrar_autograd()

        with tab3:
            self._demonstrar_rede_neural()

        with tab4:
            self._demonstrar_cnn()

        with tab5:
            self._demonstrar_gpu()

    def _demonstrar_tensores(self):
        """Demonstra operações básicas com tensores PyTorch."""
        st.subheader("📊 Tensores PyTorch")

        st.markdown("""
        **Tensores** são a unidade fundamental do PyTorch. Eles são similares aos arrays NumPy,
        mas podem ser executados na GPU e suportam autograd.
        """)

        # Demonstração interativa
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 🎮 Criação de Tensores")

            # Controles interativos
            forma_tensor = st.selectbox(
                "Forma do tensor:",
                ["1D (Vetor)", "2D (Matriz)", "3D (Cubo)"],
                key="forma_tensor"
            )

            if forma_tensor == "1D (Vetor)":
                tamanho = st.slider("Tamanho:", 1, 10, 5, key="tamanho_1d")
                tensor = torch.randn(tamanho)
                st.code(f"torch.randn({tamanho})")
            elif forma_tensor == "2D (Matriz)":
                linhas = st.slider("Linhas:", 1, 5, 3, key="linhas_2d")
                colunas = st.slider("Colunas:", 1, 5, 4, key="colunas_2d")
                tensor = torch.randn(linhas, colunas)
                st.code(f"torch.randn({linhas}, {colunas})")
            else:  # 3D
                dim1 = st.slider("Dimensão 1:", 1, 4, 2, key="dim1_3d")
                dim2 = st.slider("Dimensão 2:", 1, 4, 3, key="dim2_3d")
                dim3 = st.slider("Dimensão 3:", 1, 4, 4, key="dim3_3d")
                tensor = torch.randn(dim1, dim2, dim3)
                st.code(f"torch.randn({dim1}, {dim2}, {dim3})")

            st.markdown(f"**Forma:** {tensor.shape}")
            st.markdown(f"**Tipo:** {tensor.dtype}")
            st.markdown(f"**Dispositivo:** {tensor.device}")

        with col2:
            st.markdown("### 🔢 Operações com Tensores")

            # Cria tensores de exemplo
            a = torch.tensor([1, 2, 3])
            b = torch.tensor([4, 5, 6])

            st.markdown("**Tensores de exemplo:**")
            st.code("a = torch.tensor([1, 2, 3])\nb = torch.tensor([4, 5, 6])")

            # Operações
            operacao = st.selectbox(
                "Operação:",
                ["Soma (a + b)", "Produto elemento-a-elemento (a * b)", "Produto escalar (torch.dot)", "Concatenação"],
                key="operacao_tensor"
            )

            if operacao == "Soma (a + b)":
                resultado = a + b
                st.code("a + b")
            elif operacao == "Produto elemento-a-elemento (a * b)":
                resultado = a * b
                st.code("a * b")
            elif operacao == "Produto escalar (torch.dot)":
                resultado = torch.dot(a, b)
                st.code("torch.dot(a, b)")
            else:  # Concatenação
                resultado = torch.cat([a, b])
                st.code("torch.cat([a, b])")

            st.markdown(f"**Resultado:** {resultado}")

            # Visualização se for matriz
            if len(tensor.shape) == 2 and tensor.shape[0] <= 5 and tensor.shape[1] <= 5:
                st.markdown("### 📈 Visualização do Tensor")
                fig, ax = plt.subplots(figsize=(6, 4))
                im = ax.imshow(tensor.numpy(), cmap='viridis')
                plt.colorbar(im, ax=ax)
                ax.set_title(f'Tensor {tensor.shape}')
                st.pyplot(fig)

    def _demonstrar_autograd(self):
        """Demonstra o sistema de autograd do PyTorch."""
        st.subheader("🔄 Sistema Autograd")

        st.markdown("""
        **Autograd** é o sistema automático de diferenciação do PyTorch.
        Ele calcula automaticamente gradientes para backpropagation.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 📚 Conceito")

            st.markdown("""
            **Como funciona:**
            1. Crie tensores com `requires_grad=True`
            2. Execute operações matemáticas
            3. Chame `.backward()` para calcular gradientes
            4. Acesse gradientes via `.grad`
            """)

            st.code("""
# Exemplo básico
x = torch.tensor(2.0, requires_grad=True)
y = x**2 + 3*x + 1
y.backward()
print(x.grad)  # Imprime 2*x + 3 = 7
            """)

        with col2:
            st.markdown("### 🎮 Demonstração Interativa")

            # Controles para função
            coef_a = st.slider("Coeficiente a (ax²):", -5.0, 5.0, 1.0, 0.1, key="coef_a")
            coef_b = st.slider("Coeficiente b (bx):", -5.0, 5.0, 3.0, 0.1, key="coef_b")
            coef_c = st.slider("Coeficiente c:", -5.0, 5.0, 1.0, 0.1, key="coef_c")
            x_val = st.slider("Valor de x:", -3.0, 3.0, 2.0, 0.1, key="x_val")

            # Cálculo com PyTorch
            x = torch.tensor(x_val, requires_grad=True)
            y = coef_a * x**2 + coef_b * x + coef_c
            y.backward()

            gradiente = x.grad.item()

            st.markdown("### 📊 Cálculos")
            st.latex(f"f(x) = {coef_a}x^2 + {coef_b}x + {coef_c}")
            st.latex(f"f({x_val}) = {coef_a} \\times {x_val}^2 + {coef_b} \\times {x_val} + {coef_c} = {y.item():.3f}")
            st.latex(f"\\frac{{df}}{{dx}} = {2*coef_a}x + {coef_b} = {gradiente:.3f}")

            # Visualização
            x_range = torch.linspace(-3, 3, 100)
            y_range = coef_a * x_range**2 + coef_b * x_range + coef_c

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

            # Função
            ax1.plot(x_range.numpy(), y_range.numpy(), 'b-', linewidth=2)
            ax1.scatter([x_val], [y.item()], color='red', s=100, zorder=5)
            ax1.axvline(x=x_val, color='red', linestyle='--', alpha=0.7)
            ax1.set_xlabel('x')
            ax1.set_ylabel('f(x)')
            ax1.set_title('Função Quadrática')
            ax1.grid(True, alpha=0.3)

            # Gradiente
            grad_range = 2 * coef_a * x_range + coef_b
            ax2.plot(x_range.numpy(), grad_range.numpy(), 'r-', linewidth=2)
            ax2.scatter([x_val], [gradiente], color='red', s=100, zorder=5)
            ax2.axvline(x=x_val, color='red', linestyle='--', alpha=0.7)
            ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
            ax2.set_xlabel('x')
            ax2.set_ylabel('df/dx')
            ax2.set_title('Gradiente (Derivada)')
            ax2.grid(True, alpha=0.3)

            st.pyplot(fig)

    def _demonstrar_rede_neural(self):
        """Demonstra criação e treinamento de uma rede neural."""
        st.subheader("🧠 Rede Neural com PyTorch")

        st.markdown("""
        **Vamos criar e treinar uma rede neural simples** para resolver um problema
        de classificação não-linear (dados em formato de círculos concêntricos).
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 🏗️ Arquitetura da Rede")

            # Parâmetros da rede
            hidden_size = st.slider("Neurônios na camada oculta:", 5, 50, 20, key="hidden_size")
            learning_rate = st.slider("Taxa de aprendizado:", 0.001, 0.1, 0.01, 0.001, format="%.3f", key="lr_pytorch")
            num_epocas = st.slider("Número de épocas:", 10, 200, 50, key="epocas_pytorch")

            # Cria rede
            rede = RedeNeuralPyTorch(input_size=2, hidden_size=hidden_size, output_size=1)

            st.markdown(f"**Arquitetura:** 2 → {hidden_size} → 1")
            st.markdown("**Ativação:** ReLU na camada oculta")
            st.markdown("**Saída:** Linear (para regressão)")

        with col2:
            st.markdown("### 📊 Dados de Treino")

            # Gera dados
            X, y = self.pytorch_utils.criar_dados_exemplo(300)

            # Converte para numpy para plotar
            X_np = X.numpy()
            y_np = y.numpy().flatten()

            # Plota dados
            fig, ax = plt.subplots(figsize=(6, 6))
            scatter = ax.scatter(X_np[:, 0], X_np[:, 1], c=y_np, cmap='coolwarm', alpha=0.7, edgecolors='black')
            ax.set_xlabel('Feature 1')
            ax.set_ylabel('Feature 2')
            ax.set_title('Dados de Treino (Não-Linearmente Separáveis)')
            ax.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax, label='Classe')
            st.pyplot(fig)

        # Botão de treinamento
        if st.button("🚀 Treinar Rede Neural", key="treinar_pytorch"):
            with st.spinner("Treinando rede neural..."):
                # Treina a rede
                historico = self.pytorch_utils.treinar_rede(
                    rede, X, y, num_epocas=num_epocas, learning_rate=learning_rate
                )

                # Salva no session_state
                st.session_state.rede_treinada = rede
                st.session_state.historico_treino = historico

            st.success("✅ Treinamento concluído!")

        # Mostra resultados se disponíveis
        if 'historico_treino' in st.session_state:
            historico = st.session_state.historico_treino

            # Métricas
            perda_inicial = historico['loss'][0]
            perda_final = historico['loss'][-1]
            melhoria = ((perda_inicial - perda_final) / perda_inicial) * 100

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Perda Inicial", f"{perda_inicial:.4f}")
            with col2:
                st.metric("Perda Final", f"{perda_final:.4f}")
            with col3:
                st.metric("Melhoria", f"{melhoria:.1f}%")

            # Gráfico de convergência
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(historico['epoca'], historico['loss'], 'b-', linewidth=2, marker='o', markersize=3)
            ax.set_xlabel('Época')
            ax.set_ylabel('Perda (MSE)')
            ax.set_title('Convergência do Treinamento')
            ax.set_yscale('log')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

            # Avaliação e visualização das predições
            if 'rede_treinada' in st.session_state:
                rede = st.session_state.rede_treinada

                # Gera grid para visualização
                x1_range = np.linspace(X_np[:, 0].min() - 0.5, X_np[:, 0].max() + 0.5, 50)
                x2_range = np.linspace(X_np[:, 1].min() - 0.5, X_np[:, 1].max() + 0.5, 50)
                xx1, xx2 = np.meshgrid(x1_range, x2_range)
                grid = np.column_stack([xx1.ravel(), xx2.ravel()])
                grid_tensor = torch.FloatTensor(grid)

                # Predições
                rede.eval()
                with torch.no_grad():
                    predicoes = rede(grid_tensor).numpy().flatten()

                # Plota fronteira de decisão
                fig, ax = plt.subplots(figsize=(8, 6))
                contour = ax.contourf(xx1, xx2, predicoes.reshape(xx1.shape), alpha=0.3, cmap='coolwarm', levels=20)
                scatter = ax.scatter(X_np[:, 0], X_np[:, 1], c=y_np, cmap='coolwarm', alpha=0.8, edgecolors='black')
                plt.colorbar(contour, ax=ax, label='Predição da Rede')
                ax.set_xlabel('Feature 1')
                ax.set_ylabel('Feature 2')
                ax.set_title('Fronteira de Decisão Aprendida')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

                # Métricas de avaliação
                metricas = self.pytorch_utils.avaliar_rede(rede, X, y)
                st.markdown("### 📈 Métricas de Avaliação")
                st.metric("Acurácia de Classificação", f"{metricas['accuracy']:.1%}")
                st.metric("Perda Final (MSE)", f"{metricas['loss']:.4f}")

    def _demonstrar_cnn(self):
        """Demonstra uma rede convolucional simples."""
        st.subheader("🎨 Rede Convolucional (CNN)")

        st.markdown("""
        **Redes Convolucionais** são especializadas no processamento de imagens.
        Vamos criar uma CNN simples para classificação de dígitos MNIST.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 🏗️ Arquitetura CNN")

            st.code("""
class CNNSimples(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, 1, 1)  # 16 filtros 3x3
        self.conv2 = nn.Conv2d(16, 32, 3, 1, 1) # 32 filtros 3x3
        self.pool = nn.MaxPool2d(2, 2)           # Max pooling 2x2
        self.fc1 = nn.Linear(32 * 7 * 7, 128)   # Fully connected
        self.fc2 = nn.Linear(128, 10)           # 10 classes (0-9)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
            """)

            st.markdown("**Fluxo de dados:**")
            st.markdown("Imagem 28×28 → Conv1 → Pool1 → Conv2 → Pool2 → Flatten → FC1 → FC2 → Predições")

        with col2:
            st.markdown("### 🎯 Demonstração com MNIST")

            # Cria CNN
            cnn = self.pytorch_utils.criar_rede_convolucional_simples()

            # Mostra arquitetura
            st.markdown("**Parâmetros da rede:**")
            total_params = sum(p.numel() for p in cnn.parameters())
            trainable_params = sum(p.numel() for p in cnn.parameters() if p.requires_grad)

            st.metric("Parâmetros Totais", f"{total_params:,}")
            st.metric("Parâmetros Traináveis", f"{trainable_params:,}")

            # Simulação de uma predição
            st.markdown("### 🧠 Simulação de Predição")

            # Cria uma imagem simples de dígito (exemplo do "3")
            digit_image = np.zeros((28, 28))
            # Desenha um "3" simples
            digit_image[5:8, 8:20] = 1    # Topo
            digit_image[10:13, 16:20] = 1 # Meio direita
            digit_image[15:18, 8:20] = 1  # Fundo
            digit_image[10:18, 8:11] = 1  # Meio esquerda
            digit_image[10:18, 17:20] = 1 # Meio direita

            # Converte para tensor PyTorch
            input_tensor = torch.FloatTensor(digit_image).unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, 28, 28)

            # Forward pass
            cnn.eval()
            with torch.no_grad():
                output = cnn(input_tensor)
                probabilities = torch.softmax(output, dim=1).squeeze()

            # Mostra imagem
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.imshow(digit_image, cmap='gray')
            ax.axis('off')
            ax.set_title('Imagem de Entrada (28×28)')
            st.pyplot(fig)

            # Mostra predições
            probs_np = probabilities.numpy()
            predicted_class = np.argmax(probs_np)

            st.markdown("### 📊 Saída da CNN (Softmax)")

            # Gráfico de barras das predições
            fig, ax = plt.subplots(figsize=(10, 4))
            digits = [str(i) for i in range(10)]
            bars = ax.bar(digits, probs_np, color=['lightblue']*10)
            bars[predicted_class].set_color('darkblue')

            ax.set_xlabel('Dígito')
            ax.set_ylabel('Probabilidade')
            ax.set_title('Predições da CNN')
            ax.set_ylim(0, 1)

            # Adiciona valores nas barras
            for bar, prob in zip(bars, probs_np):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       '.2f', ha='center', va='bottom')

            st.pyplot(fig)

            st.success(f"🎯 **Classe prevista:** {predicted_class} (probabilidade: {probs_np[predicted_class]:.1%})")

    def _demonstrar_gpu(self):
        """Demonstra aceleração GPU com PyTorch."""
        st.subheader("⚡ Aceleração GPU")

        st.markdown("""
        **PyTorch** oferece aceleração massiva através de GPUs NVIDIA.
        Vamos comparar performance CPU vs GPU.
        """)

        # Informações do sistema
        gpu_info = self.pytorch_utils.demonstracao_gpu()

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 💻 Configuração do Sistema")

            st.metric("CUDA Disponível", "✅ Sim" if gpu_info['cuda_disponivel'] else "❌ Não")
            st.metric("Dispositivo Padrão", gpu_info['device'])

            if gpu_info['cuda_disponivel']:
                st.metric("GPU", gpu_info['nome_gpu'])
                st.metric("Memória Total", f"{gpu_info['memoria_total']:.1f} GB")
            else:
                st.warning("GPU não detectada. Instale drivers CUDA para aceleração GPU.")

        with col2:
            st.markdown("### 🚀 Comparação de Performance")

            if gpu_info['cuda_disponivel']:
                # Mostra métricas de performance
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Tempo CPU", f"{gpu_info['cpu_time']:.3f}s")
                with col_b:
                    st.metric("Tempo GPU", f"{gpu_info['gpu_time']:.3f}s")
                with col_c:
                    st.metric("Speedup", f"{gpu_info['speedup']:.1f}x")

                # Gráfico de comparação
                fig, ax = plt.subplots(figsize=(6, 4))
                dispositivos = ['CPU', 'GPU']
                tempos = [gpu_info['cpu_time'], gpu_info['gpu_time']]
                bars = ax.bar(dispositivos, tempos, color=['lightcoral', 'lightgreen'])
                ax.set_ylabel('Tempo (segundos)')
                ax.set_title('Comparação CPU vs GPU')
                ax.set_yscale('log')

                # Adiciona valores nas barras
                for bar, tempo in zip(bars, tempos):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                           '.3f', ha='center', va='bottom')

                st.pyplot(fig)

                st.success(f"🎯 **Aceleração alcançada:** {gpu_info['speedup']:.1f}x mais rápido na GPU!")
            else:
                st.info("Para testar aceleração GPU, você precisa de uma GPU NVIDIA com drivers CUDA instalados.")

        # Demonstração prática
        st.markdown("### 🎮 Demonstração Prática")

        tamanho_matriz = st.slider("Tamanho das matrizes (NxN):", 100, 2000, 500, 100, key="tamanho_matriz")

        if st.button("🚀 Executar Benchmark", key="benchmark_gpu"):
            with st.spinner("Executando benchmark..."):
                # Benchmark CPU
                start_time = time.time()
                a_cpu = torch.randn(tamanho_matriz, tamanho_matriz)
                b_cpu = torch.randn(tamanho_matriz, tamanho_matriz)
                c_cpu = torch.mm(a_cpu, b_cpu)
                cpu_time_bench = time.time() - start_time

                # Benchmark GPU (se disponível)
                if torch.cuda.is_available():
                    start_time = time.time()
                    a_gpu = torch.randn(tamanho_matriz, tamanho_matriz).cuda()
                    b_gpu = torch.randn(tamanho_matriz, tamanho_matriz).cuda()
                    c_gpu = torch.mm(a_gpu, b_gpu)
                    gpu_time_bench = time.time() - start_time
                    speedup_bench = cpu_time_bench / gpu_time_bench
                else:
                    gpu_time_bench = None
                    speedup_bench = None

            # Resultados
            st.markdown("### 📊 Resultados do Benchmark")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Operação", f"Matriz {tamanho_matriz}×{tamanho_matriz}")
            with col2:
                st.metric("Tempo CPU", f"{cpu_time_bench:.3f}s")
            with col3:
                if gpu_time_bench is not None:
                    st.metric("Tempo GPU", f"{gpu_time_bench:.3f}s")
                else:
                    st.metric("GPU", "Não disponível")

            if speedup_bench is not None:
                st.success(f"🚀 **Speedup GPU:** {speedup_bench:.1f}x mais rápido!")
                st.info("💡 Para problemas maiores, o speedup pode ser ainda maior!")

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
    """Cria e retorna uma instância do módulo de redes neurais."""
    return ModuloRedesNeurais()
def criar_modulo_redes_neurais():
    """Cria instância do módulo de redes neurais."""
    return ModuloRedesNeurais()


# Para execução independente
if __name__ == "__main__":
    modulo = ModuloRedesNeurais()
    modulo.mostrar_interface_principal()