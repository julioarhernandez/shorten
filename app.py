from flask import Flask, request, redirect

app = Flask(__name__)

# ID válido actual (puedes cambiarlo en el futuro)
id_valido = "3"

# Link real de la reunión
meeting_link = "https://teams.microsoft.com/l/meetup-join/19%3ameeting_YTgxNzE3NmItYjY1MS00YzQ1LWFhZDYtYjcxOGM3ZDVhMDE2%40thread.v2/0?context=%7b%22Tid%22%3a%225318335c-fe2e-4810-8cd7-1c0bcb5f0177%22%2c%22Oid%22%3a%221cfebae2-ccce-481c-82a2-1d0572b7ff8f%22%7d"

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
