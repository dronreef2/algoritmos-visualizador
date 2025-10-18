#!/usr/bin/env python3
"""
🎯 Monitor de Deploy - Algoritmos Visualizador
Script personalizado para monitoramento avançado do deploy no Streamlit Cloud
"""

import requests
import time
import json
import logging
from datetime import datetime, timedelta
import sys
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deploy_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DeployMonitor:
    def __init__(self, app_url="https://algoritmos-visualizador.streamlit.app"):
        self.app_url = app_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DeployMonitor/1.0 (Algoritmos Visualizador)'
        })

    def check_app_health(self):
        """Verifica se a aplicação está respondendo"""
        try:
            start_time = time.time()
            response = self.session.get(self.app_url, timeout=30)
            response_time = time.time() - start_time

            return {
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'is_up': response.status_code == 200,
                'timestamp': datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                'status_code': None,
                'response_time': None,
                'is_up': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def check_module_availability(self):
        """Verifica se os módulos principais estão carregando"""
        modules_to_check = [
            '/?module=1',  # Fundamentos
            '/?module=2',  # Estruturas de Dados
            '/?module=3',  # Programação Dinâmica
            '/?module=4',  # Entrevistas
            '/?module=5',  # Redes Neurais
        ]

        results = {}
        for module in modules_to_check:
            try:
                response = self.session.get(f"{self.app_url}{module}", timeout=15)
                results[f"module_{module.split('=')[1]}"] = {
                    'status': response.status_code,
                    'available': response.status_code == 200
                }
            except Exception as e:
                results[f"module_{module.split('=')[1]}"] = {
                    'status': None,
                    'available': False,
                    'error': str(e)
                }

        return results

    def generate_report(self, health_data, module_data):
        """Gera relatório detalhado do status"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'app_url': self.app_url,
            'health_check': health_data,
            'modules_check': module_data,
            'overall_status': 'HEALTHY' if health_data['is_up'] else 'DOWN'
        }

        # Análise adicional
        if health_data['is_up']:
            if health_data['response_time'] > 10:
                report['performance'] = 'SLOW'
            elif health_data['response_time'] > 5:
                report['performance'] = 'MODERATE'
            else:
                report['performance'] = 'FAST'

        return report

    def monitor_continuous(self, interval_minutes=60):
        """Monitoramento contínuo com intervalo configurável"""
        logger.info(f"🚀 Iniciando monitoramento contínuo - Intervalo: {interval_minutes} minutos")

        while True:
            try:
                # Health check básico
                health = self.check_app_health()
                logger.info(f"📊 Health Check: {health['status_code']} - {health['response_time']}s")

                # Verificação de módulos (uma vez por hora)
                if datetime.now().minute == 0:
                    modules = self.check_module_availability()
                    logger.info(f"📚 Módulos verificados: {sum(1 for m in modules.values() if m['available'])}/{len(modules)} disponíveis")

                # Gera relatório completo a cada 6 horas
                if datetime.now().hour % 6 == 0 and datetime.now().minute == 0:
                    modules = self.check_module_availability()
                    report = self.generate_report(health, modules)

                    with open(f'report_{datetime.now().strftime("%Y%m%d_%H%M")}.json', 'w') as f:
                        json.dump(report, f, indent=2)

                    logger.info(f"📋 Relatório completo gerado: {report['overall_status']}")

                time.sleep(interval_minutes * 60)

            except KeyboardInterrupt:
                logger.info("⏹️ Monitoramento interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
                time.sleep(300)  # Espera 5 minutos em caso de erro

def main():
    monitor = DeployMonitor()

    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        monitor.monitor_continuous(interval)
    else:
        # Check único
        health = monitor.check_app_health()
        modules = monitor.check_module_availability()
        report = monitor.generate_report(health, modules)

        print(json.dumps(report, indent=2))

        # Log do resultado
        status_emoji = "✅" if report['overall_status'] == 'HEALTHY' else "❌"
        logger.info(f"{status_emoji} Status da aplicação: {report['overall_status']}")

if __name__ == "__main__":
    main()