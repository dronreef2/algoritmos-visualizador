#!/usr/bin/env python3
"""
🏆 NEURAL GLOBAL COMPETITIONS - Módulo 5: Redes Neurais
====================================================

Sistema de competições globais para otimização de arquiteturas neurais.
Desafie programadores do mundo todo em torneios de otimização neural!
"""

import streamlit as st
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import time
import random
from typing import Dict, List, Optional, Any, Tuple
import io
import base64
import json
import hashlib
import datetime
from dataclasses import dataclass, asdict
import uuid

@dataclass
class CompetitionResult:
    """Resultado de uma submissão na competição"""
    participant_id: str
    participant_name: str
    architecture: Dict[str, Any]
    score: float
    accuracy: float
    loss: float
    params_count: int
    training_time: float
    submitted_at: datetime.datetime
    competition_id: str

@dataclass
class Competition:
    """Definição de uma competição"""
    id: str
    name: str
    description: str
    dataset: str
    metric: str  # 'accuracy', 'loss', 'f1', etc.
    max_params: int
    time_limit: int  # segundos
    start_date: datetime.datetime
    end_date: datetime.datetime
    status: str  # 'upcoming', 'active', 'finished'
    leaderboard: List[CompetitionResult]

class NeuralCompetitionSystem:
    """
    Sistema de competições globais para otimização neural
    """

    def __init__(self):
        self.competitions = {}
        self.participants = {}
        self.results_history = []

        # Inicializa competições de exemplo
        self._initialize_competitions()

    def _initialize_competitions(self):
        """Inicializa competições de exemplo"""

        now = datetime.datetime.now()

        competitions_data = [
            {
                'id': 'mnist-speedrun',
                'name': '🏃‍♂️ MNIST Speedrun',
                'description': 'Crie a rede neural mais rápida para classificar dígitos MNIST. Menor tempo de treinamento com acurácia > 95%!',
                'dataset': 'MNIST',
                'metric': 'speed',
                'max_params': 50000,
                'time_limit': 300,  # 5 minutos
                'start_date': now,
                'end_date': now + datetime.timedelta(days=7),
                'status': 'active'
            },
            {
                'id': 'cifar-efficiency',
                'name': '⚡ CIFAR-10 Efficiency Challenge',
                'description': 'Otimize para máxima acurácia com mínimo parâmetros. Menos de 100k parâmetros, acurácia máxima!',
                'dataset': 'CIFAR-10',
                'metric': 'efficiency',
                'max_params': 100000,
                'time_limit': 600,  # 10 minutos
                'start_date': now,
                'end_date': now + datetime.timedelta(days=14),
                'status': 'active'
            },
            {
                'id': 'regression-master',
                'name': '🎯 Regression Master',
                'description': 'Predição perfeita de funções complexas. MSE mínimo com arquitetura criativa!',
                'dataset': 'Synthetic Regression',
                'metric': 'accuracy',
                'max_params': 100000,
                'time_limit': 180,  # 3 minutos
                'start_date': now,
                'end_date': now + datetime.timedelta(days=10),
                'status': 'active'
            },
            {
                'id': 'architecture-innovation',
                'name': '🚀 Architecture Innovation',
                'description': 'Crie a arquitetura mais inovadora. Pontuação baseada em criatividade e performance!',
                'dataset': 'Mixed',
                'metric': 'innovation',
                'max_params': 200000,
                'time_limit': 900,  # 15 minutos
                'start_date': now + datetime.timedelta(days=1),
                'end_date': now + datetime.timedelta(days=21),
                'status': 'upcoming'
            }
        ]

        for comp_data in competitions_data:
            competition = Competition(
                id=comp_data['id'],
                name=comp_data['name'],
                description=comp_data['description'],
                dataset=comp_data['dataset'],
                metric=comp_data['metric'],
                max_params=comp_data['max_params'],
                time_limit=comp_data['time_limit'],
                start_date=comp_data['start_date'],
                end_date=comp_data['end_date'],
                status=comp_data['status'],
                leaderboard=[]
            )
            self.competitions[comp_data['id']] = competition

    def create_competition(self, name: str, description: str, config: Dict) -> str:
        """Cria uma nova competição"""
        comp_id = str(uuid.uuid4())[:8]

        competition = Competition(
            id=comp_id,
            name=name,
            description=description,
            dataset=config.get('dataset', 'Custom'),
            metric=config.get('metric', 'accuracy'),
            max_params=config.get('max_params', 100000),
            time_limit=config.get('time_limit', 300),
            start_date=config.get('start_date', datetime.datetime.now()),
            end_date=config.get('end_date', datetime.datetime.now() + datetime.timedelta(days=7)),
            status='upcoming',
            leaderboard=[]
        )

        self.competitions[comp_id] = competition
        return comp_id

    def submit_solution(self, competition_id: str, participant_name: str,
                       architecture: nn.Module, training_config: Dict) -> CompetitionResult:
        """Submete uma solução para competição"""

        if competition_id not in self.competitions:
            raise ValueError(f"Competição {competition_id} não existe")

        competition = self.competitions[competition_id]

        # Verifica limites
        params_count = sum(p.numel() for p in architecture.parameters())
        if params_count > competition.max_params:
            raise ValueError(f"Arquitetura excede limite de {competition.max_params} parâmetros")

        # Gera ID único para participante
        participant_id = hashlib.md5(f"{participant_name}{competition_id}".encode()).hexdigest()[:8]

        # Treina e avalia a arquitetura
        start_time = time.time()

        try:
            metrics = self._evaluate_architecture(
                architecture,
                competition.dataset,
                training_config,
                competition.time_limit
            )
        except Exception as e:
            raise ValueError(f"Erro na avaliação: {e}")

        training_time = time.time() - start_time

        # Calcula score baseado na métrica da competição
        score = self._calculate_score(competition, metrics, params_count, training_time)

        # Cria resultado
        result = CompetitionResult(
            participant_id=participant_id,
            participant_name=participant_name,
            architecture=self._serialize_architecture(architecture),
            score=score,
            accuracy=metrics.get('accuracy', 0),
            loss=metrics.get('loss', float('inf')),
            params_count=params_count,
            training_time=training_time,
            submitted_at=datetime.datetime.now(),
            competition_id=competition_id
        )

        # Adiciona ao leaderboard
        competition.leaderboard.append(result)
        competition.leaderboard.sort(key=lambda x: x.score, reverse=True)

        # Mantém apenas top 100
        competition.leaderboard = competition.leaderboard[:100]

        # Registra no histórico
        self.results_history.append(result)

        return result

    def _evaluate_architecture(self, model: nn.Module, dataset: str,
                              training_config: Dict, time_limit: int) -> Dict:
        """Avalia uma arquitetura neural"""

        # Dados de exemplo baseados no dataset
        if dataset == 'MNIST':
            input_size, output_size = 784, 10
            X, y = self._generate_mnist_like_data(1000)
        elif dataset == 'CIFAR-10':
            input_size, output_size = 3072, 10
            X, y = self._generate_cifar_like_data(1000)
        else:  # Regression ou outros
            input_size, output_size = 10, 1
            X, y = self._generate_regression_data(1000)

        # Configuração de treinamento
        epochs = training_config.get('epochs', 10)
        lr = training_config.get('lr', 0.01)
        batch_size = training_config.get('batch_size', 32)

        # Treinamento com limite de tempo
        start_time = time.time()

        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss() if output_size > 1 else nn.MSELoss()

        best_accuracy = 0
        best_loss = float('inf')

        for epoch in range(epochs):
            if time.time() - start_time > time_limit:
                break

            # Treino
            model.train()
            for i in range(0, len(X), batch_size):
                batch_X = X[i:i+batch_size]
                batch_y = y[i:i+batch_size]

                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()

            # Avaliação
            model.eval()
            with torch.no_grad():
                outputs = model(X)
                loss = criterion(outputs, y).item()

                if output_size > 1:
                    # Classificação
                    predictions = torch.argmax(outputs, dim=1)
                    accuracy = (predictions == y).float().mean().item()
                else:
                    # Regressão - usa erro relativo
                    accuracy = 1 - torch.abs(outputs - y).mean().item()

                best_accuracy = max(best_accuracy, accuracy)
                best_loss = min(best_loss, loss)

        return {
            'accuracy': best_accuracy,
            'loss': best_loss,
            'epochs_completed': epoch + 1
        }

    def _calculate_score(self, competition: Competition, metrics: Dict,
                        params_count: int, training_time: float) -> float:
        """Calcula score baseado na métrica da competição"""

        if competition.metric == 'accuracy':
            base_score = metrics['accuracy'] * 1000
        elif competition.metric == 'speed':
            # Score baseado em acurácia e velocidade
            accuracy_score = metrics['accuracy'] * 1000
            time_penalty = max(0, training_time - 60) * 10  # Penalidade por tempo extra
            base_score = accuracy_score - time_penalty
        elif competition.metric == 'efficiency':
            # Score baseado em acurácia e eficiência paramétrica
            accuracy_score = metrics['accuracy'] * 1000
            efficiency_bonus = (competition.max_params - params_count) / competition.max_params * 500
            base_score = accuracy_score + efficiency_bonus
        elif competition.metric == 'innovation':
            # Score baseado em criatividade (simulado)
            base_score = metrics['accuracy'] * 1000 + random.uniform(-100, 100)
        else:
            base_score = metrics['accuracy'] * 1000

        return max(0, base_score)

    def _serialize_architecture(self, model: nn.Module) -> Dict:
        """Serializa arquitetura para armazenamento"""
        architecture = {
            'layers': [],
            'total_params': sum(p.numel() for p in model.parameters())
        }

        for name, module in model.named_modules():
            if isinstance(module, (nn.Linear, nn.Conv2d, nn.LSTM)):
                layer_info = {
                    'type': type(module).__name__,
                    'name': name,
                    'params': sum(p.numel() for p in module.parameters())
                }

                # Adiciona parâmetros específicos
                if hasattr(module, 'in_features'):
                    layer_info['in_features'] = module.in_features
                if hasattr(module, 'out_features'):
                    layer_info['out_features'] = module.out_features

                architecture['layers'].append(layer_info)

        return architecture

    def _generate_mnist_like_data(self, n_samples: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Gera dados similares ao MNIST"""
        X = torch.randn(n_samples, 784)
        y = torch.randint(0, 10, (n_samples,))
        return X, y

    def _generate_cifar_like_data(self, n_samples: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Gera dados similares ao CIFAR-10"""
        X = torch.randn(n_samples, 3072)
        y = torch.randint(0, 10, (n_samples,))
        return X, y

    def _generate_regression_data(self, n_samples: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Gera dados de regressão sintéticos"""
        X = torch.randn(n_samples, 10)
        # Função alvo complexa
        y = (X[:, 0] * X[:, 1] + torch.sin(X[:, 2]) + X[:, 3]**2).unsqueeze(1)
        return X, y

class CompetitionDashboard:
    """Dashboard interativo para competições"""

    def __init__(self, competition_system: NeuralCompetitionSystem):
        self.system = competition_system

    def display_competition_overview(self):
        """Exibe visão geral das competições"""

        st.markdown("### 🏆 Competições Ativas")

        active_competitions = [
            comp for comp in self.system.competitions.values()
            if comp.status == 'active'
        ]

        if not active_competitions:
            st.info("Nenhuma competição ativa no momento.")
            return

        for comp in active_competitions:
            with st.expander(f"🏆 {comp.name}", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Participantes", len(comp.leaderboard))
                    st.metric("Dataset", comp.dataset)

                with col2:
                    st.metric("Métrica", comp.metric.title())
                    st.metric("Limite Parâmetros", f"{comp.max_params:,}")

                with col3:
                    time_left = comp.end_date - datetime.datetime.now()
                    st.metric("Tempo Restante", f"{time_left.days}d {time_left.seconds//3600}h")
                    st.metric("Limite Tempo", f"{comp.time_limit}s")

                st.markdown(f"*{comp.description}*")

                if comp.leaderboard:
                    st.markdown("#### 🥇 Top 3")
                    for i, result in enumerate(comp.leaderboard[:3]):
                        medal = ["🥇", "🥈", "🥉"][i]
                        st.write(f"{medal} **{result.participant_name}** - Score: {result.score:.1f}")

    def display_leaderboard(self, competition_id: str):
        """Exibe leaderboard detalhado"""

        if competition_id not in self.system.competitions:
            st.error("Competição não encontrada")
            return

        competition = self.system.competitions[competition_id]

        st.markdown(f"## 🏆 Leaderboard: {competition.name}")

        if not competition.leaderboard:
            st.info("Nenhum participante ainda.")
            return

        # Converte para DataFrame para exibição
        leaderboard_data = []
        for result in competition.leaderboard:
            leaderboard_data.append({
                'Posição': len(leaderboard_data) + 1,
                'Participante': result.participant_name,
                'Score': ".1f",
                'Acurácia': ".1%",
                'Loss': ".4f",
                'Parâmetros': f"{result.params_count:,}",
                'Tempo': ".1f",
                'Submetido': result.submitted_at.strftime("%Y-%m-%d %H:%M")
            })

        df = pd.DataFrame(leaderboard_data)
        st.dataframe(df, use_container_width=True)

        # Gráfico de distribuição de scores
        fig = px.histogram(
            leaderboard_data,
            x='Score',
            title='Distribuição de Scores',
            nbins=20
        )
        st.plotly_chart(fig)

    def display_submission_interface(self):
        """Interface para submissão de soluções"""

        st.markdown("### 🚀 Submeter Solução")

        # Seleção de competição
        active_competitions = [
            (comp.id, comp.name) for comp in self.system.competitions.values()
            if comp.status == 'active'
        ]

        if not active_competitions:
            st.warning("Nenhuma competição ativa para submissão.")
            return

        selected_comp = st.selectbox(
            "Escolha a competição:",
            options=[comp[0] for comp in active_competitions],
            format_func=lambda x: dict(active_competitions)[x]
        )

        competition = self.system.competitions[selected_comp]

        # Informações da competição
        st.markdown(f"**Dataset:** {competition.dataset}")
        st.markdown(f"**Métrica:** {competition.metric}")
        st.markdown(f"**Limite de Parâmetros:** {competition.max_params:,}")
        st.markdown(f"**Limite de Tempo:** {competition.time_limit}s")

        # Interface de criação de arquitetura
        st.markdown("#### 🧠 Defina sua Arquitetura")

        col1, col2 = st.columns(2)

        with col1:
            num_layers = st.slider("Número de Camadas", 1, 5, 2, key="comp_num_layers")
            hidden_size = st.slider("Tamanho Camadas Ocultas", 10, 200, 50, key="comp_hidden_size")

        with col2:
            use_dropout = st.checkbox("Usar Dropout", key="comp_use_dropout")
            dropout_rate = st.slider("Taxa Dropout", 0.1, 0.5, 0.2, key="comp_dropout_rate") if use_dropout else 0.0

        # Configuração de treinamento
        st.markdown("#### 🎯 Configuração de Treinamento")

        col3, col4 = st.columns(2)

        with col3:
            epochs = st.slider("Épocas", 5, 50, 20, key="comp_epochs")
            lr = st.slider("Learning Rate", 0.001, 0.1, 0.01, format="%.4f", key="comp_lr")

        with col4:
            batch_size = st.slider("Batch Size", 16, 128, 32, key="comp_batch_size")
            participant_name = st.text_input("Seu Nome", "Anônimo", key="comp_participant_name")

        # Cria arquitetura baseada nas configurações
        if st.button("🚀 Criar e Submeter Arquitetura", type="primary"):
            try:
                # Cria modelo
                layers = []
                input_size = 784 if competition.dataset == 'MNIST' else 10
                output_size = 10 if 'MNIST' in competition.dataset or 'CIFAR' in competition.dataset else 1

                # Camada de entrada
                layers.append(nn.Linear(input_size, hidden_size))
                layers.append(nn.ReLU())

                # Camadas ocultas
                for _ in range(num_layers - 1):
                    layers.append(nn.Linear(hidden_size, hidden_size))
                    layers.append(nn.ReLU())
                    if use_dropout:
                        layers.append(nn.Dropout(dropout_rate))

                # Camada de saída
                layers.append(nn.Linear(hidden_size, output_size))

                model = nn.Sequential(*layers)

                # Configuração de treinamento
                training_config = {
                    'epochs': epochs,
                    'lr': lr,
                    'batch_size': batch_size
                }

                # Submete solução
                with st.spinner("🎯 Avaliando sua arquitetura..."):
                    result = self.system.submit_solution(
                        selected_comp,
                        participant_name,
                        model,
                        training_config
                    )

                st.success("🎉 Solução submetida com sucesso!")

                # Exibe resultado
                st.markdown("#### 📊 Seu Resultado")
                col5, col6, col7 = st.columns(3)

                with col5:
                    st.metric("Score Final", ".1f")
                    st.metric("Posição", f"#{self._get_position(result, competition.leaderboard)}")

                with col6:
                    st.metric("Acurácia", ".1%")
                    st.metric("Loss", ".4f")

                with col7:
                    st.metric("Parâmetros", f"{result.params_count:,}")
                    st.metric("Tempo", ".1f")

            except Exception as e:
                st.error(f"Erro na submissão: {e}")

    def _get_position(self, result: CompetitionResult, leaderboard: List[CompetitionResult]) -> int:
        """Obtém posição do resultado no leaderboard"""
        for i, r in enumerate(leaderboard):
            if r.participant_id == result.participant_id:
                return i + 1
        return len(leaderboard) + 1

def main():
    st.markdown("# 🏆 Neural Global Competitions")
    st.markdown("Desafie programadores do mundo todo em torneios de otimização neural! 🌍⚡")

    st.markdown("""
    ## 🏆 O que são Competições Neurais?

    **Competições Neurais Globais** são torneios onde programadores competem para criar as melhores arquiteturas neurais:

    - 🏃‍♂️ **Speedrun**: Menor tempo de treinamento com alta acurácia
    - ⚡ **Efficiency**: Máxima performance com mínimo parâmetros
    - 🎯 **Accuracy**: Precisão perfeita em tarefas complexas
    - 🚀 **Innovation**: Arquiteturas mais criativas e inovadoras

    **Objetivo:** Democratizar a pesquisa em ML através da competição global! 🏆
    """)

    # Inicializa sistema
    competition_system = NeuralCompetitionSystem()
    dashboard = CompetitionDashboard(competition_system)

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Competições Ativas",
        "📊 Leaderboards",
        "🚀 Submeter Solução",
        "📚 Regras e Tutoriais"
    ])

    with tab1:
        dashboard.display_competition_overview()

    with tab2:
        # Seleção de competição para leaderboard
        competition_options = list(competition_system.competitions.keys())
        selected_comp = st.selectbox(
            "Escolha uma competição:",
            options=competition_options,
            format_func=lambda x: competition_system.competitions[x].name
        )

        dashboard.display_leaderboard(selected_comp)

    with tab3:
        dashboard.display_submission_interface()

    with tab4:
        st.markdown("### 📚 Regras e Tutoriais")

        st.markdown("""
        #### 🏆 Regras Gerais

        **1. Limites Técnicos**
        - Respeite o limite máximo de parâmetros
        - Não exceda o tempo limite de treinamento
        - Use apenas PyTorch e bibliotecas permitidas

        **2. Fair Play**
        - Cada participante pode submeter múltiplas soluções
        - Não é permitido usar dados de teste para treinamento
        - Compartilhar código é incentivado!

        **3. Pontuação**
        - Score calculado automaticamente baseado na métrica da competição
        - Desempate por tempo de submissão
        - Leaderboard atualizado em tempo real

        #### 🎯 Dicas para Vencer

        **Para Speedrun:**
        - Use otimizadores rápidos (Adam, AdamW)
        - Arquiteturas rasas mas largas
        - Learning rates altos inicialmente

        **Para Efficiency:**
        - Redes com poucos parâmetros
        - Técnicas de pruning e quantização
        - Regularização forte (dropout, weight decay)

        **Para Accuracy:**
        - Arquiteturas profundas
        - Técnicas de augmentation
        - Ensemble methods

        **Para Innovation:**
        - Arquiteturas não-convencionais
        - Conexões skip ou residuais
        - Ativações customizadas
        """)

        # Exemplo de arquitetura
        st.markdown("#### 🔧 Exemplo de Arquitetura Vencedora")

        st.code("""
# Arquitetura Eficiente para MNIST
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(64, 10)
)

# Configuração de Treinamento
training_config = {
    'epochs': 20,
    'lr': 0.001,
    'batch_size': 64
}
        """)

        # Estatísticas globais
        st.markdown("#### 🌍 Estatísticas Globais")

        total_competitions = len(competition_system.competitions)
        total_submissions = sum(len(comp.leaderboard) for comp in competition_system.competitions.values())
        total_participants = len(set(r.participant_name for comp in competition_system.competitions.values() for r in comp.leaderboard))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Competições", total_competitions)

        with col2:
            st.metric("Submissões", total_submissions)

        with col3:
            st.metric("Participantes", total_participants)

if __name__ == "__main__":
    main()