import sqlite3
import random
import time

db_path = "spotify_sample.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

def main(seed, N=10):
    songs = []
    songs.append(cur.execute(f"SELECT artist_uri, track_uri FROM tracks WHERE track_uri = '{seed}'").fetchone())
    artist_uris = f"'{songs[0][0]}'"
    s = []
    for i in range(N - 1):
        similar_artist = cur.execute(f"SELECT * FROM similarities WHERE artist_uri = '{songs[-1][0]}' AND artist_uri2 NOT IN ({artist_uris}) ORDER BY similarity DESC LIMIT 1").fetchone()
        similar_artist2 = cur.execute(f"SELECT * FROM similarities WHERE artist_uri2 = '{songs[-1][0]}' AND artist_uri NOT IN ({artist_uris}) ORDER BY similarity DESC LIMIT 1").fetchone()
        # print(str(similar_artist))
        # print(str(similar_artist2))
        if not similar_artist:
            if not similar_artist2:
                return str(songs)
            songs.append(cur.execute("SELECT artist_uri, track_uri FROM tracks WHERE artist_uri = '" + similar_artist2[0] + "' ORDER BY RANDOM() LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist2[0]}'"
            s.append(similar_artist2)
            continue
        if not similar_artist2:
            songs.append(cur.execute("SELECT artist_uri, track_uri FROM tracks WHERE artist_uri = '" + similar_artist[1] + "' ORDER BY RANDOM() LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist[1]}'"
            s.append(similar_artist)
            continue

        if similar_artist[2] > similar_artist2[2]:
            songs.append(cur.execute("SELECT artist_uri, track_uri FROM tracks WHERE artist_uri = '" + similar_artist[1] + "' ORDER BY RANDOM() LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist[1]}'"
            s.append(similar_artist)
        else:
            songs.append(cur.execute("SELECT artist_uri, track_uri FROM tracks WHERE artist_uri = '" + similar_artist2[0] + "' ORDER BY RANDOM() LIMIT 1;").fetchone())
            artist_uris += f", '{similar_artist2[0]}'"
            s.append(similar_artist2)

    return [s[1] for s in songs]

def solo(s="", N=10):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()
    
    if s:
        print(",".join(main(s, N)))
    else:
        while True:
            print("Enter song name:", end=" ")
            title = input()
            query = cur.execute(f"SELECT track_uri, track_name, artist_name FROM tracks WHERE track_name LIKE '%{title}%' LIMIT 20;").fetchall()
            print("\n".join([f"{s[0]} - {s[1]}" for s in enumerate(query)]))
            print("Select by index:", end=" ")
            index = int(input())
            if index == -1:
                continue
            else:
                s = query[index][0]
                break
        print(",".join(main(s, N)))

if __name__ == "__main__":
    ''' Timing function '''
    # tracks = ["spotify:track:4aVuWgvD0X63hcOCnZtNFA", "spotify:track:2R7858bg0GHuBBxjTyOL7N", "spotify:track:0kTZWRzfmqDN4boykkjUXH", "spotify:track:6I9VzXrHxO9rA9A5euc8Ak", "spotify:track:1R2SZUOGJqqBiLuvwKOT2Y"]
    # times = []
    # res = []
    # for t in tracks:
    #     start = time.perf_counter()
    #     r = main(t)
    #     end = time.perf_counter()
    #     res.append(r)
    #     times.append(float(f"{end - start:0.3f}"))
    # print(res)
    # print(times)

    solo()
    solo("spotify:track:4aVuWgvD0X63hcOCnZtNFA", N=10)