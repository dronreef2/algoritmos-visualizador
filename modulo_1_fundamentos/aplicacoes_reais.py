"""
🚀 APLICAÇÕES REAIS - MÓDULO 1: FUNDAMENTOS
===============================================

Este arquivo contém implementações de casos de uso reais e funcionais
para os algoritmos fundamentais do Módulo 1.

Algoritmos cobertos:
- Busca Binária: Sistema de busca em logs, versionamento, agendamento
- Dois Ponteiros: Detecção de fraudes, análise de DNA, compressão
- BFS: Rede social, roteamento, análise de dependências  
- Backtracking: Planejamento, configuração, otimização

Complexidades: O(log n), O(n), O(V+E), Exponencial
"""

import bisect
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Set, Any
from collections import deque, defaultdict
import heapq

# ============================================================================
# 🔍 BUSCA BINÁRIA - APLICAÇÕES REAIS
# ============================================================================

class SistemaBuscaLogs:
    """
    Sistema real de busca em logs por timestamp.
    Usado em sistemas de monitoramento e debugging.
    
    Complexidade: O(log n) para busca
    """
    
    def __init__(self):
        self.logs = []  # Lista de (timestamp, mensagem)
    
    def adicionar_log(self, timestamp: float, mensagem: str, nivel: str = None):
        """Adiciona log mantendo ordem cronológica."""
        # Se nivel for fornecido e a mensagem não incluir o nível, adicionar
        if nivel and not any(level in mensagem.upper() for level in ['INFO:', 'ERROR:', 'DEBUG:', 'WARN:', 'FATAL:']):
            mensagem_completa = f"{nivel.upper()}: {mensagem}"
        else:
            mensagem_completa = mensagem
        
        # Inserção ordenada usando busca binária
        pos = bisect.bisect_left(self.logs, (timestamp, ""))
        self.logs.insert(pos, (timestamp, mensagem_completa))
    
    def buscar_logs_periodo(self, inicio: float, fim: float) -> List[Tuple[float, str]]:
        """
        Busca logs em um período específico.
        
        Aplicação Real: Debugging de sistemas em produção
        """
        # Usar busca binária para encontrar limites
        pos_inicio = bisect.bisect_left(self.logs, (inicio, ""))
        pos_fim = bisect.bisect_right(self.logs, (fim, ""))
        
        return self.logs[pos_inicio:pos_fim]
    
    def buscar_primeiro_erro_apos(self, timestamp: float) -> Optional[Tuple[float, str]]:
        """
        Encontra primeiro erro após um timestamp.
        
        Aplicação Real: Análise de cascata de falhas
        """
        pos = bisect.bisect_left(self.logs, (timestamp, ""))
        
        for i in range(pos, len(self.logs)):
            if "ERROR" in self.logs[i][1] or "FATAL" in self.logs[i][1]:
                return self.logs[i]
        
        return None

class SistemaVersionamento:
    """
    Sistema de versionamento com busca binária para releases.
    Baseado em como Git encontra commits específicos.
    
    Complexidade: O(log n) para busca de versão
    """
    
    def __init__(self):
        self.versions = []  # Lista ordenada de (versao, dados)
    
    def adicionar_versao(self, versao: str, dados: dict):
        """Adiciona nova versão mantendo ordem."""
        versao_num = self._versao_para_numero(versao)
        pos = bisect.bisect_left(self.versions, (versao_num, versao, dados))
        self.versions.insert(pos, (versao_num, versao, dados))
    
    def _versao_para_numero(self, versao: str) -> int:
        """Converte versão string para número comparável."""
        # Remove prefixo 'v' se existir
        versao_limpa = versao.lstrip('v')
        partes = versao_limpa.split('.')
        return sum(int(parte) * (1000 ** (2-i)) for i, parte in enumerate(partes[:3]))
    
    def criar_versao(self, versao: str, descricao: str):
        """Alias para adicionar_versao com interface simplificada."""
        dados = {"tag": versao, "descricao": descricao, "timestamp": time.time()}
        self.adicionar_versao(versao, dados)
    
    def buscar_versao(self, versao: str) -> Optional[dict]:
        """
        Busca versão específica no sistema.
        
        Aplicação Real: Deploy de versões específicas
        """
        num_versao = self._versao_para_numero(versao)
        pos = bisect.bisect_left(self.versions, (num_versao, "", {}))
        
        if pos < len(self.versions) and self.versions[pos][0] == num_versao:
            return self.versions[pos][2]
        return None

    def buscar_versao_compativel(self, versao_minima: str) -> Optional[Tuple[str, dict]]:
        """
        Encontra primeira versão >= versão mínima.
        
        Aplicação Real: Gerenciamento de dependências
        """
        num_min = self._versao_para_numero(versao_minima)
        pos = bisect.bisect_left(self.versions, (num_min, "", {}))
        
        if pos < len(self.versions):
            return self.versions[pos][1], self.versions[pos][2]
        return None

