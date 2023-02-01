import os
import win32api
import win32file
import itertools
from string import ascii_uppercase

class Directories:
    """
    Directories class to manage directories and subdirectories.
    
    This class creates and maintains the following directories:
        - Collection/
        - Completed/
        - Queued/
        - Ripping/
        - Transcoding/
    
    It also creates subdirectories within the Collection/ directory for each
    uppercase letter and digit (e.g. Collection/A, Collection/B, Collection/0, etc.).
    
    The class also keeps track of the contents of each directory and stores them as a list
    (e.g. Collection_Dir_List, Completed_Dir_List, etc.).
    
    Additionally, the class creates a directory for each CD-ROM drive found on the system in
    the Ripping/ directory, with the name "Drive_#...", where # is the index of the drive.
    
    Attributes:
        Collection_Dir (str): The path to the Collection/ directory.
        Completed_Dir (str): The path to the Completed/ directory.
        Queued_Dir (str): The path to the Queued/ directory.
        Ripping_Dir (str): The path to the Ripping/ directory.
        Transcoding_Dir (str): The path to the Transcoding/ directory.
        Directories (list): A list of all the directories created and maintained by this class.
        Collection_Dir_List (list): A list of the contents of the Collection/ directory.
        Completed_Dir_List (list): A list of the contents of the Completed/ directory.
        Queued_Dir_List (list): A list of the contents of the Queued/ directory.
        Ripping_Dir_List (list): A list of the contents of the Ripping/ directory.
    
    Methods:
        __init__: Initializes the Directories class and creates/checks for the existence of each directory.
"""
    def __init__(self):
        self.Collection_Dir = "Collection/" # Define the directory for the collection of files
        self.Completed_Dir = "Completed/" # Define the directory for the completed files
        self.Queued_Dir = "Queued/" # Define the directory for the queued files
        self.Ripping_Dir = "Ripping/" # Define the directory for the files that are being ripped
        self.Transcoding_Dir = "Transcoding/" # Define the directory for the files that are being transcoded
        self.Directories = [
            self.Collection_Dir, # Add the collection directory to the list of directories
            self.Completed_Dir, # Add the completed directory to the list of directories
            self.Queued_Dir, # Add the queued directory to the list of directories
            self.Ripping_Dir, # Add the ripping directory to the list of directories
            self.Transcoding_Dir, # Add the transcoding directory to the list of directories
        ]
        # Check if the Collection_Dir directory exists, if not create it 
        if os.path.isdir(self.Collection_Dir) == False:
            os.mkdir(self.Collection_Dir)
            # Iterate through all uppercase letters and digits and create a directory for each
            for letter in itertools.chain(ascii_uppercase, [str(i) for i in range(10)]):
                directory = self.Collection_Dir + letter + "/"
                # Check if the directory already exists, if not create it
                if os.path.isdir(directory) != True:
                    os.mkdir(directory)
            # Get the list of all subdirectories in Collection_Dir
            self.Collection_Dir_List = os.listdir(self.Collection_Dir)
        else:
            # Get the list of all subdirectories in Collection_Dir
            self.Collection_Dir_List = os.listdir(self.Collection_Dir)

        # Check if the Completed_Dir directory already exists
        if os.path.isdir(self.Completed_Dir) == False:
            # If it does not exist, create the directory
            os.mkdir(self.Completed_Dir)
            # Get a list of the files and directories in the Completed_Dir
            self.Completed_Dir_List = os.listdir(self.Completed_Dir)
        else:
            # If it does exist, get a list of the files and directories in the Completed_Dir
            self.Completed_Dir_List = os.listdir(self.Completed_Dir)

        # Check if the "Queued" directory exists
        if os.path.isdir(self.Queued_Dir) == False:
            # If it does not exist, create the directory
            os.mkdir(self.Queued_Dir)
            # Get a list of all the files and directories in the "Queued" directory
            self.Queued_Dir_List = os.listdir(self.Queued_Dir)
        else:
            # If the "Queued" directory already exists, get a list of all the files and directories in the "Queued" directory
            self.Queued_Dir_List = os.listdir(self.Queued_Dir)

        # Check if the Ripping directory exists, if not create it
        if os.path.isdir(self.Ripping_Dir) == False:
            os.mkdir(self.Ripping_Dir)
            # Get a list of the contents of the Ripping directory
            self.Ripping_Dir_List = os.listdir(self.Ripping_Dir)
            # Initialize an empty list to hold the dvd drive names
            dvd_drive_list = []
            # Get a list of all the drives on the computer
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split("\000")[:-1]
            # Iterate through the drives and check if it is a CD-ROM drive
            for drive in drives:
                if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                    # If it is a CD-ROM drive, add it to the dvd_drive_list
                    dvd_drive_list.append(drive)
                    # Get the index of the drive in the dvd_drive_list
                    drive_number = dvd_drive_list.index(drive)
                    # Format the drive name to remove the ":\"
                    drive = drive.replace(":\\", "")
                    # Create a directory for the drive in the Ripping directory
                    os.mkdir(f"{self.Ripping_Dir}Drive_{drive_number}_{drive}")
            # Update the Ripping directory list
            self.Ripping_Dir_List = os.listdir(self.Ripping_Dir)

            try:
                # Check if the first item in the Ripping_Dir_List is a directory
                if (
                    os.path.isdir(f"{self.Ripping_Dir}{self.Ripping_Dir_List[0]}")
                    == True
                ):
                    # Assign the first item in the Ripping_Dir_List as the Ripping_Bay_1 variable
                    self.Ripping_Bay_1 = (
                        f"{self.Ripping_Dir}{self.Ripping_Dir_List[0]}/"
                    )
                    # Assign the first item in the dvd_drive_list as the Target1 variable
                    self.Target1 = (dvd_drive_list[0], 0, self.Ripping_Bay_1)
            except IndexError:
                # If there is an index error, assign None to Ripping_Bay_1 and Target1
                self.Ripping_Bay_1 = None
                self.Target1 = (None, None, self.Ripping_Bay_1)

            try:
                # Check if the directory exists for the first ripping bay
                if (
                    os.path.isdir(f"{self.Ripping_Dir}{self.Ripping_Dir_List[1]}")
                    == True
                ):
                    # Assign the directory path for the first ripping bay
                    self.Ripping_Bay_2 = (
                        f"{self.Ripping_Dir}{self.Ripping_Dir_List[1]}/"
                    )
                    # Assign the target for the first ripping bay (drive, index, directory)
                    self.Target2 = (dvd_drive_list[1], 1, self.Ripping_Bay_2)
            except IndexError:
                # If the index is out of range, assign None to the target and the ripping bay
                self.Ripping_Bay_2 = None
                self.Target2 = (None, None, self.Ripping_Bay_2)

            try:
                # Check if the directory exists for the third ripping bay
                if os.path.isdir(f"{self.Ripping_Dir}{self.Ripping_Dir_List[2]}") == True:
                    # If the directory exists, set the path for the third ripping bay
                    self.Ripping_Bay_3 = f"{self.Ripping_Dir}{self.Ripping_Dir_List[2]}/"
                    # Set the target for the third ripping bay to include the drive letter, drive number, and directory path
                    self.Target3 = (dvd_drive_list[2], 2, self.Ripping_Bay_3)
            except IndexError:
                # If an index error is caught, the third ripping bay does not exist
                self.Ripping_Bay_3 = None
                self.Target3 = (None, None, self.Ripping_Bay_3)

        else:
            # Initialize an empty list to store the DVD drive letters
            dvd_drive_list = []
            # Get the list of all logical drive strings
            drives = win32api.GetLogicalDriveStrings()
            # Split the drive strings by null characters and remove the last empty string
            drives = drives.split("\000")[:-1]
            # Iterate through the drive strings
            for drive in drives:
                # Check if the current drive is a CD-ROM drive
                if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                    # If it is, add the drive letter to the list
                    dvd_drive_list.append(drive)
                    # Get the index of the current drive in the list
                    drive_number = dvd_drive_list.index(drive)
                    # Remove the ":\" from the drive letter
                    drive = drive.replace(":\\", "")
            # Get a list of all the directories in the ripping directory
            self.Ripping_Dir_List = os.listdir(self.Ripping_Dir)
            try:
                # Assign the first directory in the list to the Ripping_Bay_1 variable
                self.Ripping_Bay_1 = f"{self.Ripping_Dir}{self.Ripping_Dir_List[0]}/"
                # Assign the first DVD drive letter, its index in the list, and the associated directory to the Target1 variable
                self.Target1 = (dvd_drive_list[0], 0, self.Ripping_Bay_1)
            except IndexError:
                # If there is no first directory, assign None to the Ripping_Bay_1 and Target1 variables
                self.Ripping_Bay_1 = None
                self.Target1 = (None, None, self.Ripping_Bay_1)
            try:
                # Assign the second directory in the list to the Ripping_Bay_2 variable
                self.Ripping_Bay_2 = f"{self.Ripping_Dir}{self.Ripping_Dir_List[1]}/"
                # Assign the second DVD drive letter, its index in the list, and the associated directory to the Target2 variable
                self.Target2 = (dvd_drive_list[1], 1, self.Ripping_Bay_2)
            except IndexError:
                # If there is no second directory, assign None to the Ripping_Bay_2 and Target2 variables
                self.Ripping_Bay_2 = None
                self.Target2 = (None, None, self.Ripping_Bay_2)
            try:
                # Assign the third directory in the list to the Ripping_Bay_3 variable
                self.Ripping_Bay_3 = f"{self.Ripping_Dir}{self.Ripping_Dir_List[2]}/"
                # Assign the third DVD drive letter, its index in the list, and the associated directory to the Target3 variable
                self.Target3 = (dvd_drive_list[2], 2, self.Ripping_Bay_3)
            except IndexError:
                # If there is no third directory, assign None to the Ripping_Bay_3 and Target3
                self.Ripping_Bay_3 = None
                self.Target3 = (None, None, self.Ripping_Bay_3)

        # check if the Transcoding directory exists, if not create it and the subdirectories
        if os.path.isdir(self.Transcoding_Dir) == False:
            os.mkdir(self.Transcoding_Dir) # create the Transcoding directory
            self.Transcoding_Dir_List = os.listdir(self.Transcoding_Dir) # get the list of files in the Transcoding directory
            os.mkdir(f"{self.Transcoding_Dir}Slot_1") # create the Slot 1 subdirectory
            self.Transcoding_slot_1 = f"{self.Transcoding_Dir}Slot_1/" # assign the path of Slot 1 to a variable
            os.mkdir(f"{self.Transcoding_Dir}Slot_2") # create the Slot 2 subdirectory
            self.Transcoding_slot_2 = f"{self.Transcoding_Dir}Slot_2/" # assign the path of Slot 2 to a variable
            os.mkdir(f"{self.Transcoding_Dir}Slot_3") # create the Slot 3 subdirectory
            self.Transcoding_slot_3 = f"{self.Transcoding_Dir}Slot_3/" # assign the path of Slot 3 to a variable
        else:
            self.Transcoding_Dir_List = os.listdir(self.Transcoding_Dir) # get the list of files in the Transcoding directory
            self.Transcoding_slot_1 = f"{self.Transcoding_Dir}Slot_1/" # assign the path of Slot 1 to a variable
            self.Transcoding_slot_2 = f"{self.Transcoding_Dir}Slot_2/" # assign the path of Slot 2 to a variable
            self.Transcoding_slot_3 = f"{self.Transcoding_Dir}Slot_3/" # assign the path of Slot 3 to a variable
            

def main():
    Directories()

if __name__ == "__main__":
    main()