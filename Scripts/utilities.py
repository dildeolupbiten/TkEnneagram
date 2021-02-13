# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .constants import SIGNS, PLANETS, CATEGORIES, HOUSE_SYSTEMS
from .modules import (
    dt, tk, os, ET, ttk, json, time, Popen, urlopen,
    URLError, PhotoImage, pickle, ConfigParser, askopenfilename
)


def load_database(filename, i=0):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            return {
                k: v
                for index, (k, v) in enumerate(data.items())
                if index >= i
            }
        else:
            return data


def convert_degree(degree):
    for i in range(12):
        if i * 30 <= degree < (i + 1) * 30:
            return degree - (30 * i), [*SIGNS][i]


def reverse_convert_degree(degree, sign):
    return degree + 30 * [*SIGNS].index(sign)


def dd_to_dms(dd):
    degree = int(dd)
    minute = int((dd - degree) * 60)
    second = round(float((dd - degree - minute / 60) * 3600))
    return f"{degree}\u00b0 {minute}\' {second}\""


def dms_to_dd(dms):
    dms = dms.replace("\u00b0", " ").replace("\'", " ").replace("\"", " ")
    degree = int(dms.split(" ")[0])
    minute = float(dms.split(" ")[1]) / 60
    second = float(dms.split(" ")[2]) / 3600
    return degree + minute + second


def create_image_files(path):
    return {
        i[:-4]: {
            "img": PhotoImage(
                file=os.path.join(os.getcwd(), path, i)
            )
        } for i in sorted(os.listdir(os.path.join(os.getcwd(), path)))
    }


def progressbar(s, r, n, pframe, pbar, pstring):
    if r != s:
        pbar["value"] = r
        pbar["maximum"] = s
        pstring.set(
            "{} %, {} minutes remaining.".format(
                int(100 * r / s),
                round(
                    (int(s / (r / (time.time() - n))) -
                     int(time.time() - n)) / 60
                )
            )
        )
    else:
        pframe.master.destroy()


def convert_coordinates(coord):
    if "n" in coord:
        d, _m = coord.split("n")
        if len(_m) == 4:
            m = _m[:2]
            s = _m[2:]
            return dms_to_dd(f"{d}\u00b0{m}'{s}\"")
        return dms_to_dd(coord.replace("n", "\u00b0") + "'0\"")
    elif "s" in coord:
        d, _m = coord.split("s")
        if len(_m) == 4:
            m = _m[:2]
            s = _m[2:]
            return -1 * dms_to_dd(f"{d}\u00b0{m}'{s}\"")
        return -1 * dms_to_dd(coord.replace("s", "\u00b0") + "'0\"")
    elif "e" in coord:
        d, _m = coord.split("e")
        if len(_m) == 4:
            m = _m[:2]
            s = _m[2:]
            return dms_to_dd(f"{d}\u00b0{m}'{s}\"")
        return dms_to_dd(coord.replace("e", "\u00b0") + "'0\"")
    elif "w" in coord:
        d, _m = coord.split("w")
        if len(_m) == 4:
            m = _m[:2]
            s = _m[2:]
            return -1 * dms_to_dd(f"{d}\u00b0{m}'{s}\"")
        return -1 * dms_to_dd(coord.replace("w", "\u00b0") + "'0\"")


def tbutton_command(cvar_list, tlevel, select):
    for item in cvar_list:
        if item[0].get() is True:
            select.append(item[1])
    tlevel.destroy()


def check_all_command(check_all, cvar_list, checkbutton_list):
    if check_all.get() is True:
        for var, c_button in zip(cvar_list, checkbutton_list):
            var[0].set(True)
            c_button.configure(variable=var[0])
    else:
        for var, c_button in zip(cvar_list, checkbutton_list):
            var[0].set(False)
            c_button.configure(variable=var[0])