class AgendadorEventos:
    """
    Sistema de agendamento com busca binária para otimização.
    Usado em calendários e sistemas de reserva.
    
    Complexidade: O(log n) para inserção, O(log n) para busca
    """
    
    def __init__(self):
        self.eventos = []  # Lista de (inicio, fim, descricao)
    
    def agendar_evento(self, inicio, fim, descricao: str) -> bool:
        """
        Agenda evento se não houver conflito.
        Aceita datetime ou timestamp.
        
        Aplicação Real: Sistema de reservas de salas
        """
        # Converter para datetime se necessário
        if isinstance(inicio, (int, float)):
            inicio = datetime.fromtimestamp(inicio)
        if isinstance(fim, (int, float)):
            fim = datetime.fromtimestamp(fim)
            
        # Verificar conflitos usando busca binária
        if self._tem_conflito(inicio, fim):
            return False
        
        # Inserir em posição ordenada
        evento = (inicio.timestamp(), fim.timestamp(), descricao)
        pos = bisect.bisect_left(self.eventos, evento)
        self.eventos.insert(pos, evento)
        return True
        return True
    
    def _tem_conflito(self, inicio: datetime, fim: datetime) -> bool:
        """Verifica se há conflito com eventos existentes."""
        inicio_ts = inicio.timestamp()
        fim_ts = fim.timestamp()
        
        # Buscar posição de inserção
        pos = bisect.bisect_left(self.eventos, (inicio_ts, 0, ""))
        
        # Verificar eventos vizinhos
        if pos > 0:
            # Evento anterior
            if self.eventos[pos-1][1] > inicio_ts:
                return True
        
        if pos < len(self.eventos):
            # Próximo evento
            if self.eventos[pos][0] < fim_ts:
                return True
        
        return False
    
    def eventos_do_dia(self, data: datetime) -> List[Tuple[datetime, datetime, str]]:
        """
        Retorna eventos de um dia específico.
        
        Aplicação Real: Interface de calendário
        """
        inicio_dia = data.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_dia = inicio_dia + timedelta(days=1)
        
        inicio_ts = inicio_dia.timestamp()
        fim_ts = fim_dia.timestamp()
        
        # Buscar range usando busca binária
        pos_inicio = bisect.bisect_left(self.eventos, (inicio_ts, 0, ""))
        pos_fim = bisect.bisect_left(self.eventos, (fim_ts, 0, ""))
        
        resultado = []
        for evento in self.eventos[pos_inicio:pos_fim]:
            inicio_dt = datetime.fromtimestamp(evento[0])
            fim_dt = datetime.fromtimestamp(evento[1])
            resultado.append((inicio_dt, fim_dt, evento[2]))
        
        return resultado
    
    def verificar_conflitos(self) -> List[Tuple]:
        """
        Verifica todos os conflitos existentes entre eventos.
        
        Aplicação Real: Validação de agenda
        """
        conflitos = []
        for i in range(len(self.eventos) - 1):
            evento_atual = self.eventos[i]
            evento_proximo = self.eventos[i + 1]
            
            # Se fim do evento atual > início do próximo = conflito
            if evento_atual[1] > evento_proximo[0]:
                conflitos.append((evento_atual, evento_proximo))
        
        return conflitos

# ============================================================================
# 👥 DOIS PONTEIROS - APLICAÇÕES REAIS  
# ============================================================================

class DetectorFraudes:
    """
    Sistema de detecção de fraudes em transações financeiras.
    Usa dois ponteiros para detectar padrões suspeitos.
    
    Complexidade: O(n) para análise de transações
    """
    
    def __init__(self):
        self.transacoes = []  # Lista de (timestamp, valor, tipo, conta)
    
    def adicionar_transacao(self, timestamp: float, valor: float, tipo: str, conta: str):
        """Adiciona transação ordenada por timestamp."""
        self.transacoes.append((timestamp, valor, tipo, conta))
        self.transacoes.sort()  # Manter ordenado
    
    def detectar_lavagem_dinheiro(self, janela_tempo: float = 3600) -> List[Tuple]:
        """
        Detecta possível lavagem usando padrão rápido de transações.
        
        Aplicação Real: Compliance bancário
        """
        suspeitas = []
        esquerda = 0
        
        for direita in range(len(self.transacoes)):
            # Mover ponteiro esquerdo para manter janela de tempo
            while (esquerda < direita and 
                   self.transacoes[direita][0] - self.transacoes[esquerda][0] > janela_tempo):
                esquerda += 1
            
            # Analisar padrão na janela atual
            transacoes_janela = self.transacoes[esquerda:direita+1]
            
            if self._padrao_suspeito(transacoes_janela):
                suspeitas.append({
                    'periodo': (self.transacoes[esquerda][0], self.transacoes[direita][0]),
                    'transacoes': transacoes_janela,
                    'motivo': 'Padrão de lavagem detectado'
                })
        
        return suspeitas
    
    def _padrao_suspeito(self, transacoes: List[Tuple]) -> bool:
        """Identifica padrões suspeitos de lavagem."""
        if len(transacoes) < 3:
            return False
        
        valores = [t[1] for t in transacoes]
        tipos = [t[2] for t in transacoes]
        
        # Padrão: Depósito grande seguido de múltiplas retiradas pequenas
        if (tipos[0] == "DEPOSITO" and valores[0] > 10000 and
            all(t == "SAQUE" for t in tipos[1:]) and
            all(v < 1000 for v in valores[1:])):
            return True
        
        return False

