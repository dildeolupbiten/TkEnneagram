# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .enneagram import Enneagram
from .constants import HOUSE_SYSTEMS
from .treeview import TreeviewToplevel
from .modules import dt, tk, ttk, ConfigParser, Nominatim


class UserEntryForm(tk.Toplevel):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("User Entry Form")
        self.geometry("500x500")
        self.resizable(width=False, height=False)
        self.icons = icons
        self.style = ttk.Style()
        self.entry_names = [
            "Name",
            "Gender",
            ["Day", "Month", "Year"],
            ["Hour", "Minute"],
            ["Place"],
            ["Latitude", "Longitude"]
        ]
        self.entries = {}
        self.var = tk.StringVar()
        for i, j in enumerate(self.entry_names):
            frame = tk.Frame(master=self)
            frame.pack()
            if isinstance(j, list):
                for k, m in enumerate(j):
                    sub_frame = tk.Frame(master=frame)
                    sub_frame.pack(side="left", padx=5)
                    label = tk.Label(master=sub_frame, text=m)
                    label.pack()
                    if m in ["Month", "Day", "Hour", "Minute"]:
                        entry = ttk.Entry(
                            master=sub_frame,
                            width=2,
                            style=f"{m}.TEntry"
                        )
                        entry.bind(
                            sequence="<KeyRelease>",
                            func=lambda event, widget=entry: self.max_char(
                                widget=widget,
                                limit=2
                            )
                        )
                        entry.pack()
                        self.entries[m] = entry
                    elif m == "Year":
                        entry = ttk.Entry(
                            master=sub_frame,
                            width=4,
                            style=f"{m}.TEntry"
                        )
                        entry.bind(
                            sequence="<KeyRelease>",
                            func=lambda event, widget=entry: self.max_char(
                                widget=widget,
                                limit=4
                            )
                        )
                        entry.pack()
                        self.entries[m] = entry
                    else:
                        if m == "Place":
                            width = 50
                            entry = ttk.Combobox(
                                master=sub_frame,
                                width=width,
                                style="TCombobox",
                                values=[]
                            )
                            entry.bind(
                                sequence="<Return>",
                                func=lambda event, widget=entry:
                                self.find_coordinates(
                                    widget=widget
                                )
                            )
                            entry.bind(
                                sequence="<KeyRelease>",
                                func=lambda event, widget=entry: self.control(
                                    widget=widget
                                )
                            )
                        else:
                            width = 10
                            entry = ttk.Entry(
                                master=sub_frame,
                                width=width,
                                style=f"{m}.TEntry",
                            )
                            entry.bind(
                                sequence="<KeyRelease>",
                                func=lambda event, widget=entry: self.max_char(
                                    widget=widget
                                )
                            )
                    entry.pack()
                    self.entries[m] = entry
            else:
                label = tk.Label(master=frame, text=j)
                label.pack()
                if i == 0:
                    entry = ttk.Entry(frame, style=f"{j}.TEntry")
                    entry.bind(
                        sequence="<KeyRelease>",
                        func=lambda event, widget=entry: self.control(
                            widget=widget
                        )
                    )
                    entry.pack()
                    self.entries[j] = entry
                elif i == 1:
                    option = tk.OptionMenu(frame, self.var, "M", "F", "N/A")
                    option.pack()
                    self.entries[j] = self.var
        self.button = tk.Button(
            master=self,
            text="Calculate",
            command=self.calculate
        )
        self.button.pack(pady=50)

    def find_coordinates(self, widget):
        nominatim = Nominatim(user_agent=__name__)
        try:
            locations = {
                i.address: (i.latitude, i.longitude)
                for i in nominatim.geocode(widget.get(), exactly_one=False)
            }
            widget.config(values=[k for k in locations])
            widget.event_generate("<Down>")
            widget.bind(
                "<<ComboboxSelected>>",
                lambda event: self.insert_coordinates(widget, locations)
            )
        except:
            MsgBox(
                title="Info",
                message="Geocoding service is \n"
                        "not available now.\nTry again.",
                icons=self.icons,
                level="info"
            )

    def insert_coordinates(self, widget, locations):
        lat, lon = locations[widget.get()]
        self.entries["Latitude"].delete("0", "end")
        self.entries["Longitude"].delete("0", "end")
        self.entries["Latitude"].insert("insert", lat)
        self.entries["Longitude"].insert("insert", lon)
        for i in ("Latitude", "Longitude"):
            self.style.configure(
                self.entries[i].cget("style"),
                fieldbackground="white"
            )

    def control(self, widget):
        if widget.get():
            self.style.configure(
                widget.cget("style"),
                fieldbackground="white"
            )

    def max_char(self, widget, limit=0):
        if limit:
            if len(widget.get()) > limit:
                widget.delete(str(limit))
        if widget.get():
            try:
                float(widget.get())
                self.style.configure(
                    widget.cget("style"),
                    fieldbackground="white"
                )
            except ValueError:
                self.style.configure(
                    widget.cget("style"),
                    fieldbackground="red"
                )
        else:
            self.style.configure(
                widget.cget("style"),
                fieldbackground="white"
            )

    def calculate(self):
        config = ConfigParser()
        config.read("defaults.ini")
        algorithm = config["ALGORITHM"]["selected"]
        hsys = HOUSE_SYSTEMS[config["HOUSE SYSTEM"]["selected"]]
        for k, v in self.entries.items():
            if k != "Place":
                if not v.get():
                    if isinstance(v, ttk.Entry):
                        self.style.configure(
                            v.cget("style"),
                            fieldbackground="red"
                        )
        for k, v in self.entries.items():
            if k in [
                "Day", "Month", "Year", "Hour",
                "Minute", "Latitude", "Longitude"
            ]:
                if not self.check(k):
                    return
        try:
            dt.strptime(
                f'{int(self.entries["Year"].get())}.'
                f'{int(self.entries["Month"].get())}.'
                f'{int(self.entries["Day"].get())} '
                f'{int(self.entries["Hour"].get())}:'
                f'{int(self.entries["Minute"].get())}',
                "%Y.%m.%d %H:%M"
            )
        except:
            MsgBox(
                title="warning",
                message="You didn't fill the datetime correctly.",
                level="warning",
                icons=self.icons
            )
            return
        if all(v.get() for k, v in self.entries.items() if k != "Place"):
            try:
                user = Enneagram(
                    year=int(self.entries["Year"].get()),
                    month=int(self.entries["Month"].get()),
                    day=int(self.entries["Day"].get()),
                    hour=int(self.entries["Hour"].get()),
                    minute=int(self.entries["Minute"].get()),
                    second=0,
                    lat=float(self.entries["Latitude"].get()),
                    lon=float(self.entries["Longitude"].get()),
                    hsys=hsys,
                    icons=self.icons
                )
            except ValueError:
                MsgBox(
                    title="warning",
                    message="The coordinates should be given \nin degrees. "
                            "\nThey are out ouf bounds.",
                    level="warning",
                    icons=self.icons
                )
                return
            info = {k: v for k, v in self.entries.items() if k != "Place"}
            info = {
                "Name": info["Name"].get(),
                "Gender": info["Gender"].get(),
                "Date": f"{info['Day'].get()}."
                        f"{info['Month'].get()}."
                        f"{info['Year'].get()}",
                "Time": f"{info['Hour'].get().zfill(2)}:"
                        f"{info['Minute'].get().zfill(2)}",
                "Latitude": info["Latitude"].get(),
                "Longitude": info["Longitude"].get()
            }
            scores = user.get_all_scores()
            if not scores:
                MsgBox(
                    icons=self.icons,
                    title="Warning",
                    message="You entered wrong key!",
                    level="warning"
                )
                return
            TreeviewToplevel(
                values=scores,
                info=info,
                hsys=hsys,
                icons=self.icons,
                patterns=user.patterns,
                algorithm=algorithm
            )
        else:
            MsgBox(
                title="warning",
                message="You didn't fill all fields.",
                level="warning",
                icons=self.icons
            )

    def check(self, name):
        try:
            float(self.entries[name].get())
            return True
        except ValueError:
            MsgBox(
                title="warning",
                message=f"You didn't fill the {name.lower()} correctly.",
                level="warning",
                icons=self.icons
            )
            return
