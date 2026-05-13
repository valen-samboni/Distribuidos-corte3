from flask import Flask, jsonify
import logging
import requests
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

errores = 0

@app.route('/')
def pedidos():

    global errores

    inicio = time.time()

    logging.info("Procesando pedido")

    try:

        inventario = requests.get(
            "http://inventario:5001/health",
            timeout=2
        ).json()

        pagos = requests.get(
            "http://pagos:5002/health",
            timeout=2
        ).json()

        tiempo = time.time() - inicio

        logging.info(f"Pedido procesado en {tiempo:.2f} segundos")

        return jsonify({
            "pedido": "procesado correctamente",
            "inventario": inventario,
            "pagos": pagos,
            "tiempo_respuesta": f"{tiempo:.2f} segundos",
            "errores": errores
        })

    except Exception as e:

        errores += 1

        logging.error(f"Error procesando pedido: {str(e)}")
        logging.error(f"Errores acumulados: {errores}")

        return jsonify({
            "error": "No se pudo procesar el pedido",
            "errores": errores
        }), 500


@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "pedidos"
    })


app.run(host='0.0.0.0', port=5000)