"""
🎯 INTERFACE DE EXERCÍCIOS PRÁTICOS INTERATIVOS
==============================================

Interface Streamlit para exercícios práticos com validação
em tempo real e feedback imediato.
"""

import streamlit as st
import time
import random
from typing import Any, Dict
from sistema_exercicios_praticos import (
    sistema_exercicios,
    Exercicio,
    TipoExercicio,
    Dificuldade,
    SessaoExercicio
)

def render_exercicios_praticos():
    """Renderiza a página principal de exercícios práticos"""

    st.markdown("""
    ## 🎯 Exercícios Práticos Interativos

    ### Pratique e consolide seu conhecimento

    Resolva exercícios interativos com **validação em tempo real**,
    **feedback imediato** e **dicas contextuais** para aprender fazendo.
    """)

    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Praticar Exercícios",
        "🎯 Por Conceito",
        "📊 Meu Desempenho",
        "🏆 Conquistas"
    ])

    with tab1:
        render_pratica_exercicios()

    with tab2:
        render_exercicios_por_conceito()

    with tab3:
        render_desempenho_usuario()

    with tab4:
        render_conquistas()

def render_pratica_exercicios():
    """Renderiza a interface de prática de exercícios"""

    st.markdown("### 📝 Prática de Exercícios")

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        dificuldade_filtro = st.selectbox(
            "Dificuldade:",
            ["Todas"] + [d.value for d in Dificuldade],
            key="dif_exercicios"
        )

    with col2:
        tipo_filtro = st.selectbox(
            "Tipo:",
            ["Todos"] + [t.value for t in TipoExercicio],
            key="tipo_exercicios"
        )

    with col3:
        modo_aleatorio = st.checkbox("Modo Aleatório", value=True)

    # Filtrar exercícios
    exercicios_filtrados = list(sistema_exercicios.exercicios.values())

    if dificuldade_filtro != "Todas":
        exercicios_filtrados = [
            ex for ex in exercicios_filtrados
            if ex.dificuldade.value == dificuldade_filtro
        ]

    if tipo_filtro != "Todos":
        exercicios_filtrados = [
            ex for ex in exercicios_filtrados
            if ex.tipo.value == tipo_filtro
        ]

    if not exercicios_filtrados:
        st.warning("Nenhum exercício encontrado com os filtros selecionados.")
        return

    # Selecionar exercício
    if modo_aleatorio:
        exercicio_selecionado = random.choice(exercicios_filtrados)
    else:
        exercicio_nomes = [ex.titulo for ex in exercicios_filtrados]
        exercicio_idx = st.selectbox(
            "Selecione um exercício:",
            range(len(exercicio_nomes)),
            format_func=lambda x: exercicio_nomes[x]
        )
        exercicio_selecionado = exercicios_filtrados[exercicio_idx]

    # Iniciar sessão se necessário
    if 'sessao_atual' not in st.session_state or \
       st.session_state.sessao_atual.exercicio_id != exercicio_selecionado.id:

        sessao = sistema_exercicios.iniciar_sessao_exercicio(exercicio_selecionado.id)
        if sessao:
            st.session_state.sessao_atual = sessao
            st.session_state.tentativa_atual = 1
            st.session_state.resposta_submetida = False
            st.session_state.feedback = None

    # Exibir exercício
    render_exercicio_interativo(exercicio_selecionado)

def render_exercicio_interativo(exercicio: Exercicio):
    """Renderiza um exercício específico de forma interativa"""

    # Cabeçalho do exercício
    st.markdown(f"## {exercicio.titulo}")
    st.markdown(f"*{exercicio.descricao}*")

    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dificuldade", exercicio.dificuldade.value.title())
    with col2:
        st.metric("Tipo", exercicio.tipo.value.replace('_', ' ').title())
    with col3:
        st.metric("Tempo Estimado", f"{exercicio.tempo_estimado}min")

    # Enunciado
    st.markdown("### 📋 Enunciado")
    st.write(exercicio.enunciado)

    # Interface baseada no tipo de exercício
    resposta_usuario = render_interface_exercicio(exercicio)

    # Controles de resposta
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("💡 Dica", key=f"dica_{exercicio.id}"):
            dica = sistema_exercicios.obter_dica(
                exercicio.id,
                st.session_state.get('tentativa_atual', 1)
            )
            if dica:
                st.info(f"💡 **Dica:** {dica}")
            else:
                st.warning("Não há mais dicas disponíveis.")

    with col2:
        if st.button("🔄 Reiniciar", key=f"reiniciar_{exercicio.id}"):
            # Reiniciar sessão
            if 'sessao_atual' in st.session_state:
                del st.session_state.sessao_atual
            st.session_state.tentativa_atual = 1
            st.session_state.resposta_submetida = False
            st.session_state.feedback = None
            st.rerun()

    with col3:
        submit_disabled = resposta_usuario is None or st.session_state.get('resposta_submetida', False)
        if st.button(
            "✅ Submeter Resposta",
            disabled=submit_disabled,
            key=f"submit_{exercicio.id}"
        ):
            # Validar resposta
            feedback = sistema_exercicios.validar_resposta(
                st.session_state.sessao_atual.exercicio_id,
                resposta_usuario
            )
            st.session_state.feedback = feedback
            st.session_state.resposta_submetida = True

    # Exibir feedback
    if st.session_state.get('feedback'):
        render_feedback(st.session_state.feedback, exercicio)

