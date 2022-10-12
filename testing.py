#!/usr/bin/python

import sqlite3
import random

conn = sqlite3.connect("new/track_metadata.db")

cur = conn.cursor()

result = cur.execute("SELECT count(*) FROM songs")

print(result.fetchone())

songs = cur.execute("SELECT * FROM songs").fetchall()

def genRandom(randoms, s):
    r = random.randint(0, s-1)
    if r in randoms:
        return genRandom(randoms, s)
    return r

def createRandom(n=10, s=1000000):
    randoms = []
    playlist = []

    for i in range(0, n):
        r = genRandom(randoms, s)
        randoms.append(r)

        playlist.append(songs[r])

    return playlist

def printSong(song):
    print(song[6] + " : " + song[3] + " | " + song[1])

def printList(playlist):
    for i in playlist:
        printSong(i)

list1 = createRandom()

printList(list1)