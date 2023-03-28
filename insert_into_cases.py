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

conn = sqlite3.connect("Z:/spotify.db")
cur = conn.cursor()
path = "data/mpd/data/"
filenames = os.listdir(path)
for i, filename in enumerate(sorted(filenames)):
    if filename.startswith("mpd.slice.") and filename.endswith(".json"):

        # file = open(path+filename, "r")
        # data = "".join(file.readlines())
        # data = re.sub("'+", "''", data)
        # data = re.sub("\"", "\u0022", data)
        # file.close()
        # file = open(path+filename, "w")
        # file.write(data)

        print("processing", filename)

        data = json.load(open(path+filename))
        playlists = pd.DataFrame(data["playlists"])

        songs = np.concatenate([["('"+song['track_uri']+"', '"+escape(song['track_name'])+"', '"+song['artist_uri']+"', '"+escape(song['artist_name'])+"', '"+song['album_uri']+"', '"+escape(song['album_name'])+"', '"+str(song["duration_ms"])+"')" for song in playlist] for playlist in playlists["tracks"]]).tolist()
        
        songs = ", ".join([song for song in songs])
        # print(songs[:800])

        cur.execute('INSERT OR IGNORE INTO tracks (track_uri, track_name, artist_uri, artist_name, album_uri, album_name, duration_ms) VALUES ' + songs + ';')
        conn.commit()


def collab(l):
    if l == "true":
        return 1
    return 0

# for i, filename in enumerate(sorted(filenames)):
#     if filename.startswith("mpd.slice.") and filename.endswith(".json"):
#         print("processing", filename)
#         data = json.load(open(path+filename))
#         playlists = pd.DataFrame(data["playlists"])

#         playlists = [[str(playlists['pid'][p]), escape(playlists['name'][p]), str(collab(playlists['collaborative'][p])), str(playlists['num_tracks'][p]), str(playlists['num_albums'][p]), str(playlists["num_followers"][p])] for p in range(len(playlists))]
#         playlists = ", ".join(["(" + ", ".join(['"'+attr+'"' for attr in l]) + ")" for l in playlists])
#         # print(playlists)
#         # f = open("playlists.txt", "w", encoding="utf-8")
#         # f.write(playlists)
#         # f.close()
#         # break

#         cur.execute('INSERT OR IGNORE INTO playlists (pid, name, collaborative, num_tracks, num_albums, num_followers) VALUES ' + playlists + ';')
#         conn.commit()


# for i, filename in enumerate(sorted(filenames)):
#     if filename.startswith("mpd.slice.") and filename.endswith(".json"):
#         print("processing", filename)

#         data = json.load(open(path+filename))
#         playlists = pd.DataFrame(data["playlists"])

#         songs = np.concatenate([["('"+str(playlists["pid"][index])+"', '"+str(song['pos'])+"', '"+song['track_uri']+"')" for song in playlist] for index, playlist in enumerate(playlists["tracks"])]).tolist()
        
#         songs = ", ".join([song for song in songs])

#         cur.execute('INSERT INTO playlist_tracks (pid, pindex, track_uri) VALUES ' + songs + ';')
#         conn.commit()

'''slowww'''
# cur.execute('BEGIN TRANSACTION;')
# playlists = cur.execute("SELECT pid, num_tracks FROM playlists;").fetchall()
# for playlist in playlists:
#     songs = cur.execute(f"SELECT * from playlist_tracks WHERE pid = '{playlist[0]}' ORDER BY pindex ASC;").fetchall()
#     for index, song in enumerate(songs):
#         if song[1] != playlist[1] - 1:
#             prevalence = cur.execute(f"SELECT prevalence from pair_occurences WHERE (track_uri1 = '{song[2]}' AND track_uri2 = '{songs[index+1][2]}');").fetchone()
#             if prevalence != None:
#                 cur.execute(f"UPDATE pair_occurences SET prevalence = {prevalence[0]+1} WHERE (track_uri1 = '{song[2]}' AND track_uri2 = '{songs[index+1][2]}');")
#                 continue

