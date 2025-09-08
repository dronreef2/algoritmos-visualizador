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
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import time

# Adicionar diretórios dos módulos ao path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "modulo_1_fundamentos"))
sys.path.append(str(project_root / "modulo_2_estruturas_dados"))
sys.path.append(str(project_root / "modulo_3_programacao_dinamica"))
sys.path.append(str(project_root / "modulo_4_entrevistas"))

# Importar sistema de aprendizado contextualizado
try:
    from aprendizado_contextual_ui import render_aprendizado_contextual
    APRENDIZADO_CONTEXTUAL_DISPONIVEL = True
except ImportError:
    APRENDIZADO_CONTEXTUAL_DISPONIVEL = False

# Importar sistema de exercícios práticos
try:
    from exercicios_praticos_ui import render_exercicios_praticos
    EXERCICIOS_PRATICOS_DISPONIVEL = True
except ImportError:
    EXERCICIOS_PRATICOS_DISPONIVEL = False

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

def render_mcp_search():
    """Renderiza a interface de busca MCP com Tavily."""
    st.markdown("## 🔍 Busca Inteligente com MCP (Tavily)")
    
    st.markdown("""
    ### 🤖 Busca Contextual com IA
    
    Use o poder da busca inteligente para encontrar informações relevantes sobre algoritmos,
    estruturas de dados e problemas de programação.
    """)
    
    # Verificar se o MCP está configurado
    try:
        from mcp_tavily_integration import TavilySearchClient
        
        # Inicializar cliente MCP
        if 'mcp_client' not in st.session_state:
            st.session_state.mcp_client = TavilySearchClient()
        
        client = st.session_state.mcp_client
        
        # Status da configuração
        if client.is_configured():
            st.success("✅ MCP Server Tavily configurado e pronto!")
        else:
            st.warning("⚠️ MCP Server precisa ser configurado. Verifique o arquivo .env")
            st.info("Para configurar: Edite `mcp-server-tavily/.env` e adicione sua chave da API Tavily")
            return
        
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
                help="Basic: busca rápida, Advanced: busca detalhada com mais contexto"
            )
            
            include_answer = st.checkbox(
                "Incluir resposta da IA",
                value=False,
                help="Gera uma resposta contextualizada usando IA baseada nos resultados"
            )
            
            max_results = st.slider(
                "Máximo de resultados:",
                min_value=1,
                max_value=10,
                value=5,
                help="Número máximo de resultados a retornar"
            )
        
        if st.button("🔍 Buscar", type="primary", use_container_width=True):
            if query.strip():
                with st.spinner("🔄 Buscando informações com IA..."):
                    try:
                        # Realizar busca
                        result = client.search(
                            query, 
                            search_depth=search_type,
                            include_answer=include_answer,
                            max_results=max_results
                        )
                        
                        if result and "results" in result:
                            st.success(f"✅ Encontrados {len(result['results'])} resultados!")
                            
                            # Exibir resposta da IA se disponível
                            if result.get("answer") and include_answer:
                                st.markdown("### 🤖 Resposta da IA")
                                st.info(result["answer"])
                                st.markdown("---")
                            
                            # Exibir resultados
                            for i, item in enumerate(result["results"], 1):
                                with st.expander(f"📄 Resultado {i}: {item.get('title', 'Sem título')[:50]}..."):
                                    st.markdown(f"**URL:** {item.get('url', 'N/A')}")
                                    st.markdown(f"**Conteúdo:** {item.get('snippet', 'N/A')}")
                                    
                                    if item.get('content'):
                                        st.markdown("**Conteúdo completo:**")
                                        st.text_area(
                                            "Conteúdo",
                                            item['content'],
                                            height=150,
                                            key=f"content_{i}"
                                        )
                        else:
                            st.warning("Nenhum resultado encontrado. Tente reformular sua consulta.")
                            
                    except Exception as e:
                        st.error(f"Erro na busca: {str(e)}")
                        st.info("Verifique se o servidor MCP está rodando e configurado corretamente.")
            else:
                st.warning("Por favor, digite uma consulta para buscar.")
        
        # Exemplos de consultas
        with st.expander("💡 Exemplos de Consultas"):
            st.markdown("""
            **Algoritmos:**
            - "como funciona o algoritmo de busca binária?"
            - "explicação do algoritmo de Dijkstra"
            - "diferença entre BFS e DFS"
            
            **Estruturas de Dados:**
            - "como implementar uma árvore binária de busca?"
            - "vantagens da tabela hash"
            - "quando usar lista ligada vs array?"
            
            **Programação Dinâmica:**
            - "problema da mochila 0/1 explicado"
            - "longest common subsequence algorithm"
            - "metodologia dos 3 passos em DP"
            """)
            
    except ImportError as e:
        st.error(f"Erro ao importar MCP: {e}")
        st.info("Certifique-se de que o módulo `mcp_tavily_integration.py` está disponível.")

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
            "🎯 Aprendizado Contextualizado",
            "🎯 Exercícios Práticos",
            "📚 Módulo 1: Fundamentos",
            "🏗️ Módulo 2: Estruturas de Dados",
            "🎯 Módulo 3: Programação Dinâmica",
            "💼 Módulo 4: Entrevistas",
            "🔍 Busca MCP (Tavily)"
        ]
    )
    
    # Roteamento baseado na seleção
    if module == "🏠 Home":
        render_home_page()
    elif module == "🎯 Aprendizado Contextualizado":
        if APRENDIZADO_CONTEXTUAL_DISPONIVEL:
            render_aprendizado_contextual()
        else:
            st.error("Sistema de aprendizado contextualizado não disponível.")
    elif module == "🎯 Exercícios Práticos":
        if EXERCICIOS_PRATICOS_DISPONIVEL:
            render_exercicios_praticos()
        else:
            st.error("Sistema de exercícios práticos não disponível.")
    elif module == "📚 Módulo 1: Fundamentos":
        render_module_1()
    elif module == "🏗️ Módulo 2: Estruturas de Dados":
        render_module_2()
    elif module == "🎯 Módulo 3: Programação Dinâmica":
        render_module_3()
    elif module == "💼 Módulo 4: Entrevistas":
        render_module_4()
    elif module == "🔍 Busca MCP (Tavily)":
        render_mcp_search()

def render_home_page():
    """Renderiza a página inicial."""
    st.markdown("""
    ## 🎉 Bem-vindo ao Algoritmos Visualizador!

    ### Uma experiência completa de aprendizado contextualizado

    Explore algoritmos e estruturas de dados através de **jornadas temáticas**,
    entenda o **contexto histórico**, veja **aplicações reais** e acompanhe seu
    **progresso personalizado** com visualizações interativas.
    """)

    # Destaque especial para exercícios práticos
    if EXERCICIOS_PRATICOS_DISPONIVEL:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 5px solid #ff6b6b;
        ">
        <h3 style="color: white; margin-top: 0;">🎯 🆕 Exercícios Práticos Interativos</h3>
        <p style="margin-bottom: 0.5rem;">
            <strong>Agora disponível!</strong> Pratique com exercícios reais, receba feedback imediato
            e acompanhe seu progresso com estatísticas detalhadas.
        </p>
        <ul style="margin-bottom: 0;">
            <li>✅ Múltipla escolha, verdadeiro/falso, ordenação</li>
            <li>✅ Análise de complexidade, debugging de código</li>
            <li>✅ Sistema de conquistas e gamificação</li>
            <li>✅ Dashboard de performance e progresso</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Destaque para aprendizado contextualizado
    if APRENDIZADO_CONTEXTUAL_DISPONIVEL:
        st.info("🎯 **Novo:** Sistema de Aprendizado Contextualizado disponível! Explore jornadas temáticas e conexões entre conceitos.")

    # Métricas gerais
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("📚 Módulos", "4", "Completos")

    with col2:
        st.metric("🎯 Algoritmos", "50+", "Implementados")

    with col3:
        st.metric("🏗️ Estruturas", "15+", "Visualizadas")

    with col4:
        st.metric("💼 Problemas", "25+", "de Entrevista")

    with col5:
        st.metric("🎯 Exercícios", "30+", "Interativos")
    
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
    
    # Card especial para exercícios práticos
    st.markdown("### 🎯 Sistema de Exercícios Práticos")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
    <h3 style="color: #d32f2f; margin-top: 0;">🎯 Exercícios Práticos Interativos</h3>
    <p style="margin-bottom: 1rem; color: #333;">
        <strong>Pratique de verdade!</strong> Resolva exercícios reais com validação automática,
        feedback imediato e acompanhamento de progresso.
    </p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
            <h4 style="color: #d32f2f; margin-bottom: 0.5rem;">📝 Tipos de Exercício</h4>
            <ul style="margin: 0; color: #555;">
                <li>Múltipla escolha</li>
                <li>Verdadeiro/Falso</li>
                <li>Ordenação de passos</li>
                <li>Análise de complexidade</li>
            </ul>
        </div>
        <div>
            <h4 style="color: #d32f2f; margin-bottom: 0.5rem;">🏆 Recursos</h4>
            <ul style="margin: 0; color: #555;">
                <li>Feedback instantâneo</li>
                <li>Dashboard de progresso</li>
                <li>Sistema de conquistas</li>
                <li>Estatísticas detalhadas</li>
            </ul>
        </div>
    </div>
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
        from modulo_1_fundamentos.aplicacoes_reais import (
            SistemaBuscaLogs, DetectorFraudesFinanceiras, RedeSocialBFS
        )
        from modulo_1_fundamentos.busca_binaria import BuscaBinaria
        from modulo_1_fundamentos.dois_ponteiros import DoisPonteiros
        from modulo_1_fundamentos.janela_deslizante import JanelaDeslizante
        
        # Seleção de aplicação
        app = st.selectbox(
            "Escolha a Aplicação",
            [
                "🔍 Sistema de Busca em Logs",
                "🚨 Detector de Fraudes", 
                "� Rede Social (BFS)",
                "🎯 Busca Binária Interativa",
                "↔️ Dois Ponteiros",
                "🪟 Janela Deslizante"
            ]
        )
        
        if app == "� Sistema de Busca em Logs":
            render_log_search_system()
        elif app == "🚨 Detector de Fraudes":
            render_fraud_detector()
        elif app == "👥 Rede Social (BFS)":
            render_social_network()
        elif app == "🎯 Busca Binária Interativa":
            render_binary_search()
        elif app == "↔️ Dois Ponteiros":
            render_two_pointers()
        elif app == "🪟 Janela Deslizante":
            render_sliding_window()
            
    except ImportError as e:
        st.error(f"Erro ao importar módulo 1: {e}")
        st.info("Certifique-se de que todos os arquivos do módulo 1 estão presentes.")

