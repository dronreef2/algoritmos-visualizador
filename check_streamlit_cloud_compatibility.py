#!/usr/bin/env python3
"""
🧪 Verificação de Compatibilidade - Streamlit Cloud
===============================================

Script para verificar se a aplicação está pronta para deploy no Streamlit Cloud.
"""

import sys
import os
from pathlib import Path

def main():
    """Verificação básica de compatibilidade"""
    print("🧪 VERIFICAÇÃO DE COMPATIBILIDADE - STREAMLIT CLOUD")
    print("="*60)

    # Verifica arquivos críticos
    critical_files = [
        'app_integrada.py',
        'requirements_streamlit_cloud.txt',
        '.streamlit/config.toml'
    ]

    print("📁 Verificando arquivos críticos...")
    all_files_ok = True

    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}: OK")
        else:
            print(f"   ❌ {file_path}: Não encontrado")
            all_files_ok = False

    # Verifica dependências básicas
    print("\n📦 Verificando dependências básicas...")
    dependencies_ok = True

    try:
        import streamlit
        print(f"   ✅ streamlit: {streamlit.__version__}")
    except ImportError:
        print("   ❌ streamlit: Não encontrado")
        dependencies_ok = False

    try:
        import torch
        print(f"   ✅ torch: {torch.__version__}")
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print("   ✅ CUDA: Disponível")
        else:
            print("   ⚠️  CUDA: Não disponível (CPU-only)")
    except ImportError:
        print("   ❌ torch: Não encontrado")
        dependencies_ok = False

    # Status final
    print("\n" + "="*60)
    if all_files_ok and dependencies_ok:
        print("🎉 STATUS: ✅ PRONTO PARA DEPLOY NO STREAMLIT CLOUD")
        print("\n🚀 Para fazer deploy:")
        print("   1. Commit dos arquivos no GitHub")
        print("   2. Acesse: https://share.streamlit.io")
        print("   3. Configure:")
        print("      - Main file: app_integrada.py")
        print("      - Requirements: requirements_streamlit_cloud.txt")
        return True
    else:
        print("⚠️  STATUS: ❌ PROBLEMAS DETECTADOS")
        print("   Verifique os arquivos e dependências acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

import sys
import os
import platform
import psutil
import time
from pathlib import Path

def check_system_resources():
    """Verifica recursos do sistema"""
    print("🔍 Verificando recursos do sistema...")

    # CPU
    cpu_count = os.cpu_count()
    print(f"   CPU: {cpu_count} cores")

    # Memória
    memory = psutil.virtual_memory()
    memory_gb = memory.total / (1024**3)
    print(f"   Memória: {memory_gb:.1f} GB")

    # Disco
    disk = psutil.disk_usage('/')
    disk_gb = disk.total / (1024**3)
    print(f"   Disco: {disk_gb:.1f} GB")
    return {
        'cpu_count': cpu_count,
        'memory_gb': memory_gb,
        'disk_gb': disk_gb
    }

def check_dependencies():
    """Verifica dependências críticas"""
    print("\n📦 Verificando dependências...")

    dependencies = [
        'streamlit',
        'torch',
        'numpy',
        'pandas',
        'plotly',
        'matplotlib',
        'PIL'
    ]

    results = {}
    for dep in dependencies:
        try:
            if dep == 'PIL':
                import PIL
                version = PIL.__version__
            else:
                module = __import__(dep)
                version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {dep}: {version}")
            results[dep] = True
        except ImportError as e:
            print(f"   ❌ {dep}: Não encontrado - {e}")
            results[dep] = False

    return results

def check_pytorch_setup():
    """Verifica configuração do PyTorch"""
    print("\n🧠 Verificando PyTorch...")

    try:
        import torch
        print(f"   ✅ PyTorch: {torch.__version__}")

        # Verifica CUDA
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print(f"   ✅ CUDA: Disponível ({torch.cuda.get_device_name()})")
        else:
            print("   ⚠️  CUDA: Não disponível (usando CPU)")

        # Testa tensor básico
        x = torch.randn(10, 10)
        y = x @ x.t()
        print("   ✅ Operações básicas: OK")

        return {
            'torch_version': torch.__version__,
            'cuda_available': cuda_available,
            'basic_ops': True
        }

    except Exception as e:
        print(f"   ❌ PyTorch: Erro - {e}")
        return None

def check_module_imports():
    """Verifica importação dos módulos principais"""
    print("\n📚 Verificando módulos da aplicação...")

    modules_to_test = [
        'app_integrada',
        'modulos_integrados',
        'cache_inteligente_moderno',
        'aprendizado_contextual_ui',
        'exercicios_praticos_ui',
        'mcp_tavily_integration'
    ]

    results = {}
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module}: OK")
            results[module] = True
        except ImportError as e:
            print(f"   ❌ {module}: Erro - {e}")
            results[module] = False

    # Testa módulos avançados (podem falhar sem GPU)
    advanced_modules = [
        'modulo_5_redes_neurais.neural_evolution',
        'modulo_5_redes_neurais.neural_sonification',
        'modulo_5_redes_neurais.neural_generative_art',
        'modulo_5_redes_neurais.neural_global_competitions'
    ]

    print("\n🚀 Verificando módulos avançados (PyTorch)...")
    for module in advanced_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}: OK")
            results[module] = True
        except Exception as e:
            print(f"   ⚠️  {module}: {e}")
            results[module] = False

    return results

