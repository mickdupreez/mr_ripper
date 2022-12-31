import os
import re
import time
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import win32api
from makemkv import MakeMKV
import urllib.request
import ctypes
import subprocess
import shutil
import imdb
from tkinter import *
import threading
from datetime import datetime
from tkinter import filedialog
from PIL import Image as Im
from PIL import Image
import imdb
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class Directories:
    """
        This class checks that all the directories that are required for the program to run
        exists, if it does not it will create it. 
        Those directories are then assigned to variables used through out the program.
        The content of these directories are then placed into lists that are then
        used throughout the program.

    """
    
    def __init__(self):
        """
            This is a method that gets called each time the Directories class is initialized
        """
        self.compressed = "compressed/" # The directory where the compressed files go.
        self.plex = "plex/" # The directory where the files go that are ready to be moved uploaded.
        self.temp = "temp/" # The directory where the file gets ripped to.
        self.transcoding = "transcoding/" # The directory where the files get transcoded.
        self.uncompressed = "uncompressed/" # The directory where the files wait to be transcoded.
        self.compressed_list = os.listdir(self.compressed) # A list of items in the compressed directory
        self.plex_list = os.listdir(self.plex) # A list of items in the plex directory
        self.temp_list = os.listdir(self.temp) # A list of items in the temp directory
        self.transcoding_list = os.listdir(self.transcoding) # A list of items in the transcoding directory
        self.uncompressed_list = os.listdir(self.uncompressed) # A list of items in the uncompressed directory
        self.directories = [ # A list of all the directories variables above that is used throughout the program
            self.compressed, # The compressed directory
            self.plex, # The plex directory
            self.temp, # The temp directory
            self.transcoding, # The transcoding directory
            self.uncompressed # The uncompressed directory
        ]
        for directory in self.directories: # For each directory in the directories list
            if os.path.isdir(directory) != True: # If directory does not exist
                os.mkdir(directory) # Create directory
            else: # Skip if directory exists
                pass
            
            
root = Tk()
root.title("Mr Ripper")
root.iconbitmap("icon.ico")
root.geometry("1491x900")
root.resizable(False, False)

# Define colors
background1 = "#282a36"
background2 = "#44475a"
white = "#f8f8f2"
navy = "#6272a4"
cyan = "#8be9fd"
green = "#50fa7b"
orange = "#ffb86c"
pink = "#ff79c6"
purple = "#bd93f9"
red = "#ff5555"
yellow = "#f1fa8c"

# Load default background image
default_background = PhotoImage(file="default.png")

# Define intro text
intro = """     Welcome to Mr Ripper's Movie Ripper.
    This Program will Automatically Rip and
    Transcode and Blu-Ray or DVD Movies.
    add it to your media collection.
    
"""

# Define instructions text
instructions1 = """This list below contains successfully transcoded movies.
Once verified, the file will be moved to your collection."""
instructions2 = """ This is a list of All your Movies. These Movies have
already been organized into directories by Letter for you.
All The Movies are inside of the "plex' directory.
"""

# Define que text
que_text1 = """There are currently no Movies waiting to
be transcoded. Movies will be added to 
the que if 4 movies are being transcoded."""
que_text2 = """ There are currently some Movies waiting
to be transcoded. Please wait until this list
is emty before quitting."""

# Define info label text
info_label = """This program is in beta, there are still
some bugs that need to ironed out.
Check out the github for Documentation"""





# Left UI elements
ui_frame_left = LabelFrame(
    root, text="Mr Ripper.v0.2.0-beta 1",
    bg=background1, font=("Comic Sans MS",18, "bold"),
    padx=10, pady=10, fg=green)
ui_frame_left.place(x=0, y=2, width=450, height=900)

back_ground_img = Label(image=default_background)
back_ground_img.place(x=447, y=0)

intro_label = Label(
    ui_frame_left, text=intro, width=0, bg=background1,
    fg=cyan, font=("Comic Sans MS", 13, "bold"))
intro_label.place(x=0, y=0)

ripping_status = Label(
    ui_frame_left, text="Please insert a DVD.", width=0,
    bg=background1, fg=green, font=("Comic Sans MS", 15, "bold"))
ripping_status.place(x=0, y=120)

transcoding_status = Label(
    ui_frame_left, text="Waiting for a Movie to transcode.", width=0,
    bg=background1, fg=green, font=("Comic Sans MS", 15, "bold"))
transcoding_status.place(x=0, y=155)

completed_status = Label(
    ui_frame_left, text="Completed Movies:", width=0, bg=background1,
    fg=purple, font=("Comic Sans MS", 15, "bold"))
completed_status.place(x=0, y=345)

completed_status_instructions = Label(
    ui_frame_left, text=instructions1, width=0, bg=background1,
    fg=cyan, font=("Comic Sans MS", 11, "bold"))