class AnalisadorDNA:
    """
    Analisador de sequências de DNA usando dois ponteiros.
    Identifica padrões e subsequências importantes.
    
    Complexidade: O(n) para busca de padrões
    """
    
    def __init__(self):
        self.bases_validas = set(['A', 'T', 'G', 'C'])
    
    def encontrar_palindromos_dna(self, sequencia: str) -> List[Tuple[int, int, str]]:
        """
        Encontra palíndromos na sequência de DNA.
        
        Aplicação Real: Identificação de sítios de restrição
        """
        palindromos = []
        
        for centro in range(len(sequencia)):
            # Palíndromos de tamanho ímpar
            esquerda, direita = centro, centro
            while (esquerda >= 0 and direita < len(sequencia) and
                   sequencia[esquerda] == sequencia[direita]):
                if direita - esquerda + 1 >= 4:  # Mínimo 4 bases
                    palindromos.append((esquerda, direita, sequencia[esquerda:direita+1]))
                esquerda -= 1
                direita += 1
            
            # Palíndromos de tamanho par
            esquerda, direita = centro, centro + 1
            while (esquerda >= 0 and direita < len(sequencia) and
                   sequencia[esquerda] == sequencia[direita]):
                if direita - esquerda + 1 >= 4:
                    palindromos.append((esquerda, direita, sequencia[esquerda:direita+1]))
                esquerda -= 1
                direita += 1
        
        return palindromos
    
    def encontrar_sequencia_complementar(self, seq1: str, seq2: str) -> List[Tuple[int, int]]:
        """
        Encontra regiões onde duas sequências são complementares.
        
        Aplicação Real: Análise de hibridização de DNA
        """
        complementos = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        regioes = []
        
        i, j = 0, 0
        while i < len(seq1) and j < len(seq2):
            if seq1[i] == complementos.get(seq2[j], ''):
                # Iniciar região complementar
                inicio_i, inicio_j = i, j
                
                # Estender enquanto complementar
                while (i < len(seq1) and j < len(seq2) and
                       seq1[i] == complementos.get(seq2[j], '')):
                    i += 1
                    j += 1
                
                # Registrar se região é significativa
                if i - inicio_i >= 6:  # Mínimo 6 bases complementares
                    regioes.append((inicio_i, inicio_j))
            else:
                i += 1
                j += 1
        
        return regioes

class CompressorTexto:
    """
    Compressor de texto usando algoritmo de dois ponteiros.
    Implementa variação do LZ77 para compressão.
    
    Complexidade: O(n²) no pior caso, O(n) caso médio
    """
    
    def __init__(self, tamanho_janela: int = 4096):
        self.tamanho_janela = tamanho_janela
    
    def comprimir(self, texto: str) -> List[Tuple]:
        """
        Comprime texto usando busca por padrões repetidos.
        
        Aplicação Real: Compressão de arquivos e dados
        """
        if not texto:
            return []
        
        resultado = []
        i = 0
        
        while i < len(texto):
            melhor_match = self._encontrar_melhor_match(texto, i)
            
            if melhor_match[2] > 2:  # Vale a pena comprimir
                # (distancia, comprimento, caractere_seguinte)
                resultado.append(melhor_match)
                i += melhor_match[1]
            else:
                # Caractere literal
                resultado.append((0, 0, texto[i]))
                i += 1
        
        return resultado
    
    def _encontrar_melhor_match(self, texto: str, pos_atual: int) -> Tuple[int, int, str]:
        """Encontra a melhor correspondência na janela anterior."""
        melhor_distancia = 0
        melhor_comprimento = 0
        
        # Definir janela de busca
        inicio_janela = max(0, pos_atual - self.tamanho_janela)
        
        # Usar dois ponteiros para encontrar matches
        for pos_busca in range(inicio_janela, pos_atual):
            comprimento = 0
            
            # Estender match enquanto caracteres coincidem
            while (pos_atual + comprimento < len(texto) and
                   pos_busca + comprimento < pos_atual and
                   texto[pos_busca + comprimento] == texto[pos_atual + comprimento]):
                comprimento += 1
            
            # Atualizar melhor match
            if comprimento > melhor_comprimento:
                melhor_comprimento = comprimento
                melhor_distancia = pos_atual - pos_busca
        
        # Próximo caractere (para casos onde não há match)
        proximo_char = texto[pos_atual + melhor_comprimento] if pos_atual + melhor_comprimento < len(texto) else ''
        
        return (melhor_distancia, melhor_comprimento, proximo_char)
    
    def descomprimir(self, dados_comprimidos: List[Tuple]) -> str:
        """Descomprime dados usando referências de volta."""
        resultado = []
        
        for item in dados_comprimidos:
            distancia, comprimento, caractere = item
            
            if distancia == 0 and comprimento == 0:
                # Caractere literal
                resultado.append(caractere)
            else:
                # Referência de volta
                pos_ref = len(resultado) - distancia
                for i in range(comprimento):
                    resultado.append(resultado[pos_ref + i])
        
        return ''.join(resultado)

