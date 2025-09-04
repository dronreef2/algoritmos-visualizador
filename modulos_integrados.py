# ==========================================
# 📚 MÓDULOS EDUCACIONAIS INTEGRADOS
# ==========================================
# Integração completa dos 4 módulos educacionais no sistema

import streamlit as st
import os
import sys
import importlib.util
from typing import Dict, List, Any, Optional
import asyncio

class ModulosEducacionaisIntegrados:
    """Classe para integração completa dos módulos educacionais"""

    def __init__(self):
        self.modulos = {
            0: {
                "nome": "Módulo 1: Fundamentos",
                "pasta": "modulo_1_fundamentos",
                "arquivos": [
                    "busca_binaria.py",
                    "dois_ponteiros.py",
                    "janela_deslizante.py",
                    "backtracking.py",
                    "bfs.py",
                    "operacoes_bits.py",
                    "otimizacao_arrays.py",
                    "aplicacoes_reais.py",
                    "casos_uso_praticos.py",
                    "guia_entrevistas.py"
                ]
            },
            1: {
                "nome": "Módulo 2: Estruturas de Dados",
                "pasta": "modulo_2_estruturas_dados",
                "arquivos": [
                    "algoritmos_ordenacao.py",
                    "algoritmos_grafos.py",
                    "estruturas_avancadas.py",
                    "structures_visualizer.py"
                ]
            },
            2: {
                "nome": "Módulo 3: Programação Dinâmica",
                "pasta": "modulo_3_programacao_dinamica",
                "arquivos": [
                    "metodologia_3_passos.py"
                ]
            },
            3: {
                "nome": "Módulo 4: Entrevistas",
                "pasta": "modulo_4_entrevistas",
                "arquivos": [
                    "interview_visualizer.py",
                    "problem_playground.py"
                ]
            }
        }

    def carregar_conteudo_modulo(self, modulo_id: int) -> Dict[str, Any]:
        """Carrega todo o conteúdo de um módulo específico"""
        if modulo_id not in self.modulos:
            return {"erro": "Módulo não encontrado"}

        modulo = self.modulos[modulo_id]
        base_path = f"/workspaces/algoritmos-visualizador/{modulo['pasta']}"

        conteudo = {
            "nome": modulo["nome"],
            "pasta": modulo["pasta"],
            "readme": None,
            "arquivos": {},
            "estatisticas": {}
        }

        # Carregar README
        readme_path = os.path.join(base_path, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    conteudo["readme"] = f.read()
            except Exception as e:
                conteudo["readme"] = f"Erro ao carregar README: {e}"

        # Carregar arquivos Python
        for arquivo in modulo["arquivos"]:
            arquivo_path = os.path.join(base_path, arquivo)
            if os.path.exists(arquivo_path):
                try:
                    with open(arquivo_path, 'r', encoding='utf-8') as f:
                        conteudo["arquivos"][arquivo] = {
                            "conteudo": f.read(),
                            "linhas": sum(1 for _ in f),
                            "tamanho": os.path.getsize(arquivo_path)
                        }
                except Exception as e:
                    conteudo["arquivos"][arquivo] = {
                        "erro": str(e)
                    }

        # Estatísticas do módulo
        conteudo["estatisticas"] = {
            "total_arquivos": len(conteudo["arquivos"]),
            "total_linhas": sum(info.get("linhas", 0) for info in conteudo["arquivos"].values() if isinstance(info, dict)),
            "algoritmos_principais": self._extrair_algoritmos_principais(modulo_id)
        }

        return conteudo

    def _extrair_algoritmos_principais(self, modulo_id: int) -> List[str]:
        """Extrai a lista de algoritmos principais de cada módulo"""
        algoritmos_por_modulo = {
            0: [  # Módulo 1
                "Busca Binária", "Dois Ponteiros", "Janela Deslizante",
                "Backtracking", "BFS", "Operações de Bits", "Otimização de Arrays"
            ],
            1: [  # Módulo 2
                "Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort",
                "Counting Sort", "BFS", "DFS", "Dijkstra", "Kruskal"
            ],
            2: [  # Módulo 3
                "Metodologia 3 Passos", "Programação Dinâmica"
            ],
            3: [  # Módulo 4
                "Visualizador de Entrevistas", "Problem Playground"
            ]
        }

        return algoritmos_por_modulo.get(modulo_id, [])

    def executar_codigo_modulo(self, modulo_id: int, arquivo: str, funcao: str = None, parametros: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa código de um módulo específico"""
        try:
            modulo = self.modulos[modulo_id]
            base_path = f"/workspaces/algoritmos-visualizador/{modulo['pasta']}"
            arquivo_path = os.path.join(base_path, arquivo)

            if not os.path.exists(arquivo_path):
                return {"erro": f"Arquivo não encontrado: {arquivo_path}"}

            # Adicionar o diretório ao path
            if base_path not in sys.path:
                sys.path.append(base_path)

            # Importar o módulo
            spec = importlib.util.spec_from_file_location(arquivo.replace('.py', ''), arquivo_path)
            modulo_importado = importlib.util.module_from_spec(spec)

            try:
                spec.loader.exec_module(modulo_importado)

                # Se uma função específica foi solicitada
                if funcao and hasattr(modulo_importado, funcao):
                    func = getattr(modulo_importado, funcao)
                    if callable(func):
                        # Executar com parâmetros se fornecidos
                        if parametros:
                            resultado = func(**parametros)
                        else:
                            resultado = func()
                        return {"sucesso": True, "resultado": resultado, "tipo": "funcao"}
                    else:
                        return {"erro": f"{funcao} não é uma função"}

                # Se não há função específica, tentar executar o módulo principal
                return {"sucesso": True, "resultado": "Módulo carregado com sucesso", "tipo": "modulo"}

            except Exception as e:
                return {"erro": f"Erro na execução: {str(e)}"}

        except Exception as e:
            return {"erro": f"Erro geral: {str(e)}"}

    def gerar_exercicios_modulo(self, modulo_id: int, dificuldade: str = "beginner") -> List[Dict[str, Any]]:
        """Gera exercícios específicos para um módulo"""
        exercicios_base = {
            0: {  # Módulo 1
                "beginner": [
                    {
                        "titulo": "Busca Binária Básica",
                        "tipo": "implementacao",
                        "descricao": "Implemente a busca binária para encontrar um elemento em um array ordenado",
                        "exemplo": "[1, 3, 5, 7, 9], target = 5",
                        "dificuldade": "beginner"
                    },
                    {
                        "titulo": "Dois Ponteiros - Soma",
                        "tipo": "implementacao",
                        "descricao": "Use dois ponteiros para encontrar dois números que somam um valor alvo",
                        "exemplo": "[1, 2, 3, 4, 5], target = 7",
                        "dificuldade": "beginner"
                    }
                ],
                "intermediate": [
                    {
                        "titulo": "Backtracking - N-Queens",
                        "tipo": "implementacao",
                        "descricao": "Implemente o algoritmo N-Queens usando backtracking",
                        "exemplo": "4x4 board",
                        "dificuldade": "intermediate"
                    }
                ]
            },
            1: {  # Módulo 2
                "beginner": [
                    {
                        "titulo": "Bubble Sort",
                        "tipo": "ordenacao",
                        "descricao": "Implemente o algoritmo Bubble Sort",
                        "exemplo": "[3, 1, 4, 1, 5, 9, 2, 6]",
                        "dificuldade": "beginner"
                    }
                ],
                "intermediate": [
                    {
                        "titulo": "Quick Sort com Pivot",
                        "tipo": "ordenacao",
                        "descricao": "Implemente Quick Sort com escolha inteligente de pivot",
                        "exemplo": "[8, 3, 1, 7, 4, 2, 9, 5, 6]",
                        "dificuldade": "intermediate"
                    }
                ]
            }
        }

        return exercicios_base.get(modulo_id, {}).get(dificuldade, [])

    def analisar_complexidade_modulo(self, modulo_id: int) -> Dict[str, Any]:
        """Analisa a complexidade dos algoritmos de um módulo"""
        analises = {
            0: {  # Módulo 1
                "Busca Binária": {"tempo": "O(log n)", "espaco": "O(1)", "caso_otimo": "Encontrar primeiro elemento"},
                "Dois Ponteiros": {"tempo": "O(n)", "espaco": "O(1)", "caso_otimo": "Arrays ordenados"},
                "Backtracking": {"tempo": "O(b^d)", "espaco": "O(d)", "caso_otimo": "Poucas escolhas por nível"},
                "BFS": {"tempo": "O(V + E)", "espaco": "O(V)", "caso_otimo": "Grafo não muito denso"}
            },
            1: {  # Módulo 2
                "Bubble Sort": {"tempo": "O(n²)", "espaco": "O(1)", "caso_otimo": "Array quase ordenado"},
                "Quick Sort": {"tempo": "O(n log n) médio", "espaco": "O(log n)", "caso_otimo": "Pivot balanceado"},
                "Merge Sort": {"tempo": "O(n log n)", "espaco": "O(n)", "caso_otimo": "Sempre consistente"},
                "Dijkstra": {"tempo": "O((V+E) log V)", "espaco": "O(V)", "caso_otimo": "Grafo esparso"}
            }
        }

        return analises.get(modulo_id, {})

# Instância global dos módulos integrados
modulos_integrados = ModulosEducacionaisIntegrados()
