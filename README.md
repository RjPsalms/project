# YouTube Playlist Downloader App

#### Video Demo: 

#### Description:
This is a simple YouTube downloader app built in Python using the the new CustomTkinter library for the GUI, and Pytube for fetching and downloading YouTube videos and playlists. No ads, simply caopy your link from Youtube then paste, then download the type you want; audio or video.

    > This is my final project for CS50x, my 2nd CS50 course after finishing CS50p, this course is way harder since I have to learn a bit of everything, but still I ended up building what I'm already familiar with, the 'CustomTKinter GUI' and Python. I built this ahead of the course, for my personal use since I had been looking for a way to download playlist from Youtube before and haven't found a decent program till now. So this is more of a personal project. 
    
    > The biggest challenge here is once again the integration of the logic to the GUI, or in general, object-oriented-programming. The Pytube library is already very friendly, just a few lines of codes and you have your videos downloaded. What consumed my time in this project is bulding the user interface and integrating the logic of the code. Many things that seem easy in my mind took hours for me to implement, just the simple CANCEL and CLEAR buttons took me a day! But well, learning and building this on my own is rewarding nonetheless. I'm forever thankful to Harvard and to Professor David for this lesson of a lifetime for FREE! I hope some people would find this useful as well.


## Features

- Download individual YouTube videos in both video and audio formats.
- Download entire YouTube playlists in both video and audio formats.
- Display thumbnails of the videos being downloaded.
- Track download progress with a progress bar and percentage display.
- Ability to cancel ongoing downloads.
- Choose download path using a file dialog.

## Requirements

- Python 3.x
- Pytube (`pip install pytube`)
- Pillow (`pip install pillow`)

## How to Use

1. Clone or download the repository to your local machine.
2. Make sure you have Python installed on your system.
3. Install the required dependencies using pip:
4. Run the `youtube_downloader.py` script.
5. Paste the link of the YouTube video or playlist in the input field.
6. Choose the download format (video or audio) and click the corresponding download button.
7. Monitor the download progress in the text box and cancel downloads if needed.

## Screenshots

![YT_Playlist downloader](images\YT_downloader.png)


## Notes

- This app is for educational purposes only. Respect YouTube's terms of service and use it responsibly.
- Downloads are subject to YouTube's restrictions and availability of videos.

