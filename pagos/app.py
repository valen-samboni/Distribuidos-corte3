from flask import Flask, jsonify
import logging
import random
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def pagos():

    inicio = time.time()

    logging.info("Procesando pago")

    falla = random.choice([True, False])

    if falla:

        logging.error("Error en el servicio de pagos")

        return jsonify({
            "error": "Servicio de pagos caído"
        }), 500

    tiempo = time.time() - inicio

    logging.info(f"Pago procesado en {tiempo:.2f} segundos")

    return jsonify({
        "pago": "exitoso",
        "tiempo_respuesta": f"{tiempo:.2f} segundos"
    })


@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "pagos"
    })


app.run(host='0.0.0.0', port=5002)