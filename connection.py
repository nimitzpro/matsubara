#!/usr/bin/python

import sqlite3
import random
import pandas as pd
import os, sys, time, random
import json
import numpy as np
import re

def escape(data):
    data = re.sub("'+", "''", data)
    data = re.sub('\"', '""', data)
    return data

conn = sqlite3.connect("Z:/other/spotify_backup.db")
cur = conn.cursor()
path = "data/mpd/data/"
filenames = os.listdir(path)
c = cur.execute("SELECT * FROM tracks LIMIT 20;").fetchall()
print(c)