
from makemkv import MakeMKV, ProgressParser
import time
import ctypes
import os
import subprocess
import shutil
import platform
import imdb
from tkinter import *
import win32api
import threading
from datetime import datetime
from tkinter import filedialog

"""
    Possibly look at searching the title of the disc with googlesearch api first before passing it to title to the imdb
    api. This might help with false positives for movie names.
    
    TO DO:
    make completed list clickable to check for failed rips
    then move to collection
    
    add web scraping ability to pull all movie data from IMDB like movie poster, description, directors, actors...
    use poster as GUI background.
    
    
"""



root = Tk()
root.title("Mr Ripper")
root.iconbitmap("icon.ico")
root.geometry("1901x1100")
root.resizable(False, False)
global switch_is_off
global stop_thread
global collection_dir
global collection
collection = []
collection_dir = None
stop_thread = threading.Event()
switch_is_off = True
off = PhotoImage(file="start_button.png")
on = PhotoImage(file="stop_button.png")


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
        

class Disc_In_Tray:
    def __init__(self):
        directories = Directories()
        self.temp = directories.temp
        self.uncompressed = directories.uncompressed
        
        try:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%y/%H:%M")
            disc_title = win32api.GetVolumeInformation("E:/")
            if disc_title == ('LOGICAL_VOLUME_ID', 923871448, 254, 21758471, 'UDF'):
                today = dt_string
                disc_title = (f"No Title {today}", 923871448, 254, 21758471, 'UDF')
                movie_title = disc_title[0]
            else:
                movie_title = disc_title[0]
        except Exception:
            movie_title = "No Disc!"
        self.movie_title = movie_title
        if self.movie_title != "No Disc!":
            if self.movie_title[:8] != "No Title":
                try:
                    movie_data_base = imdb.IMDb() # Creating instance of IMDb as movie data base
                    search = movie_data_base.search_movie(movie_title) # Search for movie in the IMDB d
                    year = search[0]['year'] # Get the year
                    title = (search[0]['title'].replace(':', '') + " "+ str(year)) # Concatenate the title a
                    self.movie_title = title # Returns the movie_title generated by IMDB
                except IndexError: # if IMDB cant find the movie just use disc/drive information
                    print("IMDB cant find the movie")
                    self.movie_title = movie_title
        else:
            pass
        
    def rip(self):
        while switch_is_off == False:
            try:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%y/%H:%M")
                disc_title = win32api.GetVolumeInformation("E:/")
                if disc_title == ('LOGICAL_VOLUME_ID', 923871448, 254, 21758471, 'UDF'):
                    today = dt_string
                    disc_title = (f"No Title {today}", 923871448, 254, 21758471, 'UDF')
                    movie_title = disc_title[0]
                else:
                    movie_title = disc_title[0]
            except Exception:
                movie_title = "No Disc!"
            self.movie_title = movie_title
            if self.movie_title != "No Disc!":
                if self.movie_title[:8] != "No Title":
                    try:
                        movie_data_base = imdb.IMDb() # Creating instance of IMDb as movie data base
                        search = movie_data_base.search_movie(movie_title) # Search for movie in the IMDB d
                        year = search[0]['year'] # Get the year
                        title = (search[0]['title'].replace(':', '') + " "+ str(year)) # Concatenate the title a
                        self.movie_title = title # Returns the movie_title generated by IMDB
                    except IndexError: # if IMDB cant find the movie just use disc/drive information
                        print("IMDB cant find the movie")
                        self.movie_title = movie_title
            else:
                pass
            global stop_thread
            if stop_thread.is_set():
                break
            if self.movie_title != "No Disc!":
            #try: # Try to rip the correct video and audio files from the DVD
                directory = os.listdir(self.temp)
                #print(f"{self.temp}{directory[0]}")
                
                try:
                    #with ProgressParser() as progress:
                    makemkv = MakeMKV(0)#, progress_handler=progress.parse_progress) # Creating an instance of MakeMKV
                    makemkv.mkv(0, self.temp) # Using MakeMKV top make rip the DVD to the temp directory
                except Exception:
                    print("Error reading disc")
                    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                try:
                    directory = os.listdir(self.temp) # Make a list of files in the temp directory
                    file_location = f"{self.temp}{directory[0]}" # The location of the file
                    os.mkdir(f"{self.uncompressed}{self.movie_title}") # Create a directory for the .mkv file
                    file_destination = f"{self.uncompressed}{self.movie_title}/{self.movie_title}U.mkv" # The Destination of the ripped .mkv file
                    os.replace(file_location, file_destination) # Move the file from the temp directory to the uncompressed directory
                    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray
                except IndexError:
                    print("Error no file to move")
            else:
                print("Error no disc")
                time.sleep(3) # Sleep for 3 seconds
                pass