# ============================================================================
# 🌐 BFS - APLICAÇÕES REAIS
# ============================================================================

class RedeSocial:
    """
    Sistema de rede social com BFS para análise de conexões.
    Implementa funcionalidades como sugestão de amigos e influência.
    
    Complexidade: O(V + E) para cada consulta BFS
    """
    
    def __init__(self):
        self.grafo = defaultdict(set)  # usuário -> set de amigos
        self.usuarios = set()
    
    def adicionar_usuario(self, usuario: str):
        """Adiciona novo usuário à rede."""
        self.usuarios.add(usuario)
    
    def adicionar_amizade(self, usuario1: str, usuario2: str):
        """Cria conexão bidirecional entre usuários."""
        self.grafo[usuario1].add(usuario2)
        self.grafo[usuario2].add(usuario1)
        self.usuarios.update([usuario1, usuario2])
    
    def grau_separacao(self, origem: str, destino: str) -> int:
        """
        Calcula graus de separação entre dois usuários.
        
        Aplicação Real: "6 graus de separação", análise de influência
        """
        if origem == destino:
            return 0
        
        if origem not in self.usuarios or destino not in self.usuarios:
            return -1
        
        visitados = {origem}
        fila = deque([(origem, 0)])
        
        while fila:
            usuario_atual, grau = fila.popleft()
            
            for amigo in self.grafo[usuario_atual]:
                if amigo == destino:
                    return grau + 1
                
                if amigo not in visitados:
                    visitados.add(amigo)
                    fila.append((amigo, grau + 1))
        
        return -1  # Não conectados
    
    def sugerir_amigos(self, usuario: str, max_sugestoes: int = 5) -> List[Tuple[str, int]]:
        """
        Sugere amigos baseado em amigos em comum.
        
        Aplicação Real: Sistema de recomendação de conexões
        """
        if usuario not in self.usuarios:
            return []
        
        amigos_diretos = self.grafo[usuario]
        candidatos = defaultdict(int)  # usuário -> número de conexões em comum
        
        # Para cada amigo direto
        for amigo in amigos_diretos:
            # Ver amigos dos amigos
            for amigo_do_amigo in self.grafo[amigo]:
                if (amigo_do_amigo != usuario and 
                    amigo_do_amigo not in amigos_diretos):
                    candidatos[amigo_do_amigo] += 1
        
        # Ordenar por número de conexões em comum
        sugestoes = sorted(candidatos.items(), key=lambda x: x[1], reverse=True)
        return sugestoes[:max_sugestoes]
    
    def encontrar_influenciadores(self, nivel_max: int = 3) -> List[Tuple[str, int]]:
        """
        Encontra usuários mais influentes por alcance de rede.
        
        Aplicação Real: Marketing de influência, análise viral
        """
        influenciadores = []
        
        for usuario in self.usuarios:
            alcance = self._calcular_alcance(usuario, nivel_max)
            influenciadores.append((usuario, alcance))
        
        return sorted(influenciadores, key=lambda x: x[1], reverse=True)
    
    def _calcular_alcance(self, usuario: str, nivel_max: int) -> int:
        """Calcula quantas pessoas podem ser alcançadas em X níveis."""
        visitados = {usuario}
        fila = deque([(usuario, 0)])
        
        while fila:
            usuario_atual, nivel = fila.popleft()
            
            if nivel < nivel_max:
                for amigo in self.grafo[usuario_atual]:
                    if amigo not in visitados:
                        visitados.add(amigo)
                        fila.append((amigo, nivel + 1))
        
        return len(visitados) - 1  # Excluir o próprio usuário

class SistemaRoteamento:
    """
    Sistema de roteamento de rede usando BFS para encontrar caminhos.
    Simula roteamento em redes de computadores.
    
    Complexidade: O(V + E) para encontrar caminho mais curto
    """
    
    def __init__(self):
        self.rede = defaultdict(dict)  # nó -> {vizinho: latencia}
        self.nos = set()
    
    def adicionar_no(self, no: str):
        """Adiciona nó à rede."""
        self.nos.add(no)
    
    def adicionar_conexao(self, no1: str, no2: str, latencia: int):
        """Adiciona conexão bidirecional com latência."""
        self.rede[no1][no2] = latencia
        self.rede[no2][no1] = latencia
        self.nos.update([no1, no2])
    
    def encontrar_caminho_otimo(self, origem: str, destino: str) -> Tuple[List[str], int]:
        """
        Encontra caminho com menor número de saltos.
        
        Aplicação Real: Roteamento de pacotes, otimização de rede
        """
        if origem == destino:
            return ([origem], 0)
        
        if origem not in self.nos or destino not in self.nos:
            return ([], -1)
        
        visitados = {origem}
        fila = deque([(origem, [origem], 0)])
        
        while fila:
            no_atual, caminho, latencia_total = fila.popleft()
            
            for vizinho, latencia in self.rede[no_atual].items():
                if vizinho == destino:
                    return (caminho + [vizinho], latencia_total + latencia)
                
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    novo_caminho = caminho + [vizinho]
                    nova_latencia = latencia_total + latencia
                    fila.append((vizinho, novo_caminho, nova_latencia))
        
        return ([], -1)  # Caminho não encontrado
    
    def analisar_redundancia(self, no_critico: str) -> Dict[Tuple[str, str], bool]:
        """
        Analisa se rede mantém conectividade sem um nó específico.
        
        Aplicação Real: Análise de falhas, planejamento de redundância
        """
        if no_critico not in self.nos:
            return {}
        
        # Criar rede temporária sem o nó crítico
        rede_temp = defaultdict(dict)
        nos_temp = self.nos - {no_critico}
        
        for no1 in nos_temp:
            for no2, latencia in self.rede[no1].items():
                if no2 != no_critico and no2 in nos_temp:
                    rede_temp[no1][no2] = latencia
        
        # Testar conectividade entre todos os pares
        resultado = {}
        nos_lista = list(nos_temp)
        
        for i, origem in enumerate(nos_lista):
            for destino in nos_lista[i+1:]:
                conectado = self._existe_caminho_temp(origem, destino, rede_temp)
                resultado[(origem, destino)] = conectado
        
        return resultado
    
    def _existe_caminho_temp(self, origem: str, destino: str, rede_temp: dict) -> bool:
        """Verifica se existe caminho na rede temporária."""
        if origem == destino:
            return True
        
        visitados = {origem}
        fila = deque([origem])
        
        while fila:
            no_atual = fila.popleft()
            
            for vizinho in rede_temp[no_atual]:
                if vizinho == destino:
                    return True
                
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        
        return False

