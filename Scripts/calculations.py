# -*- coding: utf-8 -*-

from .results import Results
from .modules import os, Thread, ConfigParser


def find_observed_values(widget, icons):
    displayed_results = []
    selected_categories = []
    ignored_categories = []
    selected_ratings = []
    checkbuttons = {}
    start = ""
    end = ""
    for i in widget.winfo_children():
        if hasattr(i, "included"):
            displayed_results += i.displayed_results
            selected_categories += i.included
            ignored_categories += i.ignored
            selected_ratings += i.selected_ratings
            start += i.start
            end += i.end
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
    path = os.path.join(
        path,
        f"From_{start}_To_{end}"
    )
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "observed_values.xlsx")
    info.update(
        {"Start Year": start, "End Year": end}
    )
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