def decrypt(file, password):
    with open(file, "rb") as f:
        data = pickle.load(f)
    return "".join(
        chr(item - password - index)
        for index, item in enumerate(data)
    )


def load_defaults():
    if os.path.exists("defaults.ini"):
        return
    config = ConfigParser()
    with open("defaults.ini", "w") as f:
        config["HOUSE SYSTEM"] = {"selected": "Placidus"}
        config["PLANETS"] = {
            planet: "true"
            for planet in PLANETS
        }
        config["ALGORITHM"] = {"selected": "2010_Algorithm_Placidus.json"}
        config["AUTH"] = {"selected": "None"}
        config["DATABASE"] = {"selected": "None"}
        config["CATEGORY SELECTION"] = {"selected": "Basic"}
        config["ENNEAGRAM SCORES"] = {
            f"Type-{i + 1}": "true"
            for i in range(9)
        }
        config.write(f)
        
        
def create_new_categories(patterns, adb):
    result = []
    for p in patterns:
        if p[0] == "Ascendant":
            p[0] = "Asc"
        elif p[0] == "Midheaven":
            p[0] = "MC"
        d = int(convert_degree(p[2])[0])
        d_ = str(d).zfill(2)
        _d = str(d + 1).zfill(2)
        frmt = f"{p[0]} : {p[1]} : {d_}\u00b0 - {_d}\u00b0"
        if adb:
            n = CATEGORIES[p[0]][p[1]][f"{d_} - {_d}"]
            result.append((n, frmt))
        else:
            result.append(frmt)
    return result
        
        
def add_category(root, icons):
    from .zodiac import Zodiac
    filename = askopenfilename(
        initialdir=".",
        title="Select a JSON file",
        filetypes=[("JSON Files", "*.json")]
    )
    if not filename:
        return
    database = load_database(filename=filename)
    config = ConfigParser()
    config.read("defaults.ini")
    error = False
    if isinstance(database, list):
        adb = True
        date_of_creation = False
        test_record = database[0]
        jd = float(test_record[6])
        lat = convert_coordinates(test_record[7])
        lon = convert_coordinates(test_record[8])
    else:
        adb = False
        date_of_creation = database["Date of Creation"]
        database = {
            k: v
            for index, (k, v) in enumerate(database.items())
            if index > 1
        }
        test_record = database[[k for k in database][0]]
        jd = test_record["Julian Date"]
        lat = test_record["Latitude"]
        lon = test_record["Longitude"]
    patterns = Zodiac(
        jd=jd,
        lat=lat,
        lon=lon,
        hsys=HOUSE_SYSTEMS[config["HOUSE SYSTEM"]["selected"]]
    ).patterns()[:4]
    categories = create_new_categories(patterns=patterns, adb=adb)
    if adb:
        if list(categories[0]) in test_record[-3]:
            error = True
    else:
        if categories[0] in test_record["Categories"]:
            error = True
    if not error:
        size = len(database)
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
        for record in database:
            if isinstance(database, list):
                jd = float(record[6])
                lat = convert_coordinates(record[7])
                lon = convert_coordinates(record[8])
            else:
                jd = database[record]["Julian Date"]
                lat = database[record]["Latitude"]
                lon = database[record]["Longitude"]
            patterns = Zodiac(
                jd=jd,
                lat=lat,
                lon=lon,
                hsys=HOUSE_SYSTEMS[config["HOUSE SYSTEM"]["selected"]]
            ).patterns()[:4]
            if isinstance(database, list):
                record[-3].extend(
                    create_new_categories(patterns=patterns, adb=adb)
                )
            else:
                try:
                    database[record]["Categories"].extend(
                        create_new_categories(patterns=patterns, adb=adb)
                    )
                except AttributeError:
                    database[record]["Categories"] = create_new_categories(
                        patterns=patterns,
                        adb=adb
                    )
                database[record]["Update Time"] = dt.utcnow().strftime(
                    "%d.%m.%Y %H:%M:%S"
                ) + " UTC"
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
        if not adb:
            new = {
                "Date of Creation": date_of_creation,
                "Last Modified": dt.utcnow().strftime(
                    "%d.%m.%Y %H:%M:%S"
                ) + " UTC"
            }
            new.update(database)
            database = new
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(database, f, ensure_ascii=False, indent=4)
        root.after(
            0,
            lambda: MsgBox(
                icons=icons,
                level="info",
                title="Info",
                message="Successfully added categories."
            )
        )
    else:
        root.after(
            0,
            lambda: MsgBox(
                icons=icons,
                level="warning",
                title="Warning",
                message="Categories have already been added."
            )
        )


