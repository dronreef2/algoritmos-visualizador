"""
MÓDULO 5: REDES NEURAIS - Otimização e Visualização
===============================================

Este módulo foca no aprendizado visual e interativo de como redes neurais
otimizam seus parâmetros para minimizar funções de perda.

Funcionalidades:
- ✅ Algoritmos de otimização (GD, SGD, Adam)
- ✅ Visualizações 3D da superfície de erro
- ✅ Animações de trajetória de otimização
- ✅ Exercícios interativos com código
- ✅ Comparação de otimizadores
- ✅ Integração com GitHub para exemplos reais
"""

from .otimizadores import (
    OtimizadorBase,
    GradienteDescendente,
    SGD,
    Adam,
    otimizar_rede_simples,
    funcao_perda_quadratica,
    gradiente_perda_quadratica
)

from .visualizacoes import (
    superficie_erro_2d,
    plot_curva_erro_2d,
    plot_convergencia,
    plot_parametros,
    criar_animacao_otimizacao
)

from .exercicios import (
    ExercicioInterativo,
    ExercicioGradienteDescendente,
    ExercicioFuncaoPerda,
    ExercicioOtimizadorComparacao,
    criar_interface_exercicio,
    mostrar_dashboard_exercicios
)

__all__ = [
    # Otimizadores
    'OtimizadorBase', 'GradienteDescendente', 'SGD', 'Adam',
    'otimizar_rede_simples', 'funcao_perda_quadratica', 'gradiente_perda_quadratica',

    # Visualizações
    'superficie_erro_2d', 'plot_curva_erro_2d', 'plot_convergencia',
    'plot_parametros', 'criar_animacao_otimizacao',

    # Exercícios
    'ExercicioInterativo', 'ExercicioGradienteDescendente',
    'ExercicioFuncaoPerda', 'ExercicioOtimizadorComparacao',
    'criar_interface_exercicio', 'mostrar_dashboard_exercicios'
]