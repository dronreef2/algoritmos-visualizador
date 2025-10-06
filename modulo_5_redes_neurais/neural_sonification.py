#!/usr/bin/env python3
"""
🎵 NEURAL SONIFICATION - Módulo 5: Redes Neurais
===========================================

Sistema de sonificação que transforma o treinamento de redes neurais em música.
Cada aspecto do aprendizado se torna um elemento musical audível!
"""

import streamlit as st
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import random
from typing import Dict, List, Optional, Any, Tuple
import io
import base64
import json

class NeuralSonification:
    """
    Sistema de sonificação para redes neurais
    Transforma métricas de treinamento em elementos musicais
    """

    def __init__(self):
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.octaves = [3, 4, 5, 6]  # Alcance vocal humano

        # Mapeamento de métricas para música
        self.metric_mappings = {
            'loss': self.loss_to_melody,
            'accuracy': self.accuracy_to_harmony,
            'gradient_norm': self.gradients_to_rhythm,
            'learning_rate': self.lr_to_tempo,
            'weights': self.weights_to_texture
        }

    def loss_to_melody(self, loss: float, epoch: int) -> Dict:
        """Converte loss em melodia (notas principais)"""
        # Loss alto = notas baixas e dissonantes
        # Loss baixo = notas altas e consonant

        normalized_loss = min(loss, 5.0) / 5.0  # Normaliza 0-1

        # Escala logarítmica para percepção musical
        pitch_index = int((1 - normalized_loss) * len(self.notes) * len(self.octaves))
        octave = self.octaves[min(pitch_index // len(self.notes), len(self.octaves) - 1)]
        note = self.notes[pitch_index % len(self.notes)]

        # Duração baseada na magnitude da mudança
        duration = 0.25 + (1 - normalized_loss) * 0.75  # 0.25-1.0 segundos

        # Volume baseado na estabilidade
        volume = 0.3 + (1 - normalized_loss) * 0.7

        return {
            'note': f"{note}{octave}",
            'duration': duration,
            'volume': volume,
            'type': 'melody'
        }

    def accuracy_to_harmony(self, accuracy: float, epoch: int) -> Dict:
        """Converte acurácia em harmonia (acordes)"""
        # Acurácia alta = acordes consonant
        # Acurácia baixa = dissonância

        if accuracy > 0.9:
            # Acorde maior (consonante)
            chord = ['C4', 'E4', 'G4']
        elif accuracy > 0.7:
            # Acorde menor
            chord = ['A3', 'C4', 'E4']
        elif accuracy > 0.5:
            # Acorde diminuto (tensão)
            chord = ['B3', 'D4', 'F4']
        else:
            # Cluster dissonante
            chord = ['C4', 'C#4', 'D4']

        return {
            'chord': chord,
            'duration': 1.0,
            'volume': 0.4,
            'type': 'harmony'
        }

    def gradients_to_rhythm(self, grad_norm: float, epoch: int) -> Dict:
        """Converte norma do gradiente em ritmo"""
        # Gradientes grandes = ritmo agitado
        # Gradientes pequenos = ritmo calmo

        normalized_grad = min(grad_norm, 10.0) / 10.0

        # BPM baseado na magnitude
        bpm = 60 + (1 - normalized_grad) * 120  # 60-180 BPM

        # Padrão rítmico
        if normalized_grad > 0.7:
            pattern = [0.125, 0.125, 0.125, 0.125]  # Semicolcheias (agitado)
        elif normalized_grad > 0.4:
            pattern = [0.25, 0.25, 0.25, 0.25]  # Colcheias
        else:
            pattern = [0.5, 0.5]  # Semínimas (calmo)

        return {
            'bpm': bpm,
            'pattern': pattern,
            'volume': 0.5,
            'type': 'rhythm'
        }

    def lr_to_tempo(self, lr: float, epoch: int) -> Dict:
        """Converte learning rate em andamento temporal"""
        # LR alto = andamento rápido
        # LR baixo = andamento lento

        # LR típico: 0.001-0.1, mapeia para andamento
        tempo_multiplier = 1 + (np.log10(lr) + 3) * 0.5  # 0.5-2.0x

        return {
            'tempo_multiplier': tempo_multiplier,
            'type': 'tempo'
        }

    def weights_to_texture(self, weights: torch.Tensor, epoch: int) -> Dict:
        """Converte pesos da rede em textura sonora"""
        # Estatísticas dos pesos criam timbres

        weights_flat = weights.flatten().detach().numpy()

        # Estatísticas
        mean_weight = np.mean(np.abs(weights_flat))
        std_weight = np.std(weights_flat)
        sparsity = np.mean(weights_flat == 0)

        # Mapeia para parâmetros de síntese
        # Mean -> Frequência fundamental
        fundamental_freq = 100 + mean_weight * 200  # 100-300 Hz

        # Std -> Ruído/brightness
        noise_amount = min(std_weight * 2, 1.0)

        # Sparsity -> Densidade de grãos
        grain_density = 0.1 + (1 - sparsity) * 0.9

        return {
            'fundamental_freq': fundamental_freq,
            'noise_amount': noise_amount,
            'grain_density': grain_density,
            'duration': 2.0,
            'type': 'texture'
        }

    def create_training_symphony(self, training_history: List[Dict]) -> Dict:
        """Cria uma sinfonia completa baseada no histórico de treinamento"""

        symphony = {
            'movements': [],
            'total_duration': 0,
            'key_elements': []
        }

        for epoch_data in training_history:
            movement = {
                'epoch': epoch_data['epoch'],
                'elements': []
            }

            # Melodia baseada no loss
            if 'loss' in epoch_data:
                melody = self.loss_to_melody(epoch_data['loss'], epoch_data['epoch'])
                movement['elements'].append(melody)

            # Harmonia baseada na acurácia
            if 'accuracy' in epoch_data:
                harmony = self.accuracy_to_harmony(epoch_data['accuracy'], epoch_data['epoch'])
                movement['elements'].append(harmony)

            # Ritmo baseado nos gradientes
            if 'grad_norm' in epoch_data:
                rhythm = self.gradients_to_rhythm(epoch_data['grad_norm'], epoch_data['epoch'])
                movement['elements'].append(rhythm)

            # Tempo baseado no learning rate
            if 'lr' in epoch_data:
                tempo = self.lr_to_tempo(epoch_data['lr'], epoch_data['epoch'])
                movement['elements'].append(tempo)

            symphony['movements'].append(movement)

        symphony['total_duration'] = len(symphony['movements']) * 2.0  # ~2s por epoch
        return symphony

class MusicalTrainingSession:
    """Sessão de treinamento com sonificação em tempo real"""

    def __init__(self):
        self.sonification = NeuralSonification()
        self.training_history = []

    def create_sample_training_data(self) -> List[Dict]:
        """Cria dados de treinamento simulados para demonstração"""
        history = []

        for epoch in range(50):
            # Simula melhoria progressiva
            progress = epoch / 49.0

            # Loss diminui exponencialmente
            loss = 2.0 * np.exp(-progress * 3) + random.uniform(0, 0.2)

            # Acurácia aumenta logisticamente
            accuracy = 1 / (1 + np.exp(-6 * (progress - 0.3))) + random.uniform(-0.05, 0.05)
            accuracy = min(max(accuracy, 0.1), 0.95)

            # Gradientes diminuem com o treinamento
            grad_norm = 1.0 * np.exp(-progress * 2) + random.uniform(0, 0.1)

            # Learning rate com decaimento
            lr = 0.01 * (0.95 ** epoch)

            history.append({
                'epoch': epoch,
                'loss': loss,
                'accuracy': accuracy,
                'grad_norm': grad_norm,
                'lr': lr
            })

        return history

    def train_with_sonification(self, model: nn.Module, train_data: Tuple[torch.Tensor, torch.Tensor],
                               epochs: int = 20, lr: float = 0.01):
        """Treina modelo com sonificação em tempo real"""

        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.MSELoss()

        X_train, y_train = train_data

        progress_bar = st.progress(0)
        status_text = st.empty()
        music_display = st.empty()

        training_history = []

        for epoch in range(epochs):
            # Forward pass
            model.train()
            outputs = model(X_train)
            loss = criterion(outputs, y_train)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()

            # Calcula norma do gradiente
            total_norm = 0
            for p in model.parameters():
                if p.grad is not None:
                    param_norm = p.grad.data.norm(2)
                    total_norm += param_norm.item() ** 2
            grad_norm = total_norm ** (1. / 2)

            optimizer.step()

            # Calcula acurácia (aproximada para regressão)
            with torch.no_grad():
                predictions = outputs
                accuracy = (1 - torch.abs(predictions - y_train).mean().item())

            # Registra métricas
            epoch_data = {
                'epoch': epoch,
                'loss': loss.item(),
                'accuracy': accuracy,
                'grad_norm': grad_norm,
                'lr': lr
            }
            training_history.append(epoch_data)

            # Sonificação em tempo real
            symphony = self.sonification.create_training_symphony([epoch_data])

            # Exibe "música" como emoji e descrição
            music_description = self.epoch_to_music_description(epoch_data)
            music_display.code(music_description, language="text")

            # Atualiza progresso
            progress = (epoch + 1) / epochs
            progress_bar.progress(progress)
            status_text.text(".1f"
                           f"Grad: {grad_norm:.3f}")

            time.sleep(0.1)  # Pausa para visualização

        return training_history

    def epoch_to_music_description(self, epoch_data: Dict) -> str:
        """Converte dados da epoch em descrição musical"""

        loss = epoch_data['loss']
        accuracy = epoch_data['accuracy']
        grad_norm = epoch_data['grad_norm']

        # Melodia baseada no loss
        if loss > 1.0:
            melody_desc = "🎵 Notas graves e dissonantes"
        elif loss > 0.5:
            melody_desc = "🎶 Melodia média, em desenvolvimento"
        else:
            melody_desc = "🎼 Melodia alta e fluida"

        # Harmonia baseada na acurácia
        if accuracy > 0.8:
            harmony_desc = "🎹 Acordes consonant, harmoniosos"
        elif accuracy > 0.6:
            harmony_desc = "🎺 Harmonia em progresso"
        else:
            harmony_desc = "🎷 Dissonância, tensão musical"

        # Ritmo baseado nos gradientes
        if grad_norm > 1.0:
            rhythm_desc = "🥁 Ritmo agitado, intenso"
        elif grad_norm > 0.5:
            rhythm_desc = "🪘 Ritmo moderado"
        else:
            rhythm_desc = "🎵 Ritmo calmo, estável"

        return f"""
🎼 Sinfonia da Época {epoch_data['epoch']}

🎵 Melodia: {melody_desc}
🎹 Harmonia: {harmony_desc}
🥁 Ritmo: {rhythm_desc}

📊 Loss: {loss:.3f} | Acurácia: {accuracy:.1%} | Grad: {grad_norm:.3f}
        """.strip()

class MusicVisualizer:
    """Visualizador da música gerada pelo treinamento"""

    def __init__(self, sonification: NeuralSonification):
        self.sonification = sonification

    def create_music_score_visualization(self, training_history: List[Dict]):
        """Cria visualização de partitura musical"""

        st.markdown("### 🎼 Partitura Neural")

        # Converte histórico em elementos musicais
        musical_elements = []

        for epoch_data in training_history:
            elements = []

            if 'loss' in epoch_data:
                elements.append(self.sonification.loss_to_melody(
                    epoch_data['loss'], epoch_data['epoch']))

            if 'accuracy' in epoch_data:
                elements.append(self.sonification.accuracy_to_harmony(
                    epoch_data['accuracy'], epoch_data['epoch']))

            if 'grad_norm' in epoch_data:
                elements.append(self.sonification.gradients_to_rhythm(
                    epoch_data['grad_norm'], epoch_data['epoch']))

            musical_elements.append({
                'epoch': epoch_data['epoch'],
                'elements': elements
            })

        # Visualização da partitura
        fig = go.Figure()

        # Eixo X: Épocas (tempo)
        # Eixo Y: Altura das notas (frequência)

        for element_set in musical_elements:
            epoch = element_set['epoch']

            for element in element_set['elements']:
                if element['type'] == 'melody':
                    # Converte nota para frequência aproximada
                    freq = self.note_to_frequency(element['note'])
                    fig.add_trace(go.Scatter(
                        x=[epoch],
                        y=[freq],
                        mode='markers',
                        marker=dict(
                            size=element['volume'] * 50,
                            color='blue',
                            symbol='circle'
                        ),
                        name=f"Melody (Epoch {epoch})",
                        showlegend=False
                    ))

                elif element['type'] == 'harmony':
                    # Mostra acordes como pontos conectados
                    for i, note in enumerate(element['chord']):
                        freq = self.note_to_frequency(note)
                        fig.add_trace(go.Scatter(
                            x=[epoch],
                            y=[freq],
                            mode='markers',
                            marker=dict(
                                size=20,
                                color='green',
                                symbol='diamond'
                            ),
                            name=f"Harmony {i+1} (Epoch {epoch})",
                            showlegend=False
                        ))

        fig.update_layout(
            title="🎼 Partitura Neural - Transformação de Métricas em Música",
            xaxis_title="Época de Treinamento",
            yaxis_title="Frequência (Hz)",
            yaxis_type="log",
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    def note_to_frequency(self, note: str) -> float:
        """Converte nota musical para frequência em Hz"""
        # Notas e suas frequências (A4 = 440Hz)
        note_freqs = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }

        if len(note) == 2:
            note_name, octave = note[0], int(note[1])
        else:
            note_name, octave = note[0], 4  # Default

        base_freq = note_freqs.get(note_name, 440.0)

        # Ajusta por oitava (A4 = 440Hz)
        octave_adjust = octave - 4
        return base_freq * (2 ** octave_adjust)

def main():
    st.markdown("# 🎵 Neural Sonification")
    st.markdown("Transforme o treinamento de redes neurais em música! 🎼🎶")

    st.markdown("""
    ## 🎼 O que é Sonificação?

    **Sonificação** é a transformação de dados em som. Neste sistema:

    - 📉 **Loss** → **Melodia**: Loss alto = notas graves/dissonantes
    - 🎯 **Acurácia** → **Harmonia**: Acurácia alta = acordes consonant
    - ⚡ **Gradientes** → **Ritmo**: Gradientes grandes = ritmo agitado
    - 📈 **Learning Rate** → **Tempo**: LR alto = andamento rápido
    - 🧠 **Pesos** → **Textura**: Estatísticas dos pesos criam timbres

    **Resultado:** Uma sinfonia que conta a história do aprendizado da rede! 🎼
    """)

    # Inicializa componentes
    session = MusicalTrainingSession()
    visualizer = MusicVisualizer(session.sonification)

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎵 Sonificação em Tempo Real",
        "🎼 Partitura Visual",
        "🎶 Demonstração Musical",
        "📚 Teoria da Sonificação"
    ])

    with tab1:
        st.markdown("### 🎵 Treinamento com Sonificação")

        # Modelo simples para demonstração
        model = nn.Sequential(
            nn.Linear(1, 10),
            nn.ReLU(),
            nn.Linear(10, 1)
        )

        # Dados de exemplo (função seno)
        X = torch.linspace(-2*np.pi, 2*np.pi, 100).unsqueeze(1)
        y = torch.sin(X) + 0.1 * torch.randn_like(X)

        col1, col2 = st.columns(2)

        with col1:
            epochs = st.slider("Épocas", 5, 50, 20)
            lr = st.slider("Learning Rate", 0.001, 0.1, 0.01)

        with col2:
            if st.button("🎼 Iniciar Treinamento Musical", type="primary"):
                st.markdown("#### 🎵 Sinfonia do Treinamento")

                history = session.train_with_sonification(
                    model, (X, y), epochs=epochs, lr=lr
                )

                st.success("🎉 Treinamento musical concluído!")

                # Gráfico final
                st.markdown("#### 📊 Resultados do Treinamento")
                fig = px.line(
                    x=[h['epoch'] for h in history],
                    y=[h['loss'] for h in history],
                    title="Evolução do Loss (agora também música! 🎵)"
                )
                st.plotly_chart(fig)

    with tab2:
        st.markdown("### 🎼 Visualização da Partitura")

        # Carrega dados de exemplo
        sample_history = session.create_sample_training_data()

        visualizer.create_music_score_visualization(sample_history)

        # Explicação
        st.markdown("""
        #### 🎼 Como Interpretar a Partitura

        - **🔵 Círculos Azuis**: Melodia (loss) - Altura = frequência da nota
        - **🟢 Losangos Verdes**: Harmonia (acurácia) - Acordes consonant/dissonant
        - **Tamanho**: Volume/intensidade das notas
        - **Eixo X**: Progressão temporal (épocas)
        - **Eixo Y**: Altura tonal (frequência em Hz)
        """)

    with tab3:
        st.markdown("### 🎶 Demonstração Musical")

        st.markdown("#### 🎼 Exemplo: Treinamento 'Perfeito'")

        # Simula treinamento perfeito
        perfect_history = []
        for epoch in range(20):
            progress = epoch / 19.0
            perfect_history.append({
                'epoch': epoch,
                'loss': 2.0 * np.exp(-progress * 4),  # Loss diminui rapidamente
                'accuracy': min(0.95, progress * 1.1),  # Acurácia sobe rápido
                'grad_norm': 1.0 * np.exp(-progress * 3),  # Gradientes estabilizam
                'lr': 0.01
            })

        # Mostra a "música" de cada epoch
        for epoch_data in perfect_history:
            with st.expander(f"🎵 Época {epoch_data['epoch']}"):
                music_desc = session.epoch_to_music_description(epoch_data)
                st.code(music_desc, language="text")

                # Pequeno gráfico da epoch
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['Loss', 'Acurácia', 'Gradiente'],
                    y=[epoch_data['loss'], epoch_data['accuracy'], epoch_data['grad_norm']],
                    marker_color=['red', 'green', 'blue']
                ))
                fig.update_layout(
                    title=f"Métricas da Época {epoch_data['epoch']}",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("### 📚 Teoria da Sonificação Neural")

        st.markdown("""
        #### 🎼 Princípios da Sonificação

        **1. Mapeamento Semântico**
        - Loss → Melodia: Reflete "saúde" do modelo
        - Acurácia → Harmonia: Representa "beleza" das previsões
        - Gradientes → Ritmo: Mostra "energia" do aprendizado

        **2. Percepção Humana**
        - Usamos escala logarítmica para frequências (como ouvido humano)
        - Dissonância musical reflete estados "problemáticos"
        - Ritmo sincroniza com velocidade de aprendizado

        **3. Benefícios Educacionais**
        - **Detecção de Anomalias**: Problemas no treinamento ficam audíveis
        - **Intuição Temporal**: Padrões de aprendizado se tornam musicais
        - **Engajamento**: Treinamento se torna uma experiência imersiva

        #### 🎶 Aplicações Avançadas

        - **Debugging Auditivo**: Identificar problemas pelo som
        - **Comparação de Modelos**: "Ouvir" diferenças arquiteturais
        - **Ensino Interativo**: Aprender ML através da música
        - **Arte Generativa**: Criar composições baseadas em aprendizado
        """)

        # Exemplo técnico
        st.markdown("#### 🔧 Exemplo Técnico")

        st.code("""
# Mapeamento Loss → Música
def loss_to_melody(loss):
    normalized = min(loss, 5.0) / 5.0  # 0-1
    note_index = int((1 - normalized) * 36)  # 3 oitavas
    octave = 3 + (note_index // 12)
    note = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][note_index % 12]
    return f"{note}{octave}"
        """)

if __name__ == "__main__":
    main()