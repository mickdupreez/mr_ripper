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
from selenium.webdriver.chrome.service import Service
from string import ascii_uppercase
import logging


def main():

    # Set up logging configuration
    logging.basicConfig(
        # Set the logging level to INFO, which will log messages of level INFO and above
        level=logging.INFO,
        # Specify the name and location of the log file
        filename="main_log.log",
        # Specify the file mode, "w" means to overwrite the file if it already exists
        filemode="w",
        # Specify the format of the log messages
        format="[(%(levelname)s)(%(funcName)s)] { %(message)s }(%(asctime)s)",
        # Specify the format of the timestamp in the log messages
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.info(
        f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!START!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
    )
    logging.info(
        f"'PRE-START CHECKS' : '!!STARTED!!': Checking That All the Directories are inplace and that there is a DVD drive connected to the PC."
    )
    # File containing the movie titles
    MOVIE_TITLES_FILE = "movie_titles.txt"
    # Directory containing completed movies
    COMPLETED_DIR = "Completed/"
    # Directory containing movies in the collection
    COLLECTION_DIR = "Collection/"
    # Directory containing movies currently being ripped
    RIPPING_DIR = "Ripping/"
    # Directory containing movies currently being transcoded
    TRANSCODING_DIR = "Transcoding/"
    # Directory containing queued movies
    QUEUED_DIR = "Queued/"
    # List of all the directories
    DIRECTORIES = [
        COMPLETED_DIR,
        COLLECTION_DIR,
        RIPPING_DIR,
        TRANSCODING_DIR,
        QUEUED_DIR,
    ]
    for directory in DIRECTORIES:
        if os.path.isdir(directory) != True:
            logging.warning(
                f"'PRE-START CHECKS' : '!!WARNING!!' The Directory'{directory}' did not exist and had to be created."
            )
            os.mkdir(directory)
    logging.info(
        f"'PRE-START CHECKS' : '!!PASS!!' All of these Directories have been created {DIRECTORIES}."
    )
    for letter in ascii_uppercase:
        directory = COLLECTION_DIR + letter + "/"
        if os.path.isdir(directory) != True:
            logging.warning(
                f"'PRE-START CHECKS' : '!!WARNING!!' The Directory '{directory}' did not exist and had to be created."
            )
            os.mkdir(directory)
    logging.info(
        f"'PRE-START CHECKS' : '!!PASS!!' All of the Directories A-Z have been created inside of the 'COLLECTION_DIR'."
    )
    COLLECTION = []
    DVD_DRIVES = []
    try:
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split("\000")[:-1]
        for drive in drives:
            if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                DVD_DRIVES.append(drive)
                logging.info(
                    f"'PRE-START CHECKS' : '!!PASS!!': Here is a list of all the connected DVD drives {DVD_DRIVES}."
                )
    except Exception as e:
        DVD_DRIVES = []
    logging.info(
        f"'PRE-START CHECKS' : '!!FINISHED!!': All of the 'PRE-START CHECKS' have finished. Ready to RIP."
    )
    logging.info(
        f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!FINISH!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
    )

    def rip_and_scrape_dvd(drive_letter):
        logging.info(
            f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!START!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
        )
        logging.info(
            f"'RIP AND SCRAPE' : '!!STARTED!!': Starting DVD info scrape and RIP to an output Directory."
        )
        drive_number = DVD_DRIVES.index(drive_letter)
        DVD_DRIVES.remove(drive_letter)
        logging.info(
            f"'RIP AND SCRAPE' : '!!PASS!!': The drive letter : '{drive_letter}' has been removed from the 'DVD_DRIVES' list : {DVD_DRIVES}."
        )
        try:
            VOLUME_INFO = win32api.GetVolumeInformation(drive_letter[:-1])
            VOLUME_INFO = (
                re.sub(r"[^A-Za-z0-9\s]", "", VOLUME_INFO[0].replace("_", " "))
                .strip()
                .lower()
            )
            logging.info(
                f"'RIP AND SCRAPE' : '!!PASS!!': Used 'win32api.GetVolumeInformation' to get the 'VOLUME_INFO' : '{VOLUME_INFO}'."
            )
        except Exception as e:
            VOLUME_INFO = None
            logging.info(
                f"'RIP AND SCRAPE' : '!!FAILED!!': Due to an 'ERRROR'.'win32api.GetVolumeInformation' Could not be used to get the 'VOLUME_INFO'. ERROR: {e}"
            )
        try:
            DISC_INFO = MakeMKV(drive_letter[:-1]).info()
            DISC_INFO = (
                re.sub(
                    r"[^A-Za-z0-9\s]", "", DISC_INFO["disc"]["name"].replace("_", " ")
                )
                .strip()
                .lower()
            )
            logging.info(
                f"'RIP AND SCRAPE' : '!!PASS!!': Used 'MakeMKV.info' to get the 'DISC_INFO' : '{DISC_INFO}'."
            )
        except Exception as e:
            DISC_INFO = None
            logging.info(
                f"'RIP AND SCRAPE' : '!!FAILED!!': Due to an 'ERRROR'.'MakeMKV.info' Could not be used to get the 'DISC_INFO' ERROR: {e}."
            )
        try:
            with codecs.open(MOVIE_TITLES_FILE, "r", encoding="utf-8") as file:
                lines = file.readlines()
                ITEMS = []
                for line in lines:
                    line_items = line.split(",")
                    ITEMS.extend(line_items)
                ITEMS = [re.sub(r"[^A-Za-z0-9\s]", "", item) for item in ITEMS]
                ITEMS = [item.strip().lower() for item in ITEMS]
                ITEMS = ITEMS
            logging.info(
                f"'RIP AND SCRAPE' : '!!PASS!!': Used 'codecs.open' to make a list of all the known movie names."
            )
        except Exception as e:
            ITEMS = []
            logging.info(
                f"'RIP AND SCRAPE' : '!!FAILED!!': Due to an 'ERRROR'.'codecs.open' Could not open or read the file '{MOVIE_TITLES_FILE}'. ERROR: {e}."
            )
        if DISC_INFO == None and VOLUME_INFO != None:
            logging.warning(
                f"'RIP AND SCRAPE' : '!!WARNING!!': Using 'VOLUME_INFO' as 'DISC_INFO' because 'DISC_INFO' is equal to : '{DISC_INFO}."
            )
            DISC_INFO = VOLUME_INFO
        if VOLUME_INFO == None and DISC_INFO != None:
            logging.warning(
                f"'RIP AND SCRAPE' : '!!WARNING!!': Using 'DISC_INFO' as 'VOLUME_INFO' because 'VOLUME_INFO' is equal to : '{VOLUME_INFO}."
            )
            VOLUME_INFO = DISC_INFO

        if ITEMS != [] and VOLUME_INFO and DISC_INFO != None:
            logging.info(
                f"'RIP AND SCRAPE' : '!!PASS!!': We have a 'VOLUME_INFO' : '{VOLUME_INFO}', 'DISC_INFO' : '{DISC_INFO}', and a list of Movies 'ITEMS'."
            )
            try:
                VOLUME_INFO_MATCH = difflib.get_close_matches(
                    VOLUME_INFO, ITEMS, n=1, cutoff=0.2
                )
                VOLUME_INFO_MATCH_PERCENT = difflib.SequenceMatcher(
                    None, VOLUME_INFO, VOLUME_INFO_MATCH[0]
                ).ratio()
                VOLUME_INFO_MATCH = VOLUME_INFO_MATCH[0]
                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': Used 'difflib.SequenceMatcher and difflib.get_close_matches' to get the Accuracy of the match for 'VOLUME_INFO': '{VOLUME_INFO_MATCH}': Accuracy '{VOLUME_INFO_MATCH_PERCENT}' out of '1.0'."
                )
            except Exception as e:
                VOLUME_INFO_MATCH = VOLUME_INFO
                VOLUME_INFO_MATCH_PERCENT = 0.0
                logging.warning(
                    f"'RIP AND SCRAPE' : '!!WARNING!!': Due to an ERROR while looking for a match with 'VOLUME_INFO', this step will be skipped. {e}"
                )
            try:
                DISC_INFO_MATCH = difflib.get_close_matches(
                    DISC_INFO, ITEMS, n=1, cutoff=0.2
                )
                DISC_INFO_MATCH_PERCENT = difflib.SequenceMatcher(
                    None, DISC_INFO, DISC_INFO_MATCH[0]
                ).ratio()
                DISC_INFO_MATCH = DISC_INFO_MATCH[0]
                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': Used 'difflib.SequenceMatcher and difflib.get_close_matches' to get the Accuracy of the match for 'DISC_INFO': '{DISC_INFO_MATCH}': Accuracy '{DISC_INFO_MATCH_PERCENT}' out of '1.0'."
                )
            except Exception as e:
                DISC_INFO_MATCH = DISC_INFO
                DISC_INFO_MATCH_PERCENT = 0.0
                logging.warning(
                    f"'RIP AND SCRAPE' : '!!WARNING!!': Due to an ERROR while looking for a match with 'DISC_INFO', this step will be skipped. {e}"
                )
            try:
                if DISC_INFO_MATCH_PERCENT < 0.40 and VOLUME_INFO_MATCH_PERCENT < 0.40:
                    logging.warning(
                        f"'RIP AND SCRAPE' : '!!WARNING!!': None of the matches were higher that 0.4. Using 'VOLUME_INFO' as the 'BEST_MATCH' : '{BEST_MATCH}'."
                    )
                    BEST_MATCH = VOLUME_INFO
                else:
                    if DISC_INFO_MATCH_PERCENT == VOLUME_INFO_MATCH_PERCENT:
                        if len(DISC_INFO_MATCH) > len(VOLUME_INFO_MATCH):
                            BEST_MATCH = DISC_INFO_MATCH
                            logging.info(
                                f"'RIP AND SCRAPE' : '!!PASS!!': Between 'VOLUME_INFO' and 'DISC_INFO' the 'BEST_MATCH' was 'DISC_INFO': '{BEST_MATCH}'."
                            )
                        else:
                            BEST_MATCH = VOLUME_INFO_MATCH
                            logging.info(
                                f"'RIP AND SCRAPE' : '!!PASS!!': Between 'VOLUME_INFO' and 'DISC_INFO' the 'BEST_MATCH' was 'VOLUME_INFO': '{BEST_MATCH}'."
                            )
                    elif DISC_INFO_MATCH_PERCENT < VOLUME_INFO_MATCH_PERCENT:
                        BEST_MATCH = VOLUME_INFO_MATCH
                        logging.info(
                            f"'RIP AND SCRAPE' : '!!PASS!!': Between 'VOLUME_INFO' and 'DISC_INFO' the 'BEST_MATCH' was 'VOLUME_INFO': '{BEST_MATCH}'."
                        )
                    else:
                        BEST_MATCH = DISC_INFO_MATCH
                        logging.info(
                            f"'RIP AND SCRAPE' : '!!PASS!!': Between 'VOLUME_INFO' and 'DISC_INFO' the 'BEST_MATCH' was 'DISC_INFO': '{BEST_MATCH}'."
                        )
            except Exception as e:
                BEST_MATCH = VOLUME_INFO
                logging.warning(
                    f"'RIP AND SCRAPE' : '!!WARNING!!': An ERROR has occurred while looking for a movie title match, using 'VOLUME_INFO' as the 'BEST_MATCH': '{BEST_MATCH}'."
                )
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
                    if a["href"].startswith(
                        "https://www.imdb.com/title/tt"
                    ) and re.match(r"\d+/$", a["href"][-6:]):
                        links.append(a["href"])
                        link = links[:1]
                        link = link[0]
                movie_imdb_link = link
                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': Used 'BeautifulSoup and Google Search' to get a IMDB link using the 'BEST_MATCH': '{BEST_MATCH}' as the TITLE. The Link {movie_imdb_link}."
                )
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                options = webdriver.ChromeOptions()
                options.add_argument("--silent")
                options.add_argument("--headless")
                options.add_argument("--log-level=3")
                options.add_argument(f"user-agent={user_agent}")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--ignore-certificate-errors")
                options.add_argument("--allow-running-insecure-content")
                options.add_argument("--disable-extensions")
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")
                options.add_argument("--start-maximized")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                service = Service("chromedriver.exe")
                service.start()
                browser = webdriver.Remote(service.service_url, options=options)
                browser.get(movie_imdb_link)
                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': Used 'webdriver.Remote and chromedriver.exe' to open a Google Chrome browser tab in the background for scraping the 'MOVIE_TITLE' and 'MOVIE_POSTER'."
                )
                MOVIE_TITLE = (
                    browser.title.replace(") - IMDb", "")
                    .replace("(", "")
                    .replace(":", "")
                )
                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': The 'MOVIE_TITLE' has been scraped from IMDB : '{MOVIE_TITLE}'."
                )
                OUTPUT_DIRECTORY = f"{RIPPING_DIR}{MOVIE_TITLE}/"
                os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': An 'OUTPUT_DIRECTORY' for the movie :'{MOVIE_TITLE}' has been created :'{OUTPUT_DIRECTORY}'."
                )
                browser.find_element(
                    By.CLASS_NAME, "ipc-lockup-overlay__screen"
                ).click()
                pattern = re.compile(
                    r'<img src="https://m\.media-amazon\.com/images/.+"'
                )
                matches = pattern.findall(browser.page_source)
                matches = str(matches[0]).split(",")
                matches = matches[0].split('"')
                for match in matches:
                    if match.startswith("https") and match.endswith("jpg"):
                        poster_link = match
                        urllib.request.urlretrieve(poster_link, "temp.jpg")
                        poster = Im.open("temp.jpg")
                        poster_hight = 900
                        hight_percent = poster_hight / float(poster.size[1])
                        poster_width = int(
                            (float(poster.size[0]) * float(hight_percent))
                        )
                        poster = poster.resize(
                            (poster_width, poster_hight), Im.Resampling.LANCZOS
                        )
                        MOVIE_POSTER = poster
                        MOVIE_POSTER.save(f"{OUTPUT_DIRECTORY}/{MOVIE_TITLE}.png")
                        logging.info(
                            f"'RIP AND SCRAPE' : '!!PASS!!': The 'MOVIE_POSTER' has been scraped from IMDB for the movie :'{MOVIE_TITLE}' and saved to the 'OUTPUT_DIRECTORY'."
                        )
                        os.remove("temp.jpg")
                        browser.quit()
                        service.stop()
                        logging.info(
                            f"'RIP AND SCRAPE' : '!!PASS!!': Scrapping completed, closing browser."
                        )
            except Exception as e:
                service.stop()
                MOVIE_TITLE = BEST_MATCH
                MOVIE_POSTER = Im.open("default.png")
                OUTPUT_DIRECTORY = f"{RIPPING_DIR}{MOVIE_TITLE}/"
                logging.warning(
                    f"'RIP AND SCRAPE' : '!!WARNING!!': An ERROR has occurred while Scraping for the 'MOVIE_TITLE' and 'MOVIE_POSTER'."
                )
                logging.warning(
                    f"'RIP AND SCRAPE' : '!!WARNING!!': The 'BEST_MATCH':'{BEST_MATCH}' will be used as the 'MOVIE_TITLE' and a default Poster will be used as the 'MOVIE_POSTER'."
                )
            try:
                makemkv = MakeMKV(drive_number)

                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': Used MakeMKV to initialize the target DVD. Beginning RIP on 'Drive Number ': '{drive_number} {drive_letter}': '{MOVIE_TITLE}' to the 'OUTPUT_DIRECTORY' : '{OUTPUT_DIRECTORY}'."
                )
                makemkv.mkv(drive_number, OUTPUT_DIRECTORY)
                time.sleep(5)
                for file in os.listdir(f"{RIPPING_DIR}{MOVIE_TITLE}"):
                    if file.endswith(".mkv"):
                        shutil.move(f"{RIPPING_DIR}{MOVIE_TITLE}", QUEUED_DIR)

                logging.info(
                    f"'RIP AND SCRAPE' : '!!PASS!!': The DVD has finished RIPPING and has been moved to the 'QUEUED_DIR' for processing."
                )
                if drive_letter not in DVD_DRIVES:
                    ctypes.windll.WINMM.mciSendStringW(
                        "set cdaudio door open", None, 0, None
                    )
                    DVD_DRIVES.append(drive_letter)
                    logging.info(
                        f"'RIP AND SCRAPE' : '!!PASS!!': The 'Drive letter' has been added back the the 'DVD_DRIVES' list : {DVD_DRIVES} and the 'DVD DRIVE' has been Opened."
                    )
                    time.sleep(5)

            except Exception as e:
                ctypes.windll.WINMM.mciSendStringW(
                    "set cdaudio door open", None, 0, None
                )
                DVD_DRIVES.append(drive_letter)
                logging.critical(
                    f"'RIP AND SCRAPE' : '!!critical!!': The 'Drive letter' has been added back the the 'DVD_DRIVES' list : {DVD_DRIVES} and the 'DVD DRIVE' has been Opened."
                )
            logging.info(
                f"'RIP AND SCRAPE' : '!!FINISHED!!': 'RIP' and 'SCRAPE' has completed successfully"
            )
            time.sleep(5)
        else:
            ctypes.windll.WINMM.mciSendStringW("set cdaudio door open", None, 0, None)
            DVD_DRIVES.append(drive_letter)
            logging.critical(
                f"'RIP AND SCRAPE' : '!!CRITICAL!!': DVD cant be ripped Due to insufficient information about the DVD ejecting Drive '{drive_number}' : '{drive_letter}'."
            )
            logging.warning(
                f"'RIP AND SCRAPE' : '!!WARNING!!': Please insert a DVD or Blu-ray Disc. : returning the 'drive_letter' : '{drive_letter}' to the 'DVD_DRIVES' list : {DVD_DRIVES}."
            )
            time.sleep(5)
        logging.info(
            f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!FINISH!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
        )
        time.sleep(5)

    def transcode_movie():

        if os.listdir(QUEUED_DIR) != []:
            logging.info(
                f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!START!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
            )
            logging.info(
                f"'TRANSCODE MOVIE' : '!!STARTED!!': Starting to Transcode any movie that is larger than '20GB'."
            )

            def transcode():
                print(os.listdir(QUEUED_DIR))
                print(os.listdir(QUEUED_DIR))
                print(os.listdir(QUEUED_DIR))
                for dir in os.listdir(TRANSCODING_DIR):
                    target_dir = dir
                    logging.info(
                        f"'TRANSCODE MOVIE' : '!!PASS!!': The Movie Directory : '{target_dir}'."
                    )
                    for file in os.listdir(f"{TRANSCODING_DIR}{target_dir}"):
                        if file.endswith(".mkv"):
                            input_file = f"{TRANSCODING_DIR}{target_dir}/{file}"
                            output_file = (
                                f"{TRANSCODING_DIR}{target_dir}/{target_dir}.mkv"
                            )
                            command = [
                                "HandBrakeCLI.exe",
                                "--preset-import-file",
                                "profile.json",
                                "-Z",
                                "PLEX",
                                "-i",
                                input_file,
                                "-o",
                                output_file,
                            ]
                            logging.info(
                                f"'TRANSCODE MOVIE' : '!!PASS!!': The Input file : '{input_file}' and the Output file : '{output_file}'."
                            )
                            subprocess.run(command, shell=True)
                            logging.info(
                                f"'TRANSCODE MOVIE' : '!!PASS!!': The Input file : '{input_file}' is now Transcoding."
                            )
                            time.sleep(3)
                            os.remove(f"{input_file}")
                            logging.info(
                                f"'TRANSCODE MOVIE' : '!!PASS!!': The Input file : '{input_file}' Has finished transcoding : {output_file}."
                            )
                            time.sleep(1)
                            shutil.move(
                                f"{TRANSCODING_DIR}{target_dir}",
                                f"{COMPLETED_DIR}",
                            )
                            logging.info(
                                f"'TRANSCODE MOVIE' : '!!PASS!!': Moved '{TRANSCODING_DIR}{target_dir}' to '{COMPLETED_DIR}'"
                            )
                            time.sleep(1)
                logging.info(
                    f"'TRANSCODE MOVIE' : '!!FINISHED!!': Transcoding of the file : {output_file} has completed."
                )
                logging.info(
                    f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!FINISHED!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
                )

            print(os.listdir(QUEUED_DIR))
            title = os.listdir(QUEUED_DIR)[0]
            print("title: " + title)
            dir_location = f"{QUEUED_DIR}{title}"
            if title != None:
                output_directory_size = sum(
                    os.path.getsize(os.path.join(dir_location, f))
                    for f in os.listdir(dir_location)
                )
                output_directory_size_gb = output_directory_size / (1024**3)
                logging.info(
                    f"'TRANSCODE MOVIE' : '!!PASS!!': The Movie : '{title}' has a file size of : '{output_directory_size_gb}'."
                )

                ################################# SWAP THE <> back !!!!
                if output_directory_size_gb > 20:
                    dir_destination = f"{TRANSCODING_DIR}"
                    if len(os.listdir(TRANSCODING_DIR)) <= 2:
                        print(dir_location)
                        print(dir_location)
                        print(dir_location)
                        print(
                            "################################################################"
                        )
                        print(dir_destination)
                        print(dir_destination)
                        print(dir_destination)
                        shutil.move(dir_location, dir_destination)
                        TRANSCODE_THREAD = threading.Thread(target=transcode)
                        TRANSCODE_THREAD.daemon = True
                        TRANSCODE_THREAD.start()
                    logging.info(
                        f"""'TRANSCODE MOVIE' : '!!PASS!!': The Movie : '{title}:{output_directory_size_gb}' has been moved to the 'Transcoding Directory' and has begun the Transcode process."""
                    )
                else:
                    dir_destination = f"{COMPLETED_DIR}"
                    for file in os.listdir(f"{QUEUED_DIR}{title}"):
                        if file.endswith(".mkv"):
                            os.rename(
                                f"{QUEUED_DIR}{title}/{file}",
                                f"{QUEUED_DIR}{title}/{title}.mkv",
                            )
                            shutil.move(dir_location, dir_destination)
                    logging.info(
                        f"'TRANSCODE MOVIE' : '!!FINISHED!!': The Movie : '{title}:{output_directory_size_gb}' has been moved to the 'Completed Directory' because it does not need to be transcoded."
                    )
                    logging.info(
                        f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!FINISHED!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
                    )
                    time.sleep(5)
        else:
            time.sleep(5)

    def rip_scrape_loop():
        while True:
            time.sleep(2)
            if DVD_DRIVES != []:
                logging.info(
                    f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!START!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
                )
                rip_and_scrape_dvd(DVD_DRIVES[0])
                RIP_AND_SCRAPE_THREAD = threading.Thread(
                    target=rip_and_scrape_dvd, args=(DVD_DRIVES[0])
                )
                RIP_AND_SCRAPE_THREAD.daemon = True
                RIP_AND_SCRAPE_THREAD.start()
                time.sleep(3)
            else:
                time.sleep(8)

    def transcode_loop():
        while True:
            time.sleep(2)
            if os.listdir(QUEUED_DIR) != []:
                logging.info(
                    f"'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!START!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'"
                )
                TRANSCODE_MOVIE_THREAD = threading.Thread(target=transcode_movie)
                TRANSCODE_MOVIE_THREAD.daemon = True
                TRANSCODE_MOVIE_THREAD.start()
                time.sleep(3)
            else:
                time.sleep(8)

    def term_ui():
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
                stdscr.addstr(
                    1,
                    1,
                    "Mr Ripper 2.2.0 https://github.com/mickdupreez/mr_ripper|",
                    BLUE | curses.A_BOLD,
                )
                if os.listdir(RIPPING_DIR) == [] and os.listdir(TRANSCODING_DIR) != []:
                    stdscr.addstr(
                        1,
                        65,
                        "!!! TRANSCODING IN PROGRES PLEASE WAIT !!!",
                        RED | curses.A_BOLD,
                    )
                if os.listdir(RIPPING_DIR) != [] and os.listdir(TRANSCODING_DIR) == []:
                    stdscr.addstr(
                        1,
                        68,
                        "!!! RIPPING IN PROGRES PLEASE WAIT !!!",
                        RED | curses.A_BOLD,
                    )
                if os.listdir(RIPPING_DIR) != [] and os.listdir(TRANSCODING_DIR) != []:
                    stdscr.addstr(
                        1,
                        62,
                        "!!! RIP AND TRANSCODE IN PROGRESS PLEASE WAIT !!!",
                        RED | curses.A_BOLD,
                    )
                if os.listdir(RIPPING_DIR) == [] and os.listdir(TRANSCODING_DIR) == []:
                    stdscr.addstr(
                        1,
                        65,
                        "!!! INSERT A DVD OR BLURAY TO GET STARTED !!!",
                        GREEN | curses.A_BOLD,
                    )
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
                total, used, free = shutil.disk_usage(
                    os.path.dirname(os.path.abspath(file_path))
                )
                total = total // (1024**3)
                total = f"{total} GB"
                used = used // (1024**3)
                used = f"{used} GB"
                free = free // (1024**3)
                free = f"{free} GB"
                return total, used, free

            def stats_box():
                (
                    total,
                    used,
                    free,
                ) = get_storage_size("README.md")
                stdscr.addstr(
                    19, 12, "- Directory Sizes and stats -", BLUE | curses.A_BOLD
                )
                stdscr.addstr(
                    20,
                    2,
                    f"Free space on Drive:      {free} out of {total}",
                    GREEN | curses.A_BOLD,
                )
                stdscr.addstr(
                    21,
                    2,
                    f"Drive space used:         {get_directory_size('.')} out of {total}",
                    GREEN | curses.A_BOLD,
                )
                stdscr.addstr(
                    22,
                    2,
                    f"Ripping Directory:        {get_directory_size(RIPPING_DIR)} out of {get_directory_size('.')}",
                    GREEN | curses.A_BOLD,
                )
                stdscr.addstr(
                    23,
                    2,
                    f"Uncompressed Directory:   {get_directory_size(QUEUED_DIR)} out of {get_directory_size('.')}",
                    GREEN | curses.A_BOLD,
                )
                stdscr.addstr(
                    24,
                    2,
                    f"Transcoding Directory:    {get_directory_size(TRANSCODING_DIR)} out of {get_directory_size('.')}",
                    GREEN | curses.A_BOLD,
                )
                stdscr.addstr(
                    25,
                    2,
                    f"Compressed Directory:     {get_directory_size(COMPLETED_DIR)} out of {get_directory_size('.')}",
                    GREEN | curses.A_BOLD,
                )
                stdscr.addstr(
                    26,
                    2,
                    f"Plex Directory:           {get_directory_size(COLLECTION_DIR)} out of {get_directory_size('.')}",
                    GREEN | curses.A_BOLD,
                )
                rectangle(stdscr, 18, 1, 27, 56)

            def temp_box():
                stdscr.addstr(
                    3, 14, "- Movies That Are Being Ripped -", MAGENTA | curses.A_BOLD
                )
                stdscr.addstr(
                    4, 27, get_directory_size(RIPPING_DIR), GREEN | curses.A_BOLD
                )
                rectangle(stdscr, 5, 1, 9, 56)
                rectangle(stdscr, 2, 1, 9, 56)
                row = 5
                col = 2
                for i in os.listdir(RIPPING_DIR):
                    word = i
                    row = row + 1
                    stdscr.addstr(row, col, word, RED | curses.A_BOLD)

            def transcoding_box():
                stdscr.addstr(
                    11, 14, "- Movies That Are Transcoding -", YELLOW | curses.A_BOLD
                )
                stdscr.addstr(
                    12, 27, get_directory_size(TRANSCODING_DIR), GREEN | curses.A_BOLD
                )
                rectangle(stdscr, 13, 1, 17, 56)
                rectangle(stdscr, 10, 1, 17, 56)
                row = 13
                col = 2
                for i in os.listdir(TRANSCODING_DIR):
                    word = i
                    row = row + 1
                    stdscr.addstr(row, col, word, RED | curses.A_BOLD)

            def uncompressed_box():
                stdscr.addstr(
                    3,
                    65,
                    "- Movies That Are Queued For Transcoding -",
                    CYAN | curses.A_BOLD,
                )
                stdscr.addstr(
                    4,
                    83,
                    get_directory_size(QUEUED_DIR),
                    GREEN | curses.A_BOLD,
                )
                rectangle(stdscr, 5, 57, 27, 114)
                rectangle(stdscr, 2, 57, 27, 114)
                row = 5
                col = 58
                for i in os.listdir(QUEUED_DIR):
                    time.sleep(0.1)
                    word = i
                    row = row + 1
                    stdscr.addstr(row, col, word, RED | curses.A_BOLD)

            count = 0
            while True:
                time.sleep(0.3)
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

        curses.wrapper(terminal_ui)

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
    Once verified, file will be moved to your collection."""
    instructions2 = """This is a list of All your Movies. These Movies have
    already been organized into directories by Letter.
    All The Movies are inside of the "plex' directory."""

    def poster_art():
        back_ground_img = Label(image=default_background)
        back_ground_img.place(x=447, y=0)

        def refresh():
            while True:
                if len(os.listdir(RIPPING_DIR)) != 0:

                    for dir in os.listdir(RIPPING_DIR):
                        for file in os.listdir(f"{RIPPING_DIR}{dir}"):
                            if file.endswith(".png"):

                                poster = Im.open(f"{RIPPING_DIR}{dir}/{file}")
                                poster = poster.resize((592, 900))
                                os.remove(f"{RIPPING_DIR}{dir}/{file}")
                                poster.save(f"{RIPPING_DIR}{dir}/{dir}.png")
                                BG_POSTER = PhotoImage(
                                    file=(f"{RIPPING_DIR}{dir}/{dir}.png")
                                )
                        if BG_POSTER == PhotoImage(
                            file=(f"{RIPPING_DIR}{dir}/{dir}.png")
                        ):
                            pass
                        else:
                            back_ground_img = Label(image=BG_POSTER)
                            back_ground_img.place(x=447, y=0)
                            time.sleep(5)
                else:
                    back_ground_img = Label(image=default_background)
                    back_ground_img.place(x=447, y=0)
                    time.sleep(5)

        poster_art_thread = threading.Thread(target=refresh)
        poster_art_thread.daemon = True
        poster_art_thread.start()

    def left_frame_ui():
        ui_frame_left = LabelFrame(
            root,
            text="Ripping And Transcoding",  # Title for the label frame
            bg=background1,  # Background color
            font=("Comic Sans MS", 18, "bold"),  # Font and size for the title
            padx=10,
            pady=10,  # Padding for the label frame
            fg=green,  # Color of the title text
        )
        intro = "Welcome to Mr Ripper's Movie Ripper.\n"
        intro2 = "This Program will Automatically Rip and Transcode \n"
        intro3 = "your Blu-Ray or DVD Movies and add them \n"
        intro4 = "to your Movie collection.\n"
        intro5 = "\nPlease wait for all the boxes below to be empty\n"
        intro6 = "before you quit the program,"
        intro_label = Label(
            ui_frame_left,
            text=intro
            + intro2
            + intro3
            + intro4
            + intro5
            + intro6,  # Text for the label
            width=0,  # Width of the label
            bg=background1,  # Background color of the label
            fg=cyan,  # Color of the text
            font=("Comic Sans MS", 13, "bold"),  # Font and size of the text
        )
        intro_label.place(x=0, y=0)
        ui_frame_left.place(x=0, y=2, width=450, height=900)

        def ripping_ui():
            ripping_status1 = Label(
                ui_frame_left,
                text="Nothing is Ripping:",
                bg=background1,
                fg=green,
                font=("Comic Sans MS", 15, "bold"),
            )
            ripping_label = "!READY! Insert a Disc or Discs for Ripping.\nYou can Rip up to 3 movies at the same time."
            ripping_label1 = "!Please Hold Tight! Movie Ripping in progress.\nPlease wait until this list is empty before quitting!"
            ripping_status2 = Label(
                ui_frame_left,
                text=ripping_label,  # Text for the label
                bg=background1,  # Background color of the label
                fg=purple,  # Color of the text
                font=("Comic Sans MS", 13, "bold"),  # Font and size of the text
            )
            ripping_listbox = Listbox(
                ui_frame_left,
                bg=background2,
                fg=orange,
                width=47,
                height=3,
                bd=0,
                font=("Comic Sans MS", 11, "bold"),
            )
            ripping_status1.place(x=0, y=204)
            ripping_status2.place(x=0, y=235)
            ripping_listbox.place(x=1, y=295)

            def refresh():
                while True:
                    if len(os.listdir(RIPPING_DIR)) != len(ripping_listbox.get(0, END)):
                        ripping_listbox.delete(0, END)
                        if os.listdir(RIPPING_DIR) != []:
                            ripping_status2.config(text=ripping_label1, fg=orange)
                            ripping_status1.config(text="Something is Ripping:", fg=red)
                            for i in os.listdir(RIPPING_DIR):
                                ripping_listbox.insert(END, f" {i}")
                        if len(os.listdir(RIPPING_DIR)) == 0:
                            ripping_status2.config(text=ripping_label, fg=purple)
                            ripping_status1.config(text="Nothing is Ripping", fg=green)
                    time.sleep(5)

            T4 = threading.Thread(target=refresh)
            T4.daemon = True
            T4.start()

        ripping_ui()

        def uncompressed_ui():
            uncompressed_label1 = Label(
                ui_frame_left,
                text="Nothing in Que:",  # Text displayed on the label
                width=0,  # Width of the label
                bg=background1,  # Background color of the label
                fg=green,  # Color of the text on the label
                font=(
                    "Comic Sans MS",
                    15,
                    "bold",
                ),  # Font and size of the text on the label
            )
            uncompressed_text1 = "!READY! Que is empty Waiting for Ripped Movies.\nThere is no limit on the number of Queued Movies."
            uncompressed_text2 = "!Please Hold Tight! There are Movies in the Que.\nPlease wait until this list is empty before quitting!"
            uncompressed_label2 = Label(
                ui_frame_left,
                text=uncompressed_text1,  # Text displayed on the label
                width=0,  # Width of the label
                bg=background1,  # Background color of the label
                fg=purple,  # Color of the text on the label
                font=(
                    "Comic Sans MS",
                    13,
                    "bold",
                ),  # Font and size of the text on the label
            )
            uncompressed_listbox = Listbox(
                ui_frame_left,
                bg=background2,  # Background color of the listbox
                fg=orange,  # Color of the text in the listbox
                width=47,  # Width of the listbox
                height=10,  # Height of the listbox
                bd=0,  # Border size of the listbox
                font=(
                    "Comic Sans MS",
                    11,
                    "bold",
                ),  # Font and size of the text in the listbox
            )
            uncompressed_label1.place(x=0, y=365)
            uncompressed_label2.place(x=0, y=396)
            uncompressed_listbox.place(x=1, y=456)

            def refresh():
                while True:
                    if len(os.listdir(QUEUED_DIR)) != len(
                        uncompressed_listbox.get(0, END)
                    ):
                        uncompressed_listbox.delete(0, END)
                        for i in os.listdir(QUEUED_DIR):
                            uncompressed_listbox.insert(END, f" {i}")
                        uncompressed_label1.configure(text="Something in Que:", fg=red)
                        uncompressed_label2.configure(
                            text=uncompressed_text2, fg=orange
                        )
                        if len(os.listdir(QUEUED_DIR)) == 0:
                            uncompressed_label1.configure(
                                text="Nothing in Que:", fg=green
                            )
                            uncompressed_label2.configure(
                                text=uncompressed_text1, fg=purple
                            )
                    time.sleep(5)

            T5 = threading.Thread(target=refresh)
            T5.daemon = True
            T5.start()

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
                font=("Comic Sans MS", 15, "bold"),  # Font and size of the text
            )
            transcoding_status2 = Label(
                ui_frame_left,
                text=transcoding_label1,  # Text for the label
                width=0,  # Width of the label
                bg=background1,  # Background color of the label
                fg=purple,  # Color of the text
                font=("Comic Sans MS", 13, "bold"),  # Font and size of the text
            )
            transcoding_dir_listbox = Listbox(
                ui_frame_left,
                bg=background2,  # Background color of the listbox
                fg=orange,  # Color of the text in the listbox
                width=47,  # Width of the listbox
                height=3,  # Height of the listbox
                bd=0,  # Border size of the listbox
                font=(
                    "Comic Sans MS",
                    11,
                    "bold",
                ),  # Font and size of the text in the listbox
            )
            transcoding_status1.place(x=0, y=679)  # + 31
            transcoding_status2.place(x=0, y=710)  # + 60
            transcoding_dir_listbox.place(x=0, y=770)

            def refresh():
                while True:
                    if len(os.listdir(TRANSCODING_DIR)) != len(
                        transcoding_dir_listbox.get(0, END)
                    ):
                        transcoding_dir_listbox.delete(0, END)
                        transcoding_status2.config(text=transcoding_label2, fg=orange)
                        transcoding_status1.config(
                            text="Something is Transcoding:", fg=red
                        )
                        for i in os.listdir(TRANSCODING_DIR):
                            transcoding_dir_listbox.insert(END, f" {i}")
                        if len(os.listdir(TRANSCODING_DIR)) == 0:
                            transcoding_status2.config(
                                text=transcoding_label1, fg=purple
                            )
                            transcoding_status1.config(
                                text="Nothing is Transcoding:", fg=green
                            )
                    time.sleep(5)

            T6 = threading.Thread(target=refresh)
            T6.daemon = True
            T6.start()

        transcoding_ui()

    def right_frame_ui():
        ui_frame_right = LabelFrame(
            root,
            text="Compressed Movies and your Collection",  # Text displayed on the label frame
            bg=background1,  # Background color of the label frame
            font=(
                "Comic Sans MS",
                16,
                "bold",
            ),  # Font and size of the text on the label frame
            padx=10,
            pady=10,  # Padding around the text on the label frame
            fg=green,  # Color of the text on the label frame
        )
        ui_frame_right.place(x=1041, y=2, width=450, height=900)

        def compressed_ui():
            completed_status = Label(
                ui_frame_right,
                text="Completed Movies:",  # Text for the label
                width=0,  # Width of the label
                bg=background1,  # Background color of the label
                fg=purple,  # Color of the text
                font=("Comic Sans MS", 15, "bold"),  # Font and size of the text
            )
            completed_status_instructions = Label(
                ui_frame_right,
                text=instructions1,  # Text for the label
                width=0,  # Width of the label
                bg=background1,  # Background color of the label
                fg=cyan,  # Color of the text
                font=("Comic Sans MS", 11, "bold"),  # Font and size of the text
            )
            compressed_dir_listbox = Listbox(
                ui_frame_right,
                bg=background2,  # Background color of the listbox
                fg=purple,  # Color of the text in the listbox
                width=47,  # Width of the listbox
                height=10,  # Height of the listbox
                bd=0,  # Border size of the listbox
                font=(
                    "Comic Sans MS",
                    11,
                    "bold",
                ),  # Font and size of the text in the listbox
            )
            completed_status.place(x=0, y=0)
            completed_status_instructions.place(x=0, y=31)
            compressed_dir_listbox.place(x=1, y=91)

            def refresh():
                while True:
                    if len(os.listdir(COMPLETED_DIR)) != len(
                        compressed_dir_listbox.get(0, END)
                    ):
                        compressed_dir_listbox.delete(0, END)
                        for i in os.listdir(COMPLETED_DIR):
                            compressed_dir_listbox.insert(END, f" {i}")
                    time.sleep(5)

            T7 = threading.Thread(target=refresh)
            T7.daemon = True
            T7.start()

        def plex_ui():
            plex_label1 = Label(
                ui_frame_right,
                text="Movie Collection:",  # Text displayed on the label
                bg=background1,  # Background color of the label
                fg=green,  # Color of the text on the label
                width=0,  # Width of the label
                font=(
                    "Comic Sans MS",
                    15,
                    "bold",
                ),  # Font and size of the text on the label
            )
            plex_label2 = Label(
                ui_frame_right,
                text=instructions2,  # Text displayed on the label
                width=0,  # Width of the label
                bg=background1,  # Background color of the label
                fg=pink,  # Color of the text on the label
                font=(
                    "Comic Sans MS",
                    11,
                    "bold",
                ),  # Font and size of the text on the label
            )
            plex_listbox = Listbox(
                ui_frame_right,
                bg=background2,  # Background color of the listbox
                fg=green,  # Color of the text in the listbox
                width=47,  # Width of the listbox
                height=18,  # Height of the listbox
                bd=0,  # Border size of the listbox
                font=(
                    "Comic Sans MS",
                    11,
                    "bold",
                ),  # Font and size of the text in the listbox
            )
            plex_label1.place(x=0, y=345)
            plex_label2.place(x=0, y=375)
            plex_listbox.place(x=1, y=446)
            for letter in os.listdir(COLLECTION_DIR):
                for movie in os.listdir(f"{COLLECTION_DIR}/{letter}"):
                    if movie not in COLLECTION:
                        COLLECTION.append(movie)
            if len(COLLECTION) != len(plex_listbox.get(0, END)):
                plex_listbox.delete(0, END)
                for letter in os.listdir(COLLECTION_DIR):
                    for movie in os.listdir(f"{COLLECTION_DIR}/{letter}"):
                        if movie not in plex_listbox.get(0, END):
                            plex_listbox.insert(END, f" {movie}")

        compressed_ui()
        plex_ui()

    POSTER_ART_THREAD = threading.Thread(target=poster_art)
    POSTER_ART_THREAD.daemon = True
    POSTER_ART_THREAD.start()
    LEFT_UI_THREAD = threading.Thread(target=left_frame_ui)
    LEFT_UI_THREAD.daemon = True
    LEFT_UI_THREAD.start()
    RIGHT_UI_THREAD = threading.Thread(target=right_frame_ui)
    RIGHT_UI_THREAD.daemon = True
    RIGHT_UI_THREAD.start()
    RIP_SCRAPE_LOOP_THREAD = threading.Thread(target=rip_scrape_loop)
    RIP_SCRAPE_LOOP_THREAD.daemon = True
    # RIP_SCRAPE_LOOP_THREAD.start()
    TRANSCODE_LOOP_THREAD = threading.Thread(target=transcode_loop)
    TRANSCODE_LOOP_THREAD.daemon = True
    TRANSCODE_LOOP_THREAD.start()
    TERMINAL_UI_THREAD = threading.Thread(target=term_ui)
    TERMINAL_UI_THREAD.daemon = True
    # TERMINAL_UI_THREAD.start()
    root.mainloop()


if __name__ == "__main__":
    main()
