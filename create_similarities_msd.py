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

def genRandomListString(n=10, s=1000000):
    randoms = genRandomList(n, s)
    string = "("
    for r in randoms:
        string += str(r) + ", "
    string = string[:len(string)-2:] + ")"

    return string

def createRandom():
    string = genRandomListString()
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

# list1 = createRandom()
# printAll(list1)
# printList(list1)
# print("\n\n")

# list2 = createFromSameArtist("Abba")
# printList(list2)
# print("\n\n")

# list3 = createFromContainingTitle("Eagle")
# printList(list3)
# print("\n\n")

# list4 = createFromTitleWord("Apple")
# printList(list4)
# print("\n\n")

# printList(createFromTitleWord("Apple", "set first word"))
# print("\n\n")

# printList(createFromTitleWord("Apple", "set last word"))

def createRandomFromSameGenre(genre):
    cur.execute("SELECT artist_name, title FROM songs2 WHERE artist_id in (SELECT artist_id FROM a_term WHERE term LIKE '" + genre + "');")
    print(cur.fetchall())

# createRandomFromSameGenre("anime")

def jaccard(n1, n2):
    n1 = set(n1)
    n2 = set(n2)

    j = len(n1.intersection(n2)) / len(n1.union(n2))

    return j

# print(jaccard([1,2,3,5,6,1],[2,4,5]))

def createSimilarities():
    artist_ids = cur.execute("SELECT DISTINCT artist_id FROM songs2").fetchall()
    d = {}
    a_term = cur.execute("SELECT * FROM a_term;").fetchall()
    for a in a_term:
        if a[1] not in d.keys():
            d[a[1]] = [a[2]]
        else:
            d[a[1]].append(a[2])

    artCount = len(d.keys())
    #print(artCount)

    similarities = {}
    for i_a, a in enumerate(d):
        i_b = i_a + 1
        l = list(d.keys())
        while i_b < artCount:
#            print(a, enumerate(d)[i_b])
            print(a, l[i_b])
            #exit()
            j = jaccard(d[a], d[l[i_b]])
            #print(d[a], "\n", d[l[i_b]])
            print(str(j))
            #print(a, l[i_b])
            #exit()
            if a in similarities.keys():
                if l[i_b] in [a2[0] for a2 in similarities[a]]:
                    i_b += 1
                    continue
            if l[i_b] in similarities.keys():
                if a in [a2[0] for a2 in similarities[l[i_b]]]:
                    i_b += 1
                    continue

            if a not in similarities.keys():
                similarities[a] = [[l[i_b], j]]
            else:
                similarities[a].append([l[i_b], j])

            i_b += 1

            #if i_b > 10:
            #    break

        #break
    #print(str(similarities))
#        print([list(similarities.keys())[i] for i in range(10)])


    z = "("
    for i in similarities:
        for j in similarities[i]:
            z += "('" + i + "', '" + j[0] + "', " + str(j[1]) + "),"

    z = z[:-1] + ");"

    cur.execute("INSERT INTO similarities (aid, aid2, similarity) VALUES" + z)

# createSimilarities()
