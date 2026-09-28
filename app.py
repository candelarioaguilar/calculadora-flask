import math
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Configura tu cliente de Gemini con tu API Key
# (Reemplaza 'PON_AQUI_TU_API_KEY' por tu clave real o guárdala de forma segura)
client = genai.Client(api_key="PON_AQUI_TU_API_KEY")


@app.route("/")
def index():
  return "Servidor activo. Visita /calculadora para acceder al módulo profesional y chat."


@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
  resultado_canal = None
  resultado_shannon = None
  respuesta_ia = None

  if request.method == "POST":
    tipo_accion = request.form.get("tipo_accion")

    # 1. Capacidad de Canal
    if tipo_accion == "canal":
      try:
        B = float(request.form.get("ancho_banda", 0))
        S_N = float(request.form.get("snr", 0))
        C = B * math.log2(1 + S_N)
        resultado_canal = f"{C:.4f} bps (bits por segundo)"
      except ValueError:
        resultado_canal = "Error en los datos ingresados."

    # 2. Cuantificación No Uniforme (Ley Mu)
    elif tipo_accion == "shannon":
      try:
        M = float(request.form.get("m_val", 255))
        valores_str = request.form.get("valores_x", "")
        max_val = float(request.form.get("max_val", 100))

        if valores_str:
          lista_x = [float(v.strip()) for v in valores_str.split(",")]
          salida_procesada = []
          for x in lista_x:
            norm = x / max_val if max_val != 0 else 0
            signo = 1 if x >= 0 else -1
            abs_norm = abs(norm)
            if (1 + M) > 0 and (1 + M * abs_norm) > 0:
              px = signo * (math.log(1 + M * abs_norm) / math.log(1 + M))
            else:
              px = 0
            salida_procesada.append(f"X: {x} -> Px(μ): {px:.4f}")

          resultado_shannon = (
              f"Procesamiento Ley μ completado. Resultados: {salida_procesada}"
          )
        else:
          resultado_shannon = "Ingresa valores válidos para X."
      except ValueError:
        resultado_shannon = "Error en el formato de los datos."

    # 3. Chat con Gemini
    elif tipo_accion == "chat_ia":
      pregunta = request.form.get("pregunta_usuario", "")
      if pregunta:
        try:
          # Usamos el modelo recomendado para texto
          response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=(
                  "Eres un asistente experto en telecomunicaciones y teoría de"
                  f" la información. Responde de forma clara y técnica: {pregunta}"
              ),
          )
          respuesta_ia = response.text
        except Exception as e:
          respuesta_ia = f"Error al conectar con la IA: {str(e)}"
      else:
        respuesta_ia = "Por favor escribe una pregunta para la IA."

  return render_template(
      "calculadora.html",
      resultado_canal=resultado_canal,
      resultado_shannon=resultado_shannon,
      respuesta_ia=respuesta_ia,
  )


if __name__ == "__main__":
  app.run(debug=True)