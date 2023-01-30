import os
import time
import curses
import shutil
from Directories import Directories

from curses import wrapper
from curses.textpad import Textbox, rectangle




def term_ui():
    def terminal_ui(stdscr):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
        RED = curses.color_pair(1)
        GREEN = curses.color_pair(2)
        YELLOW = curses.color_pair(3)
        BLUE = curses.color_pair(4)
        MAGENTA = curses.color_pair(5)
        CYAN = curses.color_pair(6)
        WHITE = curses.color_pair(7)
        BLACK = curses.color_pair(8)
        def main_box():
            stdscr.addstr(
                1,
                1,
                "Mr Ripper 2.2.0 https://github.com/mickdupreez/mr_ripper|",
                BLUE | curses.A_BOLD,
            )
            if os.listdir(Directories().Ripping_Dir) == [] and os.listdir(Directories().Transcoding_Dir) != []:
                stdscr.addstr(
                    1,
                    65,
                    "!!! TRANSCODING IN PROGRES PLEASE WAIT !!!",
                    RED | curses.A_BOLD,
                )
            if os.listdir(Directories().Ripping_Dir) != [] and os.listdir(Directories().Transcoding_Dir) == []:
                stdscr.addstr(
                    1,
                    68,
                    "!!! RIPPING IN PROGRES PLEASE WAIT !!!",
                    RED | curses.A_BOLD,
                )
            if os.listdir(Directories().Ripping_Dir) != [] and os.listdir(Directories().Transcoding_Dir) != []:
                stdscr.addstr(
                    1,
                    62,
                    "!!! RIP AND TRANSCODE IN PROGRESS PLEASE WAIT !!!",
                    RED | curses.A_BOLD,
                )
            if os.listdir(Directories().Ripping_Dir) == [] and os.listdir(Directories().Transcoding_Dir) == []:
                stdscr.addstr(
                    1,
                    65,
                    "!!! INSERT A DVD OR BLURAY TO GET STARTED !!!",
                    GREEN | curses.A_BOLD,
                )
            rectangle(stdscr, 0, 0, 28, 115)
        def get_directory_size(path):
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
        def get_storage_size(file_path):
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
        def stats_box():
            (
                total,
                used,
                free,
            ) = get_storage_size("README.md")
            stdscr.addstr(
                19, 12, "- Directory Sizes and stats -", BLUE | curses.A_BOLD
            )
            stdscr.addstr(
                20,
                2,
                f"Free space on Drive:      {free} out of {total}",
                GREEN | curses.A_BOLD,
            )
            stdscr.addstr(
                21,
                2,
                f"Drive space used:         {get_directory_size('.')} out of {total}",
                GREEN | curses.A_BOLD,
            )
            stdscr.addstr(
                22,
                2,
                f"Ripping Directory:        {get_directory_size(Directories().Ripping_Dir)} out of {get_directory_size('.')}",
                GREEN | curses.A_BOLD,
            )
            stdscr.addstr(
                23,
                2,
                f"Uncompressed Directory:   {get_directory_size(Directories().Queued_Dir)} out of {get_directory_size('.')}",
                GREEN | curses.A_BOLD,
            )
            stdscr.addstr(
                24,
                2,
                f"Transcoding Directory:    {get_directory_size(Directories().Transcoding_Dir)} out of {get_directory_size('.')}",
                GREEN | curses.A_BOLD,
            )
            stdscr.addstr(
                25,
                2,
                f"Compressed Directory:     {get_directory_size(Directories().Completed_Dir)} out of {get_directory_size('.')}",
                GREEN | curses.A_BOLD,
            )
            stdscr.addstr(
                26,
                2,
                f"Plex Directory:           {get_directory_size(Directories().Collection_Dir)} out of {get_directory_size('.')}",
                GREEN | curses.A_BOLD,
            )
            rectangle(stdscr, 18, 1, 27, 56)
        def temp_box():
            stdscr.addstr(
                3, 14, "- Movies That Are Being Ripped -", MAGENTA | curses.A_BOLD
            )
            stdscr.addstr(
                4, 27, get_directory_size(Directories().Ripping_Dir), GREEN | curses.A_BOLD
            )
            rectangle(stdscr, 5, 1, 9, 56)
            rectangle(stdscr, 2, 1, 9, 56)
            row = 5
            col = 2
            for i in os.listdir(Directories().Ripping_Dir):
                word = i
                row = row + 1
                stdscr.addstr(row, col, word, RED | curses.A_BOLD)
        def transcoding_box():
            stdscr.addstr(
                11, 14, "- Movies That Are Transcoding -", YELLOW | curses.A_BOLD
            )
            stdscr.addstr(
                12, 27, get_directory_size(Directories().Transcoding_Dir), GREEN | curses.A_BOLD
            )
            rectangle(stdscr, 13, 1, 17, 56)
            rectangle(stdscr, 10, 1, 17, 56)
            row = 13
            col = 2
            for i in os.listdir(Directories().Transcoding_Dir):
                word = i
                row = row + 1
                stdscr.addstr(row, col, word, RED | curses.A_BOLD)
        def uncompressed_box():
            stdscr.addstr(
                3,
                65,
                "- Movies That Are Queued For Transcoding -",
                CYAN | curses.A_BOLD,
            )
            stdscr.addstr(
                4,
                83,
                get_directory_size(Directories().Queued_Dir),
                GREEN | curses.A_BOLD,
            )
            rectangle(stdscr, 5, 57, 27, 114)
            rectangle(stdscr, 2, 57, 27, 114)
            row = 5
            col = 58
            for i in os.listdir(Directories().Queued_Dir):
                time.sleep(0.1)
                word = i
                row = row + 1
                stdscr.addstr(row, col, word, RED | curses.A_BOLD)
        count = 0
        while True:
            time.sleep(0.3)
            RED = curses.color_pair(1)
            stdscr.clear()
            count = count + 1
            if count % 2 == 0:
                RED = BLACK
            main_box()
            temp_box()
            transcoding_box()
            stats_box()
            uncompressed_box()
            stdscr.refresh()
    curses.wrapper(terminal_ui)
    
    
    
    
while True:
    term_ui()