create table tracks(
    track_uri TEXT primary key,
    track_name TEXT,
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
    pid TEXT,
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

SELECT DISTINCT * FROM tracks limit 20;

select count(*) from tracks;

select * from playlists WHERE collaborative = 0;

DROP TABLE playlists;

.schema playlists

-- DROP TABLE playlist_tracks;