class Transcode_And_Move:
    def __init__(self):
        directories = Directories()
        self.compressed = directories.compressed        
        self.transcoding = directories.transcoding
        self.uncompressed = directories.uncompressed

    def transcode(self):
        while switch_is_off == False:
            directories = Directories()
            self.compressed = directories.compressed    
            self.transcoding = directories.transcoding
            self.uncompressed = directories.uncompressed
            global stop_thread
            if stop_thread.is_set():
                break
            uncompressed_list = os.listdir(self.uncompressed) # Make a list of all files in the uncompressed directory.
            if uncompressed_list != []: # If list is not empty then continue.
                movie_directory = uncompressed_list[0] # The movie directory is the directory in the list.
                transcoding_dir = os.listdir(self.transcoding) # Make a list of all files in the transcoding directory.
                try:

                    if movie_directory not in transcoding_dir: # Check directory does not exists in the transcoding directory.
                            shutil.move(f"{self.uncompressed}{movie_directory}", # If the file does not exist then move the 
                                        f"{self.transcoding}{movie_directory}") # Target directory to the transcoding directory.
                            time.sleep(5) # Wait 5 seconds before continuing.
                    else: # If directory already exists in the transcoding directory
                        shutil.rmtree(f"{self.transcoding}{movie_directory}") # Remove old directory.
                        shutil.move(f"{self.uncompressed}{movie_directory}", # Move the new directory to the transcoding directory.
                                    f"{self.transcoding}{movie_directory}") 
                        time.sleep(5) # Wait 5 seconds before continuing.
                except shutil.Error:
                    time.sleep(5) # Wait 5 seconds before continuing
                    if movie_directory not in transcoding_dir: # Check directory does not exists in the transcoding directory.
                            shutil.move(f"{self.uncompressed}{movie_directory}", # If the file does not exist then move the 
                                        f"{self.transcoding}{movie_directory}") # Target directory to the transcoding directory.
                            time.sleep(5) # Wait 5 seconds before continuing.
                    else: # If directory already exists in the transcoding directory
                        shutil.rmtree(f"{self.transcoding}{movie_directory}") # Remove old directory.
                        shutil.move(f"{self.uncompressed}{movie_directory}", # Move the new directory to the transcoding directory.
                                    f"{self.transcoding}{movie_directory}") 
                        time.sleep(5) # Wait 5 seconds before continuing.

                file_dir = os.listdir(f"{self.transcoding}{movie_directory}") # Make a list of all files in the movie directory
                file = file_dir[0] # The file to be transcoded is the first file in the list.
                import_prest_file ="--preset-import-file" # An argument for the handbrake command
                select_profile = "-Z" # An argument for the handbrake command
                check_os = platform.platform() # Check system OS to select profile and CPU
                input_file = "-i" # An argument for the handbrake command
                uncompressed_file = f"{self.transcoding}{movie_directory}/{file}" # An argument for the handbrake command.
                output_file = "-o" # An argument for the handbrake command.
                compressed_file = f"{self.transcoding}{movie_directory}/{file[:-5]}.mkv" # An argument for the handbrake command.
                if check_os[0:3] == "mac": # Mac only.
                    command = "HandBrakeCLI" # An argument for the handbrake command.
                    preset_file = "M1.json" # An argument for the handbrake command.
                    profile = "M1" # An argument for the handbrake command.
                    subprocess.run( # This is where the all the arguments are passed to handbrake to transcode the file.
                        [ # This is a list of the arguments for the handbrake command.
                        f"{command} {import_prest_file} {preset_file} {select_profile} {profile} {input_file} {uncompressed_file} {output_file} {compressed_file}"
                        ],
                        shell=True, # Use the shell.
                        stdout=subprocess.DEVNULL, # Send output to DEVNULL.
                        stderr=subprocess.DEVNULL # Send errors to DEVNULL.
                        )
                elif check_os[0:3] == "Win": # Windows only
                    command = "HandBrakeCLI.exe" # An argument for the handbrake command.
                    preset_file = "profile.json" # An argument for the handbrake command.
                    profile = "PLEX" # An argument for the handbrake command.
                    command  = [ # This is a list of the arguments for the handbrake command.
                        command, import_prest_file, preset_file, profile, profile,
                        input_file, uncompressed_file, output_file, compressed_file
                    ]
                    subprocess.run( # This is where the all the arguments are passed to handbrake to transcode the file.
                        command, # The list of commands.
                        shell=True, # Use the shell.
                        stdout=subprocess.DEVNULL, # Send output to DEVNULL.
                        stderr=subprocess.DEVNULL # Send errors to DEVNULL.
                        )
                os.remove(f"{self.transcoding}{movie_directory}/{file}") # Remove the uncompressed file
                shutil.move(f"{self.transcoding}{movie_directory}", f"{self.compressed}{movie_directory}") # Move the movie directory to the compressed directory.
                uncompressed_list.pop(0)
            else: # if no file in uncompressed directory then wait for a file
                time.sleep(5) # Wait 5 seconds before continuing.
                pass

