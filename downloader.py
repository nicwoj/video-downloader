from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
from bs4 import BeautifulSoup
import requests
import re
import json

WINDOW_TITLE = "Video Downloader"
WINDOW_WIDTH = 390
WINDOW_HEIGHT = 300

# used for getting save folder location
def open_location():
    global folder_path
    folder_path = filedialog.askdirectory()

    if(len(folder_path) > 1):
        error_label_loc.config(text=folder_path, fg="green")
    else:
        error_label_loc.config(text="Choose a location to save the file:", fg="red")

def get_video(link):
    result = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) \
        Gecko/20100101 Firefox/82.0"}).content

    soup = BeautifulSoup(result, "html.parser")
    script = str(soup.find_all('script'))
    pattern = re.compile(r"https:\/\/ssrweb\.zoom\.us\/cmr\/replay\/.*")
    result = pattern.search(script)
    video = result.group(0)[:-2] # extracts video link
    #print("full link: ", video)
    return video

# combines the chosen folder path with the file name
def set_folder_path(folder_path, link):
    video_link = get_video(link)                    # extracts the link
    result = re.search("GMT.*?(.mp4)", video_link)  # extracts file name from link
    file_name = result.group(0)
    #file_name = result.group(0)[:-4]               # removes .mp4 from the end
    path = folder_path + "/" + file_name
    return path

# downloads the video
def download_video():
    choice = choices_combo.get()            # get user's video quality choice
    link = link_entry.get("1.0", "end-1c")  # get user's link entry

    if(len(link) > 1):
        if("youtu" in link[0:20]):    # YouTube video 
            for line in link.splitlines():
                yt = YouTube(line)

                if(choice == choices[0] or choice == choices[3]): # 720p or Default
                    select = yt.streams.filter(progressive=True, file_extension="mp4").last()
                elif(choice == choices[1]): # 360p
                    select = yt.streams.filter(progressive=True).first()
                elif(choice == choices[2]): # only audio
                    select = yt.streams.filter(only_audio=True).first()
                else:
                    error_label.config(text="Enter URL again:", fg="red")
            
                select.download(folder_path) # download to specified folder

            error_label.config(text="Download Complete", fg="green")
        else:   # not a YouTube video
            response = requests.get(link, stream=True)
            folder = set_folder_path(folder_path, link)
            with open(folder, "wb") as f:
                for chunk in response.iter_content(chunk_size = 1024):
                    print("test1")
                    if chunk:
                        f.write(chunk)
                        print("test2")
                    else:
                        print("err")
    else:
        error_label.config(text="Enter URL again", fg="red")


root = Tk()
root.title(WINDOW_TITLE)                                        # window title
root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))      # window size
root.columnconfigure(0, weight=1)                               # center content
#root.configure(bg="")  # window background color 

# link label and entry
link_label = Label(root, text="Enter URLs to download:")
link_label.grid()
entryVar = StringVar()
link_entry = Text(root, width=45, height=5)
link_entry.grid()

# error msg 1
error_label = Label(root, text="", fg="red")
error_label.grid()

# save file label and button
save_label = Label(root, text="Choose a location to save the file:")
save_label.grid()
folder_path = StringVar()
save_button = Button(root, width=10, bg="slate gray", fg="white", text="Browse", command=open_location)
save_button.grid()

# error msg for download location
error_label_loc = Label(root, text="", fg="red")
error_label_loc.grid()

# video quality choices
quality_label = Label(root, text="Select quality:")
quality_label.grid()
choices = ["720p", "360p", "Audio Only", "Default"]
choices_combo = ttk.Combobox(root, width=25, values=choices)
choices_combo.grid()

# download button
download_button = Button(root, text="Download", width=10, bg="slate gray", fg="white", command=download_video)
download_button.grid()

root.mainloop()