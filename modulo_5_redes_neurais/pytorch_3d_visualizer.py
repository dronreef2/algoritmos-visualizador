#!/usr/bin/env python3
"""
🌌 PYTORCH 3D VISUALIZER - Módulo 5: Redes Neurais
===============================================

Visualização 3D imersiva de redes neurais usando Plotly e animações.
Permite explorar arquiteturas de rede em tempo real com interatividade.
"""

import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time
from typing import Dict, List, Optional, Any, Tuple

class NeuralNetwork3DVisualizer:
    """
    Visualizador 3D interativo para redes neurais PyTorch
    """

    def __init__(self):
        self.models = {}
        self.current_model = None

    def create_sample_networks(self):
        """Cria exemplos de redes neurais para visualização"""

        # Rede simples (MLP)
        self.models['MLP Simples'] = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

        # Rede convolucional simples
        self.models['ConvNet'] = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

        # Autoencoder
        self.models['Autoencoder'] = nn.Sequential(
            # Encoder
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            # Decoder
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 784),
            nn.Sigmoid()
        )

    def extract_network_layers(self, model: nn.Module) -> List[Dict]:
        """Extrai informações das camadas da rede"""
        layers = []

        for name, module in model.named_modules():
            if name == '':  # Skip root module
                continue

            layer_info = {
                'name': name,
                'type': type(module).__name__,
                'parameters': sum(p.numel() for p in module.parameters() if p.requires_grad)
            }

            # Informações específicas por tipo de camada
            if isinstance(module, nn.Linear):
                layer_info.update({
                    'input_features': module.in_features,
                    'output_features': module.out_features,
                    'shape': (module.in_features, module.out_features)
                })
            elif isinstance(module, nn.Conv2d):
                layer_info.update({
                    'in_channels': module.in_channels,
                    'out_channels': module.out_channels,
                    'kernel_size': module.kernel_size,
                    'shape': (module.in_channels, module.out_channels, module.kernel_size[0], module.kernel_size[1])
                })

            layers.append(layer_info)

        return layers

    def create_3d_network_visualization(self, layers: List[Dict]) -> go.Figure:
        """Cria visualização 3D da arquitetura da rede"""

        fig = go.Figure()

        # Posições das camadas no espaço 3D
        layer_positions = []
        for i, layer in enumerate(layers):
            x = i * 2  # Espaçamento horizontal
            y = 0      # Centro vertical
            z = 0      # Profundidade

            # Ajusta posição baseada no tipo de camada
            if 'Conv' in layer['type']:
                z = 1  # Camadas conv acima
            elif 'Pool' in layer['type']:
                z = -1  # Pooling abaixo

            layer_positions.append((x, y, z, layer))

        # Conexões entre camadas
        for i in range(len(layer_positions) - 1):
            x1, y1, z1, layer1 = layer_positions[i]
            x2, y2, z2, layer2 = layer_positions[i + 1]

            # Linha conectando camadas
            fig.add_trace(go.Scatter3d(
                x=[x1, x2], y=[y1, y2], z=[z1, z2],
                mode='lines',
                line=dict(color='lightblue', width=2),
                showlegend=False
            ))

        # Nós das camadas
        for x, y, z, layer in layer_positions:
            # Tamanho baseado no número de parâmetros
            size = max(10, min(50, layer['parameters'] / 100))

            # Cor baseada no tipo de camada
            color_map = {
                'Linear': 'red',
                'Conv2d': 'blue',
                'ReLU': 'green',
                'MaxPool2d': 'orange',
                'Flatten': 'purple',
                'Sigmoid': 'pink'
            }
            color = color_map.get(layer['type'], 'gray')

            # Hover text com informações detalhadas
            hover_text = f"""
            <b>{layer['name']}</b><br>
            Tipo: {layer['type']}<br>
            Parâmetros: {layer['parameters']:,}<br>
            {'Shape: ' + str(layer.get('shape', 'N/A'))}
            """

            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers+text',
                marker=dict(
                    size=size,
                    color=color,
                    opacity=0.8,
                    symbol='circle'
                ),
                text=[layer['type']],
                textposition="top center",
                hovertext=[hover_text],
                hoverinfo="text",
                name=layer['type']
            ))

        # Configurações do layout 3D
        fig.update_layout(
            title="🌌 Arquitetura 3D da Rede Neural",
            scene=dict(
                xaxis_title="Camadas",
                yaxis_title="Largura",
                zaxis_title="Profundidade",
                xaxis=dict(showgrid=True, gridcolor='lightgray'),
                yaxis=dict(showgrid=True, gridcolor='lightgray'),
                zaxis=dict(showgrid=True, gridcolor='lightgray'),
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        # Adiciona controles de câmera
        fig.update_layout(
            scene_camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        )

        return fig

    def create_parameter_flow_animation(self, model: nn.Module) -> go.Figure:
        """Cria animação do fluxo de parâmetros durante forward pass"""

        frames = []
        layer_outputs = []

        # Dados de exemplo
        x = torch.randn(1, 2)  # Input de exemplo

        # Forward pass com captura de saídas
        with torch.no_grad():
            current_input = x

            for name, module in model.named_modules():
                if name == '':
                    continue

                # Aplica camada
                if isinstance(module, nn.Linear):
                    output = module(current_input)
                elif isinstance(module, nn.ReLU):
                    output = module(current_input)
                elif isinstance(module, nn.Sigmoid):
                    output = module(current_input)
                else:
                    continue

                layer_outputs.append({
                    'layer': name,
                    'input_shape': current_input.shape,
                    'output_shape': output.shape,
                    'input_data': current_input.numpy().flatten()[:10],  # Primeiros 10 valores
                    'output_data': output.numpy().flatten()[:10]
                })

                current_input = output

        # Cria frames da animação
        for i in range(len(layer_outputs)):
            frame_data = []

            for j, layer_data in enumerate(layer_outputs[:i+1]):
                # Distribuição dos dados de entrada
                input_hist, input_bins = np.histogram(layer_data['input_data'], bins=20)

                frame_data.append(go.Bar(
                    x=input_bins[:-1],
                    y=input_hist,
                    name=f'Input {layer_data["layer"]}',
                    marker_color='lightblue',
                    opacity=0.7,
                    showlegend=j == 0
                ))

                # Distribuição dos dados de saída
                output_hist, output_bins = np.histogram(layer_data['output_data'], bins=20)

                frame_data.append(go.Bar(
                    x=output_bins[:-1],
                    y=output_hist,
                    name=f'Output {layer_data["layer"]}',
                    marker_color='orange',
                    opacity=0.7,
                    showlegend=j == 0
                ))

            frames.append(go.Frame(data=frame_data, name=f"Camada {i+1}"))

        # Figura inicial
        initial_data = []
        if layer_outputs:
            input_hist, input_bins = np.histogram(layer_outputs[0]['input_data'], bins=20)
            initial_data.append(go.Bar(
                x=input_bins[:-1],
                y=input_hist,
                name='Input Inicial',
                marker_color='lightblue'
            ))

        fig = go.Figure(data=initial_data, frames=frames)

        # Configurações da animação
        fig.update_layout(
            title="🎬 Fluxo de Dados na Rede Neural",
            xaxis_title="Valor",
            yaxis_title="Frequência",
            updatemenus=[{
                'type': 'buttons',
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 1000, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 500}
                    }]
                }, {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }]
            }]
        )

        return fig

    def create_interactive_tensor_explorer(self) -> go.Figure:
        """Explorador interativo de tensores 4D+"""

        # Cria tensor de exemplo (batch_size, channels, height, width)
        tensor_4d = torch.randn(2, 3, 8, 8)

        # Converte para formato visualizável
        batch_idx = 0
        channel_idx = 0

        # Slice 2D do tensor
        slice_2d = tensor_4d[batch_idx, channel_idx].numpy()

        fig = go.Figure(data=go.Heatmap(
            z=slice_2d,
            colorscale='RdBu',
            zmid=0
        ))

        # Adiciona controles deslizantes
        fig.update_layout(
            title="🔍 Explorador Interativo de Tensores",
            xaxis_title="Largura",
            yaxis_title="Altura",
            annotations=[
                dict(
                    text=f"Batch: {batch_idx}, Canal: {channel_idx}",
                    showarrow=False,
                    x=0.5,
                    y=1.1,
                    xref="paper",
                    yref="paper"
                )
            ]
        )

        return fig

