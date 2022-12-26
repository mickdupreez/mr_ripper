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
import imdb
from tkinter import *
import threading
from datetime import datetime
from tkinter import filedialog
from PIL import Image as Im
import imdb



root = Tk()
root.title("Mr Ripper")
root.iconbitmap("icon.ico")
root.geometry("1491x900")
root.resizable(False, False)
global IMDB_Movie_Title
IMDB_Movie_Title = None
global IMDB_Movie_Poster
IMDB_Movie_Poster = None
global collection_dir
collection_dir = None
collection = []
global drive_ready
drive_ready = None

def movie_collection():
    global collection_dir
    collection_dir = filedialog.askdirectory()
    print(collection_dir)
    testing_select_dir_button.destroy()
    return collection_dir

grey = "#1e1f1f"
turquoise = "#5cf0c2"
pink = "#e96163"
green = "#a7e961"
purple = "#a361e9"


intro = """     Welcome to Mr Ripper's Movie Ripper.
    This Program will Automatically Rip and
    Transcode and Blu-Ray or DVD Movies.
    add it to your media collection.
    
"""
instructions1 = """This list below contains successfully transcoded movies.
Once verified, the file will br moved to your collection."""

instructions2 = """This list below contains all the movies in your collection.
Click on a movie to preview movie description and poster."""

instructions3 = """

PLEASE CLICK HERE TO SELECT COLLECTION
DIRECTORY.

If the directory does not contain the
subdirectories A-Z, then they will be 
created for you.
"""

background = PhotoImage(file="default.png")
back_ground = Label(image=background)
back_ground.place(x=447, y=0)


ui_frame1 = LabelFrame(
    root, text="Mr Ripper.v0.1.2-beta",
    bg=grey, font=("Comic Sans MS",18, "bold"),
    padx=10, pady=10, fg=purple
    )
ui_frame1.place(x=0, y=2, width=450, height=900)

intro_label = Label(
    ui_frame1, text=intro, width=0, bg=grey
    , fg=turquoise, font=("Comic Sans MS", 13, "bold")
    )
intro_label.place(x=0, y=0)

ripping_status = Label(
    ui_frame1, text="", width=0, bg=grey,
    )
ripping_status.place(x=0, y=120)

transcoding_status = Label(
    ui_frame1, text="", width=0, bg=grey,
    )
transcoding_status.place(x=0, y=155)

completed_status_ = Label(
    ui_frame1, text="Completed Movies:", width=0, bg=grey,
    fg=purple, font=("Comic Sans MS", 15, "bold")
    )
completed_status_.place(x=0, y=325)

completed_status_instructions = Label(
    ui_frame1, text=instructions1, width=0, bg=grey,
    fg=turquoise, font=("Comic Sans MS", 11)
    )
completed_status_instructions.place(x=0, y=355)





ui_frame2 = LabelFrame(
    root, text="Movie Collection", bg=grey,
    font=("Comic Sans MS",18, "bold"), padx=10, pady=10,
    fg=purple
    )
ui_frame2.place(x=1041, y=2, width=450, height=900)

testing_listbox = Listbox(ui_frame2, bg="#1e1f1f", fg="#e96163", width=47, height=20, bd=0, font=("Comic Sans MS", 11))
testing_listbox.place(x=1, y=404)

testing_select_dir_button = Button(ui_frame2, text=instructions3, command=movie_collection, font=("Comic Sans MS", 13, "bold"), bg="#1e1f1f", fg="#e96163", width=42, height=17)
testing_select_dir_button.place(x=0, y=402)

transcoded_dir_listbox = Listbox(ui_frame1, bg="#1e1f1f", fg="#e96163", width=47, height=20, bd=0, font=("Comic Sans MS", 11))
transcoded_dir_listbox.place(x=1, y=404)

completed_status_ = Label(
    ui_frame2, text="Movie Collection:", width=0, bg=grey,
    fg=purple, font=("Comic Sans MS", 15, "bold")
    )
completed_status_.place(x=0, y=325)

completed_status_instructions = Label(
    ui_frame2, text=instructions2, width=0, bg=grey,
    fg=turquoise, font=("Comic Sans MS", 11)
    )
