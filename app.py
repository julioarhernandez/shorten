import os
from flask import Flask, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO
from datetime import datetime
import pytz

app = Flask(__name__)

# Google Sheets Config
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SPREADSHEET_NAME = 'shorten-ss'

# Timezone configuration (ajusta según tu zona horaria)
TIMEZONE = pytz.timezone('America/New_York')  # Cambia según tu ubicación

# Conectar a Google Sheets desde variable de entorno
def conectar_hoja():
    creds_json = os.environ['GOOGLE_CREDS_JSON']
    creds_dict = json.load(StringIO(creds_json))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    hoja = client.open(SPREADSHEET_NAME).sheet1
    return hoja

# Verificar si la hora actual está dentro del rango permitido
def verificar_horario(id_usuario):
    ahora = datetime.now(TIMEZONE)
    hora_actual = ahora.time()
    
    # Si el ID empieza con "AM"
    if id_usuario.startswith("AM"):
        # Permitir entre 7:45 AM y 11:00 AM
        inicio = datetime.strptime("07:45", "%H:%M").time()
        fin = datetime.strptime("11:00", "%H:%M").time()
        return inicio <= hora_actual <= fin
    
    # Si el ID empieza con "PM"
    elif id_usuario.startswith("PM"):
        # Permitir entre 5:45 PM y 8:59 PM 
        inicio = datetime.strptime("17:45", "%H:%M").time()
        fin = datetime.strptime("20:59", "%H:%M").time()
        return inicio <= hora_actual <= fin
    
    # Si no tiene prefijo válido, denegar acceso
    return False

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
    
    # Verificar horario permitido
    if not verificar_horario(id_recibido):
        ahora = datetime.now(TIMEZONE)
        hora_actual = ahora.strftime("%I:%M %p")
        
        if id_recibido.startswith("AM"):
            return f"⏰ Este enlace solo está disponible entre 7:45 AM y 12:00 PM. Hora actual: {hora_actual}"
        elif id_recibido.startswith("PM"):
            return f"⏰ Este enlace solo está disponible entre 5:45 PM y 9:59 PM. Hora actual: {hora_actual}"
        else:
            return "❌ ID inválido."
    
    # Buscar el meeting link
    meeting_link = obtener_meeting_link(id_recibido)
    
    if meeting_link:
        return redirect(meeting_link)
    else:
        return "⚠️ Este ID no está registrado o ha expirado. Solicita uno nuevo."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
