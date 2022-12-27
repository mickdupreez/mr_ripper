import os
import re
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.by import By
import win32api
import win32file
from makemkv import MakeMKV
import urllib.request
import ctypes
import shutil
from PIL import Image as Im
import codecs
import difflib
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import threading

def rip_and_transcode():
    """
    This function is responsible for the overall flow of the program. It handles the setup and initialization of necessary
    variables and objects, and calls the functions that handle the various steps of the process.
    
    The steps performed by this function are:
    1. Initialize the Directories class and set up the necessary directories.
    2. Get the list of possible movie titles from the movie_titles.txt file.
    3. Get the volume information and disc information from the CD/DVD drive.
    4. Use the volume information and disc information to search for the movie title and poster online.
    5. Rip the CD/DVD using the MakeMKV class.
    6. Move the output directory to either the uncompressed or compressed directory, depending on the size of the directory.
       If the size is larger than 20GB, the directory is moved to the uncompressed directory. If it is smaller, it is moved
       to the compressed directory and is also renamed to match the movie title.
    7. Start a new thread to transcode the movie.
    8. Return the movie title.
    """
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
        except FileNotFoundError:
            print("The file specified in 'possible_title' was not found.")
            return []
        except UnicodeDecodeError:
            print("There was a problem decoding the file with the specified encoding.")
            return []
        except PermissionError:
            print("The program does not have permission to access the file.")
            return []
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return []

    def get_cd_drive():
        try:
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for drive in drives:
                if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                    return drive
        except ImportError as e:
            print(f"An error occurred while importing the win32api or win32file module: {e}")
            return None
        except WindowsError as e:
            print(f"An error occurred while accessing the drive: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while getting the CD/DVD drive: {e}")
            return None

    def preprocess_string(string):
        try:
            string = re.sub(r'\b\d{4}\b', '', string)
            string = re.sub(r'[^A-Za-z0-9\s]', '', string)
            string = string.strip().lower()
            return string
        except TypeError as e:
            print(f"An error occurred while preprocessing the string: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while preprocessing the string: {e}")
            return None

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
                print("An error occurred while accessing the CD/DVD drive")
                return None
        except OSError as e:
            print(f"An error occurred while getting the volume information due to an operating system error: {e}")
            return None
        except ValueError as e:
            print(f"An error occurred while getting the volume information due to an invalid value: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while getting the volume information: {e}")
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
                print("An error occurred while accessing the CD/DVD drive")
                return None
        except ImportError as e:
            print(f"An error occurred while importing the required module: {e}")
            return None
        except OSError as e:
            print(f"An error occurred while accessing the CD/DVD drive: {e}")
            return None
        except TypeError as e:
            print(f"An error occurred while processing the disc information: {e}")
            return None
        except AttributeError as e:
            print(f"An error occurred while accessing an attribute of the disc information: {e}")
            return None
        except KeyError as e:
            print(f"An error occurred while accessing a key of the disc information: {e}")
            return None
        except Exception as e:
            print(f"An unknown error occurred while getting the disc information: {e}")
            return None

    def get_movie_title(
        disc_info = get_disc_information(),
        volume_info = get_volume_information(),
        items = get_items()
        ):

        def get_match(string, items):
            match = None
            max_percent = 0
            for item in items:
                percent = difflib.SequenceMatcher(None, string, item).ratio()
                if percent > max_percent:
                    max_percent = percent
                    match = item
            return match, max_percent

        disc_match, disc_percent = get_match(disc_info, items)
        volume_match, volume_percent = get_match(volume_info, items)
        if disc_percent < 0.55 and volume_percent < 0.55:
            print("there are no matches")
            time.sleep(3)
            return volume_info
        else:
            print(disc_info, disc_percent)
            print(volume_info, volume_percent)
            if disc_percent > volume_percent:
                return disc_match
            else:
                return volume_match

    def get_movie_links():
        title = get_movie_title()
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
        return links[:1]

    def get_movie_data():
        link = get_movie_links()
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

    def transcode():
        time.sleep(5)
        uncompressed_list = Directories().uncompressed_list
        if uncompressed_list != []:
            name = uncompressed_list[0]
            dir_location = f"{Directories().uncompressed}{name}"
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
                else:
                    pass
        else:
            pass

    def rip():
        movie_title, movie_poster = get_movie_data()
        if movie_title == None:
            print("Error: There is no movie Title.")
        else:
            output_directory = f"{Directories().temp}{movie_title}/"
            os.makedirs(output_directory, exist_ok=True)
            movie_poster.save(f"{output_directory}/{movie_title}.jpg")
            try:
                makemkv = MakeMKV(0)
                print("starting RIP")
                makemkv.mkv(0, output_directory)
                print("Rip finished")
            except Exception:
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
        return output_directory, movie_title

    def move_and_transcode():
        output_directory, movie_title = rip()
        output_directory_size = sum(os.path.getsize(os.path.join(output_directory, f)) for f in os.listdir(output_directory))
        output_directory_size_gb = output_directory_size / (1024 ** 3)
        print(output_directory_size_gb)
        if output_directory_size_gb > 20:
            file_destination =  f"{Directories().uncompressed}"
            print("this file needs to be compressed")
            print(f"the file file destination is {file_destination} and the size is {output_directory_size_gb}")
        else:
            file_destination =  f"{Directories().compressed}"
            print("this file does not need to be compressed")
            print(f"the file file destination is {file_destination} and the size is {output_directory_size_gb}")
            print("The file will need to be renamed")
            for file in os.listdir(f"{Directories().temp}{movie_title}"):
                if file.endswith('.mkv'):
                    os.rename(f"{Directories().temp}{movie_title}/{file}", f"{Directories().temp}{movie_title}/{movie_title}.mkv")
                    
        shutil.move(output_directory, file_destination)
        threading.Thread(target=transcode).start()
        ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
        return movie_title

    move_and_transcode()

rip_and_transcode()