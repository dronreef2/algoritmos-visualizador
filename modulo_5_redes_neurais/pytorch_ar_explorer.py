#!/usr/bin/env python3
"""
🎭 PYTORCH AR/VR EXPERIENCE - Módulo 5: Redes Neurais
===============================================

Experiência imersiva de Realidade Aumentada para visualização de redes neurais.
Permite "entrar" dentro da rede neural e explorar camadas em 3D.
"""

import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
import json
from typing import Dict, List, Optional, Any, Tuple
import streamlit.components.v1 as components

class ARNeuralExplorer:
    """
    Explorador de Realidade Aumentada para redes neurais
    """

    def __init__(self):
        self.current_position = [0, 0, 0]  # Posição do usuário na rede
        self.current_layer = 0
        self.view_mode = "first_person"  # first_person, third_person, god_mode

    def create_network_world(self, model: nn.Module) -> Dict:
        """Cria um "mundo" 3D representando a rede neural"""

        layers = []
        connections = []

        layer_idx = 0
        for name, module in model.named_modules():
            if name == '':
                continue

            # Posição da camada no espaço 3D
            layer_pos = {
                'id': layer_idx,
                'name': name,
                'type': type(module).__name__,
                'position': [layer_idx * 3, 0, 0],  # Espaçamento de 3 unidades
                'size': self.get_layer_size(module),
                'color': self.get_layer_color(module),
                'neurons': self.get_neuron_positions(module, layer_idx)
            }
            layers.append(layer_pos)

            # Conexões entre camadas
            if layer_idx > 0:
                prev_layer = layers[layer_idx - 1]
                connections.extend(self.create_connections(prev_layer, layer_pos))

            layer_idx += 1

        return {
            'layers': layers,
            'connections': connections,
            'world_bounds': self.calculate_world_bounds(layers)
        }

    def get_layer_size(self, module: nn.Module) -> List[float]:
        """Calcula tamanho visual da camada"""
        if isinstance(module, nn.Linear):
            return [1, module.out_features / 10, 1]
        elif isinstance(module, nn.Conv2d):
            return [2, 2, 1]
        else:
            return [1, 1, 1]

    def get_layer_color(self, module: nn.Module) -> str:
        """Define cor da camada baseada no tipo"""
        color_map = {
            'Linear': '#FF6B6B',
            'Conv2d': '#4ECDC4',
            'ReLU': '#45B7D1',
            'MaxPool2d': '#FFA07A',
            'Flatten': '#98D8C8',
            'Sigmoid': '#F7DC6F'
        }
        return color_map.get(type(module).__name__, '#BDC3C7')

    def get_neuron_positions(self, module: nn.Module, layer_idx: int) -> List[List[float]]:
        """Calcula posições dos neurônios na camada"""
        positions = []

        if isinstance(module, nn.Linear):
            num_neurons = module.out_features
            for i in range(min(num_neurons, 20)):  # Limita para performance
                x = layer_idx * 3
                y = (i - num_neurons/2) * 0.2
                z = np.random.uniform(-0.5, 0.5)
                positions.append([x, y, z])
        elif isinstance(module, nn.Conv2d):
            # Representa como grid 2D
            out_channels = module.out_channels
            grid_size = int(np.sqrt(min(out_channels, 16)))
            for i in range(min(out_channels, 16)):
                row = i // grid_size
                col = i % grid_size
                x = layer_idx * 3
                y = (row - grid_size/2) * 0.3
                z = (col - grid_size/2) * 0.3
                positions.append([x, y, z])

        return positions

    def create_connections(self, layer1: Dict, layer2: Dict) -> List[Dict]:
        """Cria conexões visuais entre camadas"""
        connections = []

        # Conecta alguns neurônios (para performance)
        max_connections = min(50, len(layer1['neurons']), len(layer2['neurons']))

        for i in range(min(len(layer1['neurons']), max_connections)):
            for j in range(min(len(layer2['neurons']), max_connections)):
                if np.random.random() < 0.3:  # 30% de chance de conexão
                    connections.append({
                        'from': layer1['neurons'][i],
                        'to': layer2['neurons'][j],
                        'strength': np.random.uniform(0.1, 1.0)
                    })

        return connections

    def calculate_world_bounds(self, layers: List[Dict]) -> Dict:
        """Calcula limites do mundo 3D"""
        if not layers:
            return {'min': [-5, -5, -5], 'max': [5, 5, 5]}

        positions = []
        for layer in layers:
            positions.extend(layer['neurons'])

        if not positions:
            return {'min': [-5, -5, -5], 'max': [5, 5, 5]}

        positions = np.array(positions)
        return {
            'min': positions.min(axis=0).tolist(),
            'max': positions.max(axis=0).tolist()
        }

    def create_ar_interface(self, world: Dict) -> str:
        """Cria interface HTML/JS para experiência AR"""

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Neural Network AR Explorer</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
            <style>
                body {{ margin: 0; overflow: hidden; }}
                #info {{ position: absolute; top: 10px; left: 10px; color: white; font-family: Arial; }}
                .control-panel {{ position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px; }}
                button {{ margin: 5px; padding: 5px 10px; }}
            </style>
        </head>
        <body>
            <div id="info">
                <h3>🧠 Neural Network AR Explorer</h3>
                <p>Posição: <span id="position">0, 0, 0</span></p>
                <p>Camada: <span id="layer">Entrada</span></p>
            </div>

            <div class="control-panel">
                <button onclick="switchView('first_person')">👁️ First Person</button>
                <button onclick="switchView('third_person')">🎥 Third Person</button>
                <button onclick="switchView('god_mode')">🌌 God Mode</button><br>
                <button onclick="teleportToLayer(0)">🏠 Entrada</button>
                <button onclick="teleportToLayer({len(world['layers'])//2})">🏗️ Meio</button>
                <button onclick="teleportToLayer({len(world['layers'])-1})">🎯 Saída</button>
            </div>

            <script>
                // Configuração Three.js
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x0a0a0a);

                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer();
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);

                const controls = new THREE.OrbitControls(camera, renderer.domElement);

                // Dados do mundo
                const worldData = {json.dumps(world)};

                // Criar camadas
                const layers = [];
                worldData.layers.forEach((layerData, index) => {{
                    const layerGroup = new THREE.Group();

                    // Cubo representando a camada
                    const geometry = new THREE.BoxGeometry(...layerData.size);
                    const material = new THREE.MeshLambertMaterial({{ color: layerData.color }});
                    const cube = new THREE.Mesh(geometry, material);
                    cube.position.set(...layerData.position);
                    layerGroup.add(cube);

                    // Neurônios como esferas
                    layerData.neurons.forEach(neuronPos => {{
                        const neuronGeometry = new THREE.SphereGeometry(0.05);
                        const neuronMaterial = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
                        const neuron = new THREE.Mesh(neuronGeometry, neuronMaterial);
                        neuron.position.set(...neuronPos);
                        layerGroup.add(neuron);
                    }});

                    layers.push(layerGroup);
                    scene.add(layerGroup);
                }});

                // Criar conexões
                worldData.connections.forEach(conn => {{
                    const geometry = new THREE.BufferGeometry().setFromPoints([
                        new THREE.Vector3(...conn.from),
                        new THREE.Vector3(...conn.to)
                    ]);
                    const material = new THREE.LineBasicMaterial({{
                        color: 0x888888,
                        opacity: conn.strength,
                        transparent: true
                    }});
                    const line = new THREE.Line(geometry, material);
                    scene.add(line);
                }});

                // Iluminação
                const ambientLight = new THREE.AmbientLight(0x404040);
                scene.add(ambientLight);

                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
                directionalLight.position.set(1, 1, 1);
                scene.add(directionalLight);

                // Variáveis de controle
                let currentView = 'third_person';
                let currentLayerIndex = 0;

                // Funções de controle
                function switchView(mode) {{
                    currentView = mode;
                    if (mode === 'first_person') {{
                        camera.position.set(0, 0, 0);
                        controls.enabled = false;
                    }} else if (mode === 'third_person') {{
                        camera.position.set(5, 5, 5);
                        controls.enabled = true;
                    }} else if (mode === 'god_mode') {{
                        camera.position.set(0, 20, 0);
                        camera.lookAt(0, 0, 0);
                        controls.enabled = true;
                    }}
                }}

                function teleportToLayer(layerIndex) {{
                    if (layerIndex < layers.length) {{
                        const layerPos = worldData.layers[layerIndex].position;
                        if (currentView === 'first_person') {{
                            camera.position.set(...layerPos);
                        }} else {{
                            camera.position.set(
                                layerPos[0] + 5,
                                layerPos[1] + 5,
                                layerPos[2] + 5
                            );
                            camera.lookAt(...layerPos);
                        }}
                        currentLayerIndex = layerIndex;
                        updateInfo();
                    }}
                }}

                function updateInfo() {{
                    document.getElementById('position').textContent =
                        camera.position.x.toFixed(1) + ', ' +
                        camera.position.y.toFixed(1) + ', ' +
                        camera.position.z.toFixed(1);

                    const layerNames = ['Entrada', 'Oculta', 'Saída'];
                    document.getElementById('layer').textContent =
                        worldData.layers[currentLayerIndex]?.name || 'Desconhecida';
                }}

                // Inicializar
                switchView('third_person');
                camera.position.set(10, 10, 10);
                camera.lookAt(0, 0, 0);

                // Loop de animação
                function animate() {{
                    requestAnimationFrame(animate);

                    // Animação sutil das conexões
                    scene.children.forEach(child => {{
                        if (child.type === 'Line') {{
                            child.material.opacity = 0.3 + 0.2 * Math.sin(Date.now() * 0.001);
                        }}
                    }});

                    controls.update();
                    renderer.render(scene, camera);
                    updateInfo();
                }}

                animate();

                // Responsividade
                window.addEventListener('resize', () => {{
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }});
            </script>
        </body>
        </html>
        """

        return html_template

    def create_sample_network(self) -> nn.Module:
        """Cria rede neural de exemplo para demonstração"""
        return nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

def main():
    st.markdown("# 🎭 PyTorch AR/VR Experience")
    st.markdown("Entre dentro da sua rede neural! 🧠✨")

    st.markdown("""
    ## 🌟 O que é esta experiência?

    Esta é uma **experiência imersiva de Realidade Aumentada** onde você pode:

    - 🚶 **Caminhar** através das camadas da rede neural
    - 👁️ **Explorar** neurônios e conexões em 3D
    - 🎮 **Interagir** com diferentes modos de visualização
    - 🏗️ **Entender** como os dados fluem pela rede

    ## 🎯 Modos de Visualização

    - **👁️ First Person**: Caminhe dentro da rede como se estivesse dentro dela
    - **🎥 Third Person**: Visualize de fora com controles orbitais
    - **🌌 God Mode**: Vista aérea completa da arquitetura
    """)

    explorer = ARNeuralExplorer()

    # Seleção de modelo
    model_options = {
        'MLP Simples': explorer.create_sample_network(),
        'Rede Maior': nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1)
        )
    }

    selected_model = st.selectbox("🧠 Selecione uma arquitetura:", list(model_options.keys()))

    if selected_model:
        model = model_options[selected_model]

        # Criar mundo da rede
        with st.spinner("Construindo mundo neural... 🌌"):
            world = explorer.create_network_world(model)

        st.success("🌟 Mundo neural criado! Pronto para exploração!")

        # Informações da rede
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Camadas", len(world['layers']))

        with col2:
            total_neurons = sum(len(layer['neurons']) for layer in world['layers'])
            st.metric("Neurônios Visuais", total_neurons)

        with col3:
            st.metric("Conexões", len(world['connections']))

        # Controles
        st.markdown("### 🎮 Controles da Experiência")

        col4, col5, col6 = st.columns(3)

        with col4:
            view_mode = st.selectbox("Modo de Visualização",
                ["third_person", "first_person", "god_mode"],
                format_func=lambda x: {
                    "first_person": "👁️ First Person",
                    "third_person": "🎥 Third Person",
                    "god_mode": "🌌 God Mode"
                }[x]
            )

        with col5:
            if st.button("🏠 Ir para Entrada"):
                st.info("Teletransportando para camada de entrada...")

        with col6:
            if st.button("🎯 Ir para Saída"):
                st.info("Teletransportando para camada de saída...")

        # Interface AR (simulada com HTML/JS)
        st.markdown("### 🌐 Experiência AR/VR")

        if st.button("🚀 Iniciar Experiência Imersiva", type="primary"):
            st.markdown("""
            **🎭 Entrando no mundo neural...**

            *Em um navegador compatível com WebGL, você veria aqui uma experiência 3D completa!*
            """)

            # Em produção, isso seria:
            # ar_html = explorer.create_ar_interface(world)
            # components.html(ar_html, height=600)

            # Por enquanto, mostramos uma representação 2D
            st.markdown("#### 📊 Representação 2D (Preview)")

            # Criar visualização 2D das camadas
            fig = go.Figure()

            for i, layer in enumerate(world['layers']):
                # Camada como retângulo
                fig.add_shape(
                    type="rect",
                    x0=i*1.5, y0=-0.5, x1=i*1.5+1, y1=0.5,
                    fillcolor=layer['color'],
                    line=dict(color="black"),
                    opacity=0.7
                )

                # Texto da camada
                fig.add_annotation(
                    x=i*1.5+0.5, y=0,
                    text=f"{layer['name']}<br>{layer['type']}",
                    showarrow=False,
                    font=dict(size=10, color="white")
                )

                # Neurônios como pontos
                for j, neuron in enumerate(layer['neurons'][:10]):  # Limita para performance
                    fig.add_trace(go.Scatter(
                        x=[i*1.5 + 0.5],
                        y=[(j-5)*0.1],
                        mode="markers",
                        marker=dict(size=8, color="white", symbol="circle"),
                        showlegend=False
                    ))

            fig.update_layout(
                title="🏗️ Arquitetura Neural - Vista 2D",
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False, showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0.8)',
                paper_bgcolor='rgba(0,0,0,0.8)',
                font=dict(color='white')
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            **💡 Em Desenvolvimento:**
            - Integração completa com Three.js
            - Controles VR/AR nativos
            - Física de movimento dentro da rede
            - Visualização em tempo real do fluxo de dados
            - Interação tátil com neurônios
            """)

        # Instruções
        st.markdown("### 📖 Como Explorar")

        st.markdown("""
        **🎮 Controles Básicos:**
        - **Mouse**: Rotacionar câmera (modo Third Person/God Mode)
        - **Scroll**: Zoom in/out
        - **Botões**: Teletransporte entre camadas
        - **Modos**: Alterne entre perspectivas diferentes

        **🏗️ O que Representa:**
        - **Cubos Coloridos**: Camadas da rede neural
        - **Esferas Brancas**: Neurônios individuais
        - **Linhas**: Conexões entre neurônios
        - **Cores**: Tipos diferentes de camadas

        **🎯 Objetivos de Aprendizado:**
        - Visualizar como dados fluem pela rede
        - Entender profundidade e complexidade
        - Explorar arquiteturas diferentes
        - Desenvolver intuição sobre redes neurais
        """)

if __name__ == "__main__":
    main()