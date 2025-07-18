---
description: "Prompt para testar e validar implementações de algoritmos"
mode: "ask"
vars:
  - algorithm_file
  - test_cases
---

# Testar Algoritmo

Analise e execute testes para o algoritmo implementado em `{{algorithm_file}}`.

## Análise Solicitada

### 1. Verificação de Corretude
- ✅ Execute todos os casos de teste incluídos
- ✅ Verifique se os resultados esperados coincidem
- ✅ Identifique casos extremos não cobertos

### 2. Análise de Performance
- ⏱️ Confirme a complexidade temporal declarada
- 💾 Analise uso de memória
- 📊 Sugira melhorias de performance se aplicável

### 3. Qualidade do Código
- 📝 Verifique se documentação está completa
- 🧹 Identifique oportunidades de refatoração
- 🔒 Valide tratamento de entrada inválida

### 4. Casos de Teste Adicionais
- 🧪 Sugira 3-5 casos de teste adicionais
- 🚨 Inclua casos extremos não testados
- 🎯 Foque em cenários de falha potencial

## Exemplo de Testes Adicionais
{{test_cases}}

**Forneça feedback estruturado seguindo as diretrizes de revisão do projeto.**
