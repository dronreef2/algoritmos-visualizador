#!/usr/bin/env python3
"""
Script de Monitoramento Simplificado - Algoritmos Visualizador
"""

import requests
import subprocess
import sys
import os
from datetime import datetime


def check_streamlit_app():
    """Verifica se o Streamlit App está online"""
    try:
        response = requests.get("https://algoritmos-visualizador.streamlit.app/", timeout=10)
        if response.status_code == 200:
            print("✓ Streamlit App: Online")
            return True
        else:
            print(f"✗ Streamlit App: Erro HTTP {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"✗ Streamlit App: Erro de conexão")
        return False


def check_local_imports():
    """Verifica imports básicos"""
    try:
        if not os.path.exists("modulo_1_fundamentos"):
            print("✗ Testes Locais: Diretório não encontrado")
            return False

        os.chdir("modulo_1_fundamentos")
        result = subprocess.run(
            [sys.executable, "-c", "from aplicacoes_reais import SistemaBuscaLogs; print('OK')"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        os.chdir("..")

        if result.returncode == 0:
            print("✓ Testes Locais: Imports funcionando")
            return True
        else:
            print("✗ Testes Locais: Erro nos imports")
            return False

    except Exception as e:
        print("✗ Testes Locais: Erro na verificação")
        return False


def main():
    print("=" * 50)
    print(f"MONITORAMENTO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # Instalar requests se necessário
    try:
        import requests
    except ImportError:
        print("Instalando requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        import requests

    checks = [check_streamlit_app(), check_local_imports()]

    passed = sum(checks)
    total = len(checks)

    print(f"\nRESUMO: {passed}/{total} verificações passaram")

    if passed == total:
        print("STATUS: TODOS OS SISTEMAS FUNCIONANDO")
        return 0
    else:
        print("STATUS: ALGUNS PROBLEMAS DETECTADOS")
        return 1


if __name__ == "__main__":
    sys.exit(main())
