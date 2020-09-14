# -*- coding: utf-8 -*-

from .modules import pickle

def decrypt(file, password):
    with open(file, "rb") as f:
        data = pickle.load(f)
    return "".join(
        chr(item - password - index)
        for index, item in enumerate(data)
    )

