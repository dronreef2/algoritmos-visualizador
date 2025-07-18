---
description: "Prompt para gerar implementações de algoritmos com explicações detalhadas"
mode: "edit"
tools: ["codebase"]
---

# Gerar Algoritmo

Implemente o algoritmo solicitado seguindo esta estrutura:

## 1. Explicação da Abordagem
- Descreva a estratégia em linguagem natural
- Explique a intuição por trás da solução
- Mencione algoritmos relacionados ou alternativos

## 2. Análise de Complexidade
- **Tempo**: Complexidade temporal (melhor, médio, pior caso)
- **Espaço**: Complexidade espacial
- **Justificativa**: Por que essas complexidades são necessárias

## 3. Implementação
```${fileBasenameNoExtension}
// Incluir:
// - Função principal bem documentada
// - Funções auxiliares se necessário
// - Validação de entrada
// - Comentários explicativos
// - Exemplos de uso
```

## 4. Casos de Teste
- Casos básicos (entrada normal)
- Casos extremos (vazio, um elemento, etc.)
- Casos de erro (entrada inválida)
- Performance com entradas grandes

## 5. Otimizações Possíveis
- Melhorias de performance
- Trade-offs de memória vs. tempo
- Variações do algoritmo para casos específicos

**Algoritmo solicitado**: ${input:algorithm:Descreva o algoritmo que deseja implementar}

**Linguagem**: ${input:language:python}
