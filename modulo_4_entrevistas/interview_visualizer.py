"""
🎨 VISUALIZADOR DE PROBLEMAS DE ENTREVISTA
==========================================

Este módulo fornece visualizações interativas para problemas de entrevista técnica,
incluindo animações passo a passo e feedback visual.

Componentes:
- Renderer para diferentes tipos de problemas
- Animações de algoritmos
- Feedback visual de performance
- Comparação de soluções
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
from typing import List, Dict, Any, Optional
import seaborn as sns
from dataclasses import dataclass
import time

# ============================================================================
# 📊 ESTRUTURAS DE DADOS PARA VISUALIZAÇÃO
# ============================================================================


@dataclass
class VisualState:
    """Estado visual de um passo da animação."""

    step_number: int
    title: str
    description: str
    data: Dict[str, Any]
    highlight: List[int] = None
    annotations: List[str] = None


class InterviewVisualizer:
    """Visualizador principal para problemas de entrevista."""

    def __init__(self, figsize=(12, 8)):
        self.fig, self.axes = plt.subplots(2, 2, figsize=figsize)
        self.fig.suptitle("🎯 Problem Playground - Visualização", fontsize=16, fontweight="bold")

        # Configurar subplots
        self.ax_problem = self.axes[0, 0]  # Visualização do problema
        self.ax_progress = self.axes[0, 1]  # Progresso da solução
        self.ax_complexity = self.axes[1, 0]  # Análise de complexidade
        self.ax_score = self.axes[1, 1]  # Pontuação

        # Configurações visuais
        self.colors = {
            "primary": "#2E86AB",
            "secondary": "#A23B72",
            "success": "#F18F01",
            "warning": "#C73E1D",
            "background": "#F5F5F5",
            "text": "#333333",
        }

        # Estado atual
        self.current_problem = None
        self.animation_steps = []
        self.current_step = 0

    def visualize_problem(
        self,
        problem_id: str,
        steps: List[Dict[str, Any]],
        test_results: Dict[str, Any] = None,
        code_analysis: Dict[str, Any] = None,
    ):
        """
        Visualiza um problema de entrevista completo.

        Args:
            problem_id: ID do problema
            steps: Lista de passos da solução
            test_results: Resultados dos testes
            code_analysis: Análise do código
        """
        self.current_problem = problem_id
        self.animation_steps = steps

        # Limpar axes
        for ax in self.axes.flat:
            ax.clear()

        # Renderizar baseado no tipo de problema
        if problem_id == "two_sum":
            self._render_two_sum(steps, test_results, code_analysis)
        elif problem_id == "valid_parentheses":
            self._render_valid_parentheses(steps, test_results, code_analysis)
        else:
            self._render_generic_problem(steps, test_results, code_analysis)

        # Renderizar análises auxiliares
        if test_results:
            self._render_test_results(test_results)

        if code_analysis:
            self._render_code_analysis(code_analysis)

        plt.tight_layout()
        return self.fig

    def _render_two_sum(self, steps: List[Dict], test_results: Dict = None, code_analysis: Dict = None):
        """Renderiza visualização específica para Two Sum."""
        if not steps:
            return

        # Pegar dados do primeiro passo
        first_step = steps[0]
        nums = first_step["nums"]
        target = first_step["target"]

        # Configurar visualização principal
        self.ax_problem.set_title(f"🎯 Two Sum - Target: {target}", fontweight="bold")

        # Renderizar array
        bars = self.ax_problem.bar(range(len(nums)), nums, color=self.colors["primary"], alpha=0.7)

        # Adicionar valores no topo das barras
        for i, (bar, num) in enumerate(zip(bars, nums)):
            self.ax_problem.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{num}\n[{i}]",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        self.ax_problem.set_xlabel("Índices")
        self.ax_problem.set_ylabel("Valores")
        self.ax_problem.set_xticks(range(len(nums)))
        self.ax_problem.grid(True, alpha=0.3)

        # Mostrar hash map no canto
        if len(steps) > 1:
            last_step = steps[-1]
            if "hash_map" in last_step:
                hash_text = "Hash Map:\n"
                for num, idx in last_step["hash_map"].items():
                    hash_text += f"{num} → {idx}\n"

                self.ax_problem.text(
                    0.02,
                    0.98,
                    hash_text,
                    transform=self.ax_problem.transAxes,
                    verticalalignment="top",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
                )

        # Visualização de progresso
        self._render_algorithm_progress(steps)

    def _render_valid_parentheses(self, steps: List[Dict], test_results: Dict = None, code_analysis: Dict = None):
        """Renderiza visualização específica para Valid Parentheses."""
        if not steps:
            return

        # Pegar dados do primeiro passo
        first_step = steps[0]
        string = first_step["string"]

        # Configurar visualização principal
        self.ax_problem.set_title(f'🎯 Valid Parentheses - "{string}"', fontweight="bold")

        # Renderizar string como caracteres
        char_positions = range(len(string))
        char_heights = [1] * len(string)

        # Cores baseadas no tipo de parêntese
        char_colors = []
        for char in string:
            if char in "([{":
                char_colors.append(self.colors["primary"])
            elif char in ")]}":
                char_colors.append(self.colors["secondary"])
            else:
                char_colors.append(self.colors["warning"])

        bars = self.ax_problem.bar(char_positions, char_heights, color=char_colors, alpha=0.7)

        # Adicionar caracteres no topo
        for i, (bar, char) in enumerate(zip(bars, string)):
            self.ax_problem.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                char,
                ha="center",
                va="bottom",
                fontsize=14,
                fontweight="bold",
            )

        self.ax_problem.set_xlabel("Posições")
        self.ax_problem.set_ylabel("Caracteres")
        self.ax_problem.set_xticks(char_positions)
        self.ax_problem.set_ylim(0, 1.5)

        # Mostrar stack no canto
        if len(steps) > 1:
            last_step = steps[-1]
            if "stack" in last_step:
                stack_text = "Stack:\n"
                stack = last_step["stack"]
                if stack:
                    for item in reversed(stack):  # Mostrar do topo para baixo
                        stack_text += f"│ {item} │\n"
                    stack_text += "└───┘"
                else:
                    stack_text += "Empty"

                self.ax_problem.text(
                    0.02,
                    0.98,
                    stack_text,
                    transform=self.ax_problem.transAxes,
                    verticalalignment="top",
                    family="monospace",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8),
                )

        # Visualização de progresso
        self._render_algorithm_progress(steps)

    def _render_generic_problem(self, steps: List[Dict], test_results: Dict = None, code_analysis: Dict = None):
        """Renderiza visualização genérica para problemas não específicos."""
        self.ax_problem.set_title("🎯 Problema Genérico", fontweight="bold")

        # Mostrar informações básicas
        if steps:
            info_text = f"Passos: {len(steps)}\n"
            info_text += f"Tipo: {steps[0].get('tipo', 'Desconhecido')}\n"

            self.ax_problem.text(
                0.5,
                0.5,
                info_text,
                transform=self.ax_problem.transAxes,
                ha="center",
                va="center",
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8),
            )

        self.ax_problem.set_xlim(0, 1)
        self.ax_problem.set_ylim(0, 1)
        self.ax_problem.axis("off")

    def _render_algorithm_progress(self, steps: List[Dict]):
        """Renderiza progresso do algoritmo."""
        self.ax_progress.set_title("📈 Progresso do Algoritmo", fontweight="bold")

        if not steps:
            return

        # Criar timeline dos passos
        step_numbers = range(len(steps))
        step_types = [step.get("tipo", "unknown") for step in steps]

        # Mapear tipos para cores
        type_colors = {
            "inicio": self.colors["primary"],
            "verificacao": self.colors["secondary"],
            "adicionar": self.colors["success"],
            "encontrado": self.colors["warning"],
            "processando": self.colors["secondary"],
            "match": self.colors["success"],
            "push": self.colors["primary"],
            "erro": self.colors["warning"],
            "final": self.colors["success"],
        }

        colors = [type_colors.get(t, "gray") for t in step_types]

        # Plot timeline
        self.ax_progress.scatter(step_numbers, [1] * len(steps), c=colors, s=100, alpha=0.7)

        # Conectar pontos
        self.ax_progress.plot(step_numbers, [1] * len(steps), color="gray", alpha=0.3, linewidth=2)

        # Adicionar labels
        for i, step_type in enumerate(step_types):
            self.ax_progress.annotate(
                step_type,
                (i, 1),
                xytext=(0, 20),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=45,
            )

        self.ax_progress.set_xlabel("Passos")
        self.ax_progress.set_xlim(-0.5, len(steps) - 0.5)
        self.ax_progress.set_ylim(0.5, 1.5)
        self.ax_progress.set_yticks([])
        self.ax_progress.grid(True, alpha=0.3)

    def _render_test_results(self, test_results: Dict):
        """Renderiza resultados dos testes."""
        self.ax_complexity.set_title("🧪 Resultados dos Testes", fontweight="bold")

        # Dados dos testes
        passed = test_results.get("passed", 0)
        total = test_results.get("total", 1)

        # Gráfico de pizza
        labels = ["Passou", "Falhou"]
        sizes = [passed, total - passed]
        colors = [self.colors["success"], self.colors["warning"]]

        # Apenas mostrar fatia se há dados
        if total > 0:
            wedges, texts, autotexts = self.ax_complexity.pie(
                sizes, labels=labels, colors=colors, autopct=lambda pct: f"{int(pct/100 * total)}", startangle=90
            )

            # Adicionar informações
            self.ax_complexity.text(
                0,
                -1.3,
                f"Taxa de Sucesso: {passed}/{total} ({passed/total*100:.1f}%)",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

            # Tempo de execução
            exec_time = test_results.get("execution_time", 0)
            self.ax_complexity.text(0, -1.5, f"Tempo: {exec_time:.4f}s", ha="center", va="center", fontsize=9)

    def _render_code_analysis(self, code_analysis: Dict):
        """Renderiza análise do código."""
        self.ax_score.set_title("📊 Análise de Qualidade", fontweight="bold")

        # Métricas de qualidade
        metrics = {
            "Score": code_analysis.get("score", 0),
            "Complexidade": self._complexity_to_score(code_analysis.get("complexity", {}).get("time", "O(n)")),
            "Legibilidade": self._readability_to_score(code_analysis.get("readability", {})),
            "Padrões": min(100, len(code_analysis.get("patterns", [])) * 20),
        }

        # Gráfico de barras horizontais
        metrics_names = list(metrics.keys())
        metrics_values = list(metrics.values())

        bars = self.ax_score.barh(
            metrics_names,
            metrics_values,
            color=[self.colors["primary"], self.colors["secondary"], self.colors["success"], self.colors["warning"]],
        )

        # Adicionar valores nas barras
        for bar, value in zip(bars, metrics_values):
            self.ax_score.text(
                bar.get_width() + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.0f}",
                ha="left",
                va="center",
                fontweight="bold",
            )

        self.ax_score.set_xlabel("Pontuação (0-100)")
        self.ax_score.set_xlim(0, 110)
        self.ax_score.grid(True, alpha=0.3, axis="x")

        # Adicionar informações extras
        patterns = code_analysis.get("patterns", [])
        if patterns:
            patterns_text = f"Padrões: {', '.join(patterns)}"
            self.ax_score.text(
                0.02,
                0.02,
                patterns_text,
                transform=self.ax_score.transAxes,
                va="bottom",
                fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
            )

    def _complexity_to_score(self, complexity: str) -> int:
        """Converte complexidade para pontuação."""
        complexity_scores = {"O(1)": 100, "O(log n)": 90, "O(n)": 80, "O(n log n)": 70, "O(n²)": 50, "O(2^n)": 20}
        return complexity_scores.get(complexity, 60)

    def _readability_to_score(self, readability: Dict) -> int:
        """Converte métricas de legibilidade para pontuação."""
        if not readability:
            return 50

        score = 0
        score += min(30, readability.get("comment_ratio", 0) * 100)
        score += min(40, readability.get("descriptive_names_ratio", 0) * 100)
        score += min(30, max(0, 100 - readability.get("avg_line_length", 50)))

        return int(score)

    def create_animation(self, steps: List[Dict], interval: int = 1000):
        """
        Cria animação dos passos do algoritmo.

        Args:
            steps: Lista de passos
            interval: Intervalo entre frames em ms

        Returns:
            Objeto de animação matplotlib
        """
        self.animation_steps = steps
        self.current_step = 0

        def animate(frame):
            if frame < len(self.animation_steps):
                self.current_step = frame
                step = self.animation_steps[frame]

                # Atualizar visualização baseada no passo atual
                self._update_frame(step)

                return []

        anim = animation.FuncAnimation(self.fig, animate, frames=len(steps), interval=interval, blit=False, repeat=True)

        return anim

    def _update_frame(self, step: Dict):
        """Atualiza frame da animação."""
        # Implementar atualização específica baseada no tipo de problema
        if self.current_problem == "two_sum":
            self._update_two_sum_frame(step)
        elif self.current_problem == "valid_parentheses":
            self._update_valid_parentheses_frame(step)

    def _update_two_sum_frame(self, step: Dict):
        """Atualiza frame específico para Two Sum."""
        # Limpar e redesenhar
        self.ax_problem.clear()

        nums = step.get("nums", [])
        current_index = step.get("current_index", -1)

        # Redesenhar barras
        colors = ["red" if i == current_index else self.colors["primary"] for i in range(len(nums))]

        bars = self.ax_problem.bar(range(len(nums)), nums, color=colors, alpha=0.7)

        # Adicionar valores
        for i, (bar, num) in enumerate(zip(bars, nums)):
            self.ax_problem.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{num}\n[{i}]",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        # Adicionar ação atual
        action = step.get("action", "")
        self.ax_problem.set_title(f"🎯 Two Sum - {action}", fontweight="bold")

        self.ax_problem.set_xlabel("Índices")
        self.ax_problem.set_ylabel("Valores")
        self.ax_problem.set_xticks(range(len(nums)))
        self.ax_problem.grid(True, alpha=0.3)

    def _update_valid_parentheses_frame(self, step: Dict):
        """Atualiza frame específico para Valid Parentheses."""
        # Limpar e redesenhar
        self.ax_problem.clear()

        string = step.get("string", "")
        current_index = step.get("current_index", -1)

        # Redesenhar caracteres
        colors = []
        for i, char in enumerate(string):
            if i == current_index:
                colors.append("red")
            elif char in "([{":
                colors.append(self.colors["primary"])
            elif char in ")]}":
                colors.append(self.colors["secondary"])
            else:
                colors.append(self.colors["warning"])

        bars = self.ax_problem.bar(range(len(string)), [1] * len(string), color=colors, alpha=0.7)

        # Adicionar caracteres
        for i, (bar, char) in enumerate(zip(bars, string)):
            self.ax_problem.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                char,
                ha="center",
                va="bottom",
                fontsize=14,
                fontweight="bold",
            )

        # Adicionar ação atual
        action = step.get("action", "")
        self.ax_problem.set_title(f"🎯 Valid Parentheses - {action}", fontweight="bold")

        self.ax_problem.set_xlabel("Posições")
        self.ax_problem.set_ylabel("Caracteres")
        self.ax_problem.set_xticks(range(len(string)))
        self.ax_problem.set_ylim(0, 1.5)


# ============================================================================
# 🎮 RENDERER PARA STREAMLIT
# ============================================================================


class StreamlitRenderer:
    """Renderer otimizado para integração com Streamlit."""

    def __init__(self):
        self.visualizer = InterviewVisualizer()

    def render_problem_analysis(self, problem_id: str, user_code: str, submission_result: Dict[str, Any]):
        """
        Renderiza análise completa do problema no Streamlit.

        Args:
            problem_id: ID do problema
            user_code: Código do usuário
            submission_result: Resultado da submissão

        Returns:
            Figura matplotlib para exibição
        """
        # Extrair dados do resultado
        test_results = submission_result.get("test_results", {})
        code_analysis = submission_result.get("code_analysis", {})

        # Gerar passos de visualização (simulado)
        steps = self._generate_visualization_steps(problem_id, user_code)

        # Criar visualização
        fig = self.visualizer.visualize_problem(problem_id, steps, test_results, code_analysis)

        return fig

    def _generate_visualization_steps(self, problem_id: str, user_code: str) -> List[Dict]:
        """Gera passos de visualização baseados no código do usuário."""
        # Implementação simplificada - na prática, isso seria mais sofisticado
        steps = [
            {"tipo": "inicio", "action": "Iniciando análise do código"},
            {"tipo": "processando", "action": "Analisando estrutura"},
            {"tipo": "final", "action": "Análise concluída"},
        ]

        return steps

    def render_comparison(self, user_solution: str, optimal_solution: str, problem_id: str) -> Dict[str, Any]:
        """
        Renderiza comparação entre solução do usuário e solução ótima.

        Args:
            user_solution: Código do usuário
            optimal_solution: Código da solução ótima
            problem_id: ID do problema

        Returns:
            Dados para comparação visual
        """
        comparison_data = {
            "user_metrics": self._analyze_solution(user_solution),
            "optimal_metrics": self._analyze_solution(optimal_solution),
            "improvements": self._suggest_improvements(user_solution, optimal_solution),
        }

        return comparison_data

    def _analyze_solution(self, code: str) -> Dict[str, Any]:
        """Analisa uma solução e retorna métricas."""
        return {
            "lines": len(code.split("\n")),
            "complexity": "O(n)",  # Simplificado
            "readability": 75,  # Simplificado
            "patterns": ["Hash Map", "Linear Scan"],  # Simplificado
        }

    def _suggest_improvements(self, user_code: str, optimal_code: str) -> List[str]:
        """Sugere melhorias comparando com solução ótima."""
        suggestions = [
            "Considere usar um hash map para reduzir complexidade",
            "Adicione mais comentários para melhorar legibilidade",
            "Implemente validação de entrada",
        ]

        return suggestions


# ============================================================================
# 🧪 FUNÇÕES DE TESTE
# ============================================================================


def test_visualizer():
    """Testa o sistema de visualização."""
    print("🎨 TESTANDO VISUALIZADOR")
    print("=" * 50)

    # Criar visualizador
    visualizer = InterviewVisualizer()

    # Dados de teste para Two Sum
    steps = [
        {
            "tipo": "inicio",
            "nums": [2, 7, 11, 15],
            "target": 9,
            "hash_map": {},
            "current_index": -1,
            "action": "Procurando dois números que somam 9",
        },
        {
            "tipo": "verificacao",
            "nums": [2, 7, 11, 15],
            "target": 9,
            "hash_map": {},
            "current_index": 0,
            "current_num": 2,
            "complement": 7,
            "action": "Verificando nums[0] = 2, procurando 7",
        },
        {
            "tipo": "adicionar",
            "nums": [2, 7, 11, 15],
            "target": 9,
            "hash_map": {2: 0},
            "current_index": 0,
            "action": "Adicionando 2 → 0 ao hash map",
        },
        {
            "tipo": "encontrado",
            "nums": [2, 7, 11, 15],
            "target": 9,
            "hash_map": {2: 0},
            "current_index": 1,
            "complement_index": 0,
            "resultado": [0, 1],
            "action": "Encontrado! índices 0 e 1",
        },
    ]

    test_results = {"passed": 4, "total": 4, "execution_time": 0.001}

    code_analysis = {
        "score": 85,
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "readability": {"comment_ratio": 0.2, "descriptive_names_ratio": 0.8, "avg_line_length": 45},
        "patterns": ["Hash Map", "Linear Scan"],
    }

    # Visualizar
    fig = visualizer.visualize_problem("two_sum", steps, test_results, code_analysis)

    print("✅ Visualização criada com sucesso!")
    print(f"   - Passos: {len(steps)}")
    print(f"   - Testes: {test_results['passed']}/{test_results['total']}")
    print(f"   - Score: {code_analysis['score']}/100")

    return fig


if __name__ == "__main__":
    test_visualizer()
    plt.show()
