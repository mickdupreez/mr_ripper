import os
import re
import time
import curses
import emoji
import ctypes
import shutil
import codecs
import difflib
import win32api
import requests
import win32file
import threading
import subprocess
import urllib.request
from bs4 import BeautifulSoup
from tkinter import *
from PIL import Image as Im
from PIL import Image
from makemkv import MakeMKV
from googlesearch import search
from selenium import webdriver
from curses import wrapper
from curses.textpad import Textbox, rectangle
from selenium.webdriver.common.by import By
from string import ascii_uppercase
from colorit import init_colorit, background



dvd_drives = []
collection = []
try:
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
            dvd_drives.append(drive)
except Exception as e:
    print(f"An error occurred !!!NO DRIVE DETECTED!!!. Please make sure that you have a DVD drive connected to your PC: {e}")

class Directories:

    def __init__(self):
        self.compressed = "compressed/" # The directory where the compressed files go.
        self.plex = "plex/" # The directory where the files go that are ready to be moved uploaded.
        self.temp = "temp/" # The directory where the file gets ripped to.
        self.transcoding = "transcoding/" # The directory where the files get transcoded.
        self.uncompressed = "uncompressed/" # The directory where the files wait to be transcoded.
        self.directories = [ # A list of all the directories variables above that is used throughout the program
            self.compressed, # The compressed directory
            self.plex, # The plex directory
            self.temp, # The temp directory
            self.transcoding, # The transcoding directory
            self.uncompressed # The uncompressed directory
        ]
        self.create_directories() # Call the create_directories method
        self.compressed_list = os.listdir(self.compressed) # A list of items in the compressed directory
        self.plex_list = os.listdir(self.plex) # A list of items in the plex directory
        self.temp_list = os.listdir(self.temp) # A list of items in the temp directory
        self.transcoding_list = os.listdir(self.transcoding) # A list of items in the transcoding directory
        self.uncompressed_list = os.listdir(self.uncompressed) # A list of items in the uncompressed directory

    def create_directories(self):
        for directory in self.directories: # For each directory in the directories list
            if os.path.isdir(directory) != True: # If directory does not exist
                os.mkdir(directory) # Create directory
            else: # Skip if directory exists
                pass
        for letter in ascii_uppercase: # For each letter in the ascii_uppercase string
            directory = self.plex + letter + '/' # Create the directory path
            if os.path.isdir(directory) != True: # If directory does not exist
                os.mkdir(directory) # Create directory
            else: # Skip if directory exists
                pass








def terminal_ui(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    RED = curses.color_pair(1)
    GREEN = curses.color_pair(2)
    YELLOW = curses.color_pair(3)
    BLUE = curses.color_pair(4)
    MAGENTA = curses.color_pair(5)
    CYAN = curses.color_pair(6)
    WHITE = curses.color_pair(7)
    BLACK = curses.color_pair(8)

    def main_box():
        stdscr.addstr(1, 1, "Mr Ripper 2.1.1 https://github.com/mickdupreez/mr_ripper|", BLUE | curses.A_BOLD)
        if Directories().temp_list == [] and Directories().transcoding_list != []:
            stdscr.addstr(1, 65, "!!! TRANSCODING IN PROGRES PLEASE WAIT !!!", RED | curses.A_BOLD)
        if Directories().temp_list != [] and Directories().transcoding_list == []:
            stdscr.addstr(1, 68, "!!! RIPPING IN PROGRES PLEASE WAIT !!!", RED | curses.A_BOLD)
        if Directories().temp_list != [] and Directories().transcoding_list != []:
            stdscr.addstr(1, 62, "!!! RIP AND TRANSCODE IN PROGRESS PLEASE WAIT !!!", RED | curses.A_BOLD)
        if Directories().temp_list == [] and Directories().transcoding_list == []:
            stdscr.addstr(1, 65, "!!! INSERT A DVD OR BLURAY TO GET STARTED !!!", GREEN | curses.A_BOLD)
        rectangle(stdscr, 0, 0, 28, 115)
    
    def get_directory_size(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        if total_size < 1024:
            return f"{total_size} B"
        elif total_size < 1024**2:
            return f"{total_size/1024:.2f} KB"
        elif total_size < 1024**3:
            return f"{total_size/1024**2:.2f} MB"
        else:
            return f"{total_size/1024**3:.2f} GB"

    def get_storage_size(file_path):
        total, used, free = shutil.disk_usage(os.path.dirname(os.path.abspath(file_path)))
        total = total // (1024 ** 3)
        total = f"{total} GB"
        used = used // (1024 ** 3)
        used = f"{used} GB"
        free = free // (1024 ** 3)
        free = f"{free} GB"
        return total, used, free

    def stats_box():
        total, used, free, = get_storage_size('README.md')
        stdscr.addstr(19, 12, "- Directory Sizes and stats -", BLUE | curses.A_BOLD)
        stdscr.addstr(20, 2, f"Free space on Drive:      {free} out of {total}", GREEN | curses.A_BOLD)
        stdscr.addstr(21, 2, f"Drive space used:         {get_directory_size('.')} out of {total}", GREEN | curses.A_BOLD)
        stdscr.addstr(22, 2, f"Ripping Directory:        {get_directory_size(Directories().temp)} out of {get_directory_size('.')}", GREEN | curses.A_BOLD)
        stdscr.addstr(23, 2, f"Uncompressed Directory:   {get_directory_size(Directories().uncompressed)} out of {get_directory_size('.')}", GREEN | curses.A_BOLD)
        stdscr.addstr(24, 2, f"Transcoding Directory:    {get_directory_size(Directories().transcoding)} out of {get_directory_size('.')}", GREEN | curses.A_BOLD)
        stdscr.addstr(25, 2, f"Compressed Directory:     {get_directory_size(Directories().compressed)} out of {get_directory_size('.')}", GREEN | curses.A_BOLD)
        stdscr.addstr(26, 2, f"Plex Directory:           {get_directory_size(Directories().plex)} out of {get_directory_size('.')}", GREEN | curses.A_BOLD)
        rectangle(stdscr, 18, 1, 27, 56)

    
    def temp_box():
        stdscr.addstr(3, 14, "- Movies That Are Being Ripped -", MAGENTA | curses.A_BOLD)
        stdscr.addstr(4, 27, get_directory_size('temp'), GREEN | curses.A_BOLD)
        rectangle(stdscr, 5, 1, 9, 56)
        rectangle(stdscr, 2, 1, 9, 56)
        row = 5
        col = 2
        for i in Directories().temp_list:
            word = i
            row = row + 1
            stdscr.addstr(row, col, word, RED | curses.A_BOLD)
            
    def transcoding_box():
        stdscr.addstr(11, 14, "- Movies That Are Transcoding -", YELLOW | curses.A_BOLD)
        stdscr.addstr(12, 27, get_directory_size(Directories().transcoding), GREEN | curses.A_BOLD)
        rectangle(stdscr, 13, 1, 17, 56)
        rectangle(stdscr, 10, 1, 17, 56)
        row = 13
        col = 2
        for i in Directories().transcoding_list:
            word = i
            row = row + 1
            stdscr.addstr(row, col, word, RED | curses.A_BOLD)

    def uncompressed_box():
        stdscr.addstr(3, 65, "- Movies That Are Queued For Transcoding -", CYAN | curses.A_BOLD)
        stdscr.addstr(4, 83, get_directory_size(Directories().uncompressed), GREEN | curses.A_BOLD)
        rectangle(stdscr, 5, 57, 27, 114)
        rectangle(stdscr, 2, 57, 27, 114)
        row = 5
        col = 58
        for i in Directories().uncompressed_list:
            time.sleep(.1)
            word = i
            row = row + 1
            stdscr.addstr(row, col, word, RED | curses.A_BOLD)

    count = 0
    while True:
        time.sleep(0.6)
        RED = curses.color_pair(1)
        stdscr.clear()
        count = count + 1
        if count % 2 == 0:
            RED = BLACK

        main_box()
        temp_box()
        transcoding_box()
        stats_box()
        uncompressed_box()
        stdscr.refresh()

def show_terminal():
    curses.wrapper(terminal_ui)

threading.Thread(target=show_terminal).start()















class Movie:
    def __init__(self):
        drive_letter = dvd_drives[0]
        drive_number = dvd_drives.index(drive_letter)
        self.drive_letter = drive_letter
        self.drive_number = drive_number
        dvd_drives.remove(drive_letter)

    def Scrape(self):
        try:
            if self.drive_letter != None:
                volume_info = win32api.GetVolumeInformation(self.drive_letter[:-1])
                volume_info = volume_info[0]
                volume_info = volume_info.replace("_", " ")
                disc_information = MakeMKV(self.drive_letter[:-1]).info()
                disc_info = disc_information["disc"]["name"]
                disc_info = disc_info.replace("_", " ")
                try:
                    volume_info = re.sub(r'(?<!\b\d{4})(?<!\b\d)\b\d+\b(?!\d\b)', '', volume_info)
                    volume_info = re.sub(r'[^A-Za-z0-9\s]', '', volume_info).strip().lower()
                    disc_info = re.sub(r'(?<!\b\d{4})(?<!\b\d)\b\d+\b(?!\d\b)', '', disc_info)
                    disc_info = re.sub(r'[^A-Za-z0-9\s]', '', disc_info).strip().lower()
                except Exception as e:
                    print(f"An error occurred while preprocessing the string :{volume_info} or {disc_info}:: {e}")
            else:
                volume_info = None
                disc_info = None
                print("ERROR, The 'drive_letter' is None. Please connect a DVD Drive to your PC.")
        except Exception as e:
            volume_info = None
            disc_info = None
            print(f"An error has occurred, Cant gather volume information: {e}")
        try:
            possible_title = "movie_titles.txt"
            with codecs.open(possible_title, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                items = []
                for line in lines:
                    line_items = line.split(',')
                    items.extend(line_items)
                items = [re.sub(r'[^A-Za-z0-9\s]', '', item) for item in items]
                items = [item.strip() for item in items]
                items = items
        except Exception as e:
            items = None
            print(f"An error occurred while reading the {possible_title} file: {e}")
        try:
            volume_info_match = None
            volume_info_percent_max = 0
            for item in items:
                volume_info_percent = difflib.SequenceMatcher(None, volume_info, item).ratio()
                if volume_info_percent > volume_info_percent_max:
                    volume_info_percent_max = volume_info_percent
                    volume_info_match = item
            disc_info_match = None
            disc_info_percent_max = 0
            for item in items:
                disc_info_percent = difflib.SequenceMatcher(None, disc_info, item).ratio()
                if disc_info_percent > disc_info_percent_max:
                    disc_info_percent_max = volume_info_percent
                    disc_info_match = item                
            if disc_info_percent_max < 0.55 and volume_info_percent_max < 0.55:
                print("There are no matches, using the 'volume_info' as the string to search for.")
                time.sleep(3)
                best_match = volume_info
            else:
                if disc_info_percent_max > volume_info_percent_max:
                    print("best_match = disc_info_percent_max")
                    best_match = disc_info_match
                else:
                    print("best_match = volume_info_percent_max")
                    best_match = volume_info_match
        except Exception as e:
            print(f"An unexpected error occurred, using the 'volume_info' as the string to search for. Please try again later : {e}")
            best_match = volume_info
        try:
            if best_match != None:
                query = best_match.replace(" ", "+")
                url = f"https://www.google.com/search?q={query}+site:imdb.com"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
                }
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")
                links = []
                for a in soup.find_all("a", href=True):
                    if a["href"].startswith("https://www.imdb.com/title/tt") and re.match(r"\d+/$", a["href"][-6:]):
                        links.append(a["href"])
                        link = links[:1]
                        link = link[0]
            else:
                print("An error occurred, you dont have any Title matches. Please try later.")
                link = None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            link = None
        try:
            if link != None:
                movie_imdb_link = link
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                options = webdriver.ChromeOptions()
                options.headless = True  # Run the browser in headless mode (without a GUI)
                options.add_argument("--silent")  # Suppress logging
                options.add_argument(f'user-agent={user_agent}')  # Set the user agent
                options.add_argument("--window-size=1920,1080")  # Set the window size
                options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
                options.add_argument('--allow-running-insecure-content')  # Allow running insecure content
                options.add_argument("--disable-extensions")  # Disable extensions
                options.add_argument("--proxy-server='direct://'")  # Set the proxy server
                options.add_argument("--proxy-bypass-list=*")  # Set the proxy bypass list
                options.add_argument("--start-maximized")  # Start the browser maximized
                options.add_argument('--disable-gpu')  # Disable GPU acceleration
                options.add_argument('--disable-dev-shm-usage')  # Disable shared memory
                options.add_argument('--no-sandbox')  # Disable the sandbox
                browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
                browser.get(movie_imdb_link)
                movie_title = (browser.title.replace(") - IMDb", "").replace("(","").replace(":", ""))
                browser.find_element(By.CLASS_NAME, "ipc-lockup-overlay__screen").click()
                pattern = re.compile(r'<img src="https://m\.media-amazon\.com/images/.+"')
                matches = pattern.findall(browser.page_source)
                matches = str(matches[0]).split(",")
                matches = matches[0].split('"')
                for match in matches:
                    if match.startswith("https") and match.endswith("jpg"):
                        poster_link = match
                        urllib.request.urlretrieve(poster_link, "temp.jpg")
                        poster = Im.open("temp.jpg")
                        poster_hight = 900
                        hight_percent = (poster_hight / float(poster.size[1]))
                        poster_width = int((float(poster.size[0]) * float(hight_percent)))
                        poster = poster.resize((poster_width, poster_hight), Im.Resampling.LANCZOS)
                        movie_poster = poster
                        os.remove("temp.jpg")
                        browser.quit()
            else:
                print(f"An error occurred while getting the link, try again later")
                movie_title = best_match
                
                movie_poster = Im.open("default.png")
        except Exception as e:
            print(f"An error occurred while downloading the movie data from the web, try again later : {e}")
            movie_title = best_match
            movie_poster = Im.open("default.png")
        try:
            if movie_title != None:
                output_directory = f"{Directories().temp}{movie_title}/"
                os.makedirs(output_directory, exist_ok=True)
                if movie_poster == None:
                    movie_poster = Im.open("default.png")
                    movie_poster.save(f"{output_directory}/{movie_title}.png")
                else:
                    movie_poster.save(f"{output_directory}/{movie_title}.png")
            else:
                print("An error occurred while creating the output directory for this DVD, please try again.")
                drives.append(self.drive_letter)
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
                
        except Exception as e:
            print("An error occurred while creating the output directory for this DVD, please try again.")
            shutil.rmtree(f"{Directories().temp}{movie_title}")

        self.volume_info = volume_info
        self.disc_info = disc_info
        self.best_match = best_match
        self.link = link
        self.title = movie_title
        self.poster = movie_poster
        self.output_directory = output_directory

    def Rip(self):
        try:
            makemkv = MakeMKV(self.drive_number)
            makemkv.mkv(self.drive_number, self.output_directory)
        except:
            print("An error occurred while ripping this DVD, please try again.")
            uncompressed_file = None
            drives.append(self.drive_letter)
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
        try:
            for file in os.listdir(f"{Directories().temp}{self.title}"):
                if file.endswith(".mkv"):
                    uncompressed_file = file
                    print(f"Here is the output directory : {uncompressed_file}")
                    drives.append(self.drive_letter)
                    self.uncompressed_file = uncompressed_file
                    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
        except Exception as e:
            print("An error occurred while looking for the ripped file, please try again.")
            uncompressed_file = None

def rip_movie():
    if dvd_drives != []:
        print(dvd_drives)
        time.sleep(1)
        DVDDRIVE = Movie()
        DVDDRIVE.Scrape()
        DVDDRIVE.Rip()
        TITLE = DVDDRIVE.title
        POSTER = DVDDRIVE.poster
        OUTPUTDIR = DVDDRIVE.output_directory
        return DVDDRIVE, TITLE, POSTER, OUTPUTDIR
    else:
        time.sleep(10)

def transcode_movie():
    if Directories().uncompressed_list != []:
        def transcode():
            for dir in Directories().transcoding_list:
                target_dir = dir
                print(target_dir)
                for file in os.listdir(f"{Directories().transcoding}{target_dir}"):
                    print(file)
                    if file.endswith(".mkv"):
                        input_file = file
                        output_file = f"{Directories().transcoding}{target_dir}/{target_dir}.mkv"
                        command  = [
                            "HandBrakeCLI.exe", "--preset-import-file", "profile.json", "-Z", "PLEX",
                            "-i", input_file, "-o",
                            output_file
                        ]
                        print(input_file, output_file)
                        subprocess.run(command, shell=True)
                        time.sleep(3)
                        os.remove(f"{Directories().transcoding}{target_dir}/{input_file}")
                        time.sleep(1)
                        shutil.move(f"{Directories().transcoding}{target_dir}", f"{Directories().compressed}")
                        time.sleep(1)
        title = Directories().uncompressed_list[0]
        dir_location = f"{Directories().uncompressed}{title}"
        output_directory_size = sum(os.path.getsize(os.path.join(dir_location, f)) for f in os.listdir(dir_location))
        output_directory_size_gb = output_directory_size / (1024 ** 3)
        if output_directory_size_gb < 20:
            dir_destination =  f"{Directories().transcoding}"
            if len(Directories().transcoding_list) <= 1:
                shutil.move(dir_location, dir_destination)
                threading.Thread(target=transcode).start()
            else:
                pass
        else:
            dir_destination = f"{Directories().compressed}"
            for file in os.listdir(f"{Directories().uncompressed}{title}"):
                if file.endswith('.mkv'):
                    os.rename(f"{Directories().uncompressed}{title}/{file}", f"{Directories().uncompressed}{title}/{title}.mkv")
                    shutil.move(dir_location, dir_destination)
    else:
        time.sleep(5)
def rip_and_transcode():
    time.sleep(5)
    threading.Thread(target=rip_movie).start()
    threading.Thread(target=transcode_movie).start()











root = Tk()
root.title("https://github.com/mickdupreez/mr_ripper")
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
default_background = PhotoImage(file="default.png")

instructions1 = """This list below contains successfully transcoded movies.
Once verified, the file will be moved to your collection."""
instructions2 = """ This is a list of All your Movies. These Movies have
already been organized into directories by Letter for you.
All The Movies are inside of the "plex' directory."""
info_label = """This program is in beta, there are still
some bugs that need to ironed out.
Check out the github for Documentation"""

back_ground_img = Label(image=default_background)
back_ground_img.place(x=447, y=0)


def left_frame_ui():
    ui_frame_left = LabelFrame(
        root, 
        text="Ripping And Transcoding",  # Title for the label frame
        bg=background1,  # Background color
        font=("Comic Sans MS",18, "bold"),  # Font and size for the title
        padx=10, pady=10,  # Padding for the label frame
        fg=green  # Color of the title text
    )
    intro = "Welcome to Mr Ripper's Movie Ripper.\n"
    intro2 = "This Program will Automatically Rip and Transcode \n"
    intro3 = "your Blu-Ray or DVD Movies and add them \n"
    intro4 = "to your Movie collection.\n"
    intro5 = "\nPlease wait for all the boxes below to be empty\n"
    intro6 = "before you quit the program,"

    
    intro_label = Label(
        ui_frame_left, 
        text=intro+intro2+intro3+intro4+intro5+intro6,  # Text for the label
        width=0,  # Width of the label
        bg=background1,  # Background color of the label
        fg=cyan,  # Color of the text
        font=("Comic Sans MS", 13, "bold")  # Font and size of the text
    )
    intro_label.place(x=0, y=0)
    ui_frame_left.place(x=0, y=2, width=450, height=900)

    def ripping_ui():
        ripping_status1 = Label(
            ui_frame_left,
            text="Nothing is Ripping:",
            bg=background1,
            fg=green,
            font=("Comic Sans MS", 15, "bold")
        )
        ripping_label = "!READY! Insert a Disc or Discs for Ripping.\nYou can Rip up to 3 movies at the same time."
        ripping_label1 = "!Please Hold Tight! Movie Ripping in progress.\nPlease wait until this list is empty before quitting!"
        ripping_status2 = Label(
        ui_frame_left, 
        text=ripping_label,  # Text for the label
        bg=background1,  # Background color of the label
        fg=purple,  # Color of the text
        font=("Comic Sans MS", 13, "bold")  # Font and size of the text
    )
        ripping_listbox = Listbox(
            ui_frame_left,
            bg=background2,
            fg=orange,
            width=47,
            height=3,
            bd=0,
            font=("Comic Sans MS", 11, "bold")
            )
        ripping_status1.place(x=0, y=204)
        ripping_status2.place(x=0, y=235)
        ripping_listbox.place(x=1, y=295)
        
        def refresh():
            while True:
                if len(Directories().temp_list) != len(ripping_listbox.get(0, END)):
                    ripping_listbox.delete(0, END)
                    if Directories().temp_list != []:
                        temp = Directories().temp_list
                        file_being_ripped = temp[0]
                        ripping_status2.config(text=ripping_label1, fg=orange)
                        ripping_status1.config(text="Something is Ripping:", fg=red)
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
                            ripping_status2.config(text=ripping_label, fg=purple)
                            ripping_status1.config(text="Nothing is Ripping", fg=green)
                time.sleep(5)
        threading.Thread(target=refresh).start()
    
    ripping_ui()
    
    def uncompressed_ui():
        
        uncompressed_label1 = Label(
        ui_frame_left,
        text="Nothing in Que:",  # Text displayed on the label
        width=0,  # Width of the label
        bg=background1,  # Background color of the label
        fg=green,  # Color of the text on the label
        font=("Comic Sans MS", 15, "bold")  # Font and size of the text on the label
        )
        uncompressed_text1 = "!READY! Que is empty Waiting for Ripped Movies.\nThere is no limit on the number of Queued Movies."
        uncompressed_text2 = "!Please Hold Tight! There are Movies in the Que.\nPlease wait until this list is empty before quitting!"
        uncompressed_label2 = Label(
        ui_frame_left,
        text=uncompressed_text1,  # Text displayed on the label
        width=0,  # Width of the label
        bg=background1,  # Background color of the label
        fg=purple,  # Color of the text on the label
        font=("Comic Sans MS", 13, "bold")  # Font and size of the text on the label
        )
        uncompressed_listbox = Listbox(
            ui_frame_left,
            bg=background2,  # Background color of the listbox
            fg=orange,  # Color of the text in the listbox
            width=47,  # Width of the listbox
            height=10,  # Height of the listbox
            bd=0,  # Border size of the listbox
            font=("Comic Sans MS", 11, "bold")  # Font and size of the text in the listbox
            )
        
        uncompressed_label1.place(x=0, y=365)
        uncompressed_label2.place(x=0, y=396)
        uncompressed_listbox.place(x=1, y=456)
        
        
        def refresh():
            while True:
                if len(Directories().uncompressed_list) != len(uncompressed_listbox.get(0, END)):
                    uncompressed_listbox.delete(0, END)
                    for i in Directories().uncompressed_list:
                        uncompressed_listbox.insert(END, f" {i}")
                    uncompressed_label1.configure(text="Something in Que:", fg=red)
                    uncompressed_label2.configure(text=uncompressed_text2, fg=orange)
                    if len(Directories().uncompressed_list) == 0:
                        uncompressed_label1.configure(text="Nothing in Que:", fg=green)
                        uncompressed_label2.configure(text=uncompressed_text1, fg=purple)
                time.sleep(5)
        threading.Thread(target=refresh).start()

    uncompressed_ui()

    def transcoding_ui():
        transcoding_label1 = "!READY! Waiting for a movie to transcode\nYou can Transcode upto 3 movies at the same time."
        transcoding_label2 = "!Please Hold Tight! Transcoding in progress.\nPlease wait until this list is empty before quitting!"
        transcoding_status1 = Label(
            ui_frame_left, 
            text="Nothing is Transcoding:",  # Text for the label
            width=0,  # Width of the label
            bg=background1,  # Background color of the label
            fg=green,  # Color of the text
            font=("Comic Sans MS", 15, "bold")  # Font and size of the text
        )
        transcoding_status2 = Label(
            ui_frame_left, 
            text=transcoding_label1,  # Text for the label
            width=0,  # Width of the label
            bg=background1,  # Background color of the label
            fg=purple,  # Color of the text
            font=("Comic Sans MS", 13, "bold")  # Font and size of the text
        )
        transcoding_dir_listbox = Listbox(
            ui_frame_left, 
            bg=background2,  # Background color of the listbox
            fg=orange,  # Color of the text in the listbox
            width=47,  # Width of the listbox
            height=3,  # Height of the listbox
            bd=0,  # Border size of the listbox
            font=("Comic Sans MS", 11, "bold")  # Font and size of the text in the listbox
        )
        
        transcoding_status1.place(x=0, y=679) # + 31
        transcoding_status2.place(x=0, y=710) # + 60
        transcoding_dir_listbox.place(x=0, y=770)
        
        def refresh():
            while True:
                if len(Directories().transcoding_list) != len(transcoding_dir_listbox.get(0, END)):
                    transcoding_dir_listbox.delete(0, END)
                    transcoding_status2.config(text=transcoding_label2, fg=orange)
                    transcoding_status1.config(text="Something is Transcoding:", fg=red)
                    for i in Directories().transcoding_list:
                        transcoding_dir_listbox.insert(END, f" {i}")
                    if len(Directories().transcoding_list) == 0:
                        transcoding_status2.config(text=transcoding_label1, fg=purple)
                        transcoding_status1.config(text="Nothing is Transcoding:", fg=green)
                time.sleep(5)
        threading.Thread(target=refresh).start()

    transcoding_ui()
left_frame_ui()

def right_frame_ui():
    
    ui_frame_right = LabelFrame(
        root, 
        text="Compressed Movies and your Collection",  # Text displayed on the label frame
        bg=background1,  # Background color of the label frame
        font=("Comic Sans MS", 16, "bold"),  # Font and size of the text on the label frame
        padx=10, pady=10,  # Padding around the text on the label frame
        fg=green  # Color of the text on the label frame
    )
    ui_frame_right.place(x=1041, y=2, width=450, height=900)


    def compressed_ui():
        completed_status = Label(
            ui_frame_right, 
            text="Completed Movies:",  # Text for the label
            width=0,  # Width of the label
            bg=background1,  # Background color of the label
            fg=purple,  # Color of the text
            font=("Comic Sans MS", 15, "bold")  # Font and size of the text
        )
        completed_status_instructions = Label(
            ui_frame_right, 
            text=instructions1,  # Text for the label
            width=0,  # Width of the label
            bg=background1,  # Background color of the label
            fg=cyan,  # Color of the text
            font=("Comic Sans MS", 11, "bold")  # Font and size of the text
        )
        compressed_dir_listbox = Listbox(
            ui_frame_right, 
            bg=background2,  # Background color of the listbox
            fg=purple,  # Color of the text in the listbox
            width=47,  # Width of the listbox
            height=10,  # Height of the listbox
            bd=0,  # Border size of the listbox
            font=("Comic Sans MS", 11, "bold")  # Font and size of the text in the listbox
        )
        
        
        completed_status.place(x=0, y=0)
        completed_status_instructions.place(x=0, y=31)
        compressed_dir_listbox.place(x=1, y=91)

        def refresh():
            while True:
                if len(Directories().compressed_list) != len(compressed_dir_listbox.get(0, END)):
                    compressed_dir_listbox.delete(0, END)
                    for i in Directories().compressed_list:
                        compressed_dir_listbox.insert(END, f" {i}")
                time.sleep(5)
        threading.Thread(target=refresh).start()
        

    def plex_ui():
        plex_label1 = Label(
            ui_frame_right, 
            text="Movie Collection:",  # Text displayed on the label
            bg=background1,  # Background color of the label
            fg=green,  # Color of the text on the label
            width=0,  # Width of the label
            font=("Comic Sans MS", 15, "bold")  # Font and size of the text on the label
        )
        plex_label2 = Label(
            ui_frame_right, 
            text=instructions2,  # Text displayed on the label
            width=0,  # Width of the label
            bg=background1,  # Background color of the label
            fg=pink,  # Color of the text on the label
            font=("Comic Sans MS", 11, "bold")  # Font and size of the text on the label
        )
        plex_listbox = Listbox(
            ui_frame_right,
            bg=background2,  # Background color of the listbox
            fg=green,  # Color of the text in the listbox
            width=47,  # Width of the listbox
            height=18,  # Height of the listbox
            bd=0,  # Border size of the listbox
            font=("Comic Sans MS", 11, "bold")  # Font and size of the text in the listbox
            )

        plex_label1.place(x=0, y=345)
        plex_label2.place(x=0, y=375)
        plex_listbox.place(x=1, y=446)
        
        
        for letter in os.listdir(Directories().plex):
            for movie in os.listdir(f"{Directories().plex}/{letter}"):
                if movie not in collection:
                    collection.append(movie)
        
        
        if len(collection) != len(plex_listbox.get(0, END)):
            plex_listbox.delete(0, END)
            for letter in os.listdir(Directories().plex):
                for movie in os.listdir(f"{Directories().plex}/{letter}"):
                    if movie not in plex_listbox.get(0, END):
                        plex_listbox.insert(END, f" {movie}")
    
    
    compressed_ui()
    plex_ui()
right_frame_ui()

threading.Thread(target=rip_movie).start()
threading.Thread(target=transcode_movie).start()
root.mainloop()