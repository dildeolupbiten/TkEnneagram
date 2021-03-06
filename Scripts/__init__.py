# -*- coding: utf-8 -*-

from .menu import Menu
from .modules import tk, logging
from .utilities import create_image_files, load_defaults

logging.basicConfig(
    filename="log.log",
    format="- %(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
    datefmt="%d.%m.%Y %H:%M:%S"
)
logging.info("Session started")


def main():
    root = tk.Tk()
    root.title("TkEnneagram")
    root.geometry("800x650")
    root.resizable(width=False, height=False)
    icons = create_image_files(path="Icons")
    Menu(master=root, icons=icons)
    load_defaults()
    root.mainloop()
