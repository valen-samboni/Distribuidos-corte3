from flask import Flask, jsonify
import logging
import time

app = Flask(__name__)

# MONITOREO — logs del servicio
logging.basicConfig(level=logging.INFO)

# METRICAS — contador de errores
errores = 0


@app.route('/')
def inventario():

    global errores

    inicio = time.time()

    logging.info("Consultando inventario")

    try:

        # MONITOREO — simulacion de tiempo de respuesta
        time.sleep(1)

        # METRICAS — tiempo de respuesta
        tiempo = time.time() - inicio

        logging.info(f"Inventario consultado en {tiempo:.2f} segundos")

        return jsonify({
            "inventario": "disponible",
            "tiempo_respuesta": f"{tiempo:.2f} segundos",
            "errores": errores
        })

    except Exception as e:

        errores += 1

        logging.error(f"Error en inventario: {str(e)}")

        return jsonify({
            "error": "Error en inventario",
            "errores": errores
        }), 500


# HEALTH CHECK
@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "inventario"
    })


app.run(host='0.0.0.0', port=5001)

