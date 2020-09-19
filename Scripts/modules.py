# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import pickle
import logging
import numpy as np
import tkinter as tk
import swisseph as swe

from PIL import ImageTk
from tkinter import ttk
from dateutil import tz
from pytz import timezone
from subprocess import Popen
from webbrowser import open_new
from xlsxwriter import Workbook
from threading import Thread
from urllib.error import URLError
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from datetime import datetime as dt
from geopy.geocoders import Nominatim
from configparser import ConfigParser
from timezonefinder import TimezoneFinder

