import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from pytubefix import YouTube
import threading

root = tk.Tk()
root.title("Yt to Mp3 Revised")
root.geometry("500x200")
root.resizable(width=False, height=False)

def draw_widgets():
    txt_label.pack()
    input.pack(pady=5)
    button.pack(pady=5)

def remove_widgets():
    #txt_label.pack_forget()
    input.pack_forget()
    button.pack_forget()

def no_action_taken():
    draw_widgets()
    txt_label.config(text=orig_label)

def browse_dir():
    txt_label.config(text="Select a directory:")
    remove_widgets()
    return filedialog.askdirectory()

def on_progress_dl(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_dld = total_size - bytes_remaining
    percentage_of_dl = (bytes_dld / total_size) * 100
    progress_bar['value'] = percentage_of_dl
    process_window.update_idletasks()


def yt_to_mp3_dl():
    url = input.get()
    if url.find("watch") == -1:
        return
    dir = browse_dir()
    if not dir:
        no_action_taken()
        return
    global process_window, progress_bar
    process_window = tk.Toplevel(root)
    process_window.title("Downloading")
    process_window.geometry("500x100")
    process_window.resizable(width=False, height=False)

    def x_button():
        dl_label.config(text="Wait!!!")
        pass
    def close_window():
        txt_label.config(text=orig_label)
        draw_widgets()
        process_window.destroy()

    process_window.attributes("-toolwindow", True)
    # Process close button behaviour
    process_window.protocol("WM_DELETE_WINDOW", x_button)

    process_window.grab_set()
    process_window.focus()


    dl_label = tk.Label(process_window, text="Downloading...", font=("Courier", 10))
    dl_label.pack(pady=5)
    progress_bar = ttk.Progressbar(process_window, orient="horizontal", length=100, mode="determinate")
    (progress_bar.pack(pady=10))

    dl_thread = threading.Thread(target=yt_to_mp3_process, args=(url, dir, dl_label, close_window))
    dl_thread.start()

def yt_to_mp3_process(url, dir, dl_label, on_close):
    try:
        remove_widgets()
        txt_label.config(text="...")

        yt = YouTube(url, on_progress_callback=on_progress_dl)
        stream = yt.streams.get_audio_only()
        stream.download(output_path=dir, mp3=True)
        '''stream = yt.streams.get_highest_resolution()
        stream.download(output_path=dir)'''

        process_window.protocol("WM_DELETE_WINDOW", on_close)
        dl_label.config(text=f"Download Complete!\nSaved at {dir}")
        progress_bar.destroy()
        ok_button = tk.Button(process_window, text="Ok", font=("Courier", 12), command=on_close)
        (ok_button.pack(pady=10))
    except:
        dl_label.config(text="Network problem!\nCheck if wifi is connected!")
        progress_bar.destroy()
        return

def on_click():
    yt_to_mp3_dl()

icon = Image.open("youtube_ico.ico")
icon_resized = icon.resize((80, 80))
image = ImageTk.PhotoImage(icon_resized)

img_label = tk.Label(root, image=image)
img_label.pack()

orig_label = "Enter link below:"
txt_label = tk.Label(root, text=orig_label, font=("Courier", 12))
txt_label.pack()

input = tk.Entry(root, width=30, font=("Courier", 15))
input.pack(pady=5)

button = tk.Button(root, text="Download!", font=("Courier", 15), command=on_click)
button.pack(pady=5)

root.mainloop()