def key_value(key, value):
    v1 = [key]
    v2 = [
        v for k, v in value.items()
        if k not in ["Categories", "Notes", "Access Time", "Update Time"]
    ]
    v3 = [
        {i: j for i, j in enumerate(value["Categories"], 1)}
        if value["Categories"] else None
    ]
    v4 = [value["Access Time"], value["Update Time"]]
    return v1 + v2 + v3 + v4


def check_update(icons):
    try:
        new = urlopen(
            "https://raw.githubusercontent.com/dildeolupbiten"
            "/TkEnneagram/master/README.md"
        ).read().decode()
    except URLError:
        MsgBox(
            title="Warning",
            message="Couldn't connect.",
            level="warning",
            icons=icons
        )
        return
    with open("README.md", "r", encoding="utf-8") as f:
        old = f.read()[:-1]
    if new != old:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new)
    try:
        scripts = json.load(
            urlopen(
                url=f"https://api.github.com/repos/dildeolupbiten/"
                    f"TkEnneagram/contents/Scripts?ref=master"
            )
        )
    except URLError:
        MsgBox(
            title="Warning",
            message="Couldn't connect.",
            level="warning",
            icons=icons
        )
        return
    update = False
    for i in scripts:
        try:
            file = urlopen(i["download_url"]).read().decode()
        except URLError:
            MsgBox(
                title="Warning",
                message="Couldn't connect.",
                level="warning",
                icons=icons
            )
            return
        if i["name"] not in os.listdir("Scripts"):
            update = True
            with open(f"Scripts/{i['name']}", "w", encoding="utf-8") as f:
                f.write(file)
        else:
            with open(f"Scripts/{i['name']}", "r", encoding="utf-8") as f:
                if file != f.read():
                    update = True
                    with open(
                            f"Scripts/{i['name']}",
                            "w",
                            encoding="utf-8"
                    ) as g:
                        g.write(file)
    if update:
        MsgBox(
            title="Info",
            message="Program is updated.",
            level="info",
            icons=icons
        )
        if os.path.exists("defaults.ini"):
            os.remove("defaults.ini")
        if os.name == "posix":
            Popen(["python3", "run.py"])
            os.kill(os.getpid(), __import__("signal").SIGKILL)
        elif os.name == "nt":
            Popen(["python", "run.py"])
            os.system(f"TASKKILL /F /PID {os.getpid()}")
    else:
        MsgBox(
            title="Info",
            message="Program is up-to-date.",
            level="info",
            icons=icons
        )


def from_xml(filename):
    database = []
    category_names = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for i in range(1000000):
        try:
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
                sbdate_dmy = bdata[1].text
                sbtime = bdata[2].text
                jd_ut = bdata[2].get("jd_ut")
                lat = bdata[3].get("slati")
                lon = bdata[3].get("slong")
                place = bdata[3].text
                country = bdata[4].text
                categories = [
                    (
                        categories[j].get("cat_id"),
                        categories[j].text
                    )
                    for j in range(len(categories))
                ]
                for category in categories:
                    if category[1] and category[1] not in category_names:
                        category_names.append(category[1])
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
                user_data.append(categories)
                if len(user_data) != 0:
                    database.append(user_data)
        except IndexError:
            break
    return database, sorted(category_names)
