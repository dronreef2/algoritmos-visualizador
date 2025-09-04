# Integração MCP Server Tavily

Este documento explica como usar o servidor MCP Tavily integrado ao projeto Algoritmos Visualizador.

## 📋 Visão Geral

O MCP (Model Context Protocol) Server Tavily permite fazer buscas na web usando a API do Tavily, proporcionando resultados de busca contextualizados e relevantes para o projeto.

## 🚀 Configuração Inicial

### 1. Obter Chave da API

1. Acesse [Tavily](https://tavily.com/)
2. Crie uma conta gratuita
3. Obtenha sua chave da API

### 2. Configurar Ambiente

Edite o arquivo `mcp-server-tavily/.env`:

```bash
# Substitua pela sua chave real
TAVILY_API_KEY=sua_chave_aqui
PYTHONIOENCODING=utf-8
```

### 3. Verificar Instalação

Execute o script de demonstração:

```bash
python mcp_tavily_integration.py
```

## 💻 Como Usar

### Uso Básico

```python
from mcp_tavily_integration import TavilySearchClient, buscar_web

# Usando a classe cliente
client = TavilySearchClient()
resultados = client.search("Python algoritmos", "basic")

# Ou usando a função de conveniência
resultados = buscar_web("machine learning conceitos")
```

### Exemplo Completo

```python
from mcp_tavily_integration import TavilySearchClient

# Criar cliente
with TavilySearchClient() as client:
    # Fazer busca
    resultado = client.search(
        query="algoritmos de ordenação explicação",
        search_depth="advanced"  # ou "basic"
    )

    # Verificar resultado
    if "error" in resultado:
        print(f"Erro: {resultado['error']}")
    else:
        print(f"Busca realizada: {resultado['query']}")
        for item in resultado.get('results', []):
            print(f"- {item['title']}: {item['url']}")
```

## 🔧 Funcionalidades

### Busca Básica vs Avançada

- **Basic**: Busca rápida com resultados essenciais
- **Advanced**: Busca mais profunda com mais contexto

### Tratamento de Erros

O cliente trata automaticamente:
- Falta de configuração da API
- Problemas de conectividade
- Limites de taxa da API
- Erros de timeout

## 📁 Estrutura dos Arquivos

```
mcp-server-tavily/
├── src/
│   ├── server.py          # Servidor MCP principal
│   ├── client.py          # Cliente de exemplo
│   └── __init__.py        # Ponto de entrada
├── .env                   # Configurações (API key)
├── run_server.sh         # Script de inicialização
└── pyproject.toml         # Dependências

mcp_tavily_integration.py  # Módulo de integração
```

## 🔍 Exemplos de Uso no Projeto

### Busca de Algoritmos

```python
# Buscar explicações de algoritmos
resultado = buscar_web("como funciona busca binária")
```

### Pesquisa de Conceitos

```python
# Buscar conceitos de programação dinâmica
resultado = buscar_web("programação dinâmica explicação simples")
```

### Pesquisa de Aplicações Práticas

```python
# Buscar aplicações reais de grafos
resultado = buscar_web("aplicações práticas de grafos em python")
```

## 🛠️ Troubleshooting

### Erro: "Servidor não configurado"

**Solução**: Configure a chave da API no arquivo `.env`

### Erro: "Servidor não pôde ser iniciado"

**Solução**:
1. Verifique se todas as dependências estão instaladas
2. Confirme que a chave da API é válida
3. Verifique as permissões dos arquivos

### Erro de Timeout

**Solução**: Use busca "basic" ao invés de "advanced" para queries mais rápidas

## 📊 Limites da API

- **Plano Gratuito**: 1000 buscas/mês
- **Timeout**: 30 segundos por busca
- **Rate Limit**: Depende do plano

## 🔄 Atualizações

Para atualizar o servidor MCP:

```bash
cd mcp-server-tavily
git pull origin main
pip install -e .
```

## 📞 Suporte

Para problemas específicos:
1. Verifique os logs em `mcp-server-tavily/logs/`
2. Teste a conectividade com a API do Tavily
3. Consulte a documentação oficial do Tavily

---

**Nota**: Esta integração permite enriquecer o projeto com buscas contextuais, ajudando no aprendizado e pesquisa de algoritmos.
