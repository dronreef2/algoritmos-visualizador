#!/usr/bin/env python3
"""
Exemplo de Integração GitMCP com Sistema de Algoritmos
Demonstra como usar o GitMCP para enriquecer o aprendizado
"""

import sys
from typing import Dict, List, Any

# Importações do projeto
from gitmcp_integration import gitmcp_integration, gitmcp_client
from mcp_config import MCPConfig


class AprendizadoComGitMCP:
    """
    Sistema de aprendizado aprimorado com GitMCP
    Integra documentação externa com o conteúdo local
    """

    def __init__(self):
        self.config = MCPConfig()
        self.gitmcp = gitmcp_integration
        self.client = gitmcp_client

    def obter_documentacao_algoritmo(self, algoritmo: str, linguagem: str = "python") -> Dict[str, Any]:
        """
        Obtém documentação completa de um algoritmo

        Args:
            algoritmo: Nome do algoritmo
            linguagem: Linguagem de programação

        Returns:
            Dict com documentação completa
        """
        print(f"🔍 Buscando documentação para: {algoritmo} ({linguagem})")

        # Busca documentação no GitMCP
        documentacao = self.gitmcp.buscar_documentacao_algoritmo(algoritmo, linguagem)

        if documentacao["total_encontrados"] > 0:
            print(f"✅ Encontrados {documentacao['total_encontrados']} repositórios relevantes")

            # Retorna o melhor resultado
            melhor_resultado = documentacao["resultados"][0]
            return {
                "algoritmo": algoritmo,
                "linguagem": linguagem,
                "repositorio": melhor_resultado["repositorio"],
                "documentacao": melhor_resultado["documentacao"],
                "exemplos_busca": melhor_resultado["resultados_busca"],
                "fonte": "GitMCP",
            }
        else:
            print("❌ Nenhuma documentação encontrada")
            return {"algoritmo": algoritmo, "linguagem": linguagem, "erro": "Documentação não encontrada", "fonte": "GitMCP"}

    def comparar_implementacoes(self, algoritmo: str) -> Dict[str, Any]:
        """
        Compara implementações do mesmo algoritmo em diferentes linguagens

        Args:
            algoritmo: Nome do algoritmo

        Returns:
            Dict com comparações
        """
        print(f"🔄 Comparando implementações de: {algoritmo}")

        comparacao = self.gitmcp.comparar_implementacoes(algoritmo)

        if comparacao["linguagens"]:
            print(f"✅ Encontradas implementações em: {', '.join(comparacao['linguagens'])}")

            return {
                "algoritmo": algoritmo,
                "comparacoes": comparacao["comparacoes"],
                "linguagens": comparacao["linguagens"],
                "fonte": "GitMCP",
            }
        else:
            print("❌ Nenhuma implementação encontrada para comparação")
            return {"algoritmo": algoritmo, "erro": "Implementações não encontradas", "fonte": "GitMCP"}

    def obter_exemplos_praticos(self, conceito: str, max_exemplos: int = 3) -> List[Dict[str, Any]]:
        """
        Obtém exemplos práticos de código para um conceito

        Args:
            conceito: Conceito ou algoritmo
            max_exemplos: Número máximo de exemplos

        Returns:
            Lista de exemplos de código
        """
        print(f"💻 Buscando exemplos práticos para: {conceito}")

        exemplos = self.gitmcp.obter_exemplos_codigo(conceito)

        if exemplos["total_exemplos"] > 0:
            print(f"✅ Encontrados {exemplos['total_exemplos']} exemplos")

            # Retorna os melhores exemplos
            return exemplos["exemplos"][:max_exemplos]
        else:
            print("❌ Nenhum exemplo encontrado")
            return []

    def criar_sessao_aprendizado(self, topico: str) -> Dict[str, Any]:
        """
        Cria uma sessão completa de aprendizado com múltiplas fontes

        Args:
            topico: Tópico principal

        Returns:
            Dict com sessão completa de aprendizado
        """
        print(f"🎓 Criando sessão de aprendizado: {topico}")
        print("=" * 50)

        sessao = {"topico": topico, "documentacao": None, "exemplos": [], "comparacoes": None, "fontes": []}

        # 1. Obtém documentação principal
        print("\n1️⃣ Buscando documentação...")
        docs = self.obter_documentacao_algoritmo(topico)
        if "documentacao" in docs:
            sessao["documentacao"] = docs
            sessao["fontes"].append("documentacao")

        # 2. Obtém exemplos práticos
        print("\n2️⃣ Buscando exemplos práticos...")
        exemplos = self.obter_exemplos_praticos(topico, max_exemplos=3)
        if exemplos:
            sessao["exemplos"] = exemplos
            sessao["fontes"].append("exemplos")

        # 3. Compara implementações (se for algoritmo)
        if topico.lower() in ["sort", "search", "graph", "tree", "dynamic"]:
            print("\n3️⃣ Comparando implementações...")
            comparacao = self.comparar_implementacoes(topico)
            if "comparacoes" in comparacao:
                sessao["comparacoes"] = comparacao
                sessao["fontes"].append("comparacoes")

        print(f"\n✅ Sessão criada com {len(sessao['fontes'])} fontes de informação")
        return sessao

    def gerar_relatorio_aprendizado(self, sessao: Dict[str, Any]) -> str:
        """
        Gera um relatório formatado da sessão de aprendizado

        Args:
            sessao: Sessão de aprendizado

        Returns:
            String com relatório formatado
        """
        relatorio = f"""
📚 RELATÓRIO DE APRENDIZADO - {sessao['topico'].upper()}
{'=' * 60}

🎯 TÓPICO PRINCIPAL: {sessao['topico']}

📊 FONTES UTILIZADAS: {', '.join(sessao['fontes']) if sessao['fontes'] else 'Nenhuma'}

"""

        # Documentação
        if sessao["documentacao"]:
            doc = sessao["documentacao"]
            relatorio += f"""
📖 DOCUMENTAÇÃO ENCONTRADA:
• Repositório: {doc.get('repositorio', 'N/A')}
• Linguagem: {doc.get('linguagem', 'N/A')}
• Status: {'✅ Sucesso' if 'documentacao' in doc else '❌ Erro'}
"""

        # Exemplos
        if sessao["exemplos"]:
            relatorio += f"""
💻 EXEMPLOS PRÁTICOS ENCONTRADOS: {len(sessao['exemplos'])}

Exemplos disponíveis para análise detalhada.
"""

        # Comparações
        if sessao["comparacoes"]:
            comp = sessao["comparacoes"]
            linguagens = comp.get("linguagens", [])
            relatorio += f"""
🔄 COMPARAÇÕES DE IMPLEMENTAÇÃO:
• Linguagens encontradas: {', '.join(linguagens)}
• Total de comparações: {len(linguagens)}
"""

        relatorio += f"""
🎉 SESSÃO CONCLUÍDA COM SUCESSO!

💡 DICAS PARA APROFUNDAMENTO:
• Explore os exemplos de código em detalhes
• Compare implementações entre linguagens
• Teste os algoritmos com diferentes entradas
• Analise a complexidade de tempo e espaço

Fonte: GitMCP Integration 🤖
"""

        return relatorio


