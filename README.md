# 🎯 Algoritmos Visualizador - Aplicação Integrada Completa

[![Python CI](https://github.com/dronreef2/algoritmos-visualizador/actions/workflows/python-ci.yml/badge.svg)](https://github.com/dronreef2/algoritmos-visualizador/actions/workflows/python-ci.yml)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://algoritmos-visualizador.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🚀 **APLICAÇÃO INTEGRADA COMPLETA - VERSÃO 2.0**

Uma plataforma abrangente e integrada para aprendizado de algoritmos e estruturas de dados, combinando todos os módulos em uma experiência unificada com visualizações interativas, exercícios práticos e integração com IA.

---

## � **FUNCIONALIDADES COMPLETAMENTE INTEGRADAS**

### ✅ **Módulos de Aprendizado Completos**
- **📚 Módulo 1: Fundamentos** - Busca binária, dois ponteiros, janela deslizante, backtracking
- **🏗️ Módulo 2: Estruturas de Dados** - Heap, Trie, Union-Find, Segment Tree
- **🎯 Módulo 3: Programação Dinâmica** - Metodologia 3 passos, Knapsack, LCS
- **💼 Módulo 4: Entrevistas Técnicas** - Simulação completa com feedback

### 🎯 **Sistema de Aprendizado Contextualizado**
- **🗺️ Mapa Visual de Aprendizado** - Grafo interativo conectando conceitos
- **🚀 Jornadas Temáticas** - Percursos estruturados por tema
- **📚 Conceitos Interativos** - Exploração profunda com múltiplas perspectivas
- **📊 Acompanhamento de Progresso** - Métricas e recomendações personalizadas

### 🎯 **Exercícios Práticos Interativos**
- **📝 Múltipla Escolha** - Validação automática com feedback imediato
- **🔍 Análise de Complexidade** - Exercícios práticos de Big O
- **🐛 Debugging de Código** - Identificação e correção de bugs
- **🏆 Sistema de Conquistas** - Gamificação do aprendizado

### 🤖 **Busca Inteligente com MCP (Tavily)**
- **🔍 Busca Contextual** - Encontre explicações usando API real do Tavily
- **🧠 Respostas com IA** - Geração automática de respostas contextualizadas
- **📊 Resultados Personalizados** - Controle de profundidade e quantidade
- **⚡ Busca Avançada** - Suporte a buscas `basic` e `advanced`

### 📊 **Visualizações Interativas Avançadas**
- **🎨 Gráficos Matplotlib/Plotly** - Animações passo a passo
- **🎬 Demonstrações em Tempo Real** - Veja algoritmos funcionando
- **📈 Análise de Performance** - Comparação de complexidades
- **🔍 Exploração Detalhada** - Zoom e navegação interativa

### 📊 **Dashboard de Progresso Completo**
- **📈 Métricas de Aprendizado** - Acompanhamento detalhado
- **🏆 Sistema de Conquistas** - Desbloqueie achievements
- **📊 Estatísticas Avançadas** - Análise de performance
- **💡 Recomendações** - Sugestões personalizadas

---

## 🎮 **COMO USAR A APLICAÇÃO INTEGRADA**

### 🚀 **Execução Rápida**
```bash
# Execute a aplicação integrada completa
streamlit run app_integrada.py

# Ou execute módulos específicos
streamlit run streamlit_apps/main_app.py
```

### 🧭 **Navegação Principal**
1. **🏠 Home** - Visão geral e destaques
2. **📚 Módulos 1-4** - Aprendizado estruturado
3. **🎯 Aprendizado Contextualizado** - Jornadas temáticas
4. **🎯 Exercícios Práticos** - Prática interativa
5. **🔍 Busca MCP** - Consultas com IA
6. **📊 Dashboard** - Acompanhamento de progresso
7. **🏆 Conquistas** - Sistema de gamificação

---

## 🏗️ **ARQUITETURA DA APLICAÇÃO INTEGRADA**

```
app_integrada.py (🎯 PRINCIPAL)
├── 🎨 Interface Moderna (CSS Customizado)
├── 🧭 Sistema de Navegação Unificado
├── 📚 Módulos de Aprendizado
│   ├── 🔍 Busca Binária & Algoritmos
│   ├── 🏗️ Estruturas de Dados
│   ├── 🎯 Programação Dinâmica
│   └── 💼 Simulação de Entrevistas
├── 🎯 Aprendizado Contextualizado
│   ├── 🗺️ Mapa Visual
│   ├── 🚀 Jornadas Temáticas
│   └── 📊 Progresso
├── 🎯 Exercícios Práticos
│   ├── 📝 Tipos de Exercício
│   ├── ✅ Validação Automática
│   └── 🏆 Conquistas
├── 🤖 Integração MCP
│   ├── 🔍 Busca Tavily
│   └── 🧠 Respostas IA
└── 📊 Dashboard & Analytics
    ├── 📈 Métricas
    ├── 📊 Visualizações
    └── 💡 Recomendações
```

---

## 📦 **DEPENDÊNCIAS E INSTALAÇÃO**

### 🔧 **Dependências do Sistema**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libxml2-dev libxslt-dev curl git
```

### 🐍 **Dependências Python**
```bash
pip install -r requirements.txt
pip install -r requirements_mcp.txt
```

### 🤖 **Configuração MCP (Opcional)**
```bash
# Configure a chave da API Tavily
cp mcp-server-tavily/.env.example mcp-server-tavily/.env
# Edite .env e adicione sua chave: TAVILY_API_KEY=your_key_here
```

---

## 🎯 **EXPERIÊNCIA DE APRENDIZADO**

### 📚 **Percurso Recomendado**
1. **Comece pelo Home** - Entenda a plataforma
2. **Explore os Módulos** - Aprenda conceitos fundamentais
3. **Pratique com Exercícios** - Aplique o conhecimento
4. **Use a Busca MCP** - Tire dúvidas com IA
5. **Acompanhe o Progresso** - Veja suas conquistas

### 🎮 **Funcionalidades Interativas**
- **Visualizações Animadas** - Veja algoritmos em ação
- **Exercícios Validados** - Feedback imediato
- **Busca Inteligente** - Consultas contextuais
- **Sistema de Conquistas** - Motivação gamificada
- **Dashboard Analítico** - Acompanhamento detalhado

---

## 🚀 **DEPLOYMENT E PRODUÇÃO**

### 🌐 **Streamlit Sharing**
```bash
# A aplicação está pronta para deploy
# Arquivos de configuração incluídos:
# - packages.txt (dependências do sistema)
# - requirements.txt (dependências Python)
# - .streamlit/config.toml (configurações Streamlit)
```

### 🐳 **Docker (Opcional)**
```dockerfile
FROM python:3.9-slim

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \\
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app_integrada.py"]
```

---

## 📊 **MÉTRICAS E MONITORAMENTO**

### 📈 **Indicadores de Uso**
- **Módulos Completados** - Progresso por módulo
- **Exercícios Resolvidos** - Taxa de acerto
- **Tempo de Estudo** - Engajamento do usuário
- **Conquistas Desbloqueadas** - Gamificação

### 🔍 **Analytics Integrados**
- **Dashboard de Progresso** - Visualizações interativas
- **Sistema de Recomendações** - Sugestões personalizadas
- **Análise de Performance** - Métricas de aprendizado
- **Feedback Automático** - Avaliação de exercícios

---

## 🤝 **CONTRIBUIÇÃO E DESENVOLVIMENTO**

### 🛠️ **Estrutura do Projeto**
```
algoritmos-visualizador/
├── app_integrada.py           # 🎯 Aplicação principal integrada
├── streamlit_apps/            # 📱 Aplicações Streamlit modulares
├── modulo_1_fundamentos/      # 🔍 Algoritmos fundamentais
├── modulo_2_estruturas_dados/ # 🏗️ Estruturas de dados
├── modulo_3_programacao_dinamica/ # 🎯 Programação dinâmica
├── modulo_4_entrevistas/      # 💼 Simulação de entrevistas
├── aprendizado_contextual_ui.py # 🎯 Sistema contextualizado
├── exercicios_praticos_ui.py  # 🎯 Exercícios interativos
├── mcp_tavily_integration.py  # 🤖 Integração MCP
└── sistema_*.py              # 🧠 Sistemas core
```

### 🎯 **Áreas de Desenvolvimento**
- [ ] **Integração com Mais APIs** - Expandir busca inteligente
- [ ] **Sistema de Usuários** - Perfis e histórico persistente
- [ ] **Modo Offline** - Funcionalidades sem internet
- [ ] **Mobile Responsivo** - Otimização para dispositivos móveis
- [ ] **Multi-idioma** - Suporte a português e inglês

---

## 📄 **LICENÇA E CRÉDITOS**

**Licença:** MIT License
**Autor:** GitHub Copilot
**Data:** 2025
**Versão:** 2.0 - Aplicação Integrada Completa

### 🙏 **Agradecimentos**
- **Streamlit** - Framework web interativo
- **Tavily API** - Busca inteligente com IA
- **Matplotlib/Plotly** - Visualizações científicas
- **Python Community** - Ecossistema rico e colaborativo

---

## 🎉 **COMECE AGORA!**

```bash
# Execute a aplicação integrada
streamlit run app_integrada.py

# Acesse: http://localhost:8501
```

**🎯 Explore, aprenda e domine algoritmos e estruturas de dados com nossa plataforma integrada completa!**

---

*Desenvolvido com ❤️ para a comunidade de desenvolvedores e estudantes de algoritmos.*

### 🎯 Sistema de Aprendizado Contextualizado ⭐ **NOVO!**
- **Jornadas Temáticas**: Percursos estruturados por tema com objetivos claros
- **Mapa Visual de Aprendizado**: Grafo interativo mostrando conexões entre conceitos
- **Contexto Histórico**: Entenda quando e por que os algoritmos foram criados
- **Aplicações Reais**: Veja como os conceitos são usados no mundo da tecnologia
- **Sistema de Progresso**: Acompanhe seu avanço com métricas e recomendações
- **Exploração Interativa**: Mergulhe fundo em cada conceito com múltiplas perspectivas

### 🤖 Busca Inteligente com MCP (Tavily) ⭐ **NOVO!**
- **Busca Contextual:** Encontre explicações e exemplos na web usando API real do Tavily
- **Respostas com IA:** Geração automática de respostas contextualizadas
- **Busca Avançada:** Suporte a buscas `basic` e `advanced` com controle de profundidade
- **Resultados Personalizados:** Controle do número máximo de resultados (1-10)
- **Integração Completa:** Interface totalmente integrada no Streamlit

### 🔍 Visualização Interativa de Algoritmos
- **Busca Binária:** Animação passo a passo com análise MCP
- **Algoritmos de Ordenação:** Bubble Sort com visualização
- **Fibonacci:** Comparação recursivo vs iterativo
- **Análise de Complexidade:** Big O notation automática

### 🏗️ Estruturas de Dados Avançadas (NOVO!)
- **Heap (Min/Max):** Inserção e extração com visualização de árvore
- **Trie:** Árvore de prefixos para autocompletar
- **Union-Find:** Componentes conectados com path compression
- **Segment Tree:** Consultas de intervalo com lazy propagation
- **LRU Cache:** Implementação com lista duplamente ligada
- **Graph:** BFS/DFS com detecção de ciclos

### 🎯 Programação Dinâmica (NOVO!)
- **Metodologia 3 Passos:** Força Bruta → Memoização → Tabulação
- **Fibonacci:** Comparação de eficiência (135 → 31 → 9 operações)
- **Knapsack 0/1:** Problema da mochila com visualização
- **LCS:** Longest Common Subsequence
- **Coin Change:** Troco mínimo com análise de passos

### 💼 Sistema de Entrevistas Técnicas (NOVO!)
- **Simulação Completa:** Ambiente real de entrevista
- **Análise Automática:** Complexidade, padrões e qualidade
- **Feedback Inteligente:** Sugestões de melhoria
- **Problemas Clássicos:** Two Sum, Valid Parentheses, etc.
- **Pontuação:** Sistema de scoring 0-100

### 🚀 Aplicações Reais Funcionais (NOVO!)
- **Sistema de Busca em Logs:** Timestamp search O(log n)
- **Detector de Fraudes:** Análise de transações financeiras
- **Rede Social BFS:** Graus de separação entre usuários  
- **Agendador Inteligente:** Calendário sem conflitos
- **Sistema de Versionamento:** Gerenciamento de releases
- **12+ sistemas reais testados e funcionando!**

### 🤖 Integração MCP + AI (Model Context Protocol)
- **Análise Automática:** Complexidade temporal/espacial
- **Otimizações Inteligentes:** Sugestões baseadas em contexto
- **Geração de Código:** Algoritmos otimizados automaticamente
- **Benchmarks:** Testes de performance em tempo real
- **🔍 Busca Web Integrada:** MCP Server Tavily para pesquisa contextual

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

### 🎮 Interface Web Completa (NOVO!)
```bash
# Instalar dependências
pip install -r requirements_mcp.txt
pip install networkx  # Para visualizações de grafos

# Executar aplicação web modular
streamlit run streamlit_apps/main_app.py
```

### 📊 Demonstração Completa (NOVO!)
```bash
# Executar demonstração de todos os módulos
python demo_completa.py

# Executar testes integrados
python teste_integrado.py
```

### 🔧 Módulos Individuais (NOVO!)
```bash
# Módulo 2: Estruturas de Dados
python modulo_2_estruturas_dados/estruturas_avancadas.py

# Módulo 3: Programação Dinâmica
python modulo_3_programacao_dinamica/metodologia_3_passos.py

# Módulo 4: Entrevistas Técnicas
python modulo_4_entrevistas/problem_playground.py
```

### Streamlit App (Interface Web Original)
```bash
# Instalar dependências
pip install -r requirements_mcp.txt

# Executar aplicação web
streamlit run streamlit_app_mcp.py
```

### 🔍 MCP Server Tavily (Busca Web Integrada)
```bash
# Verificar configuração
python mcp_config.py

# Executar exemplo de integração
python exemplo_integracao_mcp.py

# Usar em seu código
from mcp_tavily_integration import buscar_web
resultado = buscar_web("algoritmos python explicação")
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

### 📁 **Módulo 1: Fundamentos** ✅ **COMPLETO COM APLICAÇÕES REAIS**
**Técnicas algorítmicas essenciais + Sistemas funcionais**

**🔥 Algoritmos Fundamentais:**
- ✅ [**Busca Binária**](modulo_1_fundamentos/busca_binaria.py) - Framework universal para espaços ordenados
- ✅ [**Dois Ponteiros**](modulo_1_fundamentos/dois_ponteiros.py) - Padrões rápido/lento e esquerda/direita  
- ✅ [**Janela Deslizante**](modulo_1_fundamentos/janela_deslizante.py) - Template para substring/subarray
- ✅ [**Backtracking**](modulo_1_fundamentos/backtracking.py) - Permutações, combinações, subconjuntos
- ✅ [**BFS**](modulo_1_fundamentos/bfs.py) - Busca em largura para caminhos mínimos
- ✅ [**Otimização Arrays**](modulo_1_fundamentos/otimizacao_arrays.py) - Prefixos e diferenças
- ✅ [**Operações Bits**](modulo_1_fundamentos/operacoes_bits.py) - Manipulação eficiente de bits

**🚀 Aplicações Reais Funcionais:**
- ✅ [**Sistema de Busca em Logs**](modulo_1_fundamentos/aplicacoes_reais.py) - Busca por timestamp O(log n)
- ✅ [**Sistema de Versionamento**](modulo_1_fundamentos/aplicacoes_reais.py) - Gerenciamento de releases
- ✅ [**Agendador de Eventos**](modulo_1_fundamentos/aplicacoes_reais.py) - Calendário inteligente
- ✅ [**Detector de Fraudes**](modulo_1_fundamentos/aplicacoes_reais.py) - Análise de transações financeiras
- ✅ [**Rede Social BFS**](modulo_1_fundamentos/aplicacoes_reais.py) - Graus de separação
- ✅ [**Planejador de Turnos**](modulo_1_fundamentos/aplicacoes_reais.py) - Otimização de escalas
- ✅ [**Analisador de DNA**](modulo_1_fundamentos/aplicacoes_reais.py) - Sequenciamento genético
- ✅ [**Compressor de Texto**](modulo_1_fundamentos/aplicacoes_reais.py) - Run-length encoding
- ✅ [**Sistema de Roteamento**](modulo_1_fundamentos/aplicacoes_reais.py) - Caminhos mínimos
- ✅ [**Configurador de Sistema**](modulo_1_fundamentos/aplicacoes_reais.py) - Backtracking avançado
- ✅ [**Otimizador de Recursos**](modulo_1_fundamentos/aplicacoes_reais.py) - Alocação inteligente

**🎯 Templates Prontos para Uso:**
- ✅ [**Casos de Uso Práticos**](modulo_1_fundamentos/casos_uso_praticos.py) - Templates reutilizáveis
- ✅ [**Guia de Entrevistas**](modulo_1_fundamentos/guia_entrevistas.py) - Preparação técnica
- ✅ **Todos os sistemas testados e funcionando!** 🎊

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

## 🎯 Resultados Alcançados

### ✅ **Módulo 1 Completamente Implementado**
- **12+ aplicações reais funcionando** em produção
- **Templates universais** para busca binária, dois ponteiros, BFS, backtracking
- **Sistemas testados** com casos de uso reais
- **Preparação para entrevistas** com guia completo

### 🚀 **Capacidades Desenvolvidas**
- ✅ **Identificar padrões** em problemas novos
- ✅ **Aplicar frameworks** sistematicamente  
- ✅ **Implementar soluções** eficientes e testadas
- ✅ **Usar em projetos reais** - sistemas prontos para produção
- ✅ **Explicar decisões** de design claramente
- ✅ **Resolver problemas de entrevistas** com confiança

### 🎊 **Pronto para Usar!**
Todos os sistemas foram **testados e validados**. Você pode usar essas implementações em:
- **Projetos reais de trabalho**
- **Entrevistas técnicas**  
- **Estudos avançados**
- **Base para sistemas maiores**

## 📖 Recursos Adicionais

- **[Plano Detalhado](PLANO_ESTUDO_ALGORITMOS.md)** - Cronograma completo
- **[Guia de Uso Copilot](GUIA_DE_USO.md)** - Como usar prompts personalizados
- **Exemplos Práticos** - Implementações comentadas em cada módulo

---

**🚀 Comece sua jornada agora! Vá para o [Módulo 1](modulo_1_fundamentos/) e construa uma base sólida em algoritmos.**

## 📁 Estrutura do Projeto

```
algoritmos-visualizador/
├── 📁 mcp-server-tavily/          # 🔍 Servidor MCP para buscas web
│   ├── src/                       # Código fonte do servidor
│   ├── .env                       # ⚙️ Configuração da API
│   ├── run_server.sh             # 🚀 Script de inicialização
│   └── pyproject.toml             # 📦 Dependências
├── 📁 modulo_1_fundamentos/       # ✅ Fundamentos completos
├── 📁 modulo_2_estruturas_dados/  # 🏗️ Estruturas avançadas
├── 📁 modulo_3_programacao_dinamica/ # 🎯 Programação dinâmica
├── 📁 modulo_4_entrevistas/       # 💼 Sistema de entrevistas
├── 📁 streamlit_apps/             # 🌐 Aplicações web
├── 🔧 mcp_tavily_integration.py   # 🔗 Integração MCP
├── 📚 exemplo_integracao_mcp.py   # 💡 Exemplos de uso
├── ⚙️ mcp_config.py               # 🔧 Utilitários de configuração
└── 📖 MCP_TAVILY_README.md        # 📋 Documentação completa
```

Integração com o sistema de exercícios práticos
Adição de cache inteligente para performance
Expansão para outras linguagens de programação
Interface web para exploração interativa