def render_log_search_system():
    """Renderiza o sistema de busca em logs."""
    st.markdown("### 🔍 Sistema de Busca em Logs")
    
    try:
        from modulo_1_fundamentos.aplicacoes_reais import SistemaBuscaLogs
        
        # Inicializar sistema
        if 'log_system' not in st.session_state:
            st.session_state.log_system = SistemaBuscaLogs()
            # Adicionar alguns logs de exemplo
            base_time = time.time()
            logs_exemplo = [
                (base_time - 3600, "INFO: Sistema iniciado"),
                (base_time - 3000, "WARNING: Uso alto de CPU"),
                (base_time - 2400, "ERROR: Conexão falhou"),
                (base_time - 1800, "INFO: Backup concluído"),
                (base_time - 1200, "DEBUG: Cache limpo"),
                (base_time - 600, "INFO: Usuário logado"),
                (base_time, "INFO: Sistema funcionando")
            ]
            for timestamp, msg in logs_exemplo:
                st.session_state.log_system.adicionar_log(timestamp, msg)
        
        sistema = st.session_state.log_system
        
        # Controles
        st.markdown("#### 🎮 Controles")
        col1, col2 = st.columns(2)
        
        with col1:
            novo_log = st.text_input("Nova Mensagem de Log")
            if st.button("Adicionar Log"):
                sistema.adicionar_log(time.time(), novo_log)
                st.success("Log adicionado!")
        
        with col2:
            horas_atras = st.slider("Buscar logs das últimas X horas", 1, 24, 6)
            
        # Buscar logs
        fim = time.time()
        inicio = fim - (horas_atras * 3600)
        logs_encontrados = sistema.buscar_logs_periodo(inicio, fim)
        
        # Visualização
        st.markdown("#### 📊 Logs Encontrados")
        
        if logs_encontrados:
            for timestamp, mensagem in logs_encontrados:
                dt = datetime.fromtimestamp(timestamp)
                st.markdown(f"""
                <div class="algorithm-step">
                    <strong>{dt.strftime('%Y-%m-%d %H:%M:%S')}</strong><br>
                    {mensagem}
                </div>
                """, unsafe_allow_html=True)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Logs", len(sistema.logs))
        with col2:
            st.metric("Logs Encontrados", len(logs_encontrados))
        with col3:
            st.markdown('<span class="complexity-badge">O(log n)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no sistema de logs: {e}")

def render_fraud_detector():
    """Renderiza o detector de fraudes."""
    st.markdown("### 🚨 Detector de Fraudes")
    
    try:
        from modulo_1_fundamentos.aplicacoes_reais import DetectorFraudesFinanceiras
        
        # Inicializar detector
        if 'fraud_detector' not in st.session_state:
            st.session_state.fraud_detector = DetectorFraudesFinanceiras()
        
        detector = st.session_state.fraud_detector
        
        # Controles
        st.markdown("#### 🎮 Controles")
        col1, col2 = st.columns(2)
        
        with col1:
            valor = st.number_input("Valor da Transação", min_value=0.0, value=1000.0)
            localizacao = st.selectbox("Localização", ["Brasil", "EUA", "China", "Rússia"])
            
        with col2:
            horario = st.slider("Hora da Transação", 0, 23, 14)
            usuario_id = st.number_input("ID do Usuário", min_value=1, value=123)
        
        # Adicionar transação
        if st.button("Analisar Transação"):
            eh_fraude = detector.analisar_transacao(valor, localizacao, horario, usuario_id)
            
            if eh_fraude:
                st.error("🚨 FRAUDE DETECTADA!")
                st.markdown("""
                <div class="error-badge">
                    Transação suspeita identificada pelos algoritmos de detecção
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ Transação Normal")
                st.markdown("""
                <div class="complexity-badge">
                    Transação aprovada pelos sistemas de segurança
                </div>
                """, unsafe_allow_html=True)
        
        # Estatísticas
        st.markdown("#### 📊 Estatísticas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Transações Analisadas", len(detector.historico_transacoes))
        with col2:
            fraudes = sum(1 for t in detector.historico_transacoes if t.get('fraude', False))
            st.metric("Fraudes Detectadas", fraudes)
        with col3:
            st.markdown('<span class="complexity-badge">O(n)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no detector de fraudes: {e}")

def render_social_network():
    """Renderiza a rede social com BFS."""
    st.markdown("### 👥 Rede Social (BFS)")
    
    try:
        from modulo_1_fundamentos.aplicacoes_reais import RedeSocialBFS
        
        # Inicializar rede
        if 'social_network' not in st.session_state:
            st.session_state.social_network = RedeSocialBFS()
            # Adicionar usuários de exemplo
            usuarios = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
            for usuario in usuarios:
                st.session_state.social_network.adicionar_usuario(usuario)
            
            # Adicionar conexões
            conexoes = [
                ("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "Diana"),
                ("Charlie", "Eve"), ("Diana", "Frank"), ("Eve", "Frank")
            ]
            for u1, u2 in conexoes:
                st.session_state.social_network.adicionar_conexao(u1, u2)
        
        rede = st.session_state.social_network
        
        # Controles
        st.markdown("#### 🎮 Controles")
        col1, col2 = st.columns(2)
        
        with col1:
            usuarios = list(rede.grafo.keys())
            usuario_origem = st.selectbox("Usuário de Origem", usuarios)
            usuario_destino = st.selectbox("Usuário de Destino", usuarios)
        
        with col2:
            novo_usuario = st.text_input("Novo Usuário")
            if st.button("Adicionar Usuário"):
                rede.adicionar_usuario(novo_usuario)
                st.success(f"Usuário {novo_usuario} adicionado!")
        
        # Buscar caminho
        if st.button("Encontrar Caminho"):
            caminho = rede.encontrar_caminho(usuario_origem, usuario_destino)
            
            if caminho:
                st.success(f"Caminho encontrado: {' → '.join(caminho)}")
                st.markdown(f"""
                <div class="algorithm-step">
                    <strong>Distância:</strong> {len(caminho) - 1} conexões<br>
                    <strong>Caminho:</strong> {' → '.join(caminho)}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Nenhum caminho encontrado!")
        
        # Visualização da rede
        st.markdown("#### 🌐 Visualização da Rede")
        
        # Criar grafo visual
        try:
            import networkx as nx
            
            G = nx.Graph()
            for usuario in rede.grafo.keys():
                G.add_node(usuario)
            
            for usuario, conexoes in rede.grafo.items():
                for conexao in conexoes:
                    G.add_edge(usuario, conexao)
            
            # Posicionamento dos nós
            pos = nx.spring_layout(G)
            
            # Plotar com matplotlib
            fig, ax = plt.subplots(figsize=(10, 8))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                   node_size=1500, font_size=10, font_weight='bold', ax=ax)
            ax.set_title("Rede Social - Grafo de Conexões")
            st.pyplot(fig)
            
        except ImportError:
            st.info("NetworkX não disponível. Mostrando conexões em lista:")
            for usuario, conexoes in rede.grafo.items():
                st.write(f"**{usuario}**: {', '.join(conexoes)}")
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Usuários", len(rede.grafo))
        with col2:
            total_conexoes = sum(len(conexoes) for conexoes in rede.grafo.values()) // 2
            st.metric("Conexões", total_conexoes)
        with col3:
            st.markdown('<span class="complexity-badge">O(V + E)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro na rede social: {e}")

def render_binary_search():
    """Renderiza a visualização de busca binária interativa."""
    st.markdown("### 🎯 Busca Binária Interativa")
    
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
        fig, ax = plt.subplots(figsize=(12, 6))
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
    st.markdown("### ↔️ Dois Ponteiros")
    
    # Seleção de problema
    problema = st.selectbox(
        "Escolha o Problema",
        [
            "🎯 Two Sum (Array Ordenado)",
            "🔄 Verificar Palíndromo",
            "🎨 Container with Most Water"
        ]
    )
    
    if problema == "🎯 Two Sum (Array Ordenado)":
        render_two_sum()
    elif problema == "🔄 Verificar Palíndromo":
        render_palindrome_check()
    elif problema == "🎨 Container with Most Water":
        render_container_water()

def render_two_sum():
    """Renderiza Two Sum com dois ponteiros."""
    st.markdown("#### 🎯 Two Sum - Array Ordenado")
    
    # Controles
    col1, col2 = st.columns(2)
    
    with col1:
        array_size = st.slider("Tamanho do Array", 5, 20, 10)
        target_sum = st.number_input("Soma Alvo", value=15)
    
    with col2:
        arr = sorted(np.random.randint(1, 20, array_size))
        st.write("Array:", arr)
    
    # Algoritmo Two Sum
    def two_sum_steps(arr, target):
        steps = []
        left, right = 0, len(arr) - 1
        
        while left < right:
            current_sum = arr[left] + arr[right]
            steps.append({
                'left': left,
                'right': right,
                'left_val': arr[left],
                'right_val': arr[right],
                'sum': current_sum,
                'found': current_sum == target
            })
            
            if current_sum == target:
                break
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return steps
    
    steps = two_sum_steps(arr, target_sum)
    
    if steps:
        step = st.slider("Passo", 0, len(steps) - 1, 0)
        current_step = steps[step]
        
        # Visualização
        colors = ['lightblue'] * len(arr)
        colors[current_step['left']] = 'red'
        colors[current_step['right']] = 'red'
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(arr)), arr, color=colors)
        ax.set_title(f"Two Sum - Passo {step + 1}")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        
        # Anotações
        ax.axvline(current_step['left'], color='red', linestyle='--', alpha=0.7, label='Left')
        ax.axvline(current_step['right'], color='red', linestyle='--', alpha=0.7, label='Right')
        
        ax.legend()
        st.pyplot(fig)
        
        # Informações
        st.markdown(f"""
        <div class="algorithm-step">
            <strong>Passo {step + 1}:</strong><br>
            Left: {current_step['left']} (valor: {current_step['left_val']})<br>
            Right: {current_step['right']} (valor: {current_step['right_val']})<br>
            Soma: {current_step['sum']} (alvo: {target_sum})<br>
            {"✅ Encontrado!" if current_step['found'] else "⏭️ Continuando..."}
        </div>
        """, unsafe_allow_html=True)

