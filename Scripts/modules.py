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
from webbrowser import open_new
from xlsxwriter import Workbook
from threading import Thread
from tkinter import ttk, PhotoImage
from datetime import datetime as dt
from geopy.geocoders import Nominatim
from configparser import ConfigParser
from timezonefinder import TimezoneFinder
