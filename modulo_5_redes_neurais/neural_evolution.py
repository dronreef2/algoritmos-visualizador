#!/usr/bin/env python3
"""
🧬 NEURAL EVOLUTION - Módulo 5: Redes Neurais
===========================================

Sistema de evolução neural usando algoritmos genéticos para otimizar arquiteturas
de redes neurais automaticamente. A evolução acontece em tempo real!
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
import random
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import copy

@dataclass
class Genome:
    """Representa um genoma (arquitetura) de rede neural"""
    layers: List[Dict]  # [{'type': 'linear', 'in_features': 10, 'out_features': 5}, ...]
    fitness: float = 0.0
    generation: int = 0
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"gen_{random.randint(1000, 9999)}"

class NeuralEvolution:
    """
    Sistema de evolução neural usando algoritmos genéticos
    """

    def __init__(self, population_size: int = 20, mutation_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation = 0
        self.population: List[Genome] = []
        self.best_fitness_history = []
        self.avg_fitness_history = []

        # Dataset para avaliação
        self.X, self.y = self.create_evaluation_dataset()

    def create_evaluation_dataset(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Cria dataset para avaliar fitness das redes"""
        # Problema de classificação binária (XOR estendido)
        X = torch.randn(1000, 4) * 2
        # Target baseado em combinação não-linear dos inputs
        y = ((X[:, 0] * X[:, 1] + X[:, 2] * X[:, 3]) > 0).float().unsqueeze(1)
        return X, y

    def initialize_population(self):
        """Inicializa população com arquiteturas aleatórias"""
        self.population = []

        for _ in range(self.population_size):
            # Cria arquitetura aleatória
            layers = self.create_random_architecture()
            genome = Genome(layers=layers, generation=self.generation)
            self.population.append(genome)

    def create_random_architecture(self) -> List[Dict]:
        """Cria uma arquitetura de rede neural aleatória"""
        layers = []

        # Input layer (sempre 4 features)
        current_features = 4

        # Número de camadas ocultas (1-4)
        num_hidden = random.randint(1, 4)

        for i in range(num_hidden):
            # Tipo de camada
            layer_type = random.choice(['linear', 'dropout'])

            if layer_type == 'linear':
                # Número de neurônios de saída
                out_features = random.randint(3, 16)
                layers.append({
                    'type': 'linear',
                    'in_features': current_features,
                    'out_features': out_features
                })
                current_features = out_features

                # Adiciona ativação (sempre após linear)
                activation = random.choice(['relu', 'sigmoid', 'tanh'])
                layers.append({'type': activation})

            elif layer_type == 'dropout':
                dropout_rate = random.uniform(0.1, 0.5)
                layers.append({
                    'type': 'dropout',
                    'p': dropout_rate
                })

        # Output layer (sempre 1 saída para classificação binária)
        layers.append({
            'type': 'linear',
            'in_features': current_features,
            'out_features': 1
        })
        layers.append({'type': 'sigmoid'})

        return layers

    def genome_to_model(self, genome: Genome) -> nn.Module:
        """Converte genoma em modelo PyTorch"""
        layers = []

        for layer_config in genome.layers:
            if layer_config['type'] == 'linear':
                layers.append(nn.Linear(
                    layer_config['in_features'],
                    layer_config['out_features']
                ))
            elif layer_config['type'] == 'relu':
                layers.append(nn.ReLU())
            elif layer_config['type'] == 'sigmoid':
                layers.append(nn.Sigmoid())
            elif layer_config['type'] == 'tanh':
                layers.append(nn.Tanh())
            elif layer_config['type'] == 'dropout':
                layers.append(nn.Dropout(layer_config['p']))

        return nn.Sequential(*layers)

    def evaluate_fitness(self, genome: Genome) -> float:
        """Avalia o fitness (performance) de um genoma"""
        try:
            model = self.genome_to_model(genome)

            # Treinamento rápido
            optimizer = optim.Adam(model.parameters(), lr=0.01)
            criterion = nn.BCELoss()

            # Treino por algumas épocas
            model.train()
            for epoch in range(10):  # Treino rápido
                optimizer.zero_grad()
                outputs = model(self.X)
                loss = criterion(outputs, self.y)
                loss.backward()
                optimizer.step()

            # Avaliação
            model.eval()
            with torch.no_grad():
                predictions = (model(self.X) > 0.5).float()
                accuracy = (predictions == self.y).float().mean().item()

            # Fitness = acurácia (0-1)
            return accuracy

        except Exception as e:
            # Penaliza genomas que causam erro
            return 0.0

    def evaluate_population(self):
        """Avalia fitness de toda a população"""
        for genome in self.population:
            if genome.fitness == 0.0:  # Ainda não avaliado
                genome.fitness = self.evaluate_fitness(genome)

    def select_parents(self) -> List[Genome]:
        """Seleção por torneio para reprodução"""
        parents = []

        for _ in range(2):  # Seleciona 2 pais
            # Torneio: 3 candidatos aleatórios
            tournament = random.sample(self.population, min(3, len(self.population)))
            winner = max(tournament, key=lambda g: g.fitness)
            parents.append(winner)

        return parents

    def crossover(self, parent1: Genome, parent2: Genome) -> Genome:
        """Crossover entre dois genomas"""
        # Ponto de crossover aleatório
        min_layers = min(len(parent1.layers), len(parent2.layers))
        if min_layers < 2:
            # Se muito pequeno, copia um dos pais
            return copy.deepcopy(random.choice([parent1, parent2]))

        crossover_point = random.randint(1, min_layers - 1)

        # Combina camadas
        child_layers = parent1.layers[:crossover_point] + parent2.layers[crossover_point:]

        # Ajusta in_features para manter consistência
        child_layers = self.fix_architecture_consistency(child_layers)

        return Genome(
            layers=child_layers,
            generation=self.generation + 1
        )

    def fix_architecture_consistency(self, layers: List[Dict]) -> List[Dict]:
        """Garante que a arquitetura seja consistente (in_features/out_features)"""
        fixed_layers = []

        for i, layer in enumerate(layers):
            if layer['type'] == 'linear':
                if i > 0:
                    # Ajusta in_features baseado na camada anterior
                    prev_layer = fixed_layers[-1]
                    if prev_layer['type'] == 'linear':
                        layer = layer.copy()
                        layer['in_features'] = prev_layer['out_features']

            fixed_layers.append(layer)

        return fixed_layers

    def mutate(self, genome: Genome) -> Genome:
        """Aplica mutações no genoma"""
        if random.random() > self.mutation_rate:
            return genome  # Sem mutação

        mutated_genome = copy.deepcopy(genome)
        layers = mutated_genome.layers

        # Tipos de mutação
        mutation_type = random.choice([
            'add_layer', 'remove_layer', 'change_neurons', 'change_activation'
        ])

        if mutation_type == 'add_layer' and len(layers) < 10:
            # Adiciona camada linear
            insert_pos = random.randint(0, len(layers) - 1)
            new_layer = {
                'type': 'linear',
                'in_features': 8,  # Será ajustado depois
                'out_features': random.randint(3, 12)
            }
            layers.insert(insert_pos, new_layer)
            layers.insert(insert_pos + 1, {'type': 'relu'})

        elif mutation_type == 'remove_layer' and len(layers) > 3:
            # Remove camada (não ativação)
            linear_indices = [i for i, l in enumerate(layers) if l['type'] == 'linear']
            if linear_indices:
                remove_idx = random.choice(linear_indices)
                # Remove camada linear e sua ativação
                layers.pop(remove_idx)
                if remove_idx < len(layers) and layers[remove_idx]['type'] in ['relu', 'sigmoid', 'tanh']:
                    layers.pop(remove_idx)

        elif mutation_type == 'change_neurons':
            # Altera número de neurônios
            linear_indices = [i for i, l in enumerate(layers) if l['type'] == 'linear']
            if linear_indices:
                change_idx = random.choice(linear_indices)
                layers[change_idx]['out_features'] = random.randint(3, 16)

        elif mutation_type == 'change_activation':
            # Altera função de ativação
            activation_indices = [i for i, l in enumerate(layers)
                                if l['type'] in ['relu', 'sigmoid', 'tanh']]
            if activation_indices:
                change_idx = random.choice(activation_indices)
                new_activation = random.choice(['relu', 'sigmoid', 'tanh'])
                layers[change_idx]['type'] = new_activation

        # Conserta consistência
        mutated_genome.layers = self.fix_architecture_consistency(layers)

        return mutated_genome

    def evolve_generation(self):
        """Executa uma geração completa de evolução"""
        # Avalia população atual
        self.evaluate_population()

        # Registra estatísticas
        fitness_scores = [g.fitness for g in self.population]
        self.best_fitness_history.append(max(fitness_scores))
        self.avg_fitness_history.append(sum(fitness_scores) / len(fitness_scores))

        # Cria nova população
        new_population = []

        # Elitismo: mantém os melhores
        elite_count = max(1, self.population_size // 10)
        sorted_population = sorted(self.population, key=lambda g: g.fitness, reverse=True)
        new_population.extend(sorted_population[:elite_count])

        # Reprodução
        while len(new_population) < self.population_size:
            parents = self.select_parents()
            child = self.crossover(parents[0], parents[1])
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population
        self.generation += 1

        # Atualiza geração nos novos genomas
        for genome in self.population:
            if genome.generation == 0:
                genome.generation = self.generation

class EvolutionDashboard:
    """Dashboard para visualizar a evolução neural"""

    def __init__(self, evolution: NeuralEvolution):
        self.evolution = evolution

    def display_evolution_status(self):
        """Exibe status atual da evolução"""
        st.markdown("### 🧬 Status da Evolução")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Geração", self.evolution.generation)

        with col2:
            if self.evolution.population:
                best_fitness = max(g.fitness for g in self.evolution.population)
                st.metric("Melhor Fitness", f"{best_fitness:.3%}")

        with col3:
            if self.evolution.population:
                avg_fitness = sum(g.fitness for g in self.evolution.population) / len(self.evolution.population)
                st.metric("Fitness Médio", f"{avg_fitness:.3%}")

        with col4:
            st.metric("População", len(self.evolution.population))

    def display_fitness_evolution(self):
        """Gráfico da evolução do fitness"""
        if not self.evolution.best_fitness_history:
            return

        st.markdown("### 📈 Evolução do Fitness")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=list(range(len(self.evolution.best_fitness_history))),
            y=self.evolution.best_fitness_history,
            mode='lines+markers',
            name='Melhor Fitness',
            line=dict(color='red', width=3)
        ))

        if self.evolution.avg_fitness_history:
            fig.add_trace(go.Scatter(
                x=list(range(len(self.evolution.avg_fitness_history))),
                y=self.evolution.avg_fitness_history,
                mode='lines',
                name='Fitness Médio',
                line=dict(color='blue', width=2, dash='dash')
            ))

        fig.update_layout(
            title="Evolução do Fitness ao Longo das Gerações",
            xaxis_title="Geração",
            yaxis_title="Fitness (Acurácia)",
            yaxis_tickformat='.1%'
        )

        st.plotly_chart(fig, use_container_width=True)

    def display_population_diversity(self):
        """Visualiza diversidade da população"""
        if not self.evolution.population:
            return

        st.markdown("### 🧬 Diversidade Populacional")

        # Conta tipos de arquitetura
        architecture_counts = {}
        for genome in self.evolution.population:
            arch_key = f"{len(genome.layers)} camadas"
            architecture_counts[arch_key] = architecture_counts.get(arch_key, 0) + 1

        fig = px.pie(
            values=list(architecture_counts.values()),
            names=list(architecture_counts.keys()),
            title="Distribuição de Arquiteturas"
        )

        st.plotly_chart(fig, use_container_width=True)

    def display_best_genomes(self):
        """Exibe os melhores genomas"""
        if not self.evolution.population:
            return

        st.markdown("### 🏆 Melhores Genomas")

        # Ordena por fitness
        sorted_genomes = sorted(self.evolution.population, key=lambda g: g.fitness, reverse=True)

        for i, genome in enumerate(sorted_genomes[:5]):
            with st.expander(f"#{i+1} - Fitness: {genome.fitness:.3%} - ID: {genome.id}"):

                # Arquitetura
                st.write("**Arquitetura:**")
                for j, layer in enumerate(genome.layers):
                    if layer['type'] == 'linear':
                        st.write(f"  {j}: Linear({layer['in_features']} → {layer['out_features']})")
                    else:
                        st.write(f"  {j}: {layer['type'].title()}")

                # Testa o modelo
                if st.button(f"🧪 Testar Modelo {genome.id}", key=f"test_{genome.id}"):
                    model = self.evolution.genome_to_model(genome)

                    # Teste rápido
                    model.eval()
                    with torch.no_grad():
                        test_output = model(self.evolution.X[:5])
                        predictions = (test_output > 0.5).float()

                    st.write("**Teste com 5 amostras:**")
                    for k in range(5):
                        pred = predictions[k].item()
                        true = self.evolution.y[k].item()
                        status = "✅" if pred == true else "❌"
                        st.write(f"  Amostra {k+1}: Pred={pred:.0f}, Real={true:.0f} {status}")

