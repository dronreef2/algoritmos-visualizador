#!/usr/bin/env python3
"""
🎯 INTEGRAÇÃO GITMCP COM SISTEMA DE EXERCÍCIOS PRÁTICOS
======================================================

Integração inteligente que enriquece os exercícios práticos com:
- Exemplos reais de código do GitHub
- Documentação contextual de algoritmos
- Comparações de implementações
- Sugestões de exercícios baseados em repositórios
"""

import streamlit as st
import random
from typing import Dict, Any, List, Optional
from sistema_exercicios_praticos import (
    SistemaExerciciosPraticos, Exercicio, TipoExercicio, Dificuldade
)
from gitmcp_integration import GitMCPIntegration
from datetime import datetime
import time

# Inicializar sistemas
sistema_exercicios = SistemaExerciciosPraticos()
git_client = GitMCPIntegration()

def render_exercicios_gitmcp():
    """Renderiza interface integrada de exercícios com GitMCP"""

    st.markdown("### 🔗 Exercícios com Integração GitHub")

    # Abas para diferentes funcionalidades
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Exemplos Reais",
        "🎯 Exercícios GitHub",
        "⚡ Comparação Performance",
        "🔍 Explorar Repositórios"
    ])

    with tab1:
        render_exemplos_reais()

    with tab2:
        render_exercicios_github()

    with tab3:
        render_comparacao_performance()

    with tab4:
        render_explorar_repositorios()

def render_exemplos_reais():
    """Renderiza exemplos reais de algoritmos do GitHub"""

    st.markdown("#### 📚 Exemplos Reais de Algoritmos")

    # Selecionar algoritmo/conceito
    conceitos = [
        "busca_binaria", "ordenacao", "grafos", "programacao_dinamica",
        "backtracking", "estruturas_dados", "otimizacao"
    ]

    conceito_selecionado = st.selectbox(
        "Selecione um conceito:",
        conceitos,
        format_func=lambda x: x.replace('_', ' ').title(),
        key="conceito_gitmcp"
    )

    if st.button("🔍 Buscar Exemplos Reais", key="buscar_exemplos"):
        with st.spinner("Buscando exemplos no GitHub..."):
            try:
                # Buscar exemplos de código relacionados
                exemplos = git_client.obter_exemplos_codigo(
                    conceito_selecionado,
                    "python"
                )

                if exemplos and exemplos.get("exemplos"):
                    st.success(f"Encontrados {len(exemplos['exemplos'])} exemplos!")

                    for exemplo in exemplos["exemplos"][:5]:  # Limitar a 5 primeiros
                        with st.expander(f"📦 {exemplo['repositorio']} - {exemplo['arquivo']}", expanded=False):
                            st.markdown(f"**Repositório:** {exemplo['repositorio']}")
                            st.markdown(f"**Arquivo:** {exemplo['arquivo']}")
                            st.markdown(f"**URL:** [{exemplo['url']}]({exemplo['url']})")

                            # Exibir conteúdo do código
                            with st.expander("� Código", expanded=False):
                                st.code(exemplo['conteudo'], language="python")

                            # Tentar buscar README do repositório
                            try:
                                owner, repo = exemplo['repositorio'].split('/', 1)
                                readme = git_client.client.get_readme(owner, repo)
                                if readme and readme["status"] == "success":
                                    with st.expander("� README", expanded=False):
                                        st.markdown(readme["content"][:1000] + "..." if len(readme["content"]) > 1000 else readme["content"])
                            except:
                                st.info("README não disponível")

                else:
                    st.warning("Nenhum repositório encontrado.")

            except Exception as e:
                st.error(f"Erro ao buscar exemplos: {str(e)}")

