# 🎯 Algoritmos Visualizador - Multi-Plataforma

**Sistema educacional completo** com visualização de algoritmos, exercícios práticos e integração PyTorch para múltiplas plataformas cloud.

## 🌐 Plataformas Suportadas

### 🖥️ **Desenvolvimento Local**
```bash
# Inicialização automática
python iniciar.py

# Ou diretamente
streamlit run app_integrada.py
```

### 🌐 **Google Colab** (GPU/TPU Gratuito)
```bash
# Forçar modo Colab
python iniciar.py --colab

# Ou usar launcher diretamente
python multi_platform_launcher.py
```

**Recursos Colab:**
- ✅ GPU/TPU gratuito ilimitado
- ✅ Compartilhamento instantâneo
- ✅ 25GB RAM, armazenamento ilimitado
- ✅ Integração GitHub direta

### 🤗 **Hugging Face Spaces** (Deploy Profissional)
```bash
# Forçar modo Spaces
python iniciar.py --spaces
```

**Recursos Spaces:**
- ✅ GPU persistente (T4/A10G)
- ✅ Escalável automaticamente
- ✅ API integrada
- ✅ Deploy profissional

### ☁️ **Streamlit Cloud** (CPU Otimizado)
- Deploy direto pelo GitHub
- CPU-only, 1GB RAM
- Ideal para demonstrações básicas

## 🚀 Inicialização Inteligente

O sistema detecta automaticamente a plataforma e otimiza:

```python
# Auto-detecção
python iniciar.py          # Detecta automaticamente
python iniciar.py --colab  # Força Google Colab
python iniciar.py --spaces # Força Hugging Face Spaces
python iniciar.py --local  # Força desenvolvimento local
```

## 🎯 Funcionalidades por Plataforma

| Funcionalidade | Local | Colab | Spaces | Streamlit Cloud |
|----------------|-------|-------|--------|-----------------|
| 📊 Visualizações | ✅ | ✅ | ✅ | ✅ |
| 🧠 Redes Neurais | ✅ | ✅ | ✅ | ⚠️ (CPU) |
| 🎨 Arte Generativa | ✅ | ✅ | ✅ | ❌ |
| 🏆 Competições | ✅ | ✅ | ✅ | ⚠️ (Limitado) |
| 🔍 Busca Web | ✅ | ✅ | ✅ | ✅ |
| 📝 Exercícios | ✅ | ✅ | ✅ | ✅ |

## 📦 Dependências Automáticas

O launcher instala automaticamente as dependências corretas:

- **Local/Spaces**: PyTorch com CUDA
- **Colab**: PyTorch CUDA otimizado
- **Streamlit Cloud**: PyTorch CPU-only

## 🎮 Interface Integrada

Acesse **"🚀 Deploy Multi-Plataforma"** no menu lateral para:

- 📊 **Status da Plataforma**: Recursos disponíveis
- 🌐 **Opções de Deploy**: Guias para cada plataforma
- 🔄 **Migração**: Como migrar entre plataformas
- 🧪 **Compatibilidade**: Verificação de recursos

## 🔧 Configuração Avançada

### Secrets (APIs)
```bash
# Tavily API Key
export TAVILY_API_KEY="your_key_here"

# GitHub Token (opcional)
export GITHUB_TOKEN="your_token_here"
```

### Desenvolvimento
```bash
# Verificar compatibilidade
python check_colab_spaces_compatibility.py

# Limpar cache
rm -rf __pycache__ .streamlit/cache
```

## 📊 Performance Esperada

| Plataforma | Inicialização | Memória | GPU | Timeout |
|------------|---------------|---------|-----|---------|
| Local | Instantâneo | Sistema | Sim/Não | Ilimitado |
| Colab | 30-60s | 25GB | T4/A100 | Ilimitado |
| Spaces | 45-90s | 16GB | T4/A10G | Ilimitado |
| Streamlit Cloud | 30s | 1GB | Não | 10-15min |

## 🎯 Recomendações

- **🚀 Comece com Colab**: Para testar funcionalidades avançadas
- **💼 Produção**: Use Hugging Face Spaces
- **📱 Demonstrações**: Streamlit Cloud para simplicidade
- **🔧 Desenvolvimento**: Local com GPU

## 🔗 Links Úteis

- 📚 [Documentação Completa](README.md)
- 🌐 [Google Colab](https://colab.research.google.com)
- 🤗 [Hugging Face Spaces](https://huggingface.co/spaces)
- ☁️ [Streamlit Cloud](https://share.streamlit.io)

---

**🎉 Pronto para usar em qualquer plataforma!**