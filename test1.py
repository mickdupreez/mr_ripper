
import os
import re
import time

from googlesearch import search


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os
import win32api


from makemkv import MakeMKV
import urllib.request
from PIL import Image

class Directories:
    def __init__(self):
        compressed = "compressed/"
        plex = "plex/"
        temp = "temp/"
        transcoding = "transcoding/"
        uncompressed = "uncompressed/"

        directories = [
            compressed,
            plex,
            temp,
            transcoding,
            uncompressed
        ]
        for directory in directories: # For each directory in list
            if os.path.isdir(directory) != True: # If directory does not exist
                os.mkdir(directory) # Create directory
            else: # Skip if directory does not exist
                pass
        self.compressed = compressed
        self.compressed_list = os.listdir(compressed)
        self.plex = plex
        self.plex_list = os.listdir(plex)
        self.temp = temp
        self.temp_list = os.listdir(temp)
        self.transcoding = transcoding
        self.transcoding_list = os.listdir(transcoding)
        self.uncompressed = uncompressed
        self.uncompressed_list = os.listdir(uncompressed)
        self.directories = directories
        
class Scrape_Movie_Data:
    def __init__(self) -> None:
        self.drive_letter = "E:/"
        try:
            self.disc_info = MakeMKV(self.drive_letter).info()
            print(self.disc_info)
            self.movie_title = self.disc_info["disc"]["name"]
            print(self.movie_title)
            
            
        except Exception:
            self.disc_info = win32api.GetVolumeInformation(self.drive_letter)
            self.movie_title = self.disc_info[0].replace("_"," ")
        
        
        
        self.google_search =(self.movie_title + " movie IMDB")
        print(self.google_search)
        self.search_movie = search(self.google_search, num_results=3, lang="en")
        self.links = []
        for link in self.search_movie:
            print(link)
            if link.startswith("https://www.imdb.com/title/tt") and link.endswith("/"):
                if link not in self.links:
                    self.links.append(link)
                else:
                    pass
            else:
                pass
            
        self.imdb_link = self.links[0]
        print(self.links[0])
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=self.options)
    
        self.driver.get(self.imdb_link)
        self.driver.get_screenshot_as_file("screenshot.png")
        self.poster_dir = (self.driver.title.replace(") - IMDb", "").replace("(","").replace(":", ""))
        if self.poster_dir not in os.listdir(Directories().temp):
            os.mkdir(Directories().temp+self.poster_dir)
        else:
            pass
        
        self.search = self.driver.find_element_by_class_name("ipc-lockup-overlay__screen").click()

        self.page_source = self.driver.page_source
        pattern = re.compile(r'<img src="https://m\.media-amazon\.com/images/.+"')
        matches = pattern.findall(self.page_source)
        matches = str(matches[0])
        matches = matches.split(",")
        matches = matches[0]
        matches = matches.split('"')
        #
        for match in matches:
            if match.startswith("https") and match.endswith("jpg"):
                poster = match
                print(poster)
                urllib.request.urlretrieve(poster, "testing_poster.jpg")
                basehight = 900
                img = Image.open("testing_poster.jpg")
                hpercent = (basehight / float(img.size[1]))
                wsize = int((float(img.size[0]) * float(hpercent)))
                img = img.resize((wsize, basehight), Image.Resampling.LANCZOS)
                img.save(f"{Directories().temp+self.poster_dir}/{self.poster_dir}.png")
            else:
                pass
            
                
        self.driver.quit()
        

Scrape_Movie_Data()




