#!/usr/bin/env python3
"""
Integração com GitHub API - Acesso inteligente à documentação GitHub
Permite acesso direto à documentação e código de repositórios GitHub
"""

import os
import sys
import json
import requests
import base64
from typing import Dict, List, Optional, Any


class GitHubDocsClient:
    """
    Cliente para acesso à documentação GitHub
    Usa API do GitHub para obter README e documentação
    """

    def __init__(self, github_token: str = None):
        """
        Inicializa o cliente GitHub

        Args:
            github_token: Token do GitHub (opcional, aumenta limite de requests)
        """
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Algoritmos-Visualizador/1.0", "Accept": "application/vnd.github.v3+json"})

        # Prioriza st.secrets (Streamlit Cloud), depois parâmetro, depois variável de ambiente
        token = None
        if github_token:
            token = github_token
        else:
            # Tenta carregar do st.secrets (Streamlit Cloud)
            try:
                import streamlit as st

                if hasattr(st, "secrets"):
                    try:
                        token = st.secrets.get("GITHUB_TOKEN")
                    except Exception:
                        # Handle missing secrets gracefully
                        pass
            except ImportError:
                pass

            # Fallback para variável de ambiente
            if not token:
                token = os.getenv("GITHUB_TOKEN")

        if token:
            self.session.headers["Authorization"] = f"token {token}"

    def is_available(self) -> bool:
        """
        Verifica se a API do GitHub está disponível

        Returns:
            bool: True se a API estiver acessível
        """
        try:
            response = self.session.get(f"{self.base_url}/rate_limit", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Obtém informações básicas de um repositório

        Args:
            owner: Proprietário do repositório
            repo: Nome do repositório

        Returns:
            Dict com informações do repositório
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            return {
                "status": "success",
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "language": data.get("language"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "topics": data.get("topics", []),
                "html_url": data.get("html_url"),
                "updated_at": data.get("updated_at"),
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "repository": f"{owner}/{repo}",
                "error": str(e),
                "message": "Erro ao obter informações do repositório",
            }

    def get_readme(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Obtém o README de um repositório

        Args:
            owner: Proprietário do repositório
            repo: Nome do repositório

        Returns:
            Dict com conteúdo do README
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/readme"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            content = data.get("content", "")

            # Decodifica base64 se necessário
            if data.get("encoding") == "base64":
                content = base64.b64decode(content).decode("utf-8")

            return {
                "status": "success",
                "repository": f"{owner}/{repo}",
                "filename": data.get("name", "README.md"),
                "content": content,
                "size": data.get("size", 0),
                "download_url": data.get("download_url"),
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "repository": f"{owner}/{repo}", "error": str(e), "message": "Erro ao obter README"}

    def search_code(self, owner: str, repo: str, query: str, language: str = None, max_results: int = 5) -> Dict[str, Any]:
        """
        Busca código em um repositório usando a API do GitHub

        Args:
            owner: Proprietário do repositório
            repo: Nome do repositório
            query: Termo de busca no código
            language: Linguagem de programação (opcional)
            max_results: Número máximo de resultados

        Returns:
            Dict com resultados da busca de código
        """
        try:
            url = f"{self.base_url}/search/code"
            params = {"q": f"repo:{owner}/{repo} {query}", "per_page": max_results}

            if language:
                params["q"] += f" language:{language}"

            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            # Processa os resultados
            results = []
            for item in items:
                results.append(
                    {
                        "name": item.get("name"),
                        "path": item.get("path"),
                        "url": item.get("html_url"),
                        "repository": item.get("repository", {}).get("full_name"),
                        "score": item.get("score", 0),
                    }
                )

            return {
                "status": "success",
                "query": query,
                "repository": f"{owner}/{repo}",
                "language": language,
                "results": results,
                "total_results": len(results),
                "github_total": data.get("total_count", 0),
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "query": query,
                "repository": f"{owner}/{repo}",
                "error": str(e),
                "message": "Erro ao buscar código",
            }

    def get_file_content(self, owner: str, repo: str, path: str) -> Dict[str, Any]:
        """
        Obtém conteúdo de um arquivo específico

        Args:
            owner: Proprietário do repositório
            repo: Nome do repositório
            path: Caminho do arquivo

        Returns:
            Dict com conteúdo do arquivo
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            content = data.get("content", "")

            # Decodifica base64 se necessário
            if data.get("encoding") == "base64":
                content = base64.b64decode(content).decode("utf-8")

            return {
                "status": "success",
                "repository": f"{owner}/{repo}",
                "path": path,
                "name": data.get("name"),
                "content": content,
                "size": data.get("size", 0),
                "download_url": data.get("download_url"),
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "repository": f"{owner}/{repo}",
                "path": path,
                "error": str(e),
                "message": "Erro ao obter conteúdo do arquivo",
            }


class GitMCPIntegration:
    """
    Integração completa para acesso à documentação GitHub
    """

    def __init__(self):
        self.client = GitHubDocsClient()
        self.cache = {}

    def buscar_documentacao_algoritmo(self, algoritmo: str, linguagem: str = "python") -> Dict[str, Any]:
        """
        Busca documentação específica para algoritmos

        Args:
            algoritmo: Nome do algoritmo
            linguagem: Linguagem de programação

        Returns:
            Dict com documentação encontrada
        """
        print(f"🔍 Buscando documentação para: {algoritmo} ({linguagem})")

        # Mapeamento de algoritmos para repositórios relevantes
        repos_map = {
            "sort": ["TheAlgorithms/Python", "keon/algorithms"],
            "search": ["TheAlgorithms/Python", "keon/algorithms"],
            "graph": ["TheAlgorithms/Python", "networkx/networkx"],
            "tree": ["TheAlgorithms/Python", "keon/algorithms"],
            "dynamic": ["TheAlgorithms/Python", "keon/algorithms"],
            "machine_learning": ["scikit-learn/scikit-learn", "tensorflow/tensorflow"],
        }

        algoritmo_key = algoritmo.lower().replace(" ", "_")
        repos = repos_map.get(algoritmo_key, ["TheAlgorithms/Python"])

        resultados = []

        for repo_full in repos:
            if "/" in repo_full:
                owner, repo = repo_full.split("/", 1)
            else:
                continue

            # Obtém informações do repositório
            repo_info = self.client.get_repository_info(owner, repo)
            readme = self.client.get_readme(owner, repo)

            if repo_info["status"] == "success":
                resultados.append(
                    {"repositorio": repo_full, "info": repo_info, "readme": readme if readme["status"] == "success" else None}
                )

        return {"algoritmo": algoritmo, "linguagem": linguagem, "resultados": resultados, "total_encontrados": len(resultados)}

    def obter_exemplos_codigo(self, conceito: str, linguagem: str = "python") -> Dict[str, Any]:
        """
        Obtém exemplos de código para um conceito específico

        Args:
            conceito: Conceito ou algoritmo
            linguagem: Linguagem de programação

        Returns:
            Dict com exemplos de código
        """
        print(f"💻 Buscando exemplos para: {conceito} ({linguagem})")

        # Busca nos repositórios mais relevantes
        repos = ["TheAlgorithms/Python", "keon/algorithms"]

        exemplos = []

        for repo_full in repos:
            owner, repo = repo_full.split("/", 1)

            # Busca código
            code_search = self.client.search_code(owner, repo, conceito, language=linguagem, max_results=5)

            if code_search["status"] == "success" and code_search["results"]:
                # Para cada resultado, obtém o conteúdo completo
                for result in code_search["results"]:
                    file_content = self.client.get_file_content(owner, repo, result["path"])
                    if file_content["status"] == "success":
                        exemplos.append(
                            {
                                "repositorio": repo_full,
                                "arquivo": result["name"],
                                "caminho": result["path"],
                                "url": result["url"],
                                "conteudo": file_content["content"],
                                "score": result["score"],
                            }
                        )

        return {
            "conceito": conceito,
            "linguagem": linguagem,
            "exemplos": exemplos[:10],  # Limita a 10 exemplos
            "total_exemplos": len(exemplos),
        }

    def comparar_implementacoes(self, algoritmo: str) -> Dict[str, Any]:
        """
        Compara diferentes implementações de um algoritmo

        Args:
            algoritmo: Nome do algoritmo

        Returns:
            Dict com comparações de implementações
        """
        print(f"🔄 Comparando implementações de: {algoritmo}")

        repos = ["TheAlgorithms/Python", "keon/algorithms"]

        comparacoes = {}

        for repo_full in repos:
            owner, repo = repo_full.split("/", 1)
            linguagem = "python"  # Ambos são Python

            # Busca implementação
            search = self.client.search_code(owner, repo, algoritmo, max_results=3)

            if search["status"] == "success" and search["results"]:
                if linguagem not in comparacoes:
                    comparacoes[linguagem] = []

                for result in search["results"]:
                    file_content = self.client.get_file_content(owner, repo, result["path"])
                    if file_content["status"] == "success":
                        comparacoes[linguagem].append(
                            {
                                "repositorio": repo_full,
                                "arquivo": result["name"],
                                "conteudo": file_content["content"],
                                "url": result["url"],
                            }
                        )

        return {"algoritmo": algoritmo, "comparacoes": comparacoes, "linguagens": list(comparacoes.keys())}

    def buscar_modelos_ml(self, query: str = "", formato: str = None, max_results: int = 10) -> Dict[str, Any]:
        """
        Busca modelos de machine learning no GitHub

        Args:
            query: Termo de busca (ex: "resnet", "yolo", etc.)
            formato: Formato específico (.onnx, .tflite, .h5, .pt, .pth, .mlmodel)
            max_results: Número máximo de resultados

        Returns:
            Dict com modelos encontrados
        """
        print(f"🤖 Buscando modelos ML: {query} (formato: {formato})")

        # Extensões suportadas pelo Netron
        extensoes_suportadas = {
            "onnx": [".onnx"],
            "tflite": [".tflite"],
            "keras": [".h5", ".keras"],
            "pytorch": [".pt", ".pth", ".pkl"],
            "coreml": [".mlmodel"],
            "darknet": [".cfg", ".weights"],
            "tensorflow": [".pb", ".meta"],
            "caffe": [".caffemodel", ".prototxt"],
            "todos": [".onnx", ".tflite", ".h5", ".keras", ".pt", ".pth", ".pkl", ".mlmodel", ".cfg", ".weights", ".pb", ".meta", ".caffemodel", ".prototxt"]
        }

        # Define extensões a buscar
        if formato and formato in extensoes_suportadas:
            extensoes = extensoes_suportadas[formato]
        else:
            extensoes = extensoes_suportadas["todos"]

        modelos = []

        # Busca em repositórios populares de ML
        repos_populares = [
            "onnx/models",
            "tensorflow/models",
            "pytorch/vision",
            "keras-team/keras-applications",
            "microsoft/onnxruntime",
            "tensorflow/tfhub.dev",
            "google/mediapipe",
            "apple/coremltools",
            "ultralytics/yolov5",
            "facebookresearch/detectron2"
        ]

        # Também faz busca geral no GitHub
        try:
            # Constrói query para busca geral
            search_query = f"{query} " if query else ""
            search_query += " OR ".join([f"extension:{ext[1:]}" for ext in extensoes])  # Remove o ponto
            search_query += " size:>1000"  # Arquivos maiores que 1KB (modelos são grandes)

            url = f"{self.client.base_url}/search/code"
            params = {
                "q": search_query,
                "per_page": min(max_results * 2, 100),  # Busca mais para filtrar depois
                "sort": "indexed",
                "order": "desc"
            }

            response = self.client.session.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            # Processa resultados
            for item in items[:max_results]:
                repo_full = item.get("repository", {}).get("full_name", "")
                filename = item.get("name", "")
                path = item.get("path", "")

                # Verifica se é uma extensão suportada
                if any(filename.endswith(ext) for ext in extensoes):
                    # Obtém informações do repositório
                    if "/" in repo_full:
                        owner, repo = repo_full.split("/", 1)
                        repo_info = self.client.get_repository_info(owner, repo)

                        modelos.append({
                            "nome": filename,
                            "caminho": path,
                            "repositorio": repo_full,
                            "url": item.get("html_url", ""),
                            "download_url": f"https://raw.githubusercontent.com/{repo_full}/main/{path}",
                            "formato": self._identificar_formato(filename),
                            "tamanho_kb": "Desconhecido",  # API não retorna tamanho diretamente
                            "stars": repo_info.get("stars", 0) if repo_info.get("status") == "success" else 0,
                            "descricao": repo_info.get("description", "") if repo_info.get("status") == "success" else "",
                        })

        except requests.exceptions.RequestException as e:
            print(f"Erro na busca geral: {e}")

        # Busca específica nos repositórios populares
        for repo_full in repos_populares[:5]:  # Limita para não demorar muito
            try:
                if "/" in repo_full:
                    owner, repo = repo_full.split("/", 1)

                    # Busca arquivos por extensão
                    for ext in extensoes[:3]:  # Limita extensões para performance
                        search_term = f"extension:{ext[1:]}"  # Remove o ponto
                        if query:
                            search_term += f" {query}"

                        code_search = self.client.search_code(owner, repo, search_term, max_results=3)

                        if code_search.get("status") == "success":
                            for result in code_search.get("results", []):
                                filename = result.get("name", "")
                                if not any(m["nome"] == filename and m["repositorio"] == repo_full for m in modelos):
                                    modelos.append({
                                        "nome": filename,
                                        "caminho": result.get("path", ""),
                                        "repositorio": repo_full,
                                        "url": result.get("url", ""),
                                        "download_url": f"https://raw.githubusercontent.com/{repo_full}/main/{result.get('path', '')}",
                                        "formato": self._identificar_formato(filename),
                                        "tamanho_kb": "Desconhecido",
                                        "stars": 0,  # Já sabemos que são repos populares
                                        "descricao": f"Modelo de {repo_full}",
                                    })

            except Exception as e:
                print(f"Erro ao buscar em {repo_full}: {e}")
                continue

        # Remove duplicatas e limita resultados
        modelos_unicos = []
        seen = set()
        for modelo in modelos:
            key = (modelo["nome"], modelo["repositorio"])
            if key not in seen:
                modelos_unicos.append(modelo)
                seen.add(key)

        return {
            "status": "success",
            "query": query,
            "formato": formato,
            "modelos": modelos_unicos[:max_results],
            "total_encontrados": len(modelos_unicos),
            "formatos_suportados": list(extensoes_suportadas.keys())
        }

    def _identificar_formato(self, filename: str) -> str:
        """
        Identifica o formato do modelo baseado na extensão do arquivo

        Args:
            filename: Nome do arquivo

        Returns:
            str: Formato identificado
        """
        extensao = filename.lower().split(".")[-1]

        formatos = {
            "onnx": "ONNX",
            "tflite": "TensorFlow Lite",
            "h5": "Keras",
            "keras": "Keras",
            "pt": "PyTorch",
            "pth": "PyTorch",
            "pkl": "PyTorch",
            "mlmodel": "Core ML",
            "cfg": "Darknet",
            "weights": "Darknet",
            "pb": "TensorFlow",
            "meta": "TensorFlow",
            "caffemodel": "Caffe",
            "prototxt": "Caffe"
        }

        return formatos.get(extensao, "Desconhecido")
github_client = GitHubDocsClient()
github_integration = GitMCPIntegration()

# Manter compatibilidade com código existente
gitmcp_client = github_client
gitmcp_integration = github_integration


def testar_integracao():
    """Testa a integração com GitHub API"""
    print("🧪 Testando Integração GitHub API")
    print("=" * 40)

    # Testa disponibilidade
    print(f"GitHub API disponível: {github_client.is_available()}")

    if github_client.is_available():
        # Testa busca de repositório
        print("\n📚 Testando busca de repositório...")
        repo = github_client.get_repository_info("TheAlgorithms", "Python")
        print(f"Status: {repo['status']}")
        if repo["status"] == "success":
            print(f"📖 Repositório: {repo.get('full_name')}")
            print(f"⭐ Stars: {repo.get('stars')}")
            print(f"📝 Descrição: {repo.get('description', 'N/A')[:100]}...")

        # Testa busca de README
        print("\n📄 Testando busca de README...")
        readme = github_client.get_readme("TheAlgorithms", "Python")
        print(f"Status: {readme['status']}")
        if readme["status"] == "success":
            content = readme.get("content", "")
            print(f"📏 Tamanho: {len(content)} caracteres")
            print(f"📄 Conteúdo (primeiras 200 chars): {content[:200]}...")

        # Testa busca de código
        print("\n💻 Testando busca de código...")
        code = github_client.search_code("TheAlgorithms", "Python", "bubble sort", max_results=3)
        print(f"Status: {code['status']}")
        print(f"Resultados encontrados: {code.get('total_results', 0)}")

        # Testa integração específica
        print("\n🔗 Testando integração de algoritmos...")
        integration = GitMCPIntegration()
        exemplos = integration.obter_exemplos_codigo("quick sort")
        print(f"Exemplos encontrados: {exemplos.get('total_exemplos', 0)}")

    else:
        print("GitHub API não está disponível no momento")
        print("Verifique sua conexão com a internet")


if __name__ == "__main__":
    testar_integracao()
