from flask import Flask, jsonify
import requests
import time
import logging

app = Flask(__name__)

# MONITOREO — logs del sistema
logging.basicConfig(level=logging.INFO)


@app.route('/monitor')
def monitor():

    servicios = {}

    lista = {
        "gateway": "http://gateway:5004/health",
        "pedidos": "http://pedidos:5000/health",
        "inventario": "http://inventario:5001/health",
        "pagos": "http://pagos:5002/health"
    }

    for nombre, url in lista.items():

        inicio = time.time()

        try:

            respuesta = requests.get(url, timeout=2)

            # METRICAS — tiempo de respuesta
            tiempo = time.time() - inicio

            logging.info(f"{nombre} activo")

            servicios[nombre] = {
                "estado": "activo",
                "codigo": respuesta.status_code,
                "tiempo_respuesta": f"{tiempo:.2f} segundos"
            }

        except Exception as e:

            logging.error(f"{nombre} caido")

            servicios[nombre] = {
                "estado": "caido",
                "error": str(e)
            }

    return jsonify(servicios)


# HEALTH CHECK
@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "monitor"
    })


app.run(host='0.0.0.0', port=5003)
