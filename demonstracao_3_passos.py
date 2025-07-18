"""
DEMONSTRAÇÃO: Metodologia dos 3 Passos
Problema: Calcular o N-ésimo número de Fibonacci

Este arquivo demonstra como aplicar sistematicamente a metodologia dos 3 passos
para resolver um problema algorítmico clássico.

Problema: Dado n, calcule F(n) onde F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
"""

import time
from functools import lru_cache

def demonstrar_metodologia():
    """
    Demonstra a evolução das 3 etapas da metodologia.
    """
    print("🧠 METODOLOGIA DOS 3 PASSOS - FIBONACCI")
    print("=" * 50)
    
    n = 35  # Valor para demonstrar diferenças de performance
    
    # Etapa 1: Força Bruta
    print("\n📍 ETAPA 1: FORÇA BRUTA RECURSIVA")
    start = time.time()
    resultado1 = fibonacci_forca_bruta(n)
    tempo1 = time.time() - start
    print(f"   Resultado: F({n}) = {resultado1}")
    print(f"   Tempo: {tempo1:.4f}s")
    print(f"   Complexidade: O(2^n) - EXPONENCIAL!")
    
    # Etapa 2: Memoização
    print("\n📍 ETAPA 2: MEMOIZAÇÃO (TOP-DOWN)")
    start = time.time()
    resultado2 = fibonacci_memoizacao(n)
    tempo2 = time.time() - start
    print(f"   Resultado: F({n}) = {resultado2}")
    print(f"   Tempo: {tempo2:.6f}s")
    print(f"   Complexidade: O(n) - LINEAR!")
    if tempo2 > 0:
        print(f"   Melhoria: {tempo1/tempo2:.0f}x mais rápido")
    else:
        print(f"   Melhoria: >1000x mais rápido (instantâneo!)")
    
    # Etapa 3: Tabulação
    print("\n📍 ETAPA 3: TABULAÇÃO (BOTTOM-UP)")
    start = time.time()
    resultado3 = fibonacci_tabulacao(n)
    tempo3 = time.time() - start
    print(f"   Resultado: F({n}) = {resultado3}")
    print(f"   Tempo: {tempo3:.6f}s")
    print(f"   Complexidade: O(n) tempo, O(1) espaço")
    print(f"   Melhoria espacial: Constante vs O(n)")
    
    # Verificar consistência
    print(f"\n✅ Todos os resultados são iguais: {resultado1 == resultado2 == resultado3}")
    
    # Bonus: Solução matemática
    print("\n🚀 BONUS: SOLUÇÃO MATEMÁTICA O(1)")
    start = time.time()
    resultado4 = fibonacci_formula(n)
    tempo4 = time.time() - start
    print(f"   Resultado: F({n}) = {resultado4}")
    print(f"   Tempo: {tempo4:.8f}s")
    print(f"   Complexidade: O(1) - CONSTANTE!")

# ==================== ETAPA 1: FORÇA BRUTA ====================

def fibonacci_forca_bruta(n):
    """
    ETAPA 1: Solução recursiva por força bruta.
    
    Intuição:
    - Implementa diretamente a definição matemática
    - F(n) = F(n-1) + F(n-2)
    - Casos base: F(0) = 0, F(1) = 1
    
    Problemas:
    - Recalcula os mesmos valores múltiplas vezes
    - Árvore de recursão tem altura n com sobreposição massiva
    - Complexidade exponencial O(2^n)
    
    Args:
        n: Posição na sequência de Fibonacci
        
    Returns:
        int: N-ésimo número de Fibonacci
        
    Complexidade: O(2^n) tempo, O(n) espaço (stack)
    """
    # Casos base
    if n <= 1:
        return n
    
    # Recorrência direta (ineficiente)
    return fibonacci_forca_bruta(n - 1) + fibonacci_forca_bruta(n - 2)

# ==================== ETAPA 2: MEMOIZAÇÃO ====================

@lru_cache(maxsize=None)
def fibonacci_memoizacao(n):
    """
    ETAPA 2: Otimização com memoização (Top-Down).
    
    Intuição:
    - Mesma lógica da força bruta
    - Adiciona cache para evitar recálculos
    - Cada subproblema é resolvido apenas uma vez
    
    Melhorias:
    - Elimina sobreposição de subproblemas
    - Mantém a clareza da recursão
    - Complexidade linear O(n)
    
    Args:
        n: Posição na sequência de Fibonacci
        
    Returns:
        int: N-ésimo número de Fibonacci
        
    Complexidade: O(n) tempo, O(n) espaço (cache + stack)
    """
    # Casos base (iguais à força bruta)
    if n <= 1:
        return n
    
    # Recorrência com cache automático
    return fibonacci_memoizacao(n - 1) + fibonacci_memoizacao(n - 2)

