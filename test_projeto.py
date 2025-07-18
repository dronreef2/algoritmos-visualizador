"""
Testes básicos para o projeto Algoritmos Visualizador
"""
import pytest
import sys
import os

# Adicionar o diretório do módulo 1 ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modulo_1_fundamentos'))

def test_imports():
    """Testa se os módulos principais podem ser importados"""
    try:
        from aplicacoes_reais import SistemaBuscaLogs, DetectorFraudes, RedeSocial
        from casos_uso_praticos import dois_ponteiros_soma_alvo
        assert True
    except ImportError as e:
        pytest.fail(f"Falha na importação: {e}")

def test_sistema_busca_logs():
    """Testa o sistema de busca em logs"""
    from aplicacoes_reais import SistemaBuscaLogs
    
    sistema = SistemaBuscaLogs()
    sistema.adicionar_log(1000, 'INFO', 'Teste de log')
    sistema.adicionar_log(2000, 'ERROR', 'Erro de teste')
    
    # Buscar logs em um período
    resultado = sistema.buscar_logs_periodo(500, 1500)
    assert len(resultado) == 1
    assert resultado[0][1] == 'INFO'

def test_detector_fraudes():
    """Testa o detector de fraudes"""
    from aplicacoes_reais import DetectorFraudes
    
    detector = DetectorFraudes()
    detector.adicionar_transacao(1000, 100, 'DEPOSITO', 'conta1')
    detector.adicionar_transacao(1100, 200, 'SAQUE', 'conta1')
    
    # Deve ter duas transações
    assert len(detector.transacoes) == 2

def test_rede_social():
    """Testa a rede social"""
    from aplicacoes_reais import RedeSocial
    
    rede = RedeSocial()
    rede.adicionar_amizade('Alice', 'Bob')
    rede.adicionar_amizade('Bob', 'Carol')
    
    # Testar grau de separação
    grau = rede.grau_separacao('Alice', 'Bob')
    assert grau == 1
    
    grau = rede.grau_separacao('Alice', 'Carol')
    assert grau == 2

def test_template_dois_ponteiros():
    """Testa o template de dois ponteiros"""
    from casos_uso_praticos import dois_ponteiros_soma_alvo
    
    arr = [1, 2, 3, 4, 5, 6]
    resultado = dois_ponteiros_soma_alvo(arr, 9)
    assert resultado == (2, 5)  # índices dos elementos que somam 9

def test_template_busca_binaria():
    """Testa o template de busca binária"""
    from casos_uso_praticos import busca_binaria_template
    
    arr = [1, 3, 5, 7, 9]
    resultado = busca_binaria_template(arr, 5)
    assert resultado == 2  # índice do elemento 5

if __name__ == '__main__':
    pytest.main([__file__])
