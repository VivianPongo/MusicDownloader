from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL, DownloadError
import os
import uuid

app = FastAPI()

# Configuración de CORS (permite comunicación con frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://musicdownloader-je4i.onrender.com/"],  # Cambia según frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🎵 Backend activo. Listo para descargar música."}

@app.post("/download")
def download_audio(
    url: str = Form(...),
    formato: str = Form("mp3"),
    calidad: str = Form("192")
):
    try:
        # Crear carpeta de salida
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        # Asegurar que ffmpeg esté en el mismo directorio
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg")

        # Nombre único para evitar conflictos
        unique_id = str(uuid.uuid4())[:8]
        outtmpl = os.path.join(output_dir, f'%(title)s_{unique_id}.%(ext)s')

        # Opciones de descarga
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': calidad,
            }],
            'outtmpl': outtmpl,
            'noplaylist': True,
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            final_filename = filename.rsplit('.', 1)[0] + f'.{formato}'

        if not os.path.exists(final_filename):
            raise FileNotFoundError("No se generó el archivo de salida.")

        return FileResponse(
            path=final_filename,
            filename=os.path.basename(final_filename),
            media_type='audio/mpeg'
        )

    except DownloadError as e:
        return JSONResponse(status_code=400, content={"error": "Error al descargar el audio", "detalle": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Error interno del servidor", "detalle": str(e)})
