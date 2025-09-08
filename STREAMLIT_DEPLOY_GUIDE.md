# 🚀 Guia de Deploy - Algoritmos Visualizador Integrado

## 📋 Pré-requisitos

Antes de fazer o deploy, certifique-se de que:

1. **Repositório no GitHub**: Seu código está em um repositório público no GitHub
2. **Chaves de API**: Você tem as chaves necessárias (Tavily, GitHub, etc.)
3. **Dependências**: O `requirements.txt` está atualizado com todas as dependências

## 🔧 Configuração do Deploy

### 1. Preparar Secrets
```bash
# Copie o arquivo de exemplo
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edite o arquivo com suas chaves reais
nano .streamlit/secrets.toml
```

### 2. Arquivos Necessários para Deploy
Certifique-se de que estes arquivos estão na raiz do repositório:
- ✅ `app_integrada.py` (arquivo principal)
- ✅ `requirements.txt` (dependências atualizadas)
- ✅ `packages.txt` (pacotes do sistema)
- ✅ `.streamlit/config.toml` (configurações do Streamlit)
- ✅ `.streamlit/secrets.toml` (chaves de API - NÃO commite este arquivo!)

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
├── requirements.txt              # 📦 Dependências Python
├── packages.txt                  # 🔧 Pacotes do sistema
├── .streamlit/
│   ├── config.toml              # ⚙️ Configurações Streamlit
│   └── secrets.toml             # 🔑 Chaves de API (não commite!)
├── modulo_1_fundamentos/        # 📚 Módulos educacionais
├── modulo_2_estruturas_dados/
├── modulo_3_programacao_dinamica/
├── modulo_4_entrevistas/
└── ... (outros arquivos)
```

## 🚨 Possíveis Problemas e Soluções

### Erro de Dependências
- Verifique se todas as dependências estão no `requirements.txt`
- Use versões específicas (ex: `streamlit==1.32.0`)

### Erro de Secrets
- Certifique-se de que as secrets estão configuradas no Streamlit Cloud
- Verifique se os nomes das secrets correspondem aos usados no código

### Erro de Pacotes do Sistema
- O `packages.txt` já inclui os pacotes necessários
- Se houver erros, adicione pacotes faltantes ao `packages.txt`

### Timeout no Deploy
- O deploy pode demorar alguns minutos na primeira vez
- Se der timeout, tente novamente

## 🎯 Verificação Pós-Deploy

Após o deploy, teste estas funcionalidades:
- ✅ Carregamento da página principal
- ✅ Navegação entre módulos
- ✅ Visualizações interativas
- ✅ Busca MCP (se configurada)
- ✅ Integração GitHub (se configurada)

## 📊 Monitoramento

- Acesse os logs do app no painel do Streamlit Cloud
- Monitore o uso de recursos e performance
- Configure alertas para erros

## 🔄 Atualizações

Para atualizar o app:
1. Faça as mudanças no código
2. Commit e push para o GitHub
3. O Streamlit Cloud fará o redeploy automático

---

**🎉 Parabéns!** Sua aplicação integrada está pronta para o mundo!

📧 **Suporte**: Em caso de problemas, verifique os logs do Streamlit Cloud ou abra uma issue no GitHub.
