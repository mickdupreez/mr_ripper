import os
import re
import time
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
from makemkv import MakeMKV
from PIL import Image as Im
from bs4 import BeautifulSoup
from selenium import webdriver
from googlesearch import search
from selenium.webdriver.common.by import By

def rip_and_transcode():
    class Directories:
        compressed = "compressed/"
        plex = "plex/"
        temp = "temp/"
        transcoding = "transcoding/"
        uncompressed = "uncompressed/"

        def __init__(self):
            self.compressed_list = self.get_directory_contents(self.compressed)
            self.plex_list = self.get_directory_contents(self.plex)
            self.temp_list = self.get_directory_contents(self.temp)
            self.transcoding_list = self.get_directory_contents(self.transcoding)
            self.uncompressed_list = self.get_directory_contents(self.uncompressed)
            self.directories = [
                self.compressed,
                self.plex,
                self.temp,
                self.transcoding,
                self.uncompressed
            ]

        def get_directory_contents(self, directory):
            if not os.path.exists(directory):
                os.makedirs(directory)
            return os.listdir(directory)

    def get_cd_drive():
        try:
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for drive in drives:
                if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                    return drive
        except Exception as e:
            print(f"An error occurred !!!NO DRIVE DETECTED!!!. Please make sure that you have a DVD drive connected to your PC: {e}")
            return None

    def preprocess_string(string):
        try:
            string = re.sub(r'\b\d{4}\b', '', string)
            string = re.sub(r'[^A-Za-z0-9\s]', '', string)
            string = string.strip().lower()
            return string
        except Exception as e:
            print(f"An error occurred while preprocessing the string :{string}:: {e}")
            return string

    def get_volume_information():
        try:
            drive_letter = get_cd_drive()
            if drive_letter != None:
                volume_info = win32api.GetVolumeInformation(drive_letter)
                volume_info = volume_info[0]
                volume_info = volume_info.replace("_", " ")
                volume_info = preprocess_string(volume_info)
                return volume_info
            else:
                print("ERROR, The 'drive_letter' is None. Please connect a DVD Drive to your PC.")
                return None
        except Exception as e:
            print(f"An error has occurred, please insert a DVD.: {e}")
            return None

    def get_disc_information():
        try:
            drive_letter = get_cd_drive()
            if drive_letter != None:
                disc_information = MakeMKV(drive_letter).info()
                disc_info = disc_information["disc"]["name"]
                disc_info = disc_info.replace("_", " ")
                disc_info = preprocess_string(disc_info)
                return disc_info
            else:
                print("ERROR, The 'drive_letter' is None. Please connect a DVD Drive to your PC.")
                return None
        except Exception as e:
            print(f"An error has occurred, please insert a DVD.: {e}")
            return None

    def get_items():
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
                return items
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None


    def get_movie_title():
        try:
            disc_info=get_disc_information()
            volume_info=get_volume_information()
            items=get_items()
            
            def get_match(string, items):
                match = None
                max_percent = 0
                for item in items:
                    percent = difflib.SequenceMatcher(None, string, item).ratio()
                    if percent > max_percent:
                        max_percent = percent
                        match = item
                return match, max_percent

            if disc_info is None or volume_info is None or items is None:
                print("An error occurred while getting disc, volume, or item information")
                return None
            else:
                disc_match, disc_percent = get_match(disc_info, items)
                volume_match, volume_percent = get_match(volume_info, items)
                if disc_percent < 0.55 and volume_percent < 0.55:
                    print("There are no matches, using the 'volume_info' as the string to search for.")
                    time.sleep(3)
                    return volume_info
                else:
                    print(disc_info, disc_percent)
                    print(volume_info, volume_percent)
                    if disc_percent > volume_percent:
                        return disc_match
                    else:
                        return volume_match
        except Exception as e:
            print(f"An unexpected error occurred, using the 'volume_info' as the string to search for. : {e}")
            return volume_info

    def get_movie_links():
        try:
            title = get_movie_title()
            if title != None:
                query = title.replace(" ", "+")
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
                return link
            else:
                print("An error occurred while getting the movie title")
                return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_movie_data():
        try:
            link = get_movie_links()
            if link != None:
                movie_imdb_link = link[0]
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                options = webdriver.ChromeOptions()
                options.headless = True
                options.add_argument("--silent")
                options.add_argument(f'user-agent={user_agent}')
                options.add_argument("--window-size=1920,1080")
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--allow-running-insecure-content')
                options.add_argument("--disable-extensions")
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")
                options.add_argument("--start-maximized")
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
                browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
                browser.get(movie_imdb_link)
                movie_title = (browser.title.replace(") - IMDb", "").replace("(","").replace(":", ""))
                print(movie_title)
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
                        return movie_title, movie_poster
            else:
                print(f"An error occurred while getting the link, try again later")
                movie_title = get_movie_title()
                return movie_title, None
        except Exception as e:
            print(f"An error occurred while downloading the movie data from the web, try again later : {e}")
            movie_title = get_movie_title()
            return movie_title, None

    def transcode():
        try:
            time.sleep(5)
            uncompressed_list = Directories().uncompressed_list
            if uncompressed_list == []:
                raise ValueError("The uncompressed list is empty")
            name = uncompressed_list[0]
            dir_location = f"{Directories().uncompressed}{name}"
            if not os.path.isdir(dir_location):
                raise ValueError(f"{dir_location} is not a valid directory")
            dir_destination = f"{Directories().transcoding}"
            shutil.move(dir_location, dir_destination)
            for file in os.listdir(f"{Directories().transcoding}{name}"):
                if file.endswith(".mkv"):
                    file_name = file
                    input_file = f"{Directories().transcoding}{name}/{file_name}"
                    output_file = f"{Directories().transcoding}{name}/{name}.mkv"
                    print(input_file, output_file)
                    time.sleep(5)
                    command  = [
                        "HandBrakeCLI.exe", "--preset-import-file", "profile.json", "-Z", "PLEX",
                        "-i", input_file, "-o",
                        output_file
                    ]
                    subprocess.run(command, shell=True)
                    shutil.move(f"{Directories().transcoding}{name}", f"{Directories().compressed}")
                    time.sleep(3)
                    uncompressed_file = f"{Directories().compressed}{name}/{file_name}"
                    os.remove(uncompressed_file)
                    time.sleep(2)
                    return None
                else:
                    pass
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def rip():
        try:
            movie_title, movie_poster = get_movie_data()
            if movie_title != None:
                output_directory = f"{Directories().temp}{movie_title}/"
                os.makedirs(output_directory, exist_ok=True)
                if movie_poster != None:
                    movie_poster.save(f"{output_directory}/{movie_title}.jpg")
                try:
                    makemkv = MakeMKV(0)
                    print("starting RIP")
                    makemkv.mkv(0, output_directory)
                    print("Rip finished")
                    return output_directory, movie_title
                except Exception:
                    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
                    return None, None
            else:
                print("There is no movie Title. You have issues with getting the movie data")
                return None, None
        except Exception as e:
            print(f"There Has been an issue ripping this file, please reinsert the DVD and try again. : {e}")
            return None, None

    def move_and_transcode():
        try:
            output_directory, movie_title = rip()
            if output_directory != None:
                output_directory_size = sum(os.path.getsize(os.path.join(output_directory, f)) for f in os.listdir(output_directory))
                output_directory_size_gb = output_directory_size / (1024 ** 3)
                print(output_directory_size_gb)
                if output_directory_size_gb > 20:
                    file_destination =  f"{Directories().uncompressed}"
                else:
                    file_destination =  f"{Directories().compressed}"
                    for file in os.listdir(f"{Directories().temp}{movie_title}"):
                        if file.endswith('.mkv'):
                            os.rename(f"{Directories().temp}{movie_title}/{file}", f"{Directories().temp}{movie_title}/{movie_title}.mkv")
                        else:
                            pass
                shutil.move(output_directory, file_destination)
                threading.Thread(target=transcode).start()
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
                return movie_title
            else:
                print("Error, there is no output directory")
                return None
        except Exception as e:
            print("Error While moving and transcoding file. {e}")
            return None
        
    if get_cd_drive() != None:
        if get_disc_information() is None or get_volume_information() is None:
            print("Error, Please insert a DVD into the attached DVD drive.")
            time.sleep(5)
        else:
            move_and_transcode
    else:
        print("Error, Please attach a DVD drive")
        time.sleep(5)

while True:
    rip_and_transcode()