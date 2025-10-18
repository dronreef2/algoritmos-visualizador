#!/usr/bin/env python3
"""
🚀 Inicialização Algoritmos Visualizador
========================================

Script de inicialização inteligente que:
- Detecta automaticamente a plataforma
- Configura o ambiente adequadamente
- Lança a aplicação com otimizações

Uso:
    python iniciar.py              # Auto-detecção
    python iniciar.py --colab      # Forçar modo Colab
    python iniciar.py --spaces     # Forçar modo Spaces
    python iniciar.py --local      # Forçar modo local
"""

import sys
import os
from pathlib import Path

def main():
    """Função principal de inicialização."""
    print("🎯 ALGORITMOS VISUALIZADOR - INICIALIZAÇÃO")
    print("=" * 50)

    # Verificar argumentos
    force_platform = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--colab', '-c']:
            force_platform = 'colab'
            os.environ['FORCE_PLATFORM'] = 'colab'
        elif arg in ['--spaces', '-s']:
            force_platform = 'spaces'
            os.environ['FORCE_PLATFORM'] = 'spaces'
        elif arg in ['--local', '-l']:
            force_platform = 'local'
            os.environ['FORCE_PLATFORM'] = 'local'

    if force_platform:
        print(f"🔧 Plataforma forçada: {force_platform}")
    else:
        print("🔍 Detectando plataforma automaticamente...")

    # Verificar se estamos no diretório correto
    current_dir = Path.cwd()
    app_file = current_dir / "app_integrada.py"
    launcher_file = current_dir / "multi_platform_launcher.py"

    if not app_file.exists():
        print("❌ Arquivo app_integrada.py não encontrado!")
        print(f"   Diretório atual: {current_dir}")
        print("   Certifique-se de executar este script do diretório do projeto.")
        return 1

    # Escolher método de inicialização
    if launcher_file.exists():
        print("🚀 Usando launcher multi-plataforma...")
        cmd = [sys.executable, str(launcher_file)]
    else:
        print("📱 Usando inicialização direta...")
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_file)]

        # Adicionar configurações específicas da plataforma
        if force_platform == 'colab':
            cmd.extend(["--server.port", "8501", "--server.address", "0.0.0.0"])
        elif force_platform == 'spaces':
            cmd.extend(["--server.port", "7860", "--server.address", "0.0.0.0"])

    print(f"🎯 Executando: {' '.join(cmd)}")
    print("=" * 50)

    try:
        os.execv(sys.executable, cmd)
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())