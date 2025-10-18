"""
OTIMIZADORES PARA REDES NEURAIS - Algoritmos de Otimização
Complexidade Temporal: O(n*m) onde n=épocas, m=tamanho do dataset
Complexidade Espacial: O(d) onde d=dimensões dos parâmetros

Intuição:
Os otimizadores ajustam os parâmetros da rede neural para minimizar a função de perda.
Cada algoritmo tem características diferentes em termos de convergência e robustez.
"""

import numpy as np
from typing import List, Dict, Optional, Callable, Tuple
import time


class OtimizadorBase:
    """
    Classe base para otimizadores de redes neurais.

    Args:
        learning_rate: Taxa de aprendizado
        params: Dicionário com parâmetros a otimizar
    """

    def __init__(self, learning_rate: float = 0.01, params: Optional[Dict[str, np.ndarray]] = None):
        self.learning_rate = learning_rate
        self.params = params or {}
        self.gradients_history = []
        self.params_history = []
        self.loss_history = []

    def step(self, gradients: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Atualiza os parâmetros baseado nos gradientes.

        Args:
            gradients: Gradientes calculados

        Returns:
            Dicionário com novos parâmetros
        """
        raise NotImplementedError

    def reset_history(self):
        """Reseta o histórico de otimizações."""
        self.gradients_history = []
        self.params_history = []
        self.loss_history = []


class GradienteDescendente(OtimizadorBase):
    """
    Gradiente Descendente Básico (Batch Gradient Descent)

    Complexidade: O(n*m) tempo, O(d) espaço
    Vantagens: Simples, converge para mínimo global em funções convexas
    Desvantagens: Lento em datasets grandes, pode ficar preso em mínimos locais
    """

    def step(self, gradients: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Atualiza parâmetros usando gradiente descendente."""
        for param_name, grad in gradients.items():
            if param_name in self.params:
                self.params[param_name] -= self.learning_rate * grad

        # Salva histórico
        self.params_history.append(self.params.copy())
        self.gradients_history.append(gradients.copy())

        return self.params.copy()


class SGD(OtimizadorBase):
    """
    Stochastic Gradient Descent

    Complexidade: O(1) por amostra, O(d) espaço
    Vantagens: Mais rápido que GD, pode escapar de mínimos locais
    Desvantagens: Pode oscilar, converge mais lentamente
    """

    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.0,
                 params: Optional[Dict[str, np.ndarray]] = None):
        super().__init__(learning_rate, params)
        self.momentum = momentum
        self.velocity = {}

    def step(self, gradients: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Atualiza parâmetros usando SGD com momentum opcional."""
        for param_name, grad in gradients.items():
            if param_name in self.params:
                # Inicializa velocity se necessário
                if param_name not in self.velocity:
                    self.velocity[param_name] = np.zeros_like(grad)

                # Aplica momentum
                self.velocity[param_name] = self.momentum * self.velocity[param_name] - self.learning_rate * grad

                # Atualiza parâmetro
                self.params[param_name] += self.velocity[param_name]

        # Salva histórico
        self.params_history.append(self.params.copy())
        self.gradients_history.append(gradients.copy())

        return self.params.copy()


class Adam(OtimizadorBase):
    """
    Adaptive Moment Estimation

    Complexidade: O(n*m) tempo, O(d) espaço
    Vantagens: Adapta learning rate por parâmetro, bom para funções não-convexas
    Desvantagens: Mais parâmetros para ajustar, pode ser lento
    """

    def __init__(self, learning_rate: float = 0.001, beta1: float = 0.9, beta2: float = 0.999,
                 epsilon: float = 1e-8, params: Optional[Dict[str, np.ndarray]] = None):
        super().__init__(learning_rate, params)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = {}  # Primeiro momento
        self.v = {}  # Segundo momento
        self.t = 0   # Contador de passos

    def step(self, gradients: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Atualiza parâmetros usando Adam."""
        self.t += 1

        for param_name, grad in gradients.items():
            if param_name in self.params:
                # Inicializa momentos se necessário
                if param_name not in self.m:
                    self.m[param_name] = np.zeros_like(grad)
                    self.v[param_name] = np.zeros_like(grad)

                # Atualiza momentos
                self.m[param_name] = self.beta1 * self.m[param_name] + (1 - self.beta1) * grad
                self.v[param_name] = self.beta2 * self.v[param_name] + (1 - self.beta2) * (grad ** 2)

                # Correção de bias
                m_hat = self.m[param_name] / (1 - self.beta1 ** self.t)
                v_hat = self.v[param_name] / (1 - self.beta2 ** self.t)

                # Atualiza parâmetro
                self.params[param_name] -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)

        # Salva histórico
        self.params_history.append(self.params.copy())
        self.gradients_history.append(gradients.copy())

        return self.params.copy()


def funcao_perda_quadratica(w: np.ndarray, b: float, X: np.ndarray, y: np.ndarray) -> float:
    """
    Função de perda quadrática para regressão linear simples.

    Args:
        w: Pesos
        b: Bias
        X: Features
        y: Targets

    Returns:
        Valor da perda
    """
    pred = X @ w + b
    return np.mean((pred - y) ** 2)


def gradiente_perda_quadratica(w: np.ndarray, b: float, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Gradiente da função de perda quadrática.

    Returns:
        Tupla (grad_w, grad_b)
    """
    n = len(X)
    pred = X @ w + b
    error = pred - y

    grad_w = (2/n) * X.T @ error
    grad_b = (2/n) * np.sum(error)

    return grad_w, grad_b


def otimizar_rede_simples(X: np.ndarray, y: np.ndarray, otimizador: OtimizadorBase,
                         num_epocas: int = 100) -> Dict[str, List]:
    """
    Otimiza uma rede neural simples (regressão linear) usando o otimizador fornecido.

    Args:
        X: Dados de entrada
        y: Targets
        otimizador: Instância do otimizador
        num_epocas: Número de épocas

    Returns:
        Histórico de parâmetros e perdas
    """
    # Inicializa parâmetros
    w = np.random.randn(X.shape[1]) * 0.1
    b = 0.0

    otimizador.params = {'w': w, 'b': b}

    historico = {
        'w': [],
        'b': [],
        'loss': []
    }

    for epoca in range(num_epocas):
        # Calcula gradientes
        grad_w, grad_b = gradiente_perda_quadratica(w, b, X, y)
        gradients = {'w': grad_w, 'b': grad_b}

        # Atualiza parâmetros
        novos_params = otimizador.step(gradients)
        w, b = novos_params['w'], novos_params['b']

        # Calcula perda
        loss = funcao_perda_quadratica(w, b, X, y)

        # Salva histórico
        historico['w'].append(w.copy())
        historico['b'].append(b)
        historico['loss'].append(loss)

    return historico