import os
import win32api
import win32file
import itertools
import shutil
from string import ascii_uppercase

class Directories:
    def __init__(self):
        def get_directory_size(path):
            """
            Calculates the total size of the directory at the given `path`.

            Parameters:
            - path (str): the file path to the directory.

            Returns:
            str: the total size of the directory in B, KB, MB, or GB, depending on the size of the directory.
            """
            total_size = 0
            # Loop through all the subdirectories, directory names and filenames
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    # Join the directory path and filename to get the full path of the file
                    fp = os.path.join(dirpath, f)
                    # Add the size of the file to the total size
                    total_size += os.path.getsize(fp)
            # Return the total size in B, KB, MB, or GB, depending on the size of the directory
            if total_size < 1024:
                return f"{total_size} B"
            elif total_size < 1024**2:
                return f"{total_size/1024:.2f} KB"
            elif total_size < 1024**3:
                return f"{total_size/1024**2:.2f} MB"
            else:
                return f"{total_size/1024**3:.2f} GB"

        def get_storage_size(file_path):
            """
            This function returns the total storage size, used storage, and free storage in GB of the file system that contains file_path.
            Args:
                file_path (str): The file path to a file located in the file system for which to retrieve storage information.
            Returns:
                tuple: The total storage size, used storage size, and free storage size in GB.
            """
            # Get disk usage statistics for the file system that contains file_path
            total, used, free = shutil.disk_usage(
                os.path.dirname(os.path.abspath(file_path))
            )
            # Convert total storage size to GB and format it as a string
            total = total // (1024**3)
            total = f"{total} GB"
            # Convert used storage size to GB and format it as a string
            used = used // (1024**3)
            used = f"{used} GB"
            # Convert free storage size to GB and format it as a string
            free = free // (1024**3)
            free = f"{free} GB"
            # Return the total, used, and free storage sizes in GB as a tuple
            return total, used, free

        # Get the total storage size, used storage size and free storage size of the current directory
        storage_total, storage_used, storage_free = get_storage_size(".")
        
        # Define the directory for the collection of files
        collection_directory = "Collection/"
        # Check if the collection directory exists
        if os.path.isdir(collection_directory) == False:
            # If not, create the directory
            os.mkdir(collection_directory)
            # Loop through all upper case letters and numbers as subdirectories
            for letter_or_number in itertools.chain(ascii_uppercase, [str(i) for i in range(10)]):
                # Define the subdirectory path
                directory = collection_directory + letter_or_number + "/"
                # Check if the subdirectory exists
                if os.path.isdir(directory) != True:
                    # If not, create the subdirectory
                    os.mkdir(directory)
        # Get the list of all directories in the collection directory
        collection_directory_list = os.listdir(collection_directory)
        # Get the size of the collection directory
        collection_directory_size = get_directory_size(collection_directory)

        # Define the directory for completed files
        completed_directory = "Completed/"
        # Check if the directory for completed files exists
        if os.path.isdir(completed_directory) == False:
            # If the directory does not exist, create the directory
            os.mkdir(completed_directory)
        # Get a list of all the files in the completed directory
        completed_directory_list = os.listdir(completed_directory)
        # Get the size of the completed directory in bytes
        completed_directory_size = get_directory_size(completed_directory)
        
        # Define the directory for the queued files
        queued_directory = "Queued/"
        # Check if the directory exists
        if os.path.isdir(queued_directory) == False:
            # Create the directory if it doesn't exist
            os.mkdir(queued_directory)
        # Get the list of files in the queued directory
        queued_directory_list = os.listdir(queued_directory)
        # Get the size of the queued directory
        queued_directory_size = get_directory_size(queued_directory)
        
        # Define the directory for the files that are being ripped
        ripping_directory = "Ripping/"
        # Check if the directory exists
        if os.path.isdir(ripping_directory) == False:
            # Create the directory if it doesn't exist
            os.mkdir(ripping_directory)
        # Get the list of files in the ripping directory
        ripping_directory_list = os.listdir(ripping_directory)
        # Get the size of the ripping directory
        ripping_directory_size = get_directory_size(ripping_directory)
        
        # Define the directory for transcoding
        transcoding_directory = "Transcoding/"
        # Check if the directory exists
        if os.path.isdir(transcoding_directory) == False:
            # Create the directory if it doesn't exist
            os.mkdir(transcoding_directory)
            # Create subdirectories for the slots
            os.mkdir(f"{transcoding_directory}Slot_1")
            os.mkdir(f"{transcoding_directory}Slot_2")
            os.mkdir(f"{transcoding_directory}Slot_3")
        # Get the list of files in the transcoding directory
        transcoding_directory_list = os.listdir(transcoding_directory)
        # Get the size of the transcoding directory
        transcoding_directory_size = get_directory_size(transcoding_directory)
        # Setting the path to transcoding directory slots
        # Creating the path string to the first slot in the transcoding directory
        transcoding_slot_1 = f"{transcoding_directory}Slot_1/"
        # Getting the list of files in the first transcoding slot directory
        transcoding_slot_1_list = os.listdir(transcoding_slot_1)
        # Calculating the size of the first transcoding slot directory
        transcoding_slot_1_size = get_directory_size(transcoding_slot_1)
        # Creating the path string to the second slot in the transcoding directory
        transcoding_slot_2 = f"{transcoding_directory}Slot_2/"
        # Getting the list of files in the second transcoding slot directory
        transcoding_slot_2_list = os.listdir(transcoding_slot_2)
        # Calculating the size of the second transcoding slot directory
        transcoding_slot_2_size = get_directory_size(transcoding_slot_2)
        # Creating the path string to the third slot in the transcoding directory
        transcoding_slot_3 = f"{transcoding_directory}Slot_3/"
        # Getting the list of files in the third transcoding slot directory
        transcoding_slot_3_list = os.listdir(transcoding_slot_3)
        # Calculating the size of the third transcoding slot directory
        transcoding_slot_3_size = get_directory_size(transcoding_slot_3)
        
        # Initializing an empty list to store the DVD drive letters
        dvd_drive_list = []
        # Getting the string of all logical drives on the system
        drives = win32api.GetLogicalDriveStrings()
        # Splitting the drives into a list and removing the last empty element
        drives = drives.split("\000")[:-1]

        # Looping through all the drives
        for drive in drives:
            # Checking if the current drive is a CD-ROM drive
            if win32file.GetDriveType(drive) == win32file.DRIVE_CDROM:
                # Appending the drive letter to the list of DVD drives
                dvd_drive_list.append(drive)
                # Getting the index of the current drive in the list of DVD drives
                drive_number = dvd_drive_list.index(drive)
                # Getting the letter of the current drive
                drive_letter = drive.replace(":\\", "")
                # Creating the path string to the directory for the current drive
                drive_directory = f"{ripping_directory}Bay_{drive_letter}_{drive_number}/"
                # Checking if the directory for the current drive already exists
                if os.path.isdir(drive_directory) == False:
                    # Creating the directory for the current drive if it does not exist
                    os.mkdir(drive_directory)

        # Try block to handle potential IndexError if there is not enough elements in the list
        try:
            # Check if the directory exists
            if (os.path.isdir(f"{ripping_directory}{ripping_directory_list[0]}") == True):
                # Set the full path to the directory for this bay
                ripping_directory_bay = (f"{ripping_directory}{ripping_directory_list[0]}/")
                # Get the size of the directory
                ripping_directory_bay_size = get_directory_size(ripping_directory_bay)
                # Get a list of the items in the directory
                ripping_directory_bay_list = os.listdir(ripping_directory_bay)
                # Create a tuple with the values for the first bay
                ripping_bay_1 = (dvd_drive_list[0], 0, ripping_directory_bay, ripping_directory_bay_list, ripping_directory_bay_size)
        except IndexError:
            # Set the values for the first bay to default values if there was an IndexError
            ripping_bay_1 = (None, None, [], "0 B")

        # Try block to handle potential IndexError if there is not enough elements in the list
        try:
            # Check if the directory exists
            if (os.path.isdir(f"{ripping_directory}{ripping_directory_list[1]}") == True):
                # Set the full path to the directory for this bay
                ripping_directory_bay = (f"{ripping_directory}{ripping_directory_list[1]}/")
                # Get the size of the directory
                ripping_directory_bay_size = get_directory_size(ripping_directory_bay)
                # Get a list of the items in the directory
                ripping_directory_bay_list = os.listdir(ripping_directory_bay)
                # Create a tuple with the values for the second bay
                ripping_bay_2 = (dvd_drive_list[1], 1, ripping_directory_bay, ripping_directory_bay_list, ripping_directory_bay_size)
        except IndexError:
            # Set the values for the second bay to default values if there was an IndexError
            ripping_bay_2 = (None, None, [], "0 B")

        # Try block to handle potential IndexError if there is not enough elements in the list
        try:
            # Check if the directory exists
            if (os.path.isdir(f"{ripping_directory}{ripping_directory_list[2]}") == True):
                # Set the full path to the directory for this bay
                ripping_directory_bay = (f"{ripping_directory}{ripping_directory_list[2]}/")
                # Get the size of the directory
                ripping_directory_bay_size = get_directory_size(ripping_directory_bay)
                # Get a list of the items in the directory
                ripping_directory_bay_list = os.listdir(ripping_directory_bay)
                # Create a tuple with the values for the third bay
                ripping_bay_3 = (dvd_drive_list[2], 2, ripping_directory_bay, ripping_directory_bay_list, ripping_directory_bay_size)
        except IndexError:
            # Set the values for the third bay to default values if there was an IndexError
            ripping_bay_3 = (None, None, [], "0 B")

        # Assign total storage of the drive to total_space_on_drive
        self.total_space_on_drive = storage_total
        # Assign used storage of the drive to used_space_on_drive
        self.used_space_on_drive = storage_used
        # Assign free storage of the drive to free_space_on_drive
        self.free_space_on_drive = storage_free
        # Create tuple MAIN_DIRECTORY with total_space_on_drive, used_space_on_drive, and free_space_on_drive
        self.MAIN_DIRECTORY = (self.total_space_on_drive, self.used_space_on_drive, self.free_space_on_drive)
        # Assign the collection_directory to collection_directory
        self.collection_directory = collection_directory
        # Assign list of items in collection_directory to collection_directory_list
        self.collection_directory_list = collection_directory_list
        # Assign the size of collection_directory to collection_directory_size
        self.collection_directory_size = collection_directory_size
        # Create tuple COLLECTION_DIRECTORY with collection_directory, collection_directory_list, and collection_directory_size
        self.COLLECTION_DIRECTORY = (self.collection_directory, self.collection_directory_list, self.collection_directory_size)
        # Assign the completed_directory to completed_directory
        self.completed_directory = completed_directory
        # Assign list of items in completed_directory to completed_directory_list
        self.completed_directory_list = completed_directory_list
        # Assign the size of completed_directory to completed_directory_size
        self.completed_directory_size = completed_directory_size
        # Create tuple COMPLETED_DIRECTORY with completed_directory, completed_directory_list, and completed_directory_size
        self.COMPLETED_DIRECTORY = (self.completed_directory, self.completed_directory_list, self.completed_directory_size)
        # Assign the queued_directory to queued_directory
        self.queued_directory = queued_directory
        # Assign list of items in queued_directory to queued_directory_list
        self.queued_directory_list = queued_directory_list
        # Assign the size of queued_directory to queued_directory_size
        self.queued_directory_size = queued_directory_size
        # Create tuple QUEUED_DIRECTORY with queued_directory, queued_directory_list, and queued_directory_size
        self.QUEUED_DIRECTORY = (self.queued_directory, self.queued_directory_list, self.queued_directory_size)
        # Assign the ripping_directory to ripping_directory
        self.ripping_directory = ripping_directory
        # Assign list of items in ripping_directory to ripping_directory_list
        self.ripping_directory_list = ripping_directory_list
        # Assign the size of ripping_directory to ripping_directory_size
        self.ripping_directory_size = ripping_directory_size
        # Create tuple RIPPING_DIRECTORY with ripping_directory, ripping_directory_list, and ripping_directory_size
        self.RIPPING_DIRECTORY = (self.ripping_directory, self.ripping_directory_list, self.ripping_directory_size)
        # Set the value of the transcoding directory attribute
        self.transcoding_directory = transcoding_directory
        # Set the value of the transcoding directory list attribute
        self.transcoding_directory_list = transcoding_directory_list
        # Set the value of the transcoding directory size attribute
        self.transcoding_directory_size = transcoding_directory_size
        # Create a tuple of the transcoding directory, the transcoding directory list and the transcoding directory size
        self.TRANSCODING_DIRECTORY = (self.transcoding_directory, self.transcoding_directory_list, self.transcoding_directory_size)
        # Assigning the value of transcoding_slot_1 to instance variable transcoding_slot_1
        self.transcoding_slot_1 = transcoding_slot_1
        # Assigning the value of transcoding_slot_1_list to instance variable transcoding_slot_1_list
        self.transcoding_slot_1_list = transcoding_slot_1_list
        # Assigning the value of transcoding_slot_1_size to instance variable transcoding_slot_1_size
        self.transcoding_slot_1_size = transcoding_slot_1_size
        # Creating a tuple with the values of instance variables transcoding_slot_1, transcoding_slot_1_list, and transcoding_slot_1_size
        self.TRANSCODING_SLOT_1 = (self.transcoding_slot_1, self.transcoding_slot_1_list, self.transcoding_slot_1_size)
        # Assigning the value of transcoding_slot_2 to instance variable transcoding_slot_2
        self.transcoding_slot_2 = transcoding_slot_2
        # Assigning the value of transcoding_slot_2_list to instance variable transcoding_slot_2_list
        self.transcoding_slot_2_list = transcoding_slot_2_list
        # Assigning the value of transcoding_slot_2_size to instance variable transcoding_slot_2_size
        self.transcoding_slot_2_size = transcoding_slot_2_size
        # Creating a tuple with the values of instance variables transcoding_slot_2, transcoding_slot_2_list, and transcoding_slot_2_size
        self.TRANSCODING_SLOT_2 = (self.transcoding_slot_2, self.transcoding_slot_2_list, self.transcoding_slot_2_size)
        # Assigning the value of transcoding_slot_3 to instance variable transcoding_slot_3
        self.transcoding_slot_3 = transcoding_slot_3
        # Assigning the value of transcoding_slot_3_list to instance variable transcoding_slot_3_list
        self.transcoding_slot_3_list = transcoding_slot_3_list
        # Assigning the value of transcoding_slot_3_size to instance variable transcoding_slot_3_size
        self.transcoding_slot_3_size = transcoding_slot_3_size
        # Creating a tuple with the values of instance variables transcoding_slot_3, transcoding_slot_3_list, and transcoding_slot_3_size
        self.TRANSCODING_SLOT_3 = (self.transcoding_slot_3, self.transcoding_slot_3_list, self.transcoding_slot_3_size)
        # Define a list of transcoding slots each transcoding slot is represented as an instance variable of the class
        self.TRANSCODING_SLOT_LIST = [self.transcoding_slot_1, self.transcoding_slot_2, self.transcoding_slot_3]
        # Get a list of files in the ripping directory
        self.RIPPING_BAY_LIST = os.listdir(ripping_directory)
        # Define the name of ripping bay 1
        self.RIPPING_BAY_1 = ripping_bay_1
        # Define the name of ripping bay 1
        self.RIPPING_BAY_2 = ripping_bay_2
        # Define the name of ripping bay 1
        self.RIPPING_BAY_3 = ripping_bay_3







