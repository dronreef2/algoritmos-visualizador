"""
🎯 SISTEMA DE EXERCÍCIOS PRÁTICOS INTERATIVOS
=============================================

Sistema completo de exercícios práticos para reforçar o aprendizado
de algoritmos e estruturas de dados com validação em tempo real.
"""

import streamlit as st
import random
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class TipoExercicio(Enum):
    MULTIPLA_ESCOLHA = "multipla_escolha"
    VERDADEIRO_FALSO = "verdadeiro_falso"
    CODIGO_PREENCHER = "codigo_preencher"
    ORDENAR_PASSOS = "ordenar_passos"
    COMPLEXIDADE_ANALISE = "complexidade_analise"
    DEBUGGING = "debugging"


class Dificuldade(Enum):
    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"


@dataclass
class Exercicio:
    """Representa um exercício prático"""

    id: str
    titulo: str
    descricao: str
    tipo: TipoExercicio
    dificuldade: Dificuldade
    conceito_relacionado: str
    enunciado: str
    dados_exercicio: Dict[str, Any]
    resposta_correta: Any
    explicacao: str
    dicas: List[str]
    tempo_estimado: int  # em minutos


@dataclass
class SessaoExercicio:
    """Representa uma sessão de exercícios"""

    exercicio_id: str
    respostas_usuario: List[Any]
    tempo_inicio: float
    tempo_fim: Optional[float]
    tentativas: int
    pontos: int
    concluido: bool


