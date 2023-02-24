import os
import re
import time
import ctypes
import shutil
import codecs
import difflib
import win32api
import requests
import urllib.request
from PIL import Image as Im
from makemkv import MakeMKV
from bs4 import BeautifulSoup
from selenium import webdriver
from Directories import Directories
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading


class Rip_And_Scrape:
    def __init__(self, drive_letter, drive_number, drive_bay):

        titles_list = "movie_titles.txt"

        if drive_letter is None or drive_number is None or drive_bay is None:
            pass
        else:

            if not os.listdir(drive_bay):
                movie_directory_temp = f"{drive_bay}Scanning Disc.."
                os.mkdir(movie_directory_temp)
                DVD = MakeMKV(drive_letter)
                try:
                    drive_info = win32api.GetVolumeInformation(drive_letter[:-1])
                    drive_info = (
                        re.sub(r"[^A-Za-z0-9\s]", "", drive_info[0].replace("_", " "))
                        .strip()
                        .lower()
                    )
                    drive_info = drive_info
                except BaseException:
                    os.rmdir(movie_directory_temp)
                    drive_info = None
                try:
                    dvd_info = DVD.info()
                    dvd_info = (
                        re.sub(
                            r"[^A-Za-z0-9\s]",
                            "",
                            dvd_info["disc"]["name"].replace("_", " "),
                        )
                        .strip()
                        .lower()
                    )
                    dvd_info = dvd_info
                except BaseException:
                    os.rmdir(movie_directory_temp)
                    dvd_info = None
                try:
                    with codecs.open(titles_list, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        titles = []
                        for line in lines:
                            line_items = line.split(",")
                            titles.extend(line_items)
                        titles = [
                            re.sub(r"[^A-Za-z0-9\s]", "", item) for item in titles
                        ]
                        titles = [item.strip().lower() for item in titles]
                        titles = titles
                        title_list = titles
                except Exception:
                    title_list = None
                if drive_info == None:
                    drive_info == dvd_info
                if dvd_info == None:
                    dvd_info = drive_info
                if drive_info is None or dvd_info is None or title_list is None:
                    best_match = drive_info
                else:
                    try:
                        drive_info_match = difflib.get_close_matches(
                            drive_info, title_list, n=1, cutoff=0.2
                        )
                        drive_info_match_percent = difflib.SequenceMatcher(
                            None, drive_info, drive_info_match[0]
                        ).ratio()
                        drive_info_match = drive_info_match[0]
                    except Exception as e:
                        drive_info_match = drive_info
                        drive_info_match_percent = 0.0
                    drive_info_match = drive_info_match
                    drive_info_match_percent = drive_info_match_percent
                    try:
                        dvd_info_match = difflib.get_close_matches(
                            dvd_info, title_list, n=1, cutoff=0.2
                        )
                        dvd_info_match_percent = difflib.SequenceMatcher(
                            None, dvd_info, dvd_info_match[0]
                        ).ratio()
                        dvd_info_match = dvd_info_match[0]
                    except Exception as e:
                        dvd_info_match = dvd_info
                        dvd_info_match_percent = 0.0
                    dvd_info_match = dvd_info_match
                    dvd_info_match_percent = dvd_info_match_percent
                    try:
                        if (
                            dvd_info_match_percent < 0.40
                            and drive_info_match_percent < 0.40
                        ):
                            best_match = drive_info
                        else:
                            if dvd_info_match_percent == drive_info_match_percent:
                                if len(dvd_info_match) > len(drive_info_match):
                                    best_match = dvd_info_match
                                else:
                                    best_match = drive_info_match
                            elif dvd_info_match_percent < drive_info_match_percent:
                                best_match = drive_info_match
                            else:
                                best_match = dvd_info_match
                    except Exception as e:
                        best_match = drive_info
                best_match = best_match
                if best_match == None:
                    movie_link = "https://github.com/mickdupreez/mr_ripper"
                    movie_title = best_match
                    movie_poster = Im.open("default.png")
                    movie_directory = f"{drive_bay}{movie_title}/"
                else:
                    try:
                        query = best_match.replace(" ", "+")
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
                        movie_link = link

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

                        # Start the service
                        service.start()

                        browser = webdriver.Remote(service.service_url, options=options)

                        browser.get(movie_link)

                        movie_title = (
                            browser.title.replace(") - IMDb", "")
                            .replace("(", "")
                            .replace(":", "")
                        )

                        movie_title = movie_title
                        movie_directory = f"{drive_bay}{movie_title}/"
                        os.rename(movie_directory_temp, movie_directory)
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
                                movie_poster = poster
                                movie_poster.save(f"{movie_directory}{movie_title}.png")
                                os.remove("temp.jpg")
                                browser.quit()
                                service.stop()

                    except Exception as e:
                        service.stop()
                        movie_link = "https://github.com/mickdupreez/mr_ripper"
                        movie_title = best_match
                        movie_poster = Im.open("default.png")
                        movie_directory = f"{drive_bay}{movie_title}/"
        try:
            self.drive_letter = drive_letter
            self.drive_number = drive_number
            self.drive_bay = drive_bay
            self.movie_directory_temp = f"{self.drive_bay}{self.drive_number}"
            self.DVD = DVD
            self.title_list = titles

            self.drive_info = drive_info
            self.drive_info_match = drive_info_match
            self.drive_info_match_percent = drive_info_match_percent

            self.dvd_info = dvd_info
            self.dvd_info_match = dvd_info_match
            self.dvd_info_match_percent = dvd_info_match_percent

            self.best_match = best_match
            self.movie_link = link
            self.movie_title = movie_title
            self.movie_directory = f"{self.drive_bay}{self.movie_title}/"
            self.movie_poster = poster
        except UnboundLocalError:
            pass

    def Rip(self):
        try:
            self.DVD.mkv(self.drive_number, self.movie_directory)
            ctypes.windll.WINMM.mciSendStringW(
                "set cdaudio door open", None, self.drive_number, None
            )
            shutil.move(f"{self.movie_directory}", Directories().queued_directory)
        except Exception:
            pass


#! TESTING !#
def Rip_And_Scrape_Testing():
    def BAY1():
        while True:

            TARGET = Directories().RIPPING_BAY_1
            if not TARGET[0]:
                pass
            else:
                BAY = Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2])

                print(
                    "BAY1 is ready to Rip movie : \n",
                    f"Drive Letter : {BAY.drive_letter}\n",
                    f"Drive Number : {BAY.drive_number}\n",
                    f"Drive Bay : {BAY.drive_bay}\n",
                    f"Number of Movies in the Movie Name List : {len(BAY.title_list)}\n",
                    f"DVD Name gathered from Drive Info : {BAY.drive_info}\n",
                    f"Drive Info Best match from list : {BAY.drive_info_match}\n",
                    f"Drive Info Best match 0 to 1  : {BAY.drive_info_match}\n",
                    f"DVD Name gathered from DVD Info : {BAY.dvd_info}\n",
                    f"DVD Info Best match from list : {BAY.dvd_info_match}\n",
                    f"DVD Info Best match 0 to 1  : {BAY.dvd_info_match}\n",
                    f"The best match for the Movie Name out of Drive Info and DVD Info is  : {BAY.best_match}\n",
                    f"IMDB link for the Movie name {BAY.best_match} : {BAY.movie_link}\n",
                    f"Movie title scraped from IMDB : {BAY.movie_title}\n",
                    f"Movie Directory created from the scraped Movie Title This is where the movie will Rip to: {BAY.movie_directory}\n",
                    f"Movie poster object scraped from IMDB Saved in the Movie Directory: {BAY.movie_poster}\n",
                )

                BAY.Rip()
            time.sleep(10)

    threading.Thread(target=BAY1).start()

    def BAY2():
        while True:
            TARGET = Directories().RIPPING_BAY_2
            if not TARGET[0]:
                pass
            else:
                BAY = Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2])
                print(
                    "BAY2 is ready to Rip movie : \n",
                    f"Drive Letter : {BAY.drive_letter}\n",
                    f"Drive Number : {BAY.drive_number}\n",
                    f"Drive Bay : {BAY.drive_bay}\n",
                    f"Number of Movies in the Movie Name List : {len(BAY.title_list)}\n",
                    f"DVD Name gathered from Drive Info : {BAY.drive_info}\n",
                    f"Drive Info Best match from list : {BAY.drive_info_match}\n",
                    f"Drive Info Best match 0 to 1  : {BAY.drive_info_match}\n",
                    f"DVD Name gathered from DVD Info : {BAY.dvd_info}\n",
                    f"DVD Info Best match from list : {BAY.dvd_info_match}\n",
                    f"DVD Info Best match 0 to 1  : {BAY.dvd_info_match}\n",
                    f"The best match for the Movie Name out of Drive Info and DVD Info is  : {BAY.best_match}\n",
                    f"IMDB link for the Movie name {BAY.best_match} : {BAY.movie_link}\n",
                    f"Movie title scraped from IMDB : {BAY.movie_title}\n",
                    f"Movie Directory created from the scraped Movie Title This is where the movie will Rip to: {BAY.movie_directory}\n",
                    f"Movie poster object scraped from IMDB Saved in the Movie Directory: {BAY.movie_poster}\n",
                )

                BAY.Rip()
            time.sleep(10)

    threading.Thread(target=BAY2).start()

    def BAY3():
        while True:
            TARGET = Directories().RIPPING_BAY_3
            if not TARGET[0]:
                pass
            else:
                BAY = Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2])
                print(
                    "BAY3 is ready to Rip movie : \n",
                    f"Drive Letter : {BAY.drive_letter}\n",
                    f"Drive Number : {BAY.drive_number}\n",
                    f"Drive Bay : {BAY.drive_bay}\n",
                    f"Number of Movies in the Movie Name List : {len(BAY.title_list)}\n",
                    f"DVD Name gathered from Drive Info : {BAY.drive_info}\n",
                    f"Drive Info Best match from list : {BAY.drive_info_match}\n",
                    f"Drive Info Best match 0 to 1  : {BAY.drive_info_match}\n",
                    f"DVD Name gathered from DVD Info : {BAY.dvd_info}\n",
                    f"DVD Info Best match from list : {BAY.dvd_info_match}\n",
                    f"DVD Info Best match 0 to 1  : {BAY.dvd_info_match}\n",
                    f"The best match for the Movie Name out of Drive Info and DVD Info is  : {BAY.best_match}\n",
                    f"IMDB link for the Movie name {BAY.best_match} : {BAY.movie_link}\n",
                    f"Movie title scraped from IMDB : {BAY.movie_title}\n",
                    f"Movie Directory created from the scraped Movie Title This is where the movie will Rip to: {BAY.movie_directory}\n",
                    f"Movie poster object scraped from IMDB Saved in the Movie Directory: {BAY.movie_poster}\n",
                )

                BAY.Rip()
            time.sleep(10)

    threading.Thread(target=BAY3).start()


#! TESTING !#
if __name__ == "__main__":
    Rip_And_Scrape_Testing()
