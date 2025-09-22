"""
🎯 SISTEMA DE CACHE INTELIGENTE PARA PERFORMANCE
===============================================

Sistema avançado de cache otimizado para aplicações Streamlit
com foco em algoritmos e visualizações.

Funcionalidades:
- ✅ Cache inteligente para visualizações matplotlib/plotly
- ✅ Cache para resultados de algoritmos
- ✅ Cache para dados de exercícios
- ✅ Cache para integrações MCP
- ✅ Invalidação automática baseada em tempo
- ✅ Compressão de dados grandes
- ✅ Métricas de performance

Autor: GitHub Copilot
Data: 2025
"""

import streamlit as st
import hashlib
import json
import time
import pickle
import gzip
from typing import Any, Dict, Optional, Tuple, Callable
from functools import wraps
import threading
from datetime import datetime, timedelta
import psutil
import os

# ============================================================================
# 🎯 CLASSE PRINCIPAL DO SISTEMA DE CACHE
# ============================================================================

class CacheInteligente:
    """
    Sistema de cache inteligente otimizado para Streamlit.

    Recursos:
    - Cache baseado em hash das entradas
    - Compressão automática para dados grandes
    - Invalidação baseada em tempo e uso de memória
    - Métricas de performance
    - Thread-safe para aplicações multi-usuário
    """

    def __init__(self, max_memory_mb: int = 100, ttl_seconds: int = 3600):
        """
        Inicializa o sistema de cache.

        Args:
            max_memory_mb: Memória máxima em MB
            ttl_seconds: Tempo de vida padrão em segundos
        """
        self.max_memory_mb = max_memory_mb
        self.ttl_seconds = ttl_seconds
        self._lock = threading.Lock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'saved_time': 0.0,
            'memory_usage': 0.0,
            'cache_size': 0
        }

        # Inicializar cache na sessão do Streamlit
        if 'cache_inteligente' not in st.session_state:
            st.session_state.cache_inteligente = {}

    @property
    def cache(self) -> Dict:
        """Acesso thread-safe ao cache."""
        return st.session_state.cache_inteligente

    def _gerar_hash(self, *args, **kwargs) -> str:
        """Gera hash único para as entradas."""
        # Converter args para string serializável
        args_str = json.dumps(args, sort_keys=True, default=str)
        kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
        content = f"{args_str}|{kwargs_str}"

        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _comprimir_dados(self, data: Any) -> bytes:
        """Comprime dados grandes para economizar memória."""
        try:
            return gzip.compress(pickle.dumps(data))
        except:
            return pickle.dumps(data)

    def _descomprimir_dados(self, data: bytes) -> Any:
        """Descomprime dados."""
        try:
            return pickle.loads(gzip.decompress(data))
        except:
            return pickle.loads(data)

    def _verificar_ttl(self, timestamp: float) -> bool:
        """Verifica se o cache ainda é válido baseado no TTL."""
        return time.time() - timestamp < self.ttl_seconds

    def _limpar_cache_antigo(self):
        """Remove entradas antigas do cache para liberar memória."""
        with self._lock:
            current_time = time.time()
            keys_to_remove = []

            for key, data in self.cache.items():
                if not self._verificar_ttl(data['timestamp']):
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                del self.cache[key]

            self._stats['cache_size'] = len(self.cache)

    def _verificar_memoria(self) -> bool:
        """Verifica se o uso de memória está dentro do limite."""
        try:
            memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            return memory_mb < self.max_memory_mb
        except:
            return True  # Se não conseguir verificar, assume que está OK

    def obter(self, chave: str) -> Optional[Any]:
        """
        Obtém dados do cache.

        Args:
            chave: Chave do cache

        Returns:
            Dados cacheados ou None se não encontrado/inválido
        """
        with self._lock:
            if chave not in self.cache:
                self._stats['misses'] += 1
                return None

            data = self.cache[chave]

            # Verificar TTL
            if not self._verificar_ttl(data['timestamp']):
                del self.cache[chave]
                self._stats['misses'] += 1
                return None

            # Verificar memória
            if not self._verificar_memoria():
                self._limpar_cache_antigo()
                self._stats['misses'] += 1
                return None

            self._stats['hits'] += 1
            return self._descomprimir_dados(data['dados'])

    def armazenar(self, chave: str, dados: Any, ttl: Optional[int] = None):
        """
        Armazena dados no cache.

        Args:
            chave: Chave do cache
            dados: Dados a serem cacheados
            ttl: Tempo de vida personalizado (opcional)
        """
        with self._lock:
            # Verificar memória antes de armazenar
            if not self._verificar_memoria():
                self._limpar_cache_antigo()

            # Comprimir dados grandes
            dados_comprimidos = self._comprimir_dados(dados)

            self.cache[chave] = {
                'dados': dados_comprimidos,
                'timestamp': time.time(),
                'ttl': ttl or self.ttl_seconds
            }

            self._stats['cache_size'] = len(self.cache)

    def limpar(self):
        """Limpa todo o cache."""
        with self._lock:
            self.cache.clear()
            self._stats['cache_size'] = 0

    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do cache."""
        with self._lock:
            stats = self._stats.copy()
            stats['hit_rate'] = (
                stats['hits'] / (stats['hits'] + stats['misses'])
                if (stats['hits'] + stats['misses']) > 0 else 0
            )
            stats['memory_usage'] = self._get_memory_usage()
            return stats

    def _get_memory_usage(self) -> float:
        """Calcula uso de memória do cache."""
        try:
            total_size = 0
            for data in self.cache.values():
                total_size += len(data['dados'])
            return total_size / 1024 / 1024  # MB
        except:
            return 0.0

# ============================================================================
# 🎯 DECORADORES PARA CACHE AUTOMÁTICO
# ============================================================================

def cache_visualizacao(ttl_seconds: int = 1800):
    """
    Decorador para cache de visualizações matplotlib/plotly.

    Args:
        ttl_seconds: Tempo de vida do cache em segundos
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obter instância do cache
            if 'cache_instance' not in st.session_state:
                st.session_state.cache_instance = CacheInteligente()

            cache = st.session_state.cache_instance

            # Gerar chave baseada na função e argumentos
            chave = f"viz_{func.__name__}_{cache._gerar_hash(*args, **kwargs)}"

            # Tentar obter do cache
            resultado = cache.obter(chave)
            if resultado is not None:
                return resultado

            # Executar função e cachear resultado
            start_time = time.time()
            resultado = func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Cachear apenas se a execução foi demorada (>0.1s)
            if execution_time > 0.1:
                cache.armazenar(chave, resultado, ttl_seconds)

            return resultado

        return wrapper
    return decorator

