"""
EXERCÍCIOS INTERATIVOS - Aprendizado Prático de Redes Neurais
Complexidade Temporal: O(1) para validação
Complexidade Espacial: O(1)

Intuição:
Exercícios interativos permitem que o usuário pratique conceitos de otimização
de redes neurais através de código executável e feedback imediato.
"""

import streamlit as st
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import time
import re


class ExercicioInterativo:
    """
    Classe base para exercícios interativos de redes neurais.
    """

    def __init__(self, titulo: str, descricao: str, dificuldade: str = "Iniciante"):
        self.titulo = titulo
        self.descricao = descricao
        self.dificuldade = dificuldade
        self.pontuacao_maxima = 100
        self.tentativas = 0

    def validar_codigo(self, codigo: str) -> Tuple[bool, str, int]:
        """
        Valida o código do usuário.

        Returns:
            Tupla (sucesso, feedback, pontuacao)
        """
        raise NotImplementedError

    def executar_codigo_seguro(self, codigo: str) -> Dict[str, Any]:
        """
        Executa código Python de forma segura (limitada).

        Args:
            codigo: Código a executar

        Returns:
            Resultados da execução
        """
        # Contexto seguro para execução
        contexto_seguro = {
            'np': np,
            'numpy': np,
            'math': __import__('math'),
            'random': __import__('random'),
            '__builtins__': {
                'len': len,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'int': int,
                'float': float,
                'str': str,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'print': print,
            }
        }

        try:
            # Executa o código
            exec(codigo, contexto_seguro)

            # Captura variáveis definidas
            resultado = {}
            for var in ['w', 'b', 'loss', 'grad_w', 'grad_b', 'pred']:
                if var in contexto_seguro:
                    resultado[var] = contexto_seguro[var]

            return {'sucesso': True, 'resultado': resultado, 'erro': None}

        except Exception as e:
            return {'sucesso': False, 'resultado': None, 'erro': str(e)}


class ExercicioGradienteDescendente(ExercicioInterativo):
    """
    Exercício: Implementar uma etapa do gradiente descendente.
    """

    def __init__(self):
        super().__init__(
            titulo="Implemente o Gradiente Descendente",
            descricao="""
            Implemente uma função que realize uma atualização de parâmetros usando gradiente descendente.

            **Objetivo:** Dado um peso `w`, bias `b`, gradientes `grad_w` e `grad_b`, e taxa de aprendizado `lr`,
            atualize os parâmetros usando a fórmula: `novo_param = param_atual - lr * gradiente`

            **Dica:** Use as variáveis `w`, `b`, `grad_w`, `grad_b` e `lr` que já estão definidas.
            """,
            dificuldade="Iniciante"
        )

    def validar_codigo(self, codigo: str) -> Tuple[bool, str, int]:
        self.tentativas += 1

        # Valores de teste
        w_teste, b_teste = 2.0, 1.0
        grad_w_teste, grad_b_teste = 0.5, 0.2
        lr_teste = 0.1

        # Executa código do usuário
        resultado = self.executar_codigo_seguro(codigo)

        if not resultado['sucesso']:
            return False, f"Erro na execução: {resultado['erro']}", 0

        # Verifica se as variáveis foram atualizadas corretamente
        vars_resultado = resultado['resultado']

        if 'w' not in vars_resultado or 'b' not in vars_resultado:
            return False, "As variáveis 'w' e 'b' devem ser atualizadas no código.", 10

        w_novo = vars_resultado['w']
        b_novo = vars_resultado['b']

        w_esperado = w_teste - lr_teste * grad_w_teste
        b_esperado = b_teste - lr_teste * grad_b_teste

        if abs(w_novo - w_esperado) < 1e-6 and abs(b_novo - b_esperado) < 1e-6:
            pontuacao = max(50, 100 - (self.tentativas - 1) * 10)
            return True, "Excelente! Você implementou corretamente o gradiente descendente.", pontuacao
        else:
            return False, f"Resultado incorreto. Esperado: w={w_esperado:.3f}, b={b_esperado:.3f}. Obtido: w={w_novo:.3f}, b={b_novo:.3f}", 10


