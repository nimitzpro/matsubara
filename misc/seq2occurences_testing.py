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



song1 = {}
occ = {}
song1_i = {}
occ_i = {}

''' processed up to 40000 - too slow so switched to seq2_simple gen'''

songs = cur.execute(f"SELECT * from playlist_tracks ORDER BY pid ASC, pindex ASC;").fetchall()
for i in range(len(songs) - 1):
    if int(songs[i+1][1]) != 0:
        track_uri1 = songs[i][2]
        track_uri2 = songs[i+1][2]
        
        if track_uri1 in song1.keys(): # skip checking to insert or update if already known
            if track_uri2 in song1[track_uri1]:
                a = song1[track_uri1].index(track_uri2)
                occ[track_uri1][a] += 1
                continue
        elif track_uri1 in song1_i.keys(): # skip checking to insert or update if already known
            if track_uri2 in song1_i[track_uri1]:
                a = song1_i[track_uri1].index(track_uri2)
                occ_i[track_uri1][a] += 1
                continue

        prevalence = cur.execute(f"SELECT prevalence from seq2_occurences WHERE (track_uri1 = '{track_uri1}' AND track_uri2 = '{track_uri2}');").fetchone()
        if prevalence != None: # use update query
            if track_uri1 in song1.keys():
                # if track_uri2 in song1[track_uri1]: # increment <t1,t2>
                #     a = song1[track_uri1].index(track_uri2)
                #     occ[track_uri1][a] += 1
                # else: # add track_uri2 to list of seqs for track_uri1
                song1[track_uri1].append(track_uri2)
                occ[track_uri1].append(prevalence[0]+1)
            else: # init track_uri1
                song1[track_uri1] = [track_uri2]
                occ[track_uri1] = [prevalence[0]+1]
        else: # use insert statement
            if track_uri1 in song1_i.keys():
            #     if track_uri2 in song1_i[track_uri1]: # increment <t1,t2>
            #         a = song1_i[track_uri1].index(track_uri2)
            #         occ_i[track_uri1][a] += 1
            #     else: # add track_uri2 to list of seqs for track_uri1
                song1_i[track_uri1].append(track_uri2)
                occ_i[track_uri1].append(1)
            else: # init track_uri1
                song1_i[track_uri1] = [track_uri2]
                occ_i[track_uri1] = [1]
    elif int(songs[i][0]) % 10000 == 0:
        u_string = "".join(["".join([f"WHEN (track_uri1='{t1}' AND track_uri2='{t2}') THEN '{occ[t1][i]}'\n" for i, t2 in enumerate(song1[t1])]) for t1 in song1.keys()])
        # print(str(u_string))
        i_string = ",".join([",".join([f"('{t1}','{t2}','{occ_i[t1][i]}')" for i, t2 in enumerate(song1_i[t1])]) for t1 in song1_i.keys()])
        if len(u_string) > 0:
            cur.execute(f"UPDATE seq2_occurences SET prevalence = CASE \n{u_string}ELSE prevalence\nEND;")
        if len(i_string) > 0:
            cur.execute(f"INSERT INTO seq2_occurences (track_uri1, track_uri2, prevalence) VALUES {i_string};")
        conn.commit()
        print("processed up to", str(songs[i][0]))
        song1 = {}
        occ = {}
        song1_i = {}
        occ_i = {}



u_string = "".join(["".join([f"WHEN track_uri1='{t1}' AND track_uri2='{t2}' THEN '{occ[t1][i]}'\n" for i, t2 in enumerate(song1[t1])]) for t1 in song1.keys()])
# print(str(u_string))
i_string = ",".join(["".join([f"('{t1}','{t2}','{occ_i[t1][i]}')" for i, t2 in enumerate(song1_i[t1])]) for t1 in song1_i.keys()])
if len(u_string) > 0:
    cur.execute(f"UPDATE seq2_occurences SET prevalence = CASE \n{u_string}ELSE prevalence\nEND;")
if len(i_string) > 0:
    cur.execute(f"INSERT INTO seq2_occurences (track_uri1, track_uri2, prevalence) VALUES {i_string};")
conn.commit()