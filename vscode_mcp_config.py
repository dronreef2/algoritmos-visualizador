# 🔗 Configuração VS Code + MCP

"""
Configuração para integrar o MCP Server com VS Code.
Permite dynamic tool discovery e comunicação com Streamlit.
"""

import json
from pathlib import Path

# Configuração MCP para VS Code
vscode_mcp_config = {
    "mcpServers": {
        "algorithm-analyzer": {
            "command": "python",
            "args": ["mcp_server.py"],
            "cwd": str(Path.cwd()),
            "env": {
                "PYTHONPATH": str(Path.cwd())
            }
        }
    }
}

# Configuração de settings.json para VS Code
vscode_settings = {
    "mcp.servers": [
        {
            "name": "algorithm-analyzer",
            "description": "Servidor MCP para análise de algoritmos",
            "url": "http://localhost:8000",
            "tools": [
                "analyze_algorithm",
                "benchmark_performance", 
                "suggest_optimizations",
                "generate_code",
                "complexity_calculator",
                "visualize_execution"
            ]
        }
    ],
    "github.copilot.enable": {
        "*": True,
        "yaml": True,
        "plaintext": True,
        "markdown": True,
        "python": True
    },
    "github.copilot.advanced": {
        "debug.overrideEngine": "codex",
        "length": 3000,
        "temperature": 0.1
    }
}

# Instruções customizadas para GitHub Copilot
copilot_instructions = """
# 🧠 Instruções Customizadas - Projeto Algoritmos + MCP

## Contexto do Projeto
Este é um projeto de estudo de algoritmos com integração MCP (Model Context Protocol) e Streamlit.

### Ferramentas MCP Disponíveis:
- `analyze_algorithm`: Análise de complexidade automatizada
- `benchmark_performance`: Testes de performance em tempo real
- `suggest_optimizations`: Sugestões de otimização
- `generate_code`: Geração automática de código
- `complexity_calculator`: Cálculo de Big O
- `visualize_execution`: Dados para visualização

### Padrões de Código:
1. **Análise de Algoritmos**: Sempre incluir complexidade temporal e espacial
2. **Visualizações**: Usar matplotlib/plotly para demonstrações
3. **MCP Integration**: Aproveitar ferramentas dinâmicas quando disponíveis
4. **Documentação**: Explicar o "porquê", não apenas o "como"

### Prompts Sugeridos:
- "/analyze-complexity": Analisar complexidade do código selecionado
- "/optimize-algorithm": Sugerir otimizações usando MCP
- "/generate-visualization": Criar visualização do algoritmo
- "/benchmark-performance": Executar testes de performance

### Estrutura do Projeto:
- `modulo_1_fundamentos/`: Algoritmos fundamentais implementados
- `streamlit_app_mcp.py`: App principal com integração MCP
- `mcp_server.py`: Servidor MCP customizado
- `visualizador_algoritmos.ipynb`: Notebook interativo

### Metodologia dos 3 Passos:
1. **Força Bruta**: Implementação direta
2. **Memoização**: Otimização com cache
3. **Tabulação**: Abordagem bottom-up

Use essas informações como contexto para sugestões mais precisas e relevantes.
"""

def gerar_arquivos_configuracao():
    """Gera arquivos de configuração para VS Code + MCP."""
    
    # Criar diretório .vscode se não existir
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    
    # settings.json
    with open(vscode_dir / 'settings.json', 'w', encoding='utf-8') as f:
        json.dump(vscode_settings, f, indent=2, ensure_ascii=False)
    
    # mcp.json (configuração específica MCP)
    with open(vscode_dir / 'mcp.json', 'w', encoding='utf-8') as f:
        json.dump(vscode_mcp_config, f, indent=2, ensure_ascii=False)
    
    # Instruções para Copilot
    with open('.copilot-instructions.md', 'w', encoding='utf-8') as f:
        f.write(copilot_instructions)
    
    print("✅ Arquivos de configuração gerados:")
    print("  - .vscode/settings.json")
    print("  - .vscode/mcp.json") 
    print("  - .copilot-instructions.md")

