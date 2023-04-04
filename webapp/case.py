import sqlite3
import numpy as np
from multiprocessing import Pool
from collections import Counter

db_path = "Z:\\other\\spotify_backup.db"

def var_attr(l, gamma, delta):
    mul_attr = 1
    i = 0
    while i < len(l) - 1:
        j = i + 1
        while j < len(l) and j - i < gamma:
            if l[j] != 0 and l[i] != 0 and abs(l[j] - l[i]) > delta:
                mul_attr *= ((j-i) / gamma)
                i = j
                break
            j += 1
        i += 1
    return mul_attr

def fetch(x):
    con = sqlite3.connect(db_path, check_same_thread=False)
    c = con.cursor()
    return c.execute(f"SELECT pid, track_uri FROM playlist_tracks WHERE {x} ORDER BY pid;").fetchall()

def batch_phi(songs, t, pre):
    con = sqlite3.connect(db_path, check_same_thread=False)
    c = con.cursor()
    Q_s = "(" + ",".join(["'"+i+"'" for i in songs]) + ")" # song uris
    if not pre:
        phis = dict([[b[0], float(b[1])] for b in c.execute(f"SELECT track_uri2, COUNT(*) FROM seq2_simple WHERE track_uri1 = '{t}' AND track_uri2 in {Q_s} GROUP BY track_uri2 ORDER BY track_uri2;").fetchall()])
    else:
        phis = dict([[a[0], float(a[1])] for a in c.execute(f"SELECT track_uri1, COUNT(*) FROM seq2_simple WHERE track_uri1 in {Q_s} AND track_uri2 = '{t}' GROUP BY track_uri1 ORDER BY track_uri1;").fetchall()])
    return phis

def batch_rel(setting, fetched_tracks, t):
    con = sqlite3.connect(db_path, check_same_thread=False)
    c = con.cursor()
    Q = fetched_tracks
    Q_s = "(" + ",".join(["'"+i+"'" for i in Q[1]]) + ")" # song uris
    if not setting:
        phis = dict([[b[0], float(b[1])] for b in c.execute(f"SELECT track_uri2, COUNT(*) FROM seq2_simple WHERE track_uri1 = '{t}' AND track_uri2 in {Q_s} GROUP BY track_uri2 ORDER BY track_uri2;").fetchall()])
    else:
        phis = dict([[a[0], float(a[1])] for a in c.execute(f"SELECT track_uri1, COUNT(*) FROM seq2_simple WHERE track_uri1 in {Q_s} AND track_uri2 = '{t}' GROUP BY track_uri1 ORDER BY track_uri1;").fetchall()])

    if False: # future possible variability in pattern size, adding weighting based on length
        alpha = 0.5
        theta = 2
        lq = len(q)
    beta = 0.5 # popularity weighting

    Q_s_filtered = "(" + ",".join(["'"+i+"'" for i in phis.keys()]) + ")"
    counts = np.transpose(c.execute(f"SELECT COUNT(*) FROM playlist_tracks WHERE track_uri in {Q_s_filtered} GROUP BY track_uri ORDER BY track_uri;").fetchall())[0]
    psis = np.power(counts, beta)
    rels = np.divide(psis, list(phis.values()))
    rel_d = {}
    pkeys = list(phis.keys())
    for z in range(len(Q[0])):
        if Q[1][z] in phis.keys():
            if Q[0][z] in rel_d.keys():
                rel_d[Q[0][z]] += rels[pkeys.index(Q[1][z])]
            else:
                rel_d[Q[0][z]] = rels[pkeys.index(Q[1][z])]
    return rel_d

def slim_var(song_features): # todo: fine-tuning deltas and gammas
    delta_diffs = [0.25, 1, 0.25, 0.25, 0.25]
    gammas = [3, 3, 3, 3, 3]
    feature_list = np.array(song_features).transpose()
    total_attrs = [var_attr(feature_list[i], gammas[i], delta_diffs[i]) for i in range(len(gammas))]
    total = 1
    for attr in total_attrs:
        total *= attr
    return total

