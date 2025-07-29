from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL, DownloadError
from io import BytesIO
import os
import uuid
import shutil

app = FastAPI()

# CORS para permitir comunicación con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # 👈 clave para descargar archivos
)


@app.get("/")
def root():
    return {"message": "🎵 Backend activo. Listo para descargar música."}


@app.post("/download")
def download_audio(url: str = Form(...),
                   formato: str = Form("mp3"),
                   calidad: str = Form("192")):
    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        # Ruta de ffmpeg en Replit (ajústalo si cambias el entorno)
        ffmpeg_path = "/nix/store/15alrig3q4xjwfc3rbnsgj4bj29zn6ww-ffmpeg-7.1.1-bin/bin/ffmpeg"

        # ID único
        unique_id = str(uuid.uuid4())[:8]
        outtmpl = os.path.join(output_dir, f'%(title)s_{unique_id}.%(ext)s')

        ydl_opts = {
            'format':
            'bestaudio/best',
            'ffmpeg_location':
            ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': calidad,
            }],
            'outtmpl':
            outtmpl,
            'noplaylist':
            True,
            'quiet':
            True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            downloaded_file_path = filename.rsplit('.', 1)[0] + f'.{formato}'

        if not os.path.exists(downloaded_file_path):
            raise FileNotFoundError("No se generó el archivo de salida.")

        # Obtener título y sanitizarlo
        video_title = info.get("title", f"audio_{unique_id}")
        safe_title = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_"
                             for c in video_title)
        final_filename = f"{safe_title}.{formato}"

        print(f"[✅ DEBUG] Final filename: {final_filename}")
        print(f"[✅ DEBUG] Downloaded file path: {downloaded_file_path}")

        # Leer en memoria
        file_bytes = BytesIO()
        with open(downloaded_file_path, "rb") as f:
            shutil.copyfileobj(f, file_bytes)
        file_bytes.seek(0)

        # Eliminar archivo temporal
        os.remove(downloaded_file_path)

        headers = {
            "Content-Disposition": f'attachment; filename="{final_filename}"'
        }

        return StreamingResponse(file_bytes,
                                 media_type='audio/mpeg',
                                 headers=headers)

    except DownloadError as e:
        print(f"[❌ ERROR] Descarga: {e}")
        return JSONResponse(status_code=400,
                            content={
                                "error": "Error al descargar el audio",
                                "detalle": str(e)
                            })
    except Exception as e:
        print(f"[❌ ERROR] Interno: {e}")
        return JSONResponse(status_code=500,
                            content={
                                "error": "Error interno del servidor",
                                "detalle": str(e)
                            })
