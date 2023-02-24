import os
import win32api
import win32file
import itertools
import shutil
from string import ascii_uppercase


class Directories:
    def __init__(self):

        storage_total, storage_used, storage_free = self.get_storage_size(".")

        collection_directory = "Collection/"
        if os.path.isdir(collection_directory) == False:
            os.mkdir(collection_directory)
            for letter_or_number in itertools.chain(
                ascii_uppercase, [str(i) for i in range(10)]
            ):
                directory = collection_directory + letter_or_number + "/"
                if os.path.isdir(directory) != True:
                    os.mkdir(directory)
        collection_directory_list = os.listdir(collection_directory)
        collection_directory_size = self.get_directory_size(collection_directory)

        completed_directory = "Completed/"
        if os.path.isdir(completed_directory) == False:
            os.mkdir(completed_directory)
        completed_directory_list = os.listdir(completed_directory)
        completed_directory_size = self.get_directory_size(completed_directory)

        queued_directory = "Queued/"
        if os.path.isdir(queued_directory) == False:
            os.mkdir(queued_directory)
        queued_directory_list = os.listdir(queued_directory)
        queued_directory_size = self.get_directory_size(queued_directory)

        ripping_directory = "Ripping/"
        if os.path.isdir(ripping_directory) == False:
            os.mkdir(ripping_directory)
        ripping_directory_list = os.listdir(ripping_directory)
        ripping_directory_size = self.get_directory_size(ripping_directory)

        transcoding_directory = "Transcoding/"
        if os.path.isdir(transcoding_directory) == False:
            os.mkdir(transcoding_directory)
            os.mkdir(f"{transcoding_directory}Slot_1")
            os.mkdir(f"{transcoding_directory}Slot_2")
            os.mkdir(f"{transcoding_directory}Slot_3")
        transcoding_directory_list = os.listdir(transcoding_directory)
        transcoding_directory_size = self.get_directory_size(transcoding_directory)
        transcoding_slot_1 = f"{transcoding_directory}Slot_1/"
        transcoding_slot_1_list = os.listdir(transcoding_slot_1)
        transcoding_slot_1_size = self.get_directory_size(transcoding_slot_1)
        transcoding_slot_2 = f"{transcoding_directory}Slot_2/"
        transcoding_slot_2_list = os.listdir(transcoding_slot_2)
        transcoding_slot_2_size = self.get_directory_size(transcoding_slot_2)
        transcoding_slot_3 = f"{transcoding_directory}Slot_3/"
        transcoding_slot_3_list = os.listdir(transcoding_slot_3)
        transcoding_slot_3_size = self.get_directory_size(transcoding_slot_3)

        dvd_drive_list = []
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split("\000")[:-1]

        for drive in drives:
            #!!TESTING DRIVES HERE SHOULD BE == not !=
            if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                dvd_drive_list.append(drive)
                drive_number = dvd_drive_list.index(drive)
                drive_letter = drive.replace(":\\", "")
                drive_directory = (
                    f"{ripping_directory}Bay_{drive_letter}_{drive_number}/"
                )
                if os.path.isdir(drive_directory) == False:
                    os.mkdir(drive_directory)

        try:
            if os.path.isdir(f"{ripping_directory}{ripping_directory_list[0]}") == True:
                ripping_directory_bay = (
                    f"{ripping_directory}{ripping_directory_list[0]}/"
                )
                ripping_directory_bay_size = self.get_directory_size(
                    ripping_directory_bay
                )
                ripping_directory_bay_list = os.listdir(ripping_directory_bay)
                ripping_bay_1 = (
                    dvd_drive_list[0],
                    0,
                    ripping_directory_bay,
                    ripping_directory_bay_list,
                    ripping_directory_bay_size,
                )
        except IndexError:
            ripping_bay_1 = (None, None, None, [], "0 B")

        try:
            if os.path.isdir(f"{ripping_directory}{ripping_directory_list[1]}") == True:
                ripping_directory_bay = (
                    f"{ripping_directory}{ripping_directory_list[1]}/"
                )
                ripping_directory_bay_size = self.get_directory_size(
                    ripping_directory_bay
                )
                ripping_directory_bay_list = os.listdir(ripping_directory_bay)
                ripping_bay_2 = (
                    dvd_drive_list[1],
                    1,
                    ripping_directory_bay,
                    ripping_directory_bay_list,
                    ripping_directory_bay_size,
                )
        except IndexError:
            ripping_bay_2 = (None, None, None, [], "0 B")

        try:
            if os.path.isdir(f"{ripping_directory}{ripping_directory_list[2]}") == True:
                ripping_directory_bay = (
                    f"{ripping_directory}{ripping_directory_list[2]}/"
                )
                ripping_directory_bay_size = self.get_directory_size(
                    ripping_directory_bay
                )
                ripping_directory_bay_list = os.listdir(ripping_directory_bay)
                ripping_bay_3 = (
                    dvd_drive_list[2],
                    2,
                    ripping_directory_bay,
                    ripping_directory_bay_list,
                    ripping_directory_bay_size,
                )
        except IndexError:
            ripping_bay_3 = (None, None, None, [], "0 B")

        self.total_space_on_drive = storage_total
        self.used_space_on_drive = storage_used
        self.free_space_on_drive = storage_free
        self.MAIN_DIRECTORY = (
            self.total_space_on_drive,
            self.used_space_on_drive,
            self.free_space_on_drive,
        )
        self.collection_directory = collection_directory
        self.collection_directory_list = collection_directory_list
        self.collection_directory_size = collection_directory_size
        self.COLLECTION_DIRECTORY = (
            self.collection_directory,
            self.collection_directory_list,
            self.collection_directory_size,
        )
        self.completed_directory = completed_directory
        self.completed_directory_list = completed_directory_list
        self.completed_directory_size = completed_directory_size
        self.COMPLETED_DIRECTORY = (
            self.completed_directory,
            self.completed_directory_list,
            self.completed_directory_size,
        )
        self.queued_directory = queued_directory
        self.queued_directory_list = queued_directory_list
        self.queued_directory_size = queued_directory_size
        self.QUEUED_DIRECTORY = (
            self.queued_directory,
            self.queued_directory_list,
            self.queued_directory_size,
        )
        self.ripping_directory = ripping_directory
        self.ripping_directory_list = ripping_directory_list
        self.ripping_directory_size = ripping_directory_size
        self.RIPPING_DIRECTORY = (
            self.ripping_directory,
            self.ripping_directory_list,
            self.ripping_directory_size,
        )
        self.transcoding_directory = transcoding_directory
        self.transcoding_directory_list = transcoding_directory_list
        self.transcoding_directory_size = transcoding_directory_size
        self.TRANSCODING_DIRECTORY = (
            self.transcoding_directory,
            self.transcoding_directory_list,
            self.transcoding_directory_size,
        )
        self.transcoding_slot_1 = transcoding_slot_1
        self.transcoding_slot_1_list = transcoding_slot_1_list
        self.transcoding_slot_1_size = transcoding_slot_1_size
        self.TRANSCODING_SLOT_1 = (
            self.transcoding_slot_1,
            self.transcoding_slot_1_list,
            self.transcoding_slot_1_size,
        )
        self.transcoding_slot_2 = transcoding_slot_2
        self.transcoding_slot_2_list = transcoding_slot_2_list
        self.transcoding_slot_2_size = transcoding_slot_2_size
        self.TRANSCODING_SLOT_2 = (
            self.transcoding_slot_2,
            self.transcoding_slot_2_list,
            self.transcoding_slot_2_size,
        )
        self.transcoding_slot_3 = transcoding_slot_3
        self.transcoding_slot_3_list = transcoding_slot_3_list
        self.transcoding_slot_3_size = transcoding_slot_3_size
        self.TRANSCODING_SLOT_3 = (
            self.transcoding_slot_3,
            self.transcoding_slot_3_list,
            self.transcoding_slot_3_size,
        )
        self.TRANSCODING_SLOT_LIST = [
            self.transcoding_slot_1,
            self.transcoding_slot_2,
            self.transcoding_slot_3,
        ]
        self.RIPPING_BAY_LIST = os.listdir(ripping_directory)
        self.RIPPING_BAY_1 = ripping_bay_1
        self.RIPPING_BAY_2 = ripping_bay_2
        self.RIPPING_BAY_3 = ripping_bay_3

    def get_directory_size(self, path):

        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        if total_size < 1024:
            return f"{total_size} B"
        elif total_size < 1024**2:
            return f"{total_size/1024:.2f} KB"
        elif total_size < 1024**3:
            return f"{total_size/1024**2:.2f} MB"
        else:
            return f"{total_size/1024**3:.2f} GB"

    def get_storage_size(self, file_path):

        total, used, free = shutil.disk_usage(
            os.path.dirname(os.path.abspath(file_path))
        )
        total = total // (1024**3)
        total = f"{total} GB"
        used = used // (1024**3)
        used = f"{used} GB"
        free = free // (1024**3)
        free = f"{free} GB"
        return total, used, free