class ExercicioFuncaoPerda(ExercicioInterativo):
    """
    Exercício: Implementar função de perda MSE.
    """

    def __init__(self):
        super().__init__(
            titulo="Implemente a Função de Perda MSE",
            descricao="""
            Implemente a função Mean Squared Error (MSE) para avaliar o erro de um modelo.

            **Objetivo:** Calcule o MSE entre as predições `pred` e os valores reais `y`.

            **Fórmula:** MSE = (1/n) * Σ(y_i - pred_i)²

            **Dica:** Use as variáveis `pred` e `y` que já estão definidas.
            """,
            dificuldade="Iniciante"
        )

    def validar_codigo(self, codigo: str) -> Tuple[bool, str, int]:
        self.tentativas += 1

        # Valores de teste
        pred_teste = np.array([2.1, 3.9, 5.8, 7.2])
        y_teste = np.array([2.0, 4.0, 6.0, 8.0])

        # Executa código do usuário
        resultado = self.executar_codigo_seguro(codigo)

        if not resultado['sucesso']:
            return False, f"Erro na execução: {resultado['erro']}", 0

        vars_resultado = resultado['resultado']

        if 'loss' not in vars_resultado:
            return False, "A variável 'loss' deve ser calculada no código.", 10

        loss_calculada = vars_resultado['loss']
        loss_esperada = np.mean((y_teste - pred_teste) ** 2)

        if abs(loss_calculada - loss_esperada) < 1e-6:
            pontuacao = max(50, 100 - (self.tentativas - 1) * 10)
            return True, f"Correto! MSE = {loss_esperada:.4f}", pontuacao
        else:
            return False, f"Incorreto. Esperado: {loss_esperada:.4f}, Obtido: {loss_calculada:.4f}", 10


class ExercicioOtimizadorComparacao(ExercicioInterativo):
    """
    Exercício: Comparar diferentes otimizadores.
    """

    def __init__(self):
        super().__init__(
            titulo="Compare Otimizadores: SGD vs Adam",
            descricao="""
            Analise e compare o comportamento de SGD e Adam em uma função de perda simples.

            **Objetivo:** Execute otimizações com ambos os algoritmos e observe as diferenças.

            **Instruções:**
            1. Execute o código fornecido
            2. Observe as trajetórias no gráfico 3D
            3. Compare a velocidade de convergência
            4. Responda às perguntas sobre as diferenças

            **Perguntas:**
            - Qual otimizador converge mais rápido?
            - Qual parece mais estável?
            - Em que situações você usaria cada um?
            """,
            dificuldade="Intermediário"
        )

    def validar_codigo(self, codigo: str) -> Tuple[bool, str, int]:
        # Este exercício é mais conceitual, focado em observação
        return True, "Exercício completado! Compare os gráficos e trajetórias dos otimizadores.", 100


def criar_interface_exercicio(exercicio: ExercicioInterativo):
    """
    Cria interface Streamlit para um exercício interativo.
    """
    st.header(f"🎯 {exercicio.titulo}")
    st.markdown(f"**Dificuldade:** {exercicio.dificuldade}")
    st.markdown(exercicio.descricao)

    # Área de código
    st.subheader("💻 Seu Código")
    codigo_usuario = st.text_area(
        "Digite seu código Python aqui:",
        height=200,
        key=f"codigo_{exercicio.titulo.replace(' ', '_')}"
    )

    # Botão de validação
    if st.button("🚀 Executar e Validar", key=f"validar_{exercicio.titulo.replace(' ', '_')}"):
        if not codigo_usuario.strip():
            st.warning("Por favor, digite algum código antes de validar.")
            return

        with st.spinner("Validando código..."):
            sucesso, feedback, pontuacao = exercicio.validar_codigo(codigo_usuario)

        if sucesso:
            st.success(f"✅ {feedback}")
            st.balloons()
        else:
            st.error(f"❌ {feedback}")

        # Mostra pontuação
        st.metric("Pontuação", f"{pontuacao}/{exercicio.pontuacao_maxima}")

        # Feedback adicional
        if pontuacao == exercicio.pontuacao_maxima:
            st.info("🎉 Pontuação máxima! Você dominou este conceito!")
        elif pontuacao > 50:
            st.info("👍 Bom trabalho! Continue praticando para aperfeiçoar.")
        else:
            st.info("💪 Não desista! Tente novamente com uma abordagem diferente.")


def mostrar_dashboard_exercicios():
    """
    Mostra dashboard com progresso dos exercícios.
    """
    st.header("📊 Progresso dos Exercícios")

    # Dados de exemplo (em produção, viriam do session_state)
    exercicios = [
        {"nome": "Gradiente Descendente", "status": "✅ Completado", "pontuacao": 90},
        {"nome": "Função de Perda MSE", "status": "✅ Completado", "pontuacao": 85},
        {"nome": "Comparação SGD vs Adam", "status": "🔄 Em Andamento", "pontuacao": 0},
    ]

    df = pd.DataFrame(exercicios)
    st.dataframe(df)

    # Gráfico de progresso
    completados = len([e for e in exercicios if "✅" in e["status"]])
    total = len(exercicios)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Exercícios Completados", f"{completados}/{total}")
    with col2:
        progresso = completados / total * 100
        st.progress(progresso / 100)
        st.write(f"Progresso: {progresso:.1f}%")