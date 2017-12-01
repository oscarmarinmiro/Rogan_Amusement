__author__ = '@oscarmarinmiro @ @outliers_es'

import json
import sys
import os

DIR_OUT = "/Volumes/Malasia/Rogan"

CONFIG_FILE = "../config/config.json"


my_config = json.load(open(CONFIG_FILE, "rb"))

pprint.pprint(my_config)
