# 🚀 Guia de Deploy - Algoritmos Visualizador

## 📋 Pré-requisitos para Deploy

### ✅ Arquivos de Configuração Criados
- `.streamlit/config.toml` - Configurações do Streamlit
- `packages.txt` - Dependências do sistema
- `requirements.txt` - Dependências Python

### ✅ Estrutura Verificada
- ✅ `streamlit_apps/main_app.py` - Aplicação principal
- ✅ Todos os módulos integrados e testados
- ✅ Imports funcionando corretamente

## 🌐 Deploy no Streamlit Sharing

### Passo 1: Acesse o Streamlit Sharing
1. Vá para [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub

### Passo 2: Conecte o Repositório
1. Clique em "New app"
2. Selecione o repositório `dronreef2/algoritmos-visualizador`
3. Configure:
   - **Main file path**: `streamlit_apps/main_app.py`
   - **Python version**: `3.11`
   - **Branch**: `main`

### Passo 3: Deploy Automático
Após conectar, todo push para a branch `main` fará deploy automático!

## 🔧 Configurações Técnicas

### Requirements
```
streamlit>=1.32.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
networkx>=3.1
scipy>=1.10.0
plotly>=5.15.0
seaborn>=0.12.0
```

### Packages do Sistema
```
libglib2.0-0
libsm6
libxext6
libxrender-dev
libgomp1
libgthread-2.0-0
libxml2-dev
libxslt-dev
curl
git
```

## 🎯 Funcionalidades Disponíveis

### 📚 Módulo 1: Fundamentos
- 🔍 Busca Binária
- 👥 Dois Ponteiros
- 🪟 Janela Deslizante
- 🔄 Backtracking
- 🌐 BFS
- 🚨 Detector de Fraudes
- 👥 Rede Social

### 🏗️ Módulo 2: Estruturas de Dados
- 🔺 Heap (Min/Max)
- 🌳 Trie
- 🤝 Union-Find
- 📊 Segment Tree
- 💾 LRU Cache
- 🌐 Graph

### 🎯 Módulo 3: Programação Dinâmica
- 🔢 Fibonacci (3 passos)
- 🎒 Knapsack
- 📝 LCS
- 🪙 Coin Change

### 💼 Módulo 4: Entrevistas
- 🎯 Simulação de Entrevista
- 📚 Biblioteca de Problemas
- 📊 Análise de Código
- ⏱️ Prática com Tempo

## 🚀 Status do Deploy

- ✅ **Aplicação**: Testada e funcionando
- ✅ **Módulos**: Todos integrados
- ✅ **Imports**: Corrigidos
- ✅ **Configurações**: Criadas
- 🔄 **Próximo**: Conectar no Streamlit Sharing

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs do GitHub Actions
2. Teste localmente: `streamlit run streamlit_apps/main_app.py`
3. Verifique se todos os requirements estão instalados

---
**🎉 Pronto para deploy automático!**
