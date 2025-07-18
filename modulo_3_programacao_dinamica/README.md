# 🧠 Módulo 3: Programação Dinâmica

## 🎯 Objetivo
Dominar a metodologia dos 3 passos para resolver problemas de programação dinâmica com visualizações interativas.

## 📚 Metodologia dos 3 Passos

### 1. 🔴 Força Bruta (Recursive)
- **Objetivo**: Entender o problema e a recorrência
- **Complexidade**: Exponencial (geralmente)
- **Visualização**: Árvore de recursão completa
- **Problema**: Muitas repetições de cálculos

### 2. 🟡 Memoização (Top-Down)
- **Objetivo**: Otimizar com cache
- **Complexidade**: Linear/Polinomial
- **Visualização**: Árvore de recursão com cache
- **Melhoria**: Evita recalcular subproblemas

### 3. 🟢 Tabulação (Bottom-Up)
- **Objetivo**: Solução iterativa otimizada
- **Complexidade**: Linear/Polinomial
- **Visualização**: Tabela sendo preenchida
- **Vantagem**: Melhor uso de memória

## 📚 Problemas Clássicos

### 1. Fibonacci
- **Recorrência**: F(n) = F(n-1) + F(n-2)
- **Caso Base**: F(0) = 0, F(1) = 1
- **Visualização**: Árvore de recursão → Cache → Tabela

### 2. Problema da Mochila (Knapsack)
- **Recorrência**: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])
- **Caso Base**: dp[0][w] = 0
- **Visualização**: Tabela 2D sendo preenchida

### 3. Longest Common Subsequence (LCS)
- **Recorrência**: dp[i][j] = dp[i-1][j-1] + 1 (se chars iguais)
- **Caso Base**: dp[0][j] = dp[i][0] = 0
- **Visualização**: Comparação de strings com tabela

### 4. Edit Distance (Levenshtein)
- **Recorrência**: dp[i][j] = min(insert, delete, replace)
- **Caso Base**: dp[0][j] = j, dp[i][0] = i
- **Visualização**: Transformação de strings

### 5. Coin Change
- **Recorrência**: dp[amount] = min(dp[amount-coin] + 1) para cada coin
- **Caso Base**: dp[0] = 0
- **Visualização**: Grafo de estados

## 🎬 Visualizações Interativas

### Interface em Abas
- **Aba 1**: Força Bruta + Árvore de Recursão
- **Aba 2**: Memoização + Árvore com Cache
- **Aba 3**: Tabulação + Tabela DP

### Painéis de Visualização
- **Painel Esquerdo**: Código das 3 implementações
- **Painel Central**: Visualização principal (árvore ou tabela)
- **Painel Direito**: Controles e análise

### Player Controls
- **Slider de Passos**: Navegue pela construção
- **Botões Play/Pause**: Controle automático
- **Velocidade**: Ajuste a velocidade da animação

## 🔧 Arquitetura de Visualização

### Força Bruta
```python
def render_recursion_tree(calls, current_call):
    # Gera árvore com graphviz
    # Destaca chamadas repetidas
    # Mostra sobreposição de subproblemas
```

### Memoização
```python
def render_memo_tree(calls, cache, current_call):
    # Mostra árvore com cache
    # Destaca hits e misses
    # Visualiza economia de cálculos
```

### Tabulação
```python
def render_dp_table(table, current_cell):
    # Mostra tabela sendo preenchida
    # Destaca célula atual e dependências
    # Visualiza fórmula de transição
```

## 📊 Análise Comparativa

### Métricas Coletadas
- **Tempo de Execução**: Medição precisa
- **Número de Chamadas**: Contagem de recursões
- **Uso de Memória**: Espaço ocupado
- **Cache Hits/Misses**: Eficiência da memoização

### Comparação Visual
```
Força Bruta: 🔴 2^n tempo, O(n) espaço
Memoização:  🟡 O(n) tempo, O(n) espaço
Tabulação:   🟢 O(n) tempo, O(1) espaço
```

## 🎯 Casos de Uso Práticos

### Problemas Clássicos
- **Otimização de Recursos**: Knapsack, Coin Change
- **Análise de Strings**: LCS, Edit Distance
- **Sequências**: Fibonacci, Climbing Stairs
- **Grafos**: Shortest Path, Longest Path

### Aplicações Reais
- **Algoritmos de Busca**: Otimização de consultas
- **Bioinformática**: Alinhamento de sequências
- **Economia**: Otimização de investimentos
- **Jogos**: Estratégias ótimas

## 🚀 Como Usar

1. **Selecione o Problema**: Use o sidebar para escolher
2. **Configure os Parâmetros**: Tamanho, valores, etc.
3. **Compare as Abordagens**: Veja as 3 implementações
4. **Analise a Visualização**: Entenda como cada uma funciona
5. **Compare Performance**: Veja as métricas lado a lado

## 📈 Integração MCP

### Análise Automática
- **Análise de Complexidade**: Verificação automática
- **Sugestões de Otimização**: Melhorias propostas
- **Detecção de Padrões**: Identificação de recorrências

### Geração de Código
- **Templates Automáticos**: Código base para novos problemas
- **Otimizações**: Sugestões de melhoria
- **Testes**: Casos de teste automáticos

## 📊 Próximos Passos

- Implementar todos os problemas clássicos
- Adicionar visualizações interativas
- Integrar análise MCP para otimizações
- Criar laboratório de prática
- Adicionar problemas de entrevistas