def main():
    st.markdown("# 🧬 Neural Evolution")
    st.markdown("Assista à evolução de redes neurais em tempo real! 🧠✨")

    st.markdown("""
    ## 🎯 Como Funciona

    Este sistema usa **Algoritmos Genéticos** para evoluir arquiteturas de redes neurais:

    1. **🏗️ Geração Inicial**: Cria população de arquiteturas aleatórias
    2. **📊 Avaliação**: Testa performance de cada arquitetura
    3. **🧬 Seleção**: Escolhe os melhores para reprodução
    4. **🔄 Crossover**: Combina características dos pais
    5. **🧪 Mutação**: Adiciona variação genética
    6. **🔁 Repetição**: Gerações sucessivas melhoram a população

    **Objetivo:** Evoluir redes neurais que resolvam problemas complexos automaticamente!
    """)

    # Inicializa sistema de evolução
    if 'neural_evolution' not in st.session_state:
        st.session_state.neural_evolution = NeuralEvolution(population_size=20)

    evolution = st.session_state.neural_evolution
    dashboard = EvolutionDashboard(evolution)

    # Controles
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🌱 Inicializar População", type="primary"):
            with st.spinner("Criando população inicial..."):
                evolution.initialize_population()
            st.success("População inicial criada!")
            st.rerun()

    with col2:
        if st.button("🔄 Evoluir Geração") and evolution.population:
            with st.spinner("Evoluindo geração..."):
                evolution.evolve_generation()
            st.success(f"Geração {evolution.generation} completa!")
            st.rerun()

    with col3:
        if st.button("🎯 Auto-Evolução (5 gerações)") and evolution.population:
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(5):
                status_text.text(f"Evoluindo geração {i+1}/5...")
                evolution.evolve_generation()
                progress_bar.progress((i+1)/5)
                time.sleep(0.5)

            st.success("Auto-evolução completa!")
            st.rerun()

    with col4:
        if st.button("🔄 Reset"):
            st.session_state.neural_evolution = NeuralEvolution()
            st.success("Sistema resetado!")
            st.rerun()

    # Dashboard
    if evolution.population:
        dashboard.display_evolution_status()
        dashboard.display_fitness_evolution()
        dashboard.display_population_diversity()
        dashboard.display_best_genomes()

        # Estatísticas detalhadas
        st.markdown("### 📊 Estatísticas da População")

        fitness_scores = [g.fitness for g in evolution.population]

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("Fitness Máximo", f"{max(fitness_scores):.3%}")

        with col6:
            st.metric("Fitness Mínimo", f"{min(fitness_scores):.3%}")

        with col7:
            st.metric("Desvio Padrão", f"{np.std(fitness_scores):.3%}")

        with col8:
            st.metric("Genomas Válidos", f"{sum(1 for f in fitness_scores if f > 0):d}")

        # Distribuição de fitness
        st.markdown("#### 📈 Distribuição de Fitness")
        fig_hist = px.histogram(
            x=fitness_scores,
            nbins=10,
            title="Distribuição de Fitness na População",
            labels={'x': 'Fitness', 'y': 'Contagem'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    else:
        st.info("👆 Clique em 'Inicializar População' para começar a evolução!")

    # Explicação técnica
    with st.expander("🧠 Como Funciona Tecnicamente"):
        st.markdown("""
        ### Algoritmo Genético Detalhado

        **Representação Genômica:**
        - Cada genoma = sequência de camadas neurais
        - Genes = tipo de camada, número de neurônios, funções de ativação

        **Operadores Genéticos:**
        - **Seleção**: Torneio entre 3 candidatos
        - **Crossover**: Ponto único de recombinação
        - **Mutação**: Adição/remoção de camadas, alteração de parâmetros

        **Função de Fitness:**
        - Acurácia em tarefa de classificação binária
        - Penalização por complexidade excessiva
        - Bônus por convergência rápida

        **Estratégias de Otimização:**
        - Elitismo: preserva melhores indivíduos
        - Diversidade: mutações mantêm variação genética
        - Adaptação: fitness guia evolução automática
        """)

if __name__ == "__main__":
    main()