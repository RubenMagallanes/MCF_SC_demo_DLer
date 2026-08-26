from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

import yt_dlp
import os


app = FastAPI()


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

# you will probably need to update this path with the location of your ffmpeg install. 
#instructions in README.md
FFMPEG_LOCATION = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/download", response_class=HTMLResponse)
def download(url: str = Form(...)):

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

            info = ydl.extract_info(
                url,
                download=True
            )

            filename = ydl.prepare_filename(info)


        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">

            <h2>Download complete!</h2>

            <p>{info.get("title", "Track")}</p>

            <a href="/files/{os.path.basename(filename)}">
                Download file
            </a>

            <br><br>

            <a href="/">
                Download another
            </a>

        </body>
        </html>
        """


    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">

            <h2>Download failed</h2>

            <pre>{e}</pre>

            <a href="/">Try again</a>

        </body>
        </html>
        """


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
