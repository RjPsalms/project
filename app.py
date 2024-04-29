import os
import threading
import requests
from io import BytesIO
from tkinter import filedialog
from PIL import Image, ImageTk
from pytube import YouTube, Playlist
import customtkinter as ctk

# Constants
DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
DEFAULT_THUMBNAIL_PATH = "images/def_img.png"

# Function to update download progress
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_dload = total_size - bytes_remaining
    progress_percent = int(bytes_dload / total_size * 100)
    app.download_label.configure(text=f"  {progress_percent} %")
    app.progress_bar.set(progress_percent / 100)
    app.update_idletasks()

# Main Application Class
class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("YT Playlist Downloader")
        self.geometry("800x500")
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.resizable(width=False, height=True)
        self.setup_ui()
        self.is_downloading = False
        self.cancel_flag = False
        self.download_path = DEFAULT_DOWNLOAD_PATH

    def setup_ui(self):
        # Entry field for the playlist link
        self.link_entry = ctk.CTkEntry(self, placeholder_text="    ......  control + v to paste Youtube links  ......")
        self.link_entry.grid(row=0, column=0, padx=10, pady=15, sticky="ew", columnspan=4)

        # Thumbnail display
        self.default_image_pil = Image.open(DEFAULT_THUMBNAIL_PATH)
        self.default_image = ctk.CTkImage(self.default_image_pil, size=(320, 170))
        self.center_image = ctk.CTkLabel(self, text="", image=self.default_image)
        self.center_image.grid(row=1, column=2, rowspan=2, columnspan=2, sticky="nsew")

        # Download buttons
        self.create_download_buttons()

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate", progress_color="lightgreen")
        self.progress_bar.grid(row=3, column=0, columnspan=4, padx=30, pady=10, sticky="ew")
        self.progress_bar.set(0)
        self.download_label = ctk.CTkLabel(self, text="  0 %", font=("", 15), text_color="green")
        self.download_label.grid(row=3, column=3, padx=25, sticky="e")

        # Text box for downloaded file names
        self.text_box = ctk.CTkTextbox(self, state="normal")
        self.text_box.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Clear text button
        self.clear_text_button = ctk.CTkButton(self, text="CLEAR", fg_color="gray", corner_radius=50, command=self.clear_text_box)
        self.clear_text_button.grid(row=6, column=2, padx=20, pady=10, sticky="ew")

        # Browse button for selecting download path
        self.browse_button = ctk.CTkButton(self, text="Download path", fg_color="gray", corner_radius=50, command=self.browse_path)
        self.browse_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # Cancel button
        self.cancel_button = ctk.CTkButton(self, text="CANCEL", font=("", 15), text_color="black", corner_radius=50,
                                            fg_color="gray", hover_color="red", command=self.cancel_download, state="disabled")
        self.cancel_button.grid(row=6, column=3, padx=20, pady=10, sticky="ew")

    def create_download_buttons(self):
        buttons_data = [
            ("Playlist (Video)", self.download_playlist_video),
            ("Playlist (Audio)", self.download_playlist_audio),
            ("Single Video", self.download_single_video),
            ("Single Audio", self.download_single_audio)
        ]

        for i, (text, command) in enumerate(buttons_data):
            button = ctk.CTkButton(self, height=55, text=text, font=("", 15), fg_color="gray", command=command)
            button.grid(row=i // 2 + 1, column=i % 2, padx=15, pady=15, sticky="ew")

    def browse_path(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.download_path = selected_path

    def cancel_download(self):
        if self.is_downloading:
            self.cancel_flag = True
            self.text_box.insert("end", "\n ... Cancelling all downloads ...\n")
            self.text_box.see("end")
            self.cancel_button.configure(state="disabled")
        else:
            self.text_box.insert("end", "\n Error: No download in progress.\n")
            self.text_box.see("end")

    def clear_text_box(self):
        self.text_box.delete("1.0", "end")
        self.link_entry.delete(0, "end")
        self.center_image.configure(image=self.default_image)
        self.download_label.configure(text="  0 %")
        self.progress_bar.set(0)
        self.cancel_flag = False

    def load_thumbnail(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        thumbnail = ctk.CTkImage(img, size=(320, 170))
        return thumbnail

    # Methods for downloading single videos
    def download_single_video(self):
        self.download_media("video")

    def download_single_audio(self):
        self.download_media("audio")

    def download_media(self, mode):
        if not self.link_entry.get():
            self.text_box.insert("end", f"\n Enter a {mode} link.\n")
            self.text_box.see("end")
            return

        threading.Thread(target=self.download_media_thread, args=(mode,)).start()

    def download_media_thread(self, mode):
        app.download_label.configure(text=f"({mode.capitalize()})")
        self.is_downloading = True
        self.cancel_flag = False
        self.cancel_button.configure(state="normal")

        try:
            p_link = self.link_entry.get()
            yt_video = YouTube(p_link)
            thumbnail_url = yt_video.thumbnail_url
            thumbnail_image = self.load_thumbnail(thumbnail_url)
            self.center_image.configure(image=thumbnail_image)
        except Exception as e:
            self.text_box.insert("end", f"\nError: {str(e)}\n")
            self.text_box.see("end")
            self.is_downloading = False
            return

        self.text_box.insert("end", f"\n~ Getting {yt_video.title} ({mode.capitalize()}) ... \n")
        self.text_box.see("end")
        app.progress_bar.set(0)
        yt_video.register_on_progress_callback(on_progress)

        try:
            stream = yt_video.streams.get_highest_resolution() if mode == "video" else yt_video.streams.get_audio_only()
            download_path = self.download_path
            file_extension = "mp4" if mode == "video" else "mp3"
            file_suffix = "_video" if mode == "video" else "_audio"
            file_name = f"{yt_video.title}{file_suffix}.{file_extension}"
            file_path = os.path.join(download_path, file_name)
            stream.download(output_path=download_path, filename=file_name)
        except Exception as e:
            self.text_box.insert("end", f"\nError: {str(e)}\n")
            self.text_box.see("end")

        if self.cancel_flag:
            return

        self.text_box.insert("end", f"~ Downloaded successfully!\n")
        self.text_box.see("end")
        self.link_entry.delete(0, "end")
        self.cancel_button.configure(state="disabled")
        self.is_downloading = False

    # Methods for playlist download
    def download_playlist_video(self):
        self.download_playlist_media("video")

    def download_playlist_audio(self):
        self.download_playlist_media("audio")

    def download_playlist_media(self, mode):
        if not self.link_entry.get():
            self.text_box.insert("end", f"\n Enter a Playlist link.\n")
            self.text_box.see("end")
            return

        threading.Thread(target=self.download_playlist_media_thread, args=(mode,)).start()

    def download_playlist_media_thread(self, mode):
        app.download_label.configure(text=f" Downloading ({mode.capitalize()})")
        self.is_downloading = True
        self.cancel_flag = False
        self.cancel_button.configure(state="normal")

        try:
            p_link = self.link_entry.get()
            link = Playlist(p_link)
            num_videos = len(link.video_urls)
        except Exception as e:
            self.text_box.insert("end", f"\nError: {str(e)}\n")
            self.text_box.see("end")
            self.is_downloading = False
            return

        for idx, video_url in enumerate(link.video_urls, start=1):
            if self.cancel_flag:
                break

            try:
                yt_video = YouTube(video_url)
                thumbnail_url = yt_video.thumbnail_url
                thumbnail_image = self.load_thumbnail(thumbnail_url)
                self.center_image.configure(image=thumbnail_image)
            except Exception as e:
                self.text_box.insert("end", f"\nError: {str(e)}\n")
                self.text_box.see("end")
                continue

            self.text_box.insert("end", f"\n Files to download: {num_videos}\n")
            self.text_box.insert("end", f"\n~ Getting {yt_video.title} ({mode.capitalize()}) ... \n")
            self.text_box.see("end")
            app.progress_bar.set(0)
            yt_video.register_on_progress_callback(on_progress)

            try:
                stream = yt_video.streams.get_highest_resolution() if mode == "video" else yt_video.streams.get_audio_only()
                download_path = self.download_path
                file_extension = "mp4" if mode == "video" else "mp3"
                file_suffix = "_video" if mode == "video" else "_audio"
                file_name = f"{yt_video.title}{file_suffix}.{file_extension}"
                file_path = os.path.join(download_path, file_name)
                stream.download(output_path=download_path, filename=file_name)
            except Exception as e:
                self.text_box.insert("end", f"\nError: {str(e)}\n")
                self.text_box.see("end")
                continue

            if self.cancel_flag:
                break

            self.text_box.insert("end", f"~ Downloaded successfully!\n")
            self.text_box.see("end")
            num_videos -= 1

        self.link_entry.delete(0, "end")
        self.cancel_button.configure(state="disabled")
        self.is_downloading = False

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
