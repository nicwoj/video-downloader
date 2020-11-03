from tkinter import *
from tkinter import ttk # dropdown
from tkinter import filedialog # file download location
from pytube import YouTube

folder_path = ""
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

# used to download the video
def download_video():
    choice = choices_combo.get()            # get user's video quality choice
    link = link_entry.get("1.0", "end-1c")  # get user's link entry

    if(len(link) > 1):
        for line in link.splitlines():
            yt = YouTube(line)

            if(choice == choices[0]): # 720p
                select = yt.streams.filter(progressive=True, file_extension="mp4").last()
            elif(choice == choices[1]): # 360p
                select = yt.streams.filter(progressive=True).first()
            elif(choice == choices[2]): # only audio
                select = yt.streams.filter(only_audio=True).first()
            else:
                error_label.config(text="Enter link again:", fg="red")
        
            select.download(folder_path) # download to specified folder

        error_label.config(text="Download Complete", fg="green")
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
choices = ["720p", "360p", "Audio Only"]
choices_combo = ttk.Combobox(root, width=25, values=choices)
choices_combo.grid()

# download button
download_button = Button(root, text="Download", width=10, bg="slate gray", fg="white", command=download_video)
download_button.grid()

root.mainloop()