def main():
    st.markdown("# 🌌 Visualizador 3D de Redes Neurais")
    st.markdown("Explore arquiteturas de rede neural em 3D com interatividade total!")

    visualizer = NeuralNetwork3DVisualizer()
    visualizer.create_sample_networks()

    # Seleção de modelo
    model_names = list(visualizer.models.keys())
    selected_model = st.selectbox("🧠 Selecione uma arquitetura:", model_names)

    if selected_model:
        model = visualizer.models[selected_model]
        layers = visualizer.extract_network_layers(model)

        # Abas de visualização
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏗️ Arquitetura 3D",
            "🎬 Fluxo de Dados",
            "🔍 Tensor Explorer",
            "📊 Estatísticas"
        ])

        with tab1:
            st.markdown("### 🏗️ Arquitetura 3D da Rede")
            st.markdown("Arraste para rotacionar, zoom para aproximar!")

            fig_3d = visualizer.create_3d_network_visualization(layers)
            st.plotly_chart(fig_3d, use_container_width=True)

            # Informações das camadas
            st.markdown("#### 📋 Informações das Camadas")
            layer_df = pd.DataFrame(layers)
            st.dataframe(layer_df)

        with tab2:
            st.markdown("### 🎬 Animação do Fluxo de Dados")
            st.markdown("Veja como os dados fluem através da rede neural!")

            try:
                fig_animation = visualizer.create_parameter_flow_animation(model)
                st.plotly_chart(fig_animation, use_container_width=True)
            except Exception as e:
                st.error(f"Erro na criação da animação: {e}")
                st.info("💡 Esta funcionalidade requer dados de entrada específicos.")

        with tab3:
            st.markdown("### 🔍 Explorador Interativo de Tensores")
            st.markdown("Explore tensores multidimensionais em tempo real!")

            fig_tensor = visualizer.create_interactive_tensor_explorer()
            st.plotly_chart(fig_tensor, use_container_width=True)

            # Controles interativos
            col1, col2 = st.columns(2)
            with col1:
                batch_slider = st.slider("Batch", 0, 1, 0)
            with col2:
                channel_slider = st.slider("Canal", 0, 2, 0)

        with tab4:
            st.markdown("### 📊 Estatísticas da Rede")

            # Métricas gerais
            total_params = sum(layer['parameters'] for layer in layers)
            num_layers = len(layers)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total de Parâmetros", f"{total_params:,}")

            with col2:
                st.metric("Número de Camadas", num_layers)

            with col3:
                st.metric("Parâmetros por Camada", f"{total_params/num_layers:.0f}")

            # Distribuição por tipo de camada
            st.markdown("#### 📈 Distribuição por Tipo de Camada")

            layer_types = {}
            for layer in layers:
                layer_type = layer['type']
                layer_types[layer_type] = layer_types.get(layer_type, 0) + 1

            fig_pie = px.pie(
                values=list(layer_types.values()),
                names=list(layer_types.keys()),
                title="Tipos de Camada"
            )
            st.plotly_chart(fig_pie)

            # Parâmetros por camada
            st.markdown("#### 📊 Parâmetros por Camada")

            param_df = pd.DataFrame({
                'Camada': [layer['name'] for layer in layers],
                'Parâmetros': [layer['parameters'] for layer in layers],
                'Tipo': [layer['type'] for layer in layers]
            })

            fig_bar = px.bar(
                param_df,
                x='Camada',
                y='Parâmetros',
                color='Tipo',
                title="Distribuição de Parâmetros"
            )
            st.plotly_chart(fig_bar)

if __name__ == "__main__":
    main()