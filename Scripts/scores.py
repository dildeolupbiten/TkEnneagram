# -*- coding: utf-8 -*-

from .modules import load

with open("scores.json", "r") as f:
    scores = load(f)

