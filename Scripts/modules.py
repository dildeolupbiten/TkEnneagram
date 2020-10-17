# -*- coding: utf-8 -*-

import os
import json
import time
import pickle
import logging
import numpy as np
import tkinter as tk
import swisseph as swe
import xml.etree.ElementTree as ET

from dateutil import tz
from pytz import timezone
from subprocess import Popen
from threading import Thread
from webbrowser import open_new
from xlsxwriter import Workbook
from urllib.error import URLError
from urllib.request import urlopen
from tkinter import ttk, PhotoImage
from datetime import datetime as dt
from geopy.geocoders import Nominatim
from configparser import ConfigParser
from timezonefinder import TimezoneFinder
from tkinter.filedialog import askopenfilename