def cache_algoritmo(ttl_seconds: int = 3600):
    """
    Decorador para cache de resultados de algoritmos.

    Args:
        ttl_seconds: Tempo de vida do cache em segundos
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obter instância do cache
            if 'cache_instance' not in st.session_state:
                st.session_state.cache_instance = CacheInteligente()

            cache = st.session_state.cache_instance

            # Gerar chave baseada na função e argumentos
            chave = f"algo_{func.__name__}_{cache._gerar_hash(*args, **kwargs)}"

            # Tentar obter do cache
            resultado = cache.obter(chave)
            if resultado is not None:
                return resultado

            # Executar função e cachear resultado
            start_time = time.time()
            resultado = func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Cachear resultado
            cache.armazenar(chave, resultado, ttl_seconds)

            return resultado

        return wrapper
    return decorator

def cache_mcp(ttl_seconds: int = 1800):
    """
    Decorador para cache de consultas MCP.

    Args:
        ttl_seconds: Tempo de vida do cache em segundos
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obter instância do cache
            if 'cache_instance' not in st.session_state:
                st.session_state.cache_instance = CacheInteligente()

            cache = st.session_state.cache_instance

            # Gerar chave baseada na função e argumentos
            chave = f"mcp_{func.__name__}_{cache._gerar_hash(*args, **kwargs)}"

            # Tentar obter do cache
            resultado = cache.obter(chave)
            if resultado is not None:
                return resultado

            # Executar função e cachear resultado
            resultado = func(*args, **kwargs)
            cache.armazenar(chave, resultado, ttl_seconds)

            return resultado

        return wrapper
    return decorator

# ============================================================================
# 🎯 UTILITÁRIOS DE CACHE
# ============================================================================

def obter_cache_stats() -> Dict:
    """Obtém estatísticas do sistema de cache."""
    if 'cache_instance' not in st.session_state:
        st.session_state.cache_instance = CacheInteligente()

    return st.session_state.cache_instance.obter_estatisticas()

def limpar_cache():
    """Limpa todo o cache."""
    if 'cache_instance' in st.session_state:
        st.session_state.cache_instance.limpar()

def mostrar_estatisticas_cache():
    """Exibe estatísticas do cache em formato amigável."""
    stats = obter_cache_stats()

    st.markdown("### 📊 Estatísticas do Cache Inteligente")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Taxa de Acerto", ".1%", stats.get('hit_rate', 0) * 100)

    with col2:
        st.metric("Itens em Cache", stats.get('cache_size', 0))

    with col3:
        st.metric("Tempo Economizado", ".2f", stats.get('saved_time', 0))

    st.markdown(f"""
    **📈 Detalhes:**
    - ✅ Hits: {stats.get('hits', 0)}
    - ❌ Misses: {stats.get('misses', 0)}
    - 💾 Uso de Memória: {stats.get('memory_usage', 0):.2f} MB
    """)

# ============================================================================
# 🎯 EXEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    # Exemplo de uso
    cache = CacheInteligente()

    # Cache de função
    @cache_visualizacao(ttl_seconds=300)
    def criar_grafico_complexo(dados):
        # Simular criação de gráfico complexo
        time.sleep(0.5)  # Simular processamento
        return {"tipo": "grafico", "dados": dados}

    # Teste
    dados = [1, 2, 3, 4, 5]

    print("Primeira execução (sem cache):")
    start = time.time()
    resultado1 = criar_grafico_complexo(dados)
    print(".3f")

    print("Segunda execução (com cache):")
    start = time.time()
    resultado2 = criar_grafico_complexo(dados)
    print(".3f")

    print("Estatísticas:", cache.obter_estatisticas())
