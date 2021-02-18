# -*- coding: utf-8 -*-

from .plot import Plot
from .entry import EntryFrame
from .search import SearchFrame
from .enneagram import Enneagram
from .constants import HOUSE_SYSTEMS
from .selection import SingleSelection
from .messagebox import MsgBox, ChoiceBox
from .treeview import Treeview, TreeviewToplevel
from .utilities import (
    convert_coordinates, tbutton_command,
    check_all_command, progressbar, load_database,
    from_xml
)
from .modules import (
    os, dt, tk, np, swe, ttk, json,
    time, open_new, logging, Thread, ConfigParser
)


class Database:
    def __init__(self, root, icons):
        self.icons = icons
        self.database = None
        self.category_names = []
        self.choose_operation(root=root)

    def load_database(self, root, filename):
        if filename.endswith(".xml"):
            result = self.load_adb(
                filename=os.path.join(".", "Database", filename)
            )
        else:
            result = self.load_json(
                filename=os.path.join(".", "Database", filename),
            )
        if result:
            DatabaseFrame(
                master=root,
                database=self.database,
                category_names=self.category_names,
                icons=self.icons,
            )

    def choose_operation(self, root):
        if not os.path.exists("Database"):
            os.makedirs("Database")
        if not os.listdir("Database"):
            return
        else:
            selection = SingleSelection(
                title="Database",
                catalogue=[i for i in os.listdir("Database")]
            )
            if selection.done:
                config = ConfigParser()
                config.read("defaults.ini")
                filename = config["DATABASE"]["selected"]
                Thread(
                    target=lambda: self.load_database(root, filename),
                    daemon=True
                ).start()
            else:
                return

    def add_enneagram_scores(self, filename, ext):
        result = self.calculate()
        if not result:
            return
        config = ConfigParser()
        config.read("defaults.ini")
        filename = os.path.split(filename)[-1].replace(f".{ext}", "") + "_" + \
            config["ALGORITHM"]["selected"].replace(".json", "") + ".json"
        self.extract_database(filename=filename)
        return True

    def load_adb(self, filename):
        self.database, self.category_names = from_xml(filename)
        try:
            logging.info("Completed parsing.")
            logging.info(f"{len(self.database)} records are available.")
        except tk.TclError:
            return
        return self.add_enneagram_scores(
            filename=filename,
            ext="xml"
        )

    def load_json(self, filename):
        if filename == "./Database/None":
            return
        logging.info(f"Parsing {filename} file...")
        self.database = load_database(filename=filename)
        if len(self.database[0]) != 15:
            self.add_enneagram_scores(
                filename=filename,
                ext="json"
            )
        self.category_names = []
        for record in self.database:
            for cate in record[-3]:
                if cate[1] and cate[1] not in self.category_names:
                    self.category_names.append(cate[1])
        self.category_names = sorted(self.category_names)
        try:
            logging.info("Completed parsing.")
            logging.info(f"{len(self.database)} records are available.")
        except tk.TclError:
            return
        return True

    def extract_database(self, filename):
        path = os.path.join(".", "Database", filename)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.database, file, ensure_ascii=False, indent=4)

    def calculate(self):
        config = ConfigParser()
        config.read("defaults.ini")
        logging.info("Started calculating.")
        size = len(self.database)
        received = 0
        now = time.time()
        toplevel = tk.Toplevel()
        toplevel.title("Calculating")
        toplevel.resizable(width=False, height=False)
        pframe = tk.Frame(master=toplevel)
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
        will_be_removed = []
        for record in self.database:
            try:
                result = Enneagram(
                    jd=float(record[6]),
                    lat=convert_coordinates(record[7]),
                    lon=convert_coordinates(record[8]),
                    hsys=HOUSE_SYSTEMS[config["HOUSE SYSTEM"]["selected"]]
                )
            except swe.Error:
                logging.error(
                    msg=f"Can't calculate the astrological results:\n"
                        f"\tRecord: {record}\n".expandtabs(4)
                )
                received += 1
                will_be_removed.append(record)
                try:
                    progressbar(
                        s=size,
                        r=received,
                        n=now,
                        pframe=pframe,
                        pbar=pbar,
                        pstring=pstring
                    )
                except tk.TclError:
                    return
                continue
            try:
                score = result.get_all_scores()
            except KeyError:
                logging.error(
                    msg=f"Can't calculate the score:\n"
                        f"\tRecord: {record}\n".expandtabs(4)
                )
                received += 1
                will_be_removed.append(record)
                try:
                    progressbar(
                        s=size,
                        r=received,
                        n=now,
                        pframe=pframe,
                        pbar=pbar,
                        pstring=pstring
                    )
                except tk.TclError:
                    return
                continue
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
                rindex = enneagram_type + 1
            except IndexError:
                right = s[0]
                rindex = 0
            if enneagram_type == 0:
                left = s[-1]
                lindex = 8
            else:
                left = s[enneagram_type - 1]
                lindex = enneagram_type - 1
            enneagram_wing = rindex if right > left else lindex
            enneagram_wing = f"Type-{enneagram_wing + 1}"
            enneagram_type = f"Type-{enneagram_type + 1}"
            record.extend([enneagram_type, enneagram_wing])
            received += 1
            try:
                progressbar(
                    s=size,
                    r=received,
                    n=now,
                    pframe=pframe,
                    pbar=pbar,
                    pstring=pstring
                )
            except tk.TclError:
                return
        logging.info("Completed calculating.")
        for i in will_be_removed:
            self.database.remove(i)
        return True


class DatabaseFrame(tk.Frame):
    widgets = []

    def __init__(
            self,
            database,
            category_names,
            icons,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        for i in self.widgets:
            i.destroy()
        self.pack()
        self.database = database
        self.category_names = category_names
        self.icons = icons
        self.displayed_results = []
        self.selected_ratings = []
        self.included = []
        self.ignored = []
        self.found_categories = []
        self.checkbuttons = {}
        self.category_menu = None
        self.treeview_menu = None
        self.entry_menu = None
        self.pressed_return = 0
        self.info_var = tk.StringVar()
        self.info_var.set("0")
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
            height=5,
            x_scrollbar=True
        )
        self.treeview.bind(
            sequence="<Button-1>",
            func=lambda event: self.destroy_menu(self.treeview_menu)
        )
        self.treeview.bind(
            sequence="<Button-3>",
            func=lambda event: self.button_3_on_treeview(event=event)
        )
        self.treeview.bind(
            sequence="<Control-a>",
            func=lambda event: self.treeview.selection_set(
                self.treeview.get_children()
            )
        )
        self.entry_button_frame = tk.Frame(master=self.topframe)
        self.entry_button_frame.grid(row=0, column=0)
        self.search = SearchFrame(
            master=self.entry_button_frame,
            treeview=self.treeview,
            database=self.database,
            info_var=self.info_var
        )
        self.category_label = tk.Label(
            master=self.entry_button_frame,
            text="Categories",
            fg="red"
        )
        self.category_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rrating_label = tk.Label(
            master=self.entry_button_frame,
            text="Rodden Rating",
            fg="red"
        )
        self.rrating_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.category_button = tk.Button(
            master=self.entry_button_frame,
            text="Select",
            command=self.select_categories
        )
        self.category_button.grid(row=1, column=1, padx=5, pady=5)
        self.rating_button = tk.Button(
            master=self.entry_button_frame,
            text="Select",
            command=self.select_ratings
        )
        self.rating_button.grid(row=2, column=1, padx=5, pady=5)
        self.ranges = {}
        self.range_frame = tk.Frame(master=self.topframe)
        self.range_frame.grid(row=3, column=0, columnspan=4, pady=10)
        for i in ["Year", "Latitude", "Longitude"]:
            self.ranges[i] = EntryFrame(
                master=self.range_frame,
                texts=["From", "To"],
                title=f"Select {i} Range"
            )
            self.ranges[i].pack(side="left", padx=10)
        self.button_frame = tk.Frame(master=self.topframe)
        self.button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        self.create_checkbutton()
        self.get_button = tk.Button(
            master=self.button_frame,
            text="Get Records",
            command=self.get_records,
            width=12
        )
        self.get_button.pack(side="left")
        self.display_button = tk.Button(
            master=self.button_frame,
            text="Display Records",
            command=self.display_results,
            width=12
        )
        self.display_button.pack(side="left")
        self.total_msgbox_info = tk.Label(
            master=self.bottomframe,
            text="Total = "
        )
        self.total_msgbox_info.grid(row=0, column=0)
        self.msgbox_info = tk.Label(
            master=self.bottomframe,
            textvariable=self.info_var
        )
        self.msgbox_info.grid(row=0, column=1)
        self.widgets.append(self)

    def create_checkbutton(self):
        check_frame = tk.Frame(master=self.entry_button_frame)
        check_frame.grid(row=1, column=2, pady=10, rowspan=2)
        names = (
            "event",
            "human",
            "male",
            "female",
            "North Hemisphere",
            "South Hemisphere",
            "West Hemisphere",
            "East Hemisphere"
        )
        for i, j in enumerate(names):
            var = tk.StringVar()
            var.set(value="0")
            checkbutton = tk.Checkbutton(
                master=check_frame,
                text=f"Do not display {j} charts.",
                variable=var)
            checkbutton.grid(row=i, column=2, columnspan=2, sticky="w")
            self.checkbuttons[j] = [var, checkbutton]

    def inform_user(self, message="inserted"):
        self.update()
        if len(self.displayed_results) == 0:
            MsgBox(
                title="Info",
                message=f"No record is {message}.",
                icons=self.icons,
                level="info"
            )
        elif len(self.displayed_results) == 1:
            MsgBox(
                title="Info",
                message=f"1 record is {message}.",
                icons=self.icons,
                level="info"
            )
        else:
            MsgBox(
                title="Display Records",
                message=f"{len(self.displayed_results)} "
                        f"records are {message}.",
                icons=self.icons,
                level="info"
            )

    def get_records(self, display=False):
        self.displayed_results = []
        event = self.checkbuttons["event"][0]
        human = self.checkbuttons["human"][0]
        male = self.checkbuttons["male"][0]
        female = self.checkbuttons["female"][0]
        north = self.checkbuttons["North Hemisphere"][0]
        south = self.checkbuttons["South Hemisphere"][0]
        west = self.checkbuttons["West Hemisphere"][0]
        east = self.checkbuttons["East Hemisphere"][0]
        year_from = self.ranges["Year"].widgets["From"].get()
        year_to = self.ranges["Year"].widgets["To"].get()
        latitude_from = self.ranges["Latitude"].widgets["From"].get()
        latitude_to = self.ranges["Latitude"].widgets["To"].get()
        longitude_from = self.ranges["Longitude"].widgets["From"].get()
        longitude_to = self.ranges["Longitude"].widgets["To"].get()
        for record in self.database:
            if record[3] not in self.selected_ratings:
                continue
            if event.get() == "1" and record[2] == "N/A":
                continue
            if human.get() == "1" and record[2] in ["F", "M"]:
                continue
            if male.get() == "1" and record[2] == "M":
                continue
            if female.get() == "1" and record[2] == "F":
                continue
            if (
                isinstance(record[7], str)
                and
                north.get() == "1"
                and
                "n" in record[7]
            ):
                continue
            if (
                isinstance(record[7], float)
                and
                north.get() == "1"
                and
                record[7] > 0
            ):
                continue
            if (
                isinstance(record[7], str)
                and
                south.get() == "1"
                and
                "s" in record[7]
            ):
                continue
            if (
                isinstance(record[7], float)
                and
                south.get() == "1"
                and
                record[7] < 0
            ):
                continue
            if (
                isinstance(record[8], str)
                and
                west.get() == "1"
                and
                "w" in record[8]
            ):
                continue
            if (
                isinstance(record[8], float)
                and
                west.get() == "1"
                and
                record[8] < 0
            ):
                continue
            if (
                isinstance(record[8], str)
                and
                east.get() == "1"
                and
                "e" in record[8]
            ):
                continue
            if (
                isinstance(record[8], float)
                and
                east.get() == "1"
                and
                record[8] > 0
            ):
                continue
            if record[0] in [3546, 68092]:
                continue
            if not any(
                category[1] in self.included
                for category in record[-3]
            ):
                continue
            if any(
                category[1] in self.ignored
                for category in record[-3]
            ):
                continue
            year = int(record[4].split()[2])
            if (
                year_from
                and
                year_to
                and not int(year_from) <= year <= int(year_to)
            ):
                continue
            latitude = convert_coordinates(record[7])
            if (
                latitude_from
                and
                latitude_to
                and not float(latitude_from) <= latitude < float(latitude_to)
            ):
                continue
            longitude = convert_coordinates(record[8])
            if (
                longitude_from
                and
                longitude_to
                and not float(longitude_from) <= longitude < float(longitude_to)
            ):
                continue
            self.displayed_results += [record]
        if not display:
            self.info_var.set(len(self.displayed_results))
            self.inform_user(message="gotten")

    def display_results(self):
        if self.treeview.get_children():
            msg = "There are records in treeview.\n" \
                  "Are you sure you want to insert \nthe records?\n" \
                  "If you press 'OK', \nthe records in treeview would be\n" \
                  "deleted."
            choicebox = ChoiceBox(
                title="Warning",
                level="warning",
                message=msg,
                icons=self.icons,
                width=400,
                height=200,
            )
            if choicebox.choice:
                pass
            else:
                return
        self.get_records(display=True)
        self.treeview.delete(*self.treeview.get_children())
        for index, i in enumerate(self.displayed_results):
            try:
                self.treeview.insert(
                    parent="",
                    index=index,
                    values=i
                )
                self.info_var.set(index + 1)
                self.update()
            except tk.TclError:
                return
        self.inform_user()

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

    def category_widgets(self, master, container):
        search_label = tk.Label(
            master=master,
            text="Search a category",
            font="Default 9 bold"
        )
        search_label.pack()
        entry = ttk.Entry(master=master)
        entry.pack()
        entry.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.search_category(
                event=event,
                treeview=treeview
            )
        )
        entry.bind(
            sequence="<Return>",
            func=lambda event: self.goto_next_category(
                treeview=treeview,
                event=event
            )
        )
        frame = tk.Frame(master=master)
        frame.pack()
        treeview = Treeview(
            master=frame,
            columns=["Categories"],
            width=400,
            anchor="w"
        )
        treeview.pack()
        for index, i in enumerate(self.category_names):
            treeview.insert(
                index=index,
                parent="",
                values=i.replace(" ", "\ "),
                tag=index
            )
        var = tk.StringVar()
        var.set("Selected = 0")
        info_label = tk.Label(
            master=master,
            textvariable=var
        )
        info_label.pack()
        treeview.bind(
            sequence="<Button-3>",
            func=lambda event: self.button_3_on_cat_treeview(
                event=event,
                var=var,
                container=container
            )
        )
        treeview.bind(
            sequence="<Button-1>",
            func=lambda event: self.destroy_menu(menu=self.category_menu)
        )

    def select_categories(self):
        config = ConfigParser()
        config.read("defaults.ini")
        selection = config["CATEGORY SELECTION"]["selected"]
        if selection == "Basic":
            self.select_basic_categories()
        elif selection == "Advanced":
            self.select_advanced_categories()

    def select_basic_categories(self):
        self.included = []
        self.ignored = []
        included = []
        toplevel = tk.Toplevel()
        toplevel.title("Select Categories")
        toplevel.resizable(width=False, height=False)
        toplevel.update()
        self.category_widgets(
            master=toplevel,
            container=included
        )
        button = tk.Button(
            master=toplevel,
            text="Apply",
            command=lambda: self.apply_selection(
                included=included,
                ignored=[],
                master=toplevel
            )
        )
        button.pack(side="bottom")

    def select_advanced_categories(self):
        self.included = []
        self.ignored = []
        included = []
        ignored = []
        toplevel = tk.Toplevel()
        toplevel.title("Select Categories")
        toplevel.resizable(width=False, height=False)
        toplevel.update()
        main_frame = tk.Frame(master=toplevel)
        main_frame.pack()
        left_frame = tk.Frame(master=main_frame)
        left_frame.pack(side="left")
        left_label = tk.Label(
            master=left_frame,
            text="Include",
            font="Default 12 bold"
        )
        left_label.pack()
        right_frame = tk.Frame(master=main_frame)
        right_frame.pack(side="right")
        right_label = tk.Label(
            master=right_frame,
            text="Ignore",
            font="Default 12 bold"
        )
        right_label.pack()
        self.category_widgets(
            master=left_frame,
            container=included
        )
        self.category_widgets(
            master=right_frame,
            container=ignored
        )
        button = tk.Button(
            master=toplevel,
            text="Apply",
            command=lambda: self.apply_selection(
                included=included,
                ignored=ignored,
                master=toplevel
            )
        )
        button.pack(side="bottom")

    @staticmethod
    def change_status_of_selected(var, container, widget, mode):
        selection = widget.selection()
        for i in selection:
            item = widget.item(i)["values"][0]
            tag = widget.item(i)["tags"][0]
            if mode == "add" and item not in container:
                widget.tag_configure(tag, foreground="red")
                container.append(item)
            elif mode == "remove" and item in container:
                widget.tag_configure(tag, foreground="black")
                container.remove(item)
        var.set(f"Selected = {len(container)}")

    def button_3_on_cat_treeview(self, event, var, container):
        self.destroy_menu(self.category_menu)
        self.category_menu = tk.Menu(master=None, tearoff=False)
        self.category_menu.add_command(
            label="Add",
            command=lambda: self.change_status_of_selected(
                var=var,
                container=container,
                widget=event.widget,
                mode="add"
            )
        )
        self.category_menu.add_command(
            label="Remove",
            command=lambda: self.change_status_of_selected(
                var=var,
                container=container,
                widget=event.widget,
                mode="remove"
            )
        )
        self.category_menu.post(event.x_root, event.y_root)

    def goto_next_category(self, event, treeview):
        if event.widget.get() and self.found_categories:
            if self.pressed_return + 1 == len(self.found_categories):
                self.pressed_return = 0
            else:
                self.pressed_return += 1
            key = list(self.found_categories)[self.pressed_return]
            value = self.found_categories[key]
            treeview.yview_moveto(
                key / len(treeview.get_children())
            )
            treeview.selection_set(value)

    def search_category(self, event, treeview):
        if event.widget.get().lower() and event.keysym != "Return":
            self.pressed_return = 0
            self.found_categories = {
                i: j for i, j in enumerate(treeview.get_children())
                if (
                    event.widget.get().lower()
                    in
                    treeview.item(j)["values"][0].lower()
                )
            }
            for i, j in self.found_categories.items():
                treeview.yview_moveto(
                    i / len(treeview.get_children())
                )
                treeview.selection_set(j)
                break

    def apply_selection(self, included, ignored, master):
        self.included = included
        self.ignored = ignored
        master.destroy()

    def button_3_open_scores(self):
        selected = self.treeview.selection()
        if not selected:
            pass
        else:
            try:
                values = self.treeview.item(selected)["values"]
            except tk.TclError:
                return
            latitude = str(round(convert_coordinates(values[7]), 2))
            longitude = str(round(convert_coordinates(values[8]), 2))
            config = ConfigParser()
            config.read("defaults.ini")
            algorithm = config["ALGORITHM"]["selected"]
            hsys = HOUSE_SYSTEMS[config["HOUSE SYSTEM"]["selected"]]
            if "Jul" in values[4]:
                date = values[4].split("(")[-1].replace(" greg.)", "")
            else:
                date = values[4]
            info = {
                "Name": values[1],
                "Gender": values[2],
                "Date": dt.strptime(
                    date,
                    "%d %B %Y"
                ).strftime("%d.%m.%Y"),
                "Time": values[5],
                "Latitude": latitude,
                "Longitude": longitude
            }
            user = Enneagram(
                jd=float(values[6]),
                lat=float(latitude),
                lon=float(longitude),
                hsys=hsys,
                icons=self.icons
            )
            scores = user.get_all_scores()
            TreeviewToplevel(
                values=scores,
                info=info,
                jd=float(values[6]),
                hsys=hsys,
                icons=self.icons,
                patterns=user.patterns,
                algorithm=algorithm,
                plot=Plot,
                wide=True
            )

    def button_3_remove(self):
        selected = self.treeview.selection()
        if selected:
            results = {i[0]: i for i in self.displayed_results}
            for i in selected:
                adb_id = self.treeview.item(i)["values"][0]
                self.displayed_results.remove(results[adb_id])
                self.treeview.delete(i)
            self.info_var.set(len(self.displayed_results))

    def button_3_open_url(self):
        selected = self.treeview.selection()
        if not selected:
            pass
        else:
            try:
                values = self.treeview.item(selected)["values"]
            except tk.TclError:
                return
            if values[11] != "None":
                open_new(values[11])

    def button_3_on_treeview(self, event):
        self.destroy_menu(self.treeview_menu)
        self.treeview_menu = tk.Menu(master=None, tearoff=False)
        self.treeview_menu.add_command(
            label="Open ADB Page",
            command=self.button_3_open_url
        )
        self.treeview_menu.add_command(
            label="Open Enneagram Scores",
            command=self.button_3_open_scores
        )
        self.treeview_menu.add_command(
            label="Remove",
            command=self.button_3_remove
        )
        self.treeview_menu.post(event.x_root, event.y_root)

    def button_3_on_entry(self, event):
        self.destroy_menu(self.entry_menu)
        self.entry_menu = tk.Menu(master=None, tearoff=False)
        self.entry_menu.add_command(
            label="Copy",
            command=lambda: self.focus_get().event_generate('<<Copy>>'))
        self.entry_menu.add_command(
            label="Cut",
            command=lambda: self.focus_get().event_generate('<<Cut>>'))
        self.entry_menu.add_command(
            label="Paste",
            command=lambda: self.focus_get().event_generate('<<Paste>>'))
        self.entry_menu.add_command(
            label="Remove",
            command=lambda: self.focus_get().event_generate('<<Clear>>'))
        self.entry_menu.add_command(
            label="Select All",
            command=lambda: self.focus_get().event_generate('<<SelectAll>>'))
        self.entry_menu.post(event.x_root, event.y_root)

    @staticmethod
    def destroy_menu(menu):
        if menu:
            menu.destroy()

    def select_all_items(self):
        self.treeview.selection_set(self.treeview.get_children())