# Exemplo de integração com GitHub Copilot Chat
def exemplo_prompt_copilot():
    """Exemplo de como usar prompts customizados com MCP."""
    
    prompts_exemplo = {
        "/analyze-complexity": {
            "description": "Analisa complexidade do código selecionado usando MCP",
            "example": """
            # Selecione o código e use:
            /analyze-complexity
            
            # O Copilot irá:
            # 1. Chamar o MCP server para análise
            # 2. Retornar complexidade temporal/espacial
            # 3. Sugerir otimizações se aplicável
            """
        },
        
        "/optimize-algorithm": {
            "description": "Sugere otimizações usando ferramentas MCP",
            "example": """
            # Com código selecionado:
            /optimize-algorithm --context="large_dataset" --priority="speed"
            
            # Resposta incluirá:
            # - Análise do algoritmo atual
            # - Sugestões de otimização
            # - Algoritmos alternativos
            # - Estimativa de melhoria
            """
        },
        
        "/generate-visualization": {
            "description": "Cria código para visualizar algoritmo",
            "example": """
            /generate-visualization --algorithm="binary_search" --style="animated"
            
            # Gera código para:
            # - Visualização passo a passo
            # - Gráficos interativos
            # - Integração com Streamlit
            """
        },
        
        "/benchmark-performance": {
            "description": "Executa benchmark usando MCP",
            "example": """
            /benchmark-performance --sizes="[100,1000,10000]" --iterations=10
            
            # Retorna:
            # - Tempos de execução
            # - Uso de memória
            # - Gráficos de performance
            # - Score de otimização
            """
        }
    }
    
    return prompts_exemplo

# Workflow de desenvolvimento com MCP
def workflow_desenvolvimento():
    """Descreve o workflow ideal de desenvolvimento."""
    
    workflow = """
    # 🔄 Workflow de Desenvolvimento com MCP + VS Code

    ## 1. Fase de Análise
    ```
    1. Escrever algoritmo inicial
    2. Usar /analyze-complexity para análise automática
    3. Revisar sugestões do MCP server
    4. Documentar complexidade encontrada
    ```

    ## 2. Fase de Otimização  
    ```
    1. Usar /optimize-algorithm para sugestões
    2. Implementar otimizações sugeridas
    3. Executar /benchmark-performance para validar
    4. Comparar resultados antes/depois
    ```

    ## 3. Fase de Visualização
    ```
    1. Usar /generate-visualization para criar demos
    2. Integrar com Streamlit app
    3. Testar interatividade
    4. Deploy automático no Streamlit Cloud
    ```

    ## 4. Fase de Documentação
    ```
    1. GitHub Copilot gera documentação baseada no código
    2. MCP fornece análises técnicas detalhadas
    3. Streamlit exibe documentação interativa
    4. Notebook Jupyter consolida tudo
    ```

    ## 5. Ciclo Contínuo
    ```
    Código → MCP Analysis → Otimização → Visualização → Deploy → Feedback → Repeat
    ```
    """
    
    return workflow

if __name__ == "__main__":
    print("🔧 Configurando integração VS Code + MCP...")
    
    # Gerar arquivos de configuração
    gerar_arquivos_configuracao()
    
    # Mostrar exemplos de prompts
    print("\n🤖 Prompts Copilot disponíveis:")
    prompts = exemplo_prompt_copilot()
    for prompt, info in prompts.items():
        print(f"\n{prompt}")
        print(f"  📝 {info['description']}")
    
    # Mostrar workflow
    print("\n" + workflow_desenvolvimento())
    
    print("""
    🎯 Próximos Passos:
    
    1. ✅ Configuração gerada
    2. 🔄 Reiniciar VS Code para aplicar configurações
    3. 🚀 Executar MCP server: python mcp_server.py
    4. 🎨 Testar integração com prompts customizados
    5. 🌐 Deploy Streamlit app com MCP integration
    
    🎉 Sua configuração MCP + VS Code está pronta!
    """)
