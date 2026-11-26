from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

# Precios de los productos Brunella
PRECIOS = {
    "galletas": 10000,
    "brownies": 6000,
    "postres": 13000,
    "cookiecake_entera": 70000,
    "cookiecake_porcion": 10000
}

NOMBRES = {
    "galletas": "Galletas",
    "brownies": "Brownies",
    "postres": "Postres",
    "cookiecake_entera": "Cookie Cake entero",
    "cookiecake_porcion": "Cookie Cake porción"
}

@app.get("/")
def inicio():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<path:archivo>")
def archivos(archivo):
    return send_from_directory(BASE_DIR, archivo)


@app.post("/calcular")
def calcular():
    datos = request.get_json(silent=True) or {}

    producto = str(datos.get("producto", "")).strip().lower()
    cantidad_recibida = datos.get("cantidad", 0)

    if producto not in PRECIOS:
        return jsonify({"error": "Selecciona un producto válido."}), 400

    try:
        cantidad = int(cantidad_recibida)
    except (TypeError, ValueError):
        return jsonify({"error": "Ingresa una cantidad válida."}), 400

    if cantidad < 1:
        return jsonify({"error": "La cantidad debe ser mayor que cero."}), 400

    precio_unitario = PRECIOS[producto]
    total = precio_unitario * cantidad

    return jsonify({
        "producto": NOMBRES[producto],
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": total,
        "mensaje": "Cálculo realizado correctamente."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)