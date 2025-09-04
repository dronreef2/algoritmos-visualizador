# Teste simplificado do aplicativo Streamlit
import streamlit as st
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append('.')

st.title("🧪 Teste Simplificado - Algoritmos Visualizador")

st.markdown("### 📊 Status do Sistema")

# Verificar se os módulos podem ser importados
status_modulos = {}

try:
    import modulos_integrados
    status_modulos["modulos_integrados"] = "✅ OK"
except Exception as e:
    status_modulos["modulos_integrados"] = f"❌ Erro: {e}"

try:
    from modulos_integrados import modulos_integrados
    status_modulos["instancia_modulos"] = "✅ OK"
except Exception as e:
    status_modulos["instancia_modulos"] = f"❌ Erro: {e}"

# Verificar módulos individuais
modulos_para_testar = [
    ("modulo_1_fundamentos", "busca_binaria.py"),
    ("modulo_2_estruturas_dados", "algoritmos_ordenacao.py"),
    ("modulo_3_programacao_dinamica", "metodologia_3_passos.py"),
    ("modulo_4_entrevistas", "interview_visualizer.py")
]

for pasta, arquivo in modulos_para_testar:
    try:
        caminho = os.path.join(pasta, arquivo)
        if os.path.exists(caminho):
            status_modulos[f"{pasta}/{arquivo}"] = "✅ Existe"
        else:
            status_modulos[f"{pasta}/{arquivo}"] = "❌ Não encontrado"
    except Exception as e:
        status_modulos[f"{pasta}/{arquivo}"] = f"❌ Erro: {e}"

# Exibir status
for modulo, status in status_modulos.items():
    st.write(f"**{modulo}:** {status}")

st.markdown("### 🎯 Módulos Disponíveis")

# Sidebar simples
st.sidebar.title("📚 Módulos")

modulos = [
    "🎯 Módulo 1: Fundamentos",
    "📊 Módulo 2: Estruturas de Dados",
    "🧮 Módulo 3: Programação Dinâmica",
    "🎤 Módulo 4: Entrevistas"
]

for i, modulo in enumerate(modulos):
    if st.sidebar.button(modulo, key=f"modulo_{i}"):
        st.session_state.selected_module = i
        st.success(f"✅ Módulo {i+1} selecionado!")

# Conteúdo principal baseado na seleção
if 'selected_module' in st.session_state:
    modulo_id = st.session_state.selected_module

    st.header(f"Módulo {modulo_id + 1}")

    # Tentar carregar conteúdo usando modulos_integrados
    if 'modulos_integrados' in globals():
        try:
            conteudo = modulos_integrados.carregar_conteudo_modulo(modulo_id)

            if "erro" in conteudo:
                st.error(conteudo["erro"])
            else:
                st.success("✅ Conteúdo carregado com sucesso!")

                # Exibir estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📄 Arquivos", conteudo["estatisticas"]["total_arquivos"])
                with col2:
                    st.metric("📝 Linhas", conteudo["estatisticas"]["total_linhas"])
                with col3:
                    st.metric("🎯 Algoritmos", len(conteudo["estatisticas"]["algoritmos_principais"]))

                # Lista de algoritmos
                st.markdown("### 🎯 Algoritmos Principais")
                for algoritmo in conteudo["estatisticas"]["algoritmos_principais"]:
                    st.write(f"• {algoritmo}")

        except Exception as e:
            st.error(f"Erro ao carregar módulo: {e}")
    else:
        st.warning("Sistema de módulos não disponível")

st.markdown("---")
st.markdown("**💡 Teste simplificado para verificar funcionamento básico**")
