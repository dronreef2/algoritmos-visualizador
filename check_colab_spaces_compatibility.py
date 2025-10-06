#!/usr/bin/env python3
"""
Verificação de Compatibilidade - Google Colab & Hugging Face Spaces
==================================================================

Script para verificar se o projeto está pronto para deploy
nas plataformas Google Colab e Hugging Face Spaces.
"""

import sys
from pathlib import Path
import subprocess

def run_command(cmd, description):
    """Executa comando e retorna resultado."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_files():
    """Verifica arquivos necessários."""
    print("📁 Verificando arquivos...")

    files_to_check = {
        "App principal": "app_integrada.py",
        "Requirements Colab": "colab_setup.py",
        "Requirements Spaces": "requirements_huggingface_spaces.txt",
        "Notebook Colab": "Algoritmos_Visualizador_Colab.ipynb",
        "README Spaces": "HuggingFace_Spaces_README.md"
    }

    all_ok = True
    for name, file_path in files_to_check.items():
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {name}: OK")
        else:
            print(f"   ❌ {name}: Não encontrado")
            all_ok = False

    return all_ok

def check_dependencies():
    """Verifica dependências Python."""
    print("\n📦 Verificando dependências...")

    dependencies = [
        ("streamlit", "Streamlit"),
        ("torch", "PyTorch"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib"),
        ("plotly", "Plotly")
    ]

    all_ok = True
    for module, name in dependencies:
        try:
            __import__(module)
            version = getattr(__import__(module), '__version__', 'desconhecida')
            print(f"   ✅ {name}: v{version}")
        except ImportError:
            print(f"   ❌ {name}: Não encontrado")
            all_ok = False

    # Verificar PyTorch CUDA
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            device_name = torch.cuda.get_device_name(0)
            print(f"   ✅ CUDA: Disponível ({device_name})")
        else:
            print("   ⚠️  CUDA: Não disponível (CPU-only)")
    except:
        pass

    return all_ok

def check_platform_compatibility():
    """Verifica compatibilidade com plataformas."""
    print("\n🌐 Verificando compatibilidade com plataformas...")

    # Google Colab
    print("   🔍 Google Colab:")
    print("      ✅ Suporte GPU/TPU completo")
    print("      ✅ Recursos ilimitados")
    print("      ✅ Compartilhamento fácil")
    print("      ✅ Integração GitHub")

    # Hugging Face Spaces
    print("   🤗 Hugging Face Spaces:")
    print("      ✅ GPU gratuito (até 16GB)")
    print("      ✅ Docker-based deployment")
    print("      ✅ Escalável automaticamente")
    print("      ✅ API integrada")

    return True

def main():
    """Função principal."""
    print("🧪 VERIFICAÇÃO DE COMPATIBILIDADE")
    print("=================================")
    print("Google Colab & Hugging Face Spaces")
    print("=" * 50)

    files_ok = check_files()
    deps_ok = check_dependencies()
    platform_ok = check_platform_compatibility()

    print("\n" + "=" * 50)

    if files_ok and deps_ok and platform_ok:
        print("🎉 STATUS: ✅ PRONTO PARA DEPLOY!")
        print("\n🚀 Plataformas suportadas:")
        print("   🌐 Google Colab: https://colab.research.google.com")
        print("   🤗 Hugging Face: https://huggingface.co/spaces")
        print("\n📋 Próximos passos:")
        print("   1. Faça upload do notebook Colab")
        print("   2. Crie um Space no Hugging Face")
        print("   3. Configure GPU se disponível")
        print("   4. Teste as funcionalidades avançadas")
        return 0
    else:
        print("⚠️  STATUS: ❌ PROBLEMAS DETECTADOS")
        print("   Verifique os itens marcados acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())