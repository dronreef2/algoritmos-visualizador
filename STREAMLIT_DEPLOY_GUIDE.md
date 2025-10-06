# 🚀 Guia de Deploy - Algoritmos Visualizador Integrado

## 📋 Pré-requisitos

Antes de fazer o deploy, certifique-se de que:

1. **Repositório no GitHub**: Seu código está em um repositório público no GitHub
2. **Chaves de API**: Você tem as chaves necessárias (Tavily, GitHub, etc.)
3. **Dependências**: O `requirements.txt` está atualizado com todas as dependências, incluindo PyTorch
4. **Template de Secrets**: Use o arquivo `.streamlit/secrets.toml.template` como base

## 🔧 Configuração do Deploy

### 1. Preparar Secrets
```bash
# Copie o arquivo de template
cp .streamlit/secrets.toml.template .streamlit/secrets.toml

# Edite o arquivo com suas chaves reais
nano .streamlit/secrets.toml
```

### 2. Arquivos Necessários para Deploy
Certifique-se de que estes arquivos estão na raiz do repositório:
- ✅ `app_integrada.py` (arquivo principal)
- ✅ `requirements.txt` (dependências atualizadas com PyTorch)
- ✅ `packages.txt` (pacotes do sistema)
- ✅ `.streamlit/config.toml` (configurações do Streamlit)
- ✅ `.streamlit/secrets.toml` (chaves de API - NÃO commite este arquivo!)
- ✅ `.streamlit/secrets.toml.template` (template para configuração)
- ✅ `.github/workflows/monitoramento.yml` (workflow de monitoramento)

### 3. Deploy no Streamlit Cloud

#### Opção A: Deploy Direto
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte sua conta do GitHub
3. Selecione o repositório `algoritmos-visualizador`
4. Configure:
   - **Main file path**: `app_integrada.py`
   - **Python version**: `3.9` ou superior
   - **Additional requirements**: Deixe vazio (usa requirements.txt)

#### Opção B: Deploy via GitHub Actions (Recomendado)
1. No Streamlit Cloud, configure o deploy automático
2. Toda vez que você fizer push para a branch main, o app será atualizado
3. O workflow de monitoramento será executado diariamente

## 🔐 Configuração de Secrets no Streamlit Cloud

No painel do Streamlit Cloud:

1. Vá para **Settings** > **Secrets**
2. Adicione as seguintes secrets:
```
TAVILY_API_KEY = your_actual_tavily_api_key
GITHUB_TOKEN = your_actual_github_token
OPENAI_API_KEY = your_openai_api_key  # opcional
ANTHROPIC_API_KEY = your_anthropic_api_key  # opcional
```

## 📁 Estrutura de Arquivos para Deploy

```
/workspaces/algoritmos-visualizador/
├── app_integrada.py              # 🏠 Arquivo principal
├── requirements.txt              # 📦 Dependências Python (inclui PyTorch)
├── packages.txt                  # 🔧 Pacotes do sistema
├── .streamlit/
│   ├── config.toml              # ⚙️ Configurações Streamlit
│   ├── secrets.toml             # 🔑 Chaves de API (não commite!)
│   └── secrets.toml.template    # 📝 Template para configuração de secrets
├── .github/
│   └── workflows/
│       └── monitoramento.yml    # 📊 Workflow de monitoramento automatizado
├── modulo_1_fundamentos/        # 📚 Módulos educacionais
├── modulo_2_estruturas_dados/
├── modulo_3_programacao_dinamica/
├── modulo_4_entrevistas/
└── modulo_5_redes_neurais/      # 🧠 Novo módulo com PyTorch
    ├── pytorch_utils.py         # 🔧 Utilitários PyTorch
    └── interface.py             # 🎨 Interface Streamlit para redes neurais
```

## 🚨 Possíveis Problemas e Soluções

### Erro de Dependências PyTorch
- Verifique se o `requirements.txt` inclui PyTorch e suas dependências
- Para GPU: `torch>=2.0.0` com `torchvision` e `torchaudio`
- Para CPU: `torch>=2.0.0+cpu` (mais leve para deploy)

### Erro de Dependências
- Verifique se todas as dependências estão no `requirements.txt`
- Use versões específicas (ex: `streamlit==1.32.0`)

### Erro de Secrets
- Certifique-se de que as secrets estão configuradas no Streamlit Cloud
- Verifique se os nomes das secrets correspondem aos usados no código
- Use o template `.streamlit/secrets.toml.template` como referência

### Erro de Pacotes do Sistema
- O `packages.txt` já inclui os pacotes necessários
- Se houver erros, adicione pacotes faltantes ao `packages.txt`

### Timeout no Deploy
- O deploy pode demorar alguns minutos na primeira vez (especialmente com PyTorch)
- Se der timeout, tente novamente

### Problemas com GPU/CUDA
- Streamlit Cloud roda em CPU por padrão
- PyTorch será automaticamente configurado para CPU
- Verifique se suas implementações têm fallbacks para CPU

## 🎯 Verificação Pós-Deploy

Após o deploy, teste estas funcionalidades:
- ✅ Carregamento da página principal
- ✅ Navegação entre módulos
- ✅ Visualizações interativas
- ✅ Módulo 5: Redes Neurais com PyTorch
  - Demonstrações de tensores
  - Treinamento de rede neural simples
  - Visualização de dados
- ✅ Busca MCP (se configurada)
- ✅ Integração GitHub (se configurada)
- ✅ Sistema de cache inteligente
- ✅ Monitoramento automatizado (workflow GitHub Actions)

## 📊 Monitoramento

- **Automático**: O workflow `.github/workflows/monitoramento.yml` executa diariamente
- **Manual**: Acesse os logs do app no painel do Streamlit Cloud
- **Métricas**: Monitore o uso de recursos e performance
- **Alertas**: Configure alertas para erros no GitHub Actions

### Verificar Status do Monitoramento
```bash
# Verificar se o workflow está ativo
# Vá para a aba "Actions" no GitHub e veja o status do workflow "monitoramento"
```

## 🔄 Atualizações

Para atualizar o app:
1. Faça as mudanças no código
2. Commit e push para o GitHub
3. O Streamlit Cloud fará o redeploy automático
4. O workflow de monitoramento será executado automaticamente

---

**🎉 Parabéns!** Sua aplicação integrada com PyTorch está pronta para o mundo!

📧 **Suporte**: Em caso de problemas, verifique os logs do Streamlit Cloud ou abra uma issue no GitHub.
