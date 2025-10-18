# 🎯 Algoritmos Visualizador - Instruções para Agentes IA

## 🏗️ Visão Geral da Arquitetura

**Plataforma educacional Streamlit** que combina visualização de algoritmos, exercícios interativos e integrações MCP. Estrutura principal:

- **4 Módulos de Aprendizado**: `modulo_1_fundamentos/` (busca/ordenação), `modulo_2_estruturas_dados/`, `modulo_3_programacao_dinamica/`, `modulo_4_entrevistas/`
- **Apps Principais**: `app_integrada.py` (completo), `streamlit_apps/main_app.py` (modular)
- **Cache Inteligente**: `cache_inteligente.py` com decoradores `@cache_visualizacao`, `@cache_algoritmo`, `@cache_mcp`
- **Integração MCP**: `gitmcp_integration.py` para API GitHub, `mcp_tavily_integration.py` para busca web

## 📝 Padrões de Código

### Implementação de Algoritmos (`modulo_1_fundamentos/busca_binaria.py`)
```python
"""
NOME_ALGORITMO - Descrição do Template
Complexidade Temporal: O(log n)
Complexidade Espacial: O(1)

Intuição: Breve explicação da abordagem
"""

def funcao_algoritmo(arr, target):
    """
    Descrição da função com análise Big O.

    Args:
        arr: Array/lista de entrada
        target: Elemento alvo da busca

    Returns:
        int: Resultado ou -1 se não encontrado

    Complexidade: O(log n) tempo, O(1) espaço
    """
    # Implementação com comentários detalhados
```

### Componentes UI Streamlit
```python
# Use st.columns() para layouts responsivos
col1, col2, col3 = st.columns([1, 2, 1])

# Cache operações custosas
@cache_visualizacao
def criar_plot(dados):
    fig, ax = plt.subplots()
    # lógica de plotagem
    return fig

# Trate imports opcionais com elegância
try:
    from modulo_externo import feature
    FEATURE_DISPONIVEL = True
except ImportError:
    FEATURE_DISPONIVEL = False
```

### Padrão de Integração MCP
```python
# Use GitMCPIntegration para operações GitHub
git_client = GitMCPIntegration()
resultado = git_client.buscar_documentacao_algoritmo("busca_binaria")

# Trate respostas da API consistentemente
if resultado and 'status' in resultado and resultado['status'] == 'success':
    # Processe resposta bem-sucedida
else:
    st.warning("Operação falhou")
```

## 🔄 Workflows Críticos

### Desenvolvimento Local
```bash
# Execute app integrado completo
streamlit run app_integrada.py

# Execute versão modular
streamlit run streamlit_apps/main_app.py

# Teste módulo específico
cd modulo_1_fundamentos && python -c "from busca_binaria import *; print('Import OK')"
```

### Deploy
- **Streamlit Cloud**: Usa `app_integrada.py` como ponto de entrada
- **Dependências**: Único `requirements.txt` (não múltiplos arquivos requirements)
- **Secrets**: Configure `TAVILY_API_KEY`, `GITHUB_TOKEN` no dashboard Streamlit Cloud
- **Cache**: Invalidação automática a cada 3600s, memória limitada a 100MB

### Testes
```bash
# Execute testes CI
python -m pytest test_projeto.py -v

# Faça lint do código
flake8 . --max-line-length=127 --exclude=__pycache__,venv,.git

# Formate código
black . --exclude="/(venv|__pycache__|\.git)/"
```

## 🎨 Padrões UI/UX

### Estrutura de Navegação
- **Sidebar**: Seleção de módulos com ícones emoji (📚, 🏗️, 🎯, 💼)
- **Abas**: Sub-recursos dentro dos módulos (Exemplos, Exercícios, Comparação)
- **Divulgação Progressiva**: `st.expander()` para conteúdo detalhado, `st.columns()` para layout responsivo

### Padrões de Visualização
- **Matplotlib**: Plots estáticos com `@cache_visualizacao`
- **Plotly**: Gráficos interativos para dados complexos
- **Animação**: Visualização passo-a-passo de algoritmos
- **Codificação de Cores**: Cores semânticas consistentes (verde=sucesso, vermelho=erro, azul=info)

## 🔗 Pontos de Integração

### Serviços Externos
- **API GitHub**: Busca de documentação via `GitMCPIntegration.buscar_documentacao_algoritmo()`
- **Busca Tavily**: Busca web via servidor MCP em `mcp-server-tavily/`
- **Streamlit Cloud**: Deploy com gerenciamento de secrets

### Comunicação Entre Módulos
- **Estado Compartilhado**: `st.session_state` para rastreamento de progresso do usuário
- **Imports de Módulos**: Manipulação dinâmica de path para carregamento modular
- **Tratamento de Erros**: Degradação elegante quando recursos opcionais não estão disponíveis

## 📋 Convenções do Projeto

### Nomenclatura & Documentação
- **Português**: Nomes de variáveis/funções em português (ex: `busca_binaria`, `janela_deslizante`)
- **Big O Obrigatório**: Todo algoritmo documenta complexidade temporal/espacial
- **Docstrings**: Completas com seções Args/Returns
- **Comentários**: Explicam "porquê", não apenas "o quê"

### Tratamento de Erros
```python
# Tratamento elegante de imports
try:
    from feature_opcional import func
    FEATURE_DISPONIVEL = True
except ImportError:
    FEATURE_DISPONIVEL = False

# Tratamento de erros da API
if resultado.get('status') == 'error':
    st.error(f"Erro: {resultado.get('message', 'Erro desconhecido')}")
```

### Otimização de Performance
- **Estratégia de Cache**: `@cache_visualizacao` para plots, `@cache_algoritmo` para computações
- **Carregamento Preguiçoso**: Importe módulos pesados apenas quando necessário
- **Gerenciamento de Memória**: Limites de tamanho de cache e invalidação baseada em TTL

## 🚨 Armadilhas Comuns

- **Múltiplos Arquivos Requirements**: Streamlit Cloud pode tentar instalar de todos os arquivos `requirements*.txt`
- **Secrets Ausentes**: Integrações de API falham silenciosamente sem tratamento adequado de erros
- **Dependências de Path**: Use `Path(__file__).parent` para imports relativos confiáveis
- **Reruns Streamlit**: Faça cache de operações custosas para prevenir recomputação desnecessária
