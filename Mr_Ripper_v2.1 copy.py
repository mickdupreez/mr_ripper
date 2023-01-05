import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time
from colorit import init_colorit, background
from PIL import Image

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    BLACK_BLACK = curses.color_pair(1)
    RED_BLACK = curses.color_pair(2)
    GREEN_BLACK = curses.color_pair(3)
    YELLOW_BLACK = curses.color_pair(4)
    BLUE_BLACK = curses.color_pair(5)
    MAGENTA_BLACK = curses.color_pair(6)
    CYAN_BLACK = curses.color_pair(7)
    WHITE_BLACK = curses.color_pair(8)
    
    while True:
        for i in range(30):
            stdscr.clear()
            color = GREEN_BLACK
            
            if i % 2 == 0:
                color = BLACK_BLACK
                
                
            
            rectangle(stdscr, 1, 1, 3, 23)
            rectangle(stdscr, 4, 1, 6, 23)
            rectangle(stdscr, 7, 1, 9, 23)
            rectangle(stdscr, 10, 1, 12, 23)
            rectangle(stdscr, 13, 1, 15, 23)
            stdscr.refresh()
            time.sleep(0.2)





wrapper(main)







