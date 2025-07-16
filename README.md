# 🧮 Algoritmos Visualizador - Streamlit + MCP Integration

Uma aplicação web interativa para visualização e análise de algoritmos, integrada com Model Context Protocol (MCP) para análise avançada com AI.

## 🌟 Funcionalidades Principais

### 🔍 Visualização Interativa de Algoritmos
- **Busca Binária:** Animação passo a passo com análise MCP
- **Algoritmos de Ordenação:** Bubble Sort com visualização
- **Fibonacci:** Comparação recursivo vs iterativo
- **Análise de Complexidade:** Big O notation automática

### 🤖 Integração MCP + AI (Model Context Protocol)
- **Análise Automática:** Complexidade temporal/espacial
- **Otimizações Inteligentes:** Sugestões baseadas em contexto
- **Geração de Código:** Algoritmos otimizados automaticamente
- **Benchmarks:** Testes de performance em tempo real

### 📊 Dashboard Completo
- **Progresso de Estudo:** Acompanhamento de módulos
- **Comparação de Performance:** Gráficos dinâmicos
- **Documentação Integrada:** Explicações detalhadas
- **Testes Interativos:** Execute e compare algoritmos

## 🚀 Deploy Streamlit Community Cloud

**✨ Deploy em poucos minutos - GRATUITO!**

1. **Fork/Clone este repositório**
2. **Acesse:** https://share.streamlit.io  
3. **Conecte sua conta GitHub**
4. **Configure:**
   - Repository: `seu-usuario/algoritmos-visualizador`
   - Branch: `main`
   - Main file: `streamlit_app_mcp.py`
5. **Deploy automático!** 

**Resultado:** URL pública para compartilhar suas visualizações!

## 🛠️ Execução Local

### Streamlit App (Interface Web)
```bash
# Instalar dependências
pip install -r requirements_mcp.txt

# Executar aplicação web
streamlit run streamlit_app_mcp.py
```

### MCP Server (Análise com AI)
```bash
# Executar servidor MCP (opcional, para análise avançada)
python mcp_server.py

# Reiniciar VS Code para integração MCP
```

## 🧠 Projeto de Estudo: Dominando o Pensamento Algorítmico

Um guia completo e prático para desenvolver expertise em algoritmos e estruturas de dados, com foco em preparação para entrevistas técnicas e aprimoramento de habilidades de resolução de problemas.

## 🎯 Objetivos do Projeto

- **Desenvolver pensamento algorítmico sistemático**
- **Dominar padrões fundamentais de resolução de problemas**
- **Implementar estruturas de dados do zero**
- **Aplicar metodologia consistente (3 passos) para problemas complexos**
- **Preparar-se efetivamente para entrevistas técnicas**

## 🧠 Filosofia Central: Metodologia dos 3 Passos

### 1. **Força Bruta Recursiva** 🔄
Entender o problema completamente, mapear todas as possibilidades

### 2. **Memoização (Top-Down)** 📝
Otimizar eliminando cálculos redundantes com cache

### 3. **Tabulação (Bottom-Up)** ⚡
Converter para solução iterativa mais eficiente

## 📚 Estrutura Modular do Curso

### 📁 **Módulo 1: Fundamentos** (3 semanas)
**Técnicas algorítmicas essenciais**

- ✅ [**Busca Binária**](modulo_1_fundamentos/busca_binaria.py) - Framework universal para espaços ordenados
- ✅ [**Dois Ponteiros**](modulo_1_fundamentos/dois_ponteiros.py) - Padrões rápido/lento e esquerda/direita  
- ✅ [**Janela Deslizante**](modulo_1_fundamentos/janela_deslizante.py) - Template para substring/subarray
- ✅ [**Backtracking**](modulo_1_fundamentos/backtracking.py) - Permutações, combinações, subconjuntos
- ✅ [**BFS**](modulo_1_fundamentos/bfs.py) - Busca em largura para caminhos mínimos
- ✅ [**Otimização Arrays**](modulo_1_fundamentos/otimizacao_arrays.py) - Prefixos e diferenças
- ✅ [**Operações Bits**](modulo_1_fundamentos/operacoes_bits.py) - Manipulação eficiente de bits