def movie_collection():
    global collection_dir
    collection_dir = filedialog.askdirectory()
    
    return collection_dir



completed = """

Completed
Movies:
"""
button_text = """Auto Rip and Transcode the Movie
Click the Button to START or STOP """

instructions = """
Click the Movies
in this list
to check if the
transcode was
successful.
"""
intro = """     Welcome to Mr Ripper's Movie Ripper.
    This Program will Automatically Rip and
    Transcode and Blu-Ray or DVD Movie then
    add it to your media collection.


Mr Ripper Beta release 0.0.5

"""



background = PhotoImage(file="background.png")
back_ground = Label(image=background)
back_ground.place(x=0, y=0, relwidth=1, relheight=1)

ui_frame = LabelFrame(root, text="...Loading...", bg="#44424d", font=("Comic Sans MS",18, "bold"), padx=10, pady=10, fg="#e96163")
ui_frame.place(x=2, y=2, width=450, height=900)
intro_label = Label(ui_frame, text=intro, width=0, bg="#44424d", fg="#e96163", font=("Comic Sans MS", 13, "bold"))
intro_label.place(x=0, y=0)


ui2_frame = LabelFrame(root, text="Movie Collection", bg="#44424d", font=("Comic Sans MS",18, "bold"), padx=10, pady=10, fg="#e96163")
ui2_frame.place(x=1110, y=2, width=450, height=900)
testing_listbox = Listbox(ui2_frame, bg="#44424d", fg="#e96163", width=47, height=20, bd=0, font=("Comic Sans MS", 11))
testing_listbox.place(x=1, y=404)

testing_select_dir_button = Button(ui2_frame, text="Select Directory", command=movie_collection)
testing_select_dir_button.place(x=1, y=1)


ripping_dir_label = Label(ui_frame, text="Preparing...", width=0, bg="#44424d", fg="#e96163", font=("Comic Sans MS",12, "bold"))
ripping_dir_label.place(x=0, y=300)
ripping_dir_listbox = Listbox(ui_frame, bg="#44424d", fg="#e96163", width=35, height=1, bd=0, font=("Comic Sans MS", 11))
ripping_dir_listbox.place(x=110, y=300)

ripped_dir_label = Label(ui_frame, text="In the Que", width=0, bg="#44424d", fg="#e96163", font=("Comic Sans MS",12, "bold"))
ripped_dir_label.place(x=0, y=340)
ripped_dir_listbox = Listbox(ui_frame, bg="#44424d", fg="#e96163", width=35, height=3, bd=0, font=("Comic Sans MS", 11))
ripped_dir_listbox.place(x=110, y=322)

