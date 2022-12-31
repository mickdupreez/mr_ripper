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
    """
    This function is used to rip and transcode DVDs.
    It consists of several sub-functions that perform various tasks,
    such as getting the CD drive, preprocessing strings,
    getting volume and disc information, getting items, and transcoding files.
    """

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

    def get_cd_drive():
        """
        This function tries to find the drive letter of a CD-ROM drive connected to the system.
        If a CD-ROM drive is found, the drive letter is returned as a string.
        If no CD-ROM drive is found, the function returns None.
        """
        try:
            # Get a list of all logical drives on the system
            drives = win32api.GetLogicalDriveStrings()
            # Split the list by the null character and remove the last element
            drives = drives.split('\000')[:-1]
            # Iterate through the list of drives
            for drive in drives:
                # Check if the drive type is a CD-ROM drive
                if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                    # If the drive is a CD-ROM drive, return the drive letter
                    return drive
        except Exception as e:
            # If an exception is thrown, print an error message and return None
            print(f"An error occurred !!!NO DRIVE DETECTED!!!. Please make sure that you have a DVD drive connected to your PC: {e}")
            return None

    def preprocess_string(string):
        """
        This function takes a string as input and preprocesses it in the following way:
        - Removes any 4-digit numbers from the string
        - Removes any non-alphanumeric characters from the string
        - Strips leading and trailing whitespace from the string
        - Converts the string to lowercase
        The processed string is returned as output.
        """
        try:
            # Remove any 4-digit numbers from the string
            string = re.sub(r'\b\d{4}\b', '', string)
            # Remove any non-alphanumeric characters from the string
            string = re.sub(r'[^A-Za-z0-9\s]', '', string)
            # Strip leading and trailing whitespace from the string
            string = string.strip()
            # Convert the string to lowercase
            string = string.lower()
            return string
        except Exception as e:
            # If an exception is thrown, print an error message and return the original string
            print(f"An error occurred while preprocessing the string :{string}:: {e}")
            return string

    def get_volume_information():
        """
        This function tries to get the volume information for a CD-ROM drive connected to the system.
        The volume information is returned as a string.
        If no CD-ROM drive is found or an error occurs, the function returns None.
        """
        try:
            # Get the drive letter of a CD-ROM drive
            drive_letter = get_cd_drive()
            if drive_letter != None:
                # Get the volume information for the CD-ROM drive
                print("Getting volume information")
                volume_info = win32api.GetVolumeInformation(drive_letter)
                
                # Extract the volume label from the volume information tuple
                volume_info = volume_info[0]
                # Replace underscores with spaces in the volume label
                volume_info = volume_info.replace("_", " ")
                
                # Preprocess the volume label
                volume_info = preprocess_string(volume_info)
                print(volume_info)
                return volume_info
            else:
                # If no CD-ROM drive was found, print an error message and return None
                print("ERROR, The 'drive_letter' is None. Please connect a DVD Drive to your PC.")
                return None
        except Exception as e:
            # If an exception is thrown, print an error message and return None
            print(f"An error has occurred, please insert a DVD.: {e}")
            return None

    def get_disc_information():
        """
        This function tries to get information about a DVD inserted in a CD-ROM drive.
        The information is returned as a string.
        If no CD-ROM drive is found or an error occurs, the function returns None.
        """
        try:
            # Get the drive letter of a CD-ROM drive
            drive_letter = get_cd_drive()
            if drive_letter != None:
                # Use the MakeMKV class to get information about the DVD in the CD-ROM drive
                print("Getting disc information")
                disc_information = MakeMKV(drive_letter).info()
                # Extract the disc name from the disc information dictionary
                disc_info = disc_information["disc"]["name"]
                
                # Replace underscores with spaces in the disc name
                disc_info = disc_info.replace("_", " ")
                # Preprocess the disc name
                disc_info = preprocess_string(disc_info)
                print(disc_info)
                return disc_info
            else:
                # If no CD-ROM drive was found, print an error message and return None
                print("ERROR, The 'drive_letter' is None. Please connect a DVD Drive to your PC.")
                return None
        except Exception as e:
            # If an exception is thrown, print an error message and return None
            print(f"An error has occurred, please insert a DVD.: {e}")
            return None

    def get_items():
        """
        This function tries to read a list of movie titles from a file called "movie_titles.txt"
        and returns the list of titles.
        If an error occurs, the function returns None.
        """
        try:
            # Set the name of the file containing the movie titles
            possible_title = "movie_titles.txt"
            # Open the file in read mode with utf-8 encoding
            with codecs.open(possible_title, 'r', encoding='utf-8') as file:
                # Read all lines in the file
                lines = file.readlines()
                # Initialize an empty list to store the movie titles
                items = []
                # Iterate through the lines in the file
                for line in lines:
                    # Split the line by the comma character
                    line_items = line.split(',')
                    # Add the items from the line to the list of movie titles
                    items.extend(line_items)
                # Remove any non-alphanumeric characters from the movie titles
                items = [re.sub(r'[^A-Za-z0-9\s]', '', item) for item in items]
                # Strip leading and trailing whitespace from the movie titles
                items = [item.strip() for item in items]
                return items
        except Exception as e:
            # If an exception is thrown, print an error message and return None
            print(f"An error occurred while reading the file: {e}")
            return None

    def get_movie_title():
        """
        This function attempts to determine the title of a movie from a DVD.
        It does this by extracting the disc information and volume information from the DVD,
        and searching for the best match for these strings in a list of possible movie titles.
        If the best match for either the disc information or the volume information has a match ratio greater than or equal to 0.55,
        the function returns the best match as the movie title.
        If the match ratio for both the disc information and the volume information is less than 0.55,
        the function prints a message, waits for 3 seconds, and returns the volume information as the movie title.
        If an unexpected error occurs, the function prints an error message, waits for 3 seconds,
        and returns the volume information as the movie title.
        """

        try:
            # Get the disc information for the DVD
            disc_info = get_disc_information()
            # Get the volume information for the DVD
            volume_info = get_volume_information()
            # Get the list of possible movie titles
            items = get_items()

            def get_match(string, items):
                """
                This function takes a string and a list of strings as input and returns the string from the list
                that has the highest match ratio with the input string. The match ratio is returned as well.
                """
                # Initialize variables to store the best match and the highest match ratio
                match = None
                max_percent = 0
                # Iterate through the strings in the list
                for item in items:
                    # Calculate the match ratio between the input string and the current string in the list
                    percent = difflib.SequenceMatcher(None, string, item).ratio()
                    # If the match ratio is higher than the current highest, update the best match and the highest match ratio
                    if percent > max_percent:
                        max_percent = percent
                        match = item
                # Return the best match and the highest match ratio
                return match, max_percent

            if disc_info is None or volume_info is None or items is None:
                # If any of the disc information, volume information, or movie title list is None,
                # print an error message and return None
                print("An error occurred while getting disc, volume, or item information")
                return None
            else:
                # Get the best match and the highest match ratio for the disc information
                disc_match, disc_percent = get_match(disc_info, items)
                # Get the best match and the highest match ratio for the volume information
                volume_match, volume_percent = get_match(volume_info, items)
                if disc_percent < 0.55 and volume_percent < 0.55:
                    # If the match ratio for both the disc information and the volume information is less than 0.55,
                    # print a message, wait for 3 seconds, and return the volume information as the movie title
                    print("There are no matches, using the 'volume_info' as the string to search for.")
                    time.sleep(3)
                    return volume_info
                else:
                    # Print the disc information and the match ratio for the disc information
                    print(disc_info, disc_percent)
                    # Print the volume information and the match ratio for the volume information
                    print(volume_info, volume_percent)
                    if disc_percent > volume_percent:
                        # If the match ratio for the disc information is higher than the match ratio for the volume information,
                        # return the best match for the disc information as the movie title
                        return disc_match
                    else:
                        # If the match ratio for the volume information is higher than the match ratio for the disc information,
                        # or if they are equal, return the best match for the volume information as the movie title
                        return volume_match
        except Exception as e:
            # If an unexpected error occurs, print an error message, wait for 3 seconds, and return the volume information as the movie title
            print(f"An unexpected error occurred, using the 'volume_info' as the string to search for. : {e}")
            return volume_info

    def get_movie_links():
        """
        This function is used to get a IMDB link for a movie based on its title.
    
        Returns:
            string: This string is the most likely IMDB movie link.
        """
        try:
            # Get the movie title
            title = get_movie_title()
            if title != None:
                # Replace spaces in the title with plus signs for the Google search query
                query = title.replace(" ", "+")
                # Construct the URL for the Google search
                url = f"https://www.google.com/search?q={query}+site:imdb.com"
                # Set the headers for the HTTP request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
                }
                # Send the HTTP request
                response = requests.get(url, headers=headers)
                # Parse the HTML of the search results page
                soup = BeautifulSoup(response.text, "html.parser")
                # Initialize an empty list to store the IMDb links
                links = []
                # Find all links on the page
                for a in soup.find_all("a", href=True):
                    # Check if the link is an IMDb link for a movie
                    if a["href"].startswith("https://www.imdb.com/title/tt") and re.match(r"\d+/$", a["href"][-6:]):
                        # Add the link to the list
                        links.append(a["href"])
                        # Get the first link in the list
                        link = links[:1]
                # Return the list of IMDb links
                return link
            else:
                # If an unexpected error occurs, print the error message and return None
                print("An error occurred while getting the movie title")
                return None

        except Exception as e:
            # If an unexpected error occurs, print the error message and return None
            print(f"An unexpected error occurred: {e}")
            return None

    def get_movie_data():
        """
        Retrieves data about a movie, including its title and poster image, from IMDb.

        This function first calls the `get_movie_links()` function to get a list of links to IMDb pages for movies
        that match the volume or disc information of the DVD in the drive. It then retrieves the first link in the
        list and uses it to navigate to the IMDb page for the movie using the Chrome browser in headless mode (i.e.,
        without a GUI).

        Next, the function extracts the title of the movie from the page title and cleans it up by removing certain
        characters. It then clicks on an element with the class name "ipc-lockup-overlay__screen" and uses a regular
        expression to find all image tags in the page source. It splits the matches on commas and quotation marks and
        searches for a URL that ends in ".jpg", which it assumes is the URL for the poster image.

        The function then downloads the poster image and resizes it using the `Lanczos` resampling algorithm from the
        `PIL` library. It returns the title and poster image as a tuple.

        Returns:
        tuple: A tuple containing the movie title (str) and poster image (PIL.Image).
        """
        try:
            # Get the movie links from a different function
            link = get_movie_links()
            if link != None:
                # Get the first link in the list of movie links
                movie_imdb_link = link[0]
    
                # Set a user agent string to identify the browser
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    
                # Create options for the Chrome browser
                options = webdriver.ChromeOptions()
                options.headless = False  # Run the browser in headless mode (without a GUI)
                options.add_argument("--silent")  # Suppress logging
                options.add_argument(f'user-agent={user_agent}')  # Set the user agent
                options.add_argument("--window-size=1920,1080")  # Set the window size
                options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
                options.add_argument('--allow-running-insecure-content')  # Allow running insecure content
                options.add_argument("--disable-extensions")  # Disable extensions
                options.add_argument("--proxy-server='direct://'")  # Set the proxy server
                options.add_argument("--proxy-bypass-list=*")  # Set the proxy bypass list
                options.add_argument("--start-maximized")  # Start the browser maximized
                options.add_argument('--disable-gpu')  # Disable GPU acceleration
                options.add_argument('--disable-dev-shm-usage')  # Disable shared memory
                options.add_argument('--no-sandbox')  # Disable the sandbox
    
                # Create a Chrome browser instance with the specified options
                browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
                browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    
                # Navigate to the IMDb page for the movie
                browser.get(movie_imdb_link)
    
                # Get the title of the page and clean it up
                movie_title = (browser.title.replace(") - IMDb", "").replace("(","").replace(":", ""))
                print(movie_title)
    
                # Click on an element with the class name "ipc-lockup-overlay__screen"
                browser.find_element(By.CLASS_NAME, "ipc-lockup-overlay__screen").click()
    
                # Use a regular expression to find all image tags in the page source
                pattern = re.compile(r'<img src="https://m\.media-amazon\.com/images/.+"')
                matches = pattern.findall(browser.page_source)
    
                # Split the matches on commas and then on quotation marks
                matches = str(matches[0]).split(",")
                matches = matches[0].split('"')

                for match in matches:
                    # If the match is a URL that ends in ".jpg"
                    if match.startswith("https") and match.endswith("jpg"):
                        # Set the poster link to the match
                        poster_link = match
                        # Download the image at the poster link and save it as "temp.jpg"
                        urllib.request.urlretrieve(poster_link, "temp.jpg")
                        # Open the image using the Image library from the PIL library
                        poster = Im.open("temp.jpg")
                        # Set the desired height of the poster image
                        poster_hight = 900
                        # Calculate the width of the image based on the desired height
                        hight_percent = (poster_hight / float(poster.size[1]))
                        poster_width = int((float(poster.size[0]) * float(hight_percent)))
                        # Resize the image to the desired dimensions using the Lanczos resampling algorithm
                        poster = poster.resize((poster_width, poster_hight), Im.Resampling.LANCZOS)
                        # Set the movie poster image to the resized image
                        movie_poster = poster
                        # Delete the temporary image file
                        os.remove("temp.jpg")
                        # Quit the Chrome browser
                        browser.quit()
                        # Return the movie title and poster image
                        return movie_title, movie_poster
                else:
                    # If no valid image URL was found, print an error message
                    print(f"An error occurred while getting the link, try again later")
                    # Get the movie title from a different function
                    movie_title = get_movie_title()
                    # Return the movie title and a "None" value for the poster image
                    return movie_title, None
        # Catch any exceptions that may occur
        except Exception as e:
            # Print an error message
            print(f"An error occurred while downloading the movie data from the web, try again later : {e}")
            # Get the movie title from a different function
            movie_title = get_movie_title()
            # Return the movie title and a "None" value for the poster image
            return movie_title, None

    def transcode():
        """
        Transcodes the first MKV file in the 'uncompressed' directory using HandBrakeCLI, moves it to the 'compressed' directory, and removes the uncompressed version of the file.
        This function is intended to be called after the DVD has been ripped and stored in the 'uncompressed' directory.
        """
        try:
            # Sleep for 5 seconds to allow for any file system changes to complete before attempting to transcode
            time.sleep(5)
            # Get the list of files in the 'uncompressed' directory
            uncompressed_list = Directories().uncompressed_list
            
            # If the 'uncompressed' list is empty, raise a ValueError
            if uncompressed_list == []:
                raise ValueError("The uncompressed list is empty")
            # Get the name of the first file in the 'uncompressed' directory
            name = uncompressed_list[0]
            # Create the file path of the directory containing the first file in the 'uncompressed' directory
            dir_location = f"{Directories().uncompressed}{name}"
            
            # If the directory at 'dir_location' is not a valid directory, raise a ValueError
            if not os.path.isdir(dir_location):
                raise ValueError(f"{dir_location} is not a valid directory")
            # Create the file path of the 'transcoding' directory
            dir_destination = f"{Directories().transcoding}"
            # Move the directory containing the first file in the 'uncompressed' directory to the 'transcoding' directory
            shutil.move(dir_location, dir_destination)
            
            # Iterate over the files in the directory containing the first file in the 'uncompressed' directory
            for file in os.listdir(f"{Directories().transcoding}{name}"):
                
                # If the file ends with '.mkv', transcode it using HandBrakeCLI
                if file.endswith(".mkv"):
                    # Get the name of the file
                    file_name = file
                    # Create the file path of the file to be transcoded
                    input_file = f"{Directories().transcoding}{name}/{file_name}"
                    # Create the file path of the transcoded file
                    output_file = f"{Directories().transcoding}{name}/{name}.mkv"
                    # Print the file paths of the file to be transcoded and the transcoded file
                    print(input_file, output_file)
                    # Sleep for 5 seconds to allow for any file system changes to complete before attempting to transcode
                    time.sleep(5)
                    # Create the command to transcode the file using HandBrakeCLI with the 'PLEX' preset and the 'profile.json' file as the import file
                    command  = [
                        "HandBrakeCLI.exe", "--preset-import-file", "profile.json", "-Z", "PLEX",
                        "-i", input_file, "-o",
                        output_file
                    ]
                    # Run the transcode command using the subprocess module
                    subprocess.run(command, shell=True)
                    # Move the directory containing the first file in the 'uncompressed' directory to the 'compressed' directory
                    shutil.move(f"{Directories().transcoding}{name}", f"{Directories().compressed}")
                    # Sleep for 3 seconds to allow for any file system changes to complete before attempting to delete the uncompressed file
                    time.sleep(3)
                    # Create the file path of the uncompressed file
                    uncompressed_file = f"{Directories().compressed}{name}/{file_name}"
                    # Delete the uncompressed file
                    os.remove(uncompressed_file)
                    # Sleep for 2 seconds to allow for any file system changes to complete before returning
                    time.sleep(2)
                    # Return None
                    return None
                
                else:
                    # If the file does not end with '.mkv', do nothing
                    pass
                
        except Exception as e:
            # Print an error message if an exception occurs
            print(f"An error occurred: {e}")

            # Return None
            return None

    def rip():
        """
        This function rips a movie from a DVD. It calls the `get_movie_data` function to get the movie title and movie poster.
        If the movie title is not `None`, the function creates an output directory and saves the movie poster to the output directory.
        The function then uses the `MakeMKV` library to rip the movie to the output directory.
        If an error occurs, the CD-ROM tray is opened and `None` is returned for both the output directory and the movie title.
        """
        try:
            # Get the movie title and movie poster from the `get_movie_data` function
            movie_title, movie_poster = get_movie_data()
            if movie_title != None:
                # Create the output directory and save the movie poster to it
                output_directory = f"{Directories().temp}{movie_title}/"
                os.makedirs(output_directory, exist_ok=True)
                if movie_poster != None:
                    movie_poster.save(f"{output_directory}/{movie_title}.jpg")
                try:
                    # Use the `MakeMKV` library to rip the movie to the output directory
                    makemkv = MakeMKV(0)
                    print("starting RIP")
                    makemkv.mkv(0, output_directory)
                    print("Rip finished")
                    return output_directory, movie_title
                except Exception:
                    # If an error occurs, open the CD-ROM tray
                    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
                    return None, None
            else:
                print("There is no movie Title. You have issues with getting the movie data")
                return None, None
        except Exception as e:
            print(f"There Has been an issue ripping this file, please reinsert the DVD and try again. : {e}")
            return None, None

    def move_and_transcode():
        """
        This function moves and transcodes a movie file. It first calls the `rip` function to rip the movie and get the output directory and movie title.
        If the output directory is not `None`, the function checks the size of the output directory in GB. If the size is greater than 20 GB, the movie is moved to the `uncompressed` directory.
        Otherwise, the movie is moved to the `compressed` directory and the thread `transcode` is started.
        Finally, the CD-ROM tray is opened and the movie title is returned.
        If an error occurs, an error message is printed and `None` is returned.
        """
        try:
            # Call the `rip` function to rip the movie and get the output directory and movie title
            output_directory, movie_title = rip()
            if output_directory != None:
                # Calculate the size of the output directory in GB
                output_directory_size = sum(os.path.getsize(os.path.join(output_directory, f)) for f in os.listdir(output_directory))
                output_directory_size_gb = output_directory_size / (1024 ** 3)
                print(output_directory_size_gb)
                if output_directory_size_gb > 20:
                    # If the size is greater than 20 GB, move the movie to the `uncompressed` directory
                    file_destination =  f"{Directories().uncompressed}"
                else:
                    # Otherwise, move the movie to the `compressed` directory
                    file_destination =  f"{Directories().compressed}"
                    # Rename the movie file to have the movie title
                    for file in os.listdir(f"{Directories().temp}{movie_title}"):
                        if file.endswith('.mkv'):
                            os.rename(f"{Directories().temp}{movie_title}/{file}", f"{Directories().temp}{movie_title}/{movie_title}.mkv")
                        else:
                            pass
                # Move the output directory to the `file_destination`
                shutil.move(output_directory, file_destination)
                # Start the `transcode` thread
                threading.Thread(target=transcode).start()
                # Open the CD-ROM tray
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
                return movie_title
            else:
                print("Error, there is no output directory")
                return None
        except Exception as e:
            print("Error While moving and transcoding file. {e}")
            return None

    # Attempt to get the letter of the DVD drive using the get_cd_drive function
    if get_cd_drive() != None:
        # If the get_disc_information function or the get_volume_information function returns None, print an error message and sleep for 5 seconds
        if get_disc_information() is None or get_volume_information() is None:
            print("Error, Please insert a DVD into the attached DVD drive.")
            time.sleep(5)
        # If both the get_disc_information and get_volume_information functions return a value, call the move_and_transcode function
        else:
            move_and_transcode()
    # If the get_cd_drive function returns None, print an error message and sleep for 5 seconds
    else:
        print("Error, Please attach a DVD drive")
        time.sleep(5)

