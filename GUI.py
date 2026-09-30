import tkinter as tk
from tkinter import ttk
import subprocess
import platform
import sys
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

server_process = None

def open_downloads_folder():
    if platform.system() == "Windows":
        os.startfile(DOWNLOAD_DIR)

    elif platform.system() == "Darwin":
        subprocess.Popen(["open", DOWNLOAD_DIR])

    elif system == "Linux":
        subprocess.Popen(["xdg-open", DOWNLOAD_DIR])

    else:
        print(f"Unsupported operating system: {system}. consider implementing this & submitting a pull request :)")

def append_output(text):
    output.config(state="normal")
    output.insert("end", text)
    output.see("end")
    output.config(state="disabled")


def read_output():
    while server_process is not None:
        line = server_process.stdout.readline()

        if not line:
            break

        root.after(0, append_output, line)


def start_server():
    global server_process

    if server_process is not None:
        return

    server_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    status.config(text="Status: RUNNING")
    start_button.config(state="disabled")
    stop_button.config(state="normal")

    threading.Thread(
        target=read_output,
        daemon=True
    ).start()


def stop_server():
    global server_process

    if server_process is None:
        return

    server_process.terminate()
    server_process = None

    status.config(text="Status: STOPPED")
    start_button.config(state="normal")
    stop_button.config(state="disabled")


def main():
    global root
    global status
    global start_button
    global stop_button
    global output

    root = tk.Tk()
    root.title("SoundCloud Downloader Server")
    root.geometry("700x500")

    title = ttk.Label(
        root,
        text="SoundCloud Downloader Server",
        font=("Segoe UI", 16, "bold")
    )
    title.pack(pady=(20, 10))

    status = ttk.Label(
        root,
        text="Status: STOPPED",
        font=("Segoe UI", 11)
    )
    status.pack(pady=5)

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    start_button = ttk.Button(
        button_frame,
        text="Start Server",
        command=start_server
    )
    start_button.pack(side="left", padx=5)

    stop_button = ttk.Button(
        button_frame,
        text="Stop Server",
        command=stop_server,
        state="disabled"
    )
    stop_button.pack(side="left", padx=5)
    
    downloads_button = ttk.Button(
        button_frame,
        text="Open Downloads Folder",
        command=open_downloads_folder
    )
    downloads_button.pack(side="left", padx=5)

    output = tk.Text(
        root,
        height=20,
        state="disabled"
    )
    output.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    root.mainloop()


if __name__ == "__main__":
    main()
    