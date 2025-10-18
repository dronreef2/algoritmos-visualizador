"""
🎯 EXPERIÊNCIA DE APRENDIZADO CONTEXTUALIZADO
============================================

Interface Streamlit para o sistema de aprendizado contextualizado
com jornadas temáticas, contexto histórico e aplicações práticas.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from sistema_aprendizado_contextual import sistema_aprendizado, Conceito, JornadaAprendizado, Dificuldade, Tema


def render_aprendizado_contextual():
    """Renderiza a página principal de aprendizado contextualizado"""

    st.markdown(
        """
    ## 🎯 Aprendizado Contextualizado

    ### Uma jornada imersiva através dos algoritmos e estruturas de dados

    Explore conceitos através de **jornadas temáticas**, entenda o **contexto histórico**,
    veja **aplicações reais** e conecte conceitos em um **mapa de aprendizado visual**.
    """
    )

    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🗺️ Mapa de Aprendizado", "🚀 Jornadas Temáticas", "📚 Conceitos Interativos", "📊 Meu Progresso"]
    )

    with tab1:
        render_mapa_aprendizado()

    with tab2:
        render_jornadas_tematicas()

    with tab3:
        render_conceitos_interativos()

    with tab4:
        render_progresso_usuario()


def render_mapa_aprendizado():
    """Renderiza o mapa visual de aprendizado"""

    st.markdown("### 🗺️ Mapa de Aprendizado")

    st.markdown(
        """
    Visualize como os conceitos se conectam e evoluem. Cada nó representa um conceito,
    e as conexões mostram pré-requisitos e progressão natural de aprendizado.
    """
    )

    # Criar dados para o grafo
    nodes = []
    edges = []

    # Adicionar nós (conceitos)
    for nome, conceito in sistema_aprendizado.conceitos.items():
        nodes.append(
            {
                "id": nome,
                "label": conceito.nome,
                "dificuldade": conceito.dificuldade.value,
                "tema": conceito.tema.value,
                "size": 20 + len(conceito.aplicacoes_reais) * 2,
            }
        )

        # Adicionar arestas (pré-requisitos)
        for pre_req in conceito.pre_requisitos:
            if pre_req in sistema_aprendizado.conceitos:
                edges.append({"from": pre_req, "to": nome})

    # Criar visualização com Plotly
    fig = go.Figure()

    # Adicionar nós
    for node in nodes:
        fig.add_trace(
            go.Scatter(
                x=[node["id"]],  # Posição baseada no nome (simplificado)
                y=[node["size"]],
                mode="markers+text",
                marker=dict(
                    size=node["size"],
                    color={"iniciante": "lightgreen", "intermediario": "orange", "avancado": "red"}[node["dificuldade"]],
                    line=dict(width=2, color="black"),
                ),
                text=node["label"],
                textposition="top center",
                name=node["label"],
            )
        )

    # Adicionar arestas
    for edge in edges:
        fig.add_trace(
            go.Scatter(
                x=[edge["from"], edge["to"]],
                y=[20, 20],  # Linha horizontal simplificada
                mode="lines",
                line=dict(width=2, color="gray"),
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Mapa de Conexões entre Conceitos",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Legenda
    st.markdown(
        """
    **Legenda:**
    - 🟢 Verde: Conceitos Iniciantes
    - 🟠 Laranja: Conceitos Intermediários
    - 🔴 Vermelho: Conceitos Avançados
    - 📏 Tamanho: Número de aplicações reais
    - ➡️ Setas: Pré-requisitos necessários
    """
    )


def render_jornadas_tematicas():
    """Renderiza as jornadas de aprendizado temáticas"""

    st.markdown("### 🚀 Jornadas de Aprendizado Temáticas")

    st.markdown(
        """
    Escolha uma jornada completa de aprendizado com objetivos claros,
    projetos práticos e progressão estruturada.
    """
    )

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        tema_filtro = st.selectbox("Filtrar por Tema:", ["Todos"] + [tema.value for tema in Tema], key="tema_jornada")

    with col2:
        dificuldade_filtro = st.selectbox(
            "Filtrar por Dificuldade:", ["Todos"] + [dif.value for dif in Dificuldade], key="dif_jornada"
        )

    # Filtrar jornadas
    jornadas_filtradas = sistema_aprendizado.jornadas.values()

    if tema_filtro != "Todos":
        jornadas_filtradas = [j for j in jornadas_filtradas if j.tema_principal.value == tema_filtro]

    if dificuldade_filtro != "Todos":
        jornadas_filtradas = [j for j in jornadas_filtradas if j.dificuldade.value == dificuldade_filtro]

    # Exibir jornadas
    for jornada in jornadas_filtradas:
        with st.expander(f"🎯 {jornada.titulo}", expanded=False):

            # Cabeçalho da jornada
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Dificuldade", jornada.dificuldade.value.title())
            with col2:
                st.metric("Duração", jornada.duracao_estimada)
            with col3:
                progresso = sistema_aprendizado.calcular_progresso_jornada(
                    list(sistema_aprendizado.jornadas.keys())[list(sistema_aprendizado.jornadas.values()).index(jornada)]
                )
                st.metric("Progresso", f"{progresso:.1f}%")

            st.markdown(f"**{jornada.descricao}**")

            # Objetivos de aprendizado
            st.markdown("#### 🎯 Objetivos de Aprendizado")
            for objetivo in jornada.objetivos_aprendizagem:
                st.markdown(f"• {objetivo}")

            # Conceitos incluídos
            st.markdown("#### 📚 Conceitos Incluídos")
            conceitos_texto = []
            for conceito_id in jornada.conceitos:
                if conceito_id in sistema_aprendizado.conceitos:
                    conceito = sistema_aprendizado.conceitos[conceito_id]
                    conceitos_texto.append(conceito.nome)
            st.write(", ".join(conceitos_texto))

            # Projetos práticos
            st.markdown("#### 🛠️ Projetos Práticos")
            for projeto in jornada.projetos_praticos:
                st.markdown(f"• {projeto}")

            # Botão para iniciar jornada
            if st.button(f"🚀 Iniciar Jornada: {jornada.titulo}", key=f"start_{jornada.titulo}"):
                st.success(f"Jornada '{jornada.titulo}' iniciada! 🎉")
                st.info("Funcionalidade completa será implementada em breve.")


def render_conceitos_interativos():
    """Renderiza a exploração interativa de conceitos"""

    st.markdown("### 📚 Exploração de Conceitos")

    st.markdown(
        """
    Explore conceitos individuais com contexto histórico, aplicações reais
    e conexões com outros conceitos.
    """
    )

    # Seleção de conceito
    conceitos_nomes = list(sistema_aprendizado.conceitos.keys())
    conceito_selecionado = st.selectbox(
        "Selecione um conceito para explorar:", conceitos_nomes, format_func=lambda x: sistema_aprendizado.conceitos[x].nome
    )

    if conceito_selecionado:
        conceito = sistema_aprendizado.conceitos[conceito_selecionado]

        # Cabeçalho do conceito
        st.markdown(f"## {conceito.nome}")
        st.markdown(f"*{conceito.descricao}*")

        # Métricas rápidas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dificuldade", conceito.dificuldade.value.title())
        with col2:
            st.metric("Tema", conceito.tema.value.title())
        with col3:
            st.metric("Pré-requisitos", len(conceito.pre_requisitos))

        # Tabs do conceito
        tab1, tab2, tab3, tab4 = st.tabs(["📖 Conceito", "🏛️ Contexto Histórico", "🌍 Aplicações Reais", "🔗 Conexões"])

        with tab1:
            st.markdown("#### 📖 Entendimento do Conceito")
            st.write(conceito.descricao)

            st.markdown("#### 💡 Exemplos Práticos")
            for exemplo in conceito.exemplos_praticos:
                st.markdown(f"• {exemplo}")

        with tab2:
            st.markdown("#### 🏛️ Contexto Histórico")
            st.write(conceito.contexto_historico)

        with tab3:
            st.markdown("#### 🌍 Aplicações no Mundo Real")
            for aplicacao in conceito.aplicacoes_reais:
                st.markdown(f"• {aplicacao}")

        with tab4:
            st.markdown("#### 🔗 Conexões e Pré-requisitos")

            if conceito.pre_requisitos:
                st.markdown("**Pré-requisitos necessários:**")
                for pre_req in conceito.pre_requisitos:
                    if pre_req in sistema_aprendizado.conceitos:
                        pre_conceito = sistema_aprendizado.conceitos[pre_req]
                        st.markdown(f"• {pre_conceito.nome}")
                    else:
                        st.markdown(f"• {pre_req}")

            # Recomendação do próximo conceito
            proximo = sistema_aprendizado.recomendar_proximo_conceito(conceito_selecionado)
            if proximo:
                proximo_conceito = sistema_aprendizado.conceitos[proximo]
                st.markdown(
                    f"""
                **🎯 Próximo conceito recomendado:**
                {proximo_conceito.nome} - {proximo_conceito.descricao}
                """
                )


def render_progresso_usuario():
    """Renderiza o dashboard de progresso do usuário"""

    st.markdown("### 📊 Meu Progresso de Aprendizado")

    st.markdown(
        """
    Acompanhe seu progresso através das jornadas e conceitos estudados.
    """
    )

    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        conceitos_total = len(sistema_aprendizado.conceitos)
        conceitos_completados = len(sistema_aprendizado.progresso_usuario["conceitos_completados"])
        st.metric("Conceitos Estudados", f"{conceitos_completados}/{conceitos_total}")

    with col2:
        jornadas_total = len(sistema_aprendizado.jornadas)
        jornadas_iniciadas = len(sistema_aprendizado.progresso_usuario["jornadas_iniciadas"])
        st.metric("Jornadas Iniciadas", f"{jornadas_iniciadas}/{jornadas_total}")

    with col3:
        tempo_estudado = sistema_aprendizado.progresso_usuario["tempo_estudado"]
        st.metric("Tempo Estudado", f"{tempo_estudado}h")

    with col4:
        exercicios = sistema_aprendizado.progresso_usuario["exercicios_resolvidos"]
        st.metric("Exercícios Resolvidos", exercicios)

    # Gráfico de progresso por tema
    st.markdown("#### 📈 Progresso por Tema")

    temas_progresso = {}
    for tema in Tema:
        conceitos_tema = [c for c in sistema_aprendizado.conceitos.values() if c.tema == tema]
        if conceitos_tema:
            completados_tema = len(
                [c for c in conceitos_tema if c.nome in sistema_aprendizado.progresso_usuario["conceitos_completados"]]
            )
            temas_progresso[tema.value] = (completados_tema / len(conceitos_tema)) * 100

    if temas_progresso:
        fig = px.bar(
            x=list(temas_progresso.keys()),
            y=list(temas_progresso.values()),
            title="Progresso por Tema (%)",
            labels={"x": "Tema", "y": "Progresso (%)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    # Próximas recomendações
    st.markdown("#### 🎯 Recomendações Personalizadas")

    # Simular recomendações baseadas no progresso atual
    recomendacoes = [
        "Complete os fundamentos antes de avançar para estruturas complexas",
        "Pratique algoritmos de busca antes de grafos",
        "Estude programação dinâmica após dominar recursão",
        "Aplique conceitos em projetos práticos",
    ]

    for rec in recomendacoes:
        st.info(f"💡 {rec}")


# Função para integrar com o menu principal
def integrar_aprendizado_contextual():
    """Integra o aprendizado contextualizado no menu principal"""

    # Adicionar opção no menu
    menu_options = [
        "🏠 Home",
        "🎯 Aprendizado Contextualizado",  # Nova opção
        "📚 Módulo 1: Fundamentos",
        "🏗️ Módulo 2: Estruturas de Dados",
        "🎯 Módulo 3: Programação Dinâmica",
        "💼 Módulo 4: Entrevistas",
        "🔍 Busca MCP (Tavily)",
    ]

    # Esta função deve ser chamada no lugar do selectbox principal
    return menu_options
