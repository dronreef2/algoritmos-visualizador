#!/usr/bin/env python3
"""
Script de diagnóstico para testar os módulos educacionais
"""

import sys
import os
sys.path.append('/workspaces/algoritmos-visualizador')

def testar_modulos():
    print("🔍 Iniciando diagnóstico dos módulos educacionais...")

    try:
        from modulos_integrados import modulos_integrados
        print("✅ Importação do módulo modulos_integrados: SUCESSO")

        # Testar carregamento de cada módulo
        for i in range(4):
            print(f"\n📚 Testando Módulo {i+1}...")
            try:
                conteudo = modulos_integrados.carregar_conteudo_modulo(i)
                if "erro" in conteudo:
                    print(f"❌ Erro no módulo {i+1}: {conteudo['erro']}")
                else:
                    arquivos = conteudo.get("arquivos", {})
                    print(f"✅ Módulo {i+1} carregado: {len(arquivos)} arquivos encontrados")

                    # Mostrar alguns arquivos como exemplo
                    for nome_arquivo, info in list(arquivos.items())[:3]:
                        if isinstance(info, dict) and "conteudo" in info:
                            tamanho = len(info["conteudo"])
                            print(f"   📄 {nome_arquivo}: {tamanho} caracteres")
                        else:
                            print(f"   ❌ {nome_arquivo}: erro no carregamento")

            except Exception as e:
                print(f"❌ Erro ao carregar módulo {i+1}: {e}")

        print("\n🎉 Diagnóstico concluído!")

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")

    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    testar_modulos()
