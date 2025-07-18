"""
🎯 MÓDULO 4: ENTREVISTAS TÉCNICAS - Problem Playground
=====================================================

Este módulo implementa um ambiente de prática para entrevistas técnicas
com problemas clássicos, sistema de testes e feedback via MCP.

Estrutura:
- Problemas clássicos organizados por categoria
- Sistema de testes automático
- Análise de código via MCP
- Visualizações interativas das soluções
- Feedback e pontuação

Intuição:
Simular o ambiente real de uma entrevista técnica com feedback
imediato e análise de performance para melhorar as habilidades.
"""

import time
import ast
import sys
import io
from typing import List, Dict, Tuple, Any, Optional, Callable
from collections import defaultdict, deque
from contextlib import redirect_stdout, redirect_stderr

# ============================================================================
# 🏗️ SISTEMA DE PROBLEMAS E TESTES
# ============================================================================

class Problem:
    """Classe base para problemas de entrevista."""
    
    def __init__(self, problem_id: str, title: str, description: str, 
                 examples: List[Dict], test_cases: List[Dict], 
                 optimal_solution: Callable, difficulty: str = "Medium"):
        self.problem_id = problem_id
        self.title = title
        self.description = description
        self.examples = examples
        self.test_cases = test_cases
        self.optimal_solution = optimal_solution
        self.difficulty = difficulty
        self.category = "General"
    
    def get_problem_statement(self) -> str:
        """Retorna o enunciado completo do problema."""
        statement = f"# {self.title}\n\n"
        statement += f"**Dificuldade:** {self.difficulty}\n\n"
        statement += f"{self.description}\n\n"
        
        statement += "## Exemplos:\n\n"
        for i, example in enumerate(self.examples, 1):
            statement += f"**Exemplo {i}:**\n"
            statement += f"```\n"
            statement += f"Input: {example['input']}\n"
            statement += f"Output: {example['output']}\n"
            if 'explanation' in example:
                statement += f"Explanation: {example['explanation']}\n"
            statement += f"```\n\n"
        
        return statement

class TestRunner:
    """Sistema de execução de testes para códigos de usuário."""
    
    def __init__(self):
        self.timeout = 5  # segundos
    
    def run_user_code(self, user_code: str, problem: Problem) -> Dict[str, Any]:
        """
        Executa o código do usuário contra os casos de teste.
        
        Args:
            user_code: Código fornecido pelo usuário
            problem: Problema sendo testado
            
        Returns:
            Dicionário com resultados dos testes
        """
        results = {
            'passed': 0,
            'total': len(problem.test_cases),
            'test_results': [],
            'error': None,
            'execution_time': 0
        }
        
        try:
            # Preparar ambiente de execução
            namespace = {}
            exec(user_code, namespace)
            
            # Encontrar função principal (assumindo que é a única função definida)
            user_function = None
            for name, obj in namespace.items():
                if callable(obj) and not name.startswith('_'):
                    user_function = obj
                    break
            
            if user_function is None:
                results['error'] = "Nenhuma função encontrada no código"
                return results
            
            # Executar casos de teste
            start_time = time.time()
            
            for i, test_case in enumerate(problem.test_cases):
                test_result = {
                    'case_number': i + 1,
                    'input': test_case['input'],
                    'expected': test_case['output'],
                    'actual': None,
                    'passed': False,
                    'error': None
                }
                
                try:
                    # Executar função do usuário
                    if isinstance(test_case['input'], dict):
                        actual_output = user_function(**test_case['input'])
                    else:
                        actual_output = user_function(test_case['input'])
                    
                    test_result['actual'] = actual_output
                    test_result['passed'] = actual_output == test_case['output']
                    
                    if test_result['passed']:
                        results['passed'] += 1
                
                except Exception as e:
                    test_result['error'] = str(e)
                
                results['test_results'].append(test_result)
            
            results['execution_time'] = time.time() - start_time
            
        except Exception as e:
            results['error'] = str(e)
        
        return results