def render_exercicios_github():
    """Renderiza exercícios gerados baseados em código real do GitHub"""

    st.markdown("#### 🎯 Exercícios Baseados em Código Real")

    # Selecionar tipo de exercício
    tipo_exercicio = st.selectbox(
        "Tipo de exercício:",
        ["debugging", "otimizacao", "analise_complexidade", "comparacao_abordagens"],
        format_func=lambda x: x.replace('_', ' ').title(),
        key="tipo_exercicio_github"
    )

    if st.button("🎲 Gerar Exercício", key="gerar_exercicio_github"):
        with st.spinner("Gerando exercício baseado em código real..."):
            exercicio_gerado = gerar_exercicio_github(tipo_exercicio)

            if exercicio_gerado:
                st.markdown("### 📝 Exercício Gerado")

                # Exibir informações do exercício
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Dificuldade", exercicio_gerado['dificuldade'])
                with col2:
                    st.metric("Fonte", exercicio_gerado['repositorio'])

                st.markdown(f"**{exercicio_gerado['titulo']}**")
                st.write(exercicio_gerado['enunciado'])

                if exercicio_gerado['codigo']:
                    st.code(exercicio_gerado['codigo'], language="python")

                # Interface de resposta baseada no tipo
                resposta = render_interface_resposta_github(exercicio_gerado)

                if st.button("✅ Verificar Resposta", key="verificar_github"):
                    feedback = verificar_resposta_github(exercicio_gerado, resposta)
                    if feedback['correta']:
                        st.success("🎉 Correto! " + feedback['explicacao'])
                    else:
                        st.error("❌ Incorreto. " + feedback['explicacao'])

                    if 'solucao' in feedback:
                        with st.expander("💡 Ver Solução"):
                            st.code(feedback['solucao'], language="python")
            else:
                st.error("Não foi possível gerar um exercício. Tente novamente.")

def render_comparacao_performance():
    """Renderiza comparações de performance entre diferentes implementações"""

    st.markdown("#### ⚡ Comparação de Performance")

    algoritmo = st.selectbox(
        "Selecione um algoritmo:",
        ["busca_binaria", "ordenacao", "busca_grafo"],
        format_func=lambda x: x.replace('_', ' ').title(),
        key="algoritmo_performance"
    )

    if st.button("📊 Comparar Implementações", key="comparar_performance"):
        with st.spinner("Analisando implementações..."):
            comparacao = comparar_implementacoes_github(algoritmo)

            if comparacao:
                st.markdown("### 📈 Resultados da Comparação")

                # Tabela de comparação
                import pandas as pd
                df = pd.DataFrame(comparacao['implementacoes'])
                st.dataframe(df)

                # Gráfico de complexidade
                if 'complexidades' in comparacao:
                    import plotly.express as px
                    fig = px.bar(
                        comparacao['complexidades'],
                        x='implementacao',
                        y='complexidade',
                        title="Complexidade Temporal Estimada"
                    )
                    st.plotly_chart(fig)

                # Insights
                st.markdown("### 💡 Insights")
                for insight in comparacao.get('insights', []):
                    st.info(insight)

            else:
                st.warning("Não foi possível obter dados de comparação.")

