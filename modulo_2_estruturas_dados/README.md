# 📊 Módulo 2: Estruturas de Dados e Algoritmos Avançados

## 🎯 Objetivos

- **Dominar algoritmos de ordenação** com visualização passo a passo
- **Implementar algoritmos de grafos** fundamentais
- **Analisar complexidade** temporal e espacial
- **Comparar performance** entre diferentes abordagens

## 📚 Conteúdo Implementado

### 🔄 Algoritmos de Ordenação (`algoritmos_ordenacao.py`)

#### **Algoritmos Implementados:**
1. **Bubble Sort** - O(n²)
   - Algoritmo básico por comparação
   - Visualização de trocas
   - Adaptativo para arrays quase ordenados

2. **Quick Sort** - O(n log n) médio
   - Divisão e conquista
   - Escolha de pivot
   - Recursão visualizada

3. **Merge Sort** - O(n log n) garantido
   - Sempre consistente
   - Stable sort
   - Divisão e merge visualizados

4. **Heap Sort** - O(n log n)
   - Usando estrutura heap
   - In-place sorting
   - Heapify visualizado

5. **Counting Sort** - O(n + k)
   - Para valores limitados
   - Não baseado em comparação
   - Linear para range pequeno

#### **Funcionalidades:**
- ✅ **Tracking de passos** - Cada operação registrada
- ✅ **Análise de complexidade** - Big O para todos
- ✅ **Benchmark automático** - Comparação de performance
- ✅ **Visualização de estados** - Arrays em cada passo

### 🌳 Algoritmos de Grafos (`algoritmos_grafos.py`)

#### **Algoritmos Implementados:**
1. **BFS (Busca em Largura)** - O(V + E)
   - Exploração por níveis
   - Menor caminho em grafos não-ponderados
   - Fila de processamento

2. **DFS (Busca em Profundidade)** - O(V + E)
   - Exploração recursiva
   - Detecção de ciclos
   - Pilha de processamento

3. **Dijkstra** - O((V + E) log V)
   - Menor caminho com pesos
   - Heap priority queue
   - Relaxamento de arestas

4. **Kruskal (MST)** - O(E log E)
   - Árvore geradora mínima
   - Union-Find otimizado
   - Ordenação por peso

5. **Detecção de Ciclos** - O(V + E)
   - DFS com coloração
   - Back edges
   - Grafos dirigidos/não-dirigidos

#### **Estrutura de Dados:**
- **Classe Grafo** completa
- **Representação por lista de adjacência**
- **Suporte a pesos** nas arestas
- **Grafos dirigidos e não-dirigidos**

## 🎮 Como Usar

### **Teste Local:**
```bash
# Algoritmos de ordenação
cd modulo_2_estruturas_dados
python algoritmos_ordenacao.py

# Algoritmos de grafos  
python algoritmos_grafos.py
```

### **No Streamlit (expandido):**
```python
# O streamlit_app_mcp.py foi expandido com:
# - Seção de Algoritmos de Ordenação
# - Visualização de Grafos
# - Comparação de Performance
# - Análise Interativa
```

## 📊 Análise de Complexidade

### **Ordenação:**
| Algoritmo | Melhor | Médio | Pior | Espaço | Estável |
|-----------|--------|-------|------|--------|---------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ |

### **Grafos:**
| Algoritmo | Complexidade Temporal | Complexidade Espacial | Uso |
|-----------|----------------------|---------------------|-----|
| BFS | O(V + E) | O(V) | Menor caminho, níveis |
| DFS | O(V + E) | O(V) | Ciclos, componentes |
| Dijkstra | O((V+E) log V) | O(V) | Menor caminho ponderado |
| Kruskal | O(E log E) | O(V) | Árvore geradora mínima |

## 🎯 Funcionalidades Avançadas

### **1. Tracking de Passos Detalhado:**
```python
# Cada algoritmo retorna:
resultado, passos = algoritmo_com_passos(dados)

# Cada passo contém:
{
    'tipo': 'comparacao',
    'array': [estado_atual],
    'indices': [i, j],
    'action': 'Descrição da operação'
}
```

### **2. Benchmark Automático:**
```python
# Teste de performance
resultados = benchmark_algoritmos([100, 500, 1000])
# Retorna tempos de execução para cada tamanho
```

### **3. Análise Teórica:**
```python
# Características do algoritmo
analise = analisar_complexidade('Quick Sort')
# Retorna: complexidades, propriedades, características
```

### **4. Visualização de Grafos:**
```python
# Criação e manipulação
grafo = Grafo(dirigido=False)
grafo.adicionar_aresta('A', 'B', peso=5)

# Algoritmos com passos
caminho, passos = dijkstra_com_passos(grafo, 'A')
```

## 🚀 Expansões Futuras

### **Próximos Algoritmos:**
- **A* Search** - Pathfinding inteligente
- **Floyd-Warshall** - Todos os caminhos mínimos
- **Prim's Algorithm** - MST alternativo
- **Topological Sort** - Ordenação topológica
- **Strongly Connected Components** - Kosaraju/Tarjan

### **Estruturas de Dados:**
- **Red-Black Trees** - Árvores balanceadas
- **Segment Trees** - Consultas em range
- **Trie** - Estrutura para strings
- **Disjoint Set (Union-Find)** - Componentes conexos

### **Funcionalidades:**
- **Animações em tempo real** no Streamlit
- **Comparação lado a lado** de algoritmos
- **Input customizado** para teste
- **Export de resultados** em JSON/CSV
- **Sharing de configurações** via URL

## 💡 Dicas de Estudo

### **Para Ordenação:**
1. **Entenda os trade-offs** - Tempo vs Espaço vs Estabilidade
2. **Pratique implementação** - Sem olhar referências
3. **Visualize os passos** - Use o tracking implementado
4. **Compare performance** - Execute benchmarks

### **Para Grafos:**
1. **Domine BFS/DFS** - Base para outros algoritmos
2. **Entenda representações** - Lista vs Matriz de adjacência
3. **Pratique problemas** - LeetCode, HackerRank
4. **Visualize execução** - Use os passos implementados

## 📈 Status de Implementação

- ✅ **Algoritmos de Ordenação** - 5 algoritmos completos
- ✅ **Algoritmos de Grafos** - 5 algoritmos fundamentais  
- ✅ **Tracking de Passos** - Visualização detalhada
- ✅ **Análise de Complexidade** - Teórica e prática
- ✅ **Benchmarks** - Comparação automatizada
- ✅ **Testes** - Exemplos de uso
- 🔄 **Integração Streamlit** - Em desenvolvimento
- 📋 **Documentação** - Este README

---

## 🎉 Conclusão

O Módulo 2 fornece uma base sólida em algoritmos fundamentais com foco em:
- **Implementação correta** e eficiente
- **Análise rigorosa** de complexidade  
- **Visualização educativa** de execução
- **Comparação prática** de performance

Estes algoritmos são essenciais para entrevistas técnicas e desenvolvimento profissional! 🚀✨
