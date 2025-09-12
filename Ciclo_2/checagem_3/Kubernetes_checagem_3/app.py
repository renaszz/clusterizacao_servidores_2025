import os
import socket
import random
import math
from flask import Flask, jsonify
from typing import Tuple

app = Flask(__name__)

# ---------------------------
# Funções de Simulação Monte Carlo
# ---------------------------

def monte_carlo_pi(num_samples: int) -> float:
    """Estima o valor de Pi."""
    inside_circle = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        # Considera um círculo de raio 1 centrado na origem
        if x*x + y*y <= 1.0:
            inside_circle += 1
    # A área do quadrado é 1, a área do círculo é pi*r^2/4 = pi/4
    # A proporção de pontos dentro do círculo é (pi/4)/1 = pi/4
    return (4.0 * inside_circle) / num_samples

def monte_carlo_square_area(num_samples: int) -> Tuple[float, float]:
    """
    Estima a área de um quadrado inscrito em um círculo de raio 0.5.
    A simulação ocorre em um quadrado de área 1 (pontos de 0 a 1).
    O círculo está centrado em (0.5, 0.5).
    A área teórica do quadrado inscrito é 0.5.
    """
    inside_square = 0
    
    # O lado do quadrado inscrito é r*sqrt(2), onde r=0.5.
    # Mas é mais fácil checar a distância de Manhattan do ponto ao centro (0.5, 0.5)
    # Se |x-0.5| + |y-0.5| <= s/sqrt(2), onde s é o lado, o ponto está dentro
    # de um quadrado rotacionado.
    # Para um quadrado alinhado aos eixos, a checagem é mais simples.
    # Diagonal do quadrado = diâmetro do círculo = 1. Lado s = 1/sqrt(2).
    s_div_2 = (1 / math.sqrt(2)) / 2
    lower_bound = 0.5 - s_div_2
    upper_bound = 0.5 + s_div_2

    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if (lower_bound <= x <= upper_bound) and (lower_bound <= y <= upper_bound):
            inside_square += 1
            
    # Como a área total da simulação é 1, a proporção é a estimativa da área.
    proportion = inside_square / num_samples
    estimated_area = proportion
    
    return estimated_area, proportion

# ---------------------------
# Endpoints da API
# ---------------------------

@app.route('/')
def index():
    """Endpoint principal que lista as rotas disponíveis."""
    return jsonify({
        "message": "Olá do app Flask + Kubernetes!",
        "endpoints": [
            "/docker-info",
            "/montecarlo/<n>",
            "/montecarlo-distributed/<n>",
            "/montecarlo-square/<n>" # Novo endpoint listado aqui
        ]
    })

@app.route('/docker-info')
def docker_info():
    """Retorna informações do ambiente do container."""
    return jsonify({
        "hostname": socket.gethostname(),
        "cwd": os.getcwd(),
        "env": dict(list(os.environ.items())[:10])
    })

@app.route('/montecarlo/<int:n>')
def montecarlo_single(n):
    """Executa a simulação Monte Carlo para Pi em um único processo."""
    pi_estimate = monte_carlo_pi(n)
    return jsonify({
        "samples": n,
        "pi_estimate": pi_estimate,
        "mode": "single-cpu"
    })

@app.route('/montecarlo-distributed/<int:n>')
def montecarlo_distributed(n):
    """Executa uma parte da simulação de Pi, para ambientes distribuídos."""
    replicas = int(os.getenv("POD_REPLICAS", "1"))
    pod_name = os.getenv("POD_NAME", "local-0") # Usado para um índice simulado

    # Simula um índice de pod a partir do nome (ex: "meu-pod-2" -> 2)
    try:
        pod_index = int(pod_name.split('-')[-1])
    except (ValueError, IndexError):
        pod_index = 0

    per_pod = n // replicas
    pi_estimate = monte_carlo_pi(per_pod)

    return jsonify({
        "samples_total": n,
        "samples_this_pod": per_pod,
        "replicas": replicas,
        "pod_name": pod_name,
        "pod_index": pod_index,
        "pi_partial": pi_estimate,
        "note": "Resultados devem ser agregados externamente."
    })

@app.route('/montecarlo-square/<int:n>')
def montecarlo_square_endpoint(n):
    """
    Executa a simulação Monte Carlo para estimar a área de um quadrado
    inscrito em um círculo. Funciona em modo single ou distribuído.
    """
    replicas = int(os.getenv("POD_REPLICAS", "1"))
    
    # Determina o modo de execução e o número de amostras
    if replicas > 1:
        samples_to_run = n // replicas
        mode = f"distributed ({samples_to_run} of {n} total)"
    else:
        samples_to_run = n
        mode = "single-cpu"

    estimated_area, proportion = monte_carlo_square_area(samples_to_run)

    return jsonify({
        "samples_run": samples_to_run,
        "estimated_area": estimated_area,
        "proportion_inside": proportion,
        "theoretical_area": 0.5,
        "mode": mode
    })

# ---------------------------
# Execução da Aplicação
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

