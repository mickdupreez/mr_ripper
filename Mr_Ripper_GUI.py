import customtkinter
import tkinter
from tkinter import *
from Directories import Directories
import os
from PIL import Image
import threading
import time
from PIL import Image
from tkvideo import TkVideo
from moviepy.editor import VideoFileClip

GREAY1 = "#282A36"
GREAY2 = "#44475A"
NAVY = "#6272A4"
BLUE = "#8BE9FD"
GREEN = "#50FA7B"
ORANGE = "#FFB86C"
PINK = "#FF79C6"
PURPLE = "#BD93F9"
RED = "#FF5555"
YELLOW = "#F1FA8C"


def GUI():
    class Mr_Ripper_GUI(customtkinter.CTk):
        def __init__(self):

            super().__init__()

            self.geometry(f"{1500}x{1000}")
            self.title("https://github.com/mickdupreez/mr_ripper")
            self.Left_UI_Main_Frame()
            self.Middle_UI_Main_Frame()
            self.Right_UI_Main_Frame()

        def Left_UI_Main_Frame(self):

            main_frame_left = customtkinter.CTkFrame(
                master=self,
                width=490,
                height=990,
                corner_radius=15,
                fg_color="#FF5555",
            )
            main_frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            ripping_frame = customtkinter.CTkFrame(
                master=main_frame_left,
                width=480,
                height=485,
                corner_radius=15,
                fg_color="#282A36",
            )
            ripping_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            ripping_frame_title = customtkinter.CTkLabel(
                master=ripping_frame,
                width=470,
                height=28,
                text="--------------RIPPING BAYS--------------",
                font=("Comic Sans MS", 18, "bold"),
                corner_radius=15,
                fg_color="#50fa7b",
                text_color="#282A36",
            )
            ripping_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            transcoding_frame = customtkinter.CTkFrame(
                master=main_frame_left,
                width=480,
                height=485,
                corner_radius=15,
                fg_color="#282A36",
            )
            transcoding_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            transcoding_frame_title = customtkinter.CTkLabel(
                master=transcoding_frame,
                width=470,
                height=28,
                text="----------TRANSCODING SLOTS----------",
                font=("Comic Sans MS", 18, "bold"),
                corner_radius=15,
                fg_color="#50fa7b",
                text_color="#44475a",
            )
            transcoding_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            def Riping_Bays_And_Transcoding_Slots():
                def Bay_and_Slot_Maker(number, frame):

                    bay_or_slot_frame = customtkinter.CTkFrame(
                        master=frame,
                        width=470,
                        height=141,
                        corner_radius=15,
                        fg_color="#FF5555",
                    )
                    bay_or_slot_frame.grid(
                        row=number, column=0, padx=5, pady=5, sticky="nsew"
                    )

                    def Bay_or_Slot_Info():
                        bay_or_slot_info = customtkinter.CTkFrame(
                            master=bay_or_slot_frame,
                            width=370,
                            height=131,
                            corner_radius=15,
                            fg_color="#282A36",
                        )
                        bay_or_slot_info.grid(
                            row=0, column=0, padx=5, pady=5, sticky="nsew"
                        )
                        bay_or_slot_info_title = customtkinter.CTkLabel(
                            master=bay_or_slot_info,
                            width=360,
                            height=33,
                            text="",
                            font=("Comic Sans MS", 13, "bold"),
                            corner_radius=15,
                            fg_color="#282a36",
                        )
                        bay_or_slot_info_title.grid(
                            row=0, column=0, padx=5, pady=5, sticky="nsew"
                        )
                        bay_or_slot_info_drive = customtkinter.CTkLabel(
                            master=bay_or_slot_info,
                            width=360,
                            height=33,
                            text="",
                            font=("Comic Sans MS", 13, "bold"),
                            corner_radius=15,
                            fg_color="#282a36",
                        )
                        bay_or_slot_info_drive.grid(
                            row=1, column=0, padx=5, pady=5, sticky="nsew"
                        )
                        bay_or_slot_info_size = customtkinter.CTkLabel(
                            master=bay_or_slot_info,
                            width=360,
                            height=33,
                            text="",
                            font=("Comic Sans MS", 13, "bold"),
                            corner_radius=15,
                            fg_color="#282A36",
                        )
                        bay_or_slot_info_size.grid(
                            row=2, column=0, padx=5, pady=5, sticky="nsew"
                        )
                        bay_or_slot_info_poster_main = customtkinter.CTkFrame(
                            master=bay_or_slot_frame,
                            width=85,
                            height=131,
                            corner_radius=15,
                            fg_color="#44475a",
                        )
                        bay_or_slot_info_poster = customtkinter.CTkLabel(
                            master=bay_or_slot_frame,
                            width=75,
                            height=114,
                            text="",
                            image=customtkinter.CTkImage(
                                dark_image=Image.open("default.png"),
                                size=(75, 114),
                            ),
                        )
                        bay_or_slot_info_poster.grid(
                            row=0, column=1, padx=5, pady=5, sticky="nsew"
                        )

                        def Refresh_Bay_Info():

                            POSTER = "default.png"
                            while True:

                                if number == 1:
                                    BAY = Directories().RIPPING_BAY_1
                                if number == 2:
                                    BAY = Directories().RIPPING_BAY_2
                                if number == 3:
                                    BAY = Directories().RIPPING_BAY_3
                                if number == 1 and frame == transcoding_frame:
                                    SLOT = Directories().TRANSCODING_SLOT_1
                                if number == 2 and frame == transcoding_frame:
                                    SLOT = Directories().TRANSCODING_SLOT_2
                                if number == 3 and frame == transcoding_frame:
                                    SLOT = Directories().TRANSCODING_SLOT_3
                                if frame == ripping_frame:
                                    (
                                        bay_letter,
                                        bay_number,
                                        bay_dir,
                                        bay_dir_list,
                                        bay_dir_size,
                                    ) = BAY
                                    DIR = bay_dir
                                    DIR_LIST = bay_dir_list
                                    DIR_LIST_SIZE = bay_dir_size
                                    bay_or_slot = "Bay"
                                if frame == transcoding_frame:
                                    slot_dir, slot_dir_list, slot_dir_size = SLOT
                                    DIR = slot_dir
                                    DIR_LIST = slot_dir_list
                                    DIR_LIST_SIZE = slot_dir_size
                                    bay_or_slot = "Slot"
                                try:
                                    if bay_letter:
                                        GO = True
                                    else:
                                        GO = False
                                except UnboundLocalError:
                                    if slot_dir:
                                        GO = True
                                    else:
                                        GO = False
                                if GO == True:
                                    if DIR_LIST:
                                        bay_or_slot_info_title.configure(
                                            text=DIR_LIST[0],
                                            fg_color="#ff5555",
                                            text_color="#282a36",
                                        )
                                        bay_or_slot_info_drive.configure(
                                            text=f"{DIR}{DIR_LIST[0]}",
                                            fg_color="#ff5555",
                                            text_color="#282a36",
                                        )
                                        bay_or_slot_info_size.configure(
                                            text=f"Directory Size  :  {DIR_LIST_SIZE}",
                                            fg_color="#ff5555",
                                            text_color="#282A36",
                                        )
                                        if POSTER == "default.png":
                                            try:

                                                bay_or_slot_info_poster.configure(
                                                    image=customtkinter.CTkImage(
                                                        dark_image=Image.open(
                                                            f"{DIR}{DIR_LIST[0]}/{DIR_LIST[0]}.png"
                                                        ),
                                                        size=(75, 114),
                                                    ),
                                                )

                                            except FileNotFoundError:
                                                pass

                                    else:
                                        bay_or_slot_info_title.configure(
                                            text=f"{bay_or_slot} {number} READY!",
                                            fg_color="#50fa7b",
                                            text_color="#282A36",
                                        )
                                        bay_or_slot_info_drive.configure(
                                            text=f"{bay_or_slot} {number} : Waiting..",
                                            fg_color="#50fa7b",
                                            text_color="#282A36",
                                        )
                                        bay_or_slot_info_size.configure(
                                            text=f"Insert a DVD or Blu-ray Disc to get Started..",
                                            fg_color="#50fa7b",
                                            text_color="#282A36",
                                        )
                                        if POSTER != "default.png":
                                            POSTER = "default.png"
                                            bay_or_slot_info_poster.configure(
                                                image=customtkinter.CTkImage(
                                                    dark_image=Image.open(POSTER),
                                                    size=(80, 121),
                                                ),
                                            )
                                else:
                                    bay_or_slot_info.configure(
                                        fg_color="#44475A",
                                    )
                                    bay_or_slot_info_title.configure(
                                        text=f"No Drive detected.",
                                        fg_color="#282a36",
                                        text_color="#ff5555",
                                    )
                                    bay_or_slot_info_drive.configure(
                                        text=f"Bay {number} is has not been assigned a Drive letter.",
                                        fg_color="#282a36",
                                        text_color="#ff5555",
                                    )
                                    bay_or_slot_info_size.configure(
                                        text=f"Please connect a DVD/Blu-ray Drive to get started.",
                                        fg_color="#282a36",
                                        text_color="#ff5555",
                                    )
                                    if POSTER != "default.png":
                                        POSTER = "default.png"
                                        bay_or_slot_info_poster.configure(
                                            image=customtkinter.CTkImage(
                                                dark_image=Image.open(POSTER),
                                                size=(80, 121),
                                            ),
                                        )
                                time.sleep(5)

                        threading.Thread(target=Refresh_Bay_Info, daemon=True).start()

                    Bay_or_Slot_Info()

                Bay_and_Slot_Maker(1, ripping_frame)
                Bay_and_Slot_Maker(2, ripping_frame)
                Bay_and_Slot_Maker(3, ripping_frame)
                Bay_and_Slot_Maker(1, transcoding_frame)
                Bay_and_Slot_Maker(2, transcoding_frame)
                Bay_and_Slot_Maker(3, transcoding_frame)

            Riping_Bays_And_Transcoding_Slots()

        def Middle_UI_Main_Frame(self):
            main_frame = customtkinter.CTkFrame(
                master=self,
                width=490,
                height=990,
                corner_radius=15,
                fg_color="#FF5555",
            )
            main_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

            info_frame = customtkinter.CTkFrame(
                master=main_frame,
                width=480,
                height=485,
                corner_radius=15,
                fg_color="#282A36",
            )
            info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            info_frame_title = customtkinter.CTkLabel(
                master=info_frame,
                width=470,
                height=28,
                text="--------------Mr Ripper 3.0--------------",
                font=("Comic Sans MS", 18, "bold"),
                corner_radius=15,
                fg_color="#50fa7b",
                text_color="#282A36",
            )
            info_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            ################################################################
            info_textbox = customtkinter.CTkTextbox(
                master=info_frame,
                width=470,
                height=280,
                corner_radius=15,
                fg_color="#44475A",
                text_color="#FF5555",
                font=("Comic Sans MS", 16, "bold"),
            )
            info_textbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            info_textbox.insert("1.0", "            Welcome To Mr Ripper Version 3.0\n")
            info_textbox.insert("2.0", "\n")
            info_textbox.insert(
                "3.0", "Automatically Rip and Transcode your DVDs with ease.\n"
            )
            info_textbox.insert(
                "4.0", " Attach up to 3 DVD Drives for Simultaneous Ripping.\n"
            )
            info_textbox.insert(
                "5.0", " Ripped Movies will wait in the Que to be transcoded.\n"
            )
            info_textbox.insert(
                "6.0", "      3 Movies can be Transcoded Simultaneously.\n"
            )
            info_textbox.insert("7.0", "\n")
            info_textbox.insert("8.0", "--------------Button Breakdown--------------\n")
            info_textbox.insert(
                "9.0", "CLEAR BAYS : Clears all files from the ripping bays.\n"
            )
            info_textbox.insert(
                "10.0",
                "CLEAR SLOTS : Clears half or failed transcoded files, moves the original files bang to the que.\n",
            )
            info_textbox.insert(
                "11.0",
                "CHECK MOVIES: Plays the Movies to check that the  rip and transcode has completed successfully.\n",
            )
            info_textbox.insert(
                "12.0",
                "CLEAR AND QUIT : Clears all Slots and Bays then   Quits the program.\n",
            )
            #################################################################
            info_button_frame = customtkinter.CTkFrame(
                master=info_frame,
                width=470,
                height=150,
                corner_radius=15,
                fg_color="#FF5555",
            )
            info_button_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
            ######################################################################################################
            info_button_clear_ripping_dirs = customtkinter.CTkButton(
                master=info_button_frame,
                width=225,
                height=62,
                border_width=5,
                corner_radius=15,
                border_color="#282A36",
                text_color="#282A36",
                fg_color="#FFB86C",
                font=("Comic Sans MS", 18, "bold"),
                text="CLEAR BAYS",
                command=None,
            )
            info_button_clear_ripping_dirs.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew"
            )

            info_button_clear_transcoding_dirs = customtkinter.CTkButton(
                master=info_button_frame,
                width=225,
                height=62,
                border_width=5,
                corner_radius=15,
                border_color="#282A36",
                text_color="#282A36",
                fg_color="#FFB86C",
                font=("Comic Sans MS", 18, "bold"),
                text="CLEAR SLOTS",
                command=None,
            )
            info_button_clear_transcoding_dirs.grid(
                row=1, column=0, padx=5, pady=5, sticky="nsew"
            )

            info_button_check_movies = customtkinter.CTkButton(
                master=info_button_frame,
                width=225,
                height=62,
                border_width=5,
                corner_radius=15,
                border_color="#282A36",
                text_color="#282A36",
                fg_color="#50fa7b",
                font=("Comic Sans MS", 18, "bold"),
                text="CHECK MOVIES",
                command=None,
            )
            info_button_check_movies.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew"
            )

            info_button_quit_and_clear = customtkinter.CTkButton(
                master=info_button_frame,
                width=225,
                height=62,
                border_width=5,
                corner_radius=15,
                border_color="#282A36",
                text_color="#282A36",
                fg_color="#FF0000",
                font=("Comic Sans MS", 18, "bold"),
                text="CLEAR AND QUIT",
                command=None,
            )
            info_button_quit_and_clear.grid(
                row=1, column=1, padx=5, pady=5, sticky="nsew"
            )
            ######################################################################################################
            collection_frame = customtkinter.CTkFrame(
                master=main_frame,
                width=470,
                height=485,
                corner_radius=15,
            )
            collection_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

            collection_frame_title = customtkinter.CTkLabel(
                master=collection_frame,
                width=470,
                height=28,
                text="------------MOVIE COLLECTION-----------",
                font=("Comic Sans MS", 18, "bold"),
                corner_radius=15,
                fg_color="#50fa7b",
                text_color="#282A36",
            )
            collection_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            collection_listbox_frame = customtkinter.CTkFrame(
                master=collection_frame,
                width=470,
                height=437,
                corner_radius=15,
                fg_color="#FF5555",
            )
            collection_listbox_frame.grid(
                row=1, column=0, padx=5, pady=5, sticky="nsew"
            )
            collection_listbox = Listbox(
                master=collection_listbox_frame,
                bg="#FF5555",
                borderwidth=0,
                highlightthickness=0,
                height=16,
                width=44,
                font=(
                    "Comic Sans MS",
                    13,
                    "bold",
                ),
            )
            collection_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            def Refresh():
                while True:
                    collection = []
                    (
                        collection_dir,
                        collection_list,
                        collection_size,
                    ) = Directories().COLLECTION_DIRECTORY

                    for dir in collection_list:
                        for movie in os.listdir(f"{collection_dir}{dir}"):
                            if movie not in collection:
                                collection.append(movie)
                    if len(collection) != len(collection_listbox.get(0, END)):
                        collection_listbox.delete(0, END)
                        for i in collection:
                            collection_listbox.insert(END, f" {i}")
                    time.sleep(3)

            threading.Thread(target=Refresh, daemon=True).start()

        #
        #
        #
        #
        #
        def Right_UI_Main_Frame(self):

            main_frame = customtkinter.CTkFrame(
                master=self,
                width=490,
                height=990,
                corner_radius=15,
                fg_color="#FF5555",
            )
            main_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

            queued_frame = customtkinter.CTkFrame(
                master=main_frame,
                width=480,
                height=485,
                corner_radius=15,
                fg_color="#282A36",
            )
            queued_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            queued_frame_title = customtkinter.CTkLabel(
                master=queued_frame,
                width=470,
                height=28,
                text="----------------QUEUED----------------",
                font=("Comic Sans MS", 18, "bold"),
                corner_radius=15,
                fg_color="#50fa7b",
                text_color="#282A36",
            )
            queued_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            queued_listbox_frame = customtkinter.CTkFrame(
                master=queued_frame,
                width=470,
                height=437,
                corner_radius=15,
                fg_color="#FF5555",
            )
            queued_listbox_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            queued_listbox = Listbox(
                master=queued_listbox_frame,
                bg="#FF5555",
                borderwidth=0,
                highlightthickness=0,
                height=16,
                width=45,
                font=(
                    "Comic Sans MS",
                    13,
                    "bold",
                ),
            )
            queued_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            completed_frame = customtkinter.CTkFrame(
                master=main_frame,
                width=470,
                height=485,
                corner_radius=15,
            )
            completed_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            completed_frame_title = customtkinter.CTkLabel(
                master=completed_frame,
                width=470,
                height=28,
                text="---------------COMPLETED---------------",
                font=("Comic Sans MS", 18, "bold"),
                corner_radius=15,
                fg_color="#50fa7b",
                text_color="#44475a",
            )
            completed_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            completed_listbox_frame = customtkinter.CTkFrame(
                master=completed_frame,
                width=470,
                height=437,
                corner_radius=15,
                fg_color="#FF5555",
            )
            completed_listbox_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

            completed_listbox = Listbox(
                master=completed_listbox_frame,
                bg="#FF5555",
                borderwidth=0,
                highlightthickness=0,
                height=16,
                width=45,
                font=(
                    "Comic Sans MS",
                    13,
                    "bold",
                ),
            )
            completed_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            def Refresh():
                while True:
                    (
                        queued_dir,
                        queued_list,
                        queued_size,
                    ) = Directories().QUEUED_DIRECTORY
                    (
                        Completed_dir,
                        Completed_list,
                        Completed_size,
                    ) = Directories().COMPLETED_DIRECTORY

                    if len(queued_list) != len(queued_listbox.get(0, END)):
                        queued_listbox.delete(0, END)
                        for movie in queued_list:
                            queued_listbox.insert(END, f" {movie}")
                    if len(Completed_list) != len(completed_listbox.get(0, END)):
                        completed_listbox.delete(0, END)
                        for movie in Completed_list:
                            completed_listbox.insert(END, f" {movie}")
                    time.sleep(3)

            threading.Thread(target=Refresh, daemon=True).start()

    ############################################################################################################################################################################################################
    GUI = Mr_Ripper_GUI()
    GUI.mainloop()
