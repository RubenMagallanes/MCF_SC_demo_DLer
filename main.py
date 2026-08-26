#follow MidnightCatFiesta on instagram and soundcloud

from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

import yt_dlp
import os
import uuid
import re
from datetime import datetime


app = FastAPI()


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

# you will probably need to update this path with the location of your ffmpeg install. 
#instructions in README.md
FFMPEG_LOCATION = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
ERROR_LOG = os.path.join(DOWNLOAD_DIR, "download_error_log.txt")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
# dict of [job ID] -> {
#   "status": "downloading"/"error"/"done",
#   "title": "<track title>",
#   "url": "<the link you pasted in>" 
#}
downloads = {}


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
    

    
def run_download(job_id: str, url: str):
    downloads[job_id]["status"] = "downloading"
    downloads[job_id]["url"] = url

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    #"preferredquality": "320",
                }
            ],
            "outtmpl": os.path.join(
                DOWNLOAD_DIR,
                "%(title)s.%(ext)s"
            ),
            "ffmpeg_location": FFMPEG_LOCATION,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        downloads[job_id]["status"] = "done"
        downloads[job_id]["title"] = info.get("title", "Unknown track")

    except Exception as e:
        downloads[job_id]["status"] = "error"
        error = re.sub(r"\x1b\[[0-9;]*m", "", str(e))
        
        with open(ERROR_LOG, "a", encoding="utf-8") as log:
            log.write(
                f"{datetime.now():%Y-%m-%d %H:%M} | "
                f"{url} | "
                f"{error}\n"
            )
        
        downloads[job_id]["error"] = error

@app.post("/download")
def download(
    background_tasks: BackgroundTasks,
    url: str = Form(...)
):
    url = url.strip()
    job_id = str(uuid.uuid4())
    downloads[job_id] = {
        "status": "queued"
    }
    
    background_tasks.add_task(
        run_download,
        job_id,
        url
    )
    print(f"created job with ID: {job_id}")
    return {
        "job_id": job_id
    }

@app.get("/download/{job_id}")
def get_status(job_id: str):
    job = downloads.get(job_id)

    if job is None:
        return {
            "status": "unknown"
        }

    return job

@app.get("/files/{filename}")
def get_file(filename: str):

    filepath = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    return FileResponse(
        filepath,
        filename=filename,
        media_type="application/octet-stream"
    )


# -------------------------------------------------------------------
# Run server
# -------------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000
    )
