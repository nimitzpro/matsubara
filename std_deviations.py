import sqlite3
import numpy as np
db_path = "Z:\\other\\spotify_backup.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

feature_list = ["acousticness", "instrumentalness", "speechiness", "energy", "valence"]


def stdev(feature):
    count, avg = cur.execute(f"select count({feature}), avg({feature}) from track_features where {feature} != 0.0;").fetchone()

    sum = 0
    X = cur.execute(f"select {feature} from track_features where {feature} != 0.0").fetchall()
    for x in X:
        sum += (x[0] - avg)**2
    sum /= count

    return sum


for f in feature_list:
    print(stdev(f))


'''
STDEVS
0.12559659911354276
0.14243493379256492
0.013280411877616508
0.07070953181026222
0.07261811636756003
'''