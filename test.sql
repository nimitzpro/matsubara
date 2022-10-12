select * from songs
where title like "%symphony%"
order by title

select count(*) from songs

select * from songs
order by track_7digitalid asc



select * from artist

SELECT * FROM songs_simple


; .tables for:
; track_metadata.db
; songs
; songs2 (songs with id)
; songs_simple (simplified table with id)

; artist_term.db
; artist_mbtag, artist_term, artists, mbtags, terms

; artist_similarity.db
; artists, similarity



-- create table songs2(id integer primary key autoincrement, 
--     track_id text,
--     title text, 
--     song_id text, 
--     release text, 
--     artist_id text, 
--     artist_mbid text, 
--     artist_name text, 
--     duration real, 
--     artist_familiarity real, 
--     artist_hotttnesss real, 
--     year int, 
--     track_7digitalid int, 
--     shs_perf int, 
--     shs_work int)

-- insert into songs2(
--     track_id, 
--     title, 
--     song_id, 
--     release, 
--     artist_id, 
--     artist_mbid, 
--     artist_name,
--     duration, 
--     artist_familiarity, 
--     artist_hotttnesss, 
--     year, 
--     track_7digitalid, 
--     shs_perf, 
--     shs_work) select * from songs

-- drop table songs2
-- select * from songs2

-- CREATE TABLE songs_simple(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     title TEXT,
--     release TEXT,
--     artist_name TEXT,
--     duration TEXT,
--     year INT)

-- INSERT INTO songs_simple(
--     title,
--     release,
--     artist_name,
--     duration,
--     year
--     ) SELECT title, release, artist_name, duration, year FROM songs