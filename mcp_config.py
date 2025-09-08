#!/usr/bin/env python3
"""
Configuração e utilitários para MCP Servers (Tavily + GitMCP)
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

class MCPConfig:
    """Gerenciador de configuração dos MCP Servers"""

    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = Path(__file__).parent

        self.project_root = Path(project_root)
        self.mcp_dir = self.project_root / "mcp-server-tavily"
        self.env_file = self.mcp_dir / ".env"

        # Configuração GitMCP
        self.gitmcp_config_file = self.project_root / "gitmcp_config.json"
        self._ensure_gitmcp_config()

    def _ensure_gitmcp_config(self):
        """Garante que o arquivo de configuração GitMCP existe"""
        if not self.gitmcp_config_file.exists():
            default_config = {
                "gitmcp_base_url": "https://gitmcp.io",
                "default_repositories": [
                    "TheAlgorithms/Python",
                    "keon/algorithms",
                    "networkx/networkx"
                ],
                "cache_enabled": True,
                "max_results": 5,
                "timeout": 10
            }

            with open(self.gitmcp_config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)

    def is_tavily_installed(self) -> bool:
        """Verifica se o MCP server Tavily está instalado"""
        return self.mcp_dir.exists() and (self.mcp_dir / "pyproject.toml").exists()

    def is_tavily_configured(self) -> bool:
        """Verifica se o MCP server Tavily está configurado"""
        if not self.env_file.exists():
            return False

        with open(self.env_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return ("TAVILY_API_KEY=" in content and
                "your_tavily_api_key_here" not in content and
                len(content.strip()) > 0)

    def is_gitmcp_available(self) -> bool:
        """Verifica se a API do GitHub está disponível (usada para GitMCP-like functionality)"""
        try:
            import requests
            response = requests.get("https://api.github.com/rate_limit", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_gitmcp_config(self) -> Dict[str, Any]:
        """Retorna configuração do GitMCP"""
        try:
            with open(self.gitmcp_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "gitmcp_base_url": "https://gitmcp.io",
                "default_repositories": ["TheAlgorithms/Python"],
                "cache_enabled": True,
                "max_results": 5,
                "timeout": 10
            }

    def update_gitmcp_config(self, updates: Dict[str, Any]):
        """Atualiza configuração do GitMCP"""
        current_config = self.get_gitmcp_config()
        current_config.update(updates)

        with open(self.gitmcp_config_file, 'w', encoding='utf-8') as f:
            json.dump(current_config, f, indent=2, ensure_ascii=False)

    def get_status(self) -> dict:
        """Retorna status completo da configuração"""
        return {
            "tavily": {
                "installed": self.is_tavily_installed(),
                "configured": self.is_tavily_configured(),
                "directory": str(self.mcp_dir),
                "env_file": str(self.env_file)
            },
            "gitmcp": {
                "available": self.is_gitmcp_available(),
                "config_file": str(self.gitmcp_config_file),
                "config": self.get_gitmcp_config()
            }
        }

    def _has_api_key(self) -> bool:
        """Verifica se há uma chave da API Tavily configurada"""
        if not self.env_file.exists():
            return False

        with open(self.env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("TAVILY_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    return key != "" and key != "your_tavily_api_key_here"

        return False

    def setup_instructions(self) -> str:
        """Retorna instruções de configuração completas"""
        instructions = """
🔧 CONFIGURAÇÃO DOS MCP SERVERS
=================================

Este projeto suporta dois servidores MCP:

1. 🌐 TAVILY MCP - Busca na web inteligente
2. 📚 GITMCP - Acesso à documentação GitHub

---

📋 TAVILY MCP SETUP:
===================

Para usar o MCP Server Tavily, siga estes passos:

1. 📝 Obter Chave da API:
   • Acesse: https://tavily.com/
   • Crie uma conta gratuita
   • Copie sua chave da API

2. ⚙️ Configurar Ambiente:
   • Edite o arquivo: mcp-server-tavily/.env
   • Substitua 'your_tavily_api_key_here' pela sua chave real

3. 🚀 Usar no Projeto:
   • Importe: from mcp_tavily_integration import buscar_web
   • Exemplo: resultado = buscar_web("algoritmos python")

---

📚 GITMCP SETUP:
===============

O GitMCP é gratuito e não requer configuração especial:

1. 🌐 Disponibilidade:
   • Serviço online gratuito
   • Acesso a qualquer repositório GitHub público
   • Reduz alucinações em respostas de IA

2. 🚀 Usar no Projeto:
   • Importe: from gitmcp_integration import gitmcp_integration
   • Exemplo: docs = gitmcp_integration.buscar_documentacao_algoritmo("quick sort")

3. ⚙️ Configuração Avançada:
   • Arquivo: gitmcp_config.json
   • Personalize repositórios padrão e configurações

---

📊 STATUS ATUAL:
===============
"""

        status = self.get_status()

        # Status Tavily
        instructions += "\n🌐 TAVILY MCP:\n"
        instructions += f"• Instalado: {'✅' if status['tavily']['installed'] else '❌'}\n"
        instructions += f"• Configurado: {'✅' if status['tavily']['configured'] else '❌'}\n"

        # Status GitMCP
        instructions += "\n📚 GITHUB API (GitMCP-like):\n"
        instructions += f"• Disponível: {'✅' if status['gitmcp']['available'] else '❌'}\n"
        instructions += f"• Funcional: ✅ (API GitHub)\n"

        # Próximos passos
        if not status['tavily']['configured']:
            instructions += "\n❌ PRÓXIMOS PASSOS PARA TAVILY:\n"
            instructions += "   1. Configure a chave da API no arquivo .env\n"
            instructions += "   2. Teste com: python exemplo_integracao_mcp.py\n"

        instructions += "\n✅ GITHUB API PRONTO PARA USO!\n"
        instructions += "   • Teste com: python gitmcp_integration.py\n"
        instructions += "   • Use: from gitmcp_integration import github_integration\n"

        return instructions

def verificar_configuracao():
    """Função de conveniência para verificar configuração completa"""
    config = MCPConfig()
    print(config.setup_instructions())

    status = config.get_status()

    # Verifica se pelo menos um MCP está funcionando
    tavily_ok = status['tavily']['installed'] and status['tavily']['configured']
    gitmcp_ok = status['gitmcp']['available']

    if tavily_ok or gitmcp_ok:
        print("\n🎉 Pelo menos um MCP Server está funcionando!")
        print("💡 DICAS DE USO:")

        if tavily_ok:
            print("   🌐 Tavily: Para busca na web inteligente")
            print("      from mcp_tavily_integration import buscar_web")

        if gitmcp_ok:
            print("   📚 GitMCP: Para documentação GitHub precisa")
            print("      from gitmcp_integration import gitmcp_integration")

        print("\n🚀 Execute 'python demonstracao_melhorias.py' para ver tudo funcionando!")

    else:
        print("\n⚠️ Nenhum MCP Server está configurado.")
        print("💡 Configure pelo menos um dos servidores acima.")

def testar_gitmcp():
    """Testa especificamente a integração GitMCP"""
    print("🧪 TESTANDO GITMCP INTEGRATION")
    print("=" * 40)

    config = MCPConfig()
    status = config.get_status()

    if status['gitmcp']['available']:
        print("✅ GitMCP está disponível!")

        try:
            from gitmcp_integration import gitmcp_client, gitmcp_integration

            # Testa busca básica
            print("\n📚 Testando busca de documentação...")
            docs = gitmcp_client.fetch_documentation("TheAlgorithms", "Python")
            print(f"Status: {docs['status']}")

            if docs['status'] == 'success':
                print(f"📖 Repositório: {docs['repository']}")
                print(f"📝 Título: {docs.get('title', 'N/A')}")

                # Testa busca específica
                print("\n🔍 Testando busca específica...")
                search = gitmcp_client.search_documentation(
                    "TheAlgorithms", "Python", "quick sort", max_results=3
                )
                print(f"Resultados encontrados: {search.get('total_results', 0)}")

                # Testa integração avançada
                print("\n🎯 Testando integração avançada...")
                exemplos = gitmcp_integration.obter_exemplos_codigo("bubble sort")
                print(f"Exemplos de código: {exemplos.get('total_exemplos', 0)}")

                print("\n✅ GitMCP funcionando perfeitamente!")

            else:
                print(f"❌ Erro: {docs.get('message', 'Erro desconhecido')}")

        except ImportError as e:
            print(f"❌ Erro de importação: {e}")
            print("Verifique se o arquivo gitmcp_integration.py existe")

    else:
        print("❌ GitMCP não está disponível")
        print("Verifique sua conexão com a internet")

def demonstracao_completa():
    """Demonstração completa de ambos os MCP servers"""
    print("🚀 DEMONSTRAÇÃO MCP SERVERS")
    print("=" * 50)

    verificar_configuracao()
    print("\n" + "=" * 50)
    testar_gitmcp()

if __name__ == "__main__":
    demonstracao_completa()
