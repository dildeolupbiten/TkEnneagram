# -*- coding: utf-8 -*-

from .modules import tk
from .house_systems import HouseSystemsToplevel


class Menu(tk.Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.add_command(
            label="House Systems",
            command=HouseSystemsToplevel
        )
