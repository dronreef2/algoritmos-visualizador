# 📁 Modelos de Redes Neurais

Esta pasta contém modelos de redes neurais para visualização com Netron.

## 🤖 Modelos Suportados

Netron suporta os seguintes formatos de modelos:

### 📋 Formatos Principais
- **ONNX** (`.onnx`) - Open Neural Network Exchange
- **TensorFlow Lite** (`.tflite`) - Modelos otimizados para mobile
- **Keras** (`.h5`, `.keras`) - Modelos salvos do Keras/TensorFlow
- **PyTorch** (`.pt`, `.pth`, `.pkl`) - Modelos do PyTorch
- **Core ML** (`.mlmodel`) - Modelos da Apple para iOS
- **Darknet** (`.cfg` + `.weights`) - Modelos YOLO e similares
- **TensorFlow** (`.pb`, `.meta`) - Modelos TensorFlow legados
- **Caffe** (`.caffemodel`, `.prototxt`) - Modelos Caffe

## 🔍 Buscar Modelos no GitHub

Use a funcionalidade integrada **"🔍 Buscar Modelos no GitHub"** no módulo 5 para:

1. **Buscar modelos** por nome (ex: "resnet", "yolov5", "mobilenet")
2. **Filtrar por formato** específico
3. **Baixar automaticamente** modelos encontrados
4. **Visualizar imediatamente** com Netron

### 📖 Como Usar

1. Abra a aplicação: `streamlit run app_integrada.py`
2. Navegue para **🧠 Módulo 5: Redes Neurais**
3. Selecione **🔍 Buscar Modelos no GitHub**
4. Digite um termo de busca (ex: "resnet50")
5. Selecione o formato desejado
6. Clique em **🔍 Buscar Modelos**
7. Baixe os modelos encontrados
8. Visualize com **🔍 Visualização de Modelos**

## 📊 Visualização com Netron

Após baixar um modelo, use a seção **"🔍 Visualização de Modelos"** para:

- **Upload** de modelos locais
- **Seleção** de modelos da pasta `models/`
- **Visualização interativa** da arquitetura
- **Análise** de camadas e conexões

## 🎯 Modelos de Exemplo

### Comandos para Download Manual

```bash
# ONNX Models
wget https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v2-7.onnx -O resnet50.onnx

# TensorFlow Lite
wget https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1?lite-format=tflite -O yamnet.tflite

# PyTorch
wget https://download.pytorch.org/models/resnet50-19c8e357.pth -O resnet50.pth
```

### Modelos Recomendados

- **SqueezeNet**: https://github.com/onnx/models/raw/main/vision/classification/squeezenet/model/squeezenet1.0-12.onnx
- **ResNet**: https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v2-7.onnx
- **YAMNet**: https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1?lite-format=tflite

## ⚠️ Notas Importantes

- **Modelos grandes**: Alguns modelos podem ter centenas de MB
- **GitHub API**: Respeite os limites de taxa da API
- **Licenças**: Verifique as licenças dos modelos antes de usar
- **Compatibilidade**: Nem todos os modelos são compatíveis com todas as versões do Netron

## 🆘 Troubleshooting

### Erro de Download
- Verifique sua conexão com a internet
- Alguns repositórios podem ter arquivos muito grandes
- Use VPN se necessário para acesso ao GitHub

### Netron Não Inicia
- Verifique se Netron está instalado: `pip install netron`
- Feche outras instâncias do Netron rodando
- Tente portas diferentes se 8080 estiver ocupada

### Modelos Não Aparecem
- Verifique se o arquivo foi baixado corretamente
- Alguns formatos podem precisar de arquivos auxiliares (.cfg + .weights)
- Teste com modelos menores primeiro