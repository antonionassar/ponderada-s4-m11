#!/bin/bash

# Iniciar o simulador de dados em background
python src/scripts/data_simulator.py &

# Iniciar o exporter do Prometheus
python src/exporters/metrics_exporter.py 