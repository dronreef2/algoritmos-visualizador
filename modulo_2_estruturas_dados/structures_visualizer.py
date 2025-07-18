"""
🎨 VISUALIZADOR DE ESTRUTURAS DE DADOS AVANÇADAS
==============================================

Este módulo fornece visualizações interativas para estruturas de dados avançadas,
incluindo animações em tempo real e análise de performance.

Componentes:
- Renderer para Heap (árvore binária)
- Visualizador de Trie (árvore de prefixos)
- Animação de Union-Find
- Segment Tree interativa
- LRU Cache visual
- Graph com algoritmos
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np
import networkx as nx
from typing import List, Dict, Any, Optional, Tuple
import math
from dataclasses import dataclass
import colorsys

# ============================================================================
# 🎨 CONFIGURAÇÕES VISUAIS
# ============================================================================

@dataclass
class VisualConfig:
    """Configurações visuais para os renderizadores."""
    
    primary_color: str = '#2E86AB'
    secondary_color: str = '#A23B72'
    success_color: str = '#F18F01'
    warning_color: str = '#C73E1D'
    background_color: str = '#F8F9FA'
    text_color: str = '#212529'
    
    # Tamanhos
    node_size: int = 800
    edge_width: float = 2.0
    font_size: int = 12
    title_font_size: int = 16
    
    # Animação
    animation_speed: int = 1000  # ms
    highlight_alpha: float = 0.8
    normal_alpha: float = 0.6

class AdvancedStructuresVisualizer:
    """Visualizador principal para estruturas avançadas."""
    
    def __init__(self, figsize=(16, 12)):
        self.fig = plt.figure(figsize=figsize)
        self.config = VisualConfig()
        
        # Criar grid de subplots
        self.gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Definir subplots
        self.ax_main = self.fig.add_subplot(self.gs[0:2, 0:2])  # Visualização principal
        self.ax_info = self.fig.add_subplot(self.gs[0, 2])      # Informações
        self.ax_operations = self.fig.add_subplot(self.gs[1, 2])  # Operações
        self.ax_complexity = self.fig.add_subplot(self.gs[2, :])  # Análise de complexidade
        
        self.fig.suptitle('🏗️ Advanced Data Structures Visualizer', 
                         fontsize=self.config.title_font_size, fontweight='bold')
        
        # Estado atual
        self.current_structure = None
        self.current_data = None
        self.animation_steps = []
        
    def visualize_heap(self, heap_data: Dict[str, Any]):
        """Visualiza heap como árvore binária."""
        self.current_structure = "heap"
        self.current_data = heap_data
        
        # Limpar axes
        self.ax_main.clear()
        self.ax_info.clear()
        self.ax_operations.clear()
        
        heap = heap_data['heap']
        is_max_heap = heap_data['is_max_heap']
        
        self.ax_main.set_title(f'🔺 {"Max" if is_max_heap else "Min"} Heap', 
                              fontweight='bold')
        
        if not heap:
            self.ax_main.text(0.5, 0.5, 'Heap Vazio', 
                            transform=self.ax_main.transAxes,
                            ha='center', va='center', fontsize=14)
            return
        
        # Calcular posições dos nós
        positions = self._calculate_heap_positions(heap)
        
        # Desenhar nós
        for i, (x, y) in enumerate(positions):
            if i < len(heap):
                circle = Circle((x, y), 0.3, 
                              color=self.config.primary_color, 
                              alpha=self.config.normal_alpha)
                self.ax_main.add_patch(circle)
                
                # Adicionar valor
                self.ax_main.text(x, y, str(heap[i]), 
                                ha='center', va='center', 
                                fontsize=self.config.font_size, 
                                fontweight='bold', color='white')
        
        # Desenhar arestas
        for i in range(len(heap)):
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < len(heap):
                x1, y1 = positions[i]
                x2, y2 = positions[left_child]
                self.ax_main.plot([x1, x2], [y1, y2], 
                                color=self.config.text_color, 
                                linewidth=self.config.edge_width, alpha=0.7)
            
            if right_child < len(heap):
                x1, y1 = positions[i]
                x2, y2 = positions[right_child]
                self.ax_main.plot([x1, x2], [y1, y2], 
                                color=self.config.text_color, 
                                linewidth=self.config.edge_width, alpha=0.7)
        
        self.ax_main.set_xlim(-4, 4)
        self.ax_main.set_ylim(-4, 1)
        self.ax_main.set_aspect('equal')
        self.ax_main.axis('off')
        
        # Informações
        self._render_heap_info(heap_data)
        
        # Operações
        self._render_operations(heap_data.get('operations', []))
    
    def _calculate_heap_positions(self, heap: List[int]) -> List[Tuple[float, float]]:
        """Calcula posições dos nós do heap."""
        positions = []
        
        for i in range(len(heap)):
            level = int(math.log2(i + 1))
            position_in_level = i - (2**level - 1)
            total_in_level = 2**level
            
            # Calcular posição x
            if total_in_level == 1:
                x = 0
            else:
                x = -3 + (6 * position_in_level / (total_in_level - 1))
            
            # Calcular posição y
            y = -level * 0.8
            
            positions.append((x, y))
        
        return positions
    
    def visualize_trie(self, trie_data: Dict[str, Any]):
        """Visualiza Trie como árvore de prefixos."""
        self.current_structure = "trie"
        self.current_data = trie_data
        
        # Limpar axes
        self.ax_main.clear()
        self.ax_info.clear()
        self.ax_operations.clear()
        
        self.ax_main.set_title('🌳 Trie (Prefix Tree)', fontweight='bold')
        
        # Usar NetworkX para layout da árvore
        G = nx.DiGraph()
        
        # Construir grafo a partir dos dados da Trie
        self._build_trie_graph(G, trie_data['tree_state']['root'], 'root')
        
        if G.number_of_nodes() == 0:
            self.ax_main.text(0.5, 0.5, 'Trie Vazia', 
                            transform=self.ax_main.transAxes,
                            ha='center', va='center', fontsize=14)
            return
        
        # Layout hierárquico
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Desenhar nós
        node_colors = []
        for node in G.nodes():
            if G.nodes[node].get('is_end_of_word', False):
                node_colors.append(self.config.success_color)
            else:
                node_colors.append(self.config.primary_color)
        
        nx.draw_networkx_nodes(G, pos, ax=self.ax_main,
                              node_color=node_colors,
                              node_size=self.config.node_size,
                              alpha=self.config.normal_alpha)
        
        # Desenhar arestas
        nx.draw_networkx_edges(G, pos, ax=self.ax_main,
                              edge_color=self.config.text_color,
                              width=self.config.edge_width,
                              alpha=0.7)
        
        # Adicionar labels
        labels = {node: node.split('_')[-1] if '_' in node else node 
                 for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, ax=self.ax_main,
                               font_size=self.config.font_size,
                               font_weight='bold')
        
        # Adicionar labels das arestas
        edge_labels = nx.get_edge_attributes(G, 'char')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=self.ax_main,
                                    font_size=self.config.font_size - 2)
        
        self.ax_main.set_title('🌳 Trie (Prefix Tree)', fontweight='bold')
        self.ax_main.axis('off')
        
        # Informações
        self._render_trie_info(trie_data)
        
        # Operações
        self._render_operations(trie_data.get('operations', []))
    
    def _build_trie_graph(self, G: nx.DiGraph, node_data: Dict, node_id: str):
        """Constrói grafo recursivamente a partir dos dados da Trie."""
        G.add_node(node_id, **node_data)
        
        for char, child_data in node_data.get('children', {}).items():
            child_id = f"{node_id}_{char}"
            self._build_trie_graph(G, child_data, child_id)
            G.add_edge(node_id, child_id, char=char)
    
    def visualize_union_find(self, uf_data: Dict[str, Any]):
        """Visualiza Union-Find como componentes conectados."""
        self.current_structure = "union_find"
        self.current_data = uf_data
        
        # Limpar axes
        self.ax_main.clear()
        self.ax_info.clear()
        self.ax_operations.clear()
        
        self.ax_main.set_title('🤝 Union-Find (Disjoint Set)', fontweight='bold')
        
        parent = uf_data['parent_state']
        n = len(parent)
        
        # Criar grafo das conexões
        G = nx.Graph()
        
        # Adicionar nós
        for i in range(n):
            G.add_node(i)
        
        # Adicionar arestas baseadas na estrutura Union-Find
        for i in range(n):
            if parent[i] != i:
                G.add_edge(i, parent[i])
        
        # Layout circular para cada componente
        components = []
        visited = set()
        
        for i in range(n):
            if i not in visited:
                component = []
                stack = [i]
                
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        component.append(node)
                        
                        # Adicionar filhos
                        for j in range(n):
                            if parent[j] == node and j not in visited:
                                stack.append(j)
                
                components.append(component)
        
        # Posicionar componentes
        pos = {}
        component_radius = 1.5
        
        for comp_idx, component in enumerate(components):
            # Posição central do componente
            angle = 2 * math.pi * comp_idx / len(components)
            center_x = 3 * math.cos(angle)
            center_y = 3 * math.sin(angle)
            
            # Posicionar nós do componente
            for node_idx, node in enumerate(component):
                if len(component) == 1:
                    pos[node] = (center_x, center_y)
                else:
                    node_angle = 2 * math.pi * node_idx / len(component)
                    x = center_x + component_radius * math.cos(node_angle)
                    y = center_y + component_radius * math.sin(node_angle)
                    pos[node] = (x, y)
        
        # Desenhar nós
        nx.draw_networkx_nodes(G, pos, ax=self.ax_main,
                              node_color=self.config.primary_color,
                              node_size=self.config.node_size,
                              alpha=self.config.normal_alpha)
        
        # Desenhar arestas
        nx.draw_networkx_edges(G, pos, ax=self.ax_main,
                              edge_color=self.config.text_color,
                              width=self.config.edge_width,
                              alpha=0.7)
        
        # Adicionar labels
        nx.draw_networkx_labels(G, pos, ax=self.ax_main,
                               font_size=self.config.font_size,
                               font_weight='bold')
        
        self.ax_main.axis('off')
        
        # Informações
        self._render_union_find_info(uf_data)
        
        # Operações
        self._render_operations(uf_data.get('operations', []))
    
    def visualize_segment_tree(self, seg_tree_data: Dict[str, Any]):
        """Visualiza Segment Tree."""
        self.current_structure = "segment_tree"
        self.current_data = seg_tree_data
        
        # Limpar axes
        self.ax_main.clear()
        self.ax_info.clear()
        self.ax_operations.clear()
        
        self.ax_main.set_title('🎯 Segment Tree', fontweight='bold')
        
        tree = seg_tree_data['tree_state']['tree']
        array = seg_tree_data['tree_state']['array']
        operation = seg_tree_data['tree_state']['operation']
        
        # Visualizar apenas parte relevante da árvore
        n = len(array)
        relevant_size = 4 * n
        
        # Calcular posições para árvore binária
        positions = self._calculate_segment_tree_positions(relevant_size)
        
        # Desenhar nós com valores
        for i in range(min(relevant_size, len(tree))):
            if tree[i] != 0:  # Apenas nós com valores
                x, y = positions[i]
                
                circle = Circle((x, y), 0.2, 
                              color=self.config.secondary_color, 
                              alpha=self.config.normal_alpha)
                self.ax_main.add_patch(circle)
                
                # Adicionar valor
                self.ax_main.text(x, y, str(tree[i]), 
                                ha='center', va='center', 
                                fontsize=self.config.font_size - 2, 
                                fontweight='bold', color='white')
        
        # Mostrar array original na parte inferior
        array_y = -4
        for i, val in enumerate(array):
            x = -3 + (6 * i / (len(array) - 1)) if len(array) > 1 else 0
            
            rect = Rectangle((x - 0.2, array_y - 0.2), 0.4, 0.4,
                           color=self.config.success_color,
                           alpha=self.config.normal_alpha)
            self.ax_main.add_patch(rect)
            
            self.ax_main.text(x, array_y, str(val), 
                            ha='center', va='center', 
                            fontsize=self.config.font_size, 
                            fontweight='bold')
        
        self.ax_main.set_xlim(-4, 4)
        self.ax_main.set_ylim(-5, 1)
        self.ax_main.axis('off')
        
        # Informações
        self._render_segment_tree_info(seg_tree_data)
        
        # Operações
        self._render_operations(seg_tree_data.get('operations', []))
    
    def _calculate_segment_tree_positions(self, size: int) -> List[Tuple[float, float]]:
        """Calcula posições para Segment Tree."""
        positions = []
        
        for i in range(size):
            if i == 0:
                positions.append((0, 0))
            else:
                level = int(math.log2(i + 1))
                position_in_level = i - (2**level - 1)
                total_in_level = 2**level
                
                if total_in_level == 1:
                    x = 0
                else:
                    x = -3 + (6 * position_in_level / (total_in_level - 1))
                
                y = -level * 0.8
                positions.append((x, y))
        
        return positions
    
    def visualize_lru_cache(self, lru_data: Dict[str, Any]):
        """Visualiza LRU Cache."""
        self.current_structure = "lru_cache"
        self.current_data = lru_data
        
        # Limpar axes
        self.ax_main.clear()
        self.ax_info.clear()
        self.ax_operations.clear()
        
        self.ax_main.set_title('💾 LRU Cache', fontweight='bold')
        
        cache_state = lru_data['cache_state']
        order = cache_state['order']
        capacity = cache_state['capacity']
        
        if not order:
            self.ax_main.text(0.5, 0.5, 'Cache Vazio', 
                            transform=self.ax_main.transAxes,
                            ha='center', va='center', fontsize=14)
            return
        
        # Desenhar lista duplamente ligada
        y_pos = 0
        x_spacing = 1.5
        
        for i, item in enumerate(order):
            x_pos = -2 + i * x_spacing
            
            # Desenhar nó
            rect = FancyBboxPatch((x_pos - 0.4, y_pos - 0.3), 0.8, 0.6,
                                 boxstyle="round,pad=0.1",
                                 facecolor=self.config.primary_color,
                                 alpha=self.config.normal_alpha)
            self.ax_main.add_patch(rect)
            
            # Adicionar chave:valor
            self.ax_main.text(x_pos, y_pos, f"{item['key']}:{item['value']}", 
                            ha='center', va='center', 
                            fontsize=self.config.font_size, 
                            fontweight='bold', color='white')
            
            # Desenhar seta para próximo
            if i < len(order) - 1:
                arrow = patches.FancyArrowPatch((x_pos + 0.4, y_pos), 
                                             (x_pos + x_spacing - 0.4, y_pos),
                                             arrowstyle='->', 
                                             mutation_scale=20,
                                             color=self.config.text_color)
                self.ax_main.add_patch(arrow)
        
        # Indicar MRU e LRU
        if order:
            self.ax_main.text(-2, 0.8, 'MRU', ha='center', va='center', 
                            fontsize=self.config.font_size, 
                            fontweight='bold', color=self.config.success_color)
            
            last_x = -2 + (len(order) - 1) * x_spacing
            self.ax_main.text(last_x, 0.8, 'LRU', ha='center', va='center', 
                            fontsize=self.config.font_size, 
                            fontweight='bold', color=self.config.warning_color)
        
        self.ax_main.set_xlim(-3, 3)
        self.ax_main.set_ylim(-1, 1.5)
        self.ax_main.axis('off')
        
        # Informações
        self._render_lru_info(lru_data)
        
        # Operações
        self._render_operations(lru_data.get('operations', []))
    
    def visualize_graph(self, graph_data: Dict[str, Any]):
        """Visualiza grafo com algoritmos."""
        self.current_structure = "graph"
        self.current_data = graph_data
        
        # Limpar axes
        self.ax_main.clear()
        self.ax_info.clear()
        self.ax_operations.clear()
        
        self.ax_main.set_title('📊 Graph', fontweight='bold')
        
        # Criar NetworkX graph
        G = nx.DiGraph() if graph_data['graph_state']['directed'] else nx.Graph()
        
        # Adicionar nós
        vertices = graph_data['graph_state']['vertices']
        for i in range(vertices):
            G.add_node(i)
        
        # Adicionar arestas
        adj_list = graph_data['graph_state']['adj_list']
        for u, neighbors in adj_list.items():
            for v, weight in neighbors:
                G.add_edge(u, v, weight=weight)
        
        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Desenhar nós
        nx.draw_networkx_nodes(G, pos, ax=self.ax_main,
                              node_color=self.config.primary_color,
                              node_size=self.config.node_size,
                              alpha=self.config.normal_alpha)
        
        # Desenhar arestas
        nx.draw_networkx_edges(G, pos, ax=self.ax_main,
                              edge_color=self.config.text_color,
                              width=self.config.edge_width,
                              alpha=0.7)
        
        # Adicionar labels
        nx.draw_networkx_labels(G, pos, ax=self.ax_main,
                               font_size=self.config.font_size,
                               font_weight='bold')
        
        # Adicionar pesos das arestas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=self.ax_main,
                                    font_size=self.config.font_size - 2)
        
        self.ax_main.axis('off')
        
        # Informações
        self._render_graph_info(graph_data)
        
        # Operações
        self._render_operations(graph_data.get('operations', []))
    
    def _render_heap_info(self, heap_data: Dict[str, Any]):
        """Renderiza informações do heap."""
        self.ax_info.set_title('ℹ️ Heap Info', fontweight='bold')
        
        info_text = f"Tipo: {'Max' if heap_data['is_max_heap'] else 'Min'} Heap\n"
        info_text += f"Tamanho: {heap_data['size']}\n"
        info_text += f"Operações: {len(heap_data.get('operations', []))}\n"
        
        if heap_data['heap']:
            info_text += f"Raiz: {heap_data['heap'][0]}\n"
        
        self.ax_info.text(0.05, 0.95, info_text, 
                         transform=self.ax_info.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=self.config.background_color))
        
        self.ax_info.axis('off')
    
    def _render_trie_info(self, trie_data: Dict[str, Any]):
        """Renderiza informações da Trie."""
        self.ax_info.set_title('ℹ️ Trie Info', fontweight='bold')
        
        info_text = f"Total de Palavras: {trie_data['tree_state']['total_words']}\n"
        info_text += f"Operações: {len(trie_data.get('operations', []))}\n"
        
        self.ax_info.text(0.05, 0.95, info_text, 
                         transform=self.ax_info.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=self.config.background_color))
        
        self.ax_info.axis('off')
    
    def _render_union_find_info(self, uf_data: Dict[str, Any]):
        """Renderiza informações do Union-Find."""
        self.ax_info.set_title('ℹ️ Union-Find Info', fontweight='bold')
        
        info_text = f"Elementos: {len(uf_data['parent_state'])}\n"
        info_text += f"Componentes: {uf_data['components']}\n"
        info_text += f"Operações: {len(uf_data.get('operations', []))}\n"
        
        self.ax_info.text(0.05, 0.95, info_text, 
                         transform=self.ax_info.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=self.config.background_color))
        
        self.ax_info.axis('off')
    
    def _render_segment_tree_info(self, seg_tree_data: Dict[str, Any]):
        """Renderiza informações da Segment Tree."""
        self.ax_info.set_title('ℹ️ Segment Tree Info', fontweight='bold')
        
        tree_state = seg_tree_data['tree_state']
        info_text = f"Operação: {tree_state['operation']}\n"
        info_text += f"Array Size: {len(tree_state['array'])}\n"
        info_text += f"Operações: {len(seg_tree_data.get('operations', []))}\n"
        
        self.ax_info.text(0.05, 0.95, info_text, 
                         transform=self.ax_info.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=self.config.background_color))
        
        self.ax_info.axis('off')
    
    def _render_lru_info(self, lru_data: Dict[str, Any]):
        """Renderiza informações do LRU Cache."""
        self.ax_info.set_title('ℹ️ LRU Cache Info', fontweight='bold')
        
        cache_state = lru_data['cache_state']
        info_text = f"Capacidade: {cache_state['capacity']}\n"
        info_text += f"Tamanho: {cache_state['size']}\n"
        info_text += f"Operações: {len(lru_data.get('operations', []))}\n"
        
        self.ax_info.text(0.05, 0.95, info_text, 
                         transform=self.ax_info.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=self.config.background_color))
        
        self.ax_info.axis('off')
    
    def _render_graph_info(self, graph_data: Dict[str, Any]):
        """Renderiza informações do grafo."""
        self.ax_info.set_title('ℹ️ Graph Info', fontweight='bold')
        
        graph_state = graph_data['graph_state']
        info_text = f"Vértices: {graph_state['vertices']}\n"
        info_text += f"Arestas: {graph_state['edge_count']}\n"
        info_text += f"Direcionado: {'Sim' if graph_state['directed'] else 'Não'}\n"
        info_text += f"Operações: {len(graph_data.get('operations', []))}\n"
        
        self.ax_info.text(0.05, 0.95, info_text, 
                         transform=self.ax_info.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor=self.config.background_color))
        
        self.ax_info.axis('off')
    
    def _render_operations(self, operations: List[Dict[str, Any]]):
        """Renderiza histórico de operações."""
        self.ax_operations.set_title('📋 Operações', fontweight='bold')
        
        if not operations:
            self.ax_operations.text(0.5, 0.5, 'Nenhuma operação', 
                                  transform=self.ax_operations.transAxes,
                                  ha='center', va='center', fontsize=10)
            self.ax_operations.axis('off')
            return
        
        # Mostrar últimas 5 operações
        recent_ops = operations[-5:]
        
        y_positions = np.linspace(0.9, 0.1, len(recent_ops))
        
        for i, (op, y) in enumerate(zip(recent_ops, y_positions)):
            op_text = f"{len(operations) - len(recent_ops) + i + 1}. {op['operation']}"
            
            self.ax_operations.text(0.05, y, op_text, 
                                  transform=self.ax_operations.transAxes,
                                  va='center', ha='left', fontsize=9,
                                  bbox=dict(boxstyle="round,pad=0.2", 
                                          facecolor=self.config.primary_color,
                                          alpha=0.3))
        
        self.ax_operations.axis('off')
    
    def render_complexity_analysis(self, structure_type: str, operations: List[str]):
        """Renderiza análise de complexidade."""
        self.ax_complexity.clear()
        self.ax_complexity.set_title('📊 Análise de Complexidade', fontweight='bold')
        
        # Complexidades conhecidas
        complexity_data = {
            'heap': {
                'insert': 'O(log n)',
                'extract': 'O(log n)',
                'peek': 'O(1)',
                'build': 'O(n)'
            },
            'trie': {
                'insert': 'O(m)',
                'search': 'O(m)',
                'delete': 'O(m)',
                'prefix': 'O(p + n)'
            },
            'union_find': {
                'find': 'O(α(n))',
                'union': 'O(α(n))',
                'connected': 'O(α(n))'
            },
            'segment_tree': {
                'query': 'O(log n)',
                'update': 'O(log n)',
                'build': 'O(n)'
            },
            'lru_cache': {
                'get': 'O(1)',
                'put': 'O(1)'
            },
            'graph': {
                'dfs': 'O(V + E)',
                'bfs': 'O(V + E)',
                'add_edge': 'O(1)'
            }
        }
        
        if structure_type not in complexity_data:
            return
        
        complexities = complexity_data[structure_type]
        
        # Gráfico de barras das complexidades
        operations_list = list(complexities.keys())
        complexity_values = []
        
        # Converter complexidades para valores numéricos para visualização
        complexity_to_value = {
            'O(1)': 1,
            'O(log n)': 2,
            'O(α(n))': 1.5,
            'O(m)': 3,
            'O(n)': 4,
            'O(p + n)': 5,
            'O(V + E)': 6
        }
        
        for op in operations_list:
            complexity_values.append(complexity_to_value.get(complexities[op], 3))
        
        bars = self.ax_complexity.bar(operations_list, complexity_values,
                                    color=self.config.primary_color,
                                    alpha=self.config.normal_alpha)
        
        # Adicionar labels das complexidades
        for bar, op in zip(bars, operations_list):
            height = bar.get_height()
            self.ax_complexity.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                  complexities[op],
                                  ha='center', va='bottom', fontweight='bold')
        
        self.ax_complexity.set_ylabel('Complexidade Relativa')
        self.ax_complexity.set_xlabel('Operações')
        self.ax_complexity.set_title(f'Complexidade - {structure_type.title()}')
        
        # Rotacionar labels se necessário
        plt.setp(self.ax_complexity.get_xticklabels(), rotation=45, ha='right')
    
    def get_figure(self):
        """Retorna a figura para exibição."""
        return self.fig

# ============================================================================
# 🧪 FUNÇÕES DE TESTE
# ============================================================================

def test_visualizer():
    """Testa o visualizador de estruturas avançadas."""
    print("🎨 TESTANDO VISUALIZADOR DE ESTRUTURAS AVANÇADAS")
    print("=" * 50)
    
    # Importar estruturas para teste
    from estruturas_avancadas import AdvancedHeap, Trie, UnionFind
    
    # Criar visualizador
    visualizer = AdvancedStructuresVisualizer()
    
    # Teste 1: Heap
    print("\n🔺 Teste 1: Heap")
    heap = AdvancedHeap(is_max_heap=False)
    values = [4, 1, 7, 3, 8, 5]
    
    for val in values:
        heap.insert(val)
    
    heap_data = heap.get_visualization_data()
    visualizer.visualize_heap(heap_data)
    visualizer.render_complexity_analysis('heap', ['insert', 'extract', 'peek'])
    
    print(f"✅ Heap visualizado: {heap_data['heap']}")
    
    # Teste 2: Trie
    print("\n🌳 Teste 2: Trie")
    trie = Trie()
    words = ["app", "apple", "application"]
    
    for word in words:
        trie.insert(word)
    
    trie_data = {
        'tree_state': trie._get_tree_state(),
        'operations': trie.operations
    }
    
    visualizer.visualize_trie(trie_data)
    
    print(f"✅ Trie visualizada: {len(words)} palavras")
    
    # Teste 3: Union-Find
    print("\n🤝 Teste 3: Union-Find")
    uf = UnionFind(6)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(4, 5)
    
    uf_data = {
        'parent_state': uf.parent,
        'rank_state': uf.rank,
        'components': uf.components,
        'operations': uf.operations
    }
    
    visualizer.visualize_union_find(uf_data)
    
    print(f"✅ Union-Find visualizado: {uf.components} componentes")
    
    plt.tight_layout()
    return visualizer.get_figure()

if __name__ == "__main__":
    fig = test_visualizer()
    plt.show()