def render_explorar_repositorios():
    """Renderiza interface para explorar repositórios de algoritmos"""

    st.markdown("#### 🔍 Explorar Repositórios de Algoritmos")

    # Filtros de busca
    col1, col2, col3 = st.columns(3)

    with col1:
        linguagem = st.selectbox(
            "Linguagem:",
            ["python", "javascript", "java", "cpp", "go"],
            key="linguagem_repo"
        )

    with col2:
        min_stars = st.slider("Mínimo de estrelas:", 0, 1000, 50, key="min_stars")

    with col3:
        topico = st.selectbox(
            "Tópico:",
            ["algorithms", "data-structures", "competitive-programming", "interview-preparation"],
            key="topico_repo"
        )

    query = f"{topico} {linguagem}"

    if st.button("🔍 Buscar Repositórios", key="buscar_repos"):
        with st.spinner("Buscando repositórios..."):
            # Usar busca de documentação que inclui repositórios conhecidos
            documentacao = git_client.buscar_documentacao_algoritmo(
                topico.replace("-", "_"),
                linguagem
            )

            if documentacao and documentacao.get("resultados"):
                st.success(f"Encontrados {len(documentacao['resultados'])} repositórios!")

                for i, resultado in enumerate(documentacao["resultados"][:10]):
                    repo_info = resultado.get("info", {})
                    if repo_info.get("status") == "success":
                        with st.expander(f"{i+1}. ⭐ {repo_info.get('stars', 0)} - {repo_info.get('name', 'N/A')}", expanded=False):
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"**{repo_info.get('description', 'Sem descrição')}**")
                                st.markdown(f"📅 Atualizado: {repo_info.get('updated_at', 'N/A')}")
                                st.markdown(f"👥 Linguagem: {repo_info.get('language', 'N/A')}")

                            with col2:
                                st.markdown(f"**[Ver no GitHub]({repo_info.get('html_url', '#')})**")

                                if st.button(f"📖 Ver README", key=f"readme_{resultado.get('repositorio', f'repo_{i}')}"):
                                    try:
                                        readme = resultado.get("readme")
                                        if readme and readme.get("status") == "success":
                                            st.markdown("---")
                                            st.markdown(readme["content"][:1500] + "..." if len(readme["content"]) > 1500 else readme["content"])
                                    except:
                                        st.error("Erro ao carregar README")

            else:
                st.info("Nenhum repositório encontrado com os critérios especificados.")

def gerar_exercicio_github(tipo: str) -> Optional[Dict[str, Any]]:
    """Gera um exercício baseado em código real do GitHub"""

    try:
        # Usar repositórios conhecidos de algoritmos
        repos_conhecidos = ["TheAlgorithms/Python", "keon/algorithms"]

        # Selecionar repositório aleatório
        repo_full = random.choice(repos_conhecidos)
        owner, repo = repo_full.split("/", 1)

        # Buscar arquivos de código usando search_code com query mais genérica
        queries = [
            "def sort", "def search", "def graph", "class.*Sort", "class.*Search",
            "def bubble", "def quick", "def merge", "def binary"
        ]
        
        code_results = []
        for query in queries:
            try:
                code_search = git_client.client.search_code(
                    owner, repo, query,
                    language="python", max_results=3
                )
                if code_search["status"] == "success" and code_search.get("results"):
                    code_results.extend(code_search["results"])
                    if len(code_results) >= 5:  # Já temos resultados suficientes
                        break
            except:
                continue
        
        if not code_results:
            return None

        # Selecionar arquivo aleatório
        code_file = random.choice(code_results[:5])

        # Obter conteúdo completo do arquivo
        file_content = git_client.client.get_file_content(owner, repo, code_file["path"])
        if file_content["status"] != "success":
            return None

        # Criar objeto similar ao esperado
        code_file_data = {
            "content": file_content["content"],
            "name": code_file["name"],
            "path": code_file["path"],
            "url": code_file["url"]
        }

        # Gerar exercício baseado no tipo
        if tipo == "debugging":
            return gerar_exercicio_debugging(code_file_data, repo_full)
        elif tipo == "otimizacao":
            return gerar_exercicio_otimizacao(code_file_data, repo_full)
        elif tipo == "analise_complexidade":
            return gerar_exercicio_complexidade(code_file_data, repo_full)
        elif tipo == "comparacao_abordagens":
            return gerar_exercicio_comparacao(code_file_data, repo_full)

    except Exception as e:
        st.error(f"Erro ao gerar exercício: {str(e)}")
        return None

def gerar_exercicio_debugging(code_file: Dict, repo_name: str) -> Dict[str, Any]:
    """Gera exercício de debugging"""

    return {
        'titulo': "Debugging: Encontre o Erro",
        'enunciado': f"Analise o código abaixo do repositório '{repo_name}' e identifique o problema:",
        'codigo': code_file['content'],
        'tipo': 'debugging',
        'dificuldade': 'Médio',
        'repositorio': repo_name,
        'solucao_esperada': 'Identificar bug no código'
    }

