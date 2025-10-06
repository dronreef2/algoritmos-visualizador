#!/usr/bin/env python3
"""
🧪 PYTORCH RESEARCH LAB - Módulo 5: Redes Neurais
===============================================

Laboratório colaborativo de pesquisa onde usuários podem:
- Compartilhar modelos treinados
- Competir em benchmarks
- Colaborar em projetos de pesquisa
- Explorar datasets públicos
- Publicar descobertas
"""

import streamlit as st
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import io
import base64

class ResearchLab:
    """
    Laboratório colaborativo para pesquisa em PyTorch
    """

    def __init__(self):
        self.models_db = self.load_models_database()
        self.experiments_db = self.load_experiments_database()
        self.leaderboard = self.load_leaderboard()

    def load_models_database(self) -> Dict:
        """Carrega banco de dados de modelos compartilhados"""
        if 'research_models' not in st.session_state:
            st.session_state.research_models = {
                'sample_mlp': {
                    'name': 'MLP Classificador',
                    'author': 'Sistema',
                    'description': 'Rede neural simples para classificação binária',
                    'architecture': 'MLP',
                    'dataset': 'XOR',
                    'accuracy': 0.95,
                    'parameters': 123,
                    'created_at': '2025-01-01',
                    'model_state': None  # Em produção, seria salvo em arquivo
                }
            }
        return st.session_state.research_models

    def load_experiments_database(self) -> List:
        """Carrega histórico de experimentos"""
        if 'research_experiments' not in st.session_state:
            st.session_state.research_experiments = []
        return st.session_state.research_experiments

    def load_leaderboard(self) -> List:
        """Carrega ranking de pesquisadores"""
        if 'research_leaderboard' not in st.session_state:
            st.session_state.research_leaderboard = [
                {'name': 'Sistema', 'points': 1000, 'experiments': 5, 'best_accuracy': 0.95}
            ]
        return st.session_state.research_leaderboard

    def save_experiment(self, experiment: Dict):
        """Salva experimento no banco de dados"""
        experiment['id'] = hashlib.md5(f"{experiment['author']}{experiment['timestamp']}".encode()).hexdigest()[:8]
        self.experiments_db.append(experiment)
        st.session_state.research_experiments = self.experiments_db

        # Atualiza leaderboard
        self.update_leaderboard(experiment['author'], experiment)

    def update_leaderboard(self, author: str, experiment: Dict):
        """Atualiza ranking do pesquisador"""
        # Encontra ou cria entrada do autor
        author_entry = None
        for entry in self.leaderboard:
            if entry['name'] == author:
                author_entry = entry
                break

        if not author_entry:
            author_entry = {
                'name': author,
                'points': 0,
                'experiments': 0,
                'best_accuracy': 0.0
            }
            self.leaderboard.append(author_entry)

        # Atualiza estatísticas
        author_entry['experiments'] += 1
        author_entry['points'] += experiment.get('points', 0)

        if experiment.get('accuracy', 0) > author_entry['best_accuracy']:
            author_entry['best_accuracy'] = experiment['accuracy']

        # Ordena leaderboard
        self.leaderboard.sort(key=lambda x: x['points'], reverse=True)
        st.session_state.research_leaderboard = self.leaderboard

