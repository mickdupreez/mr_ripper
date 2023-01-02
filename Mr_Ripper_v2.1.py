import os
import re
import time
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
from selenium.webdriver.common.by import By
from string import ascii_uppercase



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
        """
            This method creates the directories in the directories list if they don't exist
        """
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
        try:
            drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
            for drive in drives:
                if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                    drive_letter = drive
        except Exception as e:
            drive_letter = None
            print(f"An error occurred !!!NO DRIVE DETECTED!!!. Please make sure that you have a DVD drive connected to your PC: {e}")
        try:
            if drive_letter != None:
                volume_info = win32api.GetVolumeInformation(drive_letter)
                volume_info = volume_info[0]
                volume_info = volume_info.replace("_", " ")
                disc_information = MakeMKV(drive_letter).info()
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
            print(f"An unexpected error occurred, using the 'volume_info' as the string to search for. : {e}")
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
                print("An error occurred, you dont have any Title matches. Please try again")
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
                movie_poster = "default.png"
        except Exception as e:
            print(f"An error occurred while downloading the movie data from the web, try again later : {e}")
            movie_title = best_match
            movie_poster = "default.png"
        self.drive_letter = drive_letter
        self.volume_info = volume_info
        self.disc_info = disc_info
        self.best_match = best_match
        self.link = link
        self.title = movie_title
        self.poster = movie_poster
        print('!!!DEBUGGING!!!')
        print('The Movie Class has been successfully initialized')
        print(f"DVD Drive letter : {self.drive_letter}")
        print(f"Name in the volume information : {self.volume_info}")
        print(f"Name in the disc information : {self.disc_info}")
        print(f"Closest match found in the list of available movies : {self.best_match}")
        print(f"Here is the IMDB link fo the Movie : {self.link}")
        print(f"Here is the corrected Movie Title : {self.title}")
        print(f"Here is scraped Movie Poster : {self.poster}")

    def rip_and_transcode(self):
        try:
            if self.title != None:
                output_directory = f"{Directories().temp}{self.title}/"
                os.makedirs(output_directory, exist_ok=True)
                pass
        except Exception as e:
            print(f"There Has been an issue ripping this file, please reinsert the DVD and try again. : {e}")
