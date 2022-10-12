#!/usr/bin/python

import sqlite3
import random

conn = sqlite3.connect("data/track_metadata.db")

cur = conn.cursor()

# result = cur.execute("SELECT count(*) FROM songs")
# print(result.fetchone())
# def printSong(song): FOR songs table
#     print(song[6] + " : " + song[3] + " | " + song[1])

def genRandomList(n, s):
    randoms = []
    while len(randoms) < n:
        x = random.randint(0, s-1)
        if x not in randoms:
            randoms.append(x)
    return randoms

def createRandom(n=10, s=1000000):
    randoms = genRandomList(n, s)
    string = "("
    for r in randoms:
        string += str(r) + ", "
    string = string[:len(string)-2:] + ")"
    
    playlist = cur.execute("SELECT * FROM songs_simple WHERE id in " + string)

    return playlist

def printSong(song):
    print(song[3] + " : " + song[2] + " | " + song[1])

def printList(playlist):
    for i in playlist:
        printSong(i)

list1 = createRandom()

printList(list1)
