import os
import re
import time
import curses
import win32api
import urllib.request
import ctypes
import subprocess
import shutil
import threading
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

class Movie():
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

while True:
    time.sleep(5)
    threading.Thread(target=rip_movie).start()
    threading.Thread(target=transcode_movie).start()