from flask import Flask, Response
import psutil
import subprocess
import time
from prometheus_client import start_http_server, Gauge, Counter, generate_latest, CONTENT_TYPE_LATEST
import threading
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Prometheus metrics
cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage in percent')
memory_usage = Gauge('system_memory_usage_percent', 'Memory usage in percent')
disk_usage = Gauge('system_disk_usage_percent', 'Disk usage in percent')
error_count = Counter('system_error_count', 'Number of system errors detected')

def collect_metrics():
    """Collect system metrics continuously"""
    while True:
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_usage.set(cpu_percent)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage.set(memory.percent)

            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage.set(disk.percent)

            logger.info(f"Metrics collected - CPU: {cpu_percent}%, Memory: {memory.percent}%, Disk: {disk.percent}%")
        except Exception as e:
            logger.error(f"Error collecting metrics: {str(e)}")
            error_count.inc()

        time.sleep(5)

def monitor_system_logs():
    """Monitor system logs using log stream"""
    try:
        process = subprocess.Popen(['log', 'stream'], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        
        for line in process.stdout:
            if 'error' in line.lower():
                error_count.inc()
                logger.warning(f"System log error detected: {line.strip()}")
    except Exception as e:
        logger.error(f"Error monitoring system logs: {str(e)}")
        error_count.inc()

@app.route('/metrics')
def metrics():
    """Endpoint for exposing metrics to Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/')
def home():
    """Home page with basic system information"""
    return """
    <h1>System Monitoring Dashboard</h1>
    <p>Metrics are available at <a href="/metrics">/metrics</a></p>
    <p>View the dashboard in Grafana at <a href="http://localhost:3000">http://localhost:3000</a></p>
    """

if __name__ == '__main__':
    # Start metrics collection in a background thread
    metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
    metrics_thread.start()

    # Start log monitoring in a background thread
    logs_thread = threading.Thread(target=monitor_system_logs, daemon=True)
    logs_thread.start()

    # Start the Flask application
    app.run(host='0.0.0.0', port=5001, debug=True)
