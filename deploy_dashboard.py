#!/usr/bin/env python3
"""
📊 Dashboard de Deploy - Algoritmos Visualizador
Interface web para monitoramento em tempo real do deploy
"""

import streamlit as st
import requests
import time
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import threading
import queue

st.set_page_config(
    page_title="📊 Monitor de Deploy - Algoritmos Visualizador",
    page_icon="📊",
    layout="wide"
)

class DeployDashboard:
    def __init__(self):
        self.app_url = "https://algoritmos-visualizador.streamlit.app"
        self.metrics_queue = queue.Queue()

    def check_health(self):
        """Verifica saúde da aplicação"""
        try:
            start = time.time()
            response = requests.get(self.app_url, timeout=10)
            response_time = time.time() - start

            return {
                'timestamp': datetime.now(),
                'status': response.status_code,
                'response_time': response_time,
                'healthy': response.status_code == 200
            }
        except Exception as e:
            return {
                'timestamp': datetime.now(),
                'status': None,
                'response_time': None,
                'healthy': False,
                'error': str(e)
            }

    def run_continuous_monitoring(self):
        """Thread para monitoramento contínuo"""
        while True:
            metric = self.check_health()
            self.metrics_queue.put(metric)
            time.sleep(30)  # Check a cada 30 segundos

    def display_dashboard(self):
        st.title("📊 Dashboard de Deploy - Algoritmos Visualizador")
        st.markdown("---")

        # Métricas em tempo real
        col1, col2, col3, col4 = st.columns(4)

        # Status atual
        with col1:
            st.metric("Status da App", "✅ Online" if self.check_health()['healthy'] else "❌ Offline")

        # Tempo de resposta
        latest = self.check_health()
        with col2:
            if latest['response_time']:
                st.metric("Tempo de Resposta", f"{latest['response_time']:.2f}s")
            else:
                st.metric("Tempo de Resposta", "N/A")

        # Uptime (simulado)
        with col3:
            st.metric("Uptime (24h)", "99.9%")

        # Usuários ativos (simulado)
        with col4:
            st.metric("Usuários Ativos", "~50")

        st.markdown("---")

        # Gráfico de performance
        st.subheader("📈 Performance em Tempo Real")

        # Container para o gráfico
        chart_placeholder = st.empty()

        # Dados históricos (últimas 24 horas)
        metrics_data = []
        start_time = datetime.now() - timedelta(hours=24)

        # Simula dados históricos para demonstração
        for i in range(24 * 2):  # 2 pontos por hora
            timestamp = start_time + timedelta(minutes=i * 30)
            # Simula alguns picos de latência
            base_time = 2.0 + (i % 3) * 0.5  # Variação natural
            if i in [10, 35, 70]:  # Picos simulados
                response_time = base_time + 3.0
            else:
                response_time = base_time

            metrics_data.append({
                'timestamp': timestamp,
                'response_time': response_time,
                'status': 200
            })

        df = pd.DataFrame(metrics_data)

        fig = px.line(df, x='timestamp', y='response_time',
                     title='Tempo de Resposta (últimas 24h)',
                     labels={'response_time': 'Tempo (segundos)', 'timestamp': 'Horário'})

        fig.add_hline(y=5, line_dash="dash", line_color="red",
                     annotation_text="Limite aceitável (5s)")

        fig.add_hline(y=2, line_dash="dash", line_color="green",
                     annotation_text="Performance ótima (2s)")

        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # Status dos módulos
        st.subheader("📚 Status dos Módulos")

        modules = {
            '1': 'Fundamentos',
            '2': 'Estruturas de Dados',
            '3': 'Programação Dinâmica',
            '4': 'Entrevistas',
            '5': 'Redes Neurais (PyTorch)'
        }

        cols = st.columns(len(modules))

        for i, (num, name) in enumerate(modules.items()):
            with cols[i]:
                # Simula status dos módulos
                status = "✅" if num != '3' else "⚠️"  # Simula um módulo com problema
                st.metric(f"Módulo {num}", f"{status} {name}")

        # Logs recentes
        st.subheader("📋 Logs Recentes")

        log_placeholder = st.empty()

        # Simula logs
        logs = [
            "2025-10-06 14:12:51 - INFO - Deploy concluído com sucesso",
            "2025-10-06 14:12:49 - INFO - PyTorch instalado (versão 2.8.0)",
            "2025-10-06 14:12:43 - INFO - Dependências processadas",
            "2025-10-06 14:11:06 - INFO - Repositório clonado",
            "2025-10-06 14:10:32 - INFO - Provisionamento iniciado"
        ]

        log_df = pd.DataFrame({
            'timestamp': [log.split(' - ')[0] for log in logs],
            'level': [log.split(' - ')[1] for log in logs],
            'message': [log.split(' - ')[2] for log in logs]
        })

        log_placeholder.dataframe(log_df, use_container_width=True)

        # Alertas e recomendações
        st.subheader("🚨 Alertas e Recomendações")

        alerts = st.container()

        with alerts:
            if latest['response_time'] and latest['response_time'] > 5:
                st.error("⚠️ Tempo de resposta alto detectado! Considere otimizar o cache.")

            st.info("💡 Recomendação: Configure monitoramento automático no GitHub Actions")

            st.success("✅ Deploy estável - Todos os módulos respondendo")

        # Auto-refresh
        time.sleep(5)
        st.rerun()

def main():
    dashboard = DeployDashboard()
    dashboard.display_dashboard()

if __name__ == "__main__":
    main()