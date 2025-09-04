#!/usr/bin/env python3
"""
Exemplo de integração: Busca contextual para algoritmos
Demonstra como usar o MCP Tavily para enriquecer o aprendizado
"""

import sys
import os
sys.path.append('/workspaces/algoritmos-visualizador')

from mcp_tavily_integration import TavilySearchClient, buscar_web

def buscar_explicacao_algoritmo(nome_algoritmo: str):
    """
    Busca explicações contextuais para algoritmos específicos
    """
    query = f"{nome_algoritmo} algoritmo explicação completa em Python"
    print(f"🔍 Buscando explicação para: {nome_algoritmo}")

    resultado = buscar_web(query, "advanced")

    if "error" in resultado:
        print(f"❌ Erro na busca: {resultado['error']}")
        return None

    return resultado

def demonstrar_busca_algoritmos():
    """
    Demonstra busca contextual para diferentes algoritmos
    """
    print("🎯 Demonstração: Busca Contextual de Algoritmos")
    print("=" * 60)

    algoritmos = [
        "busca binária",
        "árvore binária de busca",
        "algoritmo de Dijkstra",
        "programação dinâmica",
        "algoritmo de ordenação quicksort"
    ]

    for algoritmo in algoritmos:
        print(f"\n🔍 Pesquisando: {algoritmo}")
        print("-" * 40)

        resultado = buscar_explicacao_algoritmo(algoritmo)

        if resultado and "results" in resultado:
            print(f"✅ Encontrados {len(resultado['results'])} resultados")

            # Mostra os primeiros 2 resultados
            for i, item in enumerate(resultado['results'][:2], 1):
                print(f"{i}. 📄 {item.get('title', 'Título não disponível')}")
                print(f"   🔗 {item.get('url', 'URL não disponível')}")
                if 'snippet' in item:
                    # Limita o snippet a 100 caracteres
                    snippet = item['snippet'][:100] + "..." if len(item['snippet']) > 100 else item['snippet']
                    print(f"   📝 {snippet}")
                print()
        else:
            print("❌ Nenhum resultado encontrado")

        print("-" * 40)

def integrar_com_visualizador():
    """
    Exemplo de como integrar com o visualizador de algoritmos
    """
    print("\n🔗 Integração com Visualizador de Algoritmos")
    print("=" * 50)

    # Simula integração com o módulo de algoritmos
    try:
        from modulo_1_fundamentos.busca_binaria import BuscaBinaria
        from modulo_1_fundamentos.aplicacoes_reais import SistemaBuscaLogs

        print("✅ Módulos do visualizador carregados")

        # Demonstra busca binária
        arr = [1, 3, 5, 7, 9, 11, 13, 15]
        alvo = 7

        busca = BuscaBinaria()
        resultado = busca.buscar(arr, alvo)

        print(f"🔍 Busca binária em {arr}")
        print(f"🎯 Procurando: {alvo}")
        print(f"📍 Resultado: índice {resultado}")

        # Busca explicação contextual
        explicacao = buscar_web("busca binária algoritmo explicação passo a passo", "basic")

        if explicacao and "results" in explicacao:
            print("\n💡 Explicação contextual:")
            print(f"   {explicacao['results'][0].get('snippet', 'Explicação não disponível')[:150]}...")

    except ImportError as e:
        print(f"⚠️ Módulo não disponível: {e}")
        print("   Execute este exemplo dentro do ambiente completo do projeto")

def exemplo_pesquisa_interativa():
    """
    Exemplo de pesquisa interativa
    """
    print("\n🎮 Pesquisa Interativa")
    print("=" * 30)

    while True:
        query = input("Digite o termo de busca (ou 'sair' para encerrar): ").strip()

        if query.lower() in ['sair', 'exit', 'quit']:
            break

        if not query:
            continue

        print(f"\n🔍 Buscando: {query}")

        resultado = buscar_web(query, "basic")

        if "error" in resultado:
            print(f"❌ Erro: {resultado['error']}")
        elif "results" in resultado:
            print(f"✅ {len(resultado['results'])} resultados encontrados")

            for i, item in enumerate(resultado['results'][:3], 1):
                print(f"{i}. {item.get('title', 'Sem título')}")
                print(f"   {item.get('url', 'Sem URL')}")
        else:
            print("❌ Nenhum resultado encontrado")

        print()

if __name__ == "__main__":
    print("🚀 Exemplos de Integração MCP Tavily")
    print("=" * 50)

    # Verifica configuração
    client = TavilySearchClient()
    if not client.is_configured():
        print("❌ CONFIGURAÇÃO NECESSÁRIA:")
        print("   1. Edite mcp-server-tavily/.env")
        print("   2. Configure TAVILY_API_KEY com sua chave da API Tavily")
        print("   3. Obtenha chave gratuita em: https://tavily.com/")
        sys.exit(1)

    # Menu de opções
    while True:
        print("\nEscolha uma opção:")
        print("1. 🔍 Demonstrar busca de algoritmos")
        print("2. 🔗 Integrar com visualizador")
        print("3. 🎮 Pesquisa interativa")
        print("4. ❌ Sair")

        try:
            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                demonstrar_busca_algoritmos()
            elif opcao == "2":
                integrar_com_visualizador()
            elif opcao == "3":
                exemplo_pesquisa_interativa()
            elif opcao == "4":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida")

        except KeyboardInterrupt:
            print("\n👋 Programa interrompido pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