def demonstracao_gitmcp_aprendizado():
    """Demonstração completa do sistema de aprendizado com GitMCP"""
    print("🚀 DEMONSTRAÇÃO: APRENDIZADO COM GITMCP")
    print("=" * 60)

    # Verifica configuração
    config = MCPConfig()
    status = config.get_status()

    if not status["gitmcp"]["available"]:
        print("❌ GitMCP não está disponível")
        print("Verifique sua conexão com a internet")
        return

    print("✅ GitMCP disponível - Iniciando demonstração...")

    # Cria sistema de aprendizado
    aprendizado = AprendizadoComGitMCP()

    # Demonstra com diferentes tópicos
    topicos = ["quick sort", "binary search", "graph"]

    for topico in topicos:
        print(f"\n{'=' * 60}")
        print(f"🎯 ANALISANDO: {topico.upper()}")
        print("=" * 60)

        # Cria sessão de aprendizado
        sessao = aprendizado.criar_sessao_aprendizado(topico)

        # Gera relatório
        relatorio = aprendizado.gerar_relatorio_aprendizado(sessao)
        print(relatorio)

        # Pausa entre tópicos
        input("\n⏯️ Pressione Enter para continuar para o próximo tópico...")

    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("💡 O GitMCP está integrado e funcionando perfeitamente!")
    print("🔗 Você pode usar essas funcionalidades no seu sistema de algoritmos")


def exemplo_uso_simples():
    """Exemplo simples de uso do GitMCP"""
    print("💡 EXEMPLO SIMPLES DE USO")
    print("=" * 40)

    # Verifica se GitMCP está disponível
    config = MCPConfig()
    if not config.is_gitmcp_available():
        print("❌ GitMCP não disponível")
        return

    # Exemplo direto
    try:
        from gitmcp_integration import gitmcp_client

        print("🔍 Buscando documentação do repositório TheAlgorithms/Python...")
        docs = gitmcp_client.get_repository_info("TheAlgorithms", "Python")

        if docs["status"] == "success":
            print("✅ Documentação encontrada!")
            print(f"📖 Título: {docs.get('title', 'N/A')}")
            print(f"📝 Descrição: {docs.get('description', 'N/A')[:100]}...")

            print("\n🔍 Buscando exemplos de 'bubble sort'...")
            exemplos = gitmcp_client.search_code("TheAlgorithms", "Python", "bubble sort", max_results=2)

            if exemplos["status"] == "success":
                print(f"✅ Encontrados {exemplos.get('total_results', 0)} exemplos!")
            else:
                print("❌ Erro na busca de exemplos")

        else:
            print(f"❌ Erro: {docs.get('message', 'Erro desconhecido')}")

    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--simples":
        exemplo_uso_simples()
    else:
        demonstracao_gitmcp_aprendizado()
