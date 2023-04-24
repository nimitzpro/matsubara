import sqlite3
import random
import time

conn = sqlite3.connect("Z:\\other\\spotify_backup.db")
cur = conn.cursor()

def main(seed, n=10):
    songs = []
    songs.append(cur.execute(f"SELECT artist_uri, track_uri FROM tracks WHERE track_uri = '{seed}'").fetchone())
    artist_uris = f"'{songs[0][0]}'"
    s = []
    for i in range(n - 1):
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

if __name__ == "__main__":
    tracks = ["spotify:track:4aVuWgvD0X63hcOCnZtNFA", "spotify:track:2R7858bg0GHuBBxjTyOL7N", "spotify:track:0kTZWRzfmqDN4boykkjUXH", "spotify:track:6I9VzXrHxO9rA9A5euc8Ak", "spotify:track:1R2SZUOGJqqBiLuvwKOT2Y"]
    times = []
    res = []
    for t in tracks:
        start = time.perf_counter()
        r = main(t)
        end = time.perf_counter()
        res.append(r)
        times.append(float(f"{end - start:0.3f}"))

    print(res)
    print(times)