class AnalisadorDependencias:
    """
    Analisador de dependências de projetos usando BFS.
    Detecta dependências circulares e ordem de instalação.
    
    Complexidade: O(V + E) para detecção de ciclos
    """
    
    def __init__(self):
        self.dependencias = defaultdict(set)  # pacote -> dependências
        self.pacotes = set()
    
    def adicionar_pacote(self, pacote: str, dependencias: List[str] = None):
        """Adiciona pacote com suas dependências."""
        self.pacotes.add(pacote)
        if dependencias:
            self.dependencias[pacote].update(dependencias)
            self.pacotes.update(dependencias)
    
    def detectar_dependencia_circular(self) -> List[List[str]]:
        """
        Detecta ciclos nas dependências.
        
        Aplicação Real: Validação de package.json, requirements.txt
        """
        ciclos = []
        visitados = set()
        pilha_recursao = set()
        
        def dfs(pacote: str, caminho: List[str]) -> bool:
            if pacote in pilha_recursao:
                # Encontrou ciclo
                inicio_ciclo = caminho.index(pacote)
                ciclo = caminho[inicio_ciclo:] + [pacote]
                ciclos.append(ciclo)
                return True
            
            if pacote in visitados:
                return False
            
            visitados.add(pacote)
            pilha_recursao.add(pacote)
            
            for dependencia in self.dependencias[pacote]:
                if dfs(dependencia, caminho + [dependencia]):
                    return True
            
            pilha_recursao.remove(pacote)
            return False
        
        for pacote in self.pacotes:
            if pacote not in visitados:
                dfs(pacote, [pacote])
        
        return ciclos
    
    def ordem_instalacao(self, pacote_alvo: str) -> List[str]:
        """
        Determina ordem de instalação das dependências.
        
        Aplicação Real: Package managers (npm, pip, etc.)
        """
        if pacote_alvo not in self.pacotes:
            return []
        
        ordem = []
        visitados = set()
        
        def dfs_instalacao(pacote: str):
            if pacote in visitados:
                return
            
            visitados.add(pacote)
            
            # Instalar dependências primeiro
            for dependencia in self.dependencias[pacote]:
                dfs_instalacao(dependencia)
            
            ordem.append(pacote)
        
        dfs_instalacao(pacote_alvo)
        return ordem
    
    def impacto_remocao(self, pacote: str) -> Set[str]:
        """
        Calcula quais pacotes serão afetados pela remoção.
        
        Aplicação Real: Análise de impacto de updates/remoções
        """
        if pacote not in self.pacotes:
            return set()
        
        afetados = set()
        fila = deque([pacote])
        
        while fila:
            pacote_atual = fila.popleft()
            
            # Encontrar quem depende deste pacote
            for pkg, deps in self.dependencias.items():
                if pacote_atual in deps and pkg not in afetados:
                    afetados.add(pkg)
                    fila.append(pkg)
        
        return afetados

# ============================================================================
# 🔄 BACKTRACKING - APLICAÇÕES REAIS
# ============================================================================

