# Guia de Uso - Personalização do GitHub Copilot

## Como Usar as Instruções Customizadas

### 1. Configuração Inicial
As instruções já estão configuradas automaticamente. Certifique-se de que:
- O arquivo `.vscode/settings.json` está presente
- A configuração `github.copilot.chat.codeGeneration.useInstructionFiles` está como `true`

### 2. Usando Prompts Personalizados

#### No Chat do Copilot:
```
/generate-algorithm: algoritmo=quick_sort linguagem=python
/optimize-algorithm
/code-review
```

#### Via Command Palette (Ctrl+Shift+P):
- `Chat: Run Prompt` → Selecione o prompt desejado

### 3. Instruções Automáticas
As instruções em `.github/copilot-instructions.md` são aplicadas automaticamente a todas as solicitações de código.

### 4. Instruções Específicas
- `algorithm.instructions.md`: Aplicado automaticamente a arquivos de código
- `review.instructions.md`: Usado para revisões de código

## Exemplos Práticos

### Gerar um Novo Algoritmo
1. Abra o chat do Copilot
2. Digite: `/generate-algorithm`
3. Especifique o algoritmo desejado quando solicitado

### Otimizar Código Existente
1. Selecione o código que deseja otimizar
2. Use `/optimize-algorithm` no chat
3. O Copilot analisará e sugerirá melhorias

### Revisar Código
1. Selecione o código para revisão
2. Use `/code-review` no chat
3. Receba uma análise detalhada seguindo as diretrizes do projeto

## Personalizando Ainda Mais

### Adicionar Novas Instruções
1. Crie um novo arquivo `.instructions.md` em `.github/instructions/`
2. Configure o `applyTo` para especificar quando aplicar
3. Escreva as instruções em linguagem natural

### Criar Novos Prompts
1. Crie um arquivo `.prompt.md` em `.github/prompts/`
2. Configure o modo (ask, edit, agent)
3. Defina o conteúdo do prompt com variáveis se necessário

### Modificar Configurações
Edite `.vscode/settings.json` para:
- Adicionar instruções para commit messages
- Configurar instruções para pull requests
- Personalizar outras funcionalidades do Copilot

## Dicas
- Mantenha instruções simples e específicas
- Use exemplos para clarificar expectativas
- Teste prompts regularmente
- Compartilhe instruções com a equipe via controle de versão
