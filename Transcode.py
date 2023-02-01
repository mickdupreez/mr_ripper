import os
import subprocess
import time
import shutil
import threading
from Directories import Directories


class Transcode:
    """
    This class provides methods for moving files from a queued directory to a slot directory,
    and transcoding the movie file in the slot directory.
    The target file is moved to a completed directory after transcoding.
    """

    def __init__(self, slot):
        """
        Constructor method to initialize the slot, queued directory, list of files in the queued directory,
        and list of files in the slot directory.
        It also performs the file movement operations.

        Args:
        slot (str): The path to the slot directory.

        Returns: None
        """
        # Get the queued directory and list of files in the queued directory
        self.queue = Directories().queued_directory
        self.queue_list = Directories().queued_directory_list
        # Get the slot directory
        self.slot = slot
        # Get the list of files in the slot directory
        self.slot_list = os.listdir(self.slot)
        # Check if there are files in the queue and if the slot is empty
        if self.queue_list and not self.slot_list:
            # Get the first file in the queue
            self.title = self.queue_list[0]
            # Get the target directory for the file in the queue
            self.target_dir = f"{self.queue}{self.title}"
            # Get the size of the target directory
            self.target_dir_size = sum(
                os.path.getsize(os.path.join(self.target_dir, f))
                for f in os.listdir(self.target_dir)
            )
            # Calculate the size of the target directory in GB
            self.target_dir_size_in_gb = self.target_dir_size / (1024**3)
            self.target_dir_size_in_gb = int(self.target_dir_size_in_gb / 0.01) / 100
            # Check if the size of the target directory is greater than 20 GB
            if self.target_dir_size_in_gb < 20:
                # Rename the .mkv file in the target directory to match the title
                for file in os.listdir(self.target_dir):
                    if file.endswith(".mkv"):
                        os.rename(
                            f"{self.target_dir}/{file}",
                            f"{self.target_dir}/{self.title}.mkv",
                        )
                # Move the target directory to the completed directory
                shutil.move(self.target_dir, Directories().completed_directory)
            else:
                # Move the target directory to the slot directory
                shutil.move(self.target_dir, self.slot)

    def Transcode(self):
        # Check if there are no files in the slot directory
        if not self.slot_list:
            # Create the input directory path with the slot and title
            self.input_dir = f"{self.slot}{self.title}"
            # Loop through files in the input directory
            for file in os.listdir(self.input_dir):
                # Check if the file ends with .mkv
                if file.endswith(".mkv"):
                    # Set the input file and output file path using the input directory path and file name
                    self.input_file = f"{self.input_dir}/{file}"
                    self.output_file = f"{self.input_dir}/{self.title}.mkv"
            # Create a list of commands to be executed by the subprocess
            command = [
                "HandBrakeCLI.exe",
                "--preset-import-file",
                "profile.json",
                "-Z",
                "PLEX",
                "-i",
                self.input_file,
                "-o",
                self.output_file,
            ]
            # Run the command with subprocess and redirect stdout and stderr to DEVNULL
            subprocess.run(
                command,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # Remove the input file
            os.remove(f"{self.input_file}")
            # Move the input directory to the completed directory
            shutil.move(self.input_dir, Directories().completed_directory)


#! TESTING !#
def TESTING():
    slot1_dir = Directories().transcoding_slot_1
    slot1 = Transcode(slot1_dir)
    threading.Thread(target=slot1.Transcode).start()
    slot2_dir = Directories().transcoding_slot_2
    slot2 = Transcode(slot2_dir)
    threading.Thread(target=slot2.Transcode).start()
    slot3_dir = Directories().transcoding_slot_3
    slot3 = Transcode(slot3_dir)
    threading.Thread(target=slot3.Transcode).start()
    time.sleep(1)


#! TESTING !#
if __name__ == "__main__":
    while True:
        TESTING()
