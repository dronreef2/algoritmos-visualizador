#!/usr/bin/env python3
"""
🎮 PYTORCH GAMIFICATION - Módulo 5: Redes Neurais
===============================================

Sistema de gamificação para tornar o aprendizado de PyTorch divertido e competitivo.
Transforma conceitos complexos em desafios interativos com pontuação e conquistas.
"""

import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import time
import random
from datetime import datetime
import json
from typing import Dict, List, Optional, Any, Tuple

class PyTorchGame:
    """
    Sistema de gamificação para aprendizado de PyTorch
    """

    def __init__(self):
        self.score = 0
        self.level = 1
        self.achievements = []
        self.streak = 0
        self.best_accuracy = 0.0
        self.games_played = 0

        # Carrega progresso salvo
        self.load_progress()

    def load_progress(self):
        """Carrega progresso do usuário"""
        if 'pytorch_game_progress' not in st.session_state:
            st.session_state.pytorch_game_progress = {
                'score': 0,
                'level': 1,
                'achievements': [],
                'streak': 0,
                'best_accuracy': 0.0,
                'games_played': 0
            }

        progress = st.session_state.pytorch_game_progress
        self.score = progress['score']
        self.level = progress['level']
        self.achievements = progress['achievements']
        self.streak = progress['streak']
        self.best_accuracy = progress['best_accuracy']
        self.games_played = progress['games_played']

    def save_progress(self):
        """Salva progresso do usuário"""
        st.session_state.pytorch_game_progress = {
            'score': self.score,
            'level': self.level,
            'achievements': self.achievements,
            'streak': self.streak,
            'best_accuracy': self.best_accuracy,
            'games_played': self.games_played
        }

    def add_points(self, points: int, reason: str):
        """Adiciona pontos e verifica conquistas"""
        self.score += points
        self.check_achievements(reason)

        # Atualiza nível baseado na pontuação
        new_level = min(10, self.score // 1000 + 1)
        if new_level > self.level:
            self.level = new_level
            self.add_achievement(f"🏆 Level {new_level} Unlocked!")

        self.save_progress()

    def add_achievement(self, achievement: str):
        """Adiciona nova conquista"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            st.balloons()  # 🎈 Animação de conquista!

    def check_achievements(self, action: str):
        """Verifica se o usuário desbloqueou conquistas"""
        achievements_map = {
            'tensor_created': '🎯 Tensor Master - Primeiro tensor criado!',
            'model_trained': '🧠 Neural Network Trainer - Modelo treinado!',
            'accuracy_90': '💎 Accuracy Champion - 90%+ de acurácia!',
            'speed_training': '⚡ Speed Demon - Treinamento em < 5 segundos!',
            'perfect_score': '🌟 Perfect Score - 100% de acurácia!',
            'streak_5': '🔥 Hot Streak - 5 jogos seguidos!',
            'pytorch_expert': '🎓 PyTorch Expert - Todos os desafios completados!'
        }

        if action in achievements_map:
            self.add_achievement(achievements_map[action])

    def display_game_ui(self):
        """Interface do jogo na sidebar"""
        with st.sidebar:
            st.markdown("### 🎮 PyTorch Game")

            # Pontuação e nível
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Pontuação", f"{self.score:,}")
            with col2:
                st.metric("Nível", self.level)

            # Barra de progresso para próximo nível
            progress = (self.score % 1000) / 1000
            st.progress(progress)
            st.caption(f"Progresso: {self.score % 1000}/1000 para nível {self.level + 1}")

            # Estatísticas
            st.markdown("#### 📊 Estatísticas")
            st.write(f"🎯 Melhor Acurácia: {self.best_accuracy:.1%}")
            st.write(f"🔥 Sequência: {self.streak}")
            st.write(f"🎮 Jogos: {self.games_played}")

            # Conquistas recentes
            if self.achievements:
                st.markdown("#### 🏆 Conquistas Recentes")
                for achievement in self.achievements[-3:]:  # Últimas 3
                    st.write(f"• {achievement}")

            # Botão de reset (para desenvolvimento)
            if st.button("🔄 Reset Progress", help="Apenas para desenvolvimento"):
                self.reset_progress()

    def reset_progress(self):
        """Reseta todo o progresso"""
        self.score = 0
        self.level = 1
        self.achievements = []
        self.streak = 0
        self.best_accuracy = 0.0
        self.games_played = 0
        self.save_progress()
        st.success("Progresso resetado!")

class TensorChallenge:
    """Desafio interativo de criação de tensores"""

    def __init__(self, game: PyTorchGame):
        self.game = game

    def run_challenge(self):
        st.markdown("### 🎯 Desafio: Criação de Tensores")

        st.markdown("""
        **Objetivo:** Crie tensores PyTorch com as especificações solicitadas!

        **Regras:**
        - ✅ Acerto = +100 pontos
        - ❌ Erro = Tente novamente
        - 🎯 Precisão conta!
        """)

        # Desafio aleatório
        challenge_type = random.choice([
            'scalar', 'vector', 'matrix', '3d_tensor', 'random_tensor'
        ])

        if challenge_type == 'scalar':
            st.markdown("**Desafio:** Crie um tensor escalar (0-D) com valor 42")
            user_code = st.text_area("Código PyTorch:", "torch.tensor(42)", height=100)

        elif challenge_type == 'vector':
            st.markdown("**Desafio:** Crie um vetor (1-D) com 5 elementos: [1, 2, 3, 4, 5]")
            user_code = st.text_area("Código PyTorch:", "torch.tensor([1, 2, 3, 4, 5])", height=100)

        elif challenge_type == 'matrix':
            st.markdown("**Desafio:** Crie uma matriz 2x3 com valores de 1 a 6")
            user_code = st.text_area("Código PyTorch:", "torch.tensor([[1, 2, 3], [4, 5, 6]])", height=100)

        elif challenge_type == '3d_tensor':
            st.markdown("**Desafio:** Crie um tensor 3D de shape (2, 2, 2)")
            user_code = st.text_area("Código PyTorch:", "torch.randn(2, 2, 2)", height=100)

        elif challenge_type == 'random_tensor':
            st.markdown("**Desafio:** Crie um tensor aleatório normal de shape (3, 3)")
            user_code = st.text_area("Código PyTorch:", "torch.randn(3, 3)", height=100)

        if st.button("🚀 Executar Desafio"):
            try:
                # Executa código do usuário (com segurança limitada)
                local_vars = {'torch': torch, 'np': np}
                exec(user_code, {"__builtins__": {}}, local_vars)

                # Verifica resultado
                result = local_vars.get('result', None)
                if result is None:
                    # Tenta encontrar variável criada
                    for var_name, var_value in local_vars.items():
                        if isinstance(var_value, torch.Tensor):
                            result = var_value
                            break

                if result is not None and isinstance(result, torch.Tensor):
                    # Verifica se atende aos critérios
                    success = self.validate_tensor(result, challenge_type)

                    if success:
                        st.success("🎉 Correto! +100 pontos!")
                        self.game.add_points(100, 'tensor_created')
                        self.game.games_played += 1
                        self.game.save_progress()

                        # Mostra resultado
                        st.write("**Seu tensor:**")
                        st.code(str(result))
                        st.write(f"**Shape:** {result.shape}")
                        st.write(f"**Tipo:** {result.dtype}")

                    else:
                        st.error("❌ Quase lá! Verifique as especificações.")
                        st.info("💡 Dica: Preste atenção no shape e valores solicitados.")

                else:
                    st.error("❌ Nenhum tensor encontrado. Certifique-se de criar uma variável 'result' ou usar uma expressão direta.")

            except Exception as e:
                st.error(f"❌ Erro na execução: {e}")
                st.info("💡 Verifique a sintaxe do PyTorch.")

    def validate_tensor(self, tensor: torch.Tensor, challenge_type: str) -> bool:
        """Valida se o tensor atende aos critérios do desafio"""
        if challenge_type == 'scalar':
            return tensor.numel() == 1 and tensor.item() == 42

        elif challenge_type == 'vector':
            expected = torch.tensor([1, 2, 3, 4, 5])
            return torch.equal(tensor, expected)

        elif challenge_type == 'matrix':
            expected = torch.tensor([[1, 2, 3], [4, 5, 6]])
            return torch.equal(tensor, expected)

        elif challenge_type == '3d_tensor':
            return tensor.shape == (2, 2, 2)

        elif challenge_type == 'random_tensor':
            return tensor.shape == (3, 3) and tensor.dtype == torch.float32

        return False

class NeuralNetworkTrainer:
    """Treinador interativo de redes neurais com pontuação"""

    def __init__(self, game: PyTorchGame):
        self.game = game

    def run_training_challenge(self):
        st.markdown("### 🧠 Desafio: Treine uma Rede Neural!")

        st.markdown("""
        **Objetivo:** Treine uma rede neural para atingir 90%+ de acurácia!

        **Regras:**
        - 🎯 Acurácia ≥ 90% = +500 pontos
        - 🧠 Modelo treinado = +200 pontos
        - ⚡ Treino rápido = +100 pontos bônus
        - 🔥 Sequência de vitórias conta!
        """)

        # Parâmetros configuráveis
        col1, col2, col3 = st.columns(3)

        with col1:
            learning_rate = st.slider("Taxa de Aprendizado", 0.001, 0.1, 0.01, 0.001)

        with col2:
            epochs = st.slider("Épocas", 10, 1000, 100, 10)

        with col3:
            hidden_size = st.slider("Neurônios Ocultos", 5, 50, 10, 1)

        # Dados de exemplo (XOR problem)
        X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
        y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

        if st.button("🚀 Treinar Modelo!", type="primary"):
            with st.spinner("Treinando rede neural... 🧠"):
                start_time = time.time()

                # Cria modelo
                model = nn.Sequential(
                    nn.Linear(2, hidden_size),
                    nn.ReLU(),
                    nn.Linear(hidden_size, 1),
                    nn.Sigmoid()
                )

                # Otimizador e loss
                optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
                criterion = nn.BCELoss()

                # Treinamento
                losses = []
                accuracies = []

                progress_bar = st.progress(0)
                status_text = st.empty()

                for epoch in range(epochs):
                    # Forward pass
                    outputs = model(X)
                    loss = criterion(outputs, y)

                    # Backward pass
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    # Calcula acurácia
                    predictions = (outputs > 0.5).float()
                    accuracy = (predictions == y).float().mean().item()

                    losses.append(loss.item())
                    accuracies.append(accuracy)

                    # Atualiza progresso
                    progress = (epoch + 1) / epochs
                    progress_bar.progress(progress)
                    status_text.text(".1f"
                                   f"Acurácia: {accuracy:.1%}")

                    # Pequena pausa para visualização
                    time.sleep(0.01)

                training_time = time.time() - start_time
                final_accuracy = accuracies[-1]

                # Resultados
                st.success(".1f"                st.balloons()

                # Pontuação baseada na performance
                points = 200  # Base por treinar
                if final_accuracy >= 0.9:
                    points += 300  # Bônus por alta acurácia
                    self.game.add_achievement("💎 Accuracy Champion - 90%+ de acurácia!")
                if training_time < 5:
                    points += 100  # Bônus por velocidade
                    self.game.add_achievement("⚡ Speed Demon - Treinamento rápido!")
                if final_accuracy >= 0.99:
                    points += 200  # Bônus por perfeição
                    self.game.add_achievement("🌟 Perfect Score - 100% de acurácia!")

                self.game.add_points(points, 'model_trained')
                self.game.games_played += 1

                # Atualiza melhor acurácia
                if final_accuracy > self.game.best_accuracy:
                    self.game.best_accuracy = final_accuracy

                # Sequência
                if final_accuracy >= 0.9:
                    self.game.streak += 1
                    if self.game.streak >= 5:
                        self.game.add_achievement("🔥 Hot Streak - 5 jogos seguidos!")
                else:
                    self.game.streak = 0

                self.game.save_progress()

                # Gráficos de treinamento
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 📉 Curva de Loss")
                    fig, ax = plt.subplots()
                    ax.plot(losses)
                    ax.set_xlabel('Época')
                    ax.set_ylabel('Loss')
                    ax.set_title('Evolução do Loss')
                    st.pyplot(fig)

                with col2:
                    st.markdown("#### 📈 Curva de Acurácia")
                    fig, ax = plt.subplots()
                    ax.plot(accuracies)
                    ax.set_xlabel('Época')
                    ax.set_ylabel('Acurácia')
                    ax.set_title('Evolução da Acurácia')
                    st.pyplot(fig)

def main():
    st.markdown("# 🎮 PyTorch Gamification")
    st.markdown("Aprenda PyTorch de forma divertida com desafios interativos!")

    # Inicializa jogo
    game = PyTorchGame()

    # Interface do jogo
    game.display_game_ui()

    # Abas de desafios
    tab1, tab2, tab3 = st.tabs(["🎯 Tensores", "🧠 Rede Neural", "🏆 Conquistas"])

    with tab1:
        challenge = TensorChallenge(game)
        challenge.run_challenge()

    with tab2:
        trainer = NeuralNetworkTrainer(game)
        trainer.run_training_challenge()

    with tab3:
        st.markdown("### 🏆 Suas Conquistas")

        if game.achievements:
            for achievement in game.achievements:
                st.success(achievement)
        else:
            st.info("🎯 Complete desafios para desbloquear conquistas!")

        # Estatísticas detalhadas
        st.markdown("### 📊 Estatísticas Detalhadas")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de Pontos", f"{game.score:,}")
            st.metric("Nível Atual", game.level)

        with col2:
            st.metric("Melhor Acurácia", f"{game.best_accuracy:.1%}")
            st.metric("Sequência Atual", game.streak)

        with col3:
            st.metric("Jogos Jogados", game.games_played)
            next_level_points = (game.level) * 1000
            st.metric("Pontos para Próximo Nível", f"{next_level_points - game.score}")

if __name__ == "__main__":
    main()