def fibonacci_memoizacao_manual(n, memo=None):
    """
    Versão alternativa com memoização manual para fins educativos.
    """
    if memo is None:
        memo = {}
    
    # Verificar se já foi calculado
    if n in memo:
        return memo[n]
    
    # Casos base
    if n <= 1:
        return n
    
    # Calcular e armazenar no cache
    memo[n] = fibonacci_memoizacao_manual(n - 1, memo) + fibonacci_memoizacao_manual(n - 2, memo)
    return memo[n]

# ==================== ETAPA 3: TABULAÇÃO ====================

def fibonacci_tabulacao(n):
    """
    ETAPA 3: Solução iterativa bottom-up (Tabulação).
    
    Intuição:
    - Constrói a solução de baixo para cima
    - Calcula F(0), F(1), F(2), ..., F(n) em ordem
    - Usa apenas os 2 valores anteriores
    
    Vantagens:
    - Elimina overhead de recursão
    - Espaço constante O(1)
    - Mesmo tempo O(n), mas mais eficiente na prática
    - Sem risco de stack overflow
    
    Args:
        n: Posição na sequência de Fibonacci
        
    Returns:
        int: N-ésimo número de Fibonacci
        
    Complexidade: O(n) tempo, O(1) espaço
    """
    # Casos base
    if n <= 1:
        return n
    
    # Inicializar os dois primeiros valores
    prev2, prev1 = 0, 1
    
    # Construir iterativamente até n
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1

def fibonacci_tabulacao_array(n):
    """
    Versão alternativa usando array completo (para fins educativos).
    Usa O(n) espaço, mas mostra claramente a construção bottom-up.
    """
    if n <= 1:
        return n
    
    # Criar array para armazenar todos os valores
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    
    # Preencher array de baixo para cima
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# ==================== BONUS: SOLUÇÃO MATEMÁTICA ====================

def fibonacci_formula(n):
    """
    BONUS: Fórmula de Binet para Fibonacci.
    
    Usa a fórmula matemática fechada:
    F(n) = (φ^n - ψ^n) / √5
    
    Onde:
    φ = (1 + √5) / 2 ≈ 1.618 (proporção áurea)
    ψ = (1 - √5) / 2 ≈ -0.618
    
    Complexidade: O(1) tempo e espaço
    
    Nota: Para n grandes, pode ter problemas de precisão de ponto flutuante.
    """
    if n <= 1:
        return n
    
    sqrt5 = 5 ** 0.5
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    
    return round((phi ** n - psi ** n) / sqrt5)

# ==================== ANÁLISE COMPARATIVA ====================

def comparar_abordagens():
    """
    Compara todas as abordagens com diferentes valores de n.
    """
    print("\n📊 ANÁLISE COMPARATIVA DE PERFORMANCE")
    print("=" * 60)
    
    valores_n = [10, 20, 30, 35]
    
    for n in valores_n:
        print(f"\n🔢 n = {n}")
        print("-" * 30)
        
        # Força bruta (só para n pequenos)
        if n <= 30:
            start = time.time()
            resultado_fb = fibonacci_forca_bruta(n)
            tempo_fb = time.time() - start
            print(f"Força Bruta:   {tempo_fb:.6f}s")
        else:
            print(f"Força Bruta:   Muito lento para n={n}")
        
        # Memoização
        start = time.time()
        resultado_memo = fibonacci_memoizacao(n)
        tempo_memo = time.time() - start
        print(f"Memoização:    {tempo_memo:.6f}s")
        
        # Tabulação
        start = time.time()
        resultado_tab = fibonacci_tabulacao(n)
        tempo_tab = time.time() - start
        print(f"Tabulação:     {tempo_tab:.6f}s")
        
        # Fórmula
        start = time.time()
        resultado_form = fibonacci_formula(n)
        tempo_form = time.time() - start
        print(f"Fórmula:       {tempo_form:.8f}s")
        
        print(f"Resultado:     {resultado_memo}")

def analisar_uso_memoria():
    """
    Analisa o uso de memória das diferentes abordagens.
    """
    print("\n💾 ANÁLISE DE USO DE MEMÓRIA")
    print("=" * 40)
    print("Força Bruta:    O(n) - stack de recursão")
    print("Memoização:     O(n) - cache + stack")
    print("Tabulação:      O(1) - apenas variáveis")
    print("Fórmula:        O(1) - apenas cálculo")
    print("\n💡 Para n grande, tabulação é ideal!")

# ==================== EXECUÇÃO PRINCIPAL ====================

if __name__ == "__main__":
    # Demonstração principal
    demonstrar_metodologia()
    
    # Análises adicionais
    comparar_abordagens()
    analisar_uso_memoria()
    
    print("\n" + "=" * 60)
    print("🎯 LIÇÕES APRENDIDAS:")
    print("1. Sempre comece com força bruta para entender o problema")
    print("2. Memoização é uma otimização natural da recursão")
    print("3. Tabulação elimina overhead e é mais eficiente")
    print("4. Análise de complexidade guia a escolha da abordagem")
    print("5. Considere soluções matemáticas quando disponíveis")
    print("=" * 60)
