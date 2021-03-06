# -*- coding: utf-8 -*-

from .about import About
from .database import Database
from .modules import os, tk, Thread
from .user_entry_form import UserEntryForm
from .constants import HOUSE_SYSTEMS, PLANETS
from .calculations import find_observed_values
from .utilities import add_category, check_update
from .selection import SingleSelection, MultipleSelection


class Menu(tk.Menu):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.database_menu = tk.Menu(master=self, tearoff=False)
        self.calculations_menu = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Database", menu=self.database_menu)
        self.add_cascade(label="Calculations", menu=self.calculations_menu)
        self.add_command(
            label="User Entry",
            command=lambda: UserEntryForm(
                icons=icons
            )
        )
        self.select_menu = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Select", menu=self.select_menu)
        self.help_menu = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Help", menu=self.help_menu)
        self.database_menu.add_command(
            label="Open",
            command=lambda: Database(
                root=self.master,
                icons=icons
            )        
        )
        self.database_menu.add_command(
            label="Add Category",
            command=lambda: Thread(
                target=lambda: add_category(
                    root=self.master,
                    icons=icons
                )
            ).start()
        )
        self.calculations_menu.add_command(
            label="Find Observed Values",
            command=lambda: find_observed_values(
                widget=self.master,
                icons=icons,
            )
        )
        self.select_menu.add_command(
            label="Category Selection",
            command=lambda: SingleSelection(
                title="Category Selection",
                catalogue=["Basic", "Advanced"]
            )
        )
        self.select_menu.add_command(
            label="House System",
            command=lambda: SingleSelection(
                title="House System",
                catalogue=HOUSE_SYSTEMS
            )
        )
        self.select_menu.add_command(
            label="Planets",
            command=lambda: MultipleSelection(
                title="Planets",
                catalogue=[i for i in PLANETS if i not in ["Asc", "MC"]]
            )
        )
        self.select_menu.add_command(
            label="Algorithm",
            command=lambda: SingleSelection(
                title="Algorithm",
                catalogue=os.listdir("Algorithms")
            )
        )
        self.help_menu.add_command(
            label="About",
            command=About
        )
        self.help_menu.add_command(
            label="Check for updates",
            command=lambda: check_update(icons=icons)
        )
