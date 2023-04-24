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

'''TRACK FEATURES'''
tracks = [t[0] for t in cur.execute("SELECT track_uri FROM tracks").fetchall()]
trackN = len(tracks)
for i in range(0, trackN, 100):
    j = min(i+100, trackN)
    features = spotify.audio_features(tracks[i:j])
    f = []
    for t in features:
        if t is not None:
            f += ["('"+t["uri"]+"','"+str(t["acousticness"])+"','"+str(t["danceability"])+"','"+str(t["energy"])+"','"+str(t["instrumentalness"])+"','"+str(t["key"])+"','"+str(t["liveness"])+"','"+str(t["loudness"])+"','"+str(t["mode"])+"','"+str(t["speechiness"])+"','"+str(t["tempo"])+"','"+str(t["time_signature"])+"','"+str(t["valence"])+"')"]
        # else:
            # f += ["('"+t["uri"]+"','0','0','0','0','0','0','0','0','0','0','0','0')"]
    f = ",".join(f)

    cur.execute(f"INSERT OR IGNORE INTO track_features (track_uri,acousticness,danceability,energy,instrumentalness,music_key,liveness,loudness,mode,speechiness,tempo,time_signature,valence) VALUES {f};")
    conn.commit()
    print("processed to", j)


'''test code'''
# tracks = cur.execute(f"SELECT track_uri FROM tracks LIMIT 0,100;").fetchall()
# features = spotify.audio_features([t[0] for t in tracks])
# features = ",".join(["("+t["uri"]+","+str(t["acousticness"])+","+str(t["danceability"])+","+str(t["energy"])+","+str(t["instrumentalness"])+","+str(t["key"])+","+str(t["liveness"])+","+str(t["loudness"])+","+str(t["mode"])+","+str(t["speechiness"])+","+str(t["tempo"])+","+str(t["time_signature"])+","+str(t["valence"])+")" for t in features])
# cur.execute(f"INSERT INTO track_features (track_uri,acousticness,danceability,energy,instrumentalness,music_key,liveness,loudness,mode,speechiness,tempo,time_signature,valence) VALUES ({features});")

# trackN = cur.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
# for i in range(0, trackN, 100):
#     tracks = cur.execute(f"SELECT track_uri FROM tracks WHERE rowid > 1267443 LIMIT {i},100;").fetchall()
#     features = spotify.audio_features([t[0] for t in tracks])
#     f = []
#     for t in features:
#         if t is not None:
#             f += ["('"+t["uri"]+"','"+str(t["acousticness"])+"','"+str(t["danceability"])+"','"+str(t["energy"])+"','"+str(t["instrumentalness"])+"','"+str(t["key"])+"','"+str(t["liveness"])+"','"+str(t["loudness"])+"','"+str(t["mode"])+"','"+str(t["speechiness"])+"','"+str(t["tempo"])+"','"+str(t["time_signature"])+"','"+str(t["valence"])+"')"]
#         # else:
#             # f += ["('"+t["uri"]+"','0','0','0','0','0','0','0','0','0','0','0','0')"]
#     f = ",".join(f)

#     cur.execute(f"INSERT OR IGNORE INTO track_features (track_uri,acousticness,danceability,energy,instrumentalness,music_key,liveness,loudness,mode,speechiness,tempo,time_signature,valence) VALUES {f};")
#     conn.commit()


'''old api'''
# ALBUM_URI: str = "1nqz3cEjuvCMo8RHLBI9kM"
# async def main(ident: str, secret: str, album_uri: str) -> None:
#     async with spotify.Client(ident, secret) as client:
#         album = await client.get_album(album_uri)

#         async for track in album:
#             print(repr(track))
# asyncio.run(main(CLIENT_ID, CLIENT_SECRET, ALBUM_URI))

'''generic spotipy test'''
# artist = spotify.search("TWICE", 1, 0, "artist")["artists"]["items"][0]["uri"]
# results = spotify.artist_albums(artist, album_type="album")
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     string = album["name"] + ": "
#     a = spotify.album(album["uri"])
#     for song in a["tracks"]["items"]:
#         string += song["name"] + " | "
#     print(string)