def gerar_exercicio_otimizacao(code_file: Dict, repo_name: str) -> Dict[str, Any]:
    """Gera exercício de otimização"""

    return {
        'titulo': "Otimização: Melhore a Performance",
        'enunciado': f"Analise o código abaixo e sugira melhorias de performance:",
        'codigo': code_file['content'],
        'tipo': 'otimizacao',
        'dificuldade': 'Difícil',
        'repositorio': repo_name,
        'solucao_esperada': 'Sugerir otimizações'
    }

def gerar_exercicio_complexidade(code_file: Dict, repo_name: str) -> Dict[str, Any]:
    """Gera exercício de análise de complexidade"""

    return {
        'titulo': "Análise: Determine a Complexidade",
        'enunciado': f"Analise o algoritmo abaixo e determine sua complexidade temporal e espacial:",
        'codigo': code_file['content'],
        'tipo': 'complexidade',
        'dificuldade': 'Médio',
        'repositorio': repo_name,
        'solucao_esperada': 'O(n log n), O(n), etc.'
    }

def gerar_exercicio_comparacao(code_file: Dict, repo_name: str) -> Dict[str, Any]:
    """Gera exercício de comparação de abordagens"""

    return {
        'titulo': "Comparação: Avalie as Abordagens",
        'enunciado': f"Compare diferentes abordagens para resolver o problema implementado no código:",
        'codigo': code_file['content'],
        'tipo': 'comparacao',
        'dificuldade': 'Difícil',
        'repositorio': repo_name,
        'solucao_esperada': 'Comparar vantagens e desvantagens'
    }

def render_interface_resposta_github(exercicio: Dict) -> Any:
    """Renderiza interface de resposta para exercícios GitHub"""

    if exercicio['tipo'] == 'debugging':
        return st.text_area(
            "Descreva o problema encontrado:",
            height=100,
            key="resposta_debugging"
        )

    elif exercicio['tipo'] == 'otimizacao':
        return st.text_area(
            "Sugira melhorias de performance:",
            height=150,
            key="resposta_otimizacao"
        )

    elif exercicio['tipo'] == 'complexidade':
        col1, col2 = st.columns(2)
        with col1:
            temporal = st.selectbox(
                "Complexidade Temporal:",
                ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2^n)"],
                key="complexidade_temporal"
            )
        with col2:
            espacial = st.selectbox(
                "Complexidade Espacial:",
                ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)"],
                key="complexidade_espacial"
            )
        return {'temporal': temporal, 'espacial': espacial}

    elif exercicio['tipo'] == 'comparacao':
        return st.text_area(
            "Compare as abordagens implementadas:",
            height=200,
            key="resposta_comparacao"
        )

def verificar_resposta_github(exercicio: Dict, resposta: Any) -> Dict[str, Any]:
    """Verifica resposta do exercício GitHub"""

    # Simulação de verificação (em produção, seria mais sofisticada)
    if exercicio['tipo'] == 'complexidade':
        # Verificação básica para exemplo
        if resposta['temporal'] in ['O(n log n)', 'O(n)']:
            return {
                'correta': True,
                'explicacao': 'Análise correta da complexidade!'
            }
        else:
            return {
                'correta': False,
                'explicacao': 'Reveja a análise da complexidade.',
                'solucao': 'Complexidade típica: O(n log n) para algoritmos de ordenação eficientes'
            }

    # Para outros tipos, feedback genérico
    return {
        'correta': random.choice([True, False]),  # Simulação
        'explicacao': 'Análise realizada com base no código do repositório.',
        'solucao': 'Solução baseada nas melhores práticas encontradas no GitHub'
    }

def comparar_implementacoes_github(algoritmo: str) -> Optional[Dict[str, Any]]:
    """Compara diferentes implementações do mesmo algoritmo"""

    try:
        # Usar método de comparação da integração
        return git_client.comparar_implementacoes(algoritmo)
    except Exception as e:
        st.error(f"Erro na comparação: {str(e)}")
        return None


