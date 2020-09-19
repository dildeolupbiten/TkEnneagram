# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .enneagram import Enneagram
from .constants import HOUSE_SYSTEMS
from .treeview import Treeview, TreeviewToplevel
from .utilities import (
    msgbox_info, convert_coordinates,
    tbutton_command, check_all_command, excepthook
)
from .modules import (
    os, dt, tk, np, ET, sys, ttk, time,
    Thread, open_new, logging, ConfigParser
)

sys.excepthook = excepthook

logging.basicConfig(
    filename="log.log",
    format="- %(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
    datefmt="%d.%m.%Y %H:%M:%S"
)


class ADB(tk.Toplevel):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ADB")
        self.resizable(width=False, height=False)
        self.icons = icons
        self.database = []
        self.category_dict = {}
        self.all_categories = {}
        self.category_names = []
        self.topframe = tk.Frame(master=self)
        self.topframe.pack()
        self.bottomframe = tk.Frame(master=self)
        self.bottomframe.pack()
        self.load_button = tk.Button(
            master=self.topframe,
            text="Load",
            width=10,
            command=lambda: Thread(target=self.load).start()
        )
        self.load_button.grid(row=0, column=0)
        self.logging_text = tk.Text(
            master=self.bottomframe,
            bg=self["bg"],
            state="disabled",
            bd=0
        )
        self.logging_text.pack()
        self.logging_text.bind(
            sequence="<Button-1>",
            func=lambda event: "break"
        )
        self.logging_text.bind(
            sequence="<Motion>",
            func=lambda event: "break"
        )
        self.logging_text.bind(
            sequence="<Button-3>",
            func=lambda event: "break"
        )
        self.open_button = tk.Button(
            master=self.bottomframe,
            text="Open",
            command=lambda: ControlPanel(
                self.database,
                self.all_categories,
                self.category_names,
                self.icons
            )
        )

    def load(self):
        self.database = []
        self.category_dict = {}
        self.logging_text["state"] = "normal"
        self.logging_text.delete("1.0", "end")
        self.logging_text["state"] = "disabled"
        self.open_button.pack_forget()
        xml_files = {
            dt.strftime(
                dt.fromtimestamp(os.stat(xml).st_mtime),
                "%d.%m.%Y"
            ): xml
            for xml in os.listdir(os.getcwd())
            if xml.endswith("xml")
        }
        if not xml_files:
            MsgBox(
                title="Warning",
                message="There is no database!",
                level="warning",
                icons=self.icons
            )
            return
        xml_files = {key: xml_files[key] for key in sorted(xml_files)}
        for xml_file in xml_files.values():
            xml_database = []
            ignored = 0
            msgbox_info(self, f"Parsing {xml_file} file...\n")
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for i in range(1000000):
                try:
                    start_stop = False
                    user_data = []
                    for gender, roddenrating, bdata, adb_link, categories in \
                            zip(
                                root[i + 2][1].findall("gender"),
                                root[i + 2][1].findall("roddenrating"),
                                root[i + 2][1].findall("bdata"),
                                root[i + 2][2].findall("adb_link"),
                                root[i + 2][3].findall("categories")
                            ):
                        name = root[i + 2][1][0].text
                        for record in self.database:
                            if name == record[1]:
                                ignored += 1
                                start_stop = True
                                break
                        if start_stop:
                            break
                        else:
                            sbdate_dmy = bdata[1].text
                            sbtime = bdata[2].text
                            jd_ut = bdata[2].get("jd_ut")
                            lat = bdata[3].get("slati")
                            lon = bdata[3].get("slong")
                            place = bdata[3].text
                            country = bdata[4].text
                            category = [
                                (
                                    categories[j].get("cat_id"),
                                    categories[j].text
                                )
                                for j in range(len(categories))
                            ]
                            for cate in category:
                                if cate[0] not in self.category_dict.keys():
                                    self.category_dict[cate[0]] = cate[1]
                            user_data.append(int(root[i + 2].get("adb_id")))
                            user_data.append(name)
                            user_data.append(gender.text)
                            user_data.append(roddenrating.text)
                            user_data.append(sbdate_dmy)
                            user_data.append(sbtime)
                            user_data.append(jd_ut)
                            user_data.append(lat)
                            user_data.append(lon)
                            user_data.append(place)
                            user_data.append(country)
                            user_data.append(adb_link.text)
                            user_data.append(category)
                            if len(user_data) != 0:
                                xml_database.append(user_data)
                except IndexError:
                    break
            try:
                msgbox_info(self, "Parsing completed.\n")
                msgbox_info(self, f"{ignored} records are ignored.\n")
                msgbox_info(self, f"{len(xml_database)} records are inserted.\n")
                self.database.extend(xml_database)
                msgbox_info(self, f"{len(self.database)} records are available.\n")
            except tk.TclError:
                return
        self.group_categories()
        self.calculate()

    def group_categories(self):
        for record in self.database:
            for category in record[-1]:
                if (category[0], category[1]) not in self.all_categories:
                    if category[1] is None:
                        pass
                    self.all_categories[(category[0], category[1])] = []
                self.all_categories[(category[0], category[1])].append(record)
        self.category_names = sorted(
            [i for i in self.category_dict.values() if i is not None]
        )

    def calculate(self):
        self.open_button.pack_forget()
        msgbox_info(self, "Calculation started.\n")
        size = len(self.database)
        received = 0
        now = time.time()
        pframe = tk.Frame(master=self)
        pbar = ttk.Progressbar(
            master=pframe,
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        pstring = tk.StringVar()
        plabel = tk.Label(master=pframe, textvariable=pstring)
        pframe.pack()
        pbar.pack(side="left")
        plabel.pack(side="left")
        for record in self.database:
            jd = float(record[6])
            lat = convert_coordinates(record[7])
            lon = convert_coordinates(record[8])
            result = Enneagram(
                jd=jd,
                lat=lat,
                lon=lon,
                hsys="P"
            )
            score = result.get_all_scores()
            dayscores = np.array(
                [v for k, v in score["sign"]["Dayscores"].items()]
            )
            effect_of_house = np.array(
                [v for k, v in score["house"]["Effect of Houses"].items()]
            )
            s = [float(i) for i in dayscores * effect_of_house][:-1]
            enneagram_type = s.index(max(s))
            try:
                right = s[enneagram_type + 1]
            except IndexError:
                right = s[0]
            left = s[enneagram_type - 1]
            enneagram_wing = right if right > left else left
            enneagram_wing = f"Type-{s.index(enneagram_wing) + 1}"
            enneagram_type = f"Type-{enneagram_type + 1}"
            record.extend([enneagram_type, enneagram_wing])
            received += 1
            if received != size:
                try:
                    pbar["value"] = received
                    pbar["maximum"] = size
                    pstring.set("{} %, {} minutes remaining.".format(
                        int(100 * received / size),
                        round(
                            (int(size /
                                 (received / (time.time() - now)))
                             - int(time.time() - now)) / 60)))
                except tk.TclError:
                    return
            else:
                pframe.destroy()
                pbar.destroy()
                plabel.destroy()
                self.open_button.pack()
                msgbox_info(self, "Calculation completed.\n")


class ControlPanel(tk.Toplevel):
    def __init__(
            self,
            database,
            all_categories,
            category_names,
            icons,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title("Control Panel")
        self.geometry("800x650")
        self.database = database
        self.all_categories = all_categories
        self.category_names = category_names
        self.icons = icons
        self.displayed_results = []
        self.selected_categories = []
        self.selected_ratings = []
        self.checkbuttons = {}
        self.menu = None
        self.msgbox_info_var = tk.StringVar()
        self.msgbox_info_var.set("0")
        self.topframe = tk.Frame(master=self)
        self.topframe.pack()
        self.midframe = tk.Frame(master=self)
        self.midframe.pack()
        self.bottomframe = tk.Frame(master=self)
        self.bottomframe.pack()
        self.columns = [
            "Adb ID", "Name", "Gender", "Rodden Rating", "Date",
            "Hour", "Julian Date", "Latitude", "Longitude", "Place",
            "Country", "Adb Link", "Category", "Type", "Wing"
        ]
        self.treeview = Treeview(
            master=self.midframe,
            columns=self.columns,
            height=5
        )
        self.treeview.bind(
            sequence="<Button-1>",
            func=lambda event: self.destroy_menu()
        )
        self.treeview.bind(
            sequence="<Button-3>",
            func=lambda event: self.button_3_on_treeview(event=event)
        )
        self.entry_button_frame = tk.Frame(master=self.topframe)
        self.entry_button_frame.grid(row=0, column=0)
        self.search_label = tk.Label(
            master=self.entry_button_frame,
            text="Search A Record By Name: ",
            fg="red"
        )
        self.search_label.grid(row=0, column=0, padx=5, sticky="w", pady=5)
        self.search_entry = tk.Entry(master=self.entry_button_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.search_func()
        )
        self.found_record = tk.Label(master=self.entry_button_frame, text="")
        self.found_record.grid(row=1, column=0, padx=5, pady=5)
        self.add_button = tk.Button(master=self.entry_button_frame, text="Add")
        self.category_label = tk.Label(
            master=self.entry_button_frame,
            text="Categories:",
            fg="red"
        )
        self.category_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.rrating_label = tk.Label(
            master=self.entry_button_frame,
            text="Rodden Rating:",
            fg="red"
        )
        self.rrating_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.category_button = tk.Button(
            master=self.entry_button_frame,
            text="Select",
            command=self.select_categories
        )
        self.category_button.grid(row=2, column=1, padx=5, pady=5)
        self.rating_button = tk.Button(
            master=self.entry_button_frame,
            text="Select",
            command=self.select_ratings
        )
        self.rating_button.grid(row=3, column=1, padx=5, pady=5)
        self.create_checkbutton()
        self.display_button = tk.Button(
            master=self.topframe,
            text="Display Records",
            command=self.display_results
        )
        self.display_button.grid(row=10, column=0, columnspan=4, pady=10)
        self.total_msgbox_info = tk.Label(master=self.bottomframe, text="Total = ")
        self.total_msgbox_info.grid(row=0, column=0)
        self.msgbox_info = tk.Label(
            master=self.bottomframe,
            textvariable=self.msgbox_info_var
        )
        self.msgbox_info.grid(row=0, column=1)
        self.resizable(width=False, height=False)

    def add_command(self, record):
        if record in self.displayed_results:
            pass
        else:
            num = len(self.treeview.get_children()) + 1
            self.treeview.insert("", num, values=[col for col in record])
            self.displayed_results.append(record)
            self.msgbox_info_var.set(len(self.displayed_results))
        self.add_button.grid_forget()
        self.found_record.configure(text="")
        self.search_entry.delete("0", "end")

    def search_func(self):
        self.update()
        save_record = ""
        count = 0
        for record in self.database:
            if self.search_entry.get() == record[1]:
                index = self.database.index(record)
                count += 1
                self.found_record.configure(text=f"Record Found = {count}")
                self.add_button.grid(row=1, column=1, padx=5, pady=5)
                self.add_button.configure(
                    command=lambda: self.add_command(record=self.database[index])
                )
                save_record += self.database[index][1]
        if save_record != self.search_entry.get() or \
                save_record == self.search_entry.get() == "":
            self.found_record.configure(text="")
            self.add_button.grid_forget()

    def create_checkbutton(self):
        check_frame = tk.Frame(master=self.topframe)
        check_frame.grid(row=0, column=2)
        for i, j in enumerate(
                (
                    "event",
                    "human",
                    "male",
                    "female",
                    "North Hemisphere",
                    "South Hemisphere"
                 )
        ):
            var = tk.StringVar()
            var.set(value="0")
            checkbutton = tk.Checkbutton(
                master=check_frame,
                text=f"Do not display {j} charts.",
                variable=var)
            checkbutton.grid(row=i, column=2, columnspan=2, sticky="w")
            self.checkbuttons[j] = [var, checkbutton]

    def south_north_check(self, item):
        north = self.checkbuttons["North Hemisphere"][0]
        south = self.checkbuttons["South Hemisphere"][0]
        if north.get() == "1" and south.get() == "0":
            if "n" in item[7]:
                pass
            else:
                self.insert_to_treeview(item)
        elif north.get() == "0" and south.get() == "1":
            if "s" in item[7]:
                pass
            else:
                self.insert_to_treeview(item)
        elif north.get() == "0" and south.get() == "0":
            self.insert_to_treeview(item)
        elif north.get() == "1" and south.get() == "1":
            pass

    def male_female_check(self, item):
        male = self.checkbuttons["male"][0]
        female = self.checkbuttons["female"][0]
        if male.get() == "1" and female.get() == "0":
            if item[2] == "M":
                pass
            else:
                self.south_north_check(item)
        elif male.get() == "0" and female.get() == "1":
            if item[2] == "F":
                pass
            else:
                self.south_north_check(item)
        elif male.get() == "0" and female.get() == "0":
            self.south_north_check(item)
        elif male.get() == "1" and female.get() == "1":
            if item[2] == "F" or item[2] == "M":
                pass
            else:
                self.south_north_check(item)

    def insert_to_treeview(self, item):
        num = len(self.treeview.get_children()) + 1
        self.treeview.insert("", num, values=[col for col in item])
        self.msgbox_info_var.set(len(self.displayed_results))
        self.displayed_results.append(item)
        self.update()

    def display_results(self):
        self.treeview.delete(*self.treeview.get_children())
        self.displayed_results = []
        event = self.checkbuttons["event"][0]
        human = self.checkbuttons["human"][0]
        for key, value in self.all_categories.items():
            if key[1] in self.selected_categories:
                for item in value:
                    if item[3] in self.selected_ratings:
                        if item in self.displayed_results:
                            pass
                        else:
                            if (
                                    event.get() == "0"
                                    and
                                    human.get() == "0"
                            ):
                                if item[0] == 3546 or item[0] == 68092:
                                    pass
                                else:
                                    self.male_female_check(item)
                            elif (
                                    event.get() == "1"
                                    and
                                    human.get() == "0"
                            ):
                                if item[2] == "N/A":
                                    pass
                                elif item[0] == 3546:
                                    pass
                                else:
                                    self.male_female_check(item)
                            elif (
                                    event.get() == "0"
                                    and
                                    human.get() == "1"
                            ):
                                if item[2] != "N/A" or item[0] == 68092:
                                    pass
                                else:
                                    self.south_north_check(item)
                            elif (
                                    event.get() == "1"
                                    and
                                    human.get() == "1"
                            ):
                                pass
        self.msgbox_info_var.set(len(self.displayed_results))
        self.update()
        if len(self.displayed_results) == 0:
            MsgBox(
                title="Info",
                message="No record is inserted.",
                icons=self.icons,
                level="info"
            )
        elif len(self.displayed_results) == 1:
            MsgBox(
                title="Info",
                message="1 record is inserted.",
                icons=self.icons,
                level="info"
            )
        else:
            MsgBox(
                title="Display Records",
                message=f"{len(self.displayed_results)} "
                        f"records are inserted.",
                icons=self.icons,
                level="info"
            )
        self.update()

    def select_ratings(self):
        self.selected_ratings = []
        toplevel = tk.Toplevel()
        toplevel.geometry("300x250")
        toplevel.resizable(width=False, height=False)
        toplevel.title("Select Rodden Ratings")
        toplevel.update()
        rating_frame = tk.Frame(master=toplevel)
        rating_frame.pack(side="top")
        button_frame = tk.Frame(master=toplevel)
        button_frame.pack(side="bottom")
        tbutton = tk.Button(master=button_frame, text="Apply")
        tbutton.pack()
        cvar_list = []
        checkbutton_list = []
        check_all = tk.BooleanVar()
        check_uncheck = tk.Checkbutton(
            master=rating_frame,
            text="Check/Uncheck All",
            variable=check_all
        )
        check_all.set(False)
        check_uncheck.grid(row=0, column=0, sticky="nw")
        for num, c in enumerate(
                ["AA", "A", "B", "C", "DD", "X", "XX", "AX"],
                1
        ):
            self.update()
            rating = c
            cvar = tk.BooleanVar()
            cvar_list.append([cvar, rating])
            checkbutton = tk.Checkbutton(
                master=rating_frame,
                text=rating,
                variable=cvar
            )
            checkbutton_list.append(checkbutton)
            cvar.set(False)
            checkbutton.grid(row=num, column=0, sticky="nw")
        tbutton.configure(
            command=lambda: tbutton_command(
                cvar_list,
                toplevel,
                self.selected_ratings
            )
        )
        check_uncheck.configure(
            command=lambda: check_all_command(
                check_all,
                cvar_list,
                checkbutton_list
            )
        )

    def select_categories(self):
        self.selected_categories = []
        toplevel = tk.Toplevel()
        toplevel.title("Select Categories")
        toplevel.resizable(width=False, height=False)
        toplevel.update()
        canvas_frame = tk.Frame(master=toplevel)
        canvas_frame.pack(side="top")
        button_frame = tk.Frame(master=toplevel)
        button_frame.pack(side="bottom")
        tcanvas = tk.Canvas(master=canvas_frame)
        tframe = tk.Frame(master=tcanvas)
        tscrollbar = tk.Scrollbar(
            master=canvas_frame,
            orient="vertical",
            command=tcanvas.yview
        )
        tcanvas.configure(yscrollcommand=tscrollbar.set)
        tscrollbar.pack(side="right", fill="y")
        tcanvas.pack()
        tcanvas.create_window((4, 4), window=tframe, anchor="nw")
        tframe.bind(
            "<Configure>",
            lambda event: tcanvas.configure(scrollregion=tcanvas.bbox("all"))
        )
        tbutton = tk.Button(master=button_frame, text="Apply")
        tbutton.pack()
        cvar_list = []
        checkbutton_list = []
        check_all = tk.BooleanVar()
        check_uncheck_ = tk.Checkbutton(
            master=tframe,
            text="Check/Uncheck All",
            variable=check_all
        )
        check_all.set(False)
        check_uncheck_.grid(row=0, column=0, sticky="nw")
        for num, category in enumerate(self.category_names, 1):
            self.update()
            cvar = tk.BooleanVar()
            cvar_list.append([cvar, category])
            checkbutton = tk.Checkbutton(
                master=tframe,
                text=category,
                variable=cvar
            )
            checkbutton_list.append(checkbutton)
            cvar.set(False)
            checkbutton.grid(row=num, column=0, sticky="nw")
        tbutton.configure(
            command=lambda: tbutton_command(
                cvar_list,
                toplevel,
                self.selected_categories
            )
        )
        check_uncheck_.configure(
            command=lambda: check_all_command(
                check_all,
                cvar_list,
                checkbutton_list
            )
        )
        self.update()

    def button_3_open_scores(self):
        selected = self.treeview.selection()
        if not selected:
            pass
        else:
            values = self.treeview.item(selected)["values"]
            config = ConfigParser()
            config.read("defaults.ini")
            algorithm = config["ALGORITHM"]["selected"]
            hsys = HOUSE_SYSTEMS[config["HOUSE SYSTEM"]["selected"]]
            info = {
                "Name": values[1],
                "Gender": values[2],
                "Date": dt.strptime(
                    values[4],
                    "%d %B %Y"
                ).strftime("%d.%m.%Y"),
                "Time": values[5],
                "Latitude": str(round(convert_coordinates(values[7]), 2)),
                "Longitude": str(round(convert_coordinates(values[8]), 2))
            }
            date = dt.strptime(values[4], "%d %B %Y")
            hour, minute = (int(i) for i in values[5].split(":"))
            user = Enneagram(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=hour,
                minute=minute,
                second=0,
                lat=float(info["Latitude"]),
                lon=float(info["Longitude"]),
                hsys=hsys,
                icons=self.icons
            )
            scores = user.get_all_scores()
            TreeviewToplevel(
                values=scores,
                info=info,
                hsys=hsys,
                icons=self.icons,
                patterns=user.patterns,
                algorithm=algorithm
            )

    def button_3_on_treeview(self, event):
        self.destroy_menu()
        self.menu = tk.Menu(master=None, tearoff=False)
        """self.menu.add_command(
            label="Remove",
            command=lambda: button_3_remove(treeview)
        )"""
        self.menu.add_command(
            label="Open ADB Page",
            command=self.button_3_open_url
        )
        self.menu.add_command(
            label="Open Enneagram Scores",
            command=self.button_3_open_scores
        )
        self.menu.post(event.x_root, event.y_root)

    def destroy_menu(self):
        if self.menu:
            self.menu.destroy()

    def button_3_open_url(self):
        selected = self.treeview.selection()
        if not selected:
            pass
        else:
            values = self.treeview.item(selected)["values"]
            open_new(values[11])