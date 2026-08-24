import math
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Servidor activo. Visita /capacidad_del_canal para acceder al módulo."

@app.route('/capacidad_del_canal', methods=['GET', 'POST'])
def capacidad_del_canal():
    resultado = None
    error = None
    valor1 = None
    valor2 = None

    if request.method == 'POST':
        # 1. Capturar los datos de los inputs del formulario HTML
        valor1_raw = request.form.get('valor1')
        valor2_raw = request.form.get('valor2')

        # Conservar los valores originales para rellenar el formulario (Jinja2)
        valor1 = valor1_raw
        valor2 = valor2_raw

        # 2. Validar que los campos no estén vacíos
        if not valor1_raw or not valor2_raw or valor1_raw.strip() == "" or valor2_raw.strip() == "":
            error = "Por favor, completa ambos campos (Ancho de Banda y Relación Señal-Ruido)."
        else:
            try:
                # 3. Conversión de string a float
                ancho_banda = float(valor1_raw)
                senial_ruido = float(valor2_raw)

                # Validar restricciones físicas (el ancho de banda no puede ser negativo ni cero)
                if ancho_banda <= 0 or senial_ruido < 0:
                    error = "El ancho de banda debe ser mayor a 0 y la señal-ruido no puede ser negativa."
                else:
                    # 4. Aplicación de la fórmula real de Shannon-Hartley: C = B * log2(1 + SNR)
                    capacidad = ancho_banda * math.log2(1 + senial_ruido)

                    # Redondear a 2 decimales para una presentación limpia en pantalla
                    resultado = round(capacidad, 2)

            except ValueError:
                error = "Los valores ingresados deben ser estrictamente numéricos."

    return render_template(
        'capacidad_del_canal.html',
        resultado=resultado,
        error=error,
        valor1=valor1,
        valor2=valor2
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)