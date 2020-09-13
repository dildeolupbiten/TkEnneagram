# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .modules import os, load, request, Popen, ImageTk


def create_image_files(path):
    return {
        i[:-4]: {
            "name": i[4:-4].replace("_", " ").title(),
            "path": os.path.join(os.getcwd(), path, i),
            "img": ImageTk.PhotoImage(
                file=os.path.join(os.getcwd(), path, i)
            )
        }
        for i in sorted(os.listdir(os.path.join(os.getcwd(), path)))
    }


def check_update(icons):
    data = load(
        request.urlopen(
            url="https://api.github.com/repos/dildeolupbiten/"
                "TkEnneagram/contents/Scripts?ref=master"
        )
    )
    update = False
    for i in data:
        file = request.urlopen(i["download_url"]).read().decode()
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
        if os.name == "posix":
            Popen(["python3", "TkAstroDb.py"])
            import signal
            os.kill(os.getpid(), signal.SIGKILL)
        elif os.name == "nt":
            Popen(["python", "TkAstroDb.py"])
            os.system(f"TASKKILL /F /PID {os.getpid()}")
    else:
        MsgBox(
            title="Info",
            message="Program is up-to-date.",
            level="info",
            icons=icons
        )
