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
    update = False
    for d in ["Scripts", "JSON"]:
        scripts = load(
            request.urlopen(
                url=f"https://api.github.com/repos/dildeolupbiten/"
                    f"TkEnneagram/contents/{d}?ref=master"
            )
        )
        for i in scripts:
            file = request.urlopen(i["download_url"]).read().decode()
            if i["name"] not in os.listdir(d):
                update = True
                with open(f"{d}/{i['name']}", "w", encoding="utf-8") as f:
                    f.write(file)
            else:
                with open(f"{d}/{i['name']}", "r", encoding="utf-8") as f:
                    if file != f.read():
                        update = True
                        with open(
                                f"{d}/{i['name']}",
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
            Popen(["python3", "run.py"])
            import signal
            os.kill(os.getpid(), signal.SIGKILL)
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
