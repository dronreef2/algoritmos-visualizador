# Algoritmos Visualizador - Google Colab Setup
# ============================================
# Notebook Colab para demonstrações interativas
# Suporte completo a GPU/TPU, recursos ilimitados

# Instalar dependências
!pip install -q streamlit>=1.32.0
!pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
!pip install -q numpy pandas matplotlib plotly seaborn scipy
!pip install -q requests pillow tavily-python psutil

# Para funcionalidades avançadas (opcional)
# !pip install -q jupyter ipywidgets
# !pip install -q gitpython pygithub

# Verificar instalação
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA disponível: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

import streamlit
print(f"Streamlit: {streamlit.__version__}")

print("✅ Todas as dependências instaladas com sucesso!")