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
        self.drive_letter = drive_letter
        self.drive_number = drive_number
        self.drive_bay = drive_bay
        if (
            self.drive_letter is None
            or self.drive_number is None
            or self.drive_bay is None
        ):
            pass
        else:
            if not os.listdir(self.drive_bay):
                self.movie_directory_temp = f"{self.drive_bay}{self.drive_number}"
                os.mkdir(self.movie_directory_temp)
                self.DVD = MakeMKV(drive_letter)
                try:
                    drive_info = win32api.GetVolumeInformation(drive_letter[:-1])
                    drive_info = (
                        re.sub(r"[^A-Za-z0-9\s]", "", drive_info[0].replace("_", " "))
                        .strip()
                        .lower()
                    )
                    self.drive_info = drive_info
                except BaseException:
                    self.drive_info = None

                try:
                    dvd_info = self.DVD.info()
                    dvd_info = (
                        re.sub(
                            r"[^A-Za-z0-9\s]",
                            "",
                            dvd_info["disc"]["name"].replace("_", " "),
                        )
                        .strip()
                        .lower()
                    )
                    self.dvd_info = dvd_info
                except BaseException:
                    self.dvd_info = None

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
                        self.title_list = titles
                except Exception:
                    self.title_list = None

                if self.drive_info == None:
                    self.drive_info == self.dvd_info
                if self.dvd_info == None:
                    self.dvd_info = self.drive_info
                if (
                    self.drive_info is None
                    or self.dvd_info is None
                    or self.title_list is None
                ):
                    best_match = self.drive_info
                else:
                    try:
                        drive_info_match = difflib.get_close_matches(
                            self.drive_info, self.title_list, n=1, cutoff=0.2
                        )
                        drive_info_match_percent = difflib.SequenceMatcher(
                            None, self.drive_info, drive_info_match[0]
                        ).ratio()
                        drive_info_match = drive_info_match[0]
                    except Exception as e:
                        drive_info_match = self.drive_info
                        drive_info_match_percent = 0.0
                    self.drive_info_match = drive_info_match
                    self.drive_info_match_percent = drive_info_match_percent
                    try:
                        dvd_info_match = difflib.get_close_matches(
                            self.dvd_info, self.title_list, n=1, cutoff=0.2
                        )
                        dvd_info_match_percent = difflib.SequenceMatcher(
                            None, self.dvd_info, dvd_info_match[0]
                        ).ratio()
                        dvd_info_match = dvd_info_match[0]
                    except Exception as e:
                        dvd_info_match = self.dvd_info
                        dvd_info_match_percent = 0.0
                    self.dvd_info_match = dvd_info_match
                    self.dvd_info_match_percent = dvd_info_match_percent
                    try:
                        if (
                            self.dvd_info_match_percent < 0.40
                            and self.drive_info_match_percent < 0.40
                        ):
                            best_match = self.drive_info
                        else:
                            if (
                                self.dvd_info_match_percent
                                == self.drive_info_match_percent
                            ):
                                if len(self.dvd_info_match) > len(
                                    self.drive_info_match
                                ):
                                    best_match = self.dvd_info_match
                                else:
                                    best_match = self.drive_info_match
                            elif (
                                self.dvd_info_match_percent
                                < self.drive_info_match_percent
                            ):
                                best_match = self.drive_info_match
                            else:
                                best_match = self.dvd_info_match
                    except Exception as e:
                        best_match = self.drive_info
                self.best_match = best_match
                if self.best_match == None:
                    self.movie_link = "https://github.com/mickdupreez/mr_ripper"
                    self.movie_title = self.best_match
                    self.movie_poster = Im.open("default.png")
                    self.movie_directory = f"{self.drive_bay}{self.movie_title}/"
                else:
                    try:
                        query = self.best_match.replace(" ", "+")
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
                        self.movie_link = link
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
                        browser.get(self.movie_link)
                        movie_title = (
                            browser.title.replace(") - IMDb", "")
                            .replace("(", "")
                            .replace(":", "")
                        )
                        self.movie_title = movie_title
                        self.movie_directory = f"{self.drive_bay}{self.movie_title}/"
                        os.rename(self.movie_directory_temp, self.movie_directory)
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
                                self.movie_poster = poster
                                self.movie_poster.save(
                                    f"{self.movie_directory}{self.movie_title}.png"
                                )
                                os.remove("temp.jpg")
                                browser.quit()
                                service.stop()
                    except Exception as e:
                        service.stop()
                        self.movie_link = "https://github.com/mickdupreez/mr_ripper"
                        self.movie_title = self.best_match
                        self.movie_poster = Im.open("default.png")
                        self.movie_directory = f"{self.drive_bay}{self.movie_title}/"

    def Rip(self):
        try:
            self.DVD.mkv(self.drive_number, self.movie_directory)
            shutil.move(f"{self.movie_directory}", Directories().Queued_Dir)
            ctypes.windll.WINMM.mciSendStringW(
                "set cdaudio door open", None, self.drive_number, None
            )
        except Exception:
            ctypes.windll.WINMM.mciSendStringW(
                "set cdaudio door open", None, self.drive_number, None
            )


#! TESTING !#
def TESTING():
    def TARGET_1():
        while True:
            TARGET = Directories().Target1
            if not TARGET[0]:
                pass
            else:
                Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2]).Rip()
            time.sleep(10)

    threading.Thread(target=TARGET_1).start()

    def TARGET_2():
        while True:
            TARGET = Directories().Target2
            if not TARGET[0]:
                pass
            else:
                Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2]).Rip()
            time.sleep(10)

    threading.Thread(target=TARGET_2).start()

    def TARGET_3():
        while True:
            TARGET = Directories().Target3
            if not TARGET[0]:
                pass
            else:
                Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2]).Rip()
            time.sleep(10)

    threading.Thread(target=TARGET_3).start()


#! TESTING !#
if __name__ == "__main__":
    TESTING()
