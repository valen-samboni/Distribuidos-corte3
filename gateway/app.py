from flask import Flask, jsonify # type: ignore
import requests # type: ignore
import logging
import time

app = Flask(__name__)

# MONITOREO — logs del gateway
logging.basicConfig(level=logging.INFO)

# METRICAS
errores_pagos = 0

# CIRCUIT BREAKER
circuit_breaker = False


@app.route('/')
def gateway():

    global errores_pagos
    global circuit_breaker

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

        # CIRCUIT BREAKER
        if circuit_breaker:

            logging.warning("Circuit Breaker ACTIVADO para pagos")

            pagos = {
                "estado": "servicio de pagos deshabilitado temporalmente"
            }

        else:

            logging.info("Consultando servicio pagos")

            pagos = requests.get(
                "http://pagos:5002/",
                timeout=3
            ).json()

        # METRICAS — tiempo de respuesta
        tiempo = time.time() - inicio

        logging.info(f"Solicitud completada en {tiempo:.2f} segundos")

        return jsonify({
            "gateway": "activo",
            "pedidos": pedidos,
            "inventario": inventario,
            "pagos": pagos,
            "circuit_breaker": circuit_breaker,
            "errores_pagos": errores_pagos,
            "tiempo_respuesta": f"{tiempo:.2f} segundos"
        })

    except Exception as e:

        errores_pagos += 1

        logging.error(f"Error en gateway: {str(e)}")
        logging.error(f"Errores acumulados pagos: {errores_pagos}")

        # CIRCUIT BREAKER
        if errores_pagos >= 3:

            circuit_breaker = True

            logging.warning("Circuit Breaker ACTIVADO")

        return jsonify({
            "error": "Servicio no disponible",
            "errores_pagos": errores_pagos,
            "circuit_breaker": circuit_breaker
        }), 500


# HEALTH CHECK
@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "gateway"
    })


# METRICAS
@app.route('/metricas')
def metricas():

    return jsonify({
        "errores_pagos": errores_pagos,
        "circuit_breaker": circuit_breaker
    })


app.run(host='0.0.0.0', port=5004)

