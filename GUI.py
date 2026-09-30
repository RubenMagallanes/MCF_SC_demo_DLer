import tkinter as tk
from tkinter import ttk


def main():
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
        text="Start Server"
    )
    start_button.pack(side="left", padx=5)

    stop_button = ttk.Button(
        button_frame,
        text="Stop Server"
    )
    stop_button.pack(side="left", padx=5)

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
    
    