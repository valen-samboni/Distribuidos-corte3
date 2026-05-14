from flask import Flask, jsonify
import requests
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

errores = 0

@app.route('/')

def gateway():

    global errores

    inicio = time.time()

    logging.info("Gateway procesando solicitud")

    try:

        pedidos = requests.get(
            "http://pedidos:5000/",
            timeout=3
        ).json()

        inventario = requests.get(
            "http://inventario:5001/",
            timeout=3
        ).json()

        pagos = requests.get(
            "http://pagos:5002/",
            timeout=3
        ).json()

        tiempo = time.time() - inicio

        logging.info(f"Solicitud completada en {tiempo:.2f} segundos")

        return jsonify({
            "gateway": "activo",
            "pedidos": pedidos,
            "inventario": inventario,
            "pagos": pagos,
            "tiempo_respuesta": f"{tiempo:.2f} segundos",
            "errores": errores
        })

    except Exception as e:

        errores += 1

        logging.error(f"Error en gateway: {str(e)}")
        logging.error(f"Errores acumulados: {errores}")

        return jsonify({
            "error": "Servicio no disponible",
            "errores": errores
        }), 500


@app.route('/health')

def health():

    return jsonify({
        "status": "ok",
        "servicio": "gateway"
    })


app.run(host='0.0.0.0', port=5004)