class CodeAnalyzer:
    """Analisador de código para feedback e pontuação."""
    
    def __init__(self):
        self.complexity_patterns = {
            'O(1)': ['constant', 'direct access'],
            'O(log n)': ['binary search', 'divide and conquer'],
            'O(n)': ['linear scan', 'single loop'],
            'O(n log n)': ['merge sort', 'heap sort'],
            'O(n²)': ['nested loops', 'bubble sort'],
            'O(2^n)': ['exponential', 'recursive without memo']
        }
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analisa o código do usuário e fornece feedback.
        
        Args:
            code: Código a ser analisado
            
        Returns:
            Dicionário com análise do código
        """
        analysis = {
            'complexity': self._estimate_complexity(code),
            'readability': self._analyze_readability(code),
            'patterns': self._detect_patterns(code),
            'suggestions': self._generate_suggestions(code),
            'score': 0
        }
        
        # Calcular pontuação
        analysis['score'] = self._calculate_score(analysis)
        
        return analysis
    
    def _estimate_complexity(self, code: str) -> Dict[str, str]:
        """Estima a complexidade temporal do código."""
        lines = code.lower().split('\n')
        
        # Análise simples baseada em padrões
        nested_loops = 0
        has_recursion = False
        has_binary_search = False
        
        for line in lines:
            if 'for' in line or 'while' in line:
                nested_loops += 1
            if 'def' in line and any(func_name in line for func_name in ['recursive', 'helper']):
                has_recursion = True
            if 'binary' in line or ('left' in line and 'right' in line and 'mid' in line):
                has_binary_search = True
        
        if has_binary_search:
            time_complexity = 'O(log n)'
        elif has_recursion:
            time_complexity = 'O(2^n)' if 'memo' not in code else 'O(n)'
        elif nested_loops >= 2:
            time_complexity = 'O(n²)'
        elif nested_loops == 1:
            time_complexity = 'O(n)'
        else:
            time_complexity = 'O(1)'
        
        return {
            'time': time_complexity,
            'space': 'O(1)' if not has_recursion else 'O(n)'
        }
    
    def _analyze_readability(self, code: str) -> Dict[str, Any]:
        """Analisa a legibilidade do código."""
        lines = code.split('\n')
        
        # Métricas básicas
        total_lines = len([line for line in lines if line.strip()])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        
        # Análise de nomes de variáveis
        variable_names = []
        for line in lines:
            if '=' in line and not line.strip().startswith('#'):
                parts = line.split('=')
                if len(parts) >= 2:
                    var_name = parts[0].strip()
                    if var_name.isidentifier():
                        variable_names.append(var_name)
        
        descriptive_names = sum(1 for name in variable_names if len(name) > 2)
        
        return {
            'total_lines': total_lines,
            'comment_ratio': comment_lines / total_lines if total_lines > 0 else 0,
            'avg_line_length': avg_line_length,
            'descriptive_names_ratio': descriptive_names / len(variable_names) if variable_names else 0
        }
    
    def _detect_patterns(self, code: str) -> List[str]:
        """Detecta padrões algorítmicos no código."""
        patterns = []
        code_lower = code.lower()
        
        pattern_keywords = {
            'Two Pointers': ['left', 'right', 'pointer'],
            'Sliding Window': ['window', 'sliding', 'left', 'right'],
            'Binary Search': ['binary', 'left', 'right', 'mid'],
            'Dynamic Programming': ['dp', 'memo', 'cache'],
            'Recursion': ['recursive', 'helper', 'return.*\\('],
            'Hash Map': ['dict', 'map', 'hash'],
            'Stack': ['stack', 'append', 'pop'],
            'Queue': ['queue', 'deque', 'popleft']
        }
        
        for pattern, keywords in pattern_keywords.items():
            if any(keyword in code_lower for keyword in keywords):
                patterns.append(pattern)
        
        return patterns
    
    def _generate_suggestions(self, code: str) -> List[str]:
        """Gera sugestões de melhoria."""
        suggestions = []
        
        # Análise básica
        if 'for' in code and 'range(len(' in code:
            suggestions.append("Considere usar enumeração: 'for i, item in enumerate(list)'")
        
        if code.count('for') >= 2:
            suggestions.append("Verifique se há como reduzir loops aninhados")
        
        if '#' not in code:
            suggestions.append("Adicione comentários para explicar a lógica")
        
        if 'def' in code and 'return' not in code:
            suggestions.append("Verifique se a função retorna o valor correto")
        
        return suggestions
    
    def _calculate_score(self, analysis: Dict[str, Any]) -> int:
        """Calcula pontuação baseada na análise."""
        score = 50  # Base
        
        # Pontuação por complexidade
        complexity_scores = {
            'O(1)': 30, 'O(log n)': 25, 'O(n)': 20,
            'O(n log n)': 15, 'O(n²)': 10, 'O(2^n)': 5
        }
        score += complexity_scores.get(analysis['complexity']['time'], 0)
        
        # Pontuação por legibilidade
        readability = analysis['readability']
        score += min(15, int(readability['comment_ratio'] * 30))
        score += min(10, int(readability['descriptive_names_ratio'] * 20))
        
        # Bonus por padrões conhecidos
        score += min(15, len(analysis['patterns']) * 5)
        
        return min(100, score)

# ============================================================================
# 📚 PROBLEMAS CLÁSSICOS
# ============================================================================

# Problema 1: Two Sum
def two_sum_optimal(nums: List[int], target: int) -> List[int]:
    """Solução ótima para Two Sum usando hash map."""
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return []

TWO_SUM_PROBLEM = Problem(
    problem_id="two_sum",
    title="Two Sum",
    description="""
    Dado um array de inteiros `nums` e um inteiro `target`, retorne os índices
    dos dois números que somam o target.
    
    Você pode assumir que cada entrada tem exatamente uma solução, e você
    não pode usar o mesmo elemento duas vezes.
    """,
    examples=[
        {
            'input': {'nums': [2, 7, 11, 15], 'target': 9},
            'output': [0, 1],
            'explanation': "nums[0] + nums[1] = 2 + 7 = 9"
        },
        {
            'input': {'nums': [3, 2, 4], 'target': 6},
            'output': [1, 2],
            'explanation': "nums[1] + nums[2] = 2 + 4 = 6"
        }
    ],
    test_cases=[
        {'input': {'nums': [2, 7, 11, 15], 'target': 9}, 'output': [0, 1]},
        {'input': {'nums': [3, 2, 4], 'target': 6}, 'output': [1, 2]},
        {'input': {'nums': [3, 3], 'target': 6}, 'output': [0, 1]},
        {'input': {'nums': [1, 2, 3, 4, 5], 'target': 9}, 'output': [3, 4]},
    ],
    optimal_solution=two_sum_optimal,
    difficulty="Easy"
)

# Problema 2: Valid Parentheses
def valid_parentheses_optimal(s: str) -> bool:
    """Solução ótima para Valid Parentheses usando stack."""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack

VALID_PARENTHESES_PROBLEM = Problem(
    problem_id="valid_parentheses",
    title="Valid Parentheses",
    description="""
    Dado uma string `s` contendo apenas os caracteres '(', ')', '{', '}', '[' e ']',
    determine se a string de entrada é válida.
    
    Uma string de entrada é válida se:
    1. Parênteses abertos são fechados pelo mesmo tipo de parênteses
    2. Parênteses abertos são fechados na ordem correta
    3. Todo parêntese fechado tem um parêntese aberto correspondente do mesmo tipo
    """,
    examples=[
        {'input': '()', 'output': True, 'explanation': "Parênteses balanceados"},
        {'input': '()[]{}}', 'output': True, 'explanation': "Todos os tipos balanceados"},
        {'input': '(]', 'output': False, 'explanation': "Tipos não correspondentes"},
    ],
    test_cases=[
        {'input': '()', 'output': True},
        {'input': '()[]{}}', 'output': True},
        {'input': '(]', 'output': False},
        {'input': '([)]', 'output': False},
        {'input': '{[]}', 'output': True},
        {'input': '', 'output': True},
    ],
    optimal_solution=valid_parentheses_optimal,
    difficulty="Easy"
)

# Problema 3: Reverse Linked List
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list_optimal(head: ListNode) -> ListNode:
    """Solução ótima para Reverse Linked List iterativa."""
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev

REVERSE_LINKED_LIST_PROBLEM = Problem(
    problem_id="reverse_linked_list",
    title="Reverse Linked List",
    description="""
    Dado o `head` de uma lista ligada, inverta a lista e retorne o novo head.
    """,
    examples=[
        {'input': [1, 2, 3, 4, 5], 'output': [5, 4, 3, 2, 1]},
        {'input': [1, 2], 'output': [2, 1]},
        {'input': [], 'output': []}
    ],
    test_cases=[
        {'input': [1, 2, 3, 4, 5], 'output': [5, 4, 3, 2, 1]},
        {'input': [1, 2], 'output': [2, 1]},
        {'input': [], 'output': []},
        {'input': [1], 'output': [1]},
    ],
    optimal_solution=reverse_linked_list_optimal,
    difficulty="Easy"
)

# ============================================================================
# 🎬 VISUALIZADOR DE SOLUÇÕES
# ============================================================================

class SolutionVisualizer:
    """Gerador de visualizações para soluções ótimas."""
    
    def __init__(self, problem: Problem):
        self.problem = problem
    
    def generate_steps(self, test_input: Any) -> List[Dict[str, Any]]:
        """
        Gera passos de visualização para a solução ótima.
        
        Args:
            test_input: Entrada para o teste
            
        Returns:
            Lista de passos para visualização
        """
        if self.problem.problem_id == "two_sum":
            return self._generate_two_sum_steps(test_input)
        elif self.problem.problem_id == "valid_parentheses":
            return self._generate_valid_parentheses_steps(test_input)
        else:
            return []
    
    def _generate_two_sum_steps(self, test_input: Dict) -> List[Dict[str, Any]]:
        """Gera passos para visualização do Two Sum."""
        nums = test_input['nums']
        target = test_input['target']
        steps = []
        
        steps.append({
            'tipo': 'inicio',
            'nums': nums,
            'target': target,
            'hash_map': {},
            'current_index': -1,
            'action': f'Procurando dois números que somam {target}'
        })
        
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            
            steps.append({
                'tipo': 'verificacao',
                'nums': nums,
                'target': target,
                'hash_map': num_to_index.copy(),
                'current_index': i,
                'current_num': num,
                'complement': complement,
                'action': f'Verificando nums[{i}] = {num}, procurando {complement}'
            })
            
            if complement in num_to_index:
                steps.append({
                    'tipo': 'encontrado',
                    'nums': nums,
                    'target': target,
                    'hash_map': num_to_index.copy(),
                    'current_index': i,
                    'complement_index': num_to_index[complement],
                    'resultado': [num_to_index[complement], i],
                    'action': f'Encontrado! índices {num_to_index[complement]} e {i}'
                })
                break
            
            num_to_index[num] = i
            steps.append({
                'tipo': 'adicionar',
                'nums': nums,
                'target': target,
                'hash_map': num_to_index.copy(),
                'current_index': i,
                'action': f'Adicionando {num} -> {i} ao hash map'
            })
        
        return steps
    
    def _generate_valid_parentheses_steps(self, s: str) -> List[Dict[str, Any]]:
        """Gera passos para visualização do Valid Parentheses."""
        steps = []
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        steps.append({
            'tipo': 'inicio',
            'string': s,
            'stack': stack.copy(),
            'current_index': -1,
            'action': f'Verificando string "{s}"'
        })
        
        for i, char in enumerate(s):
            steps.append({
                'tipo': 'processando',
                'string': s,
                'stack': stack.copy(),
                'current_index': i,
                'current_char': char,
                'action': f'Processando caractere "{char}" na posição {i}'
            })
            
            if char in mapping:
                if not stack or stack[-1] != mapping[char]:
                    steps.append({
                        'tipo': 'erro',
                        'string': s,
                        'stack': stack.copy(),
                        'current_index': i,
                        'current_char': char,
                        'action': f'Erro: "{char}" não tem correspondente válido'
                    })
                    break
                else:
                    popped = stack.pop()
                    steps.append({
                        'tipo': 'match',
                        'string': s,
                        'stack': stack.copy(),
                        'current_index': i,
                        'current_char': char,
                        'popped': popped,
                        'action': f'Match: "{popped}" com "{char}"'
                    })
            else:
                stack.append(char)
                steps.append({
                    'tipo': 'push',
                    'string': s,
                    'stack': stack.copy(),
                    'current_index': i,
                    'current_char': char,
                    'action': f'Empilhando "{char}"'
                })
        
        resultado = len(stack) == 0
        steps.append({
            'tipo': 'final',
            'string': s,
            'stack': stack.copy(),
            'resultado': resultado,
            'action': f'Resultado: {resultado} (stack {"vazia" if resultado else "não vazia"})'
        })
        
        return steps

# ============================================================================
# 🎯 SISTEMA DE ENTREVISTA
# ============================================================================

class InterviewSession:
    """Sistema de simulação de entrevista técnica."""
    
    def __init__(self):
        self.problems = {
            "two_sum": TWO_SUM_PROBLEM,
            "valid_parentheses": VALID_PARENTHESES_PROBLEM,
            "reverse_linked_list": REVERSE_LINKED_LIST_PROBLEM,
        }
        self.test_runner = TestRunner()
        self.code_analyzer = CodeAnalyzer()
        self.current_problem = None
        self.session_start_time = None
    
    def start_session(self, problem_id: str):
        """Inicia uma sessão de entrevista."""
        self.current_problem = self.problems.get(problem_id)
        self.session_start_time = time.time()
        return self.current_problem
    
    def submit_solution(self, user_code: str) -> Dict[str, Any]:
        """
        Submete uma solução e retorna feedback completo.
        
        Args:
            user_code: Código do usuário
            
        Returns:
            Dicionário com resultados completos
        """
        if not self.current_problem:
            return {'error': 'Nenhum problema ativo'}
        
        # Executar testes
        test_results = self.test_runner.run_user_code(user_code, self.current_problem)
        
        # Analisar código
        code_analysis = self.code_analyzer.analyze_code(user_code)
        
        # Calcular pontuação final
        final_score = self._calculate_final_score(test_results, code_analysis)
        
        # Gerar feedback
        feedback = self._generate_feedback(test_results, code_analysis, final_score)
        
        return {
            'test_results': test_results,
            'code_analysis': code_analysis,
            'final_score': final_score,
            'feedback': feedback,
            'session_time': time.time() - self.session_start_time if self.session_start_time else 0
        }
    
    def _calculate_final_score(self, test_results: Dict, code_analysis: Dict) -> int:
        """Calcula pontuação final baseada nos testes e análise."""
        score = 0
        
        # Corretude (50%)
        if test_results['passed'] == test_results['total']:
            score += 50
        else:
            score += (test_results['passed'] / test_results['total']) * 50
        
        # Qualidade do código (50%)
        score += code_analysis['score'] * 0.5
        
        return min(100, int(score))
    
    def _generate_feedback(self, test_results: Dict, code_analysis: Dict, final_score: int) -> str:
        """Gera feedback textual para o usuário."""
        feedback = []
        
        # Feedback sobre testes
        if test_results['passed'] == test_results['total']:
            feedback.append("✅ Parabéns! Todos os testes passaram.")
        else:
            feedback.append(f"❌ {test_results['passed']}/{test_results['total']} testes passaram.")
        
        # Feedback sobre complexidade
        complexity = code_analysis['complexity']
        feedback.append(f"📊 Complexidade: {complexity['time']} tempo, {complexity['space']} espaço")
        
        # Feedback sobre padrões
        if code_analysis['patterns']:
            feedback.append(f"🎯 Padrões identificados: {', '.join(code_analysis['patterns'])}")
        
        # Sugestões
        if code_analysis['suggestions']:
            feedback.append("💡 Sugestões:")
            for suggestion in code_analysis['suggestions']:
                feedback.append(f"   • {suggestion}")
        
        # Pontuação final
        if final_score >= 90:
            feedback.append("🎉 Excelente! Solução de alta qualidade.")
        elif final_score >= 70:
            feedback.append("👍 Boa solução! Alguns pontos para melhorar.")
        else:
            feedback.append("📚 Continue praticando! Há espaço para melhorias.")
        
        return "\n".join(feedback)

# ============================================================================
# 🧪 FUNÇÕES DE TESTE
# ============================================================================

def test_interview_system():
    """Testa o sistema de entrevistas."""
    print("🎯 TESTANDO SISTEMA DE ENTREVISTAS")
    print("=" * 50)
    
    # Inicializar sessão
    session = InterviewSession()
    
    # Teste 1: Two Sum
    print("\n📝 Teste 1: Two Sum")
    print("-" * 30)
    
    problem = session.start_session("two_sum")
    print(f"Problema: {problem.title}")
    
    # Código do usuário (solução correta)
    user_code = """
def two_sum(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return []
"""
    
    result = session.submit_solution(user_code)
    print(f"Pontuação: {result['final_score']}/100")
    print(f"Testes: {result['test_results']['passed']}/{result['test_results']['total']}")
    print(f"Complexidade: {result['code_analysis']['complexity']['time']}")
    print(f"Padrões: {result['code_analysis']['patterns']}")
    
    # Teste 2: Valid Parentheses
    print("\n📝 Teste 2: Valid Parentheses")
    print("-" * 30)
    
    problem = session.start_session("valid_parentheses")
    
    # Código do usuário (solução subótima)
    user_code = """
def valid_parentheses(s):
    # Solução O(n²) - não otimizada
    while '()' in s or '[]' in s or '{}' in s:
        s = s.replace('()', '').replace('[]', '').replace('{}', '')
    return s == ''
"""
    
    result = session.submit_solution(user_code)
    print(f"Pontuação: {result['final_score']}/100")
    print(f"Testes: {result['test_results']['passed']}/{result['test_results']['total']}")
    print(f"Complexidade: {result['code_analysis']['complexity']['time']}")
    print(f"Feedback: {result['feedback']}")

if __name__ == "__main__":
    test_interview_system()
