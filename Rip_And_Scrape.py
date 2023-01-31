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
    """
    The Rip_And_Scrape class extracts and scrapes information from a DVD in the drive specified by the user.
    
    Attributes:
        drive_letter (str): The drive letter of the DVD drive.
        drive_number (str): The number associated with the DVD drive.
        drive_bay (str): The bay location of the DVD drive.
        movie_directory_temp (str): The temporary movie directory created.
        DVD (MakeMKV): The instance of the MakeMKV class that allows to extract information from the DVD.
        drive_info (str): The information of the DVD drive obtained from win32api.GetVolumeInformation().
        dvd_info (str): The information of the DVD obtained from MakeMKV.info().
        title_list (List[str]): The list of movie titles.
        drive_info_match (str): The closest match of drive_info to the title_list.
        drive_info_match_percent (float): The similarity ratio of drive_info and drive_info_match.
        dvd_info_match (str): The closest match of dvd_info to the title_list.
        dvd_info_match_percent (float): The similarity ratio of dvd_info and dvd_info_match.
        best_match (str): The closest match of drive_info and dvd_info to the title_list.
        title_match_percent (float): The similarity ratio of best_match and the closest title in the title_list.
        scraped_data (str): The information scraped from the internet.
        soup (BeautifulSoup): The instance of the BeautifulSoup class that is used to parse the scraped data.
        movie_directory (str): The final movie directory created.
        
    """
    def __init__(self, drive_letter, drive_number, drive_bay):
        """
        The constructor of the Rip_And_Scrape class.
        
        Parameters:
            drive_letter (str): The drive letter of the DVD drive.
            drive_number (str): The number associated with the DVD drive.
            drive_bay (str): The bay location of the DVD drive.
        
        """
        # titles_list stores the file name of movie titles
        titles_list = "movie_titles.txt"
        # drive_letter stores the letter assigned to the DVD drive
        self.drive_letter = drive_letter
        # drive_number stores the drive number assigned to the DVD drive
        self.drive_number = drive_number
        # drive_bay stores the drive bay where the DVD drive is located
        self.drive_bay = drive_bay
        # Check if any of the drive parameters is None
        if (self.drive_letter is None or self.drive_number is None or self.drive_bay is None):
            # If any of the parameters is None, pass
            pass
        else:
            # Check if the drive bay is empty
            if not os.listdir(self.drive_bay):
                # If the drive bay is empty, create a directory with the drive number
                self.movie_directory_temp = f"{self.drive_bay}{self.drive_number}"
                os.mkdir(self.movie_directory_temp)
                # Create an instance of the MakeMKV class with the drive letter as the parameter
                self.DVD = MakeMKV(drive_letter)
                try:
                    # Try to get the volume information of the DVD drive
                    drive_info = win32api.GetVolumeInformation(drive_letter[:-1])
                    # Remove all non-alphanumeric characters from the volume name
                    drive_info = re.sub(r"[^A-Za-z0-9\s]", "", drive_info[0].replace("_", " ")).strip().lower()
                    # Store the cleaned volume information in the drive_info member variable
                    self.drive_info = drive_info
                except BaseException:
                    # If an exception occurs, store None in drive_info
                    self.drive_info = None
                # Try to get the information of the inserted DVD
                try:
                    # Get the information of the DVD using the `info` method of the `MakeMKV` object
                    dvd_info = self.DVD.info()
                    # Clean the name of the DVD to only include alphanumeric characters and whitespaces
                    dvd_info = (
                        re.sub(
                            r"[^A-Za-z0-9\s]",
                            "",
                            dvd_info["disc"]["name"].replace("_", " "),
                        )
                        .strip()
                        .lower()
                    )
                    # Store the cleaned DVD information
                    self.dvd_info = dvd_info
                # Catch any exception that may occur during this process
                except BaseException:
                    # Set the `dvd_info` attribute to None if the process fails
                    self.dvd_info = None
                # Try to get the list of movie titles
                try:
                    # Open the `titles_list` file in read mode
                    with codecs.open(titles_list, "r", encoding="utf-8") as file:
                        # Read all lines of the file
                        lines = file.readlines()
                        # Create a list of titles by splitting the lines and removing special characters
                        titles = []
                        for line in lines:
                            line_items = line.split(",")
                            titles.extend(line_items)
                        titles = [
                            re.sub(r"[^A-Za-z0-9\s]", "", item) for item in titles
                        ]
                        titles = [item.strip().lower() for item in titles]
                        titles = titles
                        # Store the list of movie titles
                        self.title_list = titles
                # Catch any exception that may occur during this process
                except Exception:
                    # Set the `title_list` attribute to None if the process fails
                    self.title_list = None
                if self.drive_info == None:
                    # If drive_info is None, set drive_info as dvd_info
                    self.drive_info == self.dvd_info
                if self.dvd_info == None:
                    # If dvd_info is None, set dvd_info as drive_info
                    self.dvd_info = self.drive_info
                if (
                    self.drive_info is None
                    or self.dvd_info is None
                    or self.title_list is None
                ):
                    # If any of drive_info, dvd_info, or title_list is None, set the best match as drive_info
                    best_match = self.drive_info
                else:
                    try:
                        # Find the closest match of drive_info in the title_list
                        drive_info_match = difflib.get_close_matches(
                            self.drive_info, self.title_list, n=1, cutoff=0.2
                        )
                        drive_info_match_percent = difflib.SequenceMatcher(
                            None, self.drive_info, drive_info_match[0]
                        ).ratio()
                        drive_info_match = drive_info_match[0]
                    except Exception as e:
                        # If the match fails, set drive_info_match as drive_info and match percentage as 0.0
                        drive_info_match = self.drive_info
                        drive_info_match_percent = 0.0
                    # Store the drive_info_match and drive_info_match_percent
                    self.drive_info_match = drive_info_match
                    self.drive_info_match_percent = drive_info_match_percent
                    try:
                        # Find the closest match of dvd_info in the title_list
                        dvd_info_match = difflib.get_close_matches(
                            self.dvd_info, self.title_list, n=1, cutoff=0.2
                        )
                        dvd_info_match_percent = difflib.SequenceMatcher(
                            None, self.dvd_info, dvd_info_match[0]
                        ).ratio()
                        dvd_info_match = dvd_info_match[0]
                    except Exception as e:
                        # If the match fails, set dvd_info_match as dvd_info and match percentage as 0.0
                        dvd_info_match = self.dvd_info
                        dvd_info_match_percent = 0.0
                    # Store the dvd_info_match and dvd_info_match_percent
                    self.dvd_info_match = dvd_info_match
                    self.dvd_info_match_percent = dvd_info_match_percent
                    # Compare the similarity between drive_info, dvd_info and title_list
                    try:
                        # Check if both drive_info and dvd_info matches are below 40%
                        if (self.dvd_info_match_percent < 0.40 and
                            self.drive_info_match_percent < 0.40):
                            best_match = self.drive_info
                        else:
                            # If both matches have the same similarity, choose the one with shorter length
                            if self.dvd_info_match_percent == self.drive_info_match_percent:
                                if len(self.dvd_info_match) > len(self.drive_info_match):
                                    best_match = self.dvd_info_match
                                else:
                                    best_match = self.drive_info_match
                            # Choose the match with higher similarity percentage
                            elif self.dvd_info_match_percent < self.drive_info_match_percent:
                                best_match = self.drive_info_match
                            else:
                                best_match = self.dvd_info_match
                    except Exception as e:
                        # If any error occurs, set best_match to drive_info
                        best_match = self.drive_info
                # Set the best_match attribute to the given best_match parameter
                self.best_match = best_match
                # If the best_match attribute is None
                if self.best_match == None:
                    # Set the movie_link attribute to a default URL
                    self.movie_link = "https://github.com/mickdupreez/mr_ripper"
                    # Set the movie_title attribute to the value of best_match
                    self.movie_title = self.best_match
                    # Open the default image and set it as the movie_poster attribute
                    self.movie_poster = Im.open("default.png")
                    # Set the movie_directory attribute using the drive_bay and movie_title attributes
                    self.movie_directory = f"{self.drive_bay}{self.movie_title}/"
                # If the best_match attribute is not None
                else:
                    # Try to execute the following block of code
                    try:
                        # Replace spaces in the best_match attribute with "+"
                        query = self.best_match.replace(" ", "+")
                        # Construct a URL using the best_match attribute for a Google search
                        url = f"https://www.google.com/search?q={query}+site:imdb.com"
                        # Define a dictionary for the headers to be sent with the request
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
                        }
                        # Send a GET request to the URL with the defined headers
                        response = requests.get(url, headers=headers)
                        # Parse the response text using BeautifulSoup
                        soup = BeautifulSoup(response.text, "html.parser")
                        # Initialize an empty list for links
                        links = []
                        # Iterate through all "a" elements in the soup object
                        for a in soup.find_all("a", href=True):
                            # If the "href" attribute starts with "https://www.imdb.com/title/tt"
                            # and ends with "\d+/$" using regular expression
                            if a["href"].startswith(
                                "https://www.imdb.com/title/tt"
                            ) and re.match(r"\d+/$", a["href"][-6:]):
                                # Append the "href" attribute to the links list
                                links.append(a["href"])
                                # Take the first item from the links list and set it as the link
                                link = links[:1]
                                link = link[0]
                        # Set the movie_link attribute to the value of link
                        self.movie_link = link






                        # Set the user agent string to mimic a Chrome browser 
                        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                        
                        # Create an instance of ChromeOptions to set various options for the webdriver instance
                        options = webdriver.ChromeOptions()
                        
                        # Add arguments to the options instance to set the browser to run in headless mode (without GUI), 
                        # set the log level to 3, set the user-agent, set the window size, 
                        # ignore certificate errors, allow running insecure content, disable extensions, 
                        # set the proxy server to direct, bypass all proxy settings, start the browser maximized, 
                        # disable GPU usage, disable dev shm usage, and disable sandboxing.
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
                        
                        # Create an instance of the Chrome driver service
                        service = Service("chromedriver.exe")
                        
                        # Start the service
                        service.start()
                        
                        # Create an instance of the Chrome webdriver
                        browser = webdriver.Remote(service.service_url, options=options)
                        
                        # Navigate to the IMDb page of the movie specified by the movie_link attribute
                        browser.get(self.movie_link)
                        
                        # Extract the title of the movie from the page title, and remove certain characters to clean the title.
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
