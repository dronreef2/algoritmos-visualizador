# 🚀 CI/CD Pipeline - Algoritmos Visualizador

## 📋 Visão Geral

Este projeto utiliza GitHub Actions para Continuous Integration (CI) e deploy automático no Streamlit Community Cloud.

## 🔧 Pipeline de CI

O workflow `.github/workflows/python-ci.yml` executa:

### 1. **Matriz de Testes**
- Python 3.9, 3.10, 3.11
- Ubuntu Latest

### 2. **Qualidade de Código**
- **Flake8**: Linting e detecção de erros
- **Black**: Formatação de código
- **Pytest**: Testes unitários

### 3. **Validação de Funcionalidades**
- Teste de imports dos módulos
- Validação do Módulo 1 (aplicações reais)
- Verificação da aplicação Streamlit
- Validação de todos os requirements

## 📝 Comandos Locais

### Executar Linting
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Executar Formatação
```bash
black --check --diff .
```

### Executar Testes
```bash
python -m pytest test_projeto.py -v
```

### Testar Módulo 1
```bash
cd modulo_1_fundamentos
python -c "
from aplicacoes_reais import *
from casos_uso_praticos import *
print('✅ Módulo 1 funcionando!')
"
```

## 🚀 Deploy Automático

### Streamlit Community Cloud
- **URL**: https://algoritmos-visualizador.streamlit.app/
- **Arquivo Principal**: `streamlit_app_mcp.py`
- **Deploy**: Automático a cada push na branch `main`

### Configuração do Deploy
1. Conectar repositório GitHub ao Streamlit Cloud
2. Configurar branch: `main`
3. Arquivo principal: `streamlit_app_mcp.py`
4. Requirements: `requirements_mcp.txt`

## 📊 Status dos Testes

### ✅ Testes Implementados
- **test_imports**: Verifica importações dos módulos
- **test_sistema_busca_logs**: Testa sistema de busca em logs
- **test_detector_fraudes**: Testa detector de fraudes
- **test_rede_social**: Testa rede social BFS
- **test_template_dois_ponteiros**: Testa template de dois ponteiros
- **test_template_busca_binaria**: Testa template de busca binária

### 🎯 Cobertura de Testes
- **Módulo 1**: 100% das aplicações principais
- **Templates**: 100% dos templates essenciais
- **Importações**: Todos os módulos principais

## 🔧 Configuração de Desenvolvimento

### Arquivos de Configuração
- `.flake8`: Configuração do linter
- `pyproject.toml`: Configuração do Black
- `.gitignore`: Arquivos ignorados pelo Git

### Dependências
- `requirements_mcp.txt`: Dependências principais
- `requirements_simple.txt`: Dependências mínimas
- `requirements_visualizacao.txt`: Dependências de visualização

## 📈 Monitoramento

### GitHub Actions
- Executa a cada push/PR na branch `main`
- Falha se algum teste não passar
- Relatório completo de qualidade de código

### Streamlit Cloud
- Deploy automático após CI passar
- Logs disponíveis no painel do Streamlit
- Monitoramento de uso e performance

## 🎯 Padrões de Qualidade

### Code Style
- **Linha máxima**: 127 caracteres
- **Formatação**: Black
- **Imports**: Ordenados e limpos
- **Docstrings**: Obrigatórias para funções públicas

### Testes
- **Cobertura mínima**: 80%
- **Testes unitários**: Para todas as funcionalidades principais
- **Validação de integração**: Módulos funcionando juntos

## 🚀 Como Contribuir

1. **Fork** do repositório
2. **Criar branch** para feature/fix
3. **Implementar** mudanças
4. **Executar testes** localmente
5. **Commit** com mensagens descritivas
6. **Push** para sua branch
7. **Criar PR** para branch main

### Checklist antes do PR
- [ ] Testes passam localmente
- [ ] Código formatado com Black
- [ ] Sem erros de linting
- [ ] Documentação atualizada
- [ ] Novos testes para novas funcionalidades

---

## 📞 Suporte

Para problemas com CI/CD:
1. Verificar logs do GitHub Actions
2. Executar testes localmente
3. Verificar configuração do Streamlit Cloud
4. Consultar documentação oficial

**Status:** ✅ **Pipeline funcionando perfeitamente**
**Deploy:** ✅ **Aplicação online e funcional**
**Última atualização:** 18 de julho de 2025
**URL:** https://algoritmos-visualizador.streamlit.app/
