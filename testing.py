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
background = PhotoImage(file="default.png")
back_ground = Label(image=background)
back_ground.place(x=447, y=0)


intro = """     Welcome to Mr Ripper's Movie Ripper.
    This Program will Automatically Rip and
    Transcode and Blu-Ray or DVD Movies.
    add it to your media collection.
    
"""
instructions1 = """This list below contains successfully transcoded movies.
Once verified, the file will be moved to your collection."""
instructions2 = """ This is a list of All your Movies. These Movies have
already been organized into directories by Letter for you.
All The Movies are inside of the "plex' directory.
"""

background = PhotoImage(file="default.png")
back_ground = Label(image=background)
back_ground.place(x=447, y=0)


ui_frame1 = LabelFrame(
    root, text="Mr Ripper.v0.2.0-beta 1",
    bg=background1, font=("Comic Sans MS",18, "bold"),
    padx=10, pady=10, fg=green
    )
ui_frame1.place(x=0, y=2, width=450, height=900)

intro_label = Label(
    ui_frame1, text=intro, width=0, bg=background1
    , fg=cyan, font=("Comic Sans MS", 13, "bold")
    )
intro_label.place(x=0, y=0)

ripping_status = Label(
    ui_frame1, text="Please insert a DVD.", width=0, bg=background1,
    fg=green, font=("Comic Sans MS", 15, "bold")
    )
ripping_status.place(x=0, y=120)

transcoding_status = Label(
    ui_frame1, text="Waiting for a Movie to transcode.", width=0, bg=background1,
    fg=green, font=("Comic Sans MS", 15, "bold")
    )
transcoding_status.place(x=0, y=155)
transcoding_dir_listbox = Listbox(ui_frame1, bg=background2, fg=orange, width=47, height=6, bd=0, font=("Comic Sans MS", 11, "bold"))
transcoding_dir_listbox.place(x=1, y=204)

completed_status_ = Label(
    ui_frame1, text="Completed Movies:", width=0, bg=background1,
    fg=purple, font=("Comic Sans MS", 15, "bold")
    )
completed_status_.place(x=0, y=345)

completed_status_instructions = Label(
    ui_frame1, text=instructions1, width=0, bg=background1,
    fg=cyan, font=("Comic Sans MS", 11, "bold")
    )
completed_status_instructions.place(x=0, y=375)

compressed_dir_listbox = Listbox(ui_frame1, bg=background2, fg=purple, width=47, height=18, bd=0, font=("Comic Sans MS", 11, "bold"))
compressed_dir_listbox.place(x=1, y=444)

ui_frame2 = LabelFrame(
    root, text="https://github.com/mickdupreez/mr_ripper", bg=background1,
    font=("Comic Sans MS",16, "bold"), padx=10, pady=10,
    fg=yellow
    )
ui_frame2.place(x=1041, y=2, width=450, height=900)
movie_collection_label1 = Label(ui_frame2, text="Movie Collection:", bg=background1, fg=green, width=0, font=("Comic Sans MS", 15, "bold"))
movie_collection_label1.place(x=0, y=345)
movie_collection_label2 = Label(
    ui_frame2, text=instructions2, width=0, bg=background1,
    fg=cyan, font=("Comic Sans MS", 11, "bold")
    )
movie_collection_label2.place(x=0, y=375)
plex_listbox = Listbox(ui_frame2, bg=background2, fg=green, width=47, height=18, bd=0, font=("Comic Sans MS", 11, "bold"))
plex_listbox.place(x=1, y=444)














def refresh():
    temp = os.listdir(f"{Directories().temp}")
    transcoding = os.listdir(f"{Directories().transcoding}")
    if temp != []:
        file_being_ripped = temp[0]
        for file in os.listdir(f"{Directories().temp}{file_being_ripped}"):
            if file.endswith(".jpg"):
                poster_jpg = f"{Directories().temp}{file_being_ripped}/{file_being_ripped}.jpg"
                with Image.open(poster_jpg) as ima:
                    poster_png =f"{Directories().temp}{file_being_ripped}/{file_being_ripped}.png"
                    ima.save(poster_png)
                    poster = PhotoImage(file=poster_png)
                    back_ground.config(image=poster)
                    ripping_status.config(text=f"Ripping: {file_being_ripped}", fg=red)
    else:
        back_ground.config(image=background)
        ripping_status.config(text="Please insert a DVD.", fg=green)
        
    if len(Directories().transcoding_list) != len(transcoding_dir_listbox.get(0, END)):
        transcoding_dir_listbox.delete(0, END)
        transcoding_status.config(text=f"Transcoding Movies: See list below", fg=red)
        for i in Directories().transcoding_list:
            transcoding_dir_listbox.insert(END, f" {i}")
    else:
        transcoding_status.config(text="Waiting for a Movie to transcode.", fg=green)
        
    if len(Directories().compressed_list) != len(compressed_dir_listbox.get(0, END)):
        compressed_dir_listbox.delete(0, END)
        for i in Directories().compressed_list:
            compressed_dir_listbox.insert(END, f" {i}")
    else:
        pass

refresh()
root.mainloop()