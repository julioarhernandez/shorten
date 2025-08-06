from flask import Flask, request, redirect

app = Flask(__name__)

# ID válido actual (puedes cambiarlo en el futuro)
id_valido = "3"

# Link real de la reunión
meeting_link = "https://teams.microsoft.com/l/meetup-join/ACTUAL-LINK"

@app.route("/")
def home():
    return "Usa el enlace /entrar?id=3"

@app.route("/entrar")
def entrar():
    id_recibido = request.args.get("id")

    if id_recibido == id_valido:
        return redirect(meeting_link)
    else:
        return "⚠️ Este enlace ya no es válido. Solicita el nuevo enlace al organizador."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
