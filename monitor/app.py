from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/monitor')
def monitor():

    servicios = {}

    lista = {
        "pedidos": "http://pedidos:5000/health",
        "inventario": "http://inventario:5001/health",
        "pagos": "http://pagos:5002/health"
    }

    for nombre, url in lista.items():

        try:

            respuesta = requests.get(url, timeout=2)

            servicios[nombre] = {
                "estado": respuesta.json(),
                "codigo": respuesta.status_code
            }

        except:

            servicios[nombre] = {
                "estado": "caido"
            }

    return jsonify(servicios)


@app.route('/health')
def health():

    return jsonify({
        "status": "ok",
        "servicio": "monitor"
    })


app.run(host='0.0.0.0', port=5003)