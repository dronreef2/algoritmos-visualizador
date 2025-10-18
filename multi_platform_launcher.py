#!/usr/bin/env python3
"""
🚀 Algoritmos Visualizador - Multi-Platform Launcher
====================================================

Launcher inteligente que detecta automaticamente o ambiente de execução
e configura a aplicação adequadamente para diferentes plataformas.

Plataformas Suportadas:
- 🖥️  Local Development (VS Code, terminal)
- 🌐 Google Colab (GPU/TPU support)
- 🤗 Hugging Face Spaces (GPU persistent)
- ☁️  Streamlit Cloud (CPU-only optimized)

Funcionalidades:
- ✅ Auto-detecção de ambiente
- ✅ Configuração automática de dependências
- ✅ Otimização de recursos por plataforma
- ✅ Logs detalhados de inicialização
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
import importlib.util
from typing import Dict, Any, List

class PlatformDetector:
    """Detector inteligente de plataformas de execução."""

    def __init__(self):
        self.platform_info = self._detect_platform()
        self.gpu_info = self._detect_gpu()
        self.dependencies_status = {}

    def _detect_platform(self) -> Dict[str, Any]:
        """Detecta a plataforma atual."""
        info = {
            'name': 'unknown',
            'is_colab': False,
            'is_huggingface': False,
            'is_streamlit_cloud': False,
            'is_local': True,
            'python_version': platform.python_version(),
            'system': platform.system().lower()
        }

        # Detect Google Colab
        if 'COLAB_GPU' in os.environ or 'COLAB_TPU_ADDR' in os.environ:
            info.update({
                'name': 'google_colab',
                'is_colab': True,
                'is_local': False
            })

        # Detect Hugging Face Spaces
        if 'SPACE_ID' in os.environ or 'HF_SPACE' in os.environ:
            info.update({
                'name': 'huggingface_spaces',
                'is_huggingface': True,
                'is_local': False
            })

        # Detect Streamlit Cloud
        if 'STREAMLIT_SERVER_HEADLESS' in os.environ:
            info.update({
                'name': 'streamlit_cloud',
                'is_streamlit_cloud': True,
                'is_local': False
            })

        return info

    def _detect_gpu(self) -> Dict[str, Any]:
        """Detecta informações da GPU."""
        gpu_info = {
            'available': False,
            'type': 'cpu',
            'name': 'CPU',
            'memory_gb': 0
        }

        try:
            import torch
            gpu_info['available'] = torch.cuda.is_available()
            if gpu_info['available']:
                gpu_info.update({
                    'type': 'cuda',
                    'name': torch.cuda.get_device_name(0),
                    'memory_gb': torch.cuda.get_device_properties(0).total_memory / (1024**3)
                })
        except ImportError:
            pass

        return gpu_info

    def check_dependencies(self) -> Dict[str, bool]:
        """Verifica status das dependências críticas."""
        dependencies = {
            'streamlit': 'streamlit',
            'torch': 'torch',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'matplotlib': 'matplotlib',
            'plotly': 'plotly'
        }

        status = {}
        for name, module in dependencies.items():
            try:
                importlib.import_module(module)
                status[name] = True
            except ImportError:
                status[name] = False

        self.dependencies_status = status
        return status

    def get_optimization_config(self) -> Dict[str, Any]:
        """Retorna configuração otimizada para a plataforma."""
        base_config = {
            'cache_enabled': True,
            'gpu_acceleration': self.gpu_info['available'],
            'memory_limit': None,
            'timeout_limit': None,
            'debug_mode': False
        }

        if self.platform_info['is_colab']:
            base_config.update({
                'platform_name': 'Google Colab',
                'memory_limit': 'ilimitado',
                'timeout_limit': 'ilimitado',
                'gpu_acceleration': True,
                'recommended_features': ['redes_neurais', 'arte_generativa', 'competicoes']
            })

        elif self.platform_info['is_huggingface']:
            base_config.update({
                'platform_name': 'Hugging Face Spaces',
                'memory_limit': '16GB',
                'timeout_limit': 'ilimitado',
                'gpu_acceleration': True,
                'recommended_features': ['modelos_ml', 'api_integrations', 'deploy_profissional']
            })

        elif self.platform_info['is_streamlit_cloud']:
            base_config.update({
                'platform_name': 'Streamlit Cloud',
                'memory_limit': '1GB',
                'timeout_limit': '10-15min',
                'gpu_acceleration': False,
                'recommended_features': ['visualizacoes', 'exercicios', 'aprendizado_basico']
            })

        else:
            base_config.update({
                'platform_name': 'Local Development',
                'memory_limit': 'sistema',
                'timeout_limit': 'ilimitado',
                'gpu_acceleration': self.gpu_info['available'],
                'recommended_features': ['desenvolvimento', 'debugging', 'testing']
            })

        return base_config

class MultiPlatformLauncher:
    """Launcher multi-plataforma inteligente."""

    def __init__(self):
        self.detector = PlatformDetector()
        self.config = self.detector.get_optimization_config()

    def install_dependencies(self) -> bool:
        """Instala dependências específicas da plataforma."""
        print("📦 Verificando/instalando dependências...")

        platform_deps = {
            'google_colab': [
                'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118',
                'streamlit numpy pandas matplotlib plotly seaborn scipy',
                'requests pillow tavily-python psutil'
            ],
            'huggingface_spaces': [
                'streamlit torch torchvision torchaudio numpy pandas matplotlib plotly',
                'seaborn scipy requests pillow tavily-python psutil'
            ],
            'streamlit_cloud': [
                'streamlit torch==2.0.0+cpu torchvision==0.15.0+cpu torchaudio==2.0.0',
                'numpy pandas matplotlib plotly seaborn scipy',
                'requests pillow tavily-python psutil'
            ]
        }

        platform_name = self.detector.platform_info['name']
        if platform_name in platform_deps:
            deps = platform_deps[platform_name]
            for dep in deps:
                try:
                    cmd = f"pip install -q {dep}"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
                    if result.returncode != 0:
                        print(f"   ⚠️  Erro instalando {dep}: {result.stderr}")
                        return False
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    return False

        print("   ✅ Dependências OK")
        return True

    def show_platform_info(self):
        """Exibe informações detalhadas da plataforma."""
        print("🖥️  DETECÇÃO DE PLATAFORMA")
        print("=" * 50)

        info = self.detector.platform_info
        gpu = self.detector.gpu_info

        print(f"📍 Plataforma: {self.config['platform_name']}")
        print(f"🐍 Python: {info['python_version']}")
        print(f"💻 Sistema: {info['system']}")

        if gpu['available']:
            print(f"🎮 GPU: {gpu['name']} ({gpu['memory_gb']:.1f}GB)")
        else:
            print("⚡ GPU: Não disponível (CPU-only)")

        print(f"🧠 Memória limite: {self.config['memory_limit']}")
        print(f"⏱️  Timeout: {self.config['timeout_limit']}")

        print("\n🎯 Recursos recomendados:")
        for feature in self.config['recommended_features']:
            print(f"   • {feature.replace('_', ' ').title()}")

    def launch_application(self, app_file: str = "app_integrada.py", port: int = 8501):
        """Lança a aplicação com configurações otimizadas."""
        print("\n🚀 INICIANDO APLICAÇÃO")
        print("=" * 50)

        # Configurar variáveis de ambiente
        env_vars = {
            'PLATFORM_DETECTED': self.detector.platform_info['name'],
            'GPU_AVAILABLE': str(self.detector.gpu_info['available']).lower(),
            'CACHE_ENABLED': str(self.config['cache_enabled']).lower(),
        }

        if self.detector.platform_info['is_colab']:
            env_vars.update({
                'STREAMLIT_SERVER_HEADLESS': 'true',
                'STREAMLIT_SERVER_PORT': str(port),
                'STREAMLIT_SERVER_ADDRESS': '0.0.0.0'
            })

        # Construir comando
        cmd_parts = ["streamlit", "run", app_file]

        # Adicionar configurações específicas
        if self.detector.platform_info['is_colab']:
            cmd_parts.extend(["--server.port", str(port), "--server.address", "0.0.0.0"])
        elif self.detector.platform_info['is_huggingface']:
            cmd_parts.extend(["--server.port", str(port), "--server.address", "0.0.0.0"])
        else:
            cmd_parts.extend(["--server.headless", "true", "--server.port", str(port)])

        cmd = " ".join(cmd_parts)

        print(f"🎯 Executando: {cmd}")
        print(f"🌐 URL esperada: http://localhost:{port}")
        if self.detector.platform_info['is_colab']:
            print("🔗 No Colab, um link externo será gerado automaticamente")

        print("\n" + "=" * 50)

        # Executar
        try:
            os.environ.update(env_vars)
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            print("\n⏹️  Aplicação interrompida pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro ao executar aplicação: {e}")

def main():
    """Função principal."""
    print("🎯 ALGORITMOS VISUALIZADOR - MULTI-PLATFORM LAUNCHER")
    print("=" * 60)

    launcher = MultiPlatformLauncher()

    # Detectar plataforma
    launcher.show_platform_info()

    # Verificar dependências
    print("\n📦 Verificando dependências...")
    deps_status = launcher.detector.check_dependencies()

    missing_deps = [name for name, status in deps_status.items() if not status]
    if missing_deps:
        print(f"   ⚠️  Dependências faltando: {', '.join(missing_deps)}")
        if launcher.detector.platform_info['is_colab'] or launcher.detector.platform_info['is_huggingface']:
            print("   🔄 Instalando dependências automaticamente...")
            if not launcher.install_dependencies():
                print("   ❌ Falha na instalação. Saindo...")
                return 1
        else:
            print("   💡 Execute: pip install -r requirements.txt")
            return 1
    else:
        print("   ✅ Todas as dependências OK")

    # Verificar arquivo da aplicação
    app_file = "app_integrada.py"
    if not Path(app_file).exists():
        print(f"   ❌ Arquivo {app_file} não encontrado")
        return 1

    print("   ✅ Arquivo da aplicação OK")

    # Launch application
    launcher.launch_application(app_file)

    return 0

if __name__ == "__main__":
    sys.exit(main())