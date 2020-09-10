# -*- coding: utf-8 -*-

import os
import numpy as np
import tkinter as tk
import swisseph as swe

from json import load
from PIL import ImageTk
from tkinter import ttk
from dateutil import tz
from pytz import timezone
from xlsxwriter import Workbook
from datetime import datetime as dt
from geopy.geocoders import Nominatim
from configparser import ConfigParser
from timezonefinder import TimezoneFinder
