# 🧠 Módulo 5: Redes Neurais - Otimização Visual

## 📋 Visão Geral

Este módulo oferece uma experiência interativa e visual para entender como algoritmos de otimização funcionam em redes neurais. Explore curvas de erro em 3D, trajetórias de otimização e exercícios práticos com código executável.

## 🎯 Funcionalidades Principais

### 📊 Visualização Interativa da Curva de Erro
- **Gráficos 3D** da superfície de perda com Plotly
- **Trajetória em tempo real** mostrando como os parâmetros evoluem
- **Controles interativos**: learning rate, momentum, número de épocas
- **Comparação de otimizadores**: GD, SGD, Adam

### 🎮 Exercícios Interativos
- **Sandbox de código Python** com execução segura
- **Validação automática** de algoritmos implementados
- **Feedback contextual** com dicas e correções
- **Sistema de pontuação** e progresso

### 🔗 Integração com GitHub
- **Busca de exemplos reais** de redes neurais
- **Documentação técnica** via API GitHub
- **Código de referência** de repositórios populares

## 🚀 Como Usar

### 1. Visualização Básica
```python
from modulo_5_redes_neurais import otimizadores, visualizacoes

# Criar otimizador
otimizador = otimizadores.Adam(learning_rate=0.01)

# Executar otimização
historico = otimizadores.otimizar_rede_simples(X, y, otimizador, epocas=100)

# Visualizar
fig = visualizacoes.plot_curva_erro_2d(historico, X, y)
fig.show()
```

### 2. Exercícios Práticos
```python
from modulo_5_redes_neurais.exercicios import ExercicioGradienteDescendente

# Criar exercício
exercicio = ExercicioGradienteDescendente()

# Na interface Streamlit
exercicio.criar_interface_exercicio()
```

### 3. Busca no GitHub
```python
from gitmcp_integration import GitMCPIntegration

git_client = GitMCPIntegration()
resultados = git_client.buscar_documentacao_algoritmo("neural network optimization")
```

## 📚 Algoritmos Implementados

### Otimizadores
- **Gradiente Descendente**: Atualização básica de parâmetros
- **SGD com Momentum**: Aceleração da convergência
- **Adam**: Adaptativo com momento e variância

### Funções de Perda
- **MSE (Mean Squared Error)**: Para regressão
- **Extensível**: Fácil adicionar outras perdas

## 🎨 Interface Streamlit

O módulo se integra completamente ao `app_integrada.py` como **Módulo 5: Redes Neurais** na navegação principal.

### Abas Disponíveis
1. **📊 Visualização Interativa** - Explore otimizadores em tempo real
2. **🎮 Exercícios Práticos** - Aprenda implementando algoritmos
3. **📚 Exemplos do GitHub** - Veja código real de projetos
4. **⚙️ Configurações** - Personalize a experiência

## 🔧 Dependências

```txt
numpy>=1.24.0
matplotlib>=3.7.0
plotly>=5.15.0
streamlit>=1.32.0
```

## 📖 Exemplos de Uso

### Comparação de Otimizadores
```python
import numpy as np
from modulo_5_redes_neurais import otimizadores, visualizacoes

# Dados de exemplo
X = np.random.randn(100, 1)
y = 2 * X.flatten() + 1 + 0.1 * np.random.randn(100)

# Comparar otimizadores
otimizadores_teste = [
    otimizadores.GradienteDescendente(learning_rate=0.1),
    otimizadores.SGD(learning_rate=0.1, momentum=0.9),
    otimizadores.Adam(learning_rate=0.01)
]

for otimizador in otimizadores_teste:
    historico = otimizadores.otimizar_rede_simples(X, y, otimizador, epocas=50)
    print(f"{otimizador.__class__.__name__}: Perda final = {historico['loss'][-1]:.4f}")
```

## 🎯 Objetivos de Aprendizado

Após completar este módulo, você será capaz de:

1. **Entender visualmente** como otimizadores funcionam
2. **Comparar algoritmos** de otimização diferentes
3. **Implementar** gradiente descendente do zero
4. **Diagnosticar** problemas de convergência
5. **Aplicar** conceitos em problemas reais

## 🔄 Próximos Passos

- [ ] Adicionar mais otimizadores (RMSProp, AdaGrad)
- [ ] Implementar redes neurais multicamadas
- [ ] Adicionar visualização de overfitting/underfitting
- [ ] Integrar com datasets reais (MNIST, CIFAR)
- [ ] Sistema de exercícios mais avançado

## 🤝 Contribuição

Para contribuir com este módulo:

1. Adicione novos otimizadores em `otimizadores.py`
2. Crie exercícios em `exercicios.py`
3. Implemente visualizações em `visualizacoes.py`
4. Teste a integração no `app_integrada.py`

## 📄 Licença

Este módulo faz parte do projeto [Algoritmos Visualizador](https://github.com/dronreef2/algoritmos-visualizador) e segue a mesma licença.