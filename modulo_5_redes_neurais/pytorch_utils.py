"""
UTILITÁRIOS PYTORCH - Módulo 5: Redes Neurais
============================================

Funcionalidades específicas para trabalhar com PyTorch no módulo de redes neurais.
Inclui criação, treinamento e visualização de modelos PyTorch.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Any
import time


class RedeNeuralPyTorch(nn.Module):
    """
    Rede neural simples implementada em PyTorch para demonstrações.
    """

    def __init__(self, input_size: int = 2, hidden_size: int = 10, output_size: int = 1):
        """
        Inicializa a rede neural.

        Args:
            input_size: Número de features de entrada
            hidden_size: Número de neurônios na camada oculta
            output_size: Número de saídas
        """
        super(RedeNeuralPyTorch, self).__init__()
        self.camada_oculta = nn.Linear(input_size, hidden_size)
        self.camada_saida = nn.Linear(hidden_size, output_size)
        self.ativacao = nn.ReLU()

    def forward(self, x):
        """
        Forward pass da rede.

        Args:
            x: Tensor de entrada

        Returns:
            Tensor de saída
        """
        x = self.ativacao(self.camada_oculta(x))
        x = self.camada_saida(x)
        return x


class UtilitariosPyTorch:
    """
    Utilitários para trabalhar com PyTorch no contexto educacional.
    """

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"PyTorch utilizando: {self.device}")

    def criar_dados_exemplo(self, num_amostras: int = 1000) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Cria dados de exemplo para classificação não-linear.

        Args:
            num_amostras: Número de amostras a gerar

        Returns:
            Tupla (X, y) com dados de entrada e rótulos
        """
        # Gera dados em formato de círculos concêntricos
        np.random.seed(42)
        torch.manual_seed(42)

        # Classe 0: círculo interno
        theta0 = np.random.uniform(0, 2*np.pi, num_amostras//2)
        r0 = np.random.uniform(0, 0.7, num_amostras//2)
        x0 = r0 * np.cos(theta0)
        y0 = r0 * np.sin(theta0)

        # Classe 1: círculo externo
        theta1 = np.random.uniform(0, 2*np.pi, num_amostras//2)
        r1 = np.random.uniform(0.8, 1.2, num_amostras//2)
        x1 = r1 * np.cos(theta1)
        y1 = r1 * np.sin(theta1)

        # Combina os dados
        X = np.column_stack([np.concatenate([x0, x1]), np.concatenate([y0, y1])])
        y = np.concatenate([np.zeros(num_amostras//2), np.ones(num_amostras//2)])

        # Converte para tensores PyTorch
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y).unsqueeze(1)

        return X_tensor, y_tensor

    def treinar_rede(self, modelo: nn.Module, X: torch.Tensor, y: torch.Tensor,
                    num_epocas: int = 100, learning_rate: float = 0.01) -> Dict[str, List]:
        """
        Treina uma rede neural PyTorch.

        Args:
            modelo: Modelo PyTorch a ser treinado
            X: Dados de entrada
            y: Rótulos
            num_epocas: Número de épocas de treinamento
            learning_rate: Taxa de aprendizado

        Returns:
            Dicionário com histórico de treinamento
        """
        modelo = modelo.to(self.device)
        X = X.to(self.device)
        y = y.to(self.device)

        # Função de perda e otimizador
        criterio = nn.MSELoss()
        otimizador = optim.Adam(modelo.parameters(), lr=learning_rate)

        # Histórico
        historico = {
            'loss': [],
            'epoca': []
        }

        modelo.train()
        for epoca in range(num_epocas):
            # Forward pass
            saidas = modelo(X)
            perda = criterio(saidas, y)

            # Backward pass
            otimizador.zero_grad()
            perda.backward()
            otimizador.step()

            # Registra progresso
            if epoca % 10 == 0:
                historico['loss'].append(perda.item())
                historico['epoca'].append(epoca)
                print(f'Época {epoca}/{num_epocas}, Perda: {perda.item():.4f}')

        return historico

    def avaliar_rede(self, modelo: nn.Module, X: torch.Tensor, y: torch.Tensor) -> Dict[str, float]:
        """
        Avalia o desempenho de uma rede neural.

        Args:
            modelo: Modelo treinado
            X: Dados de teste
            y: Rótulos verdadeiros

        Returns:
            Métricas de avaliação
        """
        modelo = modelo.to(self.device)
        X = X.to(self.device)
        y = y.to(self.device)

        modelo.eval()
        with torch.no_grad():
            predicoes = modelo(X)
            perda = nn.MSELoss()(predicoes, y)

            # Converte para classificação binária
            predicoes_binarias = (predicoes > 0.5).float()
            acuracia = (predicoes_binarias == y).float().mean().item()

        return {
            'loss': perda.item(),
            'accuracy': acuracia
        }

    def salvar_modelo(self, modelo: nn.Module, caminho: str):
        """
        Salva um modelo PyTorch.

        Args:
            modelo: Modelo a ser salvo
            caminho: Caminho do arquivo
        """
        torch.save(modelo.state_dict(), caminho)
        print(f"Modelo salvo em: {caminho}")

    def carregar_modelo(self, modelo: nn.Module, caminho: str) -> nn.Module:
        """
        Carrega um modelo PyTorch.

        Args:
            modelo: Instância do modelo
            caminho: Caminho do arquivo

        Returns:
            Modelo carregado
        """
        modelo.load_state_dict(torch.load(caminho))
        modelo.eval()
        print(f"Modelo carregado de: {caminho}")
        return modelo

    def demonstracao_tensores(self) -> Dict[str, Any]:
        """
        Demonstração básica de operações com tensores PyTorch.

        Returns:
            Dicionário com exemplos de tensores
        """
        # Criação de tensores
        tensor_1d = torch.tensor([1, 2, 3, 4, 5])
        tensor_2d = torch.tensor([[1, 2], [3, 4]])
        tensor_3d = torch.randn(2, 3, 4)

        # Operações básicas
        a = torch.tensor([1, 2, 3])
        b = torch.tensor([4, 5, 6])

        soma = a + b
        produto = a * b
        produto_escalar = torch.dot(a, b)

        # Operações matriciais
        matriz_a = torch.randn(3, 2)
        matriz_b = torch.randn(2, 4)
        produto_matricial = torch.mm(matriz_a, matriz_b)

        return {
            'tensor_1d': tensor_1d,
            'tensor_2d': tensor_2d,
            'tensor_3d': tensor_3d,
            'soma': soma,
            'produto': produto,
            'produto_escalar': produto_escalar,
            'produto_matricial': produto_matricial
        }

    def demonstracao_autograd(self) -> Dict[str, Any]:
        """
        Demonstração do sistema de autograd do PyTorch.

        Returns:
            Dicionário com exemplos de autograd
        """
        # Cria tensores com requires_grad=True
        x = torch.tensor(2.0, requires_grad=True)
        y = torch.tensor(3.0, requires_grad=True)

        # Computação
        z = x**2 + y**3 + 5*x*y

        # Backward pass
        z.backward()

        # Gradientes
        grad_x = x.grad
        grad_y = y.grad

        # Exemplo mais complexo
        def funcao_complexa(x, y):
            return torch.sin(x) * torch.exp(y) + torch.cos(x*y)

        x2 = torch.tensor(1.0, requires_grad=True)
        y2 = torch.tensor(2.0, requires_grad=True)

        z2 = funcao_complexa(x2, y2)
        z2.backward()

        return {
            'funcao_simples': {
                'x': x.item(), 'y': y.item(),
                'z': z.item(),
                'dz_dx': grad_x.item(),
                'dz_dy': grad_y.item()
            },
            'funcao_complexa': {
                'x': x2.item(), 'y': y2.item(),
                'z': z2.item(),
                'dz_dx': x2.grad.item(),
                'dz_dy': y2.grad.item()
            }
        }

    def criar_rede_convolucional_simples(self) -> nn.Module:
        """
        Cria uma rede convolucional simples para demonstração.

        Returns:
            Modelo CNN simples
        """
        class CNNSimples(nn.Module):
            def __init__(self):
                super(CNNSimples, self).__init__()
                self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
                self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
                self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
                self.fc1 = nn.Linear(32 * 7 * 7, 128)
                self.fc2 = nn.Linear(128, 10)
                self.relu = nn.ReLU()

            def forward(self, x):
                x = self.pool(self.relu(self.conv1(x)))
                x = self.pool(self.relu(self.conv2(x)))
                x = x.view(-1, 32 * 7 * 7)
                x = self.relu(self.fc1(x))
                x = self.fc2(x)
                return x

        return CNNSimples()

    def demonstracao_gpu(self) -> Dict[str, Any]:
        """
        Demonstração de aceleração GPU.

        Returns:
            Informações sobre GPU e comparações de performance
        """
        info = {
            'cuda_disponivel': torch.cuda.is_available(),
            'device': str(self.device)
        }

        if torch.cuda.is_available():
            info['nome_gpu'] = torch.cuda.get_device_name(0)
            info['memoria_total'] = torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB

            # Comparação de performance CPU vs GPU
            tamanho = 10000

            # CPU
            start_time = time.time()
            a_cpu = torch.randn(tamanho, tamanho)
            b_cpu = torch.randn(tamanho, tamanho)
            c_cpu = torch.mm(a_cpu, b_cpu)
            cpu_time = time.time() - start_time

            # GPU
            start_time = time.time()
            a_gpu = torch.randn(tamanho, tamanho).cuda()
            b_gpu = torch.randn(tamanho, tamanho).cuda()
            c_gpu = torch.mm(a_gpu, b_gpu)
            gpu_time = time.time() - start_time

            info['cpu_time'] = cpu_time
            info['gpu_time'] = gpu_time
            info['speedup'] = cpu_time / gpu_time

        return info


# Função para integração com o módulo principal
def criar_utilitarios_pytorch():
    """
    Cria e retorna uma instância dos utilitários PyTorch.

    Returns:
        UtilitariosPyTorch: Instância configurada
    """
    return UtilitariosPyTorch()


# Demonstração independente
if __name__ == "__main__":
    print("🚀 Demonstração dos Utilitários PyTorch")
    print("=" * 50)

    # Cria utilitários
    utils = UtilitariosPyTorch()

    # Demonstração de tensores
    print("\n📊 Demonstração de Tensores:")
    tensores = utils.demonstracao_tensores()
    print(f"Tensor 1D: {tensores['tensor_1d']}")
    print(f"Soma: {tensores['soma']}")
    print(f"Produto escalar: {tensores['produto_escalar']}")

    # Demonstração de autograd
    print("\n🔄 Demonstração de Autograd:")
    autograd = utils.demonstracao_autograd()
    simples = autograd['funcao_simples']
    print(f"Função: z = x² + y³ + 5xy")
    print(f"Para x={simples['x']}, y={simples['y']}: z={simples['z']:.3f}")
    print(f"∂z/∂x = {simples['dz_dx']:.3f}, ∂z/∂y = {simples['dz_dy']:.3f}")

    # Demonstração de GPU
    print("\n🎮 Demonstração de GPU:")
    gpu_info = utils.demonstracao_gpu()
    print(f"CUDA disponível: {gpu_info['cuda_disponivel']}")
    if gpu_info['cuda_disponivel']:
        print(f"GPU: {gpu_info['nome_gpu']}")
        print(f"Memória: {gpu_info['memoria_total']:.1f} GB")
        print(f"Speedup GPU vs CPU: {gpu_info['speedup']:.1f}x")

    # Cria e testa uma rede neural
    print("\n🧠 Demonstração de Rede Neural:")
    rede = RedeNeuralPyTorch(input_size=2, hidden_size=10, output_size=1)
    X, y = utils.criar_dados_exemplo(100)

    print(f"Dados criados: {X.shape[0]} amostras, {X.shape[1]} features")

    # Treina a rede
    historico = utils.treinar_rede(rede, X, y, num_epocas=50)

    # Avalia
    metricas = utils.avaliar_rede(rede, X, y)
    print(f"Acurácia final: {metricas['accuracy']:.1%}")
    print(f"Perda final: {metricas['loss']:.4f}")

    print("\n✅ Demonstração concluída!")