def TEST():
    TEST = Directories()
    print("DRIVE INFO | What you should see '('Drive size', 'Space used on Drive', 'Free space on Drive')' :  ", TEST.MAIN_DIRECTORY)
    print("COLLECTION_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.COLLECTION_DIRECTORY)
    print("COMPLETED_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.COMPLETED_DIRECTORY)
    print("QUEUED_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.QUEUED_DIRECTORY)
    print("RIPPING_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.RIPPING_DIRECTORY)
    print("TRANSCODING_DIRECTORY INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.TRANSCODING_DIRECTORY)
    print("TRANSCODING_SLOT_LIST INFO | What you should see '['A list of the Transcoding slot Directory locations']' :  ", TEST.TRANSCODING_SLOT_LIST)
    print("TRANSCODING_SLOT_1 INFO | What you should see '('drive size', 'space used on drive', 'free space on drive')' :  ", TEST.TRANSCODING_SLOT_1)
    print("TRANSCODING_SLOT_2 INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.TRANSCODING_SLOT_2)
    print("TRANSCODING_SLOT_3 INFO | What you should see '('Directory location', 'A list of all the items in the Directory', 'Directory size')' :  ", TEST.TRANSCODING_SLOT_3)
    print("RIPPING_BAY_LIST INFO | What you should see  '['A list of the Ripping Bay Directory locations']' :  ", TEST.RIPPING_BAY_LIST)
    print("RIPPING_BAY_1 INFO | What you should see '('Drive letter', 'Drive number', '[Movie thats Ripping]', 'Directory size')' :  ", TEST.RIPPING_BAY_1)
    print("RIPPING_BAY_2 INFO | What you should see '('Drive letter', 'Drive number', '[Movie thats Ripping]', 'Directory size')' :  ", TEST.RIPPING_BAY_2)
    print("RIPPING_BAY_3 INFO | What you should see '('Drive letter', 'Drive number', '[Movie thats Ripping]', 'Directory size')' :  ", TEST.RIPPING_BAY_3)

if __name__ == "__main__":
    TEST()