import time
import threading
from Directories import Directories
from Rip_And_Scrape import Rip_And_Scrape
from Transcode import Transcode
from Mr_Ripper_GUI import GUI


def Rip_Scrape_Transcode():
    threading.Thread(target=GUI).start()

    def SLOT_1():
        while True:
            if Directories().queued_directory_list:
                slot = Directories().transcoding_slot_1
                Transcode(slot)
            else:
                time.sleep(10)

    def SLOT_2():
        while True:
            if Directories().queued_directory_list:
                slot = Directories().transcoding_slot_2
                Transcode(slot)
            else:
                time.sleep(10)

    def SLOT_3():
        while True:
            if Directories().queued_directory_list:
                slot = Directories().transcoding_slot_3
                Transcode(slot)
            else:
                time.sleep(10)

    def BAY1():
        while True:
            TARGET = Directories().RIPPING_BAY_1
            if not TARGET[0]:
                pass
            else:
                BAY = Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2])
                BAY.Rip()
            time.sleep(10)

    def BAY2():
        while True:
            TARGET = Directories().RIPPING_BAY_2
            if not TARGET[0]:
                pass
            else:
                BAY = Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2])
                BAY.Rip()
            time.sleep(10)

    def BAY3():
        while True:
            TARGET = Directories().RIPPING_BAY_3
            if not TARGET[0]:
                pass
            else:
                BAY = Rip_And_Scrape(TARGET[0], TARGET[1], TARGET[2])
                BAY.Rip()
            time.sleep(10)

    threading.Thread(target=SLOT_1, daemon=True).start()
    time.sleep(2)
    threading.Thread(target=SLOT_2, daemon=True).start()
    time.sleep(2)
    threading.Thread(target=SLOT_3, daemon=True).start()
    time.sleep(2)
    threading.Thread(target=BAY1, daemon=True).start()
    time.sleep(2)
    threading.Thread(target=BAY2, daemon=True).start()
    time.sleep(2)
    threading.Thread(target=BAY3, daemon=True).start()
    time.sleep(15)


#! TESTING !#
if __name__ == "__main__":
    Rip_Scrape_Transcode()
