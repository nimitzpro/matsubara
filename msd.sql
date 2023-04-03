select * from songs
where title like "%symphony%"
order by title

select count(*) from songs

select * from songs
order by track_7digitalid asc



select * from artist

SELECT * FROM songs_simple

select * from artist_term

-- CREATE TABLE similarities(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     aid TEXT,
--     aid2 TEXT,
--     similarity REAL
-- );

-- CREATE TABLE similarities_mbtags(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     aid TEXT,
--     aid2 TEXT,
--     similarity REAL
-- );

SELECT * FROM similarities_mbtags;

-- DROP TABLE similarities;
-- SELECT count(*) FROM similarities WHERE similarity = 0.0;
-- DELETE FROM similarities
-- WHERE similarity = 0.0;
select * from similarities limit 30;
SELECT count(*) from similarities;

SELECT * FROM similarities WHERE aid = 'ARGU8JD1187B9AA1DA' ORDER BY similarity DESC LIMIT 10
SELECT * FROM similarities WHERE aid = 'ARGU8JD1187B9AA1DA' LIMIT 1

select * from similarities where aid2 = "ARZZZAI124207819C9" limit 20;
select * from similarities where id = (select max(id) from similarities);



SELECT artist_id, artist_name, title FROM songs2 WHERE title LIKE "Sweet Home Alabama" LIMIT 1

select * from songs2 where artist_id = (select max(artist_id) from songs2);
select distinct artist_id from songs2 order by artist_id desc limit 5;
SELECT DISTINCT artist_id FROM songs2 where id >= 295929532;

select artist_id, term from a_term group by artist_id


-- CREATE TABLE a_term(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     artist_id TEXT,
--     term TEXT
-- );
--  MOVE TABLE BETWEEN FILES
-- ATTACH DATABASE "data/track_metadata.db" AS other;
-- INSERT INTO other.a_term
-- SELECT * FROM artist_term;
-- DETACH other;

-- CREATE TABLE a_mbtag(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     artist_id TEXT,
--     mbtag TEXT
-- );
--  MOVE TABLE BETWEEN FILES
-- ATTACH DATABASE "C:\Users\astro\Documents\matsubara\data\track_metadata.db" AS other;
-- INSERT INTO other.a_mbtag (artist_id, mbtag)
-- SELECT * FROM artist_mbtag;
-- DETACH other;

-- Schema Layout
-- PRAGMA table_info(artist_term);
-- .schema a_term
-- select * from a_term
-- List Tables
.tables


select count(*) from songs2 where year IS NULL or year = 0

--  .tables for:
--  track_metadata.db
--  songs
--  songs2 (songs with id)
--  songs_simple (simplified table with id)

--  artist_term.db
--  artist_mbtag, artist_term, artists, mbtags, terms

--  artist_similarity.db
--  artists, similarity



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