transcoding_dir_label = Label(ui_frame, text="Working...", width=0, bg="#44424d", fg="#e96163", font=("Comic Sans MS",12, "bold"))
transcoding_dir_label.place(x=0, y=380)
transcoding_dir_listbox = Listbox(ui_frame, bg="#44424d", fg="#e96163", width=35, height=1, bd=0, font=("Comic Sans MS", 11))
transcoding_dir_listbox.place(x=110, y=382)

transcoded_dir_label = Label(ui_frame, text=completed, width=0, bg="#44424d", fg="#e96163", font=("Comic Sans MS",12, "bold"))
transcoded_dir_label.place(x=0, y=404)
transcoded_instructions_label = Label(ui_frame, text=instructions,  bg="#44424d", fg="#e96163", font=("Comic Sans MS",10))
transcoded_instructions_label.place(x=0, y=544)

transcoded_dir_listbox = Listbox(ui_frame, bg="#44424d", fg="#e96163", width=35, height=20, bd=0, font=("Comic Sans MS", 11))
transcoded_dir_listbox.place(x=110, y=404)

class Window_Refresh:
    
    def __init__(self):
        pass
        #self.Dir = Directories()
        #self.disc_info = Disc_In_Tray()

    def re_fresh(self):   
        
        while True:
            self.Dir = Directories()
            self.disc_info = Disc_In_Tray()
            if self.disc_info != False:
                ui_frame.config(text=self.disc_info.movie_title)
            else:
                ui_frame.config(text="Waiting for A Disc")

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

            transcoded_dir_length = len(self.Dir.compressed_list)
            transcoded_dir_listbox_length = len(transcoded_dir_listbox.get(0, END))
            if transcoded_dir_length != transcoded_dir_listbox_length:
                transcoded_dir_listbox.delete(0, END)
                for i in self.Dir.compressed_list:
                    transcoded_dir_listbox.insert(END, f" {i}")
            else:
                pass
            transcoding_dir_length = len(self.Dir.transcoding_list)
            transcoding_dir_listbox_length = len(transcoding_dir_listbox.get(0, END))
            if transcoding_dir_length != transcoding_dir_listbox_length:
                transcoding_dir_listbox.delete(0, END)
                for i in self.Dir.transcoding_list:
                    transcoding_dir_listbox.insert(END, f" {i}")
            else:
                pass
            ripped_dir_length = len(self.Dir.uncompressed_list)
            ripped_dir_listbox_length = len(ripped_dir_listbox.get(0, END))
            if ripped_dir_length != ripped_dir_listbox_length:
                ripped_dir_listbox.delete(0, END)
                for i in self.Dir.uncompressed_list:
                    ripped_dir_listbox.insert(END, f" {i}")
            else:
                pass
            ripping_dir_length = len(self.Dir.temp_list)
            ripping_dir_listbox_length = len(ripping_dir_listbox.get(0, END))
            if ripping_dir_length != ripping_dir_listbox_length:
                ripping_dir_listbox.delete(0, END)
                for i in self.Dir.temp_list:
                    ripping_dir_listbox.insert(END, f" {i}")
            else:
                pass
            time.sleep(.8) # Wait .8 seconds before continuing.



def reaper():
    disc_in_tray = Disc_In_Tray()
    transcode_and_move = Transcode_And_Move()
    threading.Thread(target=disc_in_tray.rip).start()
    threading.Thread(target=transcode_and_move.transcode).start()

def switch():
    global switch_is_off
    global stop_thread
    if switch_is_off:
        stop_thread = threading.Event()
        start_button.config(image=on)
        switch_is_off = False
        reaper()

    else:
        start_button.config(image=off)
        switch_is_off = True
        stop_thread.set()
        ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) # Open the disc tray

button_label = Label(ui_frame, text=button_text, width=0, bg="#44424d", fg="#e96163", font=("Comic Sans MS", 15, "bold"))
button_label.place(x=0, y=230)
start_button = Button(ui_frame, bg="#44424d",image=off, command=switch, bd=0, activebackground="#44424d")
start_button.place(x=372, y=230)

refresh = Window_Refresh()
threading.Thread(target=refresh.re_fresh).start()


root.mainloop()