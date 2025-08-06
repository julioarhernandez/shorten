
# Proyecto: Redireccionador de Enlaces a Microsoft Teams

Este proyecto permite redirigir URLs personalizadas como `/entrar?id=XS3Gl89` a un enlace real de Microsoft Teams almacenado en Google Sheets.

## Instrucciones

1. Crea una hoja en Google Sheets con dos columnas: `id` y `meeting_id`
2. Comparte la hoja con permisos de editor al correo del servicio generado en Google Cloud.
3. Ve a Render.com y crea un nuevo servicio web desde este repositorio.
4. En la sección Environment, añade una variable:
   - Key: `GOOGLE_CREDS_JSON`
   - Value: (contenido completo del JSON de credenciales)