class PlanejadorTurnos:
    """
    Sistema de planejamento de turnos usando backtracking.
    Resolve problemas de escalonamento com restrições complexas.
    
    Complexidade: O(b^d) onde b=opções e d=profundidade
    """
    
    def __init__(self):
        self.funcionarios = {}  # id -> {nome, habilidades, restricoes}
        self.turnos = {}  # id -> {inicio, fim, habilidades_necessarias}
    
    def adicionar_funcionario(self, id_func: str, nome: str, 
                            habilidades: Set[str], restricoes: Dict):
        """Adiciona funcionário com habilidades e restrições."""
        self.funcionarios[id_func] = {
            'nome': nome,
            'habilidades': habilidades,
            'restricoes': restricoes  # ex: {'max_horas': 40, 'dias_off': ['domingo']}
        }
    
    def adicionar_turno(self, id_turno: str, inicio: datetime, 
                       fim: datetime, habilidades_necessarias: Set[str]):
        """Adiciona turno com requisitos específicos."""
        self.turnos[id_turno] = {
            'inicio': inicio,
            'fim': fim,
            'habilidades': habilidades_necessarias
        }
    
    def gerar_escala(self) -> Optional[Dict[str, str]]:
        """
        Gera escala ótima usando backtracking.
        
        Aplicação Real: Hospitais, call centers, segurança
        """
        escala = {}  # turno_id -> funcionario_id
        turnos_ids = list(self.turnos.keys())
        
        if self._backtrack_escala(turnos_ids, 0, escala):
            return escala
        return None
    
    def _backtrack_escala(self, turnos_ids: List[str], indice: int, 
                         escala: Dict[str, str]) -> bool:
        """Algoritmo de backtracking para escalonamento."""
        if indice == len(turnos_ids):
            return True  # Todos os turnos preenchidos
        
        turno_id = turnos_ids[indice]
        turno = self.turnos[turno_id]
        
        # Tentar cada funcionário para este turno
        for func_id, funcionario in self.funcionarios.items():
            if self._pode_trabalhar(func_id, turno_id, escala):
                # Atribuir turno ao funcionário
                escala[turno_id] = func_id
                
                # Continuar com próximo turno
                if self._backtrack_escala(turnos_ids, indice + 1, escala):
                    return True
                
                # Backtrack: remover atribuição
                del escala[turno_id]
        
        return False
    
    def _pode_trabalhar(self, func_id: str, turno_id: str, 
                       escala_atual: Dict[str, str]) -> bool:
        """Verifica se funcionário pode trabalhar no turno."""
        funcionario = self.funcionarios[func_id]
        turno = self.turnos[turno_id]
        
        # Verificar habilidades
        if not turno['habilidades'].issubset(funcionario['habilidades']):
            return False
        
        # Verificar restrições de horário
        restricoes = funcionario['restricoes']
        
        # Exemplo: máximo de horas por semana
        horas_trabalhadas = self._calcular_horas_trabalhadas(func_id, escala_atual)
        duracao_turno = (turno['fim'] - turno['inicio']).total_seconds() / 3600
        
        if horas_trabalhadas + duracao_turno > restricoes.get('max_horas', 40):
            return False
        
        # Verificar dias de folga
        dia_semana = turno['inicio'].strftime('%A').lower()
        if dia_semana in restricoes.get('dias_off', []):
            return False
        
        # Verificar conflitos de horário
        for outro_turno_id, outro_func_id in escala_atual.items():
            if outro_func_id == func_id:
                outro_turno = self.turnos[outro_turno_id]
                if self._turnos_se_sobrepoe(turno, outro_turno):
                    return False
        
        return True
    
    def _calcular_horas_trabalhadas(self, func_id: str, 
                                  escala: Dict[str, str]) -> float:
        """Calcula horas já trabalhadas pelo funcionário."""
        horas = 0
        for turno_id, funcionario_id in escala.items():
            if funcionario_id == func_id:
                turno = self.turnos[turno_id]
                duracao = (turno['fim'] - turno['inicio']).total_seconds() / 3600
                horas += duracao
        return horas
    
    def _turnos_se_sobrepoe(self, turno1: Dict, turno2: Dict) -> bool:
        """Verifica se dois turnos se sobrepõem no tempo."""
        return not (turno1['fim'] <= turno2['inicio'] or 
                   turno2['fim'] <= turno1['inicio'])

class ConfiguradorSistema:
    """
    Configurador automático de sistemas usando backtracking.
    Resolve problemas de configuração com dependências complexas.
    
    Complexidade: O(2^n) para n configurações booleanas
    """
    
    def __init__(self):
        self.parametros = {}  # nome -> {tipo, dominio, restricoes}
        self.restricoes_globais = []  # Lista de funções de validação
    
    def adicionar_parametro(self, nome: str, tipo: str, dominio: List, 
                          restricoes: List = None):
        """Adiciona parâmetro de configuração."""
        self.parametros[nome] = {
            'tipo': tipo,
            'dominio': dominio,
            'restricoes': restricoes or []
        }
    
    def adicionar_restricao_global(self, funcao_validacao):
        """Adiciona restrição que envolve múltiplos parâmetros."""
        self.restricoes_globais.append(funcao_validacao)
    
    def gerar_configuracao(self, preferencias: Dict = None) -> Optional[Dict]:
        """
        Gera configuração válida usando backtracking.
        
        Aplicação Real: Auto-configuração de servidores, VMs, clusters
        """
        configuracao = {}
        parametros_nomes = list(self.parametros.keys())
        
        # Aplicar preferências se fornecidas
        if preferencias:
            for nome, valor in preferencias.items():
                if nome in self.parametros:
                    configuracao[nome] = valor
        
        if self._backtrack_configuracao(parametros_nomes, 0, configuracao):
            return configuracao
        return None
    
    def _backtrack_configuracao(self, nomes: List[str], indice: int, 
                               config: Dict) -> bool:
        """Algoritmo de backtracking para configuração."""
        if indice == len(nomes):
            # Validar configuração completa
            return self._validar_configuracao_completa(config)
        
        nome_param = nomes[indice]
        
        # Se parâmetro já foi definido (preferência), pular
        if nome_param in config:
            return self._backtrack_configuracao(nomes, indice + 1, config)
        
        parametro = self.parametros[nome_param]
        
        # Tentar cada valor possível
        for valor in parametro['dominio']:
            if self._valor_valido(nome_param, valor, config):
                config[nome_param] = valor
                
                if self._backtrack_configuracao(nomes, indice + 1, config):
                    return True
                
                # Backtrack
                del config[nome_param]
        
        return False
    
    def _valor_valido(self, nome: str, valor, config_atual: Dict) -> bool:
        """Verifica se valor é válido para o parâmetro."""
        parametro = self.parametros[nome]
        
        # Verificar restrições locais
        for restricao in parametro['restricoes']:
            if not restricao(valor, config_atual):
                return False
        
        return True
    
    def _validar_configuracao_completa(self, config: Dict) -> bool:
        """Valida configuração completa contra restrições globais."""
        for restricao in self.restricoes_globais:
            if not restricao(config):
                return False
        return True