#! TESTING !#
def Directories_Testing():
    Directories_Testing = Directories()
    print(
        "DRIVE INFO | What you should see '('Drive size', 'Space used on Drive', 'Free space on Drive')' :  ",
        Directories_Testing.MAIN_DIRECTORY,
    )
    print(
        "COLLECTION_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.COLLECTION_DIRECTORY,
    )
    print(
        "COMPLETED_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.COMPLETED_DIRECTORY,
    )
    print(
        "QUEUED_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.QUEUED_DIRECTORY,
    )
    print(
        "RIPPING_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.RIPPING_DIRECTORY,
    )
    print(
        "TRANSCODING_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.TRANSCODING_DIRECTORY,
    )
    print(
        "TRANSCODING_SLOT_LIST INFO | What you should see '['A list of the Transcoding slot Directory locations']' :  ",
        Directories_Testing.TRANSCODING_SLOT_LIST,
    )
    print(
        "TRANSCODING_SLOT_1 INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.TRANSCODING_SLOT_1,
    )
    print(
        "TRANSCODING_SLOT_2 INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.TRANSCODING_SLOT_2,
    )
    print(
        "TRANSCODING_SLOT_3 INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ",
        Directories_Testing.TRANSCODING_SLOT_3,
    )
    print(
        "RIPPING_BAY_LIST INFO | What you should see  '['A list of the Ripping Bay Directory locations']' :  ",
        Directories_Testing.RIPPING_BAY_LIST,
    )
    print(
        "RIPPING_BAY_1 INFO | What you should see '('Drive letter', 'Drive number', '[Movie thats Ripping]', 'Directory size')' :  ",
        Directories_Testing.RIPPING_BAY_1,
    )
    print(
        "RIPPING_BAY_2 INFO | What you should see '('Drive letter', 'Drive number', '[Movie thats Ripping]', 'Directory size')' :  ",
        Directories_Testing.RIPPING_BAY_2,
    )
    print(
        "RIPPING_BAY_3 INFO | What you should see '('Drive letter', 'Drive number', '[Movie thats Ripping]', 'Directory size')' :  ",
        Directories_Testing.RIPPING_BAY_3,
    )


#! TESTING !#
if __name__ == "__main__":
    try:
        for i in range(1):
            Directories_Testing()
        print(
            "################################ This Script has finished Running!################################"
        )
    except Exception as e:
        print(e)
