#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess

installed_packages = [
    p.decode().split("==")[0]
    for p in subprocess.check_output(
        [sys.executable, "-m", "pip", "freeze"]
    ).split()
]

packages = [
    "numpy",
    "geopy",
    "Pillow",
    "python-dateutil",
    "pytz",
    "six",
    "timezonefinder",
    "XlsxWriter"
]


def call(path, n):
    os.system(
        f"{sys.executable} -m pip install {os.path.join(path, files[n])}"
    )
    

if os.name == "posix":
    packages += ["pyswisseph"]
elif os.name == "nt":
    if "pyswisseph" not in installed_packages:
        path = os.path.join(".", "Eph", "Whl")
        files = [i for i in os.listdir(path) if "pyswisseph" in i]
        if sys.version_info.minor == 6:
            if platform.architecture()[0] == "32bit":
                call(path=path, n=0)
            elif platform.architecture()[0] == "64bit":
                call(path=path, n=1)
        elif sys.version_info.minor == 7:
            if platform.architecture()[0] == "32bit":
                call(path=path, n=2)
            elif platform.architecture()[0] == "64bit":
                call(path=path, n=3)
        elif sys.version_info.minor == 8:
            if platform.architecture()[0] == "32bit":
                call(path=path, n=4)
            elif platform.architecture()[0] == "64bit":
                call(path=path, n=5)

for package in packages:
    if package not in installed_packages:
        os.system(f"{sys.executable} -m pip install {package}")
           
if __name__ == "__main__":
    import Scripts
