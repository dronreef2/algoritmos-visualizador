"""
🧭 SISTEMA DE APRENDIZADO CONTEXTUALIZADO
=========================================

Este módulo implementa uma experiência de aprendizado contextualizada
para algoritmos e estruturas de dados, com jornadas temáticas,
contexto histórico e aplicações práticas.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class Dificuldade(Enum):
    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"


class Tema(Enum):
    PESQUISA = "pesquisa"
    ORDENACAO = "ordenacao"
    GRAFOS = "grafos"
    DINAMICA = "programacao_dinamica"
    ESTRUTURAS = "estruturas_dados"


@dataclass
class Conceito:
    """Representa um conceito de algoritmo/estrutura"""

    nome: str
    descricao: str
    dificuldade: Dificuldade
    tema: Tema
    pre_requisitos: List[str]
    aplicacoes_reais: List[str]
    contexto_historico: str
    exemplos_praticos: List[str]


@dataclass
class JornadaAprendizado:
    """Representa uma jornada completa de aprendizado"""

    titulo: str
    descricao: str
    tema_principal: Tema
    dificuldade: Dificuldade
    duracao_estimada: str  # em horas
    conceitos: List[str]
    projetos_praticos: List[str]
    objetivos_aprendizagem: List[str]


class SistemaAprendizadoContextualizado:
    """Sistema principal para aprendizado contextualizado"""

    def __init__(self):
        self.conceitos = self._carregar_conceitos()
        self.jornadas = self._carregar_jornadas()
        self.progresso_usuario = self._carregar_progresso()

    def _carregar_conceitos(self) -> Dict[str, Conceito]:
        """Carrega todos os conceitos disponíveis"""
        return {
            "busca_binaria": Conceito(
                nome="Busca Binária",
                descricao="Algoritmo eficiente para encontrar elementos em arrays ordenados",
                dificuldade=Dificuldade.INICIANTE,
                tema=Tema.PESQUISA,
                pre_requisitos=[],
                aplicacoes_reais=[
                    "Sistema de busca em bancos de dados",
                    "Busca em sistemas de arquivos",
                    "Localização de registros em logs ordenados",
                    "Busca em dicionários digitais",
                ],
                contexto_historico="Desenvolvido na década de 1940, é um dos algoritmos fundamentais da computação",
                exemplos_praticos=[
                    "Encontrar um contato na agenda telefônica",
                    "Localizar uma palavra em dicionário",
                    "Buscar commits no Git por data",
                ],
            ),
            "arvore_binaria": Conceito(
                nome="Árvore Binária de Busca",
                descricao="Estrutura de dados que mantém elementos ordenados para busca eficiente",
                dificuldade=Dificuldade.INTERMEDIARIO,
                tema=Tema.ESTRUTURAS,
                pre_requisitos=["busca_binaria"],
                aplicacoes_reais=[
                    "Índices de banco de dados",
                    "Sistema de arquivos (B-trees)",
                    "Estrutura de dados para compiladores",
                    "Implementação de mapas e conjuntos ordenados",
                ],
                contexto_historico="Conceito fundamental desde os anos 1960, base para muitas estruturas modernas",
                exemplos_praticos=[
                    "Mapa de preços em loja online",
                    "Índice de livros em biblioteca",
                    "Estrutura de dados para jogos (árvores de decisão)",
                ],
            ),
            "algoritmo_dijkstra": Conceito(
                nome="Algoritmo de Dijkstra",
                descricao="Algoritmo para encontrar o caminho mais curto em grafos",
                dificuldade=Dificuldade.INTERMEDIARIO,
                tema=Tema.GRAFOS,
                pre_requisitos=["grafos", "fila_prioridade"],
                aplicacoes_reais=[
                    "Sistemas de GPS e navegação",
                    "Roteamento de rede de computadores",
                    "Planejamento de rotas em jogos",
                    "Otimização de caminhos em logística",
                ],
                contexto_historico="Criado por Edsger Dijkstra em 1956, revolucionou a teoria dos grafos",
                exemplos_praticos=[
                    "Encontrar rota mais rápida no Google Maps",
                    "Roteamento de pacotes na internet",
                    "Planejamento de caminhos em jogos de estratégia",
                ],
            ),
            "programacao_dinamica": Conceito(
                nome="Programação Dinâmica",
                descricao="Técnica para resolver problemas complexos dividindo-os em subproblemas",
                dificuldade=Dificuldade.AVANCADO,
                tema=Tema.DINAMICA,
                pre_requisitos=["recursao", "memoization"],
                aplicacoes_reais=[
                    "Otimização de sequências de DNA",
                    "Compressão de dados (LZ77)",
                    "Sistemas de recomendação",
                    "Otimização de carteiras de investimento",
                ],
                contexto_historico="Desenvolvido por Richard Bellman na década de 1950 para pesquisa operacional",
                exemplos_praticos=[
                    "Correção ortográfica em editores de texto",
                    "Compressão de arquivos ZIP",
                    "Sistema de cache inteligente em navegadores",
                ],
            ),
        }

    def _carregar_jornadas(self) -> Dict[str, JornadaAprendizado]:
        """Carrega jornadas de aprendizado disponíveis"""
        return {
            "fundamentos_pesquisa": JornadaAprendizado(
                titulo="Fundamentos da Pesquisa",
                descricao="Domine os algoritmos de busca essenciais para desenvolvimento",
                tema_principal=Tema.PESQUISA,
                dificuldade=Dificuldade.INICIANTE,
                duracao_estimada="4-6 horas",
                conceitos=["busca_linear", "busca_binaria", "interpolacao"],
                projetos_praticos=[
                    "Implementar busca em agenda telefônica",
                    "Sistema de busca em biblioteca digital",
                    "Busca eficiente em logs de sistema",
                ],
                objetivos_aprendizagem=[
                    "Entender diferença entre busca linear e binária",
                    "Implementar algoritmos de busca eficientes",
                    "Analisar complexidade de algoritmos de busca",
                    "Aplicar busca em problemas reais",
                ],
            ),
            "estruturas_arvore": JornadaAprendizado(
                titulo="Estruturas em Árvore",
                descricao="Explore estruturas hierárquicas essenciais na computação",
                tema_principal=Tema.ESTRUTURAS,
                dificuldade=Dificuldade.INTERMEDIARIO,
                duracao_estimada="8-10 horas",
                conceitos=["arvore_binaria", "arvore_balanceada", "heap", "trie"],
                projetos_praticos=[
                    "Implementar corretor ortográfico com Trie",
                    "Sistema de arquivos com árvore B",
                    "Indexação de banco de dados",
                ],
                objetivos_aprendizagem=[
                    "Compreender estruturas de árvore",
                    "Implementar operações básicas em árvores",
                    "Balancear árvores para eficiência",
                    "Aplicar árvores em problemas reais",
                ],
            ),
            "algoritmos_grafos": JornadaAprendizado(
                titulo="Algoritmos em Grafos",
                descricao="Domine algoritmos para resolução de problemas em redes",
                tema_principal=Tema.GRAFOS,
                dificuldade=Dificuldade.AVANCADO,
                duracao_estimada="12-15 horas",
                conceitos=["dfs_bfs", "algoritmo_dijkstra", "bellman_ford", "floyd_warshall"],
                projetos_praticos=[
                    "Sistema de navegação GPS",
                    "Análise de redes sociais",
                    "Roteamento de rede de computadores",
                ],
                objetivos_aprendizagem=[
                    "Representar problemas como grafos",
                    "Implementar algoritmos de travessia",
                    "Resolver problemas de caminho mínimo",
                    "Aplicar grafos em sistemas reais",
                ],
            ),
        }

    def _carregar_progresso(self) -> Dict[str, Any]:
        """Carrega progresso do usuário"""
        # Em produção, isso viria de um banco de dados
        return {"conceitos_completados": [], "jornadas_iniciadas": [], "tempo_estudado": 0, "exercicios_resolvidos": 0}

    def obter_conceitos_por_dificuldade(self, dificuldade: Dificuldade) -> List[Conceito]:
        """Retorna conceitos filtrados por dificuldade"""
        return [c for c in self.conceitos.values() if c.dificuldade == dificuldade]

    def obter_jornadas_por_tema(self, tema: Tema) -> List[JornadaAprendizado]:
        """Retorna jornadas filtradas por tema"""
        return [j for j in self.jornadas.values() if j.tema_principal == tema]

    def calcular_progresso_jornada(self, jornada_id: str) -> float:
        """Calcula progresso em uma jornada específica"""
        if jornada_id not in self.jornadas:
            return 0.0

        jornada = self.jornadas[jornada_id]
        conceitos_completados = len(set(jornada.conceitos) & set(self.progresso_usuario["conceitos_completados"]))
        return (conceitos_completados / len(jornada.conceitos)) * 100 if jornada.conceitos else 0

    def recomendar_proximo_conceito(self, conceito_atual: str) -> Optional[str]:
        """Recomenda próximo conceito baseado no atual"""
        if conceito_atual not in self.conceitos:
            return None

        conceito = self.conceitos[conceito_atual]

        # Procurar conceitos relacionados no mesmo tema
        relacionados = [nome for nome, c in self.conceitos.items() if c.tema == conceito.tema and nome != conceito_atual]

        # Retornar primeiro conceito relacionado não completado
        for relacionado in relacionados:
            if relacionado not in self.progresso_usuario["conceitos_completados"]:
                return relacionado

        return None


# Instância global do sistema
sistema_aprendizado = SistemaAprendizadoContextualizado()
