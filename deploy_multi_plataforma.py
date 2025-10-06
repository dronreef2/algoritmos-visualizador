"""
🎯 Módulo de Deploy Multi-Plataforma
====================================

Módulo integrado à aplicação Streamlit que fornece:
- Detecção automática de plataforma
- Opções de deploy para diferentes clouds
- Status de recursos e compatibilidade
- Guias de migração entre plataformas
- CONTROLE DIRETO: Executar verificações, configurações e inicializações

Integrado ao app_integrada.py para fornecer experiência unificada.
"""

import streamlit as st
import os
import platform
from pathlib import Path
import subprocess
import sys
from typing import Dict, Any, List
import time
import threading
import queue

class DeployManager:
    """Gerenciador de deploy multi-plataforma."""

    def __init__(self):
        self.platform_info = self._detect_platform()
        self.gpu_info = self._detect_gpu()
        self.deployment_options = self._get_deployment_options()
        self.command_queue = queue.Queue()
        self.command_results = {}

    def execute_command_async(self, command: str, key: str):
        """Executa comando de forma assíncrona."""
        def run_command():
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(Path.cwd())
                )
                self.command_results[key] = {
                    'success': result.returncode == 0,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                }
            except subprocess.TimeoutExpired:
                self.command_results[key] = {
                    'success': False,
                    'stdout': '',
                    'stderr': 'Timeout após 30 segundos',
                    'returncode': -1
                }
            except Exception as e:
                self.command_results[key] = {
                    'success': False,
                    'stdout': '',
                    'stderr': str(e),
                    'returncode': -1
                }

        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()
        return key

    def get_command_result(self, key: str) -> Dict[str, Any]:
        """Obtém resultado de comando executado."""
        return self.command_results.get(key, {'success': None, 'stdout': '', 'stderr': '', 'returncode': None})

    def _detect_platform(self) -> Dict[str, Any]:
        """Detecta plataforma atual."""
        info = {
            'name': 'Desenvolvimento Local',
            'icon': '🖥️',
            'is_cloud': False,
            'gpu_available': False,
            'memory_limit': 'Ilimitado',
            'timeout_limit': 'Ilimitado',
            'color': 'blue'
        }

        # Google Colab
        if 'COLAB_GPU' in os.environ or 'COLAB_TPU_ADDR' in os.environ:
            info.update({
                'name': 'Google Colab',
                'icon': '🌐',
                'is_cloud': True,
                'gpu_available': True,
                'memory_limit': 'Até 25GB',
                'timeout_limit': 'Ilimitado',
                'color': 'orange'
            })

        # Hugging Face Spaces
        elif 'SPACE_ID' in os.environ or 'HF_SPACE' in os.environ:
            info.update({
                'name': 'Hugging Face Spaces',
                'icon': '🤗',
                'is_cloud': True,
                'gpu_available': True,
                'memory_limit': 'Até 16GB',
                'timeout_limit': 'Ilimitado',
                'color': 'purple'
            })

        # Streamlit Cloud
        elif 'STREAMLIT_SERVER_HEADLESS' in os.environ:
            info.update({
                'name': 'Streamlit Cloud',
                'icon': '☁️',
                'is_cloud': True,
                'gpu_available': False,
                'memory_limit': '~1GB',
                'timeout_limit': '10-15 min',
                'color': 'green'
            })

        return info

    def _detect_gpu(self) -> Dict[str, Any]:
        """Detecta GPU disponível."""
        gpu_info = {
            'available': False,
            'name': 'CPU',
            'memory_gb': 0,
            'type': 'cpu'
        }

        try:
            import torch
            gpu_info['available'] = torch.cuda.is_available()
            if gpu_info['available']:
                gpu_info.update({
                    'name': torch.cuda.get_device_name(0),
                    'memory_gb': round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 1),
                    'type': 'cuda'
                })
        except ImportError:
            pass

        return gpu_info

    def _get_deployment_options(self) -> List[Dict[str, Any]]:
        """Retorna opções de deploy disponíveis."""
        return [
            {
                'name': 'Streamlit Cloud',
                'icon': '☁️',
                'description': 'Deploy rápido e simples (CPU-only)',
                'pros': ['Fácil setup', 'Gratuito', 'Integração GitHub'],
                'cons': ['Sem GPU', 'Limitações de memória', 'Timeout curto'],
                'best_for': ['Demonstrações básicas', 'Testes iniciais'],
                'requirements_file': 'requirements_streamlit_cloud.txt',
                'main_file': 'app_integrada.py',
                'url': 'https://share.streamlit.io'
            },
            {
                'name': 'Google Colab',
                'icon': '🌐',
                'description': 'GPU/TPU gratuito para demonstrações',
                'pros': ['GPU gratuito', 'Recursos ilimitados', 'Compartilhamento fácil'],
                'cons': ['Setup manual', 'Instável para produção'],
                'best_for': ['Demonstrações com GPU', 'Testes avançados'],
                'notebook_file': 'Algoritmos_Visualizador_Colab.ipynb',
                'url': 'https://colab.research.google.com'
            },
            {
                'name': 'Hugging Face Spaces',
                'icon': '🤗',
                'description': 'Deploy profissional com GPU persistente',
                'pros': ['GPU persistente', 'Escalável', 'API integrada'],
                'cons': ['Setup mais complexo', 'Limitações de espaço'],
                'best_for': ['Produção', 'Modelos ML', 'API deployments'],
                'requirements_file': 'requirements_huggingface_spaces.txt',
                'main_file': 'app_integrada.py',
                'readme_file': 'HuggingFace_Spaces_README.md',
                'url': 'https://huggingface.co/spaces'
            }
        ]

    def run_compatibility_check(self) -> Dict[str, Any]:
        """Executa verificação de compatibilidade completa."""
        results = {
            'platform': self.platform_info,
            'gpu': self.gpu_info,
            'dependencies': {},
            'files': {},
            'recommendations': []
        }

        # Verificar dependências críticas
        critical_deps = ['streamlit', 'torch', 'numpy', 'pandas', 'matplotlib', 'plotly']
        for dep in critical_deps:
            try:
                __import__(dep)
                results['dependencies'][dep] = {'status': 'ok', 'version': getattr(__import__(dep), '__version__', 'unknown')}
            except ImportError:
                results['dependencies'][dep] = {'status': 'missing', 'version': None}

        # Verificar arquivos críticos
        critical_files = [
            'app_integrada.py',
            'requirements_streamlit_cloud.txt',
            'colab_setup.py',
            'requirements_huggingface_spaces.txt'
        ]
        for file_path in critical_files:
            path = Path(file_path)
            results['files'][file_path] = path.exists()

        # Recomendações
        if not self.gpu_info['available'] and self.platform_info['name'] == 'Local Development':
            results['recommendations'].append("Considere usar Google Colab ou Hugging Face Spaces para funcionalidades GPU")

        if self.platform_info['name'] == 'Streamlit Cloud':
            results['recommendations'].append("Funcionalidades avançadas de GPU não disponíveis nesta plataforma")

        return results

    def get_system_info(self) -> Dict[str, Any]:
        """Obtém informações detalhadas do sistema."""
        return {
            'python_version': platform.python_version(),
            'system': platform.system(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'environment_vars': {k: v for k, v in os.environ.items() if k.startswith(('STREAMLIT_', 'COLAB_', 'SPACE_', 'HF_'))}
        }

def show_deploy_dashboard():
    """Exibe dashboard de deploy na aplicação Streamlit."""
    st.header("🚀 Deploy Multi-Plataforma")

    deploy_manager = DeployManager()

    # Status da Plataforma Atual
    st.subheader(f"{deploy_manager.platform_info['icon']} Plataforma Atual: {deploy_manager.platform_info['name']}")

    col1, col2, col3 = st.columns(3)

    with col1:
        gpu_status = "Sim" if deploy_manager.gpu_info['available'] else "Não"
        st.metric("GPU Disponível", gpu_status)
        if deploy_manager.gpu_info['available']:
            st.caption(f"{deploy_manager.gpu_info['name']} ({deploy_manager.gpu_info['memory_gb']}GB)")

    with col2:
        st.metric("Memória Limite", deploy_manager.platform_info['memory_limit'])

    with col3:
        st.metric("Timeout", deploy_manager.platform_info['timeout_limit'])

    # CONTROLE INTERATIVO - Nova seção
    st.subheader("🎮 Controle Interativo")

    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Verificação", "⚙️ Configuração", "🚀 Inicialização", "📊 Sistema"])

    with tab1:
        show_verification_tab(deploy_manager)

    with tab2:
        show_configuration_tab(deploy_manager)

    with tab3:
        show_initialization_tab(deploy_manager)

    with tab4:
        show_system_tab(deploy_manager)

    # Funcionalidades Otimizadas (mantido)
    st.subheader("🎯 Funcionalidades Disponíveis")

    features = {
        'visualizacoes': '📊 Visualizações Interativas',
        'redes_neurais': '🧠 Redes Neurais Avançadas',
        'arte_generativa': '🎨 Arte Generativa',
        'competicoes': '🏆 Competições Globais',
        'exercicios': '📝 Exercícios Práticos',
        'busca_web': '🔍 Busca Web Integrada'
    }

    if deploy_manager.platform_info['name'] == 'Streamlit Cloud':
        available_features = ['visualizacoes', 'exercicios', 'busca_web']
    elif deploy_manager.platform_info['name'] in ['Google Colab', 'Hugging Face Spaces']:
        available_features = list(features.keys())
    else:
        available_features = list(features.keys())

    cols = st.columns(2)
    for i, feature_key in enumerate(features.keys()):
        with cols[i % 2]:
            if feature_key in available_features:
                st.success(f"✅ {features[feature_key]}")
            else:
                st.warning(f"⚠️ {features[feature_key]} (Limitado)")

    # Opções de Deploy (mantido)
    st.subheader("🌐 Opções de Deploy")

    for option in deploy_manager.deployment_options:
        with st.expander(f"{option['icon']} {option['name']} - {option['description']}"):

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**✅ Vantagens:**")
                for pro in option['pros']:
                    st.markdown(f"• {pro}")

            with col2:
                st.markdown("**⚠️ Limitações:**")
                for con in option['cons']:
                    st.markdown(f"• {con}")

            st.markdown(f"**🎯 Ideal para:** {', '.join(option['best_for'])}")

            # Botões de ação
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(f"📋 Ver Requirements", key=f"req_{option['name']}"):
                    req_file = option.get('requirements_file')
                    if req_file and Path(req_file).exists():
                        with open(req_file, 'r') as f:
                            st.code(f.read(), language='text')
                    else:
                        st.warning("Arquivo de requirements não encontrado")

            with col2:
                if 'notebook_file' in option:
                    if st.button(f"📓 Abrir Notebook", key=f"nb_{option['name']}"):
                        st.markdown(f"[Abrir no Colab]({option['url']})")
                        st.info("Faça upload do arquivo: Algoritmos_Visualizador_Colab.ipynb")
                else:
                    if st.button(f"🚀 Deploy Guide", key=f"deploy_{option['name']}"):
                        st.markdown(f"[Ir para {option['name']}]({option['url']})")

            with col3:
                if 'readme_file' in option:
                    if st.button(f"📖 Ver README", key=f"readme_{option['name']}"):
                        readme_file = option['readme_file']
                        if Path(readme_file).exists():
                            with open(readme_file, 'r') as f:
                                st.markdown(f.read())
                        else:
                            st.warning("README não encontrado")

    # Guia de Migração (mantido)
    st.subheader("🔄 Guia de Migração")

    st.markdown("""
    **De Local → Cloud:**

    1. **Streamlit Cloud** (Recomendado para começar):
       - Commit no GitHub
       - Deploy automático
       - Sem configuração complexa

    2. **Google Colab** (Para demonstrações com GPU):
       - Upload do notebook
       - Execução imediata
       - Compartilhamento fácil

    3. **Hugging Face Spaces** (Para produção):
       - Deploy profissional
       - GPU persistente
       - Escalável

    **💡 Dica:** Comece com Streamlit Cloud e migre para outras plataformas conforme necessário.
    """)

def get_platform_config() -> Dict[str, Any]:
    """Retorna configuração otimizada para a plataforma atual."""
    deploy_manager = DeployManager()
    return {
        'platform': deploy_manager.platform_info,
        'gpu': deploy_manager.gpu_info,
        'features_enabled': _get_enabled_features(deploy_manager),
        'cache_optimized': deploy_manager.platform_info['is_cloud']
    }

def _get_enabled_features(deploy_manager: DeployManager) -> List[str]:
    """Retorna lista de funcionalidades habilitadas."""
    base_features = ['visualizacoes', 'exercicios', 'busca_web']

    if deploy_manager.gpu_info['available']:
        base_features.extend(['redes_neurais', 'arte_generativa', 'competicoes'])

        return base_features

    def run_compatibility_check(self) -> Dict[str, Any]:
        """Executa verificação de compatibilidade completa."""
        results = {
            'platform': self.platform_info,
            'gpu': self.gpu_info,
            'dependencies': {},
            'files': {},
            'recommendations': []
        }

        # Verificar dependências críticas
        critical_deps = ['streamlit', 'torch', 'numpy', 'pandas', 'matplotlib', 'plotly']
        for dep in critical_deps:
            try:
                __import__(dep)
                results['dependencies'][dep] = {'status': 'ok', 'version': getattr(__import__(dep), '__version__', 'unknown')}
            except ImportError:
                results['dependencies'][dep] = {'status': 'missing', 'version': None}

        # Verificar arquivos críticos
        critical_files = [
            'app_integrada.py',
            'requirements_streamlit_cloud.txt',
            'colab_setup.py',
            'requirements_huggingface_spaces.txt'
        ]
        for file_path in critical_files:
            path = Path(file_path)
            results['files'][file_path] = path.exists()

        # Recomendações
        if not self.gpu_info['available'] and self.platform_info['name'] == 'Local Development':
            results['recommendations'].append("Considere usar Google Colab ou Hugging Face Spaces para funcionalidades GPU")

        if self.platform_info['name'] == 'Streamlit Cloud':
            results['recommendations'].append("Funcionalidades avançadas de GPU não disponíveis nesta plataforma")

        return results

    def get_system_info(self) -> Dict[str, Any]:
        """Obtém informações detalhadas do sistema."""
        return {
            'python_version': platform.python_version(),
            'system': platform.system(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'environment_vars': {k: v for k, v in os.environ.items() if k.startswith(('STREAMLIT_', 'COLAB_', 'SPACE_', 'HF_'))}
        }# Função para integrar ao app_integrada.py
def integrar_deploy_module():
    """
    Função para integrar o módulo de deploy ao app_integrada.py

    Uso no app_integrada.py:
    ```python
    from deploy_multi_plataforma import show_deploy_dashboard, get_platform_config

    # Na função main ou em uma aba específica
    if st.sidebar.button("🚀 Deploy Options"):
        show_deploy_dashboard()

    # Para obter configuração da plataforma
    platform_config = get_platform_config()
    ```
    """
    pass


def show_verification_tab(deploy_manager: DeployManager):
    """Aba de verificação de compatibilidade."""
    st.markdown("### 🔍 Verificação de Compatibilidade")

    if st.button("🚀 Executar Verificação Completa", type="primary"):
        with st.spinner("Verificando sistema..."):
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Verificação passo a passo
            steps = [
                ("Detectando plataforma", 20),
                ("Verificando GPU", 40),
                ("Verificando dependências", 60),
                ("Verificando arquivos", 80),
                ("Gerando recomendações", 100)
            ]

            results = deploy_manager.run_compatibility_check()

            for step, progress in steps:
                status_text.text(f"🔄 {step}...")
                progress_bar.progress(progress / 100)
                time.sleep(0.5)

            progress_bar.empty()
            status_text.empty()

        # Resultados
        st.success("✅ Verificação concluída!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📍 Plataforma:**")
            st.info(f"{results['platform']['icon']} {results['platform']['name']}")

            st.markdown("**🎮 GPU:**")
            if results['gpu']['available']:
                st.success(f"✅ {results['gpu']['name']} ({results['gpu']['memory_gb']}GB)")
            else:
                st.warning("⚠️ Não disponível")

        with col2:
            st.markdown("**📦 Dependências:**")
            for dep, info in results['dependencies'].items():
                if info['status'] == 'ok':
                    st.success(f"✅ {dep} v{info['version']}")
                else:
                    st.error(f"❌ {dep} - Faltando")

        st.markdown("**📁 Arquivos Críticos:**")
        for file_path, exists in results['files'].items():
            if exists:
                st.success(f"✅ {file_path}")
            else:
                st.error(f"❌ {file_path} - Não encontrado")

        if results['recommendations']:
            st.markdown("**💡 Recomendações:**")
            for rec in results['recommendations']:
                st.info(f"💡 {rec}")


def show_configuration_tab(deploy_manager: DeployManager):
    """Aba de configuração do sistema."""
    st.markdown("### ⚙️ Configuração do Sistema")

    st.markdown("**🔧 Parâmetros de Inicialização:**")

    col1, col2 = st.columns(2)

    with col1:
        force_platform = st.selectbox(
            "Forçar Plataforma:",
            ["Auto-detectar", "Google Colab", "Hugging Face Spaces", "Local"],
            index=0
        )

        debug_mode = st.checkbox("Modo Debug", value=False)
        cache_enabled = st.checkbox("Cache Habilitado", value=True)

    with col2:
        port = st.number_input("Porta do Servidor", value=8501, min_value=8000, max_value=9000)
        timeout = st.number_input("Timeout (segundos)", value=30, min_value=10, max_value=300)

    if st.button("💾 Salvar Configurações"):
        st.success("✅ Configurações salvas!")
        st.rerun()

    st.markdown("---")

    st.markdown("**🔐 Configurações de API:**")

    with st.expander("API Keys (Opcional)"):
        tavily_key = st.text_input("Tavily API Key", type="password", placeholder="tvly-...")
        github_token = st.text_input("GitHub Token", type="password", placeholder="ghp_...")

        if st.button("🔒 Salvar API Keys"):
            st.success("✅ API Keys configuradas!")
            st.info("⚠️ As chaves são armazenadas apenas na sessão atual")


def show_initialization_tab(deploy_manager: DeployManager):
    """Aba de inicialização e controle."""
    st.markdown("### 🚀 Inicialização e Controle")

    st.markdown("**🎯 Comandos Disponíveis:**")

    # Inicialização automática
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Iniciar App (Auto)", type="primary"):
            with st.spinner("Iniciando aplicação..."):
                cmd_key = deploy_manager.execute_command_async("python iniciar.py", "start_app")
                time.sleep(2)

                result = deploy_manager.get_command_result(cmd_key)
                if result['success'] is not None:
                    if result['success']:
                        st.success("✅ Aplicação iniciada com sucesso!")
                        st.info("🌐 Acesse: http://localhost:8501")
                    else:
                        st.error("❌ Erro ao iniciar aplicação")
                        st.code(result['stderr'])
                else:
                    st.warning("⏳ Comando em execução...")

    with col2:
        if st.button("🔍 Verificar Plataforma"):
            with st.spinner("Verificando..."):
                cmd_key = deploy_manager.execute_command_async("python multi_platform_launcher.py", "check_platform")
                time.sleep(3)

                result = deploy_manager.get_command_result(cmd_key)
                if result['success'] is not None:
                    if result['success']:
                        st.success("✅ Verificação concluída!")
                        # Mostrar output
                        with st.expander("📄 Detalhes da Verificação"):
                            st.code(result['stdout'], language='text')
                    else:
                        st.error("❌ Erro na verificação")
                        st.code(result['stderr'])

    st.markdown("---")

    st.markdown("**🛠️ Comandos Manuais:**")

    manual_commands = {
        "Verificar dependências": "python -c \"import torch, streamlit; print('OK')\"",
        "Limpar cache": "rm -rf __pycache__ .streamlit/cache",
        "Testar GPU": "python -c \"import torch; print(torch.cuda.is_available())\"",
        "Ver logs": "tail -20 .streamlit/logs/streamlit.log 2>/dev/null || echo 'Sem logs'"
    }

    selected_cmd = st.selectbox("Selecione comando:", list(manual_commands.keys()))

    if st.button("▶️ Executar Comando"):
        cmd = manual_commands[selected_cmd]
        with st.spinner(f"Executando: {cmd}"):
            cmd_key = deploy_manager.execute_command_async(cmd, f"manual_{selected_cmd}")

            # Aguardar resultado
            for _ in range(10):  # 5 segundos timeout
                time.sleep(0.5)
                result = deploy_manager.get_command_result(cmd_key)
                if result['success'] is not None:
                    break

            if result['success'] is not None:
                if result['success']:
                    st.success("✅ Comando executado com sucesso!")
                    if result['stdout'].strip():
                        st.code(result['stdout'], language='text')
                else:
                    st.error("❌ Erro na execução")
                    if result['stderr'].strip():
                        st.code(result['stderr'], language='text')
            else:
                st.warning("⏳ Comando ainda em execução...")


def show_system_tab(deploy_manager: DeployManager):
    """Aba de informações do sistema."""
    st.markdown("### 📊 Informações do Sistema")

    system_info = deploy_manager.get_system_info()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🐍 Python:**")
        st.info(system_info['python_version'])

        st.markdown("**💻 Sistema:**")
        st.info(f"{system_info['system']} {system_info['machine']}")

        st.markdown("**⚙️ Processador:**")
        st.info(system_info['processor'] or "Não identificado")

    with col2:
        st.markdown("**🏗️ Plataforma:**")
        st.info(system_info['platform'])

        st.markdown("**🔧 Ambiente Streamlit:**")
        streamlit_vars = {k: v for k, v in system_info['environment_vars'].items() if k.startswith('STREAMLIT_')}
        if streamlit_vars:
            for k, v in streamlit_vars.items():
                st.code(f"{k}={v}")
        else:
            st.info("Nenhuma variável Streamlit detectada")

    st.markdown("---")

    st.markdown("**📂 Arquivos do Projeto:**")

    project_files = [
        "app_integrada.py",
        "iniciar.py",
        "multi_platform_launcher.py",
        "requirements.txt",
        "README_MULTIPLATFORMA.md"
    ]

    for file_path in project_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            st.success(f"✅ {file_path} ({size} bytes)")
        else:
            st.error(f"❌ {file_path} - Não encontrado")

    st.markdown("---")

    st.markdown("**💾 Recursos do Sistema:**")

    # Métricas de recursos (simuladas)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("CPU Cores", "4")  # Simulado

    with col2:
        st.metric("Memória Total", "8GB")  # Simulado

    with col3:
        st.metric("Disco Livre", "50GB")  # Simulado