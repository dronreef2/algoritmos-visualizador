#!/usr/bin/env python3
"""
Script de Monitoramento - Algoritmos Visualizador
Verifica status do projeto e dependências
"""

import requests
import subprocess
import sys
import os
from datetime import datetime
import json

def check_streamlit_app():
    """Verifica se o Streamlit App está online"""
    try:
        response = requests.get("https://algoritmos-visualizador.streamlit.app/", timeout=10)
        if response.status_code == 200:
            print("✅ Streamlit App: Online")
            return True
        else:
            print(f"❌ Streamlit App: Erro HTTP {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Streamlit App: Erro de conexão - {e}")
        return False

def check_github_actions():
    """Verifica status do GitHub Actions (via GitHub CLI se disponível)"""
    try:
        result = subprocess.run(
            ["gh", "run", "list", "--limit", "1", "--json", "status,conclusion"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            runs = json.loads(result.stdout)
            if runs:
                latest_run = runs[0]
                status = latest_run.get("status", "unknown")
                conclusion = latest_run.get("conclusion", "unknown")
                
                if status == "completed" and conclusion == "success":
                    print("✅ GitHub Actions: Último build passou")
                    return True
                else:
                    print(f"❌ GitHub Actions: Status {status}, Conclusion {conclusion}")
                    return False
            else:
                print("⚠️ GitHub Actions: Nenhum run encontrado")
                return False
        else:
            print("⚠️ GitHub Actions: GitHub CLI não configurado")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ GitHub Actions: Verificação manual necessária")
        return False

def check_local_tests():
    """Executa testes locais básicos"""
    try:
        # Verificar se estamos no diretório correto
        if not os.path.exists("modulo_1_fundamentos"):
            print("❌ Testes Locais: Diretório modulo_1_fundamentos não encontrado")
            return False
            
        # Tentar importar módulos principais
        os.chdir("modulo_1_fundamentos")
        result = subprocess.run([
            sys.executable, "-c", 
            "from aplicacoes_reais import *; from casos_uso_praticos import *; print('✅ Imports OK')"
        ], capture_output=True, text=True, timeout=30)
        
        os.chdir("..")
        
        if result.returncode == 0:
            print("✅ Testes Locais: Imports funcionando")
            return True
        else:
            print(f"❌ Testes Locais: Erro - {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Testes Locais: Erro - {e}")
        return False

def check_dependencies():
    """Verifica se as dependências estão atualizadas"""
    try:
        # Verificar se pip check passa
        result = subprocess.run([sys.executable, "-m", "pip", "check"], 
                               capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Dependências: Sem conflitos")
            return True
        else:
            print(f"⚠️ Dependências: Conflitos encontrados - {result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Dependências: Erro na verificação - {e}")
        return False

def generate_report():
    """Gera relatório de monitoramento"""
    print("\n" + "="*60)
    print(f"📊 RELATÓRIO DE MONITORAMENTO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    checks = [
        ("Streamlit App", check_streamlit_app()),
        ("GitHub Actions", check_github_actions()),
        ("Testes Locais", check_local_tests()),
        ("Dependências", check_dependencies())
    ]
    
    total_checks = len(checks)
    passed_checks = sum(1 for _, passed in checks if passed)
    
    print(f"\n📈 RESUMO: {passed_checks}/{total_checks} verificações passaram")
    
    if passed_checks == total_checks:
        print("🎉 Status: TODOS OS SISTEMAS FUNCIONANDO")
        health_status = "SAUDÁVEL"
    elif passed_checks >= total_checks * 0.75:
        print("⚠️ Status: FUNCIONANDO COM ALERTAS")
        health_status = "ALERTA"
    else:
        print("❌ Status: PROBLEMAS CRÍTICOS DETECTADOS")
        health_status = "CRÍTICO"
    
    print(f"\n🔗 Links Importantes:")
    print(f"   • Streamlit App: https://algoritmos-visualizador.streamlit.app/")
    print(f"   • GitHub Actions: https://github.com/dronreef2/algoritmos-visualizador/actions")
    print(f"   • Repositório: https://github.com/dronreef2/algoritmos-visualizador")
    
    print(f"\n📋 Próximas Ações:")
    if health_status == "SAUDÁVEL":
        print("   • Continuar monitoramento regular")
        print("   • Verificar atualizações semanais")
    elif health_status == "ALERTA":
        print("   • Investigar avisos encontrados")
        print("   • Planejar correções")
    else:
        print("   • AÇÃO IMEDIATA: Corrigir problemas críticos")
        print("   • Verificar logs detalhados")
    
    print("="*60)
    return health_status

if __name__ == "__main__":
    print("🔍 Iniciando monitoramento do Algoritmos Visualizador...")
    
    # Instalar requests se não estiver disponível
    try:
        import requests
    except ImportError:
        print("📦 Instalando requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        import requests
    
    # Executar monitoramento
    health_status = generate_report()
    
    # Exit code baseado no status
    if health_status == "SAUDÁVEL":
        sys.exit(0)
    elif health_status == "ALERTA":
        sys.exit(1)
    else:
        sys.exit(2)
