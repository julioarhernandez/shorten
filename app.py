
import os
from flask import Flask, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO

app = Flask(__name__)

# Google Sheets Config
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SPREADSHEET_NAME = 'shorten-ss'  # Cambia por el nombre de tu hoja

# Conectar a Google Sheets desde variable de entorno
def conectar_hoja():
    creds_json = os.environ['GOOGLE_CREDS_JSON']
    creds_dict = json.load(StringIO(creds_json))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    hoja = client.open(SPREADSHEET_NAME).sheet1
    return hoja

# Buscar el meeting_id asociado al ID
def obtener_meeting_link(id_usuario):
    hoja = conectar_hoja()
    registros = hoja.get_all_records()
    for fila in registros:
        if fila['url'] == id_usuario:
            return f"https://teams.microsoft.com/l/meetup-join/{fila['meeting_id']}"
    return None

@app.route("/")
def home():
    return "Usa el enlace /entrar?id=TU_ID"

@app.route("/entrar")
def entrar():
    id_recibido = request.args.get("id")

    if not id_recibido:
        return "❌ Debes proporcionar un ID."

    meeting_link = obtener_meeting_link(id_recibido)

    if meeting_link:
        return redirect(meeting_link)
    else:
        return "⚠️ Este ID no está registrado o ha expirado. Solicita uno nuevo."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
