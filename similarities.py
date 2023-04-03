#!/usr/bin/python

import sqlite3
import random

conn = sqlite3.connect("Z:\\other\\spotify_backup.db")
cur = conn.cursor()

trackN = 2262292

def genRandomList(n, s):
    randoms = []
    while len(randoms) < n:
        x = random.randint(0, s-1)
        if x not in randoms:
            randoms.append(x)
    return randoms

def genRandomListString(n=10, s=trackN):
    randoms = genRandomList(n, s)
    string = "("
    for r in randoms:
        string += str(r) + ", "
    string = string[:len(string)-2:] + ")"

    return string

def createRandom():
    string = genRandomListString()
    playlist = cur.execute("SELECT track_uri FROM tracks WHERE row_id in " + string)
    return playlist


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

def createRandomFromSameGenre(genre, N=10):
    cur.execute("SELECT artist_name, track_name FROM tracks WHERE artist_uri in (SELECT artist_uri FROM artist_genres WHERE genre LIKE '" + genre + "') LIMIT " + str(N) +";")
    print(cur.fetchall())

# createRandomFromSameGenre("anime")

def jaccard(n1, n2):
    n1 = set(n1)
    n2 = set(n2)

    j = len(n1.intersection(n2)) / len(n1.union(n2))

    return j

# print(jaccard([1,2,3,5,6,1],[2,4,5]))

def createSimilarities():
    # artist_uris = cur.execute("SELECT DISTINCT artist_uri FROM tracks where artist_uri >= 'AR7C9271187FB39BF8'").fetchall()
    d = {}
    a_term = cur.execute("SELECT * FROM artist_genres;").fetchall()
    for a in a_term:
        if a[0] not in d.keys():
            d[a[0]] = [a[1]]
        else:
            d[a[0]].append(a[1])

    artCount = len(d.keys())
    similarities = {}
    z = ""
    for i_a, a in enumerate(d):
        i_b = i_a + 1
        if not i_b % 10:
            cur.execute("INSERT INTO similarities (artist_uri, artist_uri2, similarity) VALUES " + z[:-1] + ";")
            conn.commit()
            z = ""

        l = list(d.keys())
        while i_b < artCount:
            j = jaccard(d[a], d[l[i_b]])
            if j > 0: # Remove artists with 0 similarity
                z += "('" + a + "', '" + l[i_b] + "', " + str(j) + "),"
            i_b += 1

        if not i_b % 1000:
            print(i_b + " / " + artCount + "...")

    if len(z) > 0:
        cur.execute("INSERT INTO similarities (artist_uri, artist_uri2, similarity) VALUES " + z[:-1] + ";")
        conn.commit()

# createSimilarities()

def createFromSimilarity(title, pair_props=False, n=10):
    song = cur.execute("SELECT artist_uri, artist_name, title FROM tracks WHERE title LIKE %" + title + "%").fetchone()
    similar_artists = cur.execute("SELECT artist_uri2 FROM similarities WHERE artist_uri = " + song[0] + "ORDER BY similarity DESC LIMIT " + n).fetchall()
    similar_artists2 = cur.execute("SELECT artist_uri FROM similarities WHERE artist_uri2 = " + song[0] + "ORDER BY similarity DESC LIMIT " + n).fetchall()

    s = sorted(similar_artists + similar_artists2, key=lambda lst: lst[3])

    if pair_props:
        avg = 0.0
        min_sim = 0.0
        max_sim = 0.0
        for i in s:
            avg += i[3]
            if i[3] > max_sim:
                max_sim = i[3]
            if i[3] < min_sim:
                min_sim = i[3]

        avg /= n

        print("average similarity:", str(avg))
        print("closest artist:", str(max_sim))
        print("furthest artist:", str(min_sim))

    return s[:n]

def createFromSimilarityPairs(artist_name="", title="", pair_props=False, n=10):
    songs = []
    songs.append(cur.execute(f"SELECT artist_uri, track_uri FROM tracks WHERE title LIKE '%{title}%' AND artist_name LIKE '%{artist_name}%'").fetchone())
    artist_uris = f"'{songs[0][0]}'"
    s = []
    for i in range(n - 1):
        similar_artist = cur.execute(f"SELECT * FROM similarities WHERE artist_uri = '{songs[-1][0]}' AND artist_uri2 NOT IN ({artist_uris}) ORDER BY similarity DESC LIMIT 1").fetchone()
        similar_artist2 = cur.execute(f"SELECT * FROM similarities WHERE artist_uri2 = '{songs[-1][0]}' AND artist_uri NOT IN ({artist_uris}) ORDER BY similarity DESC LIMIT 1").fetchone()
        print(str(similar_artist))
        print(str(similar_artist2))
        if not similar_artist:
            if not similar_artist2:
                return str(songs)
            songs.append(cur.execute("SELECT artist_uri FROM tracks WHERE artist_uri = '" + similar_artist2[0] + "' LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist2[0]}'"
            s.append(similar_artist2)
            continue
        if not similar_artist2:
            songs.append(cur.execute("SELECT artist_uri FROM tracks WHERE artist_uri = '" + similar_artist[1] + "' LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist[1]}'"
            s.append(similar_artist)
            continue

        if similar_artist[2] > similar_artist2[2]:
            songs.append(cur.execute("SELECT artist_uri FROM tracks WHERE artist_uri = '" + similar_artist[1] + "' LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist[1]}'"
            s.append(similar_artist)
        else:
            songs.append(cur.execute("SELECT artist_uri FROM tracks WHERE artist_uri = '" + similar_artist2[0] + "' LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist2[0]}'"
            s.append(similar_artist2)

    if pair_props:
        avg = 0.0
        min_sim = (0, "", "", 1.0)
        max_sim = (0, "", "", 0.0)
        for i in s:
            avg += i[3]
            if i[3] > max_sim[3]:
                max_sim = i
            if i[3] < min_sim[3]:
                min_sim = i
        avg /= n
        print("average similarity:", str(avg))
        print("closest pair of artists:", str(max_sim))
        print("furthest pair of artists:", str(min_sim))

    return [s[1] for s in songs]

# print(createFromSimilarityPairs("yes", "roundabout", True))