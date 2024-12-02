# System Monitoring Dashboard

A real-time system monitoring dashboard for macOS that collects system metrics, processes them, and visualizes them using Prometheus and Grafana.

## Features

- Real-time system metrics collection (CPU, Memory, Disk Usage)
- System log monitoring and analysis
- Prometheus metrics exposition
- Beautiful Grafana dashboards
- Error rate monitoring

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for Prometheus and Grafana)
- macOS (for system metrics collection)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/system-monitoring-dashboard.git
cd system-monitoring-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Start the services using Docker Compose:
```bash
docker-compose up -d
```

5. Run the Flask application:
```bash
python app.py
```

## Architecture

The system consists of several components:

1. **Metrics Collector**: Python script that collects system metrics using psutil
2. **Log Monitor**: Script that monitors system logs using log stream
3. **Flask Application**: Exposes metrics in Prometheus format
4. **Prometheus**: Time series database for storing metrics
5. **Grafana**: Visualization dashboard

## Accessing the Dashboard

- Flask Application: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Configuration

- Prometheus configuration is in `prometheus/prometheus.yml`
- Grafana dashboards are in `grafana/dashboards/`
- System metrics collection settings are in `config.py`

## License

MIT License