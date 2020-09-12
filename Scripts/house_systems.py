# -*- coding: utf-8 -*-

from .constants import HOUSE_SYSTEMS
from .modules import tk, ConfigParser


class HouseSystemsToplevel(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("House Systems")
        self.geometry("200x200")
        self.resizable(width=False, height=False)
        self.hsys_frame = tk.Frame(master=self)
        self.hsys_frame.pack(side="top")
        self.button_frame = tk.Frame(master=self)
        self.button_frame.pack(side="bottom")
        self.checkbuttons = {}
        for i, j in enumerate(HOUSE_SYSTEMS):
            var = tk.StringVar()
            var.set(value="0")
            checkbutton = tk.Checkbutton(
                master=self.hsys_frame,
                text=j,
                variable=var
            )
            checkbutton.grid(row=i, column=0, sticky="w")
            self.checkbuttons[j] = [checkbutton, var]
            self.configure_checkbuttons(hsys=j)
        apply_button = tk.Button(
            master=self.button_frame,
            text="Apply",
            command=self.change_hsys
        )
        apply_button.pack()

    def change_hsys(self):
        for i in HOUSE_SYSTEMS:
            if self.checkbuttons[i][1].get() == "1":
                with open("default.ini", "w") as f:
                    config = ConfigParser()
                    config["HOUSE SYSTEM"] = {"hsys": HOUSE_SYSTEMS[i]}
                    config.write(f)
        self.destroy()

    def configure_checkbuttons(self, hsys):
        return self.checkbuttons[hsys][0].configure(
            command=lambda: self.check_uncheck(hsys=hsys)
        )

    def check_uncheck(self, hsys):
        for i in HOUSE_SYSTEMS:
            if i != hsys:
                self.checkbuttons[i][1].set("0")
                self.checkbuttons[i][0].configure(
                    variable=self.checkbuttons[i][1]
                )