def render_interface_exercicio(exercicio: Exercicio) -> Any:
    """Renderiza a interface específica para cada tipo de exercício"""

    if exercicio.tipo == TipoExercicio.MULTIPLA_ESCOLHA:
        opcoes = exercicio.dados_exercicio["opcoes"]
        return st.radio(
            "Selecione a resposta correta:",
            options=range(len(opcoes)),
            format_func=lambda x: opcoes[x],
            key=f"resposta_{exercicio.id}"
        )

    elif exercicio.tipo == TipoExercicio.VERDADEIRO_FALSO:
        afirmacoes = exercicio.dados_exercicio["afirmacoes"]
        respostas = []
        for i, afirmacao in enumerate(afirmacoes):
            resposta = st.radio(
                afirmacao,
                ["Verdadeiro", "Falso"],
                key=f"afirmacao_{i}_{exercicio.id}"
            )
            respostas.append(resposta == "Verdadeiro")
        return respostas

    elif exercicio.tipo == TipoExercicio.ORDENAR_PASSOS:
        passos = exercicio.dados_exercicio["passos"]
        st.write("Arraste para ordenar os passos:")
        ordem_atual = st.multiselect(
            "Ordene os passos (selecione em ordem):",
            options=range(len(passos)),
            format_func=lambda x: passos[x],
            default=list(range(len(passos))),
            key=f"ordem_{exercicio.id}"
        )
        return ordem_atual

    elif exercicio.tipo == TipoExercicio.COMPLEXIDADE_ANALISE:
        abordagens = exercicio.dados_exercicio["abordagens"]
        complexidades = exercicio.dados_exercicio["complexidades"]

        st.write("Associe cada abordagem à sua complexidade:")
        respostas = {}
        for i, abordagem in enumerate(abordagens):
            complexidade = st.selectbox(
                f"Complexidade de: {abordagem}",
                complexidades,
                key=f"complex_{i}_{exercicio.id}"
            )
            respostas[abordagem.lower().replace(' ', '_')] = complexidade
        return respostas

    elif exercicio.tipo == TipoExercicio.DEBUGGING:
        st.code(exercicio.dados_exercicio["codigo"], language="python")
        opcoes_bug = exercicio.dados_exercicio["opcoes_bug"]
        return st.radio(
            "Qual é o problema no código?",
            options=range(len(opcoes_bug)),
            format_func=lambda x: opcoes_bug[x],
            key=f"debug_{exercicio.id}"
        )

    return None

def render_feedback(feedback: Dict[str, Any], exercicio: Exercicio):
    """Renderiza o feedback da resposta"""

    if feedback["correta"]:
        st.success("🎉 **Correto!** Parabéns!")

        # Exibir explicação
        with st.expander("📖 Ver Explicação"):
            st.write(feedback["explicacao"])

        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tentativas", feedback["tentativas"])
        with col2:
            st.metric("Pontos", feedback["pontos"])
        with col3:
            tempo = st.session_state.sessao_atual.tempo_fim - st.session_state.sessao_atual.tempo_inicio
            st.metric("Tempo", ".1f")

        # Próximo exercício sugerido
        if st.button("🎯 Próximo Exercício", key=f"proximo_{exercicio.id}"):
            # Lógica para sugerir próximo exercício
            st.info("Funcionalidade de sugestão será implementada em breve!")

    else:
        st.error("❌ **Incorreto.** Tente novamente!")

        # Incrementar tentativa
        st.session_state.tentativa_atual = st.session_state.get('tentativa_atual', 1) + 1

        # Feedback específico baseado no tipo
        if exercicio.tipo == TipoExercicio.MULTIPLA_ESCOLHA:
            st.info("💡 Reveja as opções e considere a complexidade do algoritmo.")

        # Manter resposta submetida como False para permitir nova tentativa
        st.session_state.resposta_submetida = False

def render_exercicios_por_conceito():
    """Renderiza exercícios organizados por conceito"""

    st.markdown("### 🎯 Exercícios por Conceito")

    # Selecionar conceito
    conceitos_disponiveis = list(set(
        ex.conceito_relacionado for ex in sistema_exercicios.exercicios.values()
    ))

    conceito_selecionado = st.selectbox(
        "Selecione um conceito:",
        conceitos_disponiveis,
        key="conceito_exercicios"
    )

    if conceito_selecionado:
        exercicios_conceito = sistema_exercicios.obter_exercicios_por_conceito(conceito_selecionado)

        if not exercicios_conceito:
            st.warning(f"Nenhum exercício encontrado para o conceito '{conceito_selecionado}'.")
            return

        st.markdown(f"**Encontrados {len(exercicios_conceito)} exercícios para {conceito_selecionado}:**")

        for exercicio in exercicios_conceito:
            with st.expander(f"📝 {exercicio.titulo}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Dificuldade", exercicio.dificuldade.value.title())
                with col2:
                    st.metric("Tipo", exercicio.tipo.value.replace('_', ' ').title())
                with col3:
                    st.metric("Tempo", f"{exercicio.tempo_estimado}min")

                st.write(exercicio.descricao)
                st.write(f"**Enunciado:** {exercicio.enunciado}")

                if st.button(f"🚀 Praticar: {exercicio.titulo}", key=f"praticar_{exercicio.id}"):
                    # Armazenar exercício selecionado e mudar para aba de prática
                    st.session_state.exercicio_selecionado = exercicio
                    st.success(f"Exercício '{exercicio.titulo}' selecionado! Vá para a aba 'Praticar Exercícios'.")

def render_desempenho_usuario():
    """Renderiza estatísticas de desempenho do usuário"""

    st.markdown("### 📊 Meu Desempenho")

    # Calcular estatísticas
    stats = sistema_exercicios.calcular_estatisticas_usuario()

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Exercícios Concluídos",
            f"{stats['exercicios_concluidos']}/{stats['total_exercicios']}"
        )

    with col2:
        st.metric("Taxa de Conclusão", ".1f")

    with col3:
        st.metric("Pontos Totais", stats['pontos_totais'])

    with col4:
        st.metric("Tempo Total", ".1f")

    # Gráfico de desempenho por tipo
    st.markdown("#### 📈 Desempenho por Tipo de Exercício")

    tipos_stats = {}
    for sessao in sistema_exercicios.sessoes_ativas.values():
        if sessao.concluido:
            exercicio = sistema_exercicios.exercicios[sessao.exercicio_id]
            tipo = exercicio.tipo.value
            if tipo not in tipos_stats:
                tipos_stats[tipo] = {'concluidos': 0, 'total': 0}
            tipos_stats[tipo]['concluidos'] += 1
            tipos_stats[tipo]['total'] += 1

    # Adicionar tipos não tentados
    for tipo in TipoExercicio:
        if tipo.value not in tipos_stats:
            exercicios_tipo = [ex for ex in sistema_exercicios.exercicios.values() if ex.tipo == tipo]
            tipos_stats[tipo.value] = {'concluidos': 0, 'total': len(exercicios_tipo)}

    # Criar dados para gráfico
    tipos_nomes = list(tipos_stats.keys())
    taxas_conclusao = [
        (stats['concluidos'] / stats['total'] * 100) if stats['total'] > 0 else 0
        for stats in tipos_stats.values()
    ]

    import plotly.express as px
    fig = px.bar(
        x=tipos_nomes,
        y=taxas_conclusao,
        title="Taxa de Conclusão por Tipo (%)",
        labels={'x': 'Tipo de Exercício', 'y': 'Taxa de Conclusão (%)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def render_conquistas():
    """Renderiza sistema de conquistas e badges"""

    st.markdown("### 🏆 Conquistas e Badges")

    # Definir conquistas
    conquistas = [
        {
            "titulo": "Primeiros Passos",
            "descricao": "Complete seu primeiro exercício",
            "icone": "🎯",
            "condicao": lambda: len([s for s in sistema_exercicios.sessoes_ativas.values() if s.concluido]) >= 1
        },
        {
            "titulo": "Persistente",
            "descricao": "Tente um exercício pelo menos 3 vezes",
            "icone": "💪",
            "condicao": lambda: any(s.tentativas >= 3 for s in sistema_exercicios.sessoes_ativas.values())
        },
        {
            "titulo": "Perfeccionista",
            "descricao": "Acerte um exercício na primeira tentativa",
            "icone": "⭐",
            "condicao": lambda: any(s.tentativas == 1 and s.concluido for s in sistema_exercicios.sessoes_ativas.values())
        },
        {
            "titulo": "Explorador",
            "descricao": "Pratique exercícios de 3 tipos diferentes",
            "icone": "🗺️",
            "condicao": lambda: len(set(
                sistema_exercicios.exercicios[s.exercicio_id].tipo
                for s in sistema_exercicios.sessoes_ativas.values() if s.concluido
            )) >= 3
        }
    ]

    # Verificar conquistas desbloqueadas
    conquistas_desbloqueadas = []
    conquistas_bloqueadas = []

    for conquista in conquistas:
        if conquista["condicao"]():
            conquistas_desbloqueadas.append(conquista)
        else:
            conquistas_bloqueadas.append(conquista)

    # Exibir conquistas desbloqueadas
    if conquistas_desbloqueadas:
        st.markdown("#### ✅ Conquistas Desbloqueadas")
        for conquista in conquistas_desbloqueadas:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"# {conquista['icone']}")
            with col2:
                st.markdown(f"**{conquista['titulo']}**")
                st.write(conquista['descricao'])

    # Exibir conquistas bloqueadas
    if conquistas_bloqueadas:
        st.markdown("#### 🔒 Conquistas Disponíveis")
        for conquista in conquistas_bloqueadas:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"# ⚫")
            with col2:
                st.markdown(f"**{conquista['titulo']}**")
                st.write(conquista['descricao'])
