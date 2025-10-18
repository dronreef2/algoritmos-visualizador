#!/usr/bin/env python3
"""
🎨 NEURAL GENERATIVE ART - Módulo 5: Redes Neurais
===============================================

Sistema de arte generativa que transforma padrões de aprendizado neural em obras visuais.
Cada arquitetura, peso e processo de treinamento se torna uma obra de arte única!
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
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import seaborn as sns
import time
import random
from typing import Dict, List, Optional, Any, Tuple
import io
import base64
import json
from PIL import Image, ImageDraw, ImageFilter
import colorsys

class NeuralArtGenerator:
    """
    Gerador de arte baseado em padrões neurais
    Transforma pesos, ativações e gradientes em arte visual
    """

    def __init__(self):
        self.color_palettes = {
            'neural_fire': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'cosmic': ['#2C3E50', '#E74C3C', '#9B59B6', '#3498DB', '#F1C40F'],
            'ocean': ['#1B1464', '#0652DD', '#9980FA', '#FDA7DF', '#ED4C67'],
            'forest': ['#006266', '#1B1464', '#6F1E51', '#A3CB38', '#FDCB6E']
        }

        self.art_styles = {
            'neural_network': self.create_neural_network_art,
            'weight_landscape': self.create_weight_landscape,
            'activation_flow': self.create_activation_flow,
            'gradient_storm': self.create_gradient_storm,
            'loss_contour': self.create_loss_contour_art,
            'architecture_dream': self.create_architecture_dream
        }

    def create_neural_network_art(self, model: nn.Module, training_data: Dict) -> Dict:
        """Cria arte representando a arquitetura da rede neural"""

        # Extrai informações da arquitetura
        layers_info = []
        total_params = 0

        for name, module in model.named_modules():
            if isinstance(module, nn.Linear):
                in_features = module.in_features
                out_features = module.out_features
                params = in_features * out_features + out_features
                total_params += params

                layers_info.append({
                    'name': name,
                    'in_features': in_features,
                    'out_features': out_features,
                    'params': params
                })

        # Cria visualização artística
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_facecolor('#0f0f23')

        # Desenha camadas como círculos concêntricos
        max_features = max(max(l['in_features'], l['out_features']) for l in layers_info)

        for i, layer in enumerate(layers_info):
            # Posição da camada
            x = i * 3
            y = 0

            # Tamanho baseado no número de neurônios
            size_in = layer['in_features'] / max_features * 1000
            size_out = layer['out_features'] / max_features * 1000

            # Círculo de entrada (azul)
            circle_in = patches.Circle((x, y + 1), np.sqrt(size_in/np.pi),
                                     facecolor='#3498DB', alpha=0.7, edgecolor='white')
            ax.add_patch(circle_in)

            # Círculo de saída (verde)
            circle_out = patches.Circle((x, y - 1), np.sqrt(size_out/np.pi),
                                      facecolor='#2ECC71', alpha=0.7, edgecolor='white')
            ax.add_patch(circle_out)

            # Conexões entre camadas
            if i < len(layers_info) - 1:
                next_layer = layers_info[i + 1]
                # Linhas representando conexões
                for j in range(min(20, layer['out_features'])):  # Limita para performance
                    y1 = y - 1 + (j / min(20, layer['out_features'])) * 2
                    y2 = (i + 1) * 3
                    line = patches.ConnectionPatch((x, y1), (y2, 0),
                                                 "data", "data",
                                                 color='white', alpha=0.3, linewidth=0.5)
                    ax.add_patch(line)

        ax.set_xlim(-1, len(layers_info) * 3)
        ax.set_ylim(-3, 3)
        ax.axis('off')

        return {
            'figure': fig,
            'title': '🧠 Arquitetura Neural - Dança dos Neurônios',
            'description': f"Rede com {len(layers_info)} camadas e {total_params:,} parâmetros",
            'style': 'neural_network'
        }

    def create_weight_landscape(self, model: nn.Module, training_data: Dict) -> Dict:
        """Cria paisagem baseada na distribuição dos pesos"""

        # Coleta todos os pesos
        all_weights = []
        layer_names = []

        for name, param in model.named_parameters():
            if 'weight' in name and param.requires_grad:
                weights = param.data.flatten().cpu().numpy()
                all_weights.append(weights)
                layer_names.append(name)

        # Cria visualização como paisagem
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor('#2C3E50')

        # 1. Distribuição geral dos pesos
        all_weights_flat = np.concatenate(all_weights)
        axes[0,0].hist(all_weights_flat, bins=50, alpha=0.7, color='#E74C3C', edgecolor='white')
        axes[0,0].set_title('🌄 Distribuição dos Pesos - Montanhas Neurais', color='white')
        axes[0,0].set_facecolor('#34495E')
        axes[0,0].tick_params(colors='white')

        # 2. Correlação entre camadas
        if len(all_weights) > 1:
            means = [np.mean(w) for w in all_weights]
            stds = [np.std(w) for w in all_weights]

            scatter = axes[0,1].scatter(means, stds, c=range(len(means)),
                                       cmap='viridis', s=100, alpha=0.8)
            axes[0,1].set_xlabel('Média dos Pesos', color='white')
            axes[0,1].set_ylabel('Desvio Padrão', color='white')
            axes[0,1].set_title('🏔️ Correlação Camada-Média', color='white')
            axes[0,1].set_facecolor('#34495E')
            axes[0,1].tick_params(colors='white')
            plt.colorbar(scatter, ax=axes[0,1])

        # 3. Mapa de calor dos pesos da primeira camada
        if len(all_weights) > 0:
            weights_2d = all_weights[0].reshape(-1, min(20, len(all_weights[0])))
            if weights_2d.shape[1] > 1:
                sns.heatmap(weights_2d[:20, :], ax=axes[1,0], cmap='RdYlBu_r',
                           cbar=True, square=True)
                axes[1,0].set_title('🔥 Mapa de Calor dos Pesos', color='white')
                axes[1,0].tick_params(colors='white')

        # 4. "Paisagem" criada pelos pesos
        x = np.linspace(0, 10, 1000)
        y = np.zeros_like(x)

        # Cada camada contribui para a paisagem
        for i, weights in enumerate(all_weights):
            # Usa FFT para criar padrão orgânico
            if len(weights) > 10:
                fft_weights = np.abs(np.fft.fft(weights[:100]))[:50]
                pattern = np.interp(x, np.linspace(0, 10, len(fft_weights)), fft_weights)
                y += pattern * (0.5 ** i)  # Decaimento por camada

        axes[1,1].fill_between(x, y, alpha=0.7, color='#F1C40F')
        axes[1,1].plot(x, y, color='white', linewidth=2)
        axes[1,1].set_title('🏞️ Paisagem Neural Gerada', color='white')
        axes[1,1].set_facecolor('#34495E')
        axes[1,1].tick_params(colors='white')

        plt.tight_layout()

        return {
            'figure': fig,
            'title': '🏔️ Paisagem dos Pesos - Montanhas do Aprendizado',
            'description': f"Paisagem criada por {len(layer_names)} camadas neurais",
            'style': 'weight_landscape'
        }

    def create_activation_flow(self, model: nn.Module, training_data: Dict) -> Dict:
        """Cria arte baseada no fluxo de ativações durante o treinamento"""

        # Simula passagem forward com dados de exemplo
        if 'sample_input' not in training_data:
            # Cria entrada de exemplo
            sample_input = torch.randn(1, model[0].in_features if hasattr(model[0], 'in_features') else 10)
        else:
            sample_input = training_data['sample_input']

        # Coleta ativações por camada
        activations = []
        hooks = []

        def hook_fn(module, input, output):
            activations.append(output.detach().cpu().numpy())

        # Registra hooks
        for module in model.modules():
            if isinstance(module, (nn.Linear, nn.ReLU, nn.Sigmoid, nn.Tanh)):
                hooks.append(module.register_forward_hook(hook_fn))

        # Forward pass
        with torch.no_grad():
            _ = model(sample_input)

        # Remove hooks
        for hook in hooks:
            hook.remove()

        # Cria visualização do fluxo
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_facecolor('#1a1a2e')

        # Cores para diferentes tipos de camadas
        layer_colors = {
            'Linear': '#FF6B6B',
            'ReLU': '#4ECDC4',
            'Sigmoid': '#45B7D1',
            'Tanh': '#96CEB4'
        }

        # Desenha fluxo de ativações
        y_positions = np.linspace(0, 10, len(activations))

        for i, activation in enumerate(activations):
            act_flat = activation.flatten()
            act_sample = act_flat[:min(100, len(act_flat))]  # Amostra para performance

            # Distribuição das ativações
            y_base = y_positions[i]
            x_positions = np.linspace(0, 12, len(act_sample))

            # Cria "fluxo" com linhas conectando pontos
            points = np.array([x_positions, y_base + act_sample * 2]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            # Cor baseada no tipo de camada (aproximado)
            color = layer_colors.get('Linear', '#FF6B6B') if i % 2 == 0 else layer_colors.get('ReLU', '#4ECDC4')

            lc = LineCollection(segments, colors=color, linewidths=2, alpha=0.7)
            ax.add_collection(lc)

            # Adiciona pontos
            ax.scatter(x_positions, y_base + act_sample * 2,
                      c=color, s=20, alpha=0.8, edgecolors='white')

        ax.set_xlim(0, 12)
        ax.set_ylim(-1, 11)
        ax.axis('off')

        return {
            'figure': fig,
            'title': '🌊 Fluxo de Ativações - Rio Neural',
            'description': f"Fluxo de {len(activations)} camadas durante inferência",
            'style': 'activation_flow'
        }

    def create_gradient_storm(self, model: nn.Module, training_data: Dict) -> Dict:
        """Cria arte baseada nos gradientes durante o treinamento"""

        # Simula um passo de treinamento para obter gradientes
        if 'sample_input' not in training_data or 'sample_target' not in training_data:
            sample_input = torch.randn(1, model[0].in_features if hasattr(model[0], 'in_features') else 10)
            sample_target = torch.randn(1, 1)
        else:
            sample_input = training_data['sample_input']
            sample_target = training_data['sample_target']

        # Forward e backward para obter gradientes
        output = model(sample_input)
        loss = nn.MSELoss()(output, sample_target)
        loss.backward()

        # Coleta gradientes
        gradients = []
        param_names = []

        for name, param in model.named_parameters():
            if param.grad is not None:
                grad = param.grad.data.flatten().cpu().numpy()
                gradients.append(grad)
                param_names.append(name)

        # Cria visualização da "tempestade" de gradientes
        fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': 'polar'})
        ax.set_facecolor('#0f0f0f')

        # Converte gradientes em padrões polares
        for i, grad in enumerate(gradients):
            # Normaliza gradientes
            grad_norm = np.abs(grad) / (np.max(np.abs(grad)) + 1e-8)

            # Cria ângulos para visualização polar
            angles = np.linspace(0, 2*np.pi, len(grad_norm), endpoint=False)

            # Magnitude baseada na norma do gradiente
            r = grad_norm * (i + 1) * 2  # Aumenta raio por camada

            # Cor baseada na magnitude
            colors = plt.cm.RdYlBu_r(grad_norm)

            # Plota como scatter polar
            ax.scatter(angles, r, c=colors, s=50, alpha=0.7, cmap='RdYlBu_r')

        ax.set_title('🌪️ Tempestade de Gradientes', color='white', pad=20)
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3)

        return {
            'figure': fig,
            'title': '🌪️ Tempestade de Gradientes - Furacão Neural',
            'description': f"Visualização polar de gradientes em {len(gradients)} camadas",
            'style': 'gradient_storm'
        }

    def create_loss_contour_art(self, model: nn.Module, training_data: Dict) -> Dict:
        """Cria arte baseada na superfície de loss"""

        # Para redes simples, podemos visualizar a superfície de loss
        if not isinstance(model, nn.Sequential) or len(list(model.children())) != 3:
            # Fallback para visualização alternativa
            return self.create_weight_landscape(model, training_data)

        # Assume rede simples: Linear -> ReLU -> Linear
        layers = list(model.children())

        if not (isinstance(layers[0], nn.Linear) and isinstance(layers[2], nn.Linear)):
            return self.create_weight_landscape(model, training_data)

        # Cria grade de pesos para visualizar superfície de loss
        w1_range = np.linspace(-2, 2, 20)
        w2_range = np.linspace(-2, 2, 20)
        W1, W2 = np.meshgrid(w1_range, w2_range)

        # Dados de exemplo
        if 'sample_input' not in training_data:
            X = torch.randn(10, layers[0].in_features)
            y = torch.randn(10, layers[2].out_features)
        else:
            X = training_data['sample_input']
            y = training_data['sample_target']

        losses = np.zeros_like(W1)

        # Calcula loss para cada combinação de pesos
        for i in range(len(w1_range)):
            for j in range(len(w2_range)):
                # Modifica pesos temporariamente
                original_w1 = layers[0].weight.data.clone()
                original_w2 = layers[2].weight.data.clone()

                layers[0].weight.data = torch.full_like(layers[0].weight, w1_range[i])
                layers[2].weight.data = torch.full_like(layers[2].weight, w2_range[j])

                with torch.no_grad():
                    output = model(X)
                    loss = nn.MSELoss()(output, y)
                    losses[i, j] = loss.item()

                # Restaura pesos
                layers[0].weight.data = original_w1
                layers[2].weight.data = original_w2

        # Cria visualização artística da superfície
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#2C3E50')

        # Superfície de loss
        surf = ax.plot_surface(W1, W2, losses, cmap='viridis', alpha=0.8,
                              linewidth=0, antialiased=True)

        # Adiciona pontos de mínimo
        min_idx = np.unravel_index(np.argmin(losses), losses.shape)
        ax.scatter([w1_range[min_idx[0]]], [w2_range[min_idx[1]]],
                  [losses[min_idx]], color='red', s=100, marker='*')

        ax.set_xlabel('Peso Camada 1', color='white')
        ax.set_ylabel('Peso Camada 2', color='white')
        ax.set_zlabel('Loss', color='white')
        ax.set_title('🏔️ Superfície de Loss - Montanha da Otimização', color='white', pad=20)

        # Estiliza ticks
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')

        return {
            'figure': fig,
            'title': '🏔️ Superfície de Loss - Paisagem da Otimização',
            'description': f"Superfície de loss em 2D mostrando mínimos e vales",
            'style': 'loss_contour'
        }

    def create_architecture_dream(self, model: nn.Module, training_data: Dict) -> Dict:
        """Cria arte abstrata baseada na arquitetura completa"""

        # Cria imagem PIL para arte abstrata
        width, height = 800, 600
        image = Image.new('RGB', (width, height), '#1a1a2e')
        draw = ImageDraw.Draw(image)

        # Extrai características da arquitetura
        num_layers = len(list(model.modules()))
        total_params = sum(p.numel() for p in model.parameters())

        # Cores baseadas na arquitetura
        base_hue = (num_layers * 37) % 360  # Hue cíclico
        saturation = 0.7
        brightness = 0.8

        # Desenha elementos abstratos baseados na arquitetura
        for i in range(num_layers):
            # Posição baseada no índice da camada
            x = (i / max(1, num_layers - 1)) * width
            y = height // 2

            # Tamanho baseado no número de parâmetros
            layer_params = sum(p.numel() for p in list(model.modules())[i].parameters()) if hasattr(list(model.modules())[i], 'parameters') else 100
            size = 20 + (layer_params / total_params) * 200

            # Cor baseada na posição
            hue = (base_hue + i * 30) % 360
            rgb = colorsys.hsv_to_rgb(hue/360, saturation, brightness)
            color = tuple(int(c * 255) for c in rgb)

            # Desenha formas abstratas
            if i % 4 == 0:
                # Círculo
                draw.ellipse([x-size, y-size, x+size, y+size], fill=color, outline='white')
            elif i % 4 == 1:
                # Retângulo
                draw.rectangle([x-size, y-size, x+size, y+size], fill=color, outline='white')
            elif i % 4 == 2:
                # Triângulo
                draw.polygon([(x, y-size), (x-size, y+size), (x+size, y+size)], fill=color, outline='white')
            else:
                # Linha curva
                draw.arc([x-size, y-size, x+size, y+size], 0, 180, fill=color, width=3)

        # Aplica efeito de desfoque para arte mais onírica
        image = image.filter(ImageFilter.GaussianBlur(radius=2))

        return {
            'image': image,
            'title': '💭 Sonho Arquitetural - Visão Abstrata da Rede',
            'description': f"Arte abstrata gerada por arquitetura de {num_layers} camadas",
            'style': 'architecture_dream'
        }

class ArtGallery:
    """Galeria interativa para exibir arte neural"""

    def __init__(self, generator: NeuralArtGenerator):
        self.generator = generator

    def display_artwork(self, artwork: Dict):
        """Exibe uma obra de arte na galeria"""

        st.markdown(f"## {artwork['title']}")
        st.markdown(f"*{artwork['description']}*")

        if 'figure' in artwork:
            # Arte matplotlib/plotly
            st.pyplot(artwork['figure'])

        elif 'image' in artwork:
            # Arte PIL
            st.image(artwork['image'], use_column_width=True)

        # Metadados
        with st.expander("📋 Detalhes Técnicos"):
            st.json({
                'estilo': artwork['style'],
                'titulo': artwork['title'],
                'descricao': artwork['description']
            })

    def create_art_collection(self, model: nn.Module, training_data: Dict):
        """Cria uma coleção completa de arte baseada no modelo"""

        st.markdown("### 🎨 Coleção de Arte Neural")

        # Gera todas as obras disponíveis
        artworks = []

        for style_name, style_func in self.generator.art_styles.items():
            try:
                artwork = style_func(model, training_data)
                artworks.append(artwork)
            except Exception as e:
                st.warning(f"Erro ao gerar arte no estilo {style_name}: {e}")

        # Exibe galeria
        cols = st.columns(2)

        for i, artwork in enumerate(artworks):
            with cols[i % 2]:
                with st.expander(f"🎨 {artwork['title']}", expanded=(i==0)):
                    self.display_artwork(artwork)

def main():
    st.markdown("# 🎨 Neural Generative Art")
    st.markdown("Transforme sua rede neural em uma galeria de arte! 🖼️🎭")

    st.markdown("""
    ## 🎨 O que é Arte Neural Generativa?

    **Arte Neural Generativa** transforma elementos matemáticos das redes neurais em obras visuais:

    - 🧠 **Arquitetura** → **Estruturas Geométricas**: Camadas viram círculos concêntricos
    - ⚖️ **Pesos** → **Paisagens**: Distribuições criam montanhas e vales
    - ⚡ **Ativações** → **Fluxos**: Sinais neurais se tornam rios luminosos
    - 🌪️ **Gradientes** → **Tempestades**: Otimização cria furacões visuais
    - 📉 **Loss** → **Superfícies**: Funções de custo viram montanhas 3D
    - 💭 **Sonhos** → **Abstrações**: Arquiteturas geram arte onírica

    **Resultado:** Cada rede neural se torna uma obra de arte única! 🎨
    """)

    # Inicializa gerador
    generator = NeuralArtGenerator()
    gallery = ArtGallery(generator)

    # Modelo de exemplo
    @st.cache_resource
    def create_example_model():
        return nn.Sequential(
            nn.Linear(10, 20),
            nn.ReLU(),
            nn.Linear(20, 15),
            nn.Tanh(),
            nn.Linear(15, 1)
        )

    model = create_example_model()

    # Dados de treinamento de exemplo
    training_data = {
        'sample_input': torch.randn(32, 10),
        'sample_target': torch.randn(32, 1)
    }

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 Galeria Completa",
        "🎭 Estilos Individuais",
        "🎪 Exposição Interativa",
        "📚 Teoria da Arte Neural"
    ])

    with tab1:
        st.markdown("### 🖼️ Galeria Completa - Coleção Neural")

        if st.button("🎨 Gerar Coleção de Arte", type="primary"):
            with st.spinner("🎭 Criando obras de arte neurais..."):
                gallery.create_art_collection(model, training_data)

    with tab2:
        st.markdown("### 🎭 Estilos Individuais")

        style_options = list(generator.art_styles.keys())
        style_names = {
            'neural_network': '🧠 Rede Neural - Dança dos Neurônios',
            'weight_landscape': '🏔️ Paisagem dos Pesos',
            'activation_flow': '🌊 Fluxo de Ativações',
            'gradient_storm': '🌪️ Tempestade de Gradientes',
            'loss_contour': '🏔️ Superfície de Loss',
            'architecture_dream': '💭 Sonho Arquitetural'
        }

        selected_style = st.selectbox(
            "Escolha um estilo artístico:",
            options=style_options,
            format_func=lambda x: style_names.get(x, x)
        )

        if st.button(f"🎨 Criar Arte: {style_names[selected_style]}"):
            with st.spinner(f"🎭 Gerando arte no estilo {style_names[selected_style]}..."):
                try:
                    artwork = generator.art_styles[selected_style](model, training_data)
                    gallery.display_artwork(artwork)
                except Exception as e:
                    st.error(f"Erro ao gerar arte: {e}")

    with tab3:
        st.markdown("### 🎪 Exposição Interativa")

        st.markdown("#### 🎨 Parâmetros da Arte")

        col1, col2 = st.columns(2)

        with col1:
            palette = st.selectbox(
                "Paleta de Cores:",
                options=list(generator.color_palettes.keys()),
                format_func=lambda x: x.replace('_', ' ').title()
            )

            complexity = st.slider("Complexidade", 1, 10, 5)

        with col2:
            animation = st.checkbox("Animação Temporal", value=False)
            export_art = st.checkbox("Permitir Exportação", value=True)

        st.markdown("#### 🎭 Demonstração: Evolução da Arte")

        # Simula evolução durante treinamento
        epochs = st.slider("Épocas de Treinamento", 1, 20, 5)

        if st.button("🎨 Evoluir Arte Através do Treinamento"):
            progress_bar = st.progress(0)

            for epoch in range(epochs):
                # Simula mudança nos pesos durante treinamento
                with torch.no_grad():
                    for param in model.parameters():
                        # Adiciona pequena variação (simulando aprendizado)
                        noise = torch.randn_like(param) * 0.01
                        param.add_(noise)

                # Gera arte da arquitetura atual
                artwork = generator.create_architecture_dream(model, training_data)

                with st.expander(f"🎨 Época {epoch + 1}", expanded=(epoch == epochs-1)):
                    gallery.display_artwork(artwork)

                progress_bar.progress((epoch + 1) / epochs)
                time.sleep(0.5)

            st.success("🎉 Evolução artística completa!")

    with tab4:
        st.markdown("### 📚 Teoria da Arte Neural Generativa")

        st.markdown("""
        #### 🎨 Princípios da Arte Neural

        **1. Mapeamento Matemático-Visual**
        - Pesos → Posições/Cartografia
        - Ativações → Fluxos/Cores
        - Gradientes → Movimentos/Direções
        - Loss → Elevação/Profundidade

        **2. Percepção Humana**
        - Usamos cores e formas que o cérebro humano processa naturalmente
        - Padrões fractais e orgânicos emergem das redes neurais
        - Simetria e hierarquia refletem estruturas neurais

        **3. Benefícios Educacionais**
        - **Visualização Abstrata**: Conceitos complexos ficam intuitivos
        - **Padrões Emergentes**: Compreensão profunda através da arte
        - **Criatividade**: Inspiração para novas arquiteturas

        #### 🎭 Aplicações Artísticas

        - **Debugging Visual**: Problemas na rede ficam evidentes na arte
        - **Comparação Arquitetural**: Diferenças visuais entre modelos
        - **Inspiração Criativa**: Novas ideias nascem da visualização
        - **Arte Generativa**: Criação de obras originais baseadas em ML
        """)

        # Exemplo de código
        st.markdown("#### 🔧 Exemplo: Geração de Paisagem Neural")

        st.code("""
def create_weight_landscape(model):
    # Coleta pesos de todas as camadas
    all_weights = []
    for param in model.parameters():
        all_weights.extend(param.flatten().tolist())

    # Converte pesos em terreno 3D
    x = np.linspace(0, 10, len(all_weights))
    y = np.array(all_weights) * 100  # Escala para visualização

    # Cria paisagem suave com interpolação
    from scipy import interpolate
    f = interpolate.interp1d(x, y, kind='cubic')
    x_smooth = np.linspace(0, 10, 1000)
    y_smooth = f(x_smooth)

    # Plota como paisagem
    plt.fill_between(x_smooth, y_smooth, alpha=0.7, color='terrain')
    plt.plot(x_smooth, y_smooth, color='black', linewidth=2)
        """)

if __name__ == "__main__":
    main()