from flask import Flask, jsonify # type: ignore
import logging
import time

app = Flask(__name__)

# MONITOREO — logs del servicio
logging.basicConfig(level=logging.INFO)

# METRICAS — contador de errores
errores = 0


@app.route('/')
def pagos():

    global errores

    inicio = time.time()

    logging.info("Procesando pago")

    try:

        # MONITOREO — simulacion de tiempo de respuesta
        time.sleep(1)

        tiempo = time.time() - inicio

        logging.info(f"Pago procesado en {tiempo:.2f} segundos")

        return jsonify({
            "pago": "exitoso",
            "tiempo_respuesta": f"{tiempo:.2f} segundos",
            "errores": errores
        })

    except Exception as e:

        errores += 1

        logging.error(f"Error en pagos: {str(e)}")

        return jsonify({
            "error": "Error en pagos",
            "errores": errores
        }), 500


# HEALTH CHECK
@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "pagos"
    })


app.run(host='0.0.0.0', port=5002)