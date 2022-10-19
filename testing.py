#!/usr/bin/python

import sqlite3
import random

conn = sqlite3.connect("data/track_metadata.db")

cur = conn.cursor()

# result = cur.execute("SELECT count(*) FROM songs")
# print(result.fetchone())
# def printSong(song): FOR songs table
#     print(song[6] + " : " + song[3] + " | " + song[1])


ARTIST_NAME = 3
NEW_ID = 0
TITLE = 1
RELEASE = 2

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
    print(song[ARTIST_NAME] + " : " + song[RELEASE] + " | " + song[TITLE])

def printList(playlist):
    for i in playlist:
        printSong(i)

def printAll(playlist):
    print(playlist.fetchall())


def createFromSameArtist(artist):
    playlist = cur.execute("SELECT * FROM songs_simple WHERE artist_name LIKE '" + artist + "'")
    return playlist

def createFromContainingTitle(title):
    playlist = cur.execute("SELECT * FROM songs_simple WHERE title LIKE '%" + title + "%'")
    return playlist

def findSongsByWord(word, artist_name="", amount=20):
     return cur.execute("SELECT * FROM songs_simple WHERE title LIKE '%" + word + "%' AND (title <> '" + word + "' OR artist_name <> '"+ artist_name + "') LIMIT "+ str(amount)).fetchall()


def createFromTitleWord(word, case=0, n=10):
    playlist = []
    # words = [word]

    i = 0
    amount = 20
    while i < n:
        songs = findSongsByWord(word)
        if songs is None or songs == []:
            print("\n")
            return playlist

        song = songs[random.randint(0, len(songs)-1)]
        while song in playlist:
            song = songs[random.randint(0, len(songs)-1)]
            amount -= 1
            if amount < 1:
                print("\n")
                return playlist

        title = song[TITLE]
        print(word, "->", title, end=" || ")
        titleArray = title.split()
        if case == "set first word":
            word = titleArray[0]
        elif case == "set last word":
            word = titleArray[-1]
        else:
            word = titleArray[random.randint(0, len(titleArray)-1)]

        word = ''.join(filter(str.isalnum, word))

        playlist.append(song)
        amount = 20
        i += 1

    print("\n")
    return playlist

list1 = createRandom()
# printAll(list1)
printList(list1)
print("\n\n")

list2 = createFromSameArtist("Abba")
printList(list2)
print("\n\n")

list3 = createFromContainingTitle("Eagle")
printList(list3)
print("\n\n")

list4 = createFromTitleWord("Apple")
printList(list4)
print("\n\n")

printList(createFromTitleWord("Apple", "set first word"))
print("\n\n")

printList(createFromTitleWord("Apple", "set last word"))


# def createSimilarityTitles(n=100):




# import h5py

# filename = "data/msd_summary_file.h5"

# h5 = h5py.File(filename,'r')

# print(list(h5.keys()))
# musicbrainz = h5['musicbrainz']  # also metadata, analysis
# print(list(musicbrainz))
# h5.close()