class ExperimentRunner:
    """Executor de experimentos customizáveis"""

    def __init__(self, lab: ResearchLab):
        self.lab = lab

    def create_experiment_interface(self):
        """Interface para criação de experimentos"""

        st.markdown("### 🧪 Criar Novo Experimento")

        with st.form("experiment_form"):
            col1, col2 = st.columns(2)

            with col1:
                experiment_name = st.text_input("Nome do Experimento", "Meu Experimento")
                author_name = st.text_input("Seu Nome", "Pesquisador Anônimo")
                dataset_choice = st.selectbox("Dataset", [
                    "XOR", "Iris", "MNIST (simulado)", "Custom"
                ])

            with col2:
                model_type = st.selectbox("Tipo de Modelo", [
                    "MLP", "CNN", "RNN", "Autoencoder", "Custom"
                ])
                optimizer_choice = st.selectbox("Otimizador", [
                    "Adam", "SGD", "RMSprop"
                ])
                loss_choice = st.selectbox("Função de Loss", [
                    "MSE", "CrossEntropy", "BCE"
                ])

            # Parâmetros avançados
            st.markdown("#### ⚙️ Parâmetros Avançados")

            col3, col4, col5 = st.columns(3)

            with col3:
                learning_rate = st.slider("Learning Rate", 0.001, 0.1, 0.01)
                epochs = st.slider("Épocas", 10, 1000, 100)

            with col4:
                batch_size = st.slider("Batch Size", 1, 128, 32)
                hidden_layers = st.slider("Camadas Ocultas", 1, 5, 2)

            with col5:
                neurons_per_layer = st.slider("Neurônios/Camada", 8, 256, 64)
                dropout_rate = st.slider("Dropout", 0.0, 0.5, 0.1)

            description = st.text_area("Descrição do Experimento",
                "Experimento para testar diferentes arquiteturas de rede neural...")

            submitted = st.form_submit_button("🚀 Executar Experimento")

            if submitted:
                self.run_experiment({
                    'name': experiment_name,
                    'author': author_name,
                    'dataset': dataset_choice,
                    'model_type': model_type,
                    'optimizer': optimizer_choice,
                    'loss': loss_choice,
                    'learning_rate': learning_rate,
                    'epochs': epochs,
                    'batch_size': batch_size,
                    'hidden_layers': hidden_layers,
                    'neurons_per_layer': neurons_per_layer,
                    'dropout_rate': dropout_rate,
                    'description': description
                })

    def run_experiment(self, config: Dict):
        """Executa o experimento configurado"""

        with st.spinner("Executando experimento... 🔬"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Cria dados de exemplo baseado na escolha
            if config['dataset'] == 'XOR':
                X, y = self.create_xor_dataset()
            elif config['dataset'] == 'Iris':
                X, y = self.create_iris_dataset()
            else:
                X, y = self.create_random_dataset()

            # Cria modelo
            model = self.create_model(config)

            # Configura treinamento
            optimizer = self.create_optimizer(model, config)
            criterion = self.create_loss_function(config)

            # DataLoader
            dataset = TensorDataset(X, y)
            dataloader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=True)

            # Treinamento
            losses = []
            accuracies = []

            start_time = time.time()

            for epoch in range(config['epochs']):
                epoch_loss = 0
                correct = 0
                total = 0

                for batch_X, batch_y in dataloader:
                    optimizer.zero_grad()

                    outputs = model(batch_X)
                    loss = criterion(outputs, batch_y)
                    loss.backward()
                    optimizer.step()

                    epoch_loss += loss.item()

                    # Calcula acurácia
                    if config['loss'] in ['CrossEntropy', 'BCE']:
                        predictions = torch.argmax(outputs, dim=1)
                        correct += (predictions == batch_y).sum().item()
                    else:
                        predictions = (outputs > 0.5).float()
                        correct += (predictions == batch_y).float().sum().item()

                    total += batch_y.size(0)

                avg_loss = epoch_loss / len(dataloader)
                accuracy = correct / total

                losses.append(avg_loss)
                accuracies.append(accuracy)

                # Atualiza progresso
                progress = (epoch + 1) / config['epochs']
                progress_bar.progress(progress)
                status_text.text(".1f"
                               f"Loss: {avg_loss:.4f}")

            training_time = time.time() - start_time
            final_accuracy = accuracies[-1]

            # Salva experimento
            experiment = {
                'name': config['name'],
                'author': config['author'],
                'timestamp': datetime.now().isoformat(),
                'config': config,
                'results': {
                    'final_accuracy': final_accuracy,
                    'training_time': training_time,
                    'final_loss': losses[-1],
                    'best_accuracy': max(accuracies)
                },
                'metrics': {
                    'losses': losses,
                    'accuracies': accuracies
                },
                'points': int(final_accuracy * 1000)  # Pontuação baseada na acurácia
            }

            self.lab.save_experiment(experiment)

            # Resultados
            st.success(".1f"            st.balloons()

            # Gráficos
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📉 Curva de Loss")
                fig_loss = px.line(
                    x=list(range(len(losses))),
                    y=losses,
                    title="Evolução do Loss",
                    labels={'x': 'Época', 'y': 'Loss'}
                )
                st.plotly_chart(fig_loss)

            with col2:
                st.markdown("#### 📈 Curva de Acurácia")
                fig_acc = px.line(
                    x=list(range(len(accuracies))),
                    y=accuracies,
                    title="Evolução da Acurácia",
                    labels={'x': 'Época', 'y': 'Acurácia'}
                )
                st.plotly_chart(fig_acc)

            # Compartilhar resultado
            if st.button("📤 Compartilhar Experimento"):
                st.info("✅ Experimento compartilhado com a comunidade!")
                st.code(json.dumps(experiment, indent=2, default=str), language='json')

    def create_xor_dataset(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Cria dataset XOR"""
        X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
        y = torch.tensor([0, 1, 1, 0], dtype=torch.long)
        return X, y

    def create_iris_dataset(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Cria dataset Iris simplificado"""
        # Dados simulados do Iris
        np.random.seed(42)
        X = torch.randn(150, 4) * 2 + torch.tensor([5.1, 3.5, 1.4, 0.2])
        y = torch.randint(0, 3, (150,))
        return X, y

    def create_random_dataset(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Cria dataset aleatório"""
        X = torch.randn(1000, 10)
        y = torch.randint(0, 2, (1000,))
        return X, y

    def create_model(self, config: Dict) -> nn.Module:
        """Cria modelo baseado na configuração"""
        layers = []

        input_size = 10 if config['dataset'] == 'Custom' else 4 if config['dataset'] == 'Iris' else 2
        output_size = 3 if config['dataset'] == 'Iris' else 2

        # Input layer
        layers.append(nn.Linear(input_size, config['neurons_per_layer']))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(config['dropout_rate']))

        # Hidden layers
        for _ in range(config['hidden_layers'] - 1):
            layers.append(nn.Linear(config['neurons_per_layer'], config['neurons_per_layer']))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(config['dropout_rate']))

        # Output layer
        layers.append(nn.Linear(config['neurons_per_layer'], output_size))

        return nn.Sequential(*layers)

    def create_optimizer(self, model: nn.Module, config: Dict):
        """Cria otimizador"""
        if config['optimizer'] == 'Adam':
            return optim.Adam(model.parameters(), lr=config['learning_rate'])
        elif config['optimizer'] == 'SGD':
            return optim.SGD(model.parameters(), lr=config['learning_rate'])
        elif config['optimizer'] == 'RMSprop':
            return optim.RMSprop(model.parameters(), lr=config['learning_rate'])

    def create_loss_function(self, config: Dict):
        """Cria função de loss"""
        if config['loss'] == 'MSE':
            return nn.MSELoss()
        elif config['loss'] == 'CrossEntropy':
            return nn.CrossEntropyLoss()
        elif config['loss'] == 'BCE':
            return nn.BCELoss()

class ResearchDashboard:
    """Dashboard para visualizar pesquisa colaborativa"""

    def __init__(self, lab: ResearchLab):
        self.lab = lab

    def display_leaderboard(self):
        """Exibe ranking de pesquisadores"""
        st.markdown("### 🏆 Leaderboard de Pesquisadores")

        if self.lab.leaderboard:
            leaderboard_df = pd.DataFrame(self.lab.leaderboard)

            # Adiciona medalhas
            medals = {0: '🥇', 1: '🥈', 2: '🥉'}
            leaderboard_df['Posição'] = leaderboard_df.index.map(lambda x: medals.get(x, f'#{x+1}'))

            st.dataframe(
                leaderboard_df[['Posição', 'name', 'points', 'experiments', 'best_accuracy']],
                column_config={
                    'name': 'Pesquisador',
                    'points': st.column_config.NumberColumn('Pontos', format='%d'),
                    'experiments': 'Experimentos',
                    'best_accuracy': st.column_config.NumberColumn('Melhor Acurácia', format='%.1%')
                },
                hide_index=True
            )
        else:
            st.info("Nenhum pesquisador ainda! Seja o primeiro!")

    def display_recent_experiments(self):
        """Exibe experimentos recentes"""
        st.markdown("### 🧪 Experimentos Recentes")

        if self.lab.experiments_db:
            recent_experiments = self.lab.experiments_db[-10:]  # Últimos 10

            for exp in reversed(recent_experiments):
                with st.expander(f"🧪 {exp['name']} - {exp['author']}"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Acurácia", f"{exp['results']['final_accuracy']:.1%}")
                        st.metric("Pontos", exp.get('points', 0))

                    with col2:
                        st.metric("Tempo", f"{exp['results']['training_time']:.1f}s")
                        st.metric("Épocas", exp['config']['epochs'])

                    with col3:
                        st.metric("Dataset", exp['config']['dataset'])
                        st.metric("Modelo", exp['config']['model_type'])

                    # Gráfico rápido
                    if 'metrics' in exp and 'accuracies' in exp['metrics']:
                        fig = px.line(
                            x=list(range(len(exp['metrics']['accuracies']))),
                            y=exp['metrics']['accuracies'],
                            title="Curva de Acurácia"
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum experimento ainda! Crie o primeiro!")

def main():
    st.markdown("# 🧪 PyTorch Research Lab")
    st.markdown("Laboratório colaborativo para pesquisa em aprendizado de máquina!")

    lab = ResearchLab()
    runner = ExperimentRunner(lab)
    dashboard = ResearchDashboard(lab)

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧪 Experimentos",
        "🏆 Leaderboard",
        "📊 Dashboard",
        "🤝 Colaboração"
    ])

    with tab1:
        runner.create_experiment_interface()

    with tab2:
        dashboard.display_leaderboard()

    with tab3:
        dashboard.display_recent_experiments()

    with tab4:
        st.markdown("### 🤝 Colaboração")
        st.markdown("""
        **Como colaborar:**

        1. **📤 Compartilhe seus experimentos** - Todos os experimentos são automaticamente compartilhados
        2. **👥 Trabalhe em equipe** - Convide colegas para participar dos mesmos experimentos
        3. **📝 Publique descobertas** - Documente suas descobertas e insights
        4. **🏆 Compita no leaderboard** - Suba no ranking com melhores resultados
        5. **💡 Inspire outros** - Veja experimentos de outros pesquisadores

        **Próximas funcionalidades:**
        - 💬 Sistema de comentários em experimentos
        - 👥 Times de pesquisa colaborativos
        - 📊 Comparação de experimentos
        - 🎯 Desafios da comunidade
        - 📈 Métricas avançadas de pesquisa
        """)

        # Estatísticas da comunidade
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Pesquisadores", len(lab.leaderboard))

        with col2:
            st.metric("Experimentos", len(lab.experiments_db))

        with col3:
            total_points = sum(p['points'] for p in lab.leaderboard)
            st.metric("Pontos Totais", f"{total_points:,}")

        with col4:
            if lab.experiments_db:
                avg_accuracy = np.mean([e['results']['final_accuracy'] for e in lab.experiments_db])
                st.metric("Acurácia Média", f"{avg_accuracy:.1%}")
            else:
                st.metric("Acurácia Média", "0%")

if __name__ == "__main__":
    main()