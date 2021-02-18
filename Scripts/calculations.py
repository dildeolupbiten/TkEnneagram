# -*- coding: utf-8 -*-

from .results import Results
from .modules import os, Thread, ConfigParser


def find_observed_values(widget, icons):
    displayed_results = []
    selected_categories = []
    ignored_categories = []
    selected_ratings = []
    checkbuttons = {}
    year_from = ""
    year_to = ""
    latitude_from = ""
    latitude_to = ""
    longitude_from = ""
    longitude_to = ""
    for i in widget.winfo_children():
        if hasattr(i, "included"):
            year_from += i.ranges["Year"].widgets["From"].get()
            year_to += i.ranges["Year"].widgets["To"].get()
            latitude_from += i.ranges["Latitude"].widgets["From"].get()
            latitude_to += i.ranges["Latitude"].widgets["To"].get()
            longitude_from += i.ranges["Longitude"].widgets["From"].get()
            longitude_to += i.ranges["Longitude"].widgets["To"].get()
            displayed_results += i.displayed_results
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
    info = {
        key.title(): "True" if value[0].get() == "0" else "False"
        for key, value in checkbuttons.items()
    }
    if year_from and year_to:
        year_range = f"{year_from} - {year_to}"
    else:
        year_range = "None"
    if latitude_from and latitude_to:
        latitude_range = f"{latitude_from} - {latitude_to}"
    else:
        latitude_range = "None"
    if longitude_from and longitude_to:
        longitude_range = f"{longitude_from} - {longitude_to}"
    else:
        longitude_range = "None"
    info.update(
        {
            "Database": config["DATABASE"]["selected"]
            .replace(".json", "").replace(".xml", ""),
            "House System": config["HOUSE SYSTEM"]["selected"],
            "Rodden Rating": selected_ratings,
            "Category": selected_categories,
            "Ignored": ignored_categories,
            "Year Range": year_range,
            "Latitude Range": latitude_range,
            "Longitude Range": longitude_range
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
    if (
        info["West Hemisphere"] == "False"
        and
        info["East Hemisphere"] == "True"
    ):
        path = os.path.join(path, "East")
    elif (
        info["West Hemisphere"] == "True"
        and
        info["East Hemisphere"] == "False"
    ):
        path = os.path.join(path, "West")
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
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "observed_values.xlsx")
    Thread(
        target=lambda: start_observed_values(
            displayed_results=displayed_results,
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
        enneagram_scores,
        enneagram_wing_scores,
        info,
        widget,
        path,
        icons
):
    for i in displayed_results:
        t = i[-2]
        w = i[-1]
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