### 📁 **Módulo 2: Estruturas de Dados** (3 semanas)
**Implementações fundamentais do zero**

- 🔄 **Árvore Binária de Busca** - Operações completas
- 🔄 **Listas Ligadas** - Manipulação avançada de ponteiros
- 🔄 **Heap Binário** - Fila de prioridade eficiente
- 🔄 **Estruturas Monotônicas** - Pilha e fila especializadas
- 🔄 **Union-Find** - Componentes conectados otimizados

### 📁 **Módulo 3: Programação Dinâmica** (4 semanas)
**Metodologia sistemática para DP**

- 🔄 **Problemas Clássicos**: Mochila, LCS, Edit Distance
- 🔄 **Padrões Identificados**: Subsequências, ações, jogos
- 🔄 **Implementação Tripla**: Cada problema em 3 versões

### 📁 **Módulo 4: Entrevistas Técnicas** (2 semanas)
**Problemas de alta frequência**

- 🔄 **LRU Cache** - HashMap + Lista duplamente ligada
- 🔄 **Problema da Celebridade** - Otimização O(N²) → O(N)
- 🔄 **Coletar Água da Chuva** - Múltiplas abordagens
- 🔄 **E mais 3 problemas clássicos**

## 🛠️ Personalização do GitHub Copilot

Este projeto inclui configuração avançada do Copilot para maximizar o aprendizado:

### **Instruções Automáticas**
- `.github/copilot-instructions.md` - Padrões gerais
- `.github/instructions/algorithm.instructions.md` - Específico para algoritmos
- `.github/instructions/review.instructions.md` - Diretrizes de revisão

### **Prompts Personalizados**
- `/generate-algorithm` - Criar novos algoritmos
- `/optimize-algorithm` - Melhorar implementações existentes  
- `/code-review` - Análise detalhada de código

## 🚀 Como Começar

1. **Clone o repositório**
```bash
git clone <seu-repo>
cd algoritimo
```

2. **Configure o VS Code**
   - Certifique-se de que as configurações em `.vscode/settings.json` estão ativas
   - Instale a extensão GitHub Copilot

3. **Siga a progressão modular**
   - Comece pelo Módulo 1
   - Implemente todos os templates
   - Pratique com os exemplos fornecidos

4. **Use os prompts personalizados**
   - `/generate-algorithm` para novos desafios
   - `/optimize-algorithm` para melhorar código existente
   - `/code-review` para análise detalhada

## 📈 Cronograma Sugerido

| Semanas | Módulo | Foco |
|---------|--------|------|
| 1-3 | **Fundamentos** | Templates algorítmicos essenciais |
| 4-6 | **Estruturas** | Implementações do zero |
| 7-10 | **Prog. Dinâmica** | Metodologia dos 3 passos |
| 11-12 | **Entrevistas** | Consolidação prática |

## 🎯 Resultados Esperados

Após completar este curso, você será capaz de:

- ✅ **Identificar padrões** em problemas novos
- ✅ **Aplicar frameworks** sistematicamente
- ✅ **Implementar soluções** eficientes
- ✅ **Otimizar algoritmos** metodicamente
- ✅ **Explicar decisões** de design claramente

## 📖 Recursos Adicionais

- **[Plano Detalhado](PLANO_ESTUDO_ALGORITMOS.md)** - Cronograma completo
- **[Guia de Uso Copilot](GUIA_DE_USO.md)** - Como usar prompts personalizados
- **Exemplos Práticos** - Implementações comentadas em cada módulo

---

**🚀 Comece sua jornada agora! Vá para o [Módulo 1](modulo_1_fundamentos/) e construa uma base sólida em algoritmos.**