completed_status_instructions.place(x=0, y=355)



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
        global drive_ready
        drive_letter = "E:/" # This the the letter that has been assigned to the disc drive.
        if drive_ready != False:
            print("SECTION 1: Is The Drive Ready?") # !!!!DEBUGGING!!!!
            print(drive_ready)# !!!!DEBUGGING!!!!
            try: # Try checking if the is a disc in the tray if so continuing.
                win32api.GetVolumeInformation(drive_letter)
                print("SECTION 1: Is The Drive Ready?") # !!!!DEBUGGING!!!!
                drive_ready = False
                print(drive_ready)# !!!!DEBUGGING!!!!
                try: # Try to use MakeMKV method to get info from disc.
                    disc_info = MakeMKV(drive_letter).info() # variable that stores ALL the disc info.
                    disc_title = disc_info["disc"]["name"] # variable that stores just the disc name.
                except Exception: # If MakeMKV method fails then use the title from drive_letter volume.
                    disc_info = win32api.GetVolumeInformation(drive_letter) # Variable that stores the volume information.
                    disc_title = disc_info[0].replace("_"," ") # Variable that stores just the disc name.
            except Exception: # If no disc in tray set disc_title to None.
                print("SECTION 1: Is The Drive Ready?") # !!!!DEBUGGING!!!!
                disc_title = None # Variable that stores just the disc name is None.
                print(drive_ready)# !!!!DEBUGGING!!!!
                self.Movie_Title = None
                self.Movie_Poster = None
########     SECTION 2:
            if disc_title != None: # If disc_title is NOT None then Scrape_Movie_Data from Google.
                print("SECTION 2: Disc title is: " + disc_title) # !!!!DEBUGGING!!!!
                try: #
                    phrase = (disc_title + " movie IMDB") # Variable that stores the PHRASE the will be SEARCHED for.
                    print(phrase) # !!!!DEBUGGING!!!!
                    search_results = search(phrase, num_results=2, lang="en") # Variable that stores SEARCH results.
                    links_list = [] # Variable that stores the list of links generated from the SEARCH.
                    print("SECTION 2: Using GoogleSearch Method") # !!!!DEBUGGING!!!!
                    for link in search_results: # For LINK in search_results do the following
                        print(link) # !!!!DEBUGGING!!!!
                        if link.startswith("https://www.imdb.com/title/tt") and link.endswith("/"): # If LINK starts with 'https://www.imdb.com/title/tt' and ends with '/' then continue
                            print(link + "startswith 'https://www.imdb.com/title/tt' and ends with /" ) # !!!!DEBUGGING!!!!
                            #print(links_list+ "this is the link list be fore adding before adding") # !!!!DEBUGGING!!!!
                            if link not in links_list: # If the LINK is NOT in the links_list do the following.
                                print(link + "Is not in the links list" ) # !!!!DEBUGGING!!!!
                                links_list.append(link) # Append LINK to links_list.
                                print(links_list[0]) # !!!!DEBUGGING!!!!
                                movie_imdb_link = links_list[0] # Variable that stores the IMDB link for the IMDB poster and info scrape.
                                print(movie_imdb_link) # !!!!DEBUGGING!!!!
                                return movie_imdb_link
########     SECTION 3:
                    ## IMPORTANT NOTE - options.headless set to False to see the browser being scraped.
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                    options = webdriver.ChromeOptions() # Variable that stores the browser options.
                    options.headless = True # Makes the scraping happen in the back ground.
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

########     SECTION 4:
                    print("SECTION 4: Starting poster and title scrape from IMDB") # !!!!DEBUGGING!!!!
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
                            self.Movie_Poster = f"{Directories().temp+self.Movie_Title}/{self.Movie_Title}.png"
                            shutil.copyfile(self.Movie_Poster, "temp.png")
                            self.Movie_Poster = PhotoImage(file="temp.png") # Variable that stores the poster image location
                            time.sleep(1) #
                            back_ground.config(image=self.Movie_Poster)
                            os.remove("temp.jpg")
                            os.remove("temp.png")

                        else:
                            pass
                    print("SECTION 4: Finished Web Scraping") # !!!!DEBUGGING!!!!
                    browser.quit() # Quit the browser after scraping completes.

                except Exception:
                    print("SECTION 4: Web Scraping Has Failed using IMDB API directly") # !!!!DEBUGGING!!!!
                    pass
                    if disc_title != None:
                        try:
                            movie_data_base = imdb.IMDb() # Creating instance of IMDb as movie data base
                            search1 = movie_data_base.search_movie(disc_title) # Search for movie in the IMDB d
                            year = search1[0]['year'] # Get the year
                            title = (search1[0]['title'].replace(':', '') + " "+ str(year)) # Concatenate the title a
                            self.Movie_Title = title # Returns the movie_title generated by IMDB
                            if self.Movie_Title not in os.listdir(Directories().temp): # If the movie in NOT in the TEMP directory then continue.
                                os.mkdir(Directories().temp+self.Movie_Title) # Create a directory for the movie and all its data that will be scraped.
                            else:
                                pass
                        except IndexError: # if IMDB cant find the movie just use disc/drive information
                            print("IMDB API cant find the movie") # !!!!DEBUGGING!!!!

                            self.Movie_Title = disc_title
                            if self.Movie_Title not in os.listdir(Directories().temp): # 
                                os.mkdir(Directories().temp+self.Movie_Title) # Create a 
                            else:
                                pass
                    else:
                        pass

