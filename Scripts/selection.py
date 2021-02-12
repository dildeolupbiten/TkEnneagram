# -*- coding: utf-8 -*-

from .modules import tk, ConfigParser


class Selection(tk.Toplevel):
    def __init__(self, title, catalogue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.config = ConfigParser()
        self.config.read("defaults.ini")
        self.catalogue = catalogue
        self.resizable(width=False, height=False)
        self.topframe = tk.Frame(master=self)
        self.topframe.pack(side="top")
        self.bottomframe = tk.Frame(master=self)
        self.bottomframe.pack(side="bottom")
        self.checkbuttons = {}
        self.button = tk.Button(
            master=self.bottomframe,
            text="Apply",
            command=lambda: self.apply(title=title.upper())
        )
        self.button.pack()

    def apply(self, title):
        pass


class SingleSelection(Selection):
    def __init__(self, title, catalogue, *args, **kwargs):
        self.done = False
        super().__init__(
            title=title,
            catalogue=catalogue,
            *args,
            **kwargs
        )
        for i, j in enumerate(self.catalogue):
            var = tk.BooleanVar()
            if self.config[title.upper()]["selected"] == j:
                var.set(True)
            checkbutton = tk.Checkbutton(
                master=self.topframe,
                text=j,
                variable=var
            )
            checkbutton.grid(row=i, column=0, sticky="w")
            self.checkbuttons[j] = [checkbutton, var]
            self.configure_checkbuttons(option=j)
        self.wait_window()

    def apply(self, title):
        config = ConfigParser()
        config.read("defaults.ini")
        for i in self.catalogue:
            if self.checkbuttons[i][1].get():
                config[title] = {"selected": i}
                with open("defaults.ini", "w") as f:
                    config.write(f)
        self.done = True
        self.destroy()

    def configure_checkbuttons(self, option):
        return self.checkbuttons[option][0].configure(
            command=lambda: self.check_uncheck(option=option)
        )

    def check_uncheck(self, option):
        for i in self.catalogue:
            if i != option:
                self.checkbuttons[i][1].set("0")
                self.checkbuttons[i][0].configure(
                    variable=self.checkbuttons[i][1]
                )


class MultipleSelection(Selection):
    def __init__(self, title, catalogue, *args, **kwargs):
        super().__init__(
            title=title,
            catalogue=catalogue,
            *args,
            **kwargs
        )
        self.geometry("200x400")
        self.check_all = tk.BooleanVar()
        self.check_all.set(False)
        self.select_all = tk.Checkbutton(
            master=self.topframe,
            text="Check/Uncheck All",
            variable=self.check_all
        )
        self.select_all.grid(row=0, column=0, sticky="w")
        self.checkbuttons["Check/Uncheck All"] = [
            self.select_all, self.check_all
        ]
        for i, j in enumerate(catalogue):
            var = tk.BooleanVar()
            if self.config[title.upper()][j] == "true":
                var.set(True)
            else:
                var.set(False)
            checkbutton = tk.Checkbutton(
                master=self.topframe,
                text=j,
                variable=var
            )
            checkbutton.grid(row=i + 1, column=0, sticky="w")
            self.checkbuttons[j] = [checkbutton, var]
        self.check_all.set(False)
        self.select_all["command"] = self.check_all_command

    def check_all_command(self):
        if self.check_all.get():
            for values in self.checkbuttons.values():
                values[-1].set(True)
        else:
            for values in self.checkbuttons.values():
                values[-1].set(False)

    def apply(self, title):
        selected = {}
        for k, v in self.checkbuttons.items():
            if k == "Check/Uncheck All":
                continue
            if v[1].get():
                selected[k] = "true"
            else:
                selected[k] = "false"
        selected["asc"] = "true"
        selected["mc"] = "true"
        self.config[title] = selected
        with open("defaults.ini", "w") as f:
            self.config.write(f)
        self.destroy()
