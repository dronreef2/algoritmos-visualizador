#!/usr/bin/env python3
"""
🔍 Script de Diagnóstico de Conectividade e Autenticação
Para resolver problemas de erro 401 e outros problemas de conexão
"""

import os
import sys
import socket
import json
from datetime import datetime
import subprocess


def check_network_connectivity():
    """Verifica conectividade básica de rede"""
    print("🌐 Verificando conectividade de rede...")

    results = {}

    # Teste básico de conectividade
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        results["internet"] = "✅ OK"
        print("   ✅ Conectividade com internet: OK")
    except Exception as e:
        results["internet"] = f"❌ Falha: {e}"
        print(f"   ❌ Conectividade com internet: Falha - {e}")

    # Teste de DNS
    try:
        socket.gethostbyname("google.com")
        results["dns"] = "✅ OK"
        print("   ✅ Resolução DNS: OK")
    except Exception as e:
        results["dns"] = f"❌ Falha: {e}"
        print(f"   ❌ Resolução DNS: Falha - {e}")

    return results


def check_authentication_tokens():
    """Verifica tokens de autenticação disponíveis"""
    print("\\n🔐 Verificando tokens de autenticação...")

    results = {}

    # Verificar tokens GitHub
    github_token = os.environ.get("GITHUB_TOKEN")
    github_codespace_token = os.environ.get("GITHUB_CODESPACE_TOKEN")

    if github_token:
        results["github_token"] = "✅ Configurado"
        print("   ✅ GITHUB_TOKEN: Configurado")
        print(f"       Comprimento: {len(github_token)} caracteres")
    else:
        results["github_token"] = "❌ Não encontrado"
        print("   ❌ GITHUB_TOKEN: Não encontrado")

    if github_codespace_token:
        results["github_codespace_token"] = "✅ Configurado"
        print("   ✅ GITHUB_CODESPACE_TOKEN: Configurado")
        print(f"       Comprimento: {len(github_codespace_token)} caracteres")
    else:
        results["github_codespace_token"] = "❌ Não encontrado"
        print("   ❌ GITHUB_CODESPACE_TOKEN: Não encontrado")

    # Verificar outras variáveis de autenticação
    other_auth_vars = [
        var
        for var in os.environ.keys()
        if any(term in var.lower() for term in ["key", "secret", "auth", "token"])
        and var not in ["GITHUB_TOKEN", "GITHUB_CODESPACE_TOKEN"]
    ]

    if other_auth_vars:
        results["other_auth_vars"] = other_auth_vars
        print(f"   ℹ️  Outras variáveis de autenticação encontradas: {len(other_auth_vars)}")
        for var in other_auth_vars:
            print(f"       - {var}")

    return results


def check_service_availability():
    """Verifica disponibilidade de serviços externos"""
    print("\\n🔗 Verificando disponibilidade de serviços...")

    results = {}

    services = {"fonts.googleapis.com": 443, "visualgo.net": 80, "github.githubassets.com": 443}

    for service, port in services.items():
        try:
            socket.create_connection((service, port), timeout=5)
            results[service] = "✅ OK"
            print(f"   ✅ {service}: OK")
        except Exception as e:
            results[service] = f"❌ Indisponível: {e}"
            print(f"   ❌ {service}: Indisponível - {e}")

    return results


def check_python_imports():
    """Verifica imports do Python necessários"""
    print("\\n🐍 Verificando imports do Python...")

    results = {}

    required_modules = ["streamlit", "numpy", "pandas", "asyncio", "plotly"]

    for module in required_modules:
        try:
            __import__(module)
            results[module] = "✅ OK"
            print(f"   ✅ {module}: OK")
        except ImportError as e:
            results[module] = f"❌ Falha: {e}"
            print(f"   ❌ {module}: Falha - {e}")

    return results


def generate_recommendations(network, auth, services, imports):
    """Gera recomendações baseadas nos resultados dos testes"""
    print("\\n💡 Gerando recomendações...")

    recommendations = []

    # Recomendações de rede
    if network.get("internet", "").startswith("❌"):
        recommendations.append("🔧 Verifique sua conexão com a internet")
        recommendations.append("🔧 Execute: ping 8.8.8.8")

    if network.get("dns", "").startswith("❌"):
        recommendations.append("🔧 Verifique configuração de DNS")
        recommendations.append("🔧 Execute: nslookup google.com")

    # Recomendações de autenticação
    if auth.get("github_token", "").startswith("❌") and auth.get("github_codespace_token", "").startswith("❌"):
        recommendations.append("🔐 Configure GITHUB_TOKEN para operações GitHub")
        recommendations.append("🔐 No GitHub: Settings > Developer settings > Personal access tokens")
        recommendations.append("🔐 Execute: export GITHUB_TOKEN=your_token_here")

    # Recomendações de serviços
    unavailable_services = [service for service, status in services.items() if status.startswith("❌")]
    if unavailable_services:
        recommendations.append(f"🔗 Serviços indisponíveis: {', '.join(unavailable_services)}")
        recommendations.append("🔗 Verifique firewall/proxy ou tente novamente mais tarde")

    # Recomendações de imports
    failed_imports = [module for module, status in imports.items() if status.startswith("❌")]
    if failed_imports:
        recommendations.append(f"📦 Módulos faltando: {', '.join(failed_imports)}")
        recommendations.append("📦 Execute: pip install " + " ".join(failed_imports))

    return recommendations


def main():
    """Função principal do diagnóstico"""
    print("🚀 Iniciando diagnóstico de conectividade e autenticação")
    print("=" * 60)

    # Executar todos os testes
    network_results = check_network_connectivity()
    auth_results = check_authentication_tokens()
    service_results = check_service_availability()
    import_results = check_python_imports()

    # Gerar recomendações
    recommendations = generate_recommendations(network_results, auth_results, service_results, import_results)

    # Resumo final
    print("\\n" + "=" * 60)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 60)

    all_results = {
        "network": network_results,
        "authentication": auth_results,
        "services": service_results,
        "imports": import_results,
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat(),
    }

    # Contar status
    total_checks = 0
    successful_checks = 0

    for category_results in [network_results, auth_results, service_results, import_results]:
        for status in category_results.values():
            total_checks += 1
            if isinstance(status, str) and status.startswith("✅"):
                successful_checks += 1
            elif isinstance(status, list):  # Para listas de variáveis
                successful_checks += 1

    success_rate = (successful_checks / total_checks * 100) if total_checks > 0 else 0

    print(".1f")
    print(f"Total de verificações: {total_checks}")
    print(f"Verificações bem-sucedidas: {successful_checks}")

    # Status geral
    if success_rate >= 90:
        print("🎉 Status: EXCELENTE - Sistema funcionando perfeitamente!")
    elif success_rate >= 75:
        print("✅ Status: BOM - Pequenos ajustes podem ser necessários")
    elif success_rate >= 50:
        print("⚠️  Status: REGULAR - Algumas correções são recomendadas")
    else:
        print("❌ Status: CRÍTICO - Ação imediata necessária")

    # Exibir recomendações
    if recommendations:
        print("\\n💡 RECOMENDAÇÕES:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("\\n✅ Nenhuma recomendação necessária!")

    # Salvar relatório
    report_file = f"diagnostico_conectividade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\\n📄 Relatório salvo em: {report_file}")
    except Exception as e:
        print(f"\\n❌ Erro ao salvar relatório: {e}")

    print("\\n🎯 Diagnóstico concluído!")
    return all_results


if __name__ == "__main__":
    main()
