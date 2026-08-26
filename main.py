from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import os

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SoundCloud Downloader</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 60px auto;
            padding: 20px;
        }

        h1 {
            margin-bottom: 30px;
        }

        input {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            font-size: 16px;
            margin-bottom: 12px;
        }

        button {
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
        }

        .status {
            margin-top: 20px;
        }
    </style>
</head>

<body>

    <h1>SoundCloud Downloader</h1>

    <form method="POST" action="/download">
        <input
            type="url"
            name="url"
            placeholder="Paste SoundCloud URL"
            required
        >

        <button type="submit">Download</button>
    </form>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


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
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            filename = ydl.prepare_filename(info)

        return f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>

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

    filepath = os.path.join(DOWNLOAD_DIR, filename)

    return FileResponse(
        filepath,
        filename=filename,
        media_type="application/octet-stream"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000
    )
