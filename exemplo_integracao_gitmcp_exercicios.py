#!/usr/bin/env python3
"""
🎯 DEMONSTRAÇÃO: Integração GitMCP com Sistema de Exercícios Práticos
=====================================================================

Esta demonstração mostra como a integração entre GitMCP e o sistema
de exercícios práticos funciona, permitindo enriquecer os exercícios
com exemplos reais do GitHub.

Funcionalidades Demonstradas:
- ✅ Busca de exemplos reais de algoritmos no GitHub
- ✅ Geração de exercícios baseados em código real
- ✅ Comparação de diferentes implementações
- ✅ Exploração de repositórios de algoritmos
- ✅ Relatórios de aprendizado contextualizados

Autor: GitHub Copilot
Data: 2025
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from integracao_gitmcp_exercicios import render_exercicios_gitmcp, gerar_exercicio_github, comparar_implementacoes_github
from gitmcp_integration import GitMCPIntegration
from sistema_exercicios_praticos import SistemaExerciciosPraticos

# Inicializar cliente GitHub
git_client = GitMCPIntegration()


def demonstracao_integracao():
    """Demonstra a integração completa entre GitMCP e exercícios"""

    print("🎯 DEMONSTRAÇÃO: Integração GitMCP com Exercícios Práticos")
    print("=" * 60)

    # Verificar conectividade com GitHub
    print("\n1. 🔍 Verificando conectividade com GitHub API...")
    if git_client.client.is_available():
        print("✅ Conectado ao GitHub API com sucesso!")
    else:
        print("❌ Erro na conexão com GitHub API")
        return

    # Demonstrar busca de repositórios
    print("\n2. 📚 Buscando exemplos reais de algoritmos...")
    try:
        # Usar obter_exemplos_codigo para buscar exemplos
        exemplos = git_client.obter_exemplos_codigo("busca_binaria", "python")
        if exemplos and exemplos.get("exemplos"):
            print(f"✅ Encontrados {len(exemplos['exemplos'])} exemplos!")
            if exemplos["exemplos"]:
                primeiro = exemplos["exemplos"][0]
                print(f"📦 Primeiro exemplo: {primeiro.get('repositorio', 'N/A')}")
        else:
            print("⚠️ Nenhum exemplo encontrado")
    except Exception as e:
        print(f"❌ Erro na busca: {str(e)}")

    # Demonstrar geração de exercícios
    print("\n3. 🎯 Gerando exercício baseado em código real...")
    try:
        exercicio = gerar_exercicio_github("debugging")
        if exercicio:
            print("✅ Exercício gerado com sucesso!")
            print(f"📝 Título: {exercicio['titulo']}")
            print(f"🏷️ Tipo: {exercicio['tipo']}")
            print(f"📚 Fonte: {exercicio['repositorio']}")
        else:
            print("⚠️ Não foi possível gerar exercício")
    except Exception as e:
        print(f"❌ Erro na geração: {str(e)}")

    # Demonstrar comparação de implementações
    print("\n4. ⚡ Comparando implementações de algoritmos...")
    try:
        comparacao = git_client.comparar_implementacoes("busca_binaria")
        if comparacao and comparacao.get("implementacoes"):
            print("✅ Comparação realizada com sucesso!")
            print(f"📊 {len(comparacao['implementacoes'])} implementações analisadas")
            for impl in comparacao["implementacoes"][:2]:
                print(f"  - {impl.get('repositorio', 'N/A')}: {impl.get('abordagem', 'N/A')}")
        else:
            print("⚠️ Não foi possível realizar comparação")
    except Exception as e:
        print(f"❌ Erro na comparação: {str(e)}")

    # Demonstrar sistema de exercícios integrado
    print("\n5. 🔗 Sistema de exercícios com integração GitHub...")
    try:
        sistema = SistemaExerciciosPraticos()
        exercicios = list(sistema.exercicios.values())
        if exercicios:
            print(f"✅ Sistema carregado com {len(exercicios)} exercícios")
            print("🎯 Integração GitMCP permite:")
            print("  - Enriquecer exercícios com exemplos reais")
            print("  - Gerar exercícios baseados em código GitHub")
            print("  - Comparar diferentes abordagens de implementação")
            print("  - Explorar repositórios educacionais")
        else:
            print("⚠️ Sistema de exercícios vazio")
    except Exception as e:
        print(f"❌ Erro no sistema: {str(e)}")

    print("\n" + "=" * 60)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("\n💡 Benefícios da Integração:")
    print("  • Exemplos reais de implementação")
    print("  • Comparação de abordagens diferentes")
    print("  • Aprendizado contextualizado")
    print("  • Conexão teoria-prática")
    print("  • Acesso a código de qualidade")


def demonstracao_streamlit():
    """Demonstra como executar a interface Streamlit integrada"""

    print("\n🚀 PARA EXECUTAR A INTERFACE STREAMLIT:")
    print("   streamlit run app_integrada.py")
    print("\n📍 Navegue até a seção 'Exercícios Práticos'")
    print("   e selecione a aba 'Exercícios com GitHub'")
    print("\n🎯 Funcionalidades disponíveis:")
    print("   • 📚 Exemplos Reais - Veja implementações reais")
    print("   • 🎯 Exercícios GitHub - Pratique com código real")
    print("   • ⚡ Comparação Performance - Compare abordagens")
    print("   • 🔍 Explorar Repositórios - Descubra projetos")


if __name__ == "__main__":
    demonstracao_integracao()
    demonstracao_streamlit()
