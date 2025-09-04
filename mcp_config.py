#!/usr/bin/env python3
"""
Configuração e utilitários para MCP Server Tavily
"""

import os
import json
from pathlib import Path

class MCPConfig:
    """Gerenciador de configuração do MCP Server"""

    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = Path(__file__).parent

        self.project_root = Path(project_root)
        self.mcp_dir = self.project_root / "mcp-server-tavily"
        self.env_file = self.mcp_dir / ".env"

    def is_installed(self) -> bool:
        """Verifica se o MCP server está instalado"""
        return self.mcp_dir.exists() and (self.mcp_dir / "pyproject.toml").exists()

    def is_configured(self) -> bool:
        """Verifica se o MCP server está configurado"""
        if not self.env_file.exists():
            return False

        with open(self.env_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return ("TAVILY_API_KEY=" in content and
                "your_tavily_api_key_here" not in content and
                len(content.strip()) > 0)

    def get_status(self) -> dict:
        """Retorna status completo da configuração"""
        return {
            "installed": self.is_installed(),
            "configured": self.is_configured(),
            "mcp_directory": str(self.mcp_dir),
            "env_file": str(self.env_file),
            "has_api_key": self._has_api_key()
        }

    def _has_api_key(self) -> bool:
        """Verifica se há uma chave da API configurada"""
        if not self.env_file.exists():
            return False

        with open(self.env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("TAVILY_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    return key != "" and key != "your_tavily_api_key_here"

        return False

    def setup_instructions(self) -> str:
        """Retorna instruções de configuração"""
        instructions = """
🔧 CONFIGURAÇÃO DO MCP SERVER TAVILY
=====================================

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

4. 📚 Exemplos:
   • Execute: python exemplo_integracao_mcp.py

STATUS ATUAL:
"""

        status = self.get_status()
        instructions += f"• Instalado: {'✅' if status['installed'] else '❌'}\n"
        instructions += f"• Configurado: {'✅' if status['configured'] else '❌'}\n"
        instructions += f"• Chave API: {'✅' if status['has_api_key'] else '❌'}\n"

        if not status['configured']:
            instructions += "\n❌ PRÓXIMOS PASSOS:\n"
            instructions += "   1. Configure a chave da API no arquivo .env\n"
            instructions += "   2. Teste com: python exemplo_integracao_mcp.py\n"

        return instructions

def verificar_configuracao():
    """Função de conveniência para verificar configuração"""
    config = MCPConfig()
    print(config.setup_instructions())

    status = config.get_status()
    if status['installed'] and status['configured']:
        print("\n🎉 MCP Server pronto para uso!")
        print("💡 Dica: Execute 'python exemplo_integracao_mcp.py' para testar")
    else:
        print("\n⚠️ Configuração incompleta. Siga as instruções acima.")

if __name__ == "__main__":
    verificar_configuracao()
