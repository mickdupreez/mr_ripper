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
    class Directories:
        """
        A class representing the directories used in the rip_and_transcode function.
        """

        # Constant class variables representing the names of the directories
        compressed = "compressed/"
        plex = "plex/"
        temp = "temp/"
        transcoding = "transcoding/"
        uncompressed = "uncompressed/"

        def __init__(self):
            """
            Initialize the Directories object.

            Creates the directories if they do not exist, and initializes class variables
            representing the contents of each directory as a list.
            """
            # Get the contents of the 'compressed' directory and store it in the 'compressed_list' class variable
            self.compressed_list = self.get_directory_contents(self.compressed)
            # Get the contents of the 'plex' directory and store it in the 'plex_list' class variable
            self.plex_list = self.get_directory_contents(self.plex)
            # Get the contents of the 'temp' directory and store it in the 'temp_list' class variable
            self.temp_list = self.get_directory_contents(self.temp)
            # Get the contents of the 'transcoding' directory and store it in the 'transcoding_list' class variable
            self.transcoding_list = self.get_directory_contents(self.transcoding)
            # Get the contents of the 'uncompressed' directory and store it in the 'uncompressed_list' class variable
            self.uncompressed_list = self.get_directory_contents(self.uncompressed)

            # A list of all the directories
            self.directories = [
                self.compressed,
                self.plex,
                self.temp,
                self.transcoding,
                self.uncompressed
            ]

        def get_directory_contents(self, directory):
            """
            Get the contents of a directory as a list.

            If the directory does not exist, create it.

            Parameters:
            - directory (str): The name of the directory.

            Returns:
            - list: A list of the contents of the directory.
            """
            # Check if the directory exists. If it does not, create it.
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Return the contents of the directory as a list
            return os.listdir(directory)

    def get_items():
        """
        Get the items in the 'movie_titles.txt' file.

        Returns:
        - list: A list of the items in the file.
        """
        # The file containing the movie titles
        possible_title = "movie_titles.txt"
        # Open the file in read mode with the utf-8 encoding
        with codecs.open(possible_title, 'r', encoding='utf-8') as file:
            # Read in all the lines of the file
            lines = file.readlines()
            # Initialize an empty list to store the items
            items = []
            # For each line in the file
            for line in lines:
                # Split the line by the ',' character and store the resulting list in 'line_items'
                line_items = line.split(',')
                # Add the items in 'line_items' to the 'items' list
                items.extend(line_items)
        # Remove any non-alphanumeric characters (except for whitespace) from the items
        items = [re.sub(r'[^A-Za-z0-9\s]', '', item) for item in items]
        # Strip leading and trailing whitespace from the items
        items = [item.strip() for item in items]
        # Return the list of items
        return items

    def get_cd_drive():
        """
        Get the letter of the CD-ROM drive on the system.

        Returns:
        - str: The letter of the CD-ROM drive.
        """
        # Get a list of all the logical drive strings on the system
        drives = win32api.GetLogicalDriveStrings()
        # Split the list by the null character and remove the last element (which is an empty string)
        drives = drives.split('\000')[:-1]
        # For each drive in the list
        for drive in drives:
            # If the drive is a CD-ROM drive
            if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                # Return the drive letter
                return drive

    def preprocess_string(string):
        """
        Preprocess a string by removing any digits and non-alphanumeric characters (except for whitespace),
        and lowercasing the string.

        Parameters:
        - string (str): The string to preprocess.

        Returns:
        - str: The preprocessed string.
        """
        # Remove any 4-digit numbers from the string
        string = re.sub(r'\b\d{4}\b', '', string)
        # Remove any non-alphanumeric characters (except for whitespace) from the string
        string = re.sub(r'[^A-Za-z0-9\s]', '', string)
        # Strip leading and trailing whitespace from the string and lowercase it
        string = string.strip().lower()
        # Return the preprocessed string
        return string

    def get_volume_information():
        """
        Get the volume information of the CD-ROM drive on the system.

        Returns:
        - str: The volume information of the CD-ROM drive.
        """
        # Get the letter of the CD-ROM drive on the system
        drive_letter = get_cd_drive()
        try:
            # Get the volume information for the CD-ROM drive
            volume_info = win32api.GetVolumeInformation(drive_letter)
            # The volume information is a tuple, where the first element is the volume name
            volume_info = volume_info[0]
            # Replace any underscores in the volume name with spaces
            volume_info = volume_info.replace("_", " ")
            # Preprocess the volume name
            volume_info = preprocess_string(volume_info)
            # Return the volume name
            return volume_info

        except Exception:
            # If an exception occurs, print a message and return None
            print("The CD/DVD drive is not ready.")
            return None

    def get_disc_information():
        """
        Get the disc information of the CD-ROM drive on the system.

        Returns:
        - str: The disc information of the CD-ROM drive.
        """
        # Get the letter of the CD-ROM drive on the system
        drive_letter = get_cd_drive()
        try:
            # Get the disc information for the CD-ROM drive
            disc_information = MakeMKV(drive_letter).info()
            # The disc information is a dictionary, where the 'name' key contains the name of the disc
            disc_info = disc_information["disc"]["name"]
            # Replace any underscores in the disc name with spaces
            disc_info = disc_info.replace("_", " ")
            # Preprocess the disc name
            disc_info = preprocess_string(disc_info)
            # Return the disc name
            return disc_info

        except Exception:
            # If an exception occurs, print a message and return None
            print("The CD/DVD drive is not ready.")
            return None


        except Exception:
            print("The CD/DVD drive is not ready.")
            return None

    def get_movie_title(
        disc_info=get_disc_information(),
        volume_info=get_volume_information(),
        items=get_items()
        ):
        """
        Get the title of a movie on the CD-ROM drive, by comparing the disc and volume information to a list of possible titles.

        Parameters:
        - disc_info (str): The disc information of the CD-ROM drive.
        - volume_info (str): The volume information of the CD-ROM drive.
        - items (list): A list of possible movie titles.

        Returns:
        - str: The title of the movie.
        """
        def get_match(string, items):
            """
            Get the best matching string from a list of items, based on string similarity.

            Parameters:
            - string (str): The string to compare to the items.
            - items (list): The list of items to compare to the string.

            Returns:
            - tuple: A tuple containing the best matching item and the similarity score.
            """
            match = None
            max_percent = 0
            # For each item in the list
            for item in items:
                # Calculate the string similarity between 'string' and 'item'
                percent = difflib.SequenceMatcher(None, string, item).ratio()
                # If the similarity score is higher than the previous maximum
                if percent > max_percent:
                    # Update the maximum similarity score and the best matching item
                    max_percent = percent
                    match = item
            # Return the best matching item and the similarity score
            return match, max_percent

        # Get the best matching item and the similarity score for the disc information
        disc_match, disc_percent = get_match(disc_info, items)
        # Get the best matching item and the similarity score for the volume information
        volume_match, volume_percent = get_match(volume_info, items)
        # If the disc information has a higher similarity score than the volume information
        if disc_percent > volume_percent:
            # Return the best matching item for the disc information
            return disc_match
        else:
            # Return the best matching item for the volume information
            return volume_match

    def get_movie_links():
        """
        Get the IMDb link(s) for a movie, based on its title.

        Returns:
        - list: A list of IMDb links for the movie.
        """
        # Get the title of the movie
        title = get_movie_title()
        # Replace any spaces in the title with plus signs
        query = title.replace(" ", "+")
        # Construct a Google search URL for the movie title on IMDb
        url = f"https://www.google.com/search?q={query}+site:imdb.com"
        # Set the user agent for the request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        # Send the request to Google
        response = requests.get(url, headers=headers)
        # Parse the response HTML
        soup = BeautifulSoup(response.text, "html.parser")
        # Initialize an empty list for the IMDb links
        links = []
        # For each link in the HTML
        for a in soup.find_all("a", href=True):
            # If the link is an IMDb link for a movie (as indicated by the URL structure and the presence of the "tt" prefix)
            if a["href"].startswith("https://www.imdb.com/title/tt") and re.match(r"\d+/$", a["href"][-6:]):
                # Add the link to the list
                links.append(a["href"])
        # Return the first link in the list
        return links[:1]

    def get_movie_data():
        """
        Get data for a movie from IMDb.

        Returns:
        - str: The movie title.
        - list: A list of image URLs for the movie.
        """
        # Get the IMDb link for the movie
        link = get_movie_links()
        # Get the first link in the list (there should only be one)
        movie_imdb_link = link[0]
        # Set the user agent for the request
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        # Set options for the Chrome webdriver
        options = webdriver.ChromeOptions()
        # `headless` option is used to run the browser in headless mode
        options.headless = True
        # `silent` option is used to prevent the browser from printing logging messages to the consol
        options.add_argument("--silent")
        # `user-agent` option is used to specify the user agent string that will be sent to the web server
        options.add_argument(f'user-agent={user_agent}')
        # `window-size` option is used to set the size of the browser window
        options.add_argument("--window-size=1920,1080")
        # `ignore-certificate-errors` option is used to ignore SSL certificate errors
        options.add_argument('--ignore-certificate-errors')
        # `allow-running-insecure-content` option is used to allow the browser to run insecure content
        options.add_argument('--allow-running-insecure-content')
        # `disable-extensions` option is used to disable extensions
        options.add_argument("--disable-extensions")
        # `proxy-server` option is used to specify a proxy server to use
        options.add_argument("--proxy-server='direct://'")
        # `proxy-bypass-list` option is used to specify a list of servers that should be accessed directly, bypassing the proxy
        options.add_argument("--proxy-bypass-list=*")
        # `start-maximized` option is used to start the browser maximized
        options.add_argument("--start-maximized")
        # `disable-gpu` option is used to disable the GPU in the browser
        options.add_argument('--disable-gpu')
        # `disable-dev-shm-usage` option is used to disable the use of /dev/shm
        options.add_argument('--disable-dev-shm-usage')
        # `no-sandbox` option is used to disable the sandbox mode in the browser
        options.add_argument('--no-sandbox')
        # Create a webdriver instance with the options
        browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        # Open the IMDb page for the movie
        browser.get(movie_imdb_link)
        # Get the title of the movie from the page title
        movie_title = (browser.title.replace(") - IMDb", "").replace("(","").replace(":", ""))
        # Print the movie title
        print(movie_title)
        # Click the "play" button on the page to load the images
        browser.find_element(By.CLASS_NAME, "ipc-lockup-overlay__screen").click()
        # Use a regular expression to find image URLs in the page source
        pattern = re.compile(r'<img src="https://m\.media-amazon\.com/images/.+"')
        # Find all matches in the page source
        matches = pattern.findall(browser.page_source)
        # Split the matches into a list
        matches = str(matches[0]).split(",")
        # Split the first match into a list of strings
        matches = matches[0].split('"')
        # Iterate over the list of matches
        for match in matches:
            # If the match starts with 'https' and ends with 'jpg', we found the image link
            if match.startswith("https") and match.endswith("jpg"):
                # Assign the image link to the poster_link variable
                poster_link = match
                # Download the image from the link and save it to the 'temp.jpg' file
                urllib.request.urlretrieve(poster_link, "temp.jpg")
                # Open the image file using the PIL library
                poster = Im.open("temp.jpg")
                # Set the desired height of the poster
                poster_hight = 900
                # Calculate the percentage of the height relative to the original size of the image
                hight_percent = (poster_hight / float(poster.size[1]))
                # Calculate the width of the image based on the desired height and the aspect ratio of the original image
                poster_width = int((float(poster.size[0]) * float(hight_percent)))
                # Resize the image using the LANCZOS resampling method
                poster = poster.resize((poster_width, poster_hight), Im.Resampling.LANCZOS)
                # Assign the resized image to the movie_poster variable
                movie_poster = poster
                # Delete the 'temp.jpg' file
                os.remove("temp.jpg")
                # Quit the browser
                browser.quit()
                # Return the title and poster of the movie
                return movie_title, movie_poster

    def transcode():
        """
        Transcodes the first video file in the 'uncompressed' directory using the HandBrakeCLI tool.
        The video file is first moved from the 'uncompressed' directory to the 'transcoding' directory.
        Then, the HandBrakeCLI tool is called with the necessary command line arguments to transcode the 
        video file using the 'PLEX' preset specified in the 'profile.json' file. The transcoded video
        file is saved in the 'transcoding' directory with the same name as the original video file.
        """
        time.sleep(5)
        # Get the list of files in the 'uncompressed' directory
        uncompressed_list = Directories().uncompressed_list
        # If the 'uncompressed' directory is not empty
        if uncompressed_list != []:
            # Get the name of the first file in the 'uncompressed' directory
            name = uncompressed_list[0]
            # Create the source and destination paths for the file
            dir_location = f"{Directories().uncompressed}{name}"
            dir_destination = f"{Directories().transcoding}"
            # Move the file from the 'uncompressed' directory to the 'transcoding' directory
            shutil.move(dir_location, dir_destination)
            # Iterate through the files in the 'transcoding' directory
            for file in os.listdir(f"{Directories().transcoding}{name}"):
                # If the file is a .mkv file
                if file.endswith(".mkv"):
                    # Set the file name and input/output file paths for the transcode command
                    file_name = file
                    input_file = f"{Directories().transcoding}{name}/{file_name}"
                    output_file = f"{Directories().transcoding}{name}/{name}.mkv"
                    print(input_file, output_file)
                    time.sleep(5)
                    # Create the transcode command using the HandBrakeCLI tool and necessary arguments
                    command  = [
                        "HandBrakeCLI.exe", "--preset-import-file", "profile.json", "-Z", "PLEX",
                        "-i", input_file, "-o",
                        output_file
                    ]
                    # Run the transcode command using the subprocess module
                    subprocess.run(command, shell=True)
                else:
                    pass
        else:
            pass

    def rip():
        """
        This function rips the movie from the CD/DVD drive and saves it in the 'temp' directory.
        It also saves the movie poster in the same directory.
        """
        # Get the movie title and poster from the get_movie_data function
        movie_title, movie_poster = get_movie_data()
        # If the movie title is not found, print an error message
        if movie_title == None:
            print("Error: There is no movie Title.")
        else:
            # Create the output directory in the 'temp' directory with the movie title as the name
            output_directory = f"{Directories().temp}{movie_title}/"
            # Create the directory if it does not exist, if it does exist, do nothing
            os.makedirs(output_directory, exist_ok=True)
            # Save the movie poster in the output directory
            movie_poster.save(f"{output_directory}/{movie_title}.jpg")
            try:
                # Create an instance of the MakeMKV class for the CD/DVD drive
                makemkv = MakeMKV(0)
                print("starting RIP")
                # Call the mkv method on the MakeMKV instance to rip the movie
                makemkv.mkv(0, output_directory)
                print("Rip finished")
            except Exception:
                # Open the CD/DVD drive if an exception occurs
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
        # Return the output directory and movie title
        return output_directory, movie_title

    def move_and_transcode():
        """
        Moves the output directory to either the uncompressed or compressed directory, depending on the size of the directory.
        If the size is larger than 20GB, the directory is moved to the uncompressed directory. If it is smaller, it is moved
        to the compressed directory and is also renamed to match the movie title.
        """
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



while True:
    rip_and_transcode()