import sqlite3
import random

conn = sqlite3.connect("Z:\\other\\spotify_backup.db")
cur = conn.cursor()

trackN = 2262292 # total tracks in DB

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

def main(amount):
    string = genRandomListString(n=amount)
    return [s[0] for s in cur.execute("SELECT track_uri FROM tracks WHERE rowid in " + string).fetchall()]