def check_batch(x, y, pre, best_playlists):
    '''
    Check whether sequence <x, y> occurs in any of the k retrieved playlists and count them where either x is the song in the playlist and y is a list of candidates or the other way round. Returns list of candidates, occurence count for each is almost always at most 1 so was removed
    '''
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()
    if pre:
        return c.execute(f"SELECT p1.track_uri FROM playlist_tracks as p1 JOIN playlist_tracks as p2 WHERE p1.track_uri in ({x}) AND p2.track_uri = '{y}' AND p1.pid = p2.pid AND p1.pid in ({best_playlists}) AND p2.pindex - 1 = p1.pindex GROUP BY p1.track_uri;").fetchall()
    else:
        return c.execute(f"SELECT p1.track_uri FROM playlist_tracks as p1 JOIN playlist_tracks as p2 WHERE p1.track_uri in ({x}) AND p2.track_uri = '{y}' AND p1.pid = p2.pid AND p1.pid in ({best_playlists}) AND p2.pindex + 1 = p1.pindex GROUP BY p1.track_uri;").fetchall()

def slim_rel(phi, popularity):
    if False: # future variability in pattern size, adding weighting based on length
        alpha = 0.5
        theta = 2
        lq = len(q)
    beta = 0.5 # popularity weighting
    psi = 0
    psi = pow(popularity, beta)
    rel = phi / psi
    return rel

def h(phi, pop, song_features):
    return slim_rel(phi, pop) * slim_var(song_features)
    # todo: look-ahead factor L

def create_successors(css, cp, t, pre, best_playlists):
    tracks = check_batch(css, t, pre, best_playlists)
    buffer = []
    successors_buffer = []
    if tracks:
        for track in tracks:
            if pre:
                successor_playlist = [track[0]] + cp
                successors_buffer.append([successor_playlist, track[0], pre])
            else:
                successor_playlist = cp + [track[0]]
                successors_buffer.append([successor_playlist, track[0], pre])
            buffer.append(track[0])

    return successors_buffer, buffer