########     SECTION 5: 
                if self.Movie_Title != None:
                    try:
                        makemkv = MakeMKV(0) # Creating an instance of MakeMKV
                        makemkv.mkv(0, f"{Directories().temp+self.Movie_Title}") # Using MakeMKV top make rip the DVD to the temp directory
                    except Exception:
                        ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                        drive_ready = True
                    try:
                        file_location = f"{Directories().temp+self.Movie_Title}" # The location of the file
                        file_destination = f"{Directories().uncompressed+self.Movie_Title}" # The destination of the files one ripping has completed.
                        shutil.move(file_location, file_destination) # Move the file from the temp directory to the uncompressed directory
                        ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                        drive_ready = True
                        back_ground.config(image=background)
                    except IndexError:
                        pass
                else:
                    pass

########     SECTION 6:
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
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                print(self.Movie_Title+" has finished ripping and is now transcoding.")
                time.sleep(10)
                self.Movie_Poster = None #
                self.Movie_Title = None #
                drive_ready = True
            else:
                self.Movie_Poster = None #
                self.Movie_Title = None #
        else:
            self.Movie_Poster = None #
            self.Movie_Title = None #

def rip_scrape_transcode():

    if drive_ready != False:
        try:
            win32api.GetVolumeInformation("E:/")
            threading.Thread(target=Rip_Scrape_Transcode).start()
            time.sleep(3)
            print("Rip_Scrape_Transcode Thread started") # !!!!DEBUGGING!!!!
        except Exception:
            pass
    else:
        pass

def refresh():
    while True:

        if collection_dir != None:
            for letter in os.listdir(collection_dir):
                for movie in os.listdir(f"{collection_dir}/{letter}"):
                    if movie not in collection:
                        collection.append(movie)
                    else:
                        pass
            if len(collection) != len(testing_listbox.get(0, END)):
                testing_listbox.delete(0, END)
                for letter in os.listdir(collection_dir):
                    for movie in os.listdir(f"{collection_dir}/{letter}"):
                        if movie not in testing_listbox.get(0, END):
                            testing_listbox.insert(END, f" {movie}")
                        else:
                            pass
            else:
                pass
        else:
            pass

        if len(Directories().compressed_list) != len(transcoded_dir_listbox.get(0, END)):
            transcoded_dir_listbox.delete(0, END)
            for i in Directories().compressed_list:
                transcoded_dir_listbox.insert(END, f" {i}")
        
        
        
        
        if len(Directories().temp_list) != 0:
            ripping_status.config(text=f"Ripping : {IMDB_Movie_Title}", fg=pink, font=("Comic Sans MS", 13, "bold"))
        else:
            ripping_status.config(text="Waiting for DVD to Rip...", fg=green, font=("Comic Sans MS", 13, "bold"))

        if len(Directories().transcoding_list) != 0:
            transcoding_status.config(text=f"Transcoding : {Directories().transcoding_list[0]}", fg=pink, font=("Comic Sans MS", 13, "bold"))
        else:
            transcoding_status.config(text="Waiting for Movie to Transcode...", fg=green, font=("Comic Sans MS", 13, "bold"))
        
        
        
        
        
        
        
        
        
        
        if drive_ready != False:
            rip_scrape_transcode()
            
        else:
            time.sleep(2)
        time.sleep(.8) # Wait .8 seconds before continuing.




threading.Thread(target=refresh).start()

root.mainloop()