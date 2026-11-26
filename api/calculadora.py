import html
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


# Precios de los productos Brunella
PRECIOS = {
    "galletas": 10000,
    "brownies": 6000,
    "postres": 13000,
    "cookiecake_entera": 70000,
    "cookiecake_porcion": 10000
}

# Nombres de los productos
NOMBRES = {
    "galletas": "Galletas",
    "brownies": "Brownies",
    "postres": "Postres",
    "cookiecake_entera": "Cookie Cake entero",
    "cookiecake_porcion": "Cookie Cake porción"
}


def calcular_pedido(producto, cantidad):
    if producto not in PRECIOS:
        raise ValueError("Selecciona un producto válido.")

    if cantidad < 1:
        raise ValueError("La cantidad debe ser mayor que cero.")

    precio_unitario = PRECIOS[producto]
    total = precio_unitario * cantidad

    return {
        "producto": NOMBRES[producto],
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": total
    }


def formato_cop(valor):
    return f"${valor:,.0f}".replace(",", ".")


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        contenido = """
        <h1>Calculadora Brunella</h1>
        <p>Para calcular tu pedido, regresa al sitio y completa el formulario.</p>
        <a class="boton" href="/#calculadora">Ir a la calculadora</a>
        """

        self.enviar_pagina(contenido)

    def do_POST(self):
        try:
            longitud = int(self.headers.get("Content-Length", 0))
            datos = self.rfile.read(longitud).decode("utf-8")
            formulario = parse_qs(datos)

            producto = formulario.get("producto", [""])[0].strip().lower()
            cantidad_texto = formulario.get("cantidad", [""])[0].strip()

            if not cantidad_texto:
                raise ValueError("Ingresa una cantidad válida.")

            cantidad = int(cantidad_texto)

            resultado = calcular_pedido(producto, cantidad)

            nombre_producto = html.escape(resultado["producto"])
            precio_unitario = formato_cop(resultado["precio_unitario"])
            total = formato_cop(resultado["total"])

            contenido = f"""
            <h1>¡Gracias por elegir Brunella!</h1>

            <p>Tu cálculo se realizó correctamente.</p>

            <div class="resumen">

                <h2>Resumen de tu pedido</h2>

                <p>
                    <strong>Producto:</strong>
                    {nombre_producto}
                </p>

                <p>
                    <strong>Cantidad:</strong>
                    {resultado["cantidad"]}
                </p>

                <p>
                    <strong>Precio unitario:</strong>
                    {precio_unitario}
                </p>

                <hr>

                <h2>Total de tu pedido: {total}</h2>

            </div>

            <p>
                Este valor corresponde al cálculo de los productos
                seleccionados. Consulta por WhatsApp la disponibilidad
                de tu pedido.
            </p>

            <a class="boton"
               href="https://wa.me/573023468145"
               target="_blank">
                Consultar por WhatsApp
            </a>

            <a class="enlace" href="/#calculadora">
                Realizar otro cálculo
            </a>

            <a class="enlace" href="/">
                Volver al inicio
            </a>
            """

            self.enviar_pagina(contenido)

        except ValueError as error:
            mensaje_error = html.escape(str(error))

            contenido = f"""
            <h1>No fue posible calcular tu pedido</h1>

            <p>{mensaje_error}</p>

            <a class="boton" href="/#calculadora">
                Volver a intentarlo
            </a>
            """

            self.enviar_pagina(contenido)

    def enviar_pagina(self, contenido):

        pagina = f"""
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>Resultado | Brunella</title>

            <style>
                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    padding: 30px 15px;
                    font-family: Arial, sans-serif;
                    background: #fff5f0;
                    color: #49352f;
                }}

                .contenedor {{
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 30px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
                }}

                h1 {{
                    color: #8c5260;
                    margin-top: 0;
                }}

                .resumen {{
                    margin: 25px 0;
                    padding: 20px;
                    background: #fff5f0;
                    border-radius: 10px;
                }}

                .resumen p {{
                    margin: 14px 0;
                }}

                .resumen h2 {{
                    color: #8c5260;
                }}

                .boton {{
                    display: inline-block;
                    margin-top: 15px;
                    padding: 13px 20px;
                    background: #8c5260;
                    color: white;
                    text-decoration: none;
                    border-radius: 7px;
                }}

                .enlace {{
                    display: block;
                    margin-top: 18px;
                    color: #8c5260;
                }}
            </style>
        </head>

        <body>

            <main class="contenedor">
                {contenido}
            </main>

        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(pagina.encode("utf-8"))