class SistemaExerciciosPraticos:
    """Sistema principal de exercícios práticos"""

    def __init__(self):
        self.exercicios = self._carregar_exercicios()
        self.sessoes_ativas = {}
        self.historico = self._carregar_historico()

    def _carregar_exercicios(self) -> Dict[str, Exercicio]:
        """Carrega todos os exercícios disponíveis"""
        return {
            "busca_binaria_basico": Exercicio(
                id="busca_binaria_basico",
                titulo="Busca Binária - Conceito Básico",
                descricao="Entenda o funcionamento básico da busca binária",
                tipo=TipoExercicio.MULTIPLA_ESCOLHA,
                dificuldade=Dificuldade.INICIANTE,
                conceito_relacionado="busca_binaria",
                enunciado="Qual é a complexidade de tempo da busca binária em um array ordenado?",
                dados_exercicio={
                    "opcoes": [
                        "O(1) - Tempo constante",
                        "O(log n) - Tempo logarítmico",
                        "O(n) - Tempo linear",
                        "O(n²) - Tempo quadrático",
                    ]
                },
                resposta_correta=1,  # índice da resposta correta
                explicacao="A busca binária divide o array ao meio a cada iteração, resultando em complexidade O(log n).",
                dicas=[
                    "Pense em quantas vezes você pode dividir um array ao meio",
                    "Compare com a busca linear que verifica cada elemento",
                ],
                tempo_estimado=5,
            ),
            "busca_binaria_aplicacao": Exercicio(
                id="busca_binaria_aplicacao",
                titulo="Busca Binária - Aplicação Prática",
                descricao="Aplique busca binária em um cenário real",
                tipo=TipoExercicio.MULTIPLA_ESCOLHA,
                dificuldade=Dificuldade.INICIANTE,
                conceito_relacionado="busca_binaria",
                enunciado="Em qual situação a busca binária NÃO pode ser aplicada?",
                dados_exercicio={
                    "opcoes": [
                        "Array ordenado de números",
                        "Lista ordenada de strings",
                        "Array não ordenado",
                        "Índice de banco de dados ordenado",
                    ]
                },
                resposta_correta=2,
                explicacao="A busca binária requer que os dados estejam ordenados para funcionar corretamente.",
                dicas=["A busca binária depende da ordenação dos dados", "Considere as pré-condições do algoritmo"],
                tempo_estimado=3,
            ),
            "ordenacao_bubble_sort": Exercicio(
                id="ordenacao_bubble_sort",
                titulo="Bubble Sort - Análise de Passos",
                descricao="Analise o comportamento do Bubble Sort",
                tipo=TipoExercicio.ORDENAR_PASSOS,
                dificuldade=Dificuldade.INICIANTE,
                conceito_relacionado="bubble_sort",
                enunciado="Ordene os passos do algoritmo Bubble Sort em sua sequência correta:",
                dados_exercicio={
                    "passos": [
                        "Comparar elementos adjacentes",
                        "Trocar se estiverem na ordem errada",
                        "Mover para o próximo par",
                        "Repetir até o array estar ordenado",
                    ],
                    "ordem_correta": [0, 1, 2, 3],
                },
                resposta_correta=[0, 1, 2, 3],
                explicacao="O Bubble Sort compara e troca elementos adjacentes iterativamente até ordenar completamente.",
                dicas=["Pense no movimento das bolhas na água", "Cada passagem move o maior elemento para o final"],
                tempo_estimado=7,
            ),
            "arvore_binaria_balanceamento": Exercicio(
                id="arvore_binaria_balanceamento",
                titulo="Árvore Binária - Balanceamento",
                descricao="Entenda a importância do balanceamento em árvores",
                tipo=TipoExercicio.VERDADEIRO_FALSO,
                dificuldade=Dificuldade.INTERMEDIARIO,
                conceito_relacionado="arvore_binaria",
                enunciado="Avalie as seguintes afirmações sobre árvores binárias balanceadas:",
                dados_exercicio={
                    "afirmacoes": [
                        "Uma árvore balanceada garante complexidade O(log n) para operações",
                        "Árvores AVL são sempre balanceadas",
                        "O balanceamento evita o pior caso de complexidade O(n)",
                        "Árvores rubro-negras garantem balanceamento perfeito",
                    ]
                },
                resposta_correta=[True, True, True, False],
                explicacao="Árvores balanceadas garantem performance O(log n), mas nem sempre balanceamento perfeito como em Árvores Rubro-Negras que garantem altura máxima de 2*log n.",
                dicas=["Considere a diferença de altura entre subárvores", "Pense na relação entre altura e número de nós"],
                tempo_estimado=8,
            ),
            "grafo_dijkstra_aplicacao": Exercicio(
                id="grafo_dijkstra_aplicacao",
                titulo="Dijkstra - Aplicação em GPS",
                descricao="Aplique o algoritmo de Dijkstra em navegação",
                tipo=TipoExercicio.MULTIPLA_ESCOLHA,
                dificuldade=Dificuldade.INTERMEDIARIO,
                conceito_relacionado="algoritmo_dijkstra",
                enunciado="Por que o algoritmo de Dijkstra é usado em sistemas de GPS?",
                dados_exercicio={
                    "opcoes": [
                        "É o algoritmo mais rápido para qualquer grafo",
                        "Garante o caminho mais curto com pesos positivos",
                        "Funciona mesmo com pesos negativos",
                        "Não precisa de estrutura de dados auxiliar",
                    ]
                },
                resposta_correta=1,
                explicacao="Dijkstra garante o caminho mais curto em grafos com pesos positivos, ideal para distâncias em mapas.",
                dicas=["Considere as restrições do algoritmo", "Pense em pesos negativos (buracos negros?)"],
                tempo_estimado=6,
            ),
            "programacao_dinamica_fibonacci": Exercicio(
                id="programacao_dinamica_fibonacci",
                titulo="Programação Dinâmica - Fibonacci",
                descricao="Compare abordagens para Fibonacci",
                tipo=TipoExercicio.COMPLEXIDADE_ANALISE,
                dificuldade=Dificuldade.AVANCADO,
                conceito_relacionado="programacao_dinamica",
                enunciado="Analise a complexidade das abordagens para calcular Fibonacci:",
                dados_exercicio={
                    "abordagens": [
                        "Recursão sem memoização",
                        "Recursão com memoização",
                        "Iterativo com array",
                        "Fórmula matemática direta",
                    ],
                    "complexidades": ["O(2^n)", "O(n)", "O(n)", "O(1)"],
                },
                resposta_correta={
                    "recursao_sem_memo": "O(2^n)",
                    "recursao_com_memo": "O(n)",
                    "iterativo": "O(n)",
                    "formula": "O(1)",
                },
                explicacao="A recursão sem memoização recalcula valores, criando árvore exponencial. Memoização evita recálculos, fórmula direta é mais eficiente.",
                dicas=["Conte quantas vezes cada valor é calculado", "Considere o espaço usado para memoização"],
                tempo_estimado=10,
            ),
            "debug_codigo_busca": Exercicio(
                id="debug_codigo_busca",
                titulo="Debugging - Busca Binária com Bug",
                descricao="Encontre e corrija o bug no código",
                tipo=TipoExercicio.DEBUGGING,
                dificuldade=Dificuldade.INTERMEDIARIO,
                conceito_relacionado="busca_binaria",
                enunciado="Encontre o bug nesta implementação de busca binária:",
                dados_exercicio={
                    "codigo": """
def busca_binaria(arr, alvo):
    esquerda, direita = 0, len(arr) - 1
    
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        
        if arr[meio] == alvo:
            return meio
        elif arr[meio] < alvo:
            esquerda = meio  # BUG: deveria ser meio + 1
        else:
            direita = meio  # BUG: deveria ser meio - 1
    
    return -1
                    """,
                    "opcoes_bug": [
                        "Divisão inteira do meio pode causar overflow",
                        "Limites não são atualizados corretamente",
                        "Comparação de igualdade está errada",
                        "Array não está sendo percorrido completamente",
                    ],
                },
                resposta_correta=1,
                explicacao="Os limites esquerda e direita não são atualizados corretamente, causando loop infinito ou busca incorreta.",
                dicas=["Verifique como os limites são atualizados", "Teste com um exemplo simples"],
                tempo_estimado=8,
            ),
        }

    def _carregar_historico(self) -> Dict[str, List[SessaoExercicio]]:
        """Carrega histórico de exercícios do usuário"""
        # Em produção, isso viria de um banco de dados
        return {}

    def obter_exercicios_por_conceito(self, conceito: str) -> List[Exercicio]:
        """Retorna exercícios relacionados a um conceito"""
        return [ex for ex in self.exercicios.values() if ex.conceito_relacionado == conceito]

    def obter_exercicios_por_dificuldade(self, dificuldade: Dificuldade) -> List[Exercicio]:
        """Retorna exercícios filtrados por dificuldade"""
        return [ex for ex in self.exercicios.values() if ex.dificuldade == dificuldade]

    def iniciar_sessao_exercicio(self, exercicio_id: str) -> Optional[SessaoExercicio]:
        """Inicia uma nova sessão de exercício"""
        if exercicio_id not in self.exercicios:
            return None

        sessao_id = f"{exercicio_id}_{int(time.time())}"
        sessao = SessaoExercicio(
            exercicio_id=exercicio_id,
            respostas_usuario=[],
            tempo_inicio=time.time(),
            tempo_fim=None,
            tentativas=0,
            pontos=0,
            concluido=False,
        )

        self.sessoes_ativas[sessao_id] = sessao
        return sessao

    def validar_resposta(self, sessao_id: str, resposta_usuario: Any) -> Dict[str, Any]:
        """Valida a resposta do usuário"""
        if sessao_id not in self.sessoes_ativas:
            return {"erro": "Sessão não encontrada"}

        sessao = self.sessoes_ativas[sessao_id]
        exercicio = self.exercicios[sessao.exercicio_id]

        sessao.tentativas += 1
        sessao.respostas_usuario.append(resposta_usuario)

        # Lógica de validação baseada no tipo de exercício
        if exercicio.tipo == TipoExercicio.MULTIPLA_ESCOLHA:
            correta = resposta_usuario == exercicio.resposta_correta
        elif exercicio.tipo == TipoExercicio.VERDADEIRO_FALSO:
            correta = resposta_usuario == exercicio.resposta_correta
        elif exercicio.tipo == TipoExercicio.ORDENAR_PASSOS:
            correta = resposta_usuario == exercicio.resposta_correta
        elif exercicio.tipo == TipoExercicio.COMPLEXIDADE_ANALISE:
            correta = resposta_usuario == exercicio.resposta_correta
        elif exercicio.tipo == TipoExercicio.DEBUGGING:
            correta = resposta_usuario == exercicio.resposta_correta
        else:
            correta = False

        if correta:
            sessao.concluido = True
            sessao.tempo_fim = time.time()
            sessao.pontos = max(100 - (sessao.tentativas - 1) * 20, 20)  # Pontuação baseada em tentativas

        return {
            "correta": correta,
            "explicacao": exercicio.explicacao,
            "tentativas": sessao.tentativas,
            "pontos": sessao.pontos if correta else 0,
            "concluido": sessao.concluido,
        }

    def obter_dica(self, exercicio_id: str, tentativa_atual: int) -> Optional[str]:
        """Retorna uma dica baseada na tentativa atual"""
        if exercicio_id not in self.exercicios:
            return None

        exercicio = self.exercicios[exercicio_id]
        dicas_disponiveis = len(exercicio.dicas)

        if tentativa_atual <= dicas_disponiveis:
            return exercicio.dicas[tentativa_atual - 1]

        return None

    def calcular_estatisticas_usuario(self) -> Dict[str, Any]:
        """Calcula estatísticas de desempenho do usuário"""
        total_exercicios = len(self.exercicios)
        exercicios_concluidos = len([s for s in self.sessoes_ativas.values() if s.concluido])

        pontos_totais = sum(s.pontos for s in self.sessoes_ativas.values() if s.concluido)
        tempo_total = sum((s.tempo_fim - s.tempo_inicio) for s in self.sessoes_ativas.values() if s.tempo_fim)

        return {
            "exercicios_concluidos": exercicios_concluidos,
            "total_exercicios": total_exercicios,
            "taxa_conclusao": (exercicios_concluidos / total_exercicios * 100) if total_exercicios > 0 else 0,
            "pontos_totais": pontos_totais,
            "tempo_total_minutos": tempo_total / 60 if tempo_total > 0 else 0,
        }


# Instância global do sistema
sistema_exercicios = SistemaExerciciosPraticos()
