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
    data = re.sub("\"", "\u0022", data)
    return data

conn = sqlite3.connect("Z:/spotify.db")
cur = conn.cursor()
path = "data/mpd/data/"
filenames = os.listdir(path)
# for i, filename in enumerate(sorted(filenames)):
#     if filename.startswith("mpd.slice.") and filename.endswith(".json"):

#         file = open(path+filename, "r")
#         data = "".join(file.readlines())
#         # data = re.sub("'+", "''", data)
#         # data = re.sub("\"", "\u0022", data)
#         file.close()

#         file = open(path+filename, "w")
#         file.write(data)

#         print("processing", filename)

#         data = json.load(open(path+filename))
#         playlists = pd.DataFrame(data["playlists"])

#         songs = np.concatenate([["('"+song['track_uri']+"', '"+escape(song['track_name'])+"', '"+escape(song['artist_name'])+"', '"+song['album_uri']+"', '"+escape(song['album_name'])+"', '"+str(song["duration_ms"])+"')" for song in playlist] for playlist in playlists["tracks"]]).tolist()
        
#         songs = ", ".join([song for song in songs])
#         print(songs[:800])

#         cur.execute('INSERT OR IGNORE INTO tracks (track_uri, track_name, artist_name, album_uri, album_name, duration_ms) VALUES ' + songs + ';')
#         conn.commit()


def collab(l):
    if l == "true":
        return 1
    return 0

for i, filename in enumerate(sorted(filenames)):
    if filename.startswith("mpd.slice.") and filename.endswith(".json"):

        data = json.load(open(path+filename))
        playlists = pd.DataFrame(data["playlists"])

        playlists = [[playlists['pid'][p], escape(playlists['name'][p]), collab(playlists['collaborative'][p]), playlists['num_tracks'][p], playlists['num_albums'][p], playlists["num_followers"][p]] for p in range(len(playlists))]
        playlists = ", ".join(["(" + ", ".join(['"'+str(attr)+'"' for attr in l]) + ")" for l in playlists])
        # print(playlists)
        # f = open("playlists.txt", "w", encoding="utf-8")
        # f.write(playlists)
        # f.close()
        # break

        cur.execute('INSERT INTO playlists (pid, name, collaborative, num_tracks, num_albums, num_followers) VALUES ' + playlists + ';')
        conn.commit()
