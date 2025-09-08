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
        """Carrega a chave da API do arquivo .env ou st.secrets"""
        # Primeiro tenta carregar do st.secrets (Streamlit Cloud)
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'TAVILY_API_KEY' in st.secrets:
                return st.secrets['TAVILY_API_KEY']
        except ImportError:
            pass

        # Fallback para arquivo .env (desenvolvimento local)
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

    def search_with_context(self, query: str, context: str = "", language: str = "pt", **kwargs) -> Dict[str, Any]:
        """
        Busca com geração de resposta contextualizada
        
        Args:
            query: Termo de busca
            context: Contexto adicional para melhorar a resposta
            language: Idioma da resposta ("pt", "en", "es", etc.)
            **kwargs: Parâmetros adicionais
            
        Returns:
            Dict com resultados e resposta contextualizada
        """
        if not self.is_configured():
            return {
                "error": "Cliente não configurado",
                "message": "Configure TAVILY_API_KEY no arquivo .env"
            }

        try:
            # Query aprimorada com contexto
            enhanced_query = f"{query} {context}".strip()
            
            # Configurar parâmetros com suporte multilíngue
            search_params = {
                "query": enhanced_query,
                "search_depth": kwargs.get("search_depth", "advanced"),
                "max_results": kwargs.get("max_results", 10),
                "include_answer": True,
                "include_raw_content": True,
                "include_images": False,
            }
            
            # Adicionar idioma se suportado
            if language != "en":
                search_params["query"] = f"{search_params['query']} (responda em {language})"
            
            response = self.client.search(**search_params)
            
            # Gerar resposta contextualizada
            contextual_answer = self._generate_contextual_answer(
                query, 
                response.get("results", []), 
                context,
                language
            )
            
            return {
                "query": query,
                "enhanced_query": enhanced_query,
                "context": context,
                "language": language,
                "status": "success",
                "results": response.get("results", []),
                "answer": response.get("answer"),
                "contextual_answer": contextual_answer,
                "response_time": response.get("response_time", 0.0)
            }
            
        except Exception as e:
            return {
                "error": "Erro na busca contextual",
                "message": str(e),
                "query": query,
                "context": context
            }

    def _generate_contextual_answer(self, query: str, results: List[Dict], context: str, language: str) -> str:
        """
        Gera resposta contextualizada baseada nos resultados
        
        Args:
            query: Query original
            results: Resultados da busca
            context: Contexto adicional
            language: Idioma da resposta
            
        Returns:
            Resposta contextualizada
        """
        if not results:
            return "Não foram encontrados resultados relevantes."
        
        # Extrair informações relevantes
        relevant_info = []
        for result in results[:5]:  # Top 5 resultados
            title = result.get("title", "")
            content = result.get("content", "")[:200]  # Limitar conteúdo
            if content:
                relevant_info.append(f"- {title}: {content}")
        
        # Gerar resposta baseada no idioma
        if language == "pt":
            contextual_answer = f"""
Com base na busca por "{query}"{' e no contexto fornecido' if context else ''}:

{chr(10).join(relevant_info)}

Esta informação foi obtida de fontes confiáveis na web e pode ajudar no seu aprendizado sobre algoritmos.
            """.strip()
        elif language == "es":
            contextual_answer = f"""
Basado en la búsqueda de "{query}"{' y el contexto proporcionado' if context else ''}:

{chr(10).join(relevant_info)}

Esta información fue obtenida de fuentes confiables en la web y puede ayudar en su aprendizaje sobre algoritmos.
            """.strip()
        else:  # English default
            contextual_answer = f"""
Based on the search for "{query}"{' and the provided context' if context else ''}:

{chr(10).join(relevant_info)}

This information was obtained from reliable web sources and can help with your algorithm learning.
            """.strip()
        
        return contextual_answer

    def advanced_search(self, query: str, depth: str = "advanced", domains: List[str] = None, 
                       exclude_domains: List[str] = None, language: str = "pt") -> Dict[str, Any]:
        """
        Busca avançada com controle fino de profundidade e domínios
        
        Args:
            query: Termo de busca
            depth: Profundidade ("basic", "advanced")
            domains: Lista de domínios para incluir
            exclude_domains: Lista de domínios para excluir
            language: Idioma da busca
            
        Returns:
            Dict com resultados avançados
        """
        if not self.is_configured():
            return {
                "error": "Cliente não configurado"
            }

        try:
            search_params = {
                "query": query,
                "search_depth": depth,
                "max_results": 15,
                "include_answer": True,
                "include_raw_content": True,
            }
            
            if domains:
                search_params["include_domains"] = domains
            if exclude_domains:
                search_params["exclude_domains"] = exclude_domains
                
            # Suporte multilíngue
            if language != "en":
                search_params["query"] = f"{query} (in {language})"
            
            response = self.client.search(**search_params)
            
            # Análise de qualidade dos resultados
            quality_analysis = self._analyze_results_quality(response.get("results", []))
            
            return {
                "query": query,
                "depth": depth,
                "language": language,
                "domains_included": domains,
                "domains_excluded": exclude_domains,
                "status": "success",
                "results": response.get("results", []),
                "answer": response.get("answer"),
                "quality_analysis": quality_analysis,
                "total_results": len(response.get("results", [])),
                "response_time": response.get("response_time", 0.0)
            }
            
        except Exception as e:
            return {
                "error": "Erro na busca avançada",
                "message": str(e)
            }

    def _analyze_results_quality(self, results: List[Dict]) -> Dict[str, Any]:
        """
        Analisa a qualidade dos resultados da busca
        
        Args:
            results: Lista de resultados
            
        Returns:
            Dict com análise de qualidade
        """
        if not results:
            return {"quality_score": 0, "analysis": "Sem resultados"}
        
        total_score = 0
        high_quality_count = 0
        educational_count = 0
        
        for result in results:
            score = result.get("score", 0.5)
            total_score += score
            
            if score > 0.8:
                high_quality_count += 1
                
            # Verificar se é fonte educacional
            url = result.get("url", "").lower()
            title = result.get("title", "").lower()
            
            educational_keywords = ["tutorial", "guide", "learn", "course", "documentation", 
                                  "edu", "university", "academy", "school"]
            
            if any(keyword in url or keyword in title for keyword in educational_keywords):
                educational_count += 1
        
        avg_score = total_score / len(results)
        
        analysis = {
            "quality_score": round(avg_score, 2),
            "high_quality_results": high_quality_count,
            "educational_sources": educational_count,
            "total_results": len(results),
            "recommendation": "Excelente" if avg_score > 0.8 else "Bom" if avg_score > 0.6 else "Melhorar busca"
        }
        
        return analysis
