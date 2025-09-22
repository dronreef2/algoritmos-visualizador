"""
VISUALIZADOR DE CURVAS DE ERRO - Visualizações Interativas
Complexidade Temporal: O(n) para renderização
Complexidade Espacial: O(n*d) onde n=épocas, d=dimensões

Intuição:
Visualizar a superfície de erro e a trajetória de otimização ajuda a entender
como diferentes algoritmos convergem para o mínimo da função de perda.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple
import streamlit as st


def superficie_erro_2d(w_range: Tuple[float, float] = (-2, 2), b_range: Tuple[float, float] = (-2, 2),
                      X: Optional[np.ndarray] = None, y: Optional[np.ndarray] = None,
                      resolution: int = 50) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Gera a superfície de erro para função de perda quadrática.

    Args:
        w_range: Intervalo para pesos
        b_range: Intervalo para bias
        X, y: Dados para calcular perda real
        resolution: Resolução da grade

    Returns:
        Tupla (W, B, Loss) - grades para plotagem
    """
    if X is None or y is None:
        # Dados sintéticos para demonstração
        X = np.array([[1], [2], [3], [4]])
        y = np.array([2, 4, 6, 8])

    W = np.linspace(w_range[0], w_range[1], resolution)
    B = np.linspace(b_range[0], b_range[1], resolution)
    W, B = np.meshgrid(W, B)

    Loss = np.zeros_like(W)

    for i in range(resolution):
        for j in range(resolution):
            w_val = W[i, j]
            b_val = B[i, j]
            Loss[i, j] = funcao_perda_simples(w_val, b_val, X, y)

    return W, B, Loss


def funcao_perda_simples(w: float, b: float, X: np.ndarray, y: np.ndarray) -> float:
    """Calcula perda quadrática simples."""
    pred = X.flatten() * w + b
    return np.mean((pred - y) ** 2)


def plot_curva_erro_2d(historico: Dict[str, List], X: np.ndarray, y: np.ndarray,
                       titulo: str = "Curva de Erro - Otimização") -> go.Figure:
    """
    Plota a curva de erro 2D com trajetória de otimização.

    Args:
        historico: Histórico de parâmetros e perdas
        X, y: Dados
        titulo: Título do gráfico

    Returns:
        Figura Plotly
    """
    # Gera superfície de erro
    W, B, Loss = superficie_erro_2d((-3, 3), (-3, 3), X, y, 30)

    # Cria figura 3D
    fig = go.Figure()

    # Superfície de erro
    fig.add_trace(go.Surface(
        x=W, y=B, z=Loss,
        name='Superfície de Erro',
        opacity=0.7,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Perda")
    ))

    # Trajetória de otimização
    w_hist = np.array(historico['w'])
    b_hist = np.array(historico['b'])
    loss_hist = np.array(historico['loss'])

    # Pontos da trajetória
    fig.add_trace(go.Scatter3d(
        x=w_hist[:, 0], y=b_hist, z=loss_hist,
        mode='markers+lines',
        name='Trajetória',
        line=dict(color='red', width=4),
        marker=dict(size=6, color='red')
    ))

    # Ponto inicial
    fig.add_trace(go.Scatter3d(
        x=[w_hist[0, 0]], y=[b_hist[0]], z=[loss_hist[0]],
        mode='markers',
        name='Início',
        marker=dict(size=10, color='green', symbol='diamond')
    ))

    # Ponto final
    fig.add_trace(go.Scatter3d(
        x=[w_hist[-1, 0]], y=[b_hist[-1]], z=[loss_hist[-1]],
        mode='markers',
        name='Final',
        marker=dict(size=10, color='blue', symbol='diamond')
    ))

    fig.update_layout(
        title=titulo,
        scene=dict(
            xaxis_title='Peso (w)',
            yaxis_title='Bias (b)',
            zaxis_title='Perda',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=800,
        height=600
    )

    return fig


def plot_convergencia(historico: Dict[str, List], titulo: str = "Convergência da Perda") -> go.Figure:
    """
    Plota o gráfico de convergência da função de perda.

    Args:
        historico: Histórico de perdas
        titulo: Título do gráfico

    Returns:
        Figura Plotly
    """
    epocas = list(range(len(historico['loss'])))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=epocas,
        y=historico['loss'],
        mode='lines+markers',
        name='Perda',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title='Época',
        yaxis_title='Perda',
        width=600,
        height=400
    )

    return fig


def plot_parametros(historico: Dict[str, List], titulo: str = "Evolução dos Parâmetros") -> go.Figure:
    """
    Plota a evolução dos parâmetros ao longo das épocas.

    Args:
        historico: Histórico de parâmetros
        titulo: Título do gráfico

    Returns:
        Figura Plotly
    """
    epocas = list(range(len(historico['w'])))

    fig = go.Figure()

    # Pesos
    w_hist = np.array(historico['w'])
    for i in range(w_hist.shape[1]):
        fig.add_trace(go.Scatter(
            x=epocas,
            y=w_hist[:, i],
            mode='lines+markers',
            name=f'Peso w{i}',
            line=dict(width=2)
        ))

    # Bias
    fig.add_trace(go.Scatter(
        x=epocas,
        y=historico['b'],
        mode='lines+markers',
        name='Bias b',
        line=dict(width=2, dash='dash')
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title='Época',
        yaxis_title='Valor do Parâmetro',
        width=600,
        height=400
    )

    return fig


def criar_animacao_otimizacao(historico: Dict[str, List], X: np.ndarray, y: np.ndarray,
                             titulo: str = "Animação da Otimização") -> go.Figure:
    """
    Cria animação da trajetória de otimização.

    Args:
        historico: Histórico completo
        X, y: Dados
        titulo: Título

    Returns:
        Figura Plotly com animação
    """
    # Gera superfície
    W, B, Loss = superficie_erro_2d((-3, 3), (-3, 3), X, y, 30)

    # Dados para animação
    w_hist = np.array(historico['w'])
    b_hist = np.array(historico['b'])
    loss_hist = np.array(historico['loss'])

    # Cria frames
    frames = []
    for i in range(len(w_hist)):
        frame_data = [
            go.Surface(x=W, y=B, z=Loss, opacity=0.7, colorscale='Viridis', showscale=False),
            go.Scatter3d(
                x=w_hist[:i+1, 0], y=b_hist[:i+1], z=loss_hist[:i+1],
                mode='markers+lines',
                line=dict(color='red', width=4),
                marker=dict(size=6, color='red')
            )
        ]
        frames.append(go.Frame(data=frame_data, name=f'Época {i}'))

    # Figura inicial
    fig = go.Figure(
        data=[
            go.Surface(x=W, y=B, z=Loss, opacity=0.7, colorscale='Viridis', showscale=True, colorbar=dict(title="Perda")),
            go.Scatter3d(x=[w_hist[0, 0]], y=[b_hist[0]], z=[loss_hist[0]], mode='markers', marker=dict(size=10, color='green'))
        ],
        frames=frames
    )

    # Configura animação
    fig.update_layout(
        title=titulo,
        scene=dict(
            xaxis_title='Peso (w)',
            yaxis_title='Bias (b)',
            zaxis_title='Perda',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=800,
        height=600,
        updatemenus=[{
            'type': 'buttons',
            'buttons': [
                {
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 500, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 300}
                    }]
                },
                {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ]
        }]
    )

    return fig