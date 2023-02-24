import os
import subprocess
import time
import shutil
import threading
from Directories import Directories


class Transcode:
    def __init__(self, slot):
        input_file = None
        slot_list = os.listdir(slot)
        if not os.listdir(slot) and Directories().queued_directory_list:
            file_in_que = f"{Directories().queued_directory}{Directories().queued_directory_list[0]}"
            shutil.move(file_in_que, slot)
            target_file = Directories().get_directory_size(slot)
            target_file_size = float(target_file[:-3])
            input_file = None
            slot_list = os.listdir(slot)
            for file in os.listdir(f"{slot}/{slot_list[0]}"):
                if file.endswith(".mkv"):
                    input_file = f"{slot}/{slot_list[0]}/{file}"
                    output_file = f"{slot}/{slot_list[0]}/{slot_list[0]}.mkv"
                    command = [
                        "HandBrakeCLI.exe",
                        "--preset-import-file",
                        "profile.json",
                        "-Z",
                        "PLEX",
                        "-i",
                        input_file,
                        "-o",
                        output_file,
                    ]
                    if target_file_size < 20:
                        os.rename(input_file, output_file)
                    else:
                        subprocess.run(
                            command,
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        os.remove(f"{input_file}")
                    shutil.move(
                        f"{slot}/{slot_list[0]}", Directories().completed_directory
                    )
        else:
            input_file = None
            output_file = None
        self.slot = slot
        self.movie_name = slot_list[0]
        self.input_file = input_file
        self.output_file = output_file


def Transcode_Testing():
    def SLOT_1():
        while True:
            if Directories().queued_directory_list:
                slot = Directories().transcoding_slot_1
                slot1 = Transcode(slot)
                print(
                    "Transcode on Slot 1 completed successfully :\n",
                    f"Slot : {slot1.slot}",
                    f"File Name : {slot1.movie_name}\n",
                    f"Input File : {slot1.input_file}\n",
                    f"Output File : {slot1.output_file}\n",
                )
            else:
                time.sleep(10)

    threading.Thread(target=SLOT_1).start()
    time.sleep(3)

    def SLOT_2():
        while True:
            if Directories().queued_directory_list:
                slot = Directories().transcoding_slot_2
                slot2 = Transcode(slot)
                print(
                    "Transcode on Slot 2 completed successfully :\n",
                    f"Slot : {slot2.slot}\n",
                    f"File Name : {slot2.movie_name}\n",
                    f"Input File : {slot2.input_file}\n",
                    f"Output File : {slot2.output_file}\n",
                )
            else:
                time.sleep(10)

    threading.Thread(target=SLOT_2).start()
    time.sleep(3)

    def SLOT_3():
        while True:
            if Directories().queued_directory_list:
                slot = Directories().transcoding_slot_3
                slot3 = Transcode(slot)
                print(
                    "Transcode on Slot 3 completed successfully :\n",
                    f"Slot : {slot3.slot}\n",
                    f"File Name : {slot3.movie_name}\n",
                    f"Input File : {slot3.input_file}\n",
                    f"Output File : {slot3.output_file}\n",
                )
            else:
                time.sleep(10)

    threading.Thread(target=SLOT_3).start()
    time.sleep(10)


if __name__ == "__main__":
    Transcode_Testing()
