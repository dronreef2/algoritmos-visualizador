---
description: "Prompt para realizar revisão detalhada de código de algoritmos"
mode: "ask"
tools: ["codebase", "analysis"]
---

# Revisão de Código - Algoritmos

Realize uma revisão detalhada do código selecionado considerando:

## 1. Análise de Corretude
- [ ] O algoritmo resolve o problema corretamente?
- [ ] Todos os casos extremos são tratados?
- [ ] Há potencial para bugs ou erros lógicos?
- [ ] Validação de entrada é adequada?

## 2. Análise de Performance
- [ ] Complexidade temporal é otimizada?
- [ ] Uso de memória é eficiente?
- [ ] Estruturas de dados são apropriadas?
- [ ] Há loops desnecessários ou redundâncias?

## 3. Qualidade do Código
- [ ] Legibilidade e clareza
- [ ] Nomenclatura descritiva
- [ ] Comentários úteis e precisos
- [ ] Estrutura lógica e organizada

## 4. Manutenibilidade
- [ ] Segue padrões do projeto
- [ ] Funções têm responsabilidade única
- [ ] Código é testável
- [ ] Documentação é adequada

## Formato da Resposta
1. **Resumo**: Avaliação geral (Aprovado/Aprovado com ressalvas/Rejeitar)
2. **Pontos Positivos**: O que está bem implementado
3. **Issues Críticos**: Problemas que impedem aprovação
4. **Sugestões**: Melhorias recomendadas
5. **Exemplos**: Código melhorado quando necessário

Analisar: ${selection}