def check_file_structure():
    """Verifica estrutura de arquivos crítica"""
    print("\n📁 Verificando estrutura de arquivos...")

    critical_files = [
        'app_integrada.py',
        'requirements_streamlit_cloud.txt',
        '.streamlit/config.toml',
        'modulo_5_redes_neurais/',
        'cache_inteligente_moderno.py'
    ]

    results = {}
    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            if path.is_dir():
                file_count = len(list(path.glob('*')))
                print(f"   ✅ {file_path}: {file_count} arquivos")
            else:
                size_kb = path.stat().st_size / 1024
                print(f"   ✅ {file_path}: {size_kb:.1f} KB")
                results[file_path] = True
        else:
            print(f"   ❌ {file_path}: Não encontrado")
            results[file_path] = False

    return results

def performance_test():
    """Teste básico de performance"""
    print("\n⚡ Teste de performance...")

    try:
        import torch
        import numpy as np

        # Teste CPU
        start_time = time.time()
        x = torch.randn(100, 100)
        for _ in range(100):
            y = torch.matmul(x, x)
        cpu_time = time.time() - start_time
        print(f"   ✅ CPU time: {cpu_time:.3f}s")
        # Teste NumPy
        start_time = time.time()
        x_np = np.random.randn(100, 100)
        for _ in range(100):
            y_np = np.dot(x_np, x_np)
        numpy_time = time.time() - start_time
        print(f"   ✅ NumPy time: {numpy_time:.3f}s")
        return {
            'cpu_time': cpu_time,
            'numpy_time': numpy_time,
            'performance_ok': cpu_time < 5.0  # Menos de 5s é aceitável
        }

    except Exception as e:
        print(f"   ❌ Performance test: {e}")
        return None

def generate_report(results):
    """Gera relatório final"""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE COMPATIBILIDADE - STREAMLIT CLOUD")
    print("="*60)

    # Status geral
    all_critical_ok = all([
        results['dependencies'].get('streamlit', False),
        results['dependencies'].get('torch', False),
        results['files'].get('app_integrada.py', False),
        results['files'].get('requirements_streamlit_cloud.txt', False)
    ])

    if all_critical_ok:
        print("🎉 STATUS: ✅ PRONTO PARA DEPLOY")
    else:
        print("⚠️  STATUS: ❌ PROBLEMAS CRÍTICOS DETECTADOS")

    # Resumo por categoria
    print("\n📋 RESUMO POR CATEGORIA:")
    print(f"   🔍 Sistema: {len([r for r in results['system'].values() if r])}/{len(results['system'])} OK")
    print(f"   📦 Dependências: {len([r for r in results['dependencies'].values() if r])}/{len(results['dependencies'])} OK")
    print(f"   🧠 PyTorch: {'✅' if results['pytorch'] else '❌'}")
    print(f"   📚 Módulos: {len([r for r in results['modules'].values() if r])}/{len(results['modules'])} OK")
    print(f"   📁 Arquivos: {len([r for r in results['files'].values() if r])}/{len(results['files'])} OK")
    print(f"   ⚡ Performance: {'✅' if results['performance'] and results['performance']['performance_ok'] else '❌'}")

    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")
    if not results['pytorch'] or not results['pytorch'].get('cuda_available', False):
        print("   ⚠️  PyTorch sem GPU - funcionalidades avançadas serão limitadas")
        print("   💡 Considere arquitetura híbrida (Streamlit + AWS) para GPU")

    if results['performance'] and results['performance']['cpu_time'] > 2.0:
        print("   ⚠️  Performance CPU baixa - otimize operações pesadas")
        print("   💡 Use @st.cache_data e reduza complexidade de cálculos")

    if not all(results['files'].values()):
        print("   ❌ Arquivos críticos faltando - verifique deploy")
        print("   💡 Certifique-se que todos os arquivos estão no repositório")

    print("\n🚀 PARA DEPLOY:")
    print("   1. Faça commit dos arquivos no GitHub")
    print("   2. Acesse: https://share.streamlit.io")
    print("   3. Conecte o repositório e configure:")
    print("      - Main file: app_integrada.py")
    print("      - Requirements: requirements_streamlit_cloud.txt")
    print("   4. Deploy automático!")

    print("\n" + "="*60)

def main():
    """Função principal"""
    print("🧪 VERIFICAÇÃO DE COMPATIBILIDADE - STREAMLIT CLOUD")
    print("="*60)

    results = {}

    # Executa verificações
    results['system'] = check_system_resources()
    results['dependencies'] = check_dependencies()
    results['pytorch'] = check_pytorch_setup()
    results['modules'] = check_module_imports()
    results['files'] = check_file_structure()
    results['performance'] = performance_test()

    # Gera relatório
    generate_report(results)

    # Exit code baseado no status
    critical_ok = all([
        results['dependencies'].get('streamlit', False),
        results['dependencies'].get('torch', False),
        results['files'].get('app_integrada.py', False)
    ])

    sys.exit(0 if critical_ok else 1)

if __name__ == "__main__":
    main()