def main(seed, N=10, k=20):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()

    containing = cur.execute(f"SELECT pid, pindex FROM playlist_tracks WHERE track_uri = '{seed}';").fetchall()
    totals = []

    prev_cases = [f"(pid = {c[0]} AND pindex-1 = {c[1]})" for c in containing]
    prev_split = []
    for x in range(0, len(prev_cases), 900):
        prev_split.append("OR".join(prev_cases[x:x+900]))

    after_cases = [f"(pid = {c[0]} AND pindex+1 = {c[1]})" for c in containing]
    after_split = []
    for x in range(0, len(after_cases), 900):
        after_split.append("OR".join(after_cases[x:x+900]))


    print("fetching tracks...")
    fetched_prev_tracks = []
    fetched_after_tracks = []
    with Pool(32) as p:
        fetched_prev_tracks = p.map_async(fetch, prev_split)
        fetched_after_tracks = p.map_async(fetch, after_split)
        p.close()
        p.join()

    fpt = np.transpose([item for sublist in fetched_prev_tracks.get() for item in sublist])
    fat = np.transpose([item for sublist in fetched_after_tracks.get() for item in sublist])

    print("calculating relevances...")

    with Pool(32) as p:
        t2, t3 = p.starmap(batch_rel, [[0,fpt,seed], [1,fat,seed]])
        p.close()
        p.join()

    total_rels = Counter(t2) + Counter(t3)
    tr_tuples = list(total_rels.items())
    tr_tuples_sorted = sorted(tr_tuples, key = lambda relevance: relevance[1], reverse=True)
    tr_tuples_sorted = np.transpose(tr_tuples_sorted) # [:50] maybe

    s = ",".join(["'"+t+"'" for t in tr_tuples_sorted[0]])
    song_features = conn.execute(f"SELECT pt.pid, tf.acousticness, tf.instrumentalness, tf.speechiness, tf.energy, tf.valence FROM track_features as tf JOIN playlist_tracks as pt WHERE tf.track_uri = pt.track_uri AND pt.pid in ({s}) ORDER BY pt.pid ASC, pt.pindex ASC;").fetchall()
    playlist_features = {}
    for song in song_features:
        if song[0] not in playlist_features.keys():
            playlist_features[int(song[0])] = [(song[1],song[2],song[3],song[4],song[5])]
        else:
            playlist_features[int(song[0])].append((song[1],song[2],song[3],song[4],song[5]))

    print("calculating variances...")

    with Pool(32) as p:
        variances = p.map(slim_var,[playlist_features[int(pid)] for pid in tr_tuples_sorted[0]])
        p.close()
        p.join()
    rhos = np.multiply(np.array(variances).astype(float), tr_tuples_sorted[1].astype(float))

    totals = [(tr_tuples_sorted[0][i], rhos[i]) for i in range(len(rhos))]
    containing_sorted = sorted(totals, key = lambda prevalence: prevalence[1], reverse=True)
    best_k_playlists = [p[0] for p in containing_sorted[:k]] # list of k sorted playlist pids

    best_k_playlists_string = ",".join([f"'{b}'" for b in best_k_playlists])
    candidate_songs = [s[0] for s in cur.execute(f"SELECT DISTINCT track_uri FROM playlist_tracks WHERE pid in ({best_k_playlists_string});").fetchall()]
    current_playlist = [seed]
    # candidate_playlists = [current_playlist]
    candidate_songs_str = ",".join(["'"+c+"'" for c in candidate_songs])
    song_features = conn.execute(f"SELECT pt.track_uri, tf.acousticness, tf.instrumentalness, tf.speechiness, tf.energy, tf.valence FROM track_features as tf JOIN playlist_tracks as pt WHERE tf.track_uri = pt.track_uri AND pt.track_uri in ({candidate_songs_str},'{seed}') ORDER BY pt.pid ASC, pt.pindex ASC;").fetchall()

    song_f = {}
    for song in song_features:
        song_f[song[0]] = song[1:]
    song_popularity = conn.execute(f"SELECT track_uri, COUNT(*) FROM playlist_tracks WHERE track_uri in ({candidate_songs_str}) GROUP BY track_uri;").fetchall()
    song_p = {}
    for song in song_popularity:
        song_p[song[0]] = int(song[1])

    print(f"generating playlist from {k} input playlists...")
    # print(candidate_songs_str)

    # print(best_k_playlists_string)

    while len(current_playlist) < N:
        t = current_playlist[0]
        T = current_playlist[-1]
        successors_of_current_playlist = []
        candidate_songs_str = ",".join(["'"+c+"'" for c in candidate_songs if c not in current_playlist])

        with Pool(32) as p:
            pre_buffer, post_buffer = p.starmap(create_successors, [[candidate_songs_str, current_playlist, t, True, best_k_playlists_string], [candidate_songs_str, current_playlist, T, False, best_k_playlists_string]])
            p.close()
            p.join()

        successors_of_current_playlist = pre_buffer[0] + post_buffer[0]

        if len(successors_of_current_playlist) == 0:
            # discard current_playlist
            return "failed to create playlist"
        else: # pop new current_playlist from candidate_playlists
            with Pool(32) as p:
                phis_pres, phis_posts = p.starmap(batch_phi, [[pre_buffer[1], current_playlist[0], True], [post_buffer[1], current_playlist[-1], False]])
                p.close()
                p.join()

            succ_data = []
            for succ in successors_of_current_playlist:
                if succ[2]:
                    phi = phis_pres[succ[1]]
                else:
                    phi = phis_posts[succ[1]]
                succ_data.append((phi, song_p[succ[1]], [song_f[x] for x in succ[0]]))

            with Pool(32) as p:
                ratings = p.starmap(h, succ_data)
                p.close()
                p.join()

            for i in range(len(successors_of_current_playlist)):
                successors_of_current_playlist[i].append(ratings[i])

            successors_of_current_playlist = sorted(successors_of_current_playlist, key=lambda x: x[3], reverse=True)
            current_playlist = successors_of_current_playlist[0][0]

    return current_playlist

if __name__ == "__main__":
    print(main("spotify:track:3mScGCzxiXA9OaHdBeuk7O"))