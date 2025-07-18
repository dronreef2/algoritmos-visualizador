# 🎯 Módulo 4: Entrevistas Técnicas

## 🎯 Objetivo
Aplicar todos os conhecimentos adquiridos em um ambiente de prática de entrevistas técnicas.

## 📚 Estrutura do "Problem Playground"

### Interface em 3 Colunas
1. **Coluna Esquerda**: Problema e Código
2. **Coluna Central**: Visualização/Saída
3. **Coluna Direita**: Player/Controles

## 🏆 Problemas Clássicos de Entrevistas

### 1. Estruturas de Dados
- **LRU Cache** - Least Recently Used Cache
- **Design Hash Map** - Implementação de mapa hash
- **Implement Stack/Queue** - Estruturas básicas
- **Binary Search Tree** - Árvore de busca binária

### 2. Arrays e Strings
- **Two Sum** - Soma de dois números
- **Valid Parentheses** - Parênteses balanceados
- **Longest Substring** - Substring sem repetição
- **Merge Intervals** - Fusão de intervalos

### 3. Linked Lists
- **Reverse Linked List** - Inverter lista ligada
- **Merge Two Sorted Lists** - Mesclar listas ordenadas
- **Detect Cycle** - Detectar ciclo em lista
- **Find Intersection** - Encontrar interseção

### 4. Árvores e Grafos
- **Binary Tree Traversal** - Percurso em árvore
- **Maximum Depth** - Profundidade máxima
- **Valid Binary Search Tree** - Validar BST
- **Course Schedule** - Ordenação topológica

### 5. Programação Dinâmica
- **Climbing Stairs** - Subindo escadas
- **House Robber** - Problema do ladrão
- **Coin Change** - Troco de moedas
- **Longest Increasing Subsequence** - LIS

## 🎬 Interface Interativa

### Coluna Esquerda (Problema e Código)
```python
# Componentes Streamlit
st.markdown("### 📋 Descrição do Problema")
st.markdown(problem_description)

st.markdown("### 📝 Exemplos")
st.code(examples, language='python')

st.markdown("### 💻 Seu Código")
user_code = st.text_area("Escreva sua solução:", height=300)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🧪 Executar Testes"):
        run_tests(user_code)
with col2:
    if st.button("🔍 Analisar Código"):
        analyze_with_mcp(user_code)
with col3:
    if st.button("💡 Mostrar Solução"):
        show_optimal_solution()
```

### Coluna Central (Visualização/Saída)
```python
# Área dinâmica baseada na ação do usuário
if user_action == "run_tests":
    show_test_results()
elif user_action == "analyze_code":
    show_mcp_analysis()
elif user_action == "show_solution":
    show_interactive_visualization()
```

### Coluna Direita (Player/Controles)
```python
# Controles para solução otimizada
if solution_visible:
    st.markdown("### 🎮 Controles")
    step = st.slider("Passo", 0, len(steps)-1, 0)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏮️ Anterior"):
            step = max(0, step-1)
    with col2:
        if st.button("⏭️ Próximo"):
            step = min(len(steps)-1, step+1)
    
    st.markdown("### 📊 Análise")
    st.info(f"Passo {step+1}: {steps[step]['description']}")
    st.json(steps[step]['state'])
```

## 🔧 Arquitetura de Implementação

### Sistema de Testes
```python
class TestRunner:
    def __init__(self, problem_id):
        self.problem = load_problem(problem_id)
        self.test_cases = self.problem['test_cases']
    
    def run_user_code(self, user_code):
        # Executa código do usuário
        # Compara com casos de teste
        # Retorna resultados
        pass
    
    def analyze_complexity(self, user_code):
        # Envia para MCP server
        # Retorna análise de complexidade
        pass
```

### Visualizador de Soluções
```python
class SolutionVisualizer:
    def __init__(self, problem_id):
        self.solution = load_optimal_solution(problem_id)
        self.steps = self.solution['steps']
    
    def render_step(self, step_index):
        # Renderiza visualização do passo
        # Usa componentes apropriados (gráfico, tabela, etc.)
        pass
```

### Integração MCP
```python
class InterviewMentor:
    def __init__(self):
        self.mcp_client = MCPClient()
    
    def analyze_user_code(self, code):
        return self.mcp_client.call_tool('analyze_algorithm', {
            'code': code,
            'context': 'interview_practice'
        })
    
    def suggest_optimizations(self, code):
        return self.mcp_client.call_tool('suggest_optimizations', {
            'code': code,
            'focus': 'interview_performance'
        })
```

## 📊 Feedback e Análise

### Métricas de Avaliação
- **Corretude**: Passou em todos os testes?
- **Complexidade**: Temporal e espacial
- **Legibilidade**: Código limpo e bem estruturado
- **Otimização**: Usa a melhor abordagem?

### Sistema de Pontuação
```python
def calculate_score(user_code, test_results, mcp_analysis):
    score = 0
    
    # Corretude (40%)
    if test_results['all_passed']:
        score += 40
    
    # Complexidade (30%)
    if mcp_analysis['complexity']['optimal']:
        score += 30
    
    # Legibilidade (20%)
    score += mcp_analysis['readability_score'] * 0.2
    
    # Otimização (10%)
    score += mcp_analysis['optimization_score'] * 0.1
    
    return min(100, score)
```

## 🎯 Casos de Uso Práticos

### Preparação para Entrevistas
- **Prática Guiada**: Problemas ordenados por dificuldade
- **Feedback Imediato**: Análise automática via MCP
- **Comparação**: Sua solução vs. solução ótima
- **Timing**: Prática com cronômetro

### Simulação de Entrevista
- **Ambiente Real**: Interface similar a entrevistas
- **Pressão de Tempo**: Cronômetro visível
- **Feedback Pós-Entrevista**: Análise detalhada
- **Áreas de Melhoria**: Sugestões específicas

## 🚀 Como Usar

1. **Selecione o Problema**: Escolha da lista de problemas
2. **Leia a Descrição**: Entenda o problema completamente
3. **Escreva Sua Solução**: Use o editor de código
4. **Execute os Testes**: Verifique se funciona
5. **Analise o Feedback**: Use as sugestões do MCP
6. **Compare com Ótima**: Veja a solução visualizada
7. **Pratique Mais**: Tente problemas similares

## 📈 Integração MCP

### Análise Automática
- **Feedback Instantâneo**: Análise em tempo real
- **Sugestões Personalizadas**: Baseadas no seu código
- **Detecção de Padrões**: Identifica abordagens comuns
- **Benchmark**: Compara com soluções típicas

### Mentor Virtual
- **Dicas Contextuais**: Ajuda quando necessário
- **Estratégias**: Ensina como abordar problemas
- **Best Practices**: Padrões de código para entrevistas
- **Preparação**: Roadmap personalizado

## 📊 Próximos Passos

- Implementar todos os problemas clássicos
- Adicionar sistema de testes automáticos
- Integrar cronômetro e simulação de entrevista
- Criar sistema de pontuação e progresso
- Adicionar feedback personalizado via MCP
