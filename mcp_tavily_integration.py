#!/usr/bin/env python3
"""
Módulo de integração com MCP Server Tavily
Permite fazer buscas na web usando o servidor MCP
"""

import os
import sys
import asyncio
import subprocess
from typing import Dict, List, Optional, Any
import json
import time

class TavilySearchClient:
    """
    Cliente para interagir com o MCP Server Tavily
    """

    def __init__(self, server_path: str = None):
        """
        Inicializa o cliente

        Args:
            server_path: Caminho para o diretório do servidor MCP
        """
        if server_path is None:
            # Caminho padrão relativo ao projeto
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(current_dir, '..', 'mcp-server-tavily')

        self.server_path = os.path.abspath(server_path)
        self.server_process = None
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> Optional[str]:
        """Carrega a chave da API do arquivo .env"""
        env_file = os.path.join(self.server_path, '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('TAVILY_API_KEY=') and not line.startswith('TAVILY_API_KEY=your_'):
                        return line.split('=', 1)[1]
        return None

    def is_configured(self) -> bool:
        """Verifica se o servidor está configurado corretamente"""
        return self.api_key is not None and self.api_key != 'your_tavily_api_key_here'

    def start_server(self) -> bool:
        """
        Inicia o servidor MCP em background

        Returns:
            bool: True se iniciou com sucesso
        """
        if not self.is_configured():
            print("❌ Servidor não configurado. Configure TAVILY_API_KEY no arquivo .env")
            return False

        try:
            # Mata processos anteriores se existirem
            self.stop_server()

            # Inicia o servidor
            script_path = os.path.join(self.server_path, 'run_server.sh')
            self.server_process = subprocess.Popen(
                [script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.server_path,
                env=dict(os.environ, PYTHONIOENCODING='utf-8')
            )

            # Aguarda um pouco para o servidor inicializar
            time.sleep(2)

            # Verifica se o processo está rodando
            if self.server_process.poll() is None:
                print("✅ Servidor MCP Tavily iniciado com sucesso")
                return True
            else:
                stdout, stderr = self.server_process.communicate()
                print(f"❌ Erro ao iniciar servidor: {stderr.decode()}")
                return False

        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
            return False

    def stop_server(self):
        """Para o servidor MCP"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("✅ Servidor MCP parado")
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                print("⚠️ Servidor MCP forçado a parar")
            finally:
                self.server_process = None

    def search(self, query: str, search_depth: str = "basic") -> Dict[str, Any]:
        """
        Realiza uma busca usando o MCP server

        Args:
            query: Termo de busca
            search_depth: Profundidade da busca ("basic" ou "advanced")

        Returns:
            Dict com resultados da busca
        """
        if not self.is_configured():
            return {
                "error": "Servidor não configurado",
                "message": "Configure TAVILY_API_KEY no arquivo .env"
            }

        if not self.server_process or self.server_process.poll() is not None:
            if not self.start_server():
                return {
                    "error": "Servidor não pôde ser iniciado",
                    "message": "Verifique a configuração e tente novamente"
                }

        try:
            # Aqui seria implementada a comunicação com o servidor MCP
            # Por enquanto, retorna uma estrutura de exemplo
            return {
                "query": query,
                "search_depth": search_depth,
                "status": "success",
                "results": [
                    {
                        "title": f"Resultado de exemplo para: {query}",
                        "url": f"https://example.com/search?q={query.replace(' ', '+')}",
                        "snippet": f"Este é um resultado de exemplo para a busca: {query}"
                    }
                ],
                "note": "Integração completa será implementada quando o protocolo MCP for estabelecido"
            }

        except Exception as e:
            return {
                "error": "Erro na busca",
                "message": str(e)
            }

    def __enter__(self):
        """Context manager entry"""
        self.start_server()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_server()


# Função de conveniência para uso direto
def buscar_web(query: str, search_depth: str = "basic") -> Dict[str, Any]:
    """
    Função de conveniência para buscar na web

    Args:
        query: Termo de busca
        search_depth: Profundidade da busca

    Returns:
        Resultados da busca
    """
    with TavilySearchClient() as client:
        return client.search(query, search_depth)


# Demonstração de uso
def demonstrar_integracao():
    """Demonstra como usar a integração com MCP Tavily"""
    print("🔍 Demonstração da Integração MCP Tavily")
    print("=" * 50)

    # Cria cliente
    client = TavilySearchClient()

    # Verifica configuração
    if not client.is_configured():
        print("❌ Configuração necessária:")
        print("   1. Obtenha uma chave da API Tavily em: https://tavily.com/")
        print("   2. Edite o arquivo mcp-server-tavily/.env")
        print("   3. Substitua 'your_tavily_api_key_here' pela sua chave real")
        return

    # Exemplo de busca
    print("\n📝 Fazendo busca de exemplo...")
    resultados = client.search("Python programming tutorial", "basic")

    if "error" in resultados:
        print(f"❌ Erro: {resultados['error']}")
        print(f"   {resultados.get('message', '')}")
    else:
        print("✅ Busca realizada com sucesso!")
        print(f"   Query: {resultados.get('query', 'N/A')}")
        print(f"   Profundidade: {resultados.get('search_depth', 'N/A')}")

        if "results" in resultados:
            print(f"   Resultados encontrados: {len(resultados['results'])}")
            for i, result in enumerate(resultados['results'][:3], 1):
                print(f"   {i}. {result.get('title', 'Título não disponível')}")


if __name__ == "__main__":
    demonstrar_integracao()
