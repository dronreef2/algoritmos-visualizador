#!/usr/bin/env python3
"""
🚀 Script de Deploy Automático - Algoritmos Visualizador
======================================================

Este script automatiza o processo de deploy no Streamlit Cloud.

Uso: python deploy.py
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado."""
    print(f"\n🔧 {descricao}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {descricao} - Sucesso!")
        if resultado.stdout:
            print(resultado.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {descricao} - Falhou!")
        print(f"Erro: {e}")
        if e.stdout:
            print(f"Saída: {e.stdout}")
        if e.stderr:
            print(f"Erro detalhado: {e.stderr}")
        return False


def verificar_prerequisitos():
    """Verifica se todos os pré-requisitos estão atendidos."""
    print("📋 Verificando pré-requisitos...")

    # Verificar se estamos em um repositório git
    if not os.path.exists(".git"):
        print("❌ Não está em um repositório Git!")
        return False

    # Verificar arquivos obrigatórios
    arquivos_obrigatorios = ["app_integrada.py", "requirements.txt", ".streamlit/config.toml"]

    for arquivo in arquivos_obrigatorios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo obrigatório faltando: {arquivo}")
            return False

    print("✅ Todos os pré-requisitos atendidos!")
    return True


def fazer_deploy():
    """Executa o processo completo de deploy."""
    print("🚀 INICIANDO DEPLOY - ALGORITMOS VISUALIZADOR")
    print("=" * 50)

    # Verificar pré-requisitos
    if not verificar_prerequisitos():
        print("\n❌ Pré-requisitos não atendidos. Abortando deploy.")
        return False

    # Verificar status do git
    if not executar_comando("git status --porcelain", "Verificando status do Git"):
        return False

    # Fazer commit se necessário
    status = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if status.stdout.strip():
        print("\n📝 Há mudanças não commitadas. Fazendo commit...")
        if not executar_comando("git add .", "Adicionando arquivos"):
            return False
        if not executar_comando('git commit -m "🚀 Deploy automático"', "Fazendo commit"):
            return False

    # Fazer push
    if not executar_comando("git push origin main", "Fazendo push para GitHub"):
        return False

    print("\n🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Acesse: https://share.streamlit.io")
    print("2. Conecte sua conta GitHub")
    print("3. Selecione o repositório: algoritmos-visualizador")
    print("4. Configure:")
    print("   - Main file path: app_integrada.py")
    print("   - Python version: 3.9+")
    print("5. Configure as secrets no painel do Streamlit Cloud:")
    print("   - TAVILY_API_KEY")
    print("   - GITHUB_TOKEN")
    print("   - OPENAI_API_KEY (opcional)")
    print("   - ANTHROPIC_API_KEY (opcional)")

    # Abrir navegador
    try:
        webbrowser.open("https://share.streamlit.io")
        print("\n🌐 Abrindo Streamlit Cloud no navegador...")
    except:
        print("\n🌐 Acesse manualmente: https://share.streamlit.io")

    return True


if __name__ == "__main__":
    sucesso = fazer_deploy()
    sys.exit(0 if sucesso else 1)
