# -*- coding: utf-8 -*-

__version__ = "1.0.0"

from .menu import Menu
from .modules import tk
from .utilities import create_image_files
from .user_entry_form import UserEntryForm


def main():
    root = tk.Tk()
    root.title("TkEnneagram")
    root.geometry("500x500")
    root.resizable(width=False, height=False)
    icons = create_image_files(path="Icons")
    Menu(master=root)
    UserEntryForm(master=root, icons=icons)
    root.mainloop()
    
    
main()