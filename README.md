# MCF_SC_demo_DLer

## pre
set up tailscale on both your host pc and your phone.
activeate venv `.\venv\Scripts\Activate.ps1`
install requirements ``

#run
on the pc run `python main.py` to host the API.
visit the page on your phone - there will be a line like this in the server output in pwoershell `Uvicorn running on ←[1mhttp://0.0.0.0:8000←[0m (Press CTRL+C to quit)` - note the port its running on `0.0.0.0:<PORT NUMBER>`
you can run `tailscale status` to check your computers tailscale ip addr.

paste the soundcloud track url in to the input box and the server will download it to your pc if a stream is available


example track that can be downloaded. 
https://soundcloud.com/koltercologne/take-five