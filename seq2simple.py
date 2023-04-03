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

buffer = []
songs = cur.execute(f"SELECT * from playlist_tracks ORDER BY pid ASC, pindex ASC;").fetchall()
for i in range(len(songs) - 1):
    if int(songs[i+1][1]) != 0:
        buffer.append(f"('{songs[i][2]}','{songs[i+1][2]}')")
    elif int(songs[i][0]) % 1000 == 0:
        cur.execute(f"INSERT INTO seq2_simple (track_uri1, track_uri2) VALUES {','.join(buffer)};")
        conn.commit()
        print("processed up to", str(songs[i][0]))
        buffer = []


if len(buffer) > 0:
    cur.execute(f"INSERT INTO seq2_simple (track_uri1, track_uri2) VALUES {','.join(buffer)};")
    conn.commit()