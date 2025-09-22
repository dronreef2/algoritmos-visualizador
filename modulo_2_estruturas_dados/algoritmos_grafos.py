# 🌳 Algoritmos de Grafos
# Implementações com visualização de passos

import time
from collections import deque, defaultdict
import heapq


class Grafo:
    """
    Classe para representação de grafos com métodos de visualização
    """

    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.vertices = set()
        self.arestas = defaultdict(list)
        self.pesos = {}

    def adicionar_vertice(self, v):
        """Adiciona um vértice ao grafo"""
        self.vertices.add(v)

    def adicionar_aresta(self, u, v, peso=1):
        """Adiciona uma aresta ao grafo"""
        self.vertices.add(u)
        self.vertices.add(v)
        self.arestas[u].append(v)
        self.pesos[(u, v)] = peso

        if not self.dirigido:
            self.arestas[v].append(u)
            self.pesos[(v, u)] = peso

    def obter_vizinhos(self, v):
        """Retorna os vizinhos de um vértice"""
        return self.arestas[v]

    def obter_peso(self, u, v):
        """Retorna o peso de uma aresta"""
        return self.pesos.get((u, v), float("inf"))


def bfs_com_passos(grafo, inicio):
    """
    Busca em Largura (BFS) com tracking de passos

    Complexidade: O(V + E)
    Espaço: O(V)
    """
    passos = []
    visitados = set()
    fila = deque([inicio])
    visitados.add(inicio)
    ordem_visita = []

    passos.append(
        {
            "tipo": "inicio",
            "fila": list(fila),
            "visitados": list(visitados),
            "atual": inicio,
            "action": f"Iniciando BFS a partir de {inicio}",
        }
    )

    while fila:
        atual = fila.popleft()
        ordem_visita.append(atual)

        passos.append(
            {
                "tipo": "processando",
                "fila": list(fila),
                "visitados": list(visitados),
                "atual": atual,
                "ordem_visita": ordem_visita.copy(),
                "action": f"Processando vértice {atual}",
            }
        )

        for vizinho in grafo.obter_vizinhos(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

                passos.append(
                    {
                        "tipo": "descoberta",
                        "fila": list(fila),
                        "visitados": list(visitados),
                        "atual": atual,
                        "vizinho": vizinho,
                        "ordem_visita": ordem_visita.copy(),
                        "action": f"Descobriu vizinho {vizinho} de {atual}",
                    }
                )

    passos.append({"tipo": "fim", "ordem_final": ordem_visita, "action": f"BFS completo. Ordem: {ordem_visita}"})

    return ordem_visita, passos


def dfs_com_passos(grafo, inicio):
    """
    Busca em Profundidade (DFS) com tracking de passos

    Complexidade: O(V + E)
    Espaço: O(V)
    """
    passos = []
    visitados = set()
    pilha = [inicio]
    ordem_visita = []

    passos.append(
        {
            "tipo": "inicio",
            "pilha": pilha.copy(),
            "visitados": list(visitados),
            "atual": inicio,
            "action": f"Iniciando DFS a partir de {inicio}",
        }
    )

    while pilha:
        atual = pilha.pop()

        if atual not in visitados:
            visitados.add(atual)
            ordem_visita.append(atual)

            passos.append(
                {
                    "tipo": "visitando",
                    "pilha": pilha.copy(),
                    "visitados": list(visitados),
                    "atual": atual,
                    "ordem_visita": ordem_visita.copy(),
                    "action": f"Visitando vértice {atual}",
                }
            )

            # Adicionar vizinhos na pilha (em ordem reversa para manter ordem)
            vizinhos = grafo.obter_vizinhos(atual)
            for vizinho in reversed(vizinhos):
                if vizinho not in visitados:
                    pilha.append(vizinho)

                    passos.append(
                        {
                            "tipo": "empilhando",
                            "pilha": pilha.copy(),
                            "visitados": list(visitados),
                            "atual": atual,
                            "vizinho": vizinho,
                            "ordem_visita": ordem_visita.copy(),
                            "action": f"Empilhou vizinho {vizinho} de {atual}",
                        }
                    )

    passos.append({"tipo": "fim", "ordem_final": ordem_visita, "action": f"DFS completo. Ordem: {ordem_visita}"})

    return ordem_visita, passos


def dijkstra_com_passos(grafo, inicio):
    """
    Algoritmo de Dijkstra com tracking de passos

    Complexidade: O((V + E) log V)
    Espaço: O(V)
    """
    passos = []
    distancias = {v: float("inf") for v in grafo.vertices}
    distancias[inicio] = 0
    predecessores = {}
    visitados = set()
    heap = [(0, inicio)]

    passos.append(
        {
            "tipo": "inicio",
            "distancias": distancias.copy(),
            "heap": heap.copy(),
            "visitados": list(visitados),
            "action": f"Iniciando Dijkstra a partir de {inicio}",
        }
    )

    while heap:
        dist_atual, atual = heapq.heappop(heap)

        if atual in visitados:
            continue

        visitados.add(atual)

        passos.append(
            {
                "tipo": "processando",
                "atual": atual,
                "dist_atual": dist_atual,
                "distancias": distancias.copy(),
                "visitados": list(visitados),
                "heap": heap.copy(),
                "action": f"Processando {atual} com distância {dist_atual}",
            }
        )

        for vizinho in grafo.obter_vizinhos(atual):
            if vizinho not in visitados:
                nova_dist = distancias[atual] + grafo.obter_peso(atual, vizinho)

                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    predecessores[vizinho] = atual
                    heapq.heappush(heap, (nova_dist, vizinho))

                    passos.append(
                        {
                            "tipo": "relaxamento",
                            "atual": atual,
                            "vizinho": vizinho,
                            "nova_dist": nova_dist,
                            "dist_anterior": distancias[vizinho] if nova_dist != distancias[vizinho] else float("inf"),
                            "distancias": distancias.copy(),
                            "heap": heap.copy(),
                            "action": f"Relaxou aresta {atual}→{vizinho}: distância {nova_dist}",
                        }
                    )

    passos.append(
        {
            "tipo": "fim",
            "distancias_finais": distancias,
            "predecessores": predecessores,
            "action": f"Dijkstra completo. Distâncias: {distancias}",
        }
    )

    return distancias, predecessores, passos


def kruskal_com_passos(grafo):
    """
    Algoritmo de Kruskal (MST) com tracking de passos

    Complexidade: O(E log E)
    Espaço: O(V)
    """
    passos = []

    # Union-Find para detectar ciclos
    pai = {v: v for v in grafo.vertices}
    rank = {v: 0 for v in grafo.vertices}

    def find(x):
        if pai[x] != x:
            pai[x] = find(pai[x])
        return pai[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        pai[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    # Obter todas as arestas ordenadas por peso
    arestas = []
    for u in grafo.vertices:
        for v in grafo.obter_vizinhos(u):
            if not grafo.dirigido and u > v:  # Evitar arestas duplicadas
                continue
            peso = grafo.obter_peso(u, v)
            arestas.append((peso, u, v))

    arestas.sort()

    passos.append(
        {
            "tipo": "inicio",
            "arestas_ordenadas": arestas,
            "componentes": {v: [v] for v in grafo.vertices},
            "action": f"Arestas ordenadas por peso: {arestas}",
        }
    )

    mst = []
    peso_total = 0

    for peso, u, v in arestas:
        # Verificar componentes atuais
        componentes = {}
        for vertice in grafo.vertices:
            raiz = find(vertice)
            if raiz not in componentes:
                componentes[raiz] = []
            componentes[raiz].append(vertice)

        if find(u) != find(v):  # Não forma ciclo
            union(u, v)
            mst.append((u, v, peso))
            peso_total += peso

            passos.append(
                {
                    "tipo": "adicionar",
                    "aresta": (u, v, peso),
                    "mst": mst.copy(),
                    "peso_total": peso_total,
                    "componentes_antes": componentes,
                    "action": f"Adicionou aresta {u}─{v} (peso {peso})",
                }
            )
        else:
            passos.append(
                {
                    "tipo": "rejeitar",
                    "aresta": (u, v, peso),
                    "motivo": "formaria ciclo",
                    "componentes": componentes,
                    "action": f"Rejeitou aresta {u}─{v} (formaria ciclo)",
                }
            )

    passos.append(
        {"tipo": "fim", "mst_final": mst, "peso_total": peso_total, "action": f"MST completo. Peso total: {peso_total}"}
    )

    return mst, peso_total, passos


def a_star_com_passos(grafo, inicio, objetivo, heuristicas=None):
    """
    Algoritmo A* com tracking de passos

    Complexidade: O((V + E) log V) com heap
    Espaço: O(V)

    Args:
        grafo: Instância da classe Grafo
        inicio: Vértice inicial
        objetivo: Vértice objetivo
        heuristicas: Dicionário com heurísticas para cada vértice (opcional)
    """
    if heuristicas is None:
        # Heurística padrão: 0 para todos (torna-se Dijkstra)
        heuristicas = {v: 0 for v in grafo.vertices}

    passos = []
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (0, inicio))  # (f_score, vértice)

    g_score = {v: float("inf") for v in grafo.vertices}
    g_score[inicio] = 0

    f_score = {v: float("inf") for v in grafo.vertices}
    f_score[inicio] = heuristicas.get(inicio, 0)

    predecessores = {v: None for v in grafo.vertices}

    passos.append(
        {
            "fila": [inicio],
            "g_scores": g_score.copy(),
            "f_scores": f_score.copy(),
            "action": f"Inicialização: início={inicio}, objetivo={objetivo}",
        }
    )

    while fila_prioridade:
        _, atual = heapq.heappop(fila_prioridade)

        passos.append(
            {
                "atual": atual,
                "fila": [v for _, v in fila_prioridade],
                "g_scores": g_score.copy(),
                "f_scores": f_score.copy(),
                "action": f"Explorando vértice {atual}",
            }
        )

        if atual == objetivo:
            # Reconstruir caminho
            caminho = []
            atual_caminho = objetivo
            while atual_caminho is not None:
                caminho.append(atual_caminho)
                atual_caminho = predecessores[atual_caminho]
            caminho.reverse()

            passos.append(
                {
                    "caminho_encontrado": caminho,
                    "custo_total": g_score[objetivo],
                    "action": f"Caminho encontrado: {caminho} (custo: {g_score[objetivo]})",
                }
            )

            return caminho, g_score[objetivo], passos

        for vizinho in grafo.obter_vizinhos(atual):
            peso_aresta = grafo.obter_peso(atual, vizinho)
            g_tentativa = g_score[atual] + peso_aresta

            if g_tentativa < g_score[vizinho]:
                predecessores[vizinho] = atual
                g_score[vizinho] = g_tentativa
                f_score[vizinho] = g_tentativa + heuristicas.get(vizinho, 0)

                # Verificar se vizinho já está na fila
                na_fila = any(v == vizinho for _, v in fila_prioridade)
                if not na_fila:
                    heapq.heappush(fila_prioridade, (f_score[vizinho], vizinho))

                passos.append(
                    {
                        "vizinho": vizinho,
                        "g_tentativa": g_tentativa,
                        "f_score": f_score[vizinho],
                        "predecessores": predecessores.copy(),
                        "action": f"Atualizou {vizinho}: g={g_tentativa}, f={f_score[vizinho]}",
                    }
                )

    # Não encontrou caminho
    passos.append(
        {"caminho_nao_encontrado": True, "action": f"Não foi possível encontrar caminho de {inicio} para {objetivo}"}
    )

    return [], float("inf"), passos


def heuristica_euclidiana(posicoes):
    """
    Calcula heurísticas euclidianas para A*

    Args:
        posicoes: Dicionário {vértice: (x, y)}

    Returns:
        Dicionário com heurísticas para cada vértice
    """
    objetivo = max(posicoes.keys())  # Último vértice como objetivo
    obj_x, obj_y = posicoes[objetivo]

    heuristicas = {}
    for v, (x, y) in posicoes.items():
        distancia = ((x - obj_x) ** 2 + (y - obj_y) ** 2) ** 0.5
        heuristicas[v] = distancia

    return heuristicas


def detectar_ciclo_com_passos(grafo):
    """
    Detecção de ciclo usando DFS com tracking de passos

    Complexidade: O(V + E)
    Espaço: O(V)
    """
    passos = []
    cores = {v: "branco" for v in grafo.vertices}  # branco, cinza, preto
    tem_ciclo = False

    def dfs_ciclo(v, passos):
        nonlocal tem_ciclo
        cores[v] = "cinza"

        passos.append({"tipo": "visita", "vertice": v, "cores": cores.copy(), "action": f"Visitando {v} (marcado como cinza)"})

        for vizinho in grafo.obter_vizinhos(v):
            if cores[vizinho] == "cinza":  # Back edge - ciclo detectado
                tem_ciclo = True
                passos.append(
                    {
                        "tipo": "ciclo_detectado",
                        "vertice": v,
                        "vizinho": vizinho,
                        "cores": cores.copy(),
                        "action": f"CICLO detectado: {v}→{vizinho} (back edge)",
                    }
                )
                return True
            elif cores[vizinho] == "branco" and dfs_ciclo(vizinho, passos):
                return True

        cores[v] = "preto"
        passos.append(
            {
                "tipo": "finalizado",
                "vertice": v,
                "cores": cores.copy(),
                "action": f"Finalizou processamento de {v} (marcado como preto)",
            }
        )

        return False

    passos.append({"tipo": "inicio", "cores": cores.copy(), "action": "Iniciando detecção de ciclo com DFS"})

    for vertice in grafo.vertices:
        if cores[vertice] == "branco":
            if dfs_ciclo(vertice, passos):
                break

    passos.append(
        {
            "tipo": "resultado",
            "tem_ciclo": tem_ciclo,
            "cores_finais": cores,
            "action": f'Resultado: {"Ciclo detectado" if tem_ciclo else "Sem ciclos"}',
        }
    )

    return tem_ciclo, passos


def benchmark_grafos():
    """
    Benchmark dos algoritmos de grafos
    """
    # Criar grafo de teste
    g = Grafo(dirigido=False)

    # Adicionar vértices e arestas
    vertices = ["A", "B", "C", "D", "E", "F"]
    for v in vertices:
        g.adicionar_vertice(v)

    arestas = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]

    for u, v, peso in arestas:
        g.adicionar_aresta(u, v, peso)

    resultados = {}

    # Benchmark BFS
    start = time.time()
    _, passos_bfs = bfs_com_passos(g, "A")
    resultados["BFS"] = {"tempo": time.time() - start, "passos": len(passos_bfs)}

    # Benchmark DFS
    start = time.time()
    _, passos_dfs = dfs_com_passos(g, "A")
    resultados["DFS"] = {"tempo": time.time() - start, "passos": len(passos_dfs)}

    # Benchmark Dijkstra
    start = time.time()
    _, _, passos_dijkstra = dijkstra_com_passos(g, "A")
    resultados["Dijkstra"] = {"tempo": time.time() - start, "passos": len(passos_dijkstra)}

    # Benchmark Kruskal
    start = time.time()
    _, _, passos_kruskal = kruskal_com_passos(g)
    resultados["Kruskal"] = {"tempo": time.time() - start, "passos": len(passos_kruskal)}

    return resultados


if __name__ == "__main__":
    # Exemplo de uso
    print("🌳 Testando algoritmos de grafos:")

    # Criar grafo de exemplo
    g = Grafo(dirigido=False)
    vertices = ["A", "B", "C", "D", "E"]
    for v in vertices:
        g.adicionar_vertice(v)

    arestas = [("A", "B", 1), ("A", "C", 4), ("B", "C", 2), ("B", "D", 5), ("C", "D", 1), ("D", "E", 3)]

    for u, v, peso in arestas:
        g.adicionar_aresta(u, v, peso)

    print(f"Grafo criado com {len(g.vertices)} vértices e {sum(len(adj) for adj in g.arestas.values()) // 2} arestas")

    # Testar BFS
    print("\n🔍 BFS a partir de A:")
    ordem_bfs, passos_bfs = bfs_com_passos(g, "A")
    print(f"Ordem de visita: {ordem_bfs}")
    print(f"Passos executados: {len(passos_bfs)}")

    # Testar Dijkstra
    print("\n🛣️ Dijkstra a partir de A:")
    distancias, predecessores, passos_dijkstra = dijkstra_com_passos(g, "A")
    print(f"Distâncias: {distancias}")
    print(f"Passos executados: {len(passos_dijkstra)}")

    # Testar Kruskal
    print("\n🌲 MST usando Kruskal:")
    mst, peso_total, passos_kruskal = kruskal_com_passos(g)
    print(f"MST: {mst}")
    print(f"Peso total: {peso_total}")
    print(f"Passos executados: {len(passos_kruskal)}")
