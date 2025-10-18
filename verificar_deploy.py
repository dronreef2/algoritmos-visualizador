#!/usr/bin/env python3
"""
🔍 Verificador de Deploy - Algoritmos Visualizador
===============================================

Este script verifica se todos os componentes necessários estão
presentes e funcionando antes do deploy no Streamlit Cloud.

Uso: python verificar_deploy.py
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path


def verificar_arquivos_obrigatorios():
    """Verifica se todos os arquivos obrigatórios estão presentes."""
    print("📁 Verificando arquivos obrigatórios...")

    arquivos_obrigatorios = ["app_integrada.py", "requirements.txt", "packages.txt", ".streamlit/config.toml"]

    arquivos_opcionais = [".streamlit/secrets.toml", "STREAMLIT_DEPLOY_GUIDE.md"]

    todos_presentes = True

    for arquivo in arquivos_obrigatorios:
        if os.path.exists(arquivo):
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo} - ARQUIVO FALTANDO!")
            todos_presentes = False

    print("\n📋 Arquivos opcionais:")
    for arquivo in arquivos_opcionais:
        if os.path.exists(arquivo):
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ⚠️  {arquivo} - Recomendado criar")

    return todos_presentes


def verificar_modulos():
    """Verifica se os módulos principais podem ser importados."""
    print("\n📚 Verificando módulos principais...")

    modulos_para_testar = ["streamlit", "numpy", "matplotlib", "pandas", "plotly", "requests"]

    modulos_opcionais = ["tavily", "github", "git"]

    print("📦 Módulos obrigatórios:")
    for modulo in modulos_para_testar:
        try:
            importlib.import_module(modulo)
            print(f"  ✅ {modulo}")
        except ImportError:
            print(f"  ❌ {modulo} - Módulo não encontrado")

    print("\n🔧 Módulos opcionais:")
    for modulo in modulos_opcionais:
        try:
            importlib.import_module(modulo)
            print(f"  ✅ {modulo}")
        except ImportError:
            print(f"  ⚠️  {modulo} - Módulo opcional não encontrado")


def verificar_estrutura_diretorios():
    """Verifica se a estrutura de diretórios está correta."""
    print("\n🏗️  Verificando estrutura de diretórios...")

    diretorios_esperados = [
        "modulo_1_fundamentos",
        "modulo_2_estruturas_dados",
        "modulo_3_programacao_dinamica",
        "modulo_4_entrevistas",
        ".streamlit",
    ]

    for diretorio in diretorios_esperados:
        if os.path.isdir(diretorio):
            print(f"  ✅ {diretorio}/")
        else:
            print(f"  ❌ {diretorio}/ - Diretório faltando")


def verificar_configuracao_streamlit():
    """Verifica se a configuração do Streamlit está adequada."""
    print("\n⚙️  Verificando configuração do Streamlit...")

    config_path = ".streamlit/config.toml"
    if os.path.exists(config_path):
        print("  ✅ Arquivo config.toml encontrado")

        # Verificar configurações importantes
        with open(config_path, "r") as f:
            config_content = f.read()

        configuracoes_importantes = [("address", "0.0.0.0"), ("headless", "true"), ("developmentMode", "false")]

        for config, valor_esperado in configuracoes_importantes:
            if valor_esperado in config_content:
                print(f"  ✅ {config} = {valor_esperado}")
            else:
                print(f"  ⚠️  {config} pode precisar ser ajustado")
    else:
        print("  ❌ Arquivo config.toml não encontrado")


def verificar_dependencias():
    """Verifica se as dependências no requirements.txt estão corretas."""
    print("\n📦 Verificando dependências...")

    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            requirements = f.read()

        dependencias_importantes = ["streamlit", "numpy", "matplotlib", "pandas", "plotly"]

        for dep in dependencias_importantes:
            if dep in requirements:
                print(f"  ✅ {dep} encontrado no requirements.txt")
            else:
                print(f"  ❌ {dep} não encontrado no requirements.txt")
    else:
        print("  ❌ requirements.txt não encontrado")


def verificar_secrets():
    """Verifica configuração de secrets."""
    print("\n🔑 Verificando configuração de secrets...")

    secrets_path = ".streamlit/secrets.toml"
    example_path = ".streamlit/secrets.toml.example"

    if os.path.exists(secrets_path):
        print("  ✅ secrets.toml encontrado")
        print("  ⚠️  Lembre-se: NUNCA commite o arquivo secrets.toml!")
    elif os.path.exists(example_path):
        print("  ✅ secrets.toml.example encontrado")
        print("  📝 Configure suas chaves de API no secrets.toml")
    else:
        print("  ❌ Nenhum arquivo de secrets encontrado")
        print("  📝 Crie .streamlit/secrets.toml com suas chaves de API")


def executar_teste_basico():
    """Executa um teste básico da aplicação."""
    print("\n🧪 Executando teste básico...")

    try:
        # Tentar importar a aplicação
        sys.path.append(".")
        import app_integrada

        print("  ✅ app_integrada.py pode ser importado")
    except Exception as e:
        print(f"  ❌ Erro ao importar app_integrada.py: {e}")


def main():
    """Função principal do verificador."""
    print("🚀 VERIFICADOR DE DEPLOY - ALGORITMOS VISUALIZADOR")
    print("=" * 60)

    # Executar todas as verificações
    arquivos_ok = verificar_arquivos_obrigatorios()
    verificar_modulos()
    verificar_estrutura_diretorios()
    verificar_configuracao_streamlit()
    verificar_dependencias()
    verificar_secrets()
    executar_teste_basico()

    print("\n" + "=" * 60)
    print("📊 RESUMO DA VERIFICAÇÃO:")

    if arquivos_ok:
        print("✅ Todos os arquivos obrigatórios estão presentes!")
        print("🎯 Status: PRONTO PARA DEPLOY")
        print("\n📋 Próximos passos:")
        print("1. Configure suas chaves de API no .streamlit/secrets.toml")
        print("2. Commit e push para o GitHub")
        print("3. Deploy no Streamlit Cloud via share.streamlit.io")
    else:
        print("❌ Alguns arquivos obrigatórios estão faltando!")
        print("🔧 Status: CORRIJA OS PROBLEMAS ANTES DO DEPLOY")

    print("\n📖 Para mais detalhes, consulte: STREAMLIT_DEPLOY_GUIDE.md")


if __name__ == "__main__":
    main()