class OtimizadorRecursos:
    """
    Otimizador de alocação de recursos usando backtracking.
    Resolve problemas de bin packing e alocação ótima.
    
    Complexidade: O(2^n) para n recursos
    """
    
    def __init__(self):
        self.recursos = {}  # id -> {capacidade, custo, tipo}
        self.tarefas = {}   # id -> {demanda, prioridade, restricoes}
    
    def adicionar_recurso(self, id_recurso: str, capacidade: int, 
                         custo: float, tipo: str):
        """Adiciona recurso disponível."""
        self.recursos[id_recurso] = {
            'capacidade': capacidade,
            'custo': custo,
            'tipo': tipo,
            'usado': 0
        }
    
    def adicionar_tarefa(self, id_tarefa: str, demanda: int, 
                        prioridade: int, restricoes: Dict = None):
        """Adiciona tarefa a ser alocada."""
        self.tarefas[id_tarefa] = {
            'demanda': demanda,
            'prioridade': prioridade,
            'restricoes': restricoes or {}
        }
    
    def otimizar_alocacao(self) -> Tuple[Dict[str, str], float]:
        """
        Encontra alocação ótima de tarefas para recursos.
        
        Aplicação Real: Cloud computing, alocação de VMs, scheduling
        """
        # Ordenar tarefas por prioridade (maior primeiro)
        tarefas_ordenadas = sorted(self.tarefas.items(), 
                                 key=lambda x: x[1]['prioridade'], 
                                 reverse=True)
        
        melhor_alocacao = {}
        melhor_custo = float('inf')
        
        # Resetar uso dos recursos
        for recurso in self.recursos.values():
            recurso['usado'] = 0
        
        alocacao_atual = {}
        if self._backtrack_alocacao(tarefas_ordenadas, 0, alocacao_atual, 0):
            custo_atual = self._calcular_custo(alocacao_atual)
            if custo_atual < melhor_custo:
                melhor_alocacao = alocacao_atual.copy()
                melhor_custo = custo_atual
        
        return melhor_alocacao, melhor_custo
    
    def _backtrack_alocacao(self, tarefas_ordenadas: List, indice: int,
                           alocacao: Dict[str, str], custo_atual: float) -> bool:
        """Algoritmo de backtracking para alocação."""
        if indice == len(tarefas_ordenadas):
            return True  # Todas as tarefas alocadas
        
        id_tarefa, tarefa = tarefas_ordenadas[indice]
        
        # Tentar alocar em cada recurso compatível
        for id_recurso, recurso in self.recursos.items():
            if self._pode_alocar(id_tarefa, id_recurso):
                # Fazer alocação
                alocacao[id_tarefa] = id_recurso
                recurso['usado'] += tarefa['demanda']
                
                novo_custo = custo_atual + self._custo_alocacao(id_tarefa, id_recurso)
                
                # Continuar com próxima tarefa
                if self._backtrack_alocacao(tarefas_ordenadas, indice + 1, 
                                          alocacao, novo_custo):
                    return True
                
                # Backtrack
                del alocacao[id_tarefa]
                recurso['usado'] -= tarefa['demanda']
        
        return False
    
    def _pode_alocar(self, id_tarefa: str, id_recurso: str) -> bool:
        """Verifica se tarefa pode ser alocada no recurso."""
        tarefa = self.tarefas[id_tarefa]
        recurso = self.recursos[id_recurso]
        
        # Verificar capacidade
        if recurso['usado'] + tarefa['demanda'] > recurso['capacidade']:
            return False
        
        # Verificar restrições de tipo
        restricoes = tarefa['restricoes']
        if 'tipos_permitidos' in restricoes:
            if recurso['tipo'] not in restricoes['tipos_permitidos']:
                return False
        
        return True
    
    def _custo_alocacao(self, id_tarefa: str, id_recurso: str) -> float:
        """Calcula custo de alocar tarefa específica no recurso."""
        tarefa = self.tarefas[id_tarefa]
        recurso = self.recursos[id_recurso]
        
        return (tarefa['demanda'] / recurso['capacidade']) * recurso['custo']
    
    def _calcular_custo(self, alocacao: Dict[str, str]) -> float:
        """Calcula custo total da alocação."""
        custo_total = 0
        for id_tarefa, id_recurso in alocacao.items():
            custo_total += self._custo_alocacao(id_tarefa, id_recurso)
        return custo_total

