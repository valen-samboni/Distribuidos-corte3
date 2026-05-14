from flask import Flask, jsonify # type: ignore
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def inventario():

    inicio = time.time()

    logging.info("Consultando inventario")

    time.sleep(1)

    tiempo = time.time() - inicio

    logging.info(f"Inventario consultado en {tiempo:.2f} segundos")

    return jsonify({
        "inventario": "disponible",
        "tiempo_respuesta": f"{tiempo:.2f} segundos"
    })


@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "inventario"
    })


app.run(host='0.0.0.0', port=5001)