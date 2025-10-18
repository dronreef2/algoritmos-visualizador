#!/usr/bin/env python3
"""
Versão simplificada do aplicativo Streamlit para testar módulos
"""

import streamlit as st
import sys
import os

sys.path.append("/workspaces/algoritmos-visualizador")

# Configuração básica
st.set_page_config(page_title="Teste Módulos", page_icon="🧪", layout="wide")

st.title("🧪 Teste dos Módulos Educacionais")

# Testar importação
try:
    from modulos_integrados import modulos_integrados

    st.success("✅ Módulos integrados importados com sucesso!")

    # Testar carregamento de módulos
    tab1, tab2, tab3, tab4 = st.tabs(["Módulo 1", "Módulo 2", "Módulo 3", "Módulo 4"])

    for i, tab in enumerate([tab1, tab2, tab3, tab4]):
        with tab:
            st.header(f"Módulo {i+1}")

            if st.button(f"Carregar Módulo {i+1}", key=f"load_{i}"):
                with st.spinner(f"Carregando módulo {i+1}..."):
                    conteudo = modulos_integrados.carregar_conteudo_modulo(i)

                    if "erro" in conteudo:
                        st.error(f"Erro: {conteudo['erro']}")
                    else:
                        st.success(f"✅ Módulo {i+1} carregado!")

                        # Estatísticas
                        stats = conteudo.get("estatisticas", {})
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Arquivos", stats.get("total_arquivos", 0))
                        with col2:
                            st.metric("Linhas", stats.get("total_linhas", 0))
                        with col3:
                            st.metric("Algoritmos", len(stats.get("algoritmos_principais", [])))

                        # Lista de arquivos (limitada)
                        arquivos = conteudo.get("arquivos", {})
                        st.subheader("📄 Arquivos Disponíveis")

                        for j, (nome_arquivo, info) in enumerate(list(arquivos.items())[:3]):  # Apenas 3 primeiros
                            with st.expander(f"📄 {nome_arquivo}", expanded=False):
                                if "erro" in info:
                                    st.error(f"Erro: {info['erro']}")
                                else:
                                    # Preview limitado
                                    conteudo_arquivo = info.get("conteudo", "")
                                    linhas = conteudo_arquivo.split("\n")[:5]  # Apenas 5 primeiras linhas
                                    preview = "\n".join(linhas)
                                    st.code(preview, language="python")

                                    if len(conteudo_arquivo) > 1000:
                                        st.info(f"Arquivo tem {len(conteudo_arquivo)} caracteres. Preview limitado.")

except ImportError as e:
    st.error(f"❌ Erro de importação: {e}")

except Exception as e:
    st.error(f"❌ Erro geral: {e}")

st.markdown("---")
st.markdown("**Status:** Teste simplificado dos módulos educacionais")
