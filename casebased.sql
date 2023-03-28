create table tracks(
    track_uri TEXT primary key,
    track_name TEXT,
    artist_uri TEXT,
    artist_name TEXT,
    album_uri TEXT,
    album_name TEXT,
    duration_ms INT
);

DELETE FROM tracks
WHERE EXISTS (
  SELECT 1 FROM tracks p2 
  WHERE tracks.track_uri = p2.track_uri
  AND tracks.rowid > tracks.rowid
);

create table playlist_tracks(
    pid INT,
    pindex INT,
    track_uri TEXT
);

create table playlists(
    pid INT primary key,
    name TEXT,
    collaborative INT,
    num_tracks INT,
    num_albums INT,
    num_followers INT
);

.tables

-- DROP table tracks;

SELECT DISTINCT * FROM tracks limit 0, 20;

select count(*) from playlist_tracks;
select count(*) from tracks;
select * from playlist_tracks WHERE pid = 1;
select count(*) from playlists WHERE collaborative = 1;

-- DROP TABLE playlist_tracks;

.schema tracks

create table seq2_occurences(
    track_uri1 TEXT,
    track_uri2 TEXT,
    prevalence INT
);

create table seq2_simple(
    track_uri1 TEXT,
    track_uri2 TEXT
);

select count(*) from seq2_occurences;
select count(*) from (select distinct * from seq2_simple);
select * from seq2_simple limit 20;
select count(*) from seq2_simple where track_uri1 = "spotify:track:0UaMYEvWZi0ZqiDOoHU3YI" and track_uri2 = "spotify:track:6I9VzXrHxO9rA9A5euc8Ak";

SELECT * from playlist_tracks ORDER BY pid ASC, pindex ASC limit 300;

SELECT COUNT(*) FROM track_features;
select * from track_features where track_uri = "spotify:track:1M76LbtuDzesSKZGQ42bRz";
select track_uri, count(track_uri) from track_features group by track_uri order by 2 asc;
select max(rowid), * from tracks;

select * from track_features limit 20;
select max(rowid), * from track_features
SELECT rowid, track_uri FROM tracks WHERE rowid >= 1267443 LIMIT 20
select rowid, * from tracks where track_uri = 'spotify:track:4M8WOAm0hN57xvPbTaXHfj';

create table track_features(
    track_uri TEXT primary key,
    acousticness REAL,
    danceability REAL,
    energy REAL,
    instrumentalness REAL,
    music_key INT,
    liveness REAL,
    loudness REAL,
    mode INT,
    speechiness REAL,
    tempo REAL,
    time_signature INT,
    valence REAL
);

create table artist_genres(
    artist_uri TEXT,
    genre TEXT
);
select * from artist_genres limit 30;
drop table artist_genres;

select count(*) from artist_genres;
select count(distinct artist_uri) from artist_genres;

select COUNT(DISTINCT artist_uri) from tracks;

select * from tracks limit 30;



SELECT pid, pindex FROM playlist_tracks WHERE track_uri = 'spotify:track:6I9VzXrHxO9rA9A5euc8Ak';

SELECT track_uri FROM playlist_tracks WHERE pid = 38 AND pindex-1 = 30;