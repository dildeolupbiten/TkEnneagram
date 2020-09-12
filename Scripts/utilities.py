# -*- coding: utf-8 -*-

from .modules import os, ImageTk


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
