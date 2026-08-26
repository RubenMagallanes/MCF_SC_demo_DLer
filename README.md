# MCF_SC_demo_DLer

a simple server that sits on your home pc, exposes a webpage that you can open on your phone (via tailscale), paste in a soudcloud track link, and have the server download it to your home pc, ready for when you get home. 



## setup
- set up tailscale on both your host pc and your phone.
1. activeate venv `.\venv\Scripts\Activate.ps1`
2. install requirements `pip install -r requirements.txt`
3. install ffmpeg (if its not already installed) `winget install Gyan.FFmpeg`
4. find the location of your ffmpeg installation with the following command: 
```
    Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match "Gyan.*FFmpeg|FFmpeg.*Gyan" }
```
5. paste it in to `main.py` in the variable named `FFMPEG_LOCATION`

## run

1. on the pc run `python main.py` to host the API.
2. visit the page on your phone 
    - there will be a line like this in the server output in powershell `Uvicorn running on ←[1mhttp://0.0.0.0:5000←[0m (Press CTRL+C to quit)` 
    - note the port its running on `0.0.0.0:<PORT NUMBER>`
    - run `tailscale status` to check your computers tailscale ip addr, will start with 100 eg `100.108.170.250`
    - on your phone, visit the page by sticking together the ip address and the port number like so `100.108.170.250:5000` (replaceing the numbers with whatever your address and port number is )

3. paste the soundcloud track url in to the input box and the server will download it to your pc if a stream is available
4. the track should appear on your pc in a downloads folder thats created wherever you ran python from 

note: some tracks cant be downloaded due to DRM protection. 