completed_status_instructions.place(x=0, y=375)

ripping_listbox = Listbox(ui_frame_left)

transcoding_dir_listbox = Listbox(
    ui_frame_left, bg=background2, fg=orange, width=47,
    height=6, bd=0, font=("Comic Sans MS", 11, "bold"))
transcoding_dir_listbox.place(x=1, y=204)


compressed_dir_listbox = Listbox(
    ui_frame_left, bg=background2, fg=purple, width=47,
    height=18, bd=0, font=("Comic Sans MS", 11, "bold"))
compressed_dir_listbox.place(x=1, y=444)

# Right ui frame
ui_frame_right = LabelFrame(
    root, text="https://github.com/mickdupreez/mr_ripper",
    bg=background1, font=("Comic Sans MS", 16, "bold"),
    padx=10, pady=10, fg=yellow)
ui_frame_right.place(x=1041, y=2, width=450, height=900)

movie_collection_label1 = Label(
    ui_frame_right, text="Movie Collection:", bg=background1,
    fg=green, width=0, font=("Comic Sans MS", 15, "bold"))
movie_collection_label1.place(x=0, y=345)

movie_collection_label2 = Label(
    ui_frame_right, text=instructions2, width=0, bg=background1,
    fg=pink, font=("Comic Sans MS", 11, "bold"))
movie_collection_label2.place(x=0, y=375)

uncompressed_label = Label(
    ui_frame_right, text=que_text1, width=0, bg=background1,
    fg=green, font=("Comic Sans MS", 15, "bold"))
uncompressed_label.place(x=0, y=100)

info_label = Label(
    ui_frame_right, text=info_label, width=0, bg=background1,
    fg=cyan, font=("Comic Sans MS", 15, "bold"))
info_label.place(x=0, y=0)

plex_listbox = Listbox(
    ui_frame_right, bg=background2, fg=green, width=47,
    height=18, bd=0, font=("Comic Sans MS", 11, "bold"))
plex_listbox.place(x=1, y=446)

uncompressed_listbox = Listbox(
    ui_frame_right, bg=background2, fg=orange, width=47,
    height=6, bd=0, font=("Comic Sans MS", 11, "bold"))
uncompressed_listbox.place(x=1, y=204)


def refresh():
    while True:
        time.sleep(1)
        if len(Directories().temp_list) != len(ripping_listbox.get(0, END)):
            ripping_listbox.delete(0, END)
            if Directories().temp_list != []:
                temp = Directories().temp_list
                file_being_ripped = temp[0]
                ripping_status.config(text=f"Ripping: {file_being_ripped}", fg=red)
                try:
                    for file in os.listdir(f"{Directories().temp}{file_being_ripped}"):
                        if file.endswith(".jpg"):
                            poster_jpg = f"{Directories().temp}{file_being_ripped}/{file_being_ripped}.jpg"
                    with Image.open(poster_jpg) as ima:
                        poster_png =f"{Directories().temp}{file_being_ripped}/{file_being_ripped}.png"
                        ima.save(poster_png)
                        poster = PhotoImage(file=poster_png)
                        back_ground_img.config(image=poster)
                except Exception:
                    pass
                for i in Directories().temp_list:
                    ripping_listbox.insert(END, f" {i}")
            if len(Directories().temp_list) == 0:
                    back_ground_img.config(image=default_background)
                    ripping_status.config(text="Please insert a DVD.", fg=green)
                    
        if len(Directories().transcoding_list) != len(transcoding_dir_listbox.get(0, END)):
            transcoding_dir_listbox.delete(0, END)
            transcoding_status.config(text=f"Transcoding Movies: See list below", fg=red)
            for i in Directories().transcoding_list:
                transcoding_dir_listbox.insert(END, f" {i}")
        if len(Directories().transcoding_list) == 0:
            transcoding_status.config(text="Waiting for a Movie to transcode.", fg=green)

        if len(Directories().uncompressed_list) != len(uncompressed_listbox.get(0, END)):
            uncompressed_listbox.delete(0, END)
            for i in Directories().uncompressed_list:
                uncompressed_listbox.insert(END, f" {i}")
            uncompressed_label.configure(text=que_text2, fg=red)
            if len(Directories().uncompressed_list) == 0:
                uncompressed_label.configure(text=que_text1, fg=green)
                
        if len(Directories().compressed_list) != len(compressed_dir_listbox.get(0, END)):
            compressed_dir_listbox.delete(0, END)
            for i in Directories().compressed_list:
                compressed_dir_listbox.insert(END, f" {i}")
        
        if len(Directories().plex_list) != len(plex_listbox.get(0, END)):
            plex_listbox.delete(0, END)
            for i in Directories().plex_list:
                plex_listbox.insert(END, f" {i}")
        time.sleep(1)

threading.Thread(target=refresh).start()
root.mainloop()