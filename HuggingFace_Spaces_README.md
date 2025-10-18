# Algoritmos Visualizador - Hugging Face Spaces

🎯 **Plataforma educacional interativa** com visualização de algoritmos, exercícios práticos e integração PyTorch completa.

## 🚀 Deploy no Hugging Face Spaces

### Passo 1: Criar Space
1. Acesse [Hugging Face Spaces](https://huggingface.co/spaces)
2. Clique em "Create new Space"
3. Configure:
   - **Space name**: `algoritmos-visualizador`
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU basic (gratuito) ou GPU (upgrade)

### Passo 2: Upload dos Arquivos
```bash
# Clone seu repositório
git clone https://github.com/dronreef2/algoritmos-visualizador.git
cd algoritmos-visualizador

# Faça commit dos arquivos
git add .
git commit -m "Deploy Hugging Face Spaces"
git push origin main
```

### Passo 3: Configurar Space
No seu Space, configure:

**Settings > App File**: `app_integrada.py`  
**Settings > Requirements**: `requirements_huggingface_spaces.txt`  
**Settings > Python Version**: 3.10

## ⚡ Vantagens do Hugging Face Spaces

- **GPU Gratuito**: Até 16GB GPU persistent
- **Escalável**: Recursos aumentam conforme uso
- **Docker-based**: Deploy confiável e isolado
- **API Integrada**: Fácil integração com modelos HF
- **Comunidade**: Espaços descobribles e compartilháveis

## 🔧 Configurações Avançadas

### Secrets (opcional)
Configure secrets no Space settings:
- `TAVILY_API_KEY`: Para busca web
- `GITHUB_TOKEN`: Para integração GitHub

### Hardware Recommendations
- **CPU Basic**: Para demonstrações básicas (gratuito)
- **GPU T4 Small**: Para redes neurais leves
- **GPU A10G Large**: Para modelos avançados

### Custom Domain
- Configure domínio personalizado nas settings
- Suporte a HTTPS automático

## 🎮 Funcionalidades Suportadas

✅ **Todos os módulos**: Fundamentos, Estruturas, Programação Dinâmica, Entrevistas, Redes Neurais  
✅ **PyTorch GPU**: Treinamento e inferência acelerados  
✅ **Visualizações**: Matplotlib + Plotly com animações  
✅ **Exercícios**: Correção automática e feedback  
✅ **Integrações**: Tavily API, GitHub MCP  
✅ **Competições**: Rankings globais  

## 📊 Performance Esperada

| Hardware | Tempo de Inicialização | Memória | GPU Support |
|----------|----------------------|---------|-------------|
| CPU Basic | ~30s | 2GB | ❌ |
| T4 Small | ~45s | 8GB | ✅ |
| A10G Large | ~60s | 24GB | ✅ |

## 🔗 Links Úteis

- **Space Demo**: [https://huggingface.co/spaces/SEU_USERNAME/algoritmos-visualizador](https://huggingface.co/spaces)
- **Documentação**: [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- **Repositório**: [GitHub Source](https://github.com/dronreef2/algoritmos-visualizador)

---

**🎯 Pronto para deploy profissional com GPU!**