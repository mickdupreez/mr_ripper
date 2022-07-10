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
import ctypes
import subprocess
import shutil
import platform
import imdb
from tkinter import *
import threading
from datetime import datetime
from tkinter import filedialog
from PIL import Image as Im





global IMDB_Movie_Title
IMDB_Movie_Title = None




class Directories:
    """
        This class checks that all the directories that are required for the program to run
        exists, if it does not it will create it. 
        Those directories are then assigned to variables used through out hte program.
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
        self.compressed_list = os.listdir(self.compressed) # A list of items in the compressed directory
        self.plex_list = os.listdir(self.plex) # A list of items in the plex directory
        self.temp_list = os.listdir(self.temp) # A list of items in the temp directory
        self.transcoding_list = os.listdir(self.transcoding) # A list of items in the transcoding directory
        self.uncompressed_list = os.listdir(self.uncompressed) # A list of items in the uncompressed directory
        self.directories = [ # A list of all the directories variables above that is used throughout the program
            self.compressed, # The compressed directory
            self.plex, # The plex directory
            self.temp, # The temp directory
            self.transcoding, # The transcoding directory
            self.uncompressed # The uncompressed directory
        ]
        for directory in self.directories: # For each directory in the directories list
            if os.path.isdir(directory) != True: # If directory does not exist
                os.mkdir(directory) # Create directory
            else: # Skip if directory exists
                pass

class Rip_Scrape_Transcode:
    
    """
        This class is used to scrape the movie data from the disc itself and then use that to scrape IMDB website
        for Movie title and poster art work, this will also grab the movie data like cast and description in the future.
        
        TO DO:
            Add functionality to grab the movie data like cast and description.

    """
    def __init__(self):
        """
            This function gets called when Scrape_Movie_Data gets initialized.
            
            SECTION 1: This is where the variable disc_title is created.
            SECTION 2: This is where the variable disc_title is passed through a google search to
            generate the movie_imdb_link.
            SECTION 3: This is where the default setting are set for the webdriver used for web scraping.
            SECTION 4: This is where the scraping takes places items currently scraped :
                MOVIE TITLE     : as self.Movie_Title
                MOVIE POSTER    : as self.Movie_Poster
            SECTION 5: This is where the disc is ripped and moved to the uncompressed directory.
            section 6: This is where the movie is is transcoded in the background.
        """
        
        
######## SECTION 1:
        try: # Try checking if the is a disc in the tray if so continuing.
            drive_letter = "E:/" # This the the letter that has been assigned to the disc drive.
            win32api.GetVolumeInformation(drive_letter)
            try: # Try to use MakeMKV method to get info from disc.
                disc_info = MakeMKV(drive_letter).info() # variable that stores ALL the disc info.
                disc_title = disc_info["disc"]["name"] # variable that stores just the disc name.
            except Exception: # If MakeMKV method fails then use the title from drive_letter volume.
                disc_info = win32api.GetVolumeInformation(drive_letter) # Variable that stores the volume information.
                disc_title = disc_info[0].replace("_"," ") # Variable that stores just the disc name.
        except Exception: # If no disc in tray set disc_title to None.
            disc_title = None # Variable that stores just the disc name is None.

######## SECTION 2:
        if disc_title != None: # If disc_title is NOT None then Scrape_Movie_Data from Google.
            phrase = (disc_title + " movie IMDB") # Variable that stores the PHRASE the will be SEARCHED for.
            search_results = search(phrase, num_results=3, lang="en") # Variable that stores SEARCH results.
            links_list = [] # Variable that stores the list of links generated from the SEARCH.
            for link in search_results: # For LINK in search_results do the following
                if link.startswith("https://www.imdb.com/title/tt") and link.endswith("/"): # If LINK starts with 'https://www.imdb.com/title/tt' and ends with '/' then continue
                    if link not in links_list: # If the LINK is NOT in the links_list do the following.
                        links_list.append(link) # Append LINK to links_list.
                    else:
                        pass
                else:
                    pass
            movie_imdb_link = links_list[0] # Variable that stores the IMDB link for the IMDB poster and info scrape.

######## SECTION 3:
            ## IMPORTANT NOTE - options.headless set to False to see the browser being scraped.
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            options = webdriver.ChromeOptions() # Variable that stores the browser options.
            options.headless = False # Makes the scraping happen in the back ground.
            # These next .add_arguments are used to optimize the efficiency and speed of the scraping.
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
            browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options) # variable for storing the configured browser instance.

######## SECTION 4:
            browser.get(movie_imdb_link) # Search for the movie on IMDB.com using the movie_imdb_link
            global IMDB_Movie_Title
            self.Movie_Title = (browser.title.replace(") - IMDb", "").replace("(","").replace(":", "")) # Variable that stores the TITLE of the movie name.
            IMDB_Movie_Title = self.Movie_Title
            if self.Movie_Title not in os.listdir(Directories().temp): # If the movie in NOT in the TEMP directory then continue.
                os.mkdir(Directories().temp+self.Movie_Title) # Create a directory for the movie and all its data that will be scraped.
            else:
                pass
            browser.find_element_by_class_name("ipc-lockup-overlay__screen").click() # Open poster artwork page to scrape the poster.
            pattern = re.compile(r'<img src="https://m\.media-amazon\.com/images/.+"') # Variable that stores the the pattern that we are looking for in the page source code.
            matches = pattern.findall(browser.page_source) # Variable that stores the matches in a list.
            matches = str(matches[0]).split(",") # Formatting the matches in the list.
            matches = matches[0].split('"') # Formatting the matches in the list.
            for match in matches: # For match in the list of matches check:
                if match.startswith("https") and match.endswith("jpg"): # If LINK starts with 'https' and ends with 'jpg' continue.
                    poster_link = match # Variable that stores the URL of the poster image. 
                    urllib.request.urlretrieve(poster_link, "temp.jpg") # Download the poster image from the URL.
                    poster = Im.open("temp.jpg") # Variable that stores the poster image it 
                    poster_hight = 900 # Variable that stores the poster hight.
                    hight_percent = (poster_hight / float(poster.size[1])) # Variable that stores the height to width percentage of the poster.
                    poster_width = int((float(poster.size[0]) * float(hight_percent))) # Variable that stores the poster width.
                    poster = poster.resize((poster_width, poster_hight), Im.Resampling.LANCZOS) # Variable that stores the resized poster image.
                    poster.save(f"{Directories().temp+self.Movie_Title}/{self.Movie_Title}.png") # Save poster image the the temp/self.movie_title directory.
                    self.Movie_Poster = f"{Directories().temp+self.Movie_Title}/{self.Movie_Title}.png" # Variable that stores the poster image location
                    #back_ground.config(image=self.Movie_Poster)
                    os.remove("temp.jpg")
                else:
                    pass
            browser.quit() # Quit the browser after scraping completes.


######## SECTION 5: 
            if self.Movie_Title != None:
                #try:
                #    makemkv = MakeMKV(0) # Creating an instance of MakeMKV
                #    makemkv.mkv(0, f"{Directories().temp+self.Movie_Title}") # Using MakeMKV top make rip the DVD to the temp directory
                #except Exception:
                #    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                try:
                    file_location = f"{Directories().temp+self.Movie_Title}" # The location of the file
                    file_destination = f"{Directories().uncompressed+self.Movie_Title}" # The destination of the files one ripping has completed.
                    shutil.move(file_location, file_destination) # Move the file from the temp directory to the uncompressed directory
                    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                except IndexError:
                    pass
            else:
                pass

######## SECTION 6:
            def transcode():
                if os.path.exists(f"{Directories().transcoding+self.Movie_Title}"):
                    shutil.rmtree(f"{Directories().transcoding+self.Movie_Title}")
                else:
                    pass
                try:
                    shutil.move(f"{Directories().uncompressed+self.Movie_Title}",
                                f"{Directories().transcoding+self.Movie_Title}")
                    time.sleep(3) # Waiting for 3 seconds before continuing
                except shutil.Error:
                    time.sleep(5) # Waiting for 5 seconds before continuing
                    shutil.move(f"{Directories().uncompressed+self.Movie_Title}",
                                f"{Directories().transcoding+self.Movie_Title}")
                    time.sleep(3)

                for file in os.listdir(f"{Directories().transcoding+self.Movie_Title}"):
                    if file.endswith(".mkv"):
                        uncompressed_file =  file
                        command  = [ # This is a list of the arguments for the handbrake command.
                            "HandBrakeCLI.exe", "--preset-import-file", "profile.json", "-Z", "PLEX",
                            "-i", f"{Directories().transcoding+self.Movie_Title}/{uncompressed_file}", "-o",
                            f"{Directories().transcoding+self.Movie_Title}/{self.Movie_Title}.mkv"
                        ]
                        subprocess.run( # This is where the all the arguments are passed to handbrake to transcode the file.
                            command, # The list of commands.
                            shell=True) # Use the shell.
                        os.remove(f"{Directories().transcoding+self.Movie_Title}/{uncompressed_file}")
                        shutil.move(f"{Directories().transcoding+self.Movie_Title}", 
                                    f"{Directories().compressed+self.Movie_Title}")
                    else:
                        pass
            threading.Thread(target=transcode).start()
        else:
            self.Movie_Poster = None #
            self.Movie_Title = None #
            
            
Rip_Scrape_Transcode()