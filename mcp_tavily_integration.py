#!/usr/bin/env python3
"""
Módulo de integração com Tavily API
Permite fazer buscas na web usando o SDK oficial do Tavily
"""

import os
import sys
from typing import Dict, List, Optional, Any
from tavily import TavilyClient

class TavilySearchClient:
    """
    Cliente para interagir com a API Tavily
    """

    def __init__(self, server_path: str = None):
        """
        Inicializa o cliente Tavily

        Args:
            server_path: Caminho para o diretório do servidor (mantido para compatibilidade)
        """
        self.api_key = self._load_api_key()
        self.client = None
        
        if self.api_key:
            try:
                self.client = TavilyClient(api_key=self.api_key)
            except Exception as e:
                print(f"Erro ao inicializar cliente Tavily: {e}")
                self.client = None

    def _load_api_key(self) -> Optional[str]:
        """Carrega a chave da API do arquivo .env"""
        env_file = os.path.join(os.path.dirname(__file__), 'mcp-server-tavily', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('TAVILY_API_KEY=') and not line.startswith('TAVILY_API_KEY=your_'):
                        return line.split('=', 1)[1]
        return None

    def is_configured(self) -> bool:
        """Verifica se o cliente está configurado corretamente"""
        return self.client is not None and self.api_key is not None

    def search(self, query: str, search_depth: str = "basic", **kwargs) -> Dict[str, Any]:
        """
        Realiza uma busca usando a API Tavily

        Args:
            query: Termo de busca
            search_depth: Profundidade da busca ("basic" ou "advanced")
            **kwargs: Parâmetros adicionais para a busca

        Returns:
            Dict com resultados da busca
        """
        if not self.is_configured():
            return {
                "error": "Cliente não configurado",
                "message": "Configure TAVILY_API_KEY no arquivo .env"
            }

        try:
            # Configurar parâmetros da busca
            search_params = {
                "query": query,
                "search_depth": search_depth,
                "max_results": kwargs.get("max_results", 5),
                "include_answer": kwargs.get("include_answer", False),
                "include_raw_content": kwargs.get("include_raw_content", False),
                "include_images": kwargs.get("include_images", False),
            }
            
            # Adicionar parâmetros adicionais se fornecidos
            if "topic" in kwargs:
                search_params["topic"] = kwargs["topic"]
            if "include_domains" in kwargs:
                search_params["include_domains"] = kwargs["include_domains"]
            if "exclude_domains" in kwargs:
                search_params["exclude_domains"] = kwargs["exclude_domains"]

            # Realizar a busca
            response = self.client.search(**search_params)
            
            # Formatar resposta para compatibilidade
            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append({
                    "title": result.get("title", "Sem título"),
                    "url": result.get("url", ""),
                    "snippet": result.get("content", ""),
                    "content": result.get("raw_content", ""),
                    "score": result.get("score", 0.0)
                })
            
            return {
                "query": query,
                "search_depth": search_depth,
                "status": "success",
                "results": formatted_results,
                "answer": response.get("answer"),
                "response_time": response.get("response_time", 0.0),
                "total_results": len(formatted_results)
            }

        except Exception as e:
            return {
                "error": "Erro na busca",
                "message": str(e),
                "query": query,
                "search_depth": search_depth
            }

    def extract(self, urls: List[str], **kwargs) -> Dict[str, Any]:
        """
        Extrai conteúdo de URLs usando Tavily Extract

        Args:
            urls: Lista de URLs para extrair
            **kwargs: Parâmetros adicionais

        Returns:
            Dict com conteúdo extraído
        """
        if not self.is_configured():
            return {
                "error": "Cliente não configurado",
                "message": "Configure TAVILY_API_KEY no arquivo .env"
            }

        try:
            response = self.client.extract(urls=urls, **kwargs)
            
            # Formatar resposta
            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append({
                    "url": result.get("url", ""),
                    "content": result.get("raw_content", ""),
                    "images": result.get("images", [])
                })
            
            return {
                "status": "success",
                "results": formatted_results,
                "failed_results": response.get("failed_results", []),
                "response_time": response.get("response_time", 0.0)
            }
            
        except Exception as e:
            return {
                "error": "Erro na extração",
                "message": str(e)
            }