# ============================================================================
# 🧪 TESTES E DEMONSTRAÇÕES
# ============================================================================

def demonstrar_aplicacoes_reais():
    """
    Demonstra todas as aplicações reais implementadas.
    """
    print("🚀 DEMONSTRAÇÃO: APLICAÇÕES REAIS - MÓDULO 1")
    print("=" * 60)
    
    # 1. Busca Binária - Sistema de Logs
    print("\n🔍 1. BUSCA BINÁRIA - Sistema de Busca em Logs")
    print("-" * 50)
    
    sistema_logs = SistemaBuscaLogs()
    
    # Simular logs
    base_time = time.time()
    logs_test = [
        (base_time + 10, "INFO: Sistema iniciado"),
        (base_time + 25, "DEBUG: Processando requisição"),
        (base_time + 45, "ERROR: Falha na conexão com banco"),
        (base_time + 60, "INFO: Reconectando..."),
        (base_time + 80, "FATAL: Sistema crítico falhando"),
        (base_time + 100, "INFO: Sistema recuperado")
    ]
    
    for timestamp, msg in logs_test:
        sistema_logs.adicionar_log(timestamp, msg)
    
    # Buscar logs em período específico
    logs_periodo = sistema_logs.buscar_logs_periodo(base_time + 20, base_time + 70)
    print(f"Logs entre 20s e 70s: {len(logs_periodo)} encontrados")
    
    # Buscar primeiro erro
    primeiro_erro = sistema_logs.buscar_primeiro_erro_apos(base_time + 30)
    if primeiro_erro:
        print(f"Primeiro erro após 30s: {primeiro_erro[1]}")
    
    # 2. Dois Ponteiros - Detector de Fraudes
    print("\n👥 2. DOIS PONTEIROS - Detector de Fraudes Bancárias")
    print("-" * 50)
    
    detector = DetectorFraudes()
    
    # Simular transações suspeitas
    base_time = time.time()
    transacoes_test = [
        (base_time, 15000, "DEPOSITO", "conta123"),
        (base_time + 300, 800, "SAQUE", "conta123"),
        (base_time + 600, 750, "SAQUE", "conta123"),
        (base_time + 900, 900, "SAQUE", "conta123"),
        (base_time + 1200, 600, "SAQUE", "conta123")
    ]
    
    for transacao in transacoes_test:
        detector.adicionar_transacao(*transacao)
    
    suspeitas = detector.detectar_lavagem_dinheiro()
    print(f"Padrões suspeitos detectados: {len(suspeitas)}")
    
    # 3. BFS - Rede Social
    print("\n🌐 3. BFS - Análise de Rede Social")
    print("-" * 50)
    
    rede = RedeSocial()
    
    # Criar rede de exemplo
    usuarios = ["Alice", "Bob", "Carol", "David", "Eve", "Frank"]
    for usuario in usuarios:
        rede.adicionar_usuario(usuario)
    
    # Conectar usuários
    conexoes = [
        ("Alice", "Bob"), ("Bob", "Carol"), ("Carol", "David"),
        ("Alice", "Eve"), ("Eve", "Frank"), ("Bob", "David")
    ]
    
    for u1, u2 in conexoes:
        rede.adicionar_amizade(u1, u2)
    
    # Analisar separação
    separacao = rede.grau_separacao("Alice", "Frank")
    print(f"Graus de separação Alice-Frank: {separacao}")
    
    # Sugerir amigos para Alice
    sugestoes = rede.sugerir_amigos("Alice")
    print(f"Sugestões de amigos para Alice: {sugestoes}")
    
    # 4. Backtracking - Planejador de Turnos
    print("\n🔄 4. BACKTRACKING - Planejador de Turnos")
    print("-" * 50)
    
    planejador = PlanejadorTurnos()
    
    # Adicionar funcionários
    planejador.adicionar_funcionario(
        "func1", "João", 
        {"atendimento", "vendas"}, 
        {"max_horas": 40, "dias_off": ["domingo"]}
    )
    
    planejador.adicionar_funcionario(
        "func2", "Maria", 
        {"atendimento", "suporte"}, 
        {"max_horas": 35, "dias_off": ["sabado"]}
    )
    
    # Adicionar turnos
    inicio = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    fim = inicio.replace(hour=17)
    
    planejador.adicionar_turno(
        "turno1", inicio, fim, {"atendimento"}
    )
    
    escala = planejador.gerar_escala()
    if escala:
        print(f"Escala gerada: {escala}")
    else:
        print("Não foi possível gerar escala válida")
    
    print("\n✅ Demonstração completa! Todas as aplicações funcionando.")

if __name__ == "__main__":
    demonstrar_aplicacoes_reais()