#             prevalence = cur.execute(f"SELECT prevalence from pair_occurences WHERE (track_uri2 = '{song[2]}' AND track_uri1 = '{songs[index+1][2]}');").fetchone()
#             if prevalence != None:
#                 cur.execute(f"UPDATE pair_occurences SET prevalence = {prevalence[0]+1} WHERE (track_uri2 = '{song[2]}' AND track_uri1 = '{songs[index+1][2]}');")
#                 continue

#             cur.execute(f"INSERT INTO pair_occurences (track_uri1, track_uri2, prevalence) VALUES ('{song[2]}', '{songs[index+1][2]}', 1);")
    
#     if playlist[0] % 1000 == 0:
#         conn.commit()
#         print("processed to", str(playlist[0]))

# conn.commit()
# cur.execute('END TRANSACTION;')



# OLD CODE DOESN'T RESPECT ORDER - got to 298000 in spotify.db
# playlists = cur.execute("SELECT pid, num_tracks FROM playlists;").fetchall()
# songs = cur.execute(f"SELECT * from playlist_tracks WHERE pid > 298000 ORDER BY pid ASC, pindex ASC;").fetchall()
# songd = pd.DataFrame(columns=['track_uri1', 'track_uri2', 'prevalence'])
# for i in range(len(songs) - 1):
#     if int(songs[i+1][1]) != 0:
#         track_uri1 = songs[i][2]
#         track_uri2 = songs[i+1][2]
#         if len(songd[(songd["track_uri1"] == track_uri1) & (songd["track_uri2"] == track_uri2)]) > 0:
#             songd.loc[(songd["track_uri1"] == track_uri1) & (songd["track_uri2"] == track_uri2), 'prevalence'] += 1
#         elif len(songd[(songd["track_uri2"] == track_uri1) & (songd["track_uri1"] == track_uri2)]) > 0:
#             songd.loc[(songd["track_uri2"] == track_uri1) & (songd["track_uri1"] == track_uri2), 'prevalence'] += 1
#         else:
#             songd.loc[len(songd)] = [track_uri1, track_uri2, 1]
#     elif int(songs[i][0]) % 100 == 0:
#         print("processed to", str(songs[i][0]))
#         print(songd[songd["prevalence"] > 1].head())
#         songd.to_sql('pair_occurences', conn, if_exists='append', index=False, chunksize=10000)
#         songd = None
#         songd = pd.DataFrame(columns=['track_uri1', 'track_uri2', 'prevalence'])

# print(songd.head())
# songd.to_sql('pair_occurences', conn, if_exists='append', index=False, chunksize=10000)

# WIP pandas non-duplicate solution
# songs = cur.execute(f"SELECT * from playlist_tracks ORDER BY pid ASC, pindex ASC;").fetchall()
# songd = pd.DataFrame(columns=['track_uri1', 'track_uri2', 'prevalence'])
# for i in range(len(songs) - 1):
#     if int(songs[i+1][1]) != 0:
#         track_uri1 = songs[i][2]
#         track_uri2 = songs[i+1][2]
#         if len(songd[(songd["track_uri1"] == track_uri1) & (songd["track_uri2"] == track_uri2)]) > 0:
#             songd.loc[(songd["track_uri1"] == track_uri1) & (songd["track_uri2"] == track_uri2), 'prevalence'] += 1
#         else:
#             songd.loc[len(songd)] = [track_uri1, track_uri2, 1]
#     elif int(songs[i][0]) % 100 == 0:
#         print("processed to", str(songs[i][0]))
#         # print(songd[songd["prevalence"] > 1].head())
#         songd.to_sql('seq2_occurences', conn, if_exists='append', index=False, chunksize=10000)
#         songd = None
#         songd = pd.DataFrame(columns=['track_uri1', 'track_uri2', 'prevalence'])

# # print(songd.head())
# songd.to_sql('seq2_occurences', conn, if_exists='append', index=False, chunksize=10000)