import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import youtube_dl
import threading
import time
import os
import json

def download_video(url, format, download_path):
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }] if format == 'mp3' else [],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_duration = info_dict.get('duration', 0)
        ydl.download([url])
    return video_duration

def start_download():
    url = url_entry.get()
    format = format_var.get()
    if not url:
        messagebox.showerror('Error', 'URL is required')
        return
    threading.Thread(target=download, args=(url, format, download_path.get())).start()

def download(url, format, download_path):
    start_time = time.time()
    video_duration = download_video(url, format, download_path)
    end_time = time.time()
    download_time = end_time - start_time
    progress['value'] = 0
    while progress['value'] < 100:
        time.sleep(video_duration / 100)
        progress['value'] += 1
    messagebox.showinfo('Success', f'Download completed in {download_time} seconds')

def select_folder():
    folder_selected = filedialog.askdirectory()
    download_path.set(folder_selected)
    with open('path.json', 'w') as json_file:
        json.dump(folder_selected, json_file)

root = tk.Tk()
root.title('YouTube Downloader')

url_label = tk.Label(root, text='URL:')
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

format_var = tk.StringVar(value='mp4')
mp4_radio = tk.Radiobutton(root, text='MP4', variable=format_var, value='mp4')
mp4_radio.pack()
mp3_radio = tk.Radiobutton(root, text='MP3', variable=format_var, value='mp3')
mp3_radio.pack()

download_path = tk.StringVar()
try:
    with open('path.json', 'r') as json_file:
        download_path.set(json.load(json_file))
except FileNotFoundError:
    pass

folder_button = tk.Button(root, text='Select Folder', command=select_folder)
folder_button.pack()

download_button = tk.Button(root, text='Download', command=start_download)
download_button.pack()

progress = ttk.Progressbar(root, length=100, mode='determinate')
progress.pack()

root.mainloop()
