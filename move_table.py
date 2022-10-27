#!/usr/bin/python

import sqlite3
import random

conn = sqlite3.connect("data/artist_term.db")

cur = conn.cursor()

cur.execute("ATTACH DATABASE 'data/track_metadata.db' AS other;")
cur.execute("INSERT INTO other.a_term (artist_id, term) SELECT * FROM artist_term;")
conn.commit()
cur.execute("DETACH other;")
conn.commit()
conn.close()