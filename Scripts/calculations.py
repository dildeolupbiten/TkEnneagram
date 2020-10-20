# -*- coding: utf-8 -*-

from .results import Results
from .modules import tk, os, ttk, Thread, ConfigParser


def select_year_range(displayed_results):
    toplevel = tk.Toplevel()
    toplevel.title("Select Year Range")
    toplevel.geometry("200x100")
    toplevel.resizable(width=False, height=False)
    frame = tk.Frame(master=toplevel)
    frame.pack()
    years = [int(i[4].split(" ")[2]) for i in displayed_results]
    max_min_years = [min(years), max(years)]
    entries = {}
    for i, j in enumerate(["Minimum", "Maximum"]):
        label = tk.Label(master=frame, text=j, font="Default 10 bold")
        label.grid(row=i, column=0, sticky="w")
        entry = ttk.Entry(master=frame)
        entry.grid(row=i, column=1, sticky="w")
        entry.insert("insert", max_min_years[i])
        entries[j] = entry
    filtered = []
    year_range = []
    apply = tk.Button(
        master=toplevel,
        text="Apply",
        command=lambda: apply_year_range(
            toplevel=toplevel,
            entries=entries,
            displayed_results=displayed_results,
            filtered=filtered,
            year_range=year_range

        )
    )
    apply.pack()
    toplevel.wait_window()
    return filtered, year_range


def apply_year_range(
        toplevel,
        entries,
        displayed_results,
        filtered,
        year_range,
):
    error = False
    for k, v in entries.items():
        if not v.get():
            error = True
        try:
            int(v.get())
        except ValueError:
            error = True
    if not error:
        filtered += [
            i for i in displayed_results
            if int(i[4].split(" ")[2]) in range(
                int(entries["Minimum"].get()),
                int(entries["Maximum"].get()) + 1
            )
        ]
        year_range += [
            int(entries["Minimum"].get()),
            int(entries["Maximum"].get())
        ]
        toplevel.destroy()


def find_observed_values(widget, icons):
    displayed_results = []
    selected_categories = []
    ignored_categories = []
    selected_ratings = []
    checkbuttons = {}
    mode = ""
    for i in widget.winfo_children():
        if hasattr(i, "included"):
            mode += i.mode
            displayed_results += [
                i.treeview.item(j)["values"]
                for j in i.treeview.get_children()
            ]
            selected_categories += i.included
            ignored_categories += i.ignored
            selected_ratings += i.selected_ratings
            checkbuttons.update(i.checkbuttons)
            break
    if not displayed_results:
        return
    if selected_categories:
        if len(selected_categories) > 1:
            selected_categories = "Control_Group"
        else:
            selected_categories = selected_categories[0]\
                .replace(" : ", "/").replace(" ", "_")
    else:
        if len(displayed_results) == 1:
            selected_categories = displayed_results[0][1]\
                .replace(", ", "_-_")
        else:
            selected_categories = "Special"
    if ignored_categories:
        if len(ignored_categories) > 1:
            ignored_categories = f"Totally {len(ignored_categories)} " \
                                 f"categories are ignored."
        else:
            ignored_categories = f"{ignored_categories[0]} is ignored."
    else:
        ignored_categories = "No category is ignored."
    if selected_ratings:
        selected_ratings = "+".join(selected_ratings)
    else:
        selected_ratings = "None"
    config = ConfigParser()
    config.read("defaults.ini")
    if "event" in checkbuttons:
        info = {
            key.title(): "True" if value[0].get() == "0" else "False"
            for key, value in checkbuttons.items()
        }
    else:
        info = {"Event": "False", "Human": "True"}
        info.update(
            {
                key.title(): "True" if value[0].get() == "0" else "False"
                for key, value in checkbuttons.items()
            }
        )
    info.update(
        {
            "Database": config["DATABASE"]["selected"]
            .replace(".json", "").replace(".xml", ""),
            "House System": config["HOUSE SYSTEM"]["selected"],
            "Rodden Rating": selected_ratings,
            "Category": selected_categories,
            "Ignored": ignored_categories
        }
    )
    path = os.path.join(
        *selected_categories.split("/"),
        f"RR_{selected_ratings}",
        config["HOUSE SYSTEM"]["selected"]
    )
    if info["Event"] == "False" and info["Human"] == "True":
        if info["Male"] == "False" and info["Female"] == "True":
            path = os.path.join(path, "Female")
        elif info["Male"] == "True" and info["Female"] == "False":
            path = os.path.join(path, "Male")
        else:
            path = os.path.join(path, "Human")
    elif info["Event"] == "True" and info["Human"] == "False":
        path = os.path.join(path, "Event")
    else:
        if info["Male"] == "False" and info["Female"] == "True":
            path = os.path.join(path, "Event+Female")
        elif info["Male"] == "True" and info["Female"] == "False":
            path = os.path.join(path, "Event+Male")
        else:
            path = os.path.join(path, "Event+Human")
    if (
            info["South Hemisphere"] == "False"
            and
            info["North Hemisphere"] == "True"
    ):
        path = os.path.join(path, "North")
    elif (
            info["South Hemisphere"] == "True"
            and
            info["North Hemisphere"] == "False"
    ):
        path = os.path.join(path, "South")
    else:
        path = path
    enneagram_scores = {
        f"Type-{i}": 0 for i in range(1, 10)
    }
    enneagram_wing_scores = {
        f"Type-{i}": {
            f"Type-{j if j not in [0, 10] else 9 if i == 1 else 1}": 0
            for j in [i - 1, i + 1]
        } for i in range(1, 10)
    }
    displayed_results, year_range = select_year_range(
        displayed_results=displayed_results
    )
    path = os.path.join(
        path,
        f"From_{year_range[0]}_To_{year_range[1]}"
    )
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "observed_values.xlsx")
    info.update(
        {"Minimum Year": year_range[0], "Maximum Year": year_range[1]}
    )
    Thread(
        target=lambda: start_observed_values(
            displayed_results=displayed_results,
            mode=mode,
            enneagram_scores=enneagram_scores,
            enneagram_wing_scores=enneagram_wing_scores,
            info=info,
            widget=widget,
            path=path,
            icons=icons
        )
    ).start()


def start_observed_values(
        displayed_results,
        mode,
        enneagram_scores,
        enneagram_wing_scores,
        info,
        widget,
        path,
        icons
):
    for i in displayed_results:
        if mode == "adb":
            t = i[-2]
            w = i[-1]
        else:
            t, w = i[9], i[10]
        enneagram_scores[t] += 1
        enneagram_wing_scores[t][w] += 1
    widget.after(
        0,
        lambda: Results(
            info=info,
            enneagram_scores=enneagram_scores,
            enneagram_wing_scores=enneagram_wing_scores,
            path=path,
            icons=icons
        )
    )