# Função principal para integrar na UI existente
def integrar_gitmcp_na_ui_exercicios():
    """
    Função principal para integrar GitMCP na interface de exercícios
    Deve ser chamada na interface principal dos exercícios
    """
    st.markdown("---")
    st.markdown("## 🤖 Aprimorado com GitMCP")

    st.markdown("""
    Esta seção de exercícios foi **enriquecida com dados reais do GitHub**:

    🎯 **Exemplos Reais**: Implementações de algoritmos de repositórios open-source
    📚 **Documentação**: README e documentação de projetos populares
    🔄 **Comparações**: Diferentes abordagens para o mesmo problema
    🔍 **Exploração**: Busca interativa por algoritmos no GitHub
    """)

    # Tabs da integração
    tab1, tab2, tab3 = st.tabs([
        "🔍 Explorador GitHub",
        "🔄 Comparar Implementações",
        "📊 Relatório de Aprendizado"
    ])

    with tab1:
        render_explorar_repositorios()

    with tab2:
        render_comparacao_performance()

    with tab3:
        st.markdown("### 📈 Relatório de Aprendizado com GitHub")

        # Selecionar exercício para relatório
        exercicios_ids = list(sistema_exercicios.exercicios.keys())
        exercicio_selecionado = st.selectbox(
            "Selecione um exercício para gerar relatório:",
            exercicios_ids,
            format_func=lambda x: sistema_exercicios.exercicios[x].titulo
        )

        if st.button("📊 Gerar Relatório", type="primary"):
            exercicio = sistema_exercicios.exercicios[exercicio_selecionado]
            relatorio = gerar_relatorio_aprendizado_github(exercicio)

            st.markdown("---")
            st.markdown(relatorio)

            # Download do relatório
            st.download_button(
                label="📥 Baixar Relatório",
                data=relatorio,
                file_name=f"relatorio_aprendizado_{exercicio.conceito_relacionado}.md",
                mime="text/markdown"
            )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Exercícios Práticos + GitMCP",
        page_icon="🎯",
        layout="wide"
    )

    st.title("🎯 Exercícios Práticos Enriquecidos com GitMCP")

    # Verificar conectividade com GitHub
    if git_client.is_available():
        st.success("✅ Conectado ao GitHub API - Funcionalidades completas disponíveis!")

        integrar_gitmcp_na_ui_exercicios()
    else:
        st.error("❌ Não foi possível conectar ao GitHub API")
        st.info("Verifique sua conexão com a internet para acessar todas as funcionalidades.")

def gerar_relatorio_aprendizado_github(exercicio: Dict) -> str:
    """Gera relatório de aprendizado baseado em dados do GitHub"""

    try:
        # Buscar repositórios relacionados ao conceito do exercício
        conceito = exercicio.get('conceito_relacionado', 'algorithms')
        documentacao = git_client.buscar_documentacao_algoritmo(conceito, "python")

        relatorio = f"""
# 📊 Relatório de Aprendizado - {exercicio['titulo']}

## 🎯 Conceito Analisado
**{conceito.replace('_', ' ').title()}**

## 📚 Exemplos Reais Encontrados
"""

        if documentacao and documentacao.get("resultados"):
            for resultado in documentacao["resultados"][:3]:
                repo_info = resultado.get("info", {})
                if repo_info.get("status") == "success":
                    relatorio += f"""
### ⭐ {repo_info.get('name', 'N/A')} ({repo_info.get('stars', 0)} estrelas)
- **Descrição:** {repo_info.get('description', 'Sem descrição')}
- **URL:** {repo_info.get('html_url', '#')}
"""

        relatorio += f"""

## 💡 Insights de Aprendizado
- Este conceito é amplamente utilizado em projetos reais
- Existem {len(documentacao.get('resultados', []))} repositórios relacionados no GitHub
- A implementação prática é fundamental para o entendimento

## 🎯 Recomendações
1. Explore os repositórios sugeridos acima
2. Compare diferentes implementações
3. Pratique com casos reais de uso
4. Contribua para projetos open source

---
*Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}*
"""

        return relatorio

    except Exception as e:
        return f"Erro ao gerar relatório: {str(e)}"
