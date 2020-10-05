# -*- coding: utf-8 -*-

from .about import About
from .database import Database
from .modules import os, tk, Thread
from .utilities import add_category
from .user_entry_form import UserEntryForm
from .constants import HOUSE_SYSTEMS, PLANETS
from .selection import SingleSelection, MultipleSelection


class Menu(tk.Menu):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.database = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Database", menu=self.database)
        self.add_command(
            label="User Entry",
            command=lambda: UserEntryForm(
                icons=icons
            )
        )
        self.select = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Select", menu=self.select)
        self.help = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Help", menu=self.help)
        self.database.add_command(
            label="Open",
            command=lambda: Database(
                root=self.master,
                icons=icons
            )        
        )
        self.database.add_command(
            label="Add Category",
            command=lambda: Thread(
                target=lambda: add_category(
                    root=self.master,
                    icons=icons
                )
            ).start()
        )        
        self.select.add_command(
            label="House System",
            command=lambda: SingleSelection(
                title="House System",
                catalogue=HOUSE_SYSTEMS
            )
        )
        self.select.add_command(
            label="Planets",
            command=lambda: MultipleSelection(
                title="Planets",
                catalogue=[i for i in PLANETS if i not in ["Asc", "MC"]]
            )
        )
        self.select.add_command(
            label="Algorithm",
            command=lambda: SingleSelection(
                title="Algorithm",
                catalogue=os.listdir("Algorithms")
            )
        )
        self.help.add_command(
            label="About",
            command=About
        )
