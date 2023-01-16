import os
import re
import time
import curses
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
import logging




logging.basicConfig(
    level=logging.INFO,
    filename="main_log.log",
    filemode="w",
    format = "[(%(levelname)s)(%(asctime)s)(%(funcName)s)] MESSAGE : { %(message)s }", datefmt="%d-%b-%y %H:%M:%S"
    )




DVD_DRIVES = []
MOVIE_TITLES_FILE = "movie_titles.txt"

logging.info(f".............STARTED : PRE-START CHECKS.............")
try:
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
            DVD_DRIVES.append(drive)
    logging.info(f"'PASS' : Here is a list of all the attached DVD Drives'{DVD_DRIVES}.'")
    COMPLETED_DIR = "Completed/" # The directory where the compressed files go.
    COLLECTION_DIR = "Collection/" # The directory where the files go that are ready to be moved uploaded.
    RIPPING_DIR = "Ripping/" # The directory where the file gets ripped to.
    TRANSCODING_DIR = "Transcoding/" # The directory where the files get transcoded.
    QUEUED_DIR = "Queued/" # The directory where the files wait to be transcoded.
    DIRECTORIES = [ # A list of all the directories variables above that is used throughout the program
        COMPLETED_DIR, # The compressed directory
        COLLECTION_DIR, # The plex directory
        RIPPING_DIR, # The temp directory
        TRANSCODING_DIR, # The transcoding directory
        QUEUED_DIR # The uncompressed directory
    ]
    for directory in DIRECTORIES: # For each directory in the directories list
        if os.path.isdir(directory) != True: # If directory does not exist
            logging.warning(f"The Directory '{directory}' did not exist and had to be created.")
            os.mkdir(directory) # Create directory
    logging.info(f"'PASS' : All of the Directories needed exist.")
    for letter in ascii_uppercase: # For each letter in the ascii_uppercase string
        directory = COLLECTION_DIR + letter + '/' # Create the directory path
        if os.path.isdir(directory) != True: # If directory does not exist
            logging.warning(f"The Directory '{directory}' did not exist and had to be created.")
            os.mkdir(directory) # Create directory
    logging.info(f"'PASS' : All of the SUB Directories for your the 'COLLECTION_DIR' exist.")
    COMPLETED_DIR_LIST = os.listdir(COMPLETED_DIR) # A list of items in the compressed directory
    COLLECTION_DIR_LIST = os.listdir(COLLECTION_DIR) # A list of items in the plex directory
    RIPPING_DIR_LIST = os.listdir(RIPPING_DIR) # A list of items in the temp directory
    TRANSCODING_DIR_LIST = os.listdir(TRANSCODING_DIR) # A list of items in the transcoding directory
    QUEUED_DIR_LIST = os.listdir(QUEUED_DIR) # A list of items in the uncompressed directory
    
except Exception as e:
    logging.critical(f"""
                     'FAIL' : An error occurred during the PRE-START CHECKS, here is what we know :
                     DVD drives connected to the system : {DVD_DRIVES}
                     The '{COMPLETED_DIR}' EXISTS
                     The '{COLLECTION_DIR}' EXISTS
                     The '{TRANSCODING_DIR}' EXISTS
                     The '{QUEUED_DIR}' EXISTS
                     The '{RIPPING_DIR}' EXISTS
                     """, exc_info=True)
    
logging.info(f".............FINISHED : PRE-START CHECKS.............")







def rip_dvd(drive_letter):
    logging.info(f"..........................STARTED : SCRAPE ON DRIVE : '{drive_letter}'..........................")
    drive_number = DVD_DRIVES.index(drive_letter)
    DVD_DRIVES.remove(drive_letter)
    logging.info(f"'PASS' : Drive letter '{drive_letter}', has been removed from Available DVD Drives: '{DVD_DRIVES}'. Ready for RIPPING.")
    
    
    
    
    def get_dvd_info():
        try:
            VOLUME_INFO = win32api.GetVolumeInformation(drive_letter[:-1])
            VOLUME_INFO = re.sub(r'[^A-Za-z0-9\s]', '', VOLUME_INFO[0].replace("_", " ")).strip().lower()
            logging.info(f"'PASS' : Used 'win32api.GetVolumeInformation' to get the 'VOLUME_INFO' from the DVD. 'VOLUME_INFO' = '{VOLUME_INFO}'")
        except Exception as e:
            logging.critical(f"""
                             'FAIL' : An error occurred while getting the 'VOLUME_INFO' from the DVD. Here is what we know:
                             Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                             Here is the Error : {e}
                             """, exc_info=True)
        try:
            DISC_INFO = MakeMKV(drive_letter[:-1]).info()
            DISC_INFO = re.sub(r'[^A-Za-z0-9\s]', '', DISC_INFO["disc"]["name"].replace("_", " ")).strip().lower()
            logging.info(f"'PASS' : Used 'MakeMKV.info' to get the 'DISC_INFO' from the DVD. 'DISC_INFO' = '{DISC_INFO}'")
        except Exception as e:
            logging.critical(f"""
                             'FAIL' : An error occurred while getting the 'DISC_INFO' from the DVD. Here is what we know:
                             Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                             Here is the Error : {e}
                             """, exc_info=True)
        try:
            with codecs.open(MOVIE_TITLES_FILE, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                ITEMS = []
                for line in lines:
                    line_items = line.split(',')
                    ITEMS.extend(line_items)
                ITEMS = [re.sub(r'[^A-Za-z0-9\s]', '', item) for item in ITEMS]
                ITEMS = [item.strip().lower() for item in ITEMS]
                ITEMS = ITEMS
            logging.info(f"'PASS' : Used 'codecs.open' to get the 'ITEMS' from the 'MOVIE_TITLES_FILE'.'")
        except Exception as e:
            logging.critical(f"""
                             'FAIL' : An error occurred while getting the 'ITEMS' from the 'MOVIE_TITLES_FILE'. Here is what we know:
                             Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                             This is the file {MOVIE_TITLES_FILE}.
                             Here is the Error : {e}
                             """, exc_info=True)
        return VOLUME_INFO, DISC_INFO, ITEMS

    VOLUME_INFO, DISC_INFO, ITEMS = get_dvd_info()
    
    def get_best_match():
        try:
            VOLUME_INFO_MATCH = difflib.get_close_matches(VOLUME_INFO, ITEMS, n=1, cutoff=0.2)
            VOLUME_INFO_MATCH_PERCENT = difflib.SequenceMatcher(None, VOLUME_INFO, VOLUME_INFO_MATCH[0]).ratio()
            VOLUME_INFO_MATCH = VOLUME_INFO_MATCH[0]
            logging.info(f"'PASS' : Found a match for 'VOLUME_INFO' : '{VOLUME_INFO_MATCH}' with a probability of : '{VOLUME_INFO_MATCH_PERCENT}' out of 1.00")
        except Exception as e:
            logging.critical(f"""
                             'FAIL' : An error occurred while finding a match using 'VOLUME_INFO':. Here is what we know:
                             Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                             This is the file {MOVIE_TITLES_FILE}.
                             Here is the Error : {e}
                             """, exc_info=True)
        try:
            DISC_INFO_MATCH = difflib.get_close_matches(DISC_INFO, ITEMS, n=1, cutoff=0.2)
            DISC_INFO_MATCH_PERCENT = difflib.SequenceMatcher(None, DISC_INFO, DISC_INFO_MATCH[0]).ratio()
            DISC_INFO_MATCH = DISC_INFO_MATCH[0]
            logging.info(f"'PASS' : Found a match for 'DISC_INFO' : '{DISC_INFO_MATCH}' with a probability of : '{DISC_INFO_MATCH_PERCENT}' out of 1.00")
        except Exception as e:
            logging.critical(f"""
                             'FAIL' : An error occurred while finding a match using 'DISC_INFO':. Here is what we know:
                             Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                             This is the file {MOVIE_TITLES_FILE}.
                             Here is the Error : {e}
                             """, exc_info=True)
        try:
            if DISC_INFO_MATCH_PERCENT < 0.40 and VOLUME_INFO_MATCH_PERCENT < 0.40:
                logging.warning(f"'WARNING' : None of the matches have high enough probability using 'VOLUME_INFO' as the best match : {VOLUME_INFO}")
                BEST_MATCH = VOLUME_INFO
            else:
                if DISC_INFO_MATCH_PERCENT == VOLUME_INFO_MATCH_PERCENT:
                    if len(DISC_INFO_MATCH) > len(VOLUME_INFO_MATCH):
                        logging.info(f"'PASS' : The Most likely Movie title for Drive '{drive_letter}{DISC_INFO}' is : '{DISC_INFO_MATCH}'  ")
                        BEST_MATCH = DISC_INFO_MATCH
                    else:
                        logging.info(f"'PASS' : The Most likely Movie title for Drive '{drive_letter}{VOLUME_INFO}' is : '{VOLUME_INFO_MATCH}'  ")
                        BEST_MATCH = VOLUME_INFO_MATCH
                elif DISC_INFO_MATCH_PERCENT < VOLUME_INFO_MATCH_PERCENT:
                    logging.info(f"'PASS' : The Most likely Movie title for Drive '{drive_letter}{VOLUME_INFO}' is : '{VOLUME_INFO_MATCH}'  ")
                    BEST_MATCH = VOLUME_INFO_MATCH
                else:
                    logging.info(f"'PASS' : The Most likely Movie title for Drive '{drive_letter}{DISC_INFO}' is : '{DISC_INFO_MATCH}'  ")
                    BEST_MATCH = DISC_INFO_MATCH
        except Exception as e:
            BEST_MATCH = VOLUME_INFO
            logging.critical(f"""
                             'FAIL' : An error occurred while finding the best match using 'DISC_INFO_MATCH' and 'VOLUME_INFO_MATCH'
                             useing '{VOLUME_INFO}' as the BEST_MATCH:.
                             Here is what we know:
                             Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                             This is the file {MOVIE_TITLES_FILE}.
                             Here is the DISC_INFO and DISC_INFO_MATCH : {DISC_INFO} : {DISC_INFO_MATCH} : {DISC_INFO_MATCH_PERCENT}
                             Here is the DISC_INFO and DISC_INFO_MATCH : {VOLUME_INFO} : {VOLUME_INFO_MATCH} : {VOLUME_INFO_MATCH_PERCENT}
                             Here is the BEST_MATCH : {BEST_MATCH}
                             Here is the Error : {e}
                             """, exc_info=True)
        return BEST_MATCH, VOLUME_INFO_MATCH, VOLUME_INFO_MATCH_PERCENT, DISC_INFO_MATCH, DISC_INFO_MATCH_PERCENT

    BEST_MATCH, VOLUME_INFO_MATCH, VOLUME_INFO_MATCH_PERCENT, DISC_INFO_MATCH, DISC_INFO_MATCH_PERCENT = get_best_match()

    def get_title_and_poster():
        try:
            query = BEST_MATCH.replace(" ", "+")
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
            logging.info(f"'PASS' : We have a IMDB link for the movie'{drive_letter}{DISC_INFO}'-'{BEST_MATCH}' : {link}")

            movie_imdb_link = link
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            options = webdriver.ChromeOptions()
            options.headless = False  # Run the browser in headless mode (without a GUI)
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
            MOVIE_TITLE = (browser.title.replace(") - IMDb", "").replace("(","").replace(":", ""))
            logging.info(f"'PASS' : We have a MOVIE TITLE from IMDB for the DVD'{drive_letter}{DISC_INFO}' : '{MOVIE_TITLE}'")
            OUTPUT_DIRECTORY = f"{RIPPING_DIR}{MOVIE_TITLE}/"
            os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
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
                    MOVIE_POSTER = poster
                    MOVIE_POSTER.save(f"{OUTPUT_DIRECTORY}/{MOVIE_TITLE}.png")
                    logging.info(f"'PASS' : We have a MOVIE POSTER from IMDB for the DVD")
                    os.remove("temp.jpg")
                    browser.quit()
                    logging.info(f"'PASS' : The directory for the movie : '{MOVIE_TITLE}' has been created and the POSTER has been downloaded")
                    logging.info(f"'PASS' : Ready to RIP : '{MOVIE_TITLE}' to the location {OUTPUT_DIRECTORY}")

        except Exception as e:
            MOVIE_TITLE = BEST_MATCH
            MOVIE_POSTER = Im.open("default.png")
            DVD_DRIVES.append(drive_letter)
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
            logging.critical(f"""
                     'FAIL' : An error occurred while scrapeing the web for the IMDB TITLE and POSTER.
                     The BEST_MATCH and the default.png will be used as the filename and poster.
                     Here is what we know:
                     Here is the drive letter that was used : {drive_letter}. Number : {drive_number}
                     This is the file {MOVIE_TITLES_FILE}.
                     Here is the DISC_INFO and DISC_INFO_MATCH : {DISC_INFO} : {DISC_INFO_MATCH} : {DISC_INFO_MATCH_PERCENT}
                     Here is the DISC_INFO and DISC_INFO_MATCH : {VOLUME_INFO} : {VOLUME_INFO_MATCH} : {VOLUME_INFO_MATCH_PERCENT}
                     Here is the BEST_MATCH : {BEST_MATCH}
                     Here is the link : {link}
                     Here is the MOVIE_TITLE : {MOVIE_TITLE}
                     Here is the MOVIE_POSTER : {MOVIE_POSTER}
                     Here is the output directory : {OUTPUT_DIRECTORY}
                     The DVD has been ejected, and the drive_letter has been added back into the list : {DVD_DRIVES}
                     Here is the Error : {e}
                     """, exc_info=True)
        
        return MOVIE_TITLE, MOVIE_POSTER, OUTPUT_DIRECTORY
    
    MOVIE_TITLE, MOVIE_POSTER, OUTPUT_DIRECTORY  = get_title_and_poster()
    
    def rip_DVD():
        logging.info(f"'PASS' : Beginning DVD Rip : '{MOVIE_TITLE}.mkv' to the location {OUTPUT_DIRECTORY}")
        makemkv = MakeMKV(drive_number)
        makemkv.mkv(drive_number, OUTPUT_DIRECTORY)
        logging.info(f"'PASS' : DVD HAS FINISHED RIPPING : '{MOVIE_TITLE}.mkv' to the location {OUTPUT_DIRECTORY}")
        for file in os.listdir(f"{RIPPING_DIR}{MOVIE_TITLE}"):
            if file.endswith(".mkv"):
                uncompressed_file = file
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
                if drive_letter not in DVD_DRIVES:
                    DVD_DRIVES.append(drive_letter)
                shutil.move(f"{RIPPING_DIR}{MOVIE_TITLE}", QUEUED_DIR)
                logging.info(f"'PASS' : The movie directory has been moved to the QUEUED directory : {QUEUED_DIR_LIST}")

rip_dvd(DVD_DRIVES[0])










