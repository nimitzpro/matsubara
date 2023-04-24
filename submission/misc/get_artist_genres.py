import sqlite3
import random
import pandas as pd
import os, sys, time, random
import json
import numpy as np
import re
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

secrets = open("secrets.txt")
CLIENT_ID: str = secrets.readline().rstrip()
CLIENT_SECRET: str = secrets.readline()
secrets.close()


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

conn = sqlite3.connect("Z:/spotify.db")
cur = conn.cursor()

def escape(data):
    data = re.sub("'+", "''", data)
    data = re.sub('\"', '""', data)
    return data

'''ARTIST GENRES'''
artist_uris = [a[0] for a in cur.execute("select DISTINCT artist_uri from tracks;").fetchall()]
len_artists = len(artist_uris)
for i in range(0, len_artists, 50):
    j = min(i+50, len_artists)
    artists = spotify.artists(artist_uris[i:j])
    values = ""
    print("J:", j)
    print("arists", len(artists["artists"]))
    print([a["genres"] for a in artists["artists"]])
    values = ",".join([",".join(["('"+artists['artists'][a]['uri']+"','"+escape(genre)+"')" for genre in artists["artists"][a]["genres"]]) for a in range(j-i)])
    values = re.sub(",,+", ",", values)
    print(values)
    if values[0] == ",":
        values = values[1::]
    if values[-1] == ",":
        values = values[:len(values)-1:]
    cur.execute(f"INSERT INTO artist_genres (artist_uri, genre) VALUES "+values+";")
    conn.commit()