def render_palindrome_check():
    """Renderiza verificação de palíndromo."""
    st.markdown("#### 🔄 Verificar Palíndromo")
    
    # Controles
    texto = st.text_input("Digite um texto", value="A man a plan a canal Panama")
    
    # Limpar texto
    texto_limpo = ''.join(c.lower() for c in texto if c.isalnum())
    
    # Algoritmo de verificação
    def palindrome_steps(s):
        steps = []
        left, right = 0, len(s) - 1
        
        while left < right:
            steps.append({
                'left': left,
                'right': right,
                'left_char': s[left],
                'right_char': s[right],
                'match': s[left] == s[right]
            })
            
            if s[left] != s[right]:
                break
            
            left += 1
            right -= 1
        
        return steps
    
    if texto_limpo:
        steps = palindrome_steps(texto_limpo)
        
        # Mostrar texto limpo
        st.write(f"Texto processado: **{texto_limpo}**")
        
        if steps:
            step = st.slider("Passo", 0, len(steps) - 1, 0)
            current_step = steps[step]
            
            # Visualização
            chars = list(texto_limpo)
            colors = ['lightblue'] * len(chars)
            colors[current_step['left']] = 'red'
            colors[current_step['right']] = 'red'
            
            # Mostrar caracteres
            col_chars = st.columns(len(chars))
            for i, (char, color) in enumerate(zip(chars, colors)):
                with col_chars[i]:
                    if color == 'red':
                        st.markdown(f"**:red[{char}]**")
                    else:
                        st.markdown(f"{char}")
            
            # Informações
            st.markdown(f"""
            <div class="algorithm-step">
                <strong>Passo {step + 1}:</strong><br>
                Left: {current_step['left']} ('{current_step['left_char']}')<br>
                Right: {current_step['right']} ('{current_step['right_char']}')<br>
                {"✅ Caracteres coincidem!" if current_step['match'] else "❌ Não é palíndromo"}
            </div>
            """, unsafe_allow_html=True)

def render_container_water():
    """Renderiza Container with Most Water."""
    st.markdown("#### 🎨 Container with Most Water")
    
    # Controles
    array_size = st.slider("Número de Linhas", 5, 15, 8)
    heights = np.random.randint(1, 20, array_size)
    
    # Mostrar alturas
    st.write("Alturas:", heights.tolist())
    
    # Algoritmo
    def container_steps(heights):
        steps = []
        left, right = 0, len(heights) - 1
        max_area = 0
        
        while left < right:
            width = right - left
            area = min(heights[left], heights[right]) * width
            max_area = max(max_area, area)
            
            steps.append({
                'left': left,
                'right': right,
                'left_height': heights[left],
                'right_height': heights[right],
                'width': width,
                'area': area,
                'max_area': max_area
            })
            
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1
        
        return steps
    
    steps = container_steps(heights)
    
    if steps:
        step = st.slider("Passo", 0, len(steps) - 1, 0)
        current_step = steps[step]
        
        # Visualização
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Desenhar barras
        colors = ['lightblue'] * len(heights)
        colors[current_step['left']] = 'red'
        colors[current_step['right']] = 'red'
        
        bars = ax.bar(range(len(heights)), heights, color=colors)
        
        # Desenhar container
        left_idx = current_step['left']
        right_idx = current_step['right']
        container_height = min(heights[left_idx], heights[right_idx])
        
        # Área do container
        ax.fill_between([left_idx, right_idx], 0, container_height, 
                       alpha=0.3, color='blue', label='Container')
        
        ax.set_title(f"Container with Most Water - Passo {step + 1}")
        ax.set_xlabel("Posição")
        ax.set_ylabel("Altura")
        ax.legend()
        
        st.pyplot(fig)
        
        # Informações
        st.markdown(f"""
        <div class="algorithm-step">
            <strong>Passo {step + 1}:</strong><br>
            Left: {current_step['left']} (altura: {current_step['left_height']})<br>
            Right: {current_step['right']} (altura: {current_step['right_height']})<br>
            Largura: {current_step['width']}<br>
            Área atual: {current_step['area']}<br>
            Maior área: {current_step['max_area']}
        </div>
        """, unsafe_allow_html=True)

def render_sliding_window():
    """Renderiza a visualização de janela deslizante."""
    st.markdown("### 🪟 Janela Deslizante")
    
    # Seleção de problema
    problema = st.selectbox(
        "Escolha o Problema",
        [
            "📊 Soma Máxima de Subarray (Tamanho K)",
            "🔍 Substring mais longa sem repetição",
            "🎯 Mínimo em Janela Deslizante"
        ]
    )
    
    if problema == "📊 Soma Máxima de Subarray (Tamanho K)":
        render_max_sum_subarray()
    elif problema == "🔍 Substring mais longa sem repetição":
        render_longest_substring()
    elif problema == "🎯 Mínimo em Janela Deslizante":
        render_sliding_window_minimum()

def render_max_sum_subarray():
    """Renderiza soma máxima de subarray com janela deslizante."""
    st.markdown("#### 📊 Soma Máxima de Subarray (Tamanho K)")
    
    # Controles
    col1, col2 = st.columns(2)
    
    with col1:
        array_size = st.slider("Tamanho do Array", 5, 20, 10)
        k = st.slider("Tamanho da Janela (K)", 2, min(array_size, 5), 3)
    
    with col2:
        arr = np.random.randint(-10, 20, array_size)
        st.write("Array:", arr.tolist())
    
    # Algoritmo
    def sliding_window_max_sum(arr, k):
        if len(arr) < k:
            return []
        
        steps = []
        window_sum = sum(arr[:k])
        max_sum = window_sum
        
        steps.append({
            'start': 0,
            'end': k-1,
            'window': arr[:k].tolist(),
            'sum': window_sum,
            'max_sum': max_sum
        })
        
        for i in range(1, len(arr) - k + 1):
            window_sum = window_sum - arr[i-1] + arr[i+k-1]
            max_sum = max(max_sum, window_sum)
            
            steps.append({
                'start': i,
                'end': i+k-1,
                'window': arr[i:i+k].tolist(),
                'sum': window_sum,
                'max_sum': max_sum
            })
        
        return steps
    
    steps = sliding_window_max_sum(arr, k)
    
    if steps:
        step = st.slider("Passo", 0, len(steps) - 1, 0)
        current_step = steps[step]
        
        # Visualização
        colors = ['lightblue'] * len(arr)
        for i in range(current_step['start'], current_step['end'] + 1):
            colors[i] = 'red'
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(arr)), arr, color=colors)
        
        # Destacar janela
        ax.axvspan(current_step['start'] - 0.5, current_step['end'] + 0.5, 
                  alpha=0.3, color='yellow', label='Janela')
        
        ax.set_title(f"Janela Deslizante - Passo {step + 1}")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        ax.legend()
        
        st.pyplot(fig)
        
        # Informações
        st.markdown(f"""
        <div class="algorithm-step">
            <strong>Passo {step + 1}:</strong><br>
            Janela: [{current_step['start']} - {current_step['end']}]<br>
            Valores: {current_step['window']}<br>
            Soma atual: {current_step['sum']}<br>
            Soma máxima: {current_step['max_sum']}
        </div>
        """, unsafe_allow_html=True)

def render_longest_substring():
    """Renderiza substring mais longa sem repetição."""
    st.markdown("#### 🔍 Substring mais longa sem repetição")
    
    # Controles
    texto = st.text_input("Digite um texto", value="abcabcbb")
    
    # Algoritmo
    def longest_substring_steps(s):
        steps = []
        left = 0
        char_set = set()
        max_len = 0
        
        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            
            char_set.add(s[right])
            max_len = max(max_len, right - left + 1)
            
            steps.append({
                'left': left,
                'right': right,
                'substring': s[left:right+1],
                'length': right - left + 1,
                'max_length': max_len,
                'char_set': sorted(list(char_set))
            })
        
        return steps
    
    if texto:
        steps = longest_substring_steps(texto)
        
        if steps:
            step = st.slider("Passo", 0, len(steps) - 1, 0)
            current_step = steps[step]
            
            # Visualização
            chars = list(texto)
            colors = ['lightblue'] * len(chars)
            
            for i in range(current_step['left'], current_step['right'] + 1):
                colors[i] = 'red'
            
            # Mostrar caracteres
            col_chars = st.columns(len(chars))
            for i, (char, color) in enumerate(zip(chars, colors)):
                with col_chars[i]:
                    if color == 'red':
                        st.markdown(f"**:red[{char}]**")
                    else:
                        st.markdown(f"{char}")
            
            # Informações
            st.markdown(f"""
            <div class="algorithm-step">
                <strong>Passo {step + 1}:</strong><br>
                Janela: [{current_step['left']} - {current_step['right']}]<br>
                Substring: "{current_step['substring']}"<br>
                Comprimento atual: {current_step['length']}<br>
                Comprimento máximo: {current_step['max_length']}<br>
                Caracteres únicos: {current_step['char_set']}
            </div>
            """, unsafe_allow_html=True)

def render_sliding_window_minimum():
    """Renderiza mínimo em janela deslizante."""
    st.markdown("#### 🎯 Mínimo em Janela Deslizante")
    st.info("Implementação em desenvolvimento...")

def render_module_2():
    """Renderiza o módulo 2 - Estruturas de Dados."""
    st.markdown("## 🏗️ Módulo 2: Estruturas de Dados")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import (
            AdvancedHeap, Trie, UnionFind, SegmentTree, LRUCache, Graph
        )
        
        # Seleção de estrutura
        estrutura = st.selectbox(
            "Escolha a Estrutura de Dados",
            [
                "🔺 Heap (Min/Max)",
                "🌳 Trie (Árvore de Prefixos)",
                "🤝 Union-Find",
                "📊 Segment Tree",
                "💾 LRU Cache",
                "🌐 Graph (Grafo)"
            ]
        )
        
        if estrutura == "🔺 Heap (Min/Max)":
            render_heap_structure()
        elif estrutura == "🌳 Trie (Árvore de Prefixos)":
            render_trie_structure()
        elif estrutura == "🤝 Union-Find":
            render_union_find_structure()
        elif estrutura == "📊 Segment Tree":
            render_segment_tree_structure()
        elif estrutura == "💾 LRU Cache":
            render_lru_cache_structure()
        elif estrutura == "🌐 Graph (Grafo)":
            render_graph_structure()
            
    except ImportError as e:
        st.error(f"Erro ao importar módulo 2: {e}")
        st.info("Certifique-se de que todos os arquivos do módulo 2 estão presentes.")

def render_heap_structure():
    """Renderiza a estrutura Heap."""
    st.markdown("### 🔺 Heap (Min/Max)")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import AdvancedHeap
        
        # Inicializar heap
        if 'heap' not in st.session_state:
            st.session_state.heap = AdvancedHeap()
        
        heap = st.session_state.heap
        
        # Controles
        col1, col2, col3 = st.columns(3)
        
        with col1:
            valor = st.number_input("Valor", value=10)
            if st.button("Inserir"):
                heap.insert(valor)
                st.success(f"Valor {valor} inserido!")
        
        with col2:
            if st.button("Extrair Mínimo"):
                if heap.heap:
                    min_val = heap.extract_min()
                    st.success(f"Mínimo extraído: {min_val}")
                else:
                    st.error("Heap vazio!")
        
        with col3:
            if st.button("Limpar Heap"):
                st.session_state.heap = AdvancedHeap()
                st.success("Heap limpo!")
        
        # Visualização
        if heap.heap:
            st.markdown("#### 📊 Visualização do Heap")
            
            # Mostrar estrutura
            st.write("**Estrutura do Heap:**", heap.heap)
            
            # Gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(range(len(heap.heap)), heap.heap, color='lightblue')
            ax.set_title("Heap - Estrutura Atual")
            ax.set_xlabel("Índice")
            ax.set_ylabel("Valor")
            
            # Destacar mínimo
            if heap.heap:
                bars[0].set_color('red')
                ax.annotate(f'MIN: {heap.heap[0]}', xy=(0, heap.heap[0]), 
                           xytext=(0, heap.heap[0] + 2), ha='center',
                           arrowprops=dict(arrowstyle='->', color='red'))
            
            st.pyplot(fig)
            
            # Operações
            st.markdown("#### 🔍 Operações")
            operacoes = heap.get_operations()
            
            for i, op in enumerate(operacoes[-10:]):  # Últimas 10 operações
                st.markdown(f"""
                <div class="algorithm-step">
                    <strong>Operação {i+1}:</strong> {op['operation']} 
                    {f"(valor: {op['value']})" if 'value' in op else ""}
                </div>
                """, unsafe_allow_html=True)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tamanho", len(heap.heap))
        with col2:
            st.metric("Mínimo", heap.heap[0] if heap.heap else "N/A")
        with col3:
            st.markdown('<span class="complexity-badge">O(log n)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no Heap: {e}")

def render_trie_structure():
    """Renderiza a estrutura Trie."""
    st.markdown("### 🌳 Trie (Árvore de Prefixos)")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import Trie
        
        # Inicializar trie
        if 'trie' not in st.session_state:
            st.session_state.trie = Trie()
            # Adicionar palavras de exemplo
            palavras_exemplo = ["apple", "app", "apricot", "banana", "band", "bandana"]
            for palavra in palavras_exemplo:
                st.session_state.trie.insert(palavra)
        
        trie = st.session_state.trie
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            nova_palavra = st.text_input("Nova Palavra")
            if st.button("Inserir Palavra"):
                trie.insert(nova_palavra)
                st.success(f"Palavra '{nova_palavra}' inserida!")
        
        with col2:
            busca_palavra = st.text_input("Buscar Palavra")
            if st.button("Buscar"):
                encontrada = trie.search(busca_palavra)
                if encontrada:
                    st.success(f"✅ Palavra '{busca_palavra}' encontrada!")
                else:
                    st.error(f"❌ Palavra '{busca_palavra}' não encontrada!")
        
        # Busca por prefixo
        st.markdown("#### 🔍 Busca por Prefixo")
        prefixo = st.text_input("Digite um prefixo")
        
        if prefixo:
            palavras_prefixo = trie.get_words_with_prefix(prefixo)
            if palavras_prefixo:
                st.success(f"Palavras com prefixo '{prefixo}':")
                for palavra in palavras_prefixo:
                    st.write(f"- {palavra}")
            else:
                st.info(f"Nenhuma palavra encontrada com prefixo '{prefixo}'")
        
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Operações", len(trie.get_operations()))
        with col2:
            st.metric("Prefixos", len(trie.get_words_with_prefix("")) if hasattr(trie, 'get_words_with_prefix') else "N/A")
        with col3:
            st.markdown('<span class="complexity-badge">O(m)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no Trie: {e}")

def render_union_find_structure():
    """Renderiza a estrutura Union-Find."""
    st.markdown("### 🤝 Union-Find")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import UnionFind
        
        # Inicializar Union-Find
        if 'union_find' not in st.session_state:
            st.session_state.union_find = UnionFind(10)
        
        uf = st.session_state.union_find
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔗 Conectar Elementos")
            elem1 = st.number_input("Elemento 1", min_value=0, max_value=9, value=0)
            elem2 = st.number_input("Elemento 2", min_value=0, max_value=9, value=1)
            
            if st.button("Conectar"):
                uf.union(elem1, elem2)
                st.success(f"Elementos {elem1} e {elem2} conectados!")
        
        with col2:
            st.markdown("#### 🔍 Verificar Conexão")
            check1 = st.number_input("Verificar 1", min_value=0, max_value=9, value=0)
            check2 = st.number_input("Verificar 2", min_value=0, max_value=9, value=1)
            
            if st.button("Verificar"):
                conectados = uf.connected(check1, check2)
                if conectados:
                    st.success(f"✅ Elementos {check1} e {check2} estão conectados!")
                else:
                    st.error(f"❌ Elementos {check1} e {check2} não estão conectados!")
        
        # Visualização
        st.markdown("#### 🌐 Visualização dos Componentes")
        
        # Mostrar componentes
        componentes = {}
        for i in range(10):
            root = uf.find(i)
            if root not in componentes:
                componentes[root] = []
            componentes[root].append(i)
        
        for root, elementos in componentes.items():
            st.markdown(f"""
            <div class="algorithm-step">
                <strong>Componente {root}:</strong> {elementos}
            </div>
            """, unsafe_allow_html=True)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Componentes", len(componentes))
        with col2:
            st.metric("Operações", len(uf.get_operations()))
        with col3:
            st.markdown('<span class="complexity-badge">O(α(n))</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no Union-Find: {e}")

def render_segment_tree_structure():
    """Renderiza a estrutura Segment Tree."""
    st.markdown("### 📊 Segment Tree")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import SegmentTree
        
        # Inicializar Segment Tree
        if 'segment_tree' not in st.session_state:
            arr = [1, 3, 5, 7, 9, 11]
            st.session_state.segment_tree = SegmentTree(arr)
        
        seg_tree = st.session_state.segment_tree
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Atualizar Valor")
            index = st.number_input("Índice", min_value=0, max_value=len(seg_tree.arr)-1, value=0)
            new_value = st.number_input("Novo Valor", value=10)
            
            if st.button("Atualizar"):
                seg_tree.update(index, new_value)
                st.success(f"Valor no índice {index} atualizado para {new_value}!")
        
        with col2:
            st.markdown("#### 🔍 Consulta de Soma")
            left = st.number_input("Índice Esquerdo", min_value=0, max_value=len(seg_tree.arr)-1, value=0)
            right = st.number_input("Índice Direito", min_value=0, max_value=len(seg_tree.arr)-1, value=2)
            
            if st.button("Consultar"):
                soma = seg_tree.query(left, right)
                st.success(f"Soma do intervalo [{left}, {right}]: {soma}")
        
        # Visualização
        st.markdown("#### 📊 Array Atual")
        st.write(seg_tree.arr)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(seg_tree.arr)), seg_tree.arr, color='lightblue')
        ax.set_title("Segment Tree - Array")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        
        st.pyplot(fig)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tamanho", len(seg_tree.arr))
        with col2:
            st.metric("Operações", len(seg_tree.get_operations()))
        with col3:
            st.markdown('<span class="complexity-badge">O(log n)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no Segment Tree: {e}")

def render_lru_cache_structure():
    """Renderiza a estrutura LRU Cache."""
    st.markdown("### 💾 LRU Cache")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import LRUCache
        
        # Inicializar LRU Cache
        if 'lru_cache' not in st.session_state:
            st.session_state.lru_cache = LRUCache(4)
        
        cache = st.session_state.lru_cache
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Adicionar/Atualizar")
            key = st.text_input("Chave")
            value = st.text_input("Valor")
            
            if st.button("Adicionar"):
                cache.put(key, value)
                st.success(f"Chave '{key}' adicionada com valor '{value}'!")
        
        with col2:
            st.markdown("#### 🔍 Buscar")
            search_key = st.text_input("Buscar Chave")
            
            if st.button("Buscar"):
                result = cache.get(search_key)
                if result != -1:
                    st.success(f"Valor encontrado: {result}")
                else:
                    st.error(f"Chave '{search_key}' não encontrada!")
        
        # Visualização do cache
        st.markdown("#### 💾 Estado do Cache")
        
        # Mostrar cache atual
        if hasattr(cache, 'cache') and cache.cache:
            cache_items = list(cache.cache.items())
            for i, (key, node) in enumerate(cache_items):
                st.markdown(f"""
                <div class="algorithm-step">
                    <strong>Posição {i+1}:</strong> {key} → {node.value}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Cache vazio")
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Capacidade", cache.capacity)
        with col2:
            current_size = len(cache.cache) if hasattr(cache, 'cache') else 0
            st.metric("Tamanho Atual", current_size)
        with col3:
            st.markdown('<span class="complexity-badge">O(1)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no LRU Cache: {e}")

def render_graph_structure():
    """Renderiza a estrutura Graph."""
    st.markdown("### 🌐 Graph (Grafo)")
    
    try:
        from modulo_2_estruturas_dados.estruturas_avancadas import Graph
        
        # Inicializar Graph
        if 'graph' not in st.session_state:
            st.session_state.graph = Graph()
            # Adicionar nós e arestas de exemplo
            nodes = ["A", "B", "C", "D", "E"]
            edges = [("A", "B"), ("B", "C"), ("C", "D"), ("A", "E"), ("E", "D")]
            
            for node in nodes:
                st.session_state.graph.add_node(node)
            for u, v in edges:
                st.session_state.graph.add_edge(u, v)
        
        graph = st.session_state.graph
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Adicionar Nó/Aresta")
            new_node = st.text_input("Novo Nó")
            if st.button("Adicionar Nó"):
                graph.add_node(new_node)
                st.success(f"Nó '{new_node}' adicionado!")
        
        with col2:
            st.markdown("#### 🔗 Conectar Nós")
            node1 = st.text_input("Nó 1")
            node2 = st.text_input("Nó 2")
            if st.button("Adicionar Aresta"):
                graph.add_edge(node1, node2)
                st.success(f"Aresta {node1} ↔ {node2} adicionada!")
        
        # Algoritmos
        st.markdown("#### 🔍 Algoritmos")
        col1, col2 = st.columns(2)
        
        with col1:
            start_node = st.selectbox("Nó de Início", list(graph.graph.keys()))
            if st.button("BFS"):
                result = graph.bfs(start_node)
                st.success(f"BFS: {result}")
        
        with col2:
            if st.button("DFS"):
                result = graph.dfs(start_node)
                st.success(f"DFS: {result}")
        
        # Visualização
        st.markdown("#### 🌐 Visualização do Grafo")
        
        try:
            import networkx as nx
            
            G = nx.Graph()
            for node in graph.graph.keys():
                G.add_node(node)
            
            for node, neighbors in graph.graph.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)
            
            # Plotar
            fig, ax = plt.subplots(figsize=(10, 8))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                   node_size=1500, font_size=12, font_weight='bold', ax=ax)
            ax.set_title("Grafo - Visualização")
            st.pyplot(fig)
            
        except ImportError:
            st.info("NetworkX não disponível. Mostrando adjacências:")
            for node, neighbors in graph.graph.items():
                st.write(f"**{node}**: {neighbors}")
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nós", len(graph.graph))
        with col2:
            total_edges = sum(len(neighbors) for neighbors in graph.graph.values()) // 2
            st.metric("Arestas", total_edges)
        with col3:
            st.markdown('<span class="complexity-badge">O(V + E)</span>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro no Graph: {e}")

def render_module_3():
    """Renderiza o módulo 3 - Programação Dinâmica."""
    st.markdown("## 🎯 Módulo 3: Programação Dinâmica")
    
    try:
        from modulo_3_programacao_dinamica.metodologia_3_passos import Metodologia3Passos
        
        # Inicializar metodologia
        if 'metodologia' not in st.session_state:
            st.session_state.metodologia = Metodologia3Passos()
        
        metodologia = st.session_state.metodologia
        
        # Seleção de problema
        problema = st.selectbox(
            "Escolha o Problema",
            [
                "🔢 Fibonacci",
                "🎒 Knapsack (0/1)",
                "📝 Longest Common Subsequence",
                "🪙 Coin Change"
            ]
        )
        
        if problema == "🔢 Fibonacci":
            render_fibonacci_problem()
        elif problema == "🎒 Knapsack (0/1)":
            render_knapsack_problem()
        elif problema == "📝 Longest Common Subsequence":
            render_lcs_problem()
        elif problema == "🪙 Coin Change":
            render_coin_change_problem()
            
    except ImportError as e:
        st.error(f"Erro ao importar módulo 3: {e}")
        st.info("Certifique-se de que todos os arquivos do módulo 3 estão presentes.")

def render_fibonacci_problem():
    """Renderiza o problema de Fibonacci."""
    st.markdown("### 🔢 Fibonacci - Metodologia 3 Passos")
    
    try:
        from modulo_3_programacao_dinamica.metodologia_3_passos import Metodologia3Passos
        
        metodologia = Metodologia3Passos()
        
        # Controles
        n = st.slider("Valor de n", 0, 20, 10)
        
        # Abordagem
        abordagem = st.radio(
            "Escolha a Abordagem",
            ["💪 Força Bruta", "🧠 Memoização", "📊 Tabulação"]
        )
        
        # Executar
        if st.button("Calcular Fibonacci"):
            if abordagem == "💪 Força Bruta":
                resultado = metodologia.fibonacci_forca_bruta(n)
                st.success(f"Fibonacci({n}) = {resultado}")
                st.markdown(f'<span class="error-badge">O(2^n)</span>', unsafe_allow_html=True)
                
            elif abordagem == "🧠 Memoização":
                resultado = metodologia.fibonacci_memoizacao(n)
                st.success(f"Fibonacci({n}) = {resultado}")
                st.markdown(f'<span class="warning-badge">O(n)</span>', unsafe_allow_html=True)
                
            elif abordagem == "📊 Tabulação":
                resultado = metodologia.fibonacci_tabulacao(n)
                st.success(f"Fibonacci({n}) = {resultado}")
                st.markdown(f'<span class="complexity-badge">O(n)</span>', unsafe_allow_html=True)
        
        # Explicação da metodologia
        st.markdown("#### 📚 Metodologia 3 Passos")
        
        st.markdown("""
        <div class="algorithm-step">
            <strong>Passo 1: Força Bruta</strong><br>
            Implementação recursiva direta sem otimização.<br>
            Complexidade: O(2^n) - Exponencial
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="algorithm-step">
            <strong>Passo 2: Memoização</strong><br>
            Adiciona cache para evitar recalcular subproblemas.<br>
            Complexidade: O(n) - Linear
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="algorithm-step">
            <strong>Passo 3: Tabulação</strong><br>
            Abordagem bottom-up com tabela DP.<br>
            Complexidade: O(n) - Linear, O(1) espaço
        </div>
        """, unsafe_allow_html=True)
        
        # Visualização da sequência
        if n > 0:
            st.markdown("#### 📊 Sequência de Fibonacci")
            fib_sequence = []
            a, b = 0, 1
            fib_sequence.append(a)
            if n > 0:
                fib_sequence.append(b)
            
            for i in range(2, n + 1):
                c = a + b
                fib_sequence.append(c)
                a, b = b, c
            
            # Gráfico
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(range(n + 1), fib_sequence, 'bo-', linewidth=2, markersize=8)
            ax.set_title(f"Sequência de Fibonacci até F({n})")
            ax.set_xlabel("n")
            ax.set_ylabel("Fibonacci(n)")
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"Erro no Fibonacci: {e}")

def render_knapsack_problem():
    """Renderiza o problema da Knapsack."""
    st.markdown("### 🎒 Knapsack (0/1) - Metodologia 3 Passos")
    
    try:
        from modulo_3_programacao_dinamica.metodologia_3_passos import Metodologia3Passos
        
        metodologia = Metodologia3Passos()
        
        # Controles
        st.markdown("#### 🎮 Configuração")
        
        col1, col2 = st.columns(2)
        
        with col1:
            capacity = st.slider("Capacidade da Mochila", 1, 20, 10)
            
        with col2:
            num_items = st.slider("Número de Itens", 1, 10, 5)
        
        # Gerar itens aleatórios ou usar valores padrão
        if st.button("Gerar Itens Aleatórios"):
            weights = np.random.randint(1, 8, num_items).tolist()
            values = np.random.randint(1, 15, num_items).tolist()
            st.session_state.knapsack_weights = weights
            st.session_state.knapsack_values = values
        
        # Usar valores padrão se não existirem
        if 'knapsack_weights' not in st.session_state:
            st.session_state.knapsack_weights = [2, 3, 4, 5, 6]
            st.session_state.knapsack_values = [3, 4, 5, 6, 7]
        
        weights = st.session_state.knapsack_weights[:num_items]
        values = st.session_state.knapsack_values[:num_items]
        
        # Mostrar itens
        st.markdown("#### 📦 Itens Disponíveis")
        items_df = {
            'Item': [f'Item {i+1}' for i in range(len(weights))],
            'Peso': weights,
            'Valor': values,
            'Valor/Peso': [round(v/w, 2) for v, w in zip(values, weights)]
        }
        st.dataframe(items_df, use_container_width=True)
        
        # Abordagem
        abordagem = st.radio(
            "Escolha a Abordagem",
            ["💪 Força Bruta", "🧠 Memoização", "📊 Tabulação"]
        )
        
        # Executar
        if st.button("Resolver Knapsack"):
            if abordagem == "💪 Força Bruta":
                resultado = metodologia.knapsack_forca_bruta(weights, values, capacity)
                st.success(f"Valor máximo: {resultado}")
                st.markdown(f'<span class="error-badge">O(2^n)</span>', unsafe_allow_html=True)
                
            elif abordagem == "🧠 Memoização":
                resultado = metodologia.knapsack_memoizacao(weights, values, capacity)
                st.success(f"Valor máximo: {resultado}")
                st.markdown(f'<span class="warning-badge">O(n*W)</span>', unsafe_allow_html=True)
                
            elif abordagem == "📊 Tabulação":
                resultado = metodologia.knapsack_tabulacao(weights, values, capacity)
                st.success(f"Valor máximo: {resultado}")
                st.markdown(f'<span class="complexity-badge">O(n*W)</span>', unsafe_allow_html=True)
        
        # Visualização
        st.markdown("#### 📊 Visualização dos Itens")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de pesos vs valores
        ax1.scatter(weights, values, s=100, alpha=0.7, c='blue')
        for i, (w, v) in enumerate(zip(weights, values)):
            ax1.annotate(f'Item {i+1}', (w, v), xytext=(5, 5), 
                        textcoords='offset points', fontsize=8)
        ax1.set_xlabel('Peso')
        ax1.set_ylabel('Valor')
        ax1.set_title('Peso vs Valor dos Itens')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de barras - eficiência
        efficiency = [v/w for v, w in zip(values, weights)]
        bars = ax2.bar(range(len(weights)), efficiency, alpha=0.7, color='green')
        ax2.set_xlabel('Itens')
        ax2.set_ylabel('Valor/Peso')
        ax2.set_title('Eficiência dos Itens')
        ax2.set_xticks(range(len(weights)))
        ax2.set_xticklabels([f'Item {i+1}' for i in range(len(weights))])
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Erro no Knapsack: {e}")

def render_lcs_problem():
    """Renderiza o problema de Longest Common Subsequence."""
    st.markdown("### 📝 Longest Common Subsequence - Metodologia 3 Passos")
    
    try:
        from modulo_3_programacao_dinamica.metodologia_3_passos import Metodologia3Passos
        
        metodologia = Metodologia3Passos()
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            str1 = st.text_input("String 1", value="ABCDGH")
            
        with col2:
            str2 = st.text_input("String 2", value="AEDFHR")
        
        # Abordagem
        abordagem = st.radio(
            "Escolha a Abordagem",
            ["💪 Força Bruta", "🧠 Memoização", "📊 Tabulação"]
        )
        
        # Executar
        if st.button("Calcular LCS"):
            if abordagem == "💪 Força Bruta":
                resultado = metodologia.lcs_forca_bruta(str1, str2)
                st.success(f"Comprimento da LCS: {resultado}")
                st.markdown(f'<span class="error-badge">O(2^n)</span>', unsafe_allow_html=True)
                
            elif abordagem == "🧠 Memoização":
                resultado = metodologia.lcs_memoizacao(str1, str2)
                st.success(f"Comprimento da LCS: {resultado}")
                st.markdown(f'<span class="warning-badge">O(m*n)</span>', unsafe_allow_html=True)
                
            elif abordagem == "📊 Tabulação":
                resultado = metodologia.lcs_tabulacao(str1, str2)
                st.success(f"Comprimento da LCS: {resultado}")
                st.markdown(f'<span class="complexity-badge">O(m*n)</span>', unsafe_allow_html=True)
        
        # Visualização das strings
        st.markdown("#### 🔤 Comparação das Strings")
        
        if str1 and str2:
            # Mostrar caracteres
            st.markdown("**String 1:**")
            cols1 = st.columns(len(str1))
            for i, char in enumerate(str1):
                with cols1[i]:
                    st.markdown(f"**{char}**")
            
            st.markdown("**String 2:**")
            cols2 = st.columns(len(str2))
            for i, char in enumerate(str2):
                with cols2[i]:
                    st.markdown(f"**{char}**")
            
            # Encontrar caracteres comuns
            common_chars = set(str1) & set(str2)
            st.markdown(f"**Caracteres em comum:** {sorted(common_chars)}")
        
        # Explicação
        st.markdown("#### 💡 Conceito")
        st.markdown("""
        <div class="algorithm-step">
            <strong>Longest Common Subsequence (LCS)</strong><br>
            Encontra a maior subsequência comum entre duas strings.<br>
            Exemplo: "ABCDGH" e "AEDFHR" → LCS = "ADH" (comprimento 3)
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro no LCS: {e}")

def render_coin_change_problem():
    """Renderiza o problema de Coin Change."""
    st.markdown("### 🪙 Coin Change - Metodologia 3 Passos")
    
    try:
        from modulo_3_programacao_dinamica.metodologia_3_passos import Metodologia3Passos
        
        metodologia = Metodologia3Passos()
        
        # Controles
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Quantidade", min_value=1, max_value=100, value=11)
            
        with col2:
            coins_input = st.text_input("Moedas (separadas por vírgula)", value="1,2,5")
            
        try:
            coins = [int(x.strip()) for x in coins_input.split(",")]
        except:
            coins = [1, 2, 5]
        
        st.write(f"**Moedas disponíveis:** {coins}")
        st.write(f"**Quantidade alvo:** {amount}")
        
        # Abordagem
        abordagem = st.radio(
            "Escolha a Abordagem",
            ["💪 Força Bruta", "🧠 Memoização", "📊 Tabulação"]
        )
        
        # Executar
        if st.button("Calcular Coin Change"):
            if abordagem == "💪 Força Bruta":
                resultado = metodologia.coin_change_forca_bruta(coins, amount)
                if resultado == float('inf'):
                    st.error("Não é possível formar a quantidade com as moedas disponíveis")
                else:
                    st.success(f"Número mínimo de moedas: {resultado}")
                st.markdown(f'<span class="error-badge">O(2^n)</span>', unsafe_allow_html=True)
                
            elif abordagem == "🧠 Memoização":
                resultado = metodologia.coin_change_memoizacao(coins, amount)
                if resultado == float('inf'):
                    st.error("Não é possível formar a quantidade com as moedas disponíveis")
                else:
                    st.success(f"Número mínimo de moedas: {resultado}")
                st.markdown(f'<span class="warning-badge">O(n*amount)</span>', unsafe_allow_html=True)
                
            elif abordagem == "📊 Tabulação":
                resultado = metodologia.coin_change_tabulacao(coins, amount)
                if resultado == float('inf'):
                    st.error("Não é possível formar a quantidade com as moedas disponíveis")
                else:
                    st.success(f"Número mínimo de moedas: {resultado}")
                st.markdown(f'<span class="complexity-badge">O(n*amount)</span>', unsafe_allow_html=True)
        
        # Visualização
        st.markdown("#### 🪙 Visualização das Moedas")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Mostrar moedas como barras
        bars = ax.bar(range(len(coins)), coins, alpha=0.7, color='gold')
        ax.set_xlabel('Tipo de Moeda')
        ax.set_ylabel('Valor')
        ax.set_title('Moedas Disponíveis')
        ax.set_xticks(range(len(coins)))
        ax.set_xticklabels([f'Moeda {i+1}' for i in range(len(coins))])
        
        # Adicionar valores nas barras
        for bar, coin in zip(bars, coins):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{coin}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig)
        
        # Explicação
        st.markdown("#### 💡 Conceito")
        st.markdown("""
        <div class="algorithm-step">
            <strong>Coin Change Problem</strong><br>
            Encontra o número mínimo de moedas necessárias para formar uma quantia.<br>
            Exemplo: Para 11 com moedas [1,2,5] → 3 moedas (5+5+1)
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro no Coin Change: {e}")

def render_module_4():
    """Renderiza o módulo 4 - Entrevistas."""
    st.markdown("## 💼 Módulo 4: Entrevistas")
    
    try:
        from modulo_4_entrevistas.problem_playground import InterviewSession
        
        # Inicializar sessão de entrevista
        if 'interview_session' not in st.session_state:
            st.session_state.interview_session = InterviewSession()
        
        session = st.session_state.interview_session
        
        # Seleção de modo
        mode = st.selectbox(
            "Escolha o Modo",
            [
                "🎯 Simulação de Entrevista",
                "📚 Biblioteca de Problemas",
                "📊 Análise de Código",
                "⏱️ Prática com Tempo"
            ]
        )
        
        if mode == "🎯 Simulação de Entrevista":
            render_interview_simulation()
        elif mode == "📚 Biblioteca de Problemas":
            render_problem_library()
        elif mode == "📊 Análise de Código":
            render_code_analysis()
        elif mode == "⏱️ Prática com Tempo":
            render_timed_practice()
            
    except ImportError as e:
        st.error(f"Erro ao importar módulo 4: {e}")
        st.info("Certifique-se de que todos os arquivos do módulo 4 estão presentes.")

def render_interview_simulation():
    """Renderiza a simulação de entrevista."""
    st.markdown("### 🎯 Simulação de Entrevista")
    
    try:
        from modulo_4_entrevistas.problem_playground import InterviewSession
        
        session = st.session_state.interview_session
        
        # Configurações da entrevista
        st.markdown("#### ⚙️ Configurações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            difficulty = st.selectbox("Dificuldade", ["Easy", "Medium", "Hard"])
            category = st.selectbox("Categoria", ["Array", "String", "Tree", "Graph", "Dynamic Programming"])
            
        with col2:
            time_limit = st.slider("Tempo Limite (minutos)", 15, 60, 30)
            show_hints = st.checkbox("Mostrar Dicas", value=True)
        
        # Iniciar entrevista
        if st.button("🚀 Iniciar Nova Entrevista"):
            problem = session.get_random_problem(difficulty, category)
            st.session_state.current_problem = problem
            st.session_state.interview_start_time = time.time()
            st.session_state.interview_active = True
            st.success("Entrevista iniciada!")
        
        # Mostrar problema atual
        if hasattr(st.session_state, 'current_problem') and st.session_state.current_problem:
            problem = st.session_state.current_problem
            
            st.markdown("#### 📋 Problema Atual")
            st.markdown(f"""
            <div class="algorithm-step">
                <strong>{problem['title']}</strong><br>
                <strong>Dificuldade:</strong> {problem['difficulty']}<br>
                <strong>Categoria:</strong> {problem['category']}<br><br>
                {problem['description']}
            </div>
            """, unsafe_allow_html=True)
            
            # Exemplos
            if 'examples' in problem:
                st.markdown("#### 💡 Exemplos")
                for i, example in enumerate(problem['examples']):
                    st.markdown(f"""
                    <div class="metric-card">
                        <strong>Exemplo {i+1}:</strong><br>
                        <strong>Input:</strong> {example['input']}<br>
                        <strong>Output:</strong> {example['output']}<br>
                        <strong>Explicação:</strong> {example.get('explanation', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Editor de código
            st.markdown("#### 💻 Sua Solução")
            code = st.text_area("Escreva seu código aqui:", height=300, 
                              value=problem.get('template', '# Escreva sua solução aqui'))
            
            # Botões de ação
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🧪 Testar Código"):
                    # Aqui você pode adicionar lógica de teste
                    st.info("Testando código...")
                    
            with col2:
                if st.button("💡 Dica"):
                    if show_hints and 'hints' in problem:
                        hint = problem['hints'][0] if problem['hints'] else "Nenhuma dica disponível"
                        st.success(f"💡 {hint}")
                    else:
                        st.info("Dicas desabilitadas")
                        
            with col3:
                if st.button("✅ Submeter"):
                    # Análise do código
                    analysis = session.analyze_code(code)
                    st.success("Código submetido!")
                    
                    # Mostrar análise
                    st.markdown("#### 📊 Análise da Solução")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Complexidade", analysis.get('complexity', 'N/A'))
                    with col2:
                        st.metric("Estilo", analysis.get('style_score', 'N/A'))
                    with col3:
                        st.metric("Corretude", analysis.get('correctness', 'N/A'))
                    
                    # Feedback
                    if 'feedback' in analysis:
                        st.markdown(f"""
                        <div class="algorithm-step">
                            <strong>Feedback:</strong><br>
                            {analysis['feedback']}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Timer
        if hasattr(st.session_state, 'interview_active') and st.session_state.interview_active:
            elapsed = time.time() - st.session_state.interview_start_time
            remaining = max(0, time_limit * 60 - elapsed)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tempo Decorrido", f"{int(elapsed // 60)}:{int(elapsed % 60):02d}")
            with col2:
                st.metric("Tempo Restante", f"{int(remaining // 60)}:{int(remaining % 60):02d}")
                
            if remaining <= 0:
                st.error("⏰ Tempo esgotado!")
                st.session_state.interview_active = False
                
    except Exception as e:
        st.error(f"Erro na simulação: {e}")

def render_problem_library():
    """Renderiza a biblioteca de problemas."""
    st.markdown("### 📚 Biblioteca de Problemas")
    
    # Problemas exemplo
    problems = [
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "category": "Array",
            "description": "Encontre dois números em um array que somem um valor alvo.",
            "examples": [
                {"input": "[2,7,11,15], target=9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"}
            ]
        },
        {
            "title": "Reverse Linked List",
            "difficulty": "Easy",
            "category": "Linked List",
            "description": "Inverta uma lista ligada.",
            "examples": [
                {"input": "1->2->3->4->5", "output": "5->4->3->2->1", "explanation": "Inverter a ordem dos nós"}
            ]
        },
        {
            "title": "Maximum Subarray",
            "difficulty": "Medium",
            "category": "Array",
            "description": "Encontre o subarray contíguo com a maior soma.",
            "examples": [
                {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "Subarray [4,-1,2,1] tem soma 6"}
            ]
        },
        {
            "title": "Climbing Stairs",
            "difficulty": "Easy",
            "category": "Dynamic Programming",
            "description": "Quantas maneiras distintas existem para subir n degraus?",
            "examples": [
                {"input": "n=3", "output": "3", "explanation": "1+1+1, 1+2, 2+1"}
            ]
        }
    ]
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        filter_difficulty = st.selectbox("Filtrar por Dificuldade", ["Todas", "Easy", "Medium", "Hard"])
        
    with col2:
        filter_category = st.selectbox("Filtrar por Categoria", 
                                     ["Todas", "Array", "String", "Linked List", "Tree", "Dynamic Programming"])
    
    # Aplicar filtros
    filtered_problems = problems
    if filter_difficulty != "Todas":
        filtered_problems = [p for p in filtered_problems if p['difficulty'] == filter_difficulty]
    if filter_category != "Todas":
        filtered_problems = [p for p in filtered_problems if p['category'] == filter_category]
    
    # Mostrar problemas
    st.markdown("#### 📋 Problemas Disponíveis")
    
    for i, problem in enumerate(filtered_problems):
        with st.expander(f"{problem['title']} ({problem['difficulty']})"):
            st.markdown(f"""
            <div class="algorithm-step">
                <strong>Categoria:</strong> {problem['category']}<br>
                <strong>Descrição:</strong> {problem['description']}
            </div>
            """, unsafe_allow_html=True)
            
            # Exemplos
            if 'examples' in problem:
                st.markdown("**Exemplos:**")
                for j, example in enumerate(problem['examples']):
                    st.markdown(f"""
                    - **Input:** {example['input']}
                    - **Output:** {example['output']}
                    - **Explicação:** {example.get('explanation', 'N/A')}
                    """)
            
            if st.button(f"Resolver {problem['title']}", key=f"solve_{i}"):
                st.session_state.current_problem = problem
                st.success(f"Problema '{problem['title']}' selecionado!")
    
    # Estatísticas
    st.markdown("#### 📊 Estatísticas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Problemas", len(problems))
        
    with col2:
        easy_count = len([p for p in problems if p['difficulty'] == 'Easy'])
        st.metric("Problemas Easy", easy_count)
        
    with col3:
        medium_count = len([p for p in problems if p['difficulty'] == 'Medium'])
        st.metric("Problemas Medium", medium_count)

def render_code_analysis():
    """Renderiza a análise de código."""
    st.markdown("### 📊 Análise de Código")
    
    st.markdown("#### 💻 Cole seu código para análise")
    
    # Editor de código
    code = st.text_area("Código:", height=300, 
                       value="""def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""")
    
    # Análise
    if st.button("🔍 Analisar Código"):
        try:
            from modulo_4_entrevistas.problem_playground import InterviewSession
            
            session = InterviewSession()
            analysis = session.analyze_code(code)
            
            st.markdown("#### 📈 Resultados da Análise")
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                complexity = analysis.get('time_complexity', 'N/A')
                st.metric("Complexidade Temporal", complexity)
                
            with col2:
                space_complexity = analysis.get('space_complexity', 'N/A')
                st.metric("Complexidade Espacial", space_complexity)
                
            with col3:
                style_score = analysis.get('style_score', 'N/A')
                st.metric("Pontuação de Estilo", f"{style_score}/10" if isinstance(style_score, (int, float)) else style_score)
                
            with col4:
                correctness = analysis.get('correctness', 'N/A')
                st.metric("Corretude", correctness)
            
            # Feedback detalhado
            if 'feedback' in analysis:
                st.markdown("#### 💬 Feedback Detalhado")
                st.markdown(f"""
                <div class="algorithm-step">
                    {analysis['feedback']}
                </div>
                """, unsafe_allow_html=True)
            
            # Sugestões de melhoria
            if 'suggestions' in analysis:
                st.markdown("#### 💡 Sugestões de Melhoria")
                for suggestion in analysis['suggestions']:
                    st.markdown(f"""
                    <div class="metric-card">
                        {suggestion}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Comparação com solução otimizada
            if 'optimized_solution' in analysis:
                st.markdown("#### ⚡ Solução Otimizada")
                st.code(analysis['optimized_solution'], language='python')
                
        except Exception as e:
            st.error(f"Erro na análise: {e}")
            
            # Análise básica manual
            st.markdown("#### 📊 Análise Básica")
            
            lines = code.split('\n')
            has_nested_loops = any('for' in line and any('for' in other for other in lines[i+1:]) for i, line in enumerate(lines))
            
            if has_nested_loops:
                st.markdown('<span class="error-badge">O(n²) - Complexidade alta detectada</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="complexity-badge">O(n) ou melhor</span>', unsafe_allow_html=True)
            
            st.info("Análise detalhada indisponível. Verifique se o módulo 4 está instalado corretamente.")

def render_timed_practice():
    """Renderiza a prática com tempo."""
    st.markdown("### ⏱️ Prática com Tempo")
    
    # Configurações
    col1, col2 = st.columns(2)
    
    with col1:
        practice_time = st.slider("Tempo de Prática (minutos)", 5, 30, 15)
        
    with col2:
        problem_type = st.selectbox("Tipo de Problema", ["Fácil", "Médio", "Difícil", "Misto"])
    
    # Iniciar prática
    if st.button("🏃 Iniciar Prática"):
        st.session_state.practice_start_time = time.time()
        st.session_state.practice_active = True
        st.session_state.practice_duration = practice_time * 60
        st.success("Prática iniciada!")
    
    # Timer e progresso
    if hasattr(st.session_state, 'practice_active') and st.session_state.practice_active:
        elapsed = time.time() - st.session_state.practice_start_time
        remaining = max(0, st.session_state.practice_duration - elapsed)
        
        # Barra de progresso
        progress = min(1.0, elapsed / st.session_state.practice_duration)
        st.progress(progress)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tempo Decorrido", f"{int(elapsed // 60)}:{int(elapsed % 60):02d}")
        with col2:
            st.metric("Tempo Restante", f"{int(remaining // 60)}:{int(remaining % 60):02d}")
        
        if remaining <= 0:
            st.success("🏁 Prática finalizada!")
            st.session_state.practice_active = False
            st.balloons()
    
    # Estatísticas de prática
    st.markdown("#### 📊 Estatísticas de Prática")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Problemas Resolvidos", st.session_state.get('problems_solved', 0))
        
    with col2:
        st.metric("Tempo Médio", f"{st.session_state.get('avg_time', 0):.1f} min")
        
    with col3:
        st.metric("Taxa de Acerto", f"{st.session_state.get('success_rate', 0):.1f}%")
    
    # Dicas para prática
    st.markdown("#### 💡 Dicas para Prática Eficiente")
    
    tips = [
        "Comece com problemas mais fáceis para ganhar confiança",
        "Pratique algoritmos fundamentais regularmente",
        "Analise soluções de outras pessoas após resolver",
        "Mantenha um tempo limite para cada problema",
        "Foque na clareza do código, não apenas na solução"
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="metric-card">
            💡 {tip}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
