# -*- coding: utf-8 -*-

from .about import About
from .modules import os, tk
from .database import Database
from .user_entry_form import UserEntryForm
from .constants import HOUSE_SYSTEMS, PLANETS
from .selection import SingleSelection, MultipleSelection


class Menu(tk.Menu):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.add_command(
            label="Database",
            command=lambda: Database(
                root=self.master,
                icons=icons
            )
        )
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
