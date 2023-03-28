import pandas as pd
import os, sys, time, random
import json
import numpy as np
# import keras

feature_list = ["track_name", "artist_name", "album_name", "duration_ms"]

data = json.load(open("data/mpd/data/mpd.slice.0-999.json"))

playlists = pd.DataFrame(data["playlists"])

stripped_lists = [[song["track_uri"] for song in playlist] for playlist in playlists["tracks"]]

candidate_songs = list(set(np.concatenate(stripped_lists))) # remove duplicates
# current_playlist = ['spotify:track:6I9VzXrHxO9rA9A5euc8Ak'] # Britney Spears - Toxic
# candidate_playlists = [current_playlist]
print(candidate_songs)

string = ",".join([s[14::] for s in candidate_songs])

print(string)

f = open("songs.txt", "w")

f.write(string)

f.close()