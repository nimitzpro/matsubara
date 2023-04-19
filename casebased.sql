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

select distinct count(*) from tracks;

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
select count(*) from seq2_simple;
select * from seq2_simple limit 56;
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

select * from tracks where track_name like '%miiro%';

select * from playlist_tracks where pid = 999884;

select * from tracks where track_uri = 'spotify:track:2374M0fQpWi3dLnB54qaLX';

SELECT track_uri1, COUNT(*) FROM seq2_simple WHERE track_uri2 = 'spotify:track:4aVuWgvD0X63hcOCnZtNFA' GROUP BY track_uri1 ORDER BY COUNT(*) DESC;


SELECT p1.pid, p1.pindex, p2.pindex FROM playlist_tracks as p1 JOIN playlist_tracks as p2 WHERE p1.track_uri = 'spotify:track:4aVuWgvD0X63hcOCnZtNFA' AND p2.track_uri = 'spotify:track:2Nz6aF1umHh5Et6I5H581L' AND p1.pid = p2.pid AND p1.pid in ('531576','965625','561943','487573','552959','106406','230157','749920','118365','177079','54044','140335','511896','903900','347383','468744','816689','256962','472466','550703') AND p1.pindex + 2 = p2.pindex;

SELECT p2.track_uri, count(*) FROM playlist_tracks as p1 JOIN playlist_tracks as p2 WHERE p1.track_uri = 'spotify:track:4aVuWgvD0X63hcOCnZtNFA' AND p2.track_uri in ('spotify:track:2Nz6aF1umHh5Et6I5H581L','spotify:track:6SKwQghsR8AISlxhcwyA9R','spotify:track:4DdF1l0DzBQy8YL2UVhPrU','spotify:track:4FXdIM78OBdw7KIY2jeM8D','spotify:track:5nkYHBWXu7KCgcdwP6jcB1','spotify:track:4aVuWgvD0X63hcOCnZtNFA','spotify:track:7zVCrzzEJU7u24sbJPXA5W','spotify:track:0S5EEpFAHcT7cm5XOASc29','spotify:track:2WpTJCv2LrNGhVTvmEBiSS','spotify:track:12qZHAeOyTf93YAWvGDTat','spotify:track:79cuOz3SPQTuFrp8WgftAu','spotify:track:6RsWqX8zABZLhZydXxEFOm','spotify:track:0s6OWiWGuiCcm1Muzch5A8','spotify:track:5IkhhO8Kw7lglYTWzcCxdl','spotify:track:12lZTPlXwUtrQuhEty6098','spotify:track:4QlzkaRHtU8gAdwqjWmO8n','spotify:track:4DMKwE2E2iYDKY01C335Uw','spotify:track:6NxsCnLeLd8Ai1TrgGxzIx','spotify:track:4z7maGZkAonDlXlwo8q69f','spotify:track:5lXcSvHRVjQJ3LB2rLKQog','spotify:track:5uuJruktM9fMdN9Va0DUMl','spotify:track:2B4LcSLZTDmTIFgKpjScjR','spotify:track:57DKmLJBRI5ZtiCgLUQMZY','spotify:track:5VJjhHyG8NZ5xdgG6uTb3P','spotify:track:43DeSV93pJPT4lCZaWZ6b1','spotify:track:4OTw5splgMdlYklwHMHxLK','spotify:track:4nXkbcTj3nyww1cHkw5RAP','spotify:track:1mqlc0vEP9mU1kZgTi6LIQ','spotify:track:1k1Bqnv2R0uJXQN4u6LKYt','spotify:track:6cb0HzFQPN4BGADOmSzPCw','spotify:track:01iyCAUm8EvOFqVWYJ3dVX','spotify:track:5nPdMALTEd7HOjn16oNf2X','spotify:track:5QTxFnGygVM4jFQiBovmRo','spotify:track:1HOMkjp0nHMaTnfAkslCQj','spotify:track:4YOJFyjqh8eAcbKFfv88mV','spotify:track:1q4XkQXsmgDgK2S1Umqf7D','spotify:track:6pyzBTIjcO2AMkKE6x2Otb','spotify:track:5BUD7ROiES4DBoY6z4yZPs','spotify:track:5EWPGh7jbTNO2wakv8LjUI','spotify:track:0d8ZbnRoW1TJ3qEleTrYHH','spotify:track:38yBBH2jacvDxrznF7h08J','spotify:track:152lZdxL1OR0ZMW6KquMif','spotify:track:6rbeWjEavBHvX2kr6lSogS','spotify:track:63OQWdXMq0Pe6pRpWY5gO0','spotify:track:6Z8R6UsFuGXGtiIxiD8ISb','spotify:track:6QgjcU0zLnzq5OrUoSZ3OK','spotify:track:2H3ZUSE54pST4ubRd5FzFR','spotify:track:4Z1fbYp0HuxLBje4MOZcSD','spotify:track:5DiXcVovI0FcY2s0icWWUu','spotify:track:4gr5E5KWc7o9WgeDrheed2','spotify:track:5V1AHQugSTASVez5ffJtFo','spotify:track:2SiXAy7TuUkycRVbbWDEpo','spotify:track:4bHsxqR3GMrXTxEPLuK5ue','spotify:track:6pmuu4qSz2WrtGkBjUfyuz','spotify:track:41pFyxOpS119Pb8JEzhx0w','spotify:track:7vidktgNZFQylTgH1GEnMs','spotify:track:3vV3cr2TpPqFk07zxYUbla','spotify:track:4o6BgsqLIBViaGVbx5rbRk','spotify:track:6qUEOWqOzu1rLPUPQ1ECpx','spotify:track:1lguQJjlNrIOoOylYVZN3M','spotify:track:3Gq8JNmlCJ5KdYwrNAZC2v','spotify:track:40riOy7x9W7GXjyGp4pjAv','spotify:track:2zvot9pY2FNl1E94kc4K8M','spotify:track:0qRR9d89hIS0MHRkQ0ejxX','spotify:track:5sMIFZaagXcwKiSfl95zIW','spotify:track:17FqORwDoxSb1SkO2sN0mM','spotify:track:1hQr0D1ZXbGHFcWLhusijv','spotify:track:6tP1NaAIoxSTzeFgCUO66V','spotify:track:4qO03RMQm88DdpTJcxlglY','spotify:track:5aeiP4cwXeSraMJzdjG6LE','spotify:track:7hzY0LHz8KdEr1PowHhbdu','spotify:track:3ZKQVyxT4Jg2lLZRLs7Vgo','spotify:track:28NBmftocOzTPEb6OYA9fW','spotify:track:0pu8DQu3XlzJsMUMVCYY27','spotify:track:65lHwG8JFJs67PnOUhCYPq','spotify:track:0G3fbPbE1vGeABDEZF0jeG','spotify:track:0bSTBRdN4iBepZ8bUcVq0S','spotify:track:383Xl5QTigwj3QiA3Qc6S7','spotify:track:6ztstiyZL6FXzh4aG46ZPD','spotify:track:1CQqupcyMg7176PPmIVmSj','spotify:track:6HZKlK1mDDBsILMoNNncxL','spotify:track:6c0G8K6G2LlIfJTsRLJjfs','spotify:track:6EOdY7I7Xm1vPP1cyaGbWZ','spotify:track:72ahyckBJfTigJCFCviVN7','spotify:track:5gys5nzVQIYhgHIfiOJYva','spotify:track:3DHWxeWr4uh19MklWjLpR0','spotify:track:1wX0xJFcM6zjqObQ2107Lm','spotify:track:2OgVsp77En2nju8pnCieVU','spotify:track:4rcHWl68ai6KvpXlc8vbnE','spotify:track:2oSpQ7QtIKTNFfA08Cy0ku','spotify:track:2rD9tU2bws0PgOPsI6aIZo','spotify:track:26fZwf1ImE4aUJ4XaqOkUg','spotify:track:0XIvZ82aDF7JiSi3ZE320u','spotify:track:0RdUX4WE0fO30VnlUbDVL6','spotify:track:1GqlvSEtMx5xbGptxOTTyk','spotify:track:1QEEqeFIZktqIpPI4jSVSF','spotify:track:02gV5Zc9ctbZxD1uTNIok5','spotify:track:0VL2zZ9Tt10nHFhG7Ks0n0','spotify:track:1MAYOJYnihOZr8fZuMv3HD','spotify:track:2uEz2uLMNj9ySHMkwuCDo5','spotify:track:0P4JuEXYJmu2Q7BTtQW5nR','spotify:track:3L9ClO1W5KmebIXTrlKShF','spotify:track:4NnWuGQujzWUEg0uZokO5M','spotify:track:1I7zHEdDx8Ny5RxzYPqsU2','spotify:track:23hrvdvkIi1X1voQG2bJH9','spotify:track:4t0Pj3iBnSCZv5pDEPNmzG','spotify:track:2Foc5Q5nqNiosCNqttzHof','spotify:track:7Ko8eQ58gmHF8m3drHGUZT','spotify:track:5b88tNINg4Q4nrRbrCXUmg','spotify:track:32OlwWuMpZ6b0aN2RZOeMS','spotify:track:3AYcyxEACnmE6d96RPubID','spotify:track:1TfqLAPs4K3s2rJMoCokcS','spotify:track:02mQcDoU5cn15U6tqZmL4e','spotify:track:5n6RDaGFSN88oRWuGtYAIN','spotify:track:2fuCquhmrzHpu5xcA1ci9x','spotify:track:3Z9PJ6xiEGmcqo2hESEB5n','spotify:track:3VZmChrnVW8JK6ano4gSED','spotify:track:0ErrsvDylBWZeAUYbqLllv','spotify:track:2s4BsyV3KhhrtsdtNfzoqb','spotify:track:5aHHf6jrqDRb1fcBmue2kn','spotify:track:0Bs0hUYxz7REyIHH7tRhL2','spotify:track:37BTh5g05cxBIRYMbw8g2T','spotify:track:2WfaOiMkCvy7F5fcp2zZ8L','spotify:track:0EMmVUYs9ZZRHtlADB88uz','spotify:track:2RTZeBJjNe91ts4S542PSd','spotify:track:33VihH9UNQMxiQS4wcPIKL','spotify:track:0upSMyj1Wzs6qyiZRuiFWD','spotify:track:3Cx4yrFaX8CeHwBMReOWXI','spotify:track:4aWn4NHlELpOehxsBaQeoe','spotify:track:6qBSGvyUzqNQv8XtnzCr9n','spotify:track:2EGaDf0cPX789H3LNeB03D','spotify:track:7o9uu2GDtVDr9nsR7ZRN73','spotify:track:5RsUlxLto4NZbhJpqJbHfN','spotify:track:3BGbqEDio3ocx1v4egIYr6','spotify:track:2771LMNxwf62FTAdpJMQfM','spotify:track:2dCcDpm6O6ocomusl5ao6p','spotify:track:5o4yGlG0PfeVUa6ClIyOxq','spotify:track:11dxtPJKR4E0wlSr0A0t47','spotify:track:5c0aiERRxHjbvu5tQ9jwAE','spotify:track:67ECoCqwmo16mC52b1S7N9','spotify:track:6EMoFOfRE7gudmtp4m5CXJ','spotify:track:1evB5tjKBN4v5zKsuordT0','spotify:track:5tz69p7tJuGPeMGwNTxYuV','spotify:track:3S2R0EVwBSAVMd5UMgKTL0','spotify:track:4nVBt6MZDDP6tRVdQTgxJg','spotify:track:3oEekS4xhmFQ88ieCVTZ7H','spotify:track:5OMwQFBcte0aWFJFqrr5oj','spotify:track:3FS2e59gXFXrcg7sN2mL5z','spotify:track:5N8nNuTmIzkZOfcxXlygUw','spotify:track:0k93MXOj0kSXo84SvSDeUz','spotify:track:1Cwsd5xI8CajJz795oy4XF','spotify:track:4r8lRYnoOGdEi6YyI5OC1o','spotify:track:6UwHnTgVozXB14CooVyVek','spotify:track:5SZ6zX4rOrEQferfFC2MfP','spotify:track:4gMgiXfqyzZLMhsksGmbQV','spotify:track:5IKLwqBQG6KU6MP2zP80Nu','spotify:track:2oiMNaVCul7qmMzpRStjCg','spotify:track:1ppuHX1oVMku5LTL0swNZP','spotify:track:5bQduNI1lNfkNbDCKhBNX6','spotify:track:1aRrJewQmqU3wMUf86VVc6','spotify:track:2yNWwardt8VzlpNBWrGYD6','spotify:track:4Ij6wDENH7lpOPIFMTU6RV','spotify:track:0dEIca2nhcxDUV8C5QkPYb','spotify:track:2374M0fQpWi3dLnB54qaLX','spotify:track:3OZ40egQbNWeTe0BnR2QKa','spotify:track:3T6R0ppqCnUW6iJhtUYhO3','spotify:track:18sytW2s53Of6NVudQyUlH','spotify:track:6xMHglHoafdDFGXS6qfwSH','spotify:track:3DJzbnITxJVoLjtYGu4NeV','spotify:track:6U0D8PIh75fnX6T6TWJLxl','spotify:track:04iBJqKEnONaF6zb2yeRwN','spotify:track:3AQNToGvoZdnBqIqM08yBS','spotify:track:3mbcW1KDbnkdgjq03JHiQ6','spotify:track:3XVozq1aeqsJwpXrEZrDJ9','spotify:track:4flpgxHWeJITvgvRLBdGsK','spotify:track:2xfdvnGUikUfZZipwVw8nO','spotify:track:2B8UVVY69xM1HrqVspYdJF','spotify:track:2lrHKMXyu8LTLxMorzJkTQ','spotify:track:0vBug2KGD9EAmIGJafqaPP','spotify:track:6SHGwVAVrpqNGUlY5j8hN5','spotify:track:4WxNNTugaVgnZajnMifdmO','spotify:track:0cqRj7pUJDkTCEsJkx8snD','spotify:track:5CGkOvlLG6hTHwojDX1JUb','spotify:track:3KYiA4vq6RPO1dE2XROXd8','spotify:track:4ECNtOnqzxutZkXP4TE3n3','spotify:track:4W4wYHtsrgDiivRASVOINL','spotify:track:0v1XpBHnsbkCn7iJ9Ucr1l','spotify:track:39lSeqnyjZJejRuaREfyLL','spotify:track:6gQUbFwwdYXlKdmqRoWKJe','spotify:track:5QhBKPqsnX1uY9fZNaAtZg','spotify:track:2PpruBYCo4H7WOBJ7Q2EwM','spotify:track:0XUfyU2QviPAs6bxSpXYG4','spotify:track:4wY7saaaFfQBcNzimjdJ5Q','spotify:track:1D066zixBwqFYqBhKgdPzp') AND p1.pid = p2.pid AND p1.pid in ('531576','965625','561943','487573','552959','106406','230157','749920','118365','177079','54044','140335','511896','903900','347383','468744','816689','256962','472466','550703') AND p1.pindex + 1 = p2.pindex GROUP BY p2.track_uri;


SELECT track_uri1, track_uri2, COUNT(*) FROM seq2_simple WHERE (track_uri1 = 'spotify:track:2Nz6aF1umHh5Et6I5H581L' AND track_uri2 = 'spotify:track:6SKwQghsR8AISlxhcwyA9R') OR (track_uri1 = 'spotify:track:2Nz6aF1umHh5Et6I5H581L' AND track_uri2 = 'spotify:track:4aVuWgvD0X63hcOCnZtNFA') GROUP BY track_uri1, track_uri2;

select * from seq2_simple limit 2
SELECT track_uri1, COUNT(*) FROM seq2_simple WHERE track_uri1 in ('spotify:track:0RdUX4WE0fO30VnlUbDVL6','spotify:track:0d8ZbnRoW1TJ3qEleTrYHH','spotify:track:1Cwsd5xI8CajJz795oy4XF','spotify:track:1D066zixBwqFYqBhKgdPzp','spotify:track:1q4XkQXsmgDgK2S1Umqf7D','spotify:track:2374M0fQpWi3dLnB54qaLX','spotify:track:2Foc5Q5nqNiosCNqttzHof','spotify:track:2SiXAy7TuUkycRVbbWDEpo','spotify:track:2lrHKMXyu8LTLxMorzJkTQ','spotify:track:3DHWxeWr4uh19MklWjLpR0','spotify:track:3ZKQVyxT4Jg2lLZRLs7Vgo','spotify:track:4DMKwE2E2iYDKY01C335Uw','spotify:track:4aWn4NHlELpOehxsBaQeoe','spotify:track:5V1AHQugSTASVez5ffJtFo','spotify:track:5c0aiERRxHjbvu5tQ9jwAE','spotify:track:5sMIFZaagXcwKiSfl95zIW','spotify:track:6ztstiyZL6FXzh4aG46ZPD','spotify:track:7zVCrzzEJU7u24sbJPXA5W') AND track_uri2 = 'spotify:track:4aVuWgvD0X63hcOCnZtNFA' GROUP BY track_uri1 ORDER BY track_uri1;

SELECT track_uri1, COUNT(*) FROM seq2_simple WHERE track_uri1 = 'spotify:track:5o4yGlG0PfeVUa6ClIyOxq' AND track_uri2 = 'spotify:track:11dxtPJKR4E0wlSr0A0t47';

select * from tracks where track_uri = 'spotify:track:2mfUa8bLs2s5N4VaqJZ4lZ'
select * from tracks where track_uri = 'spotify:track:57JRZbE80MLsYbmb24cPee'

SELECT count(DISTINCT track_uri) FROM playlist_tracks WHERE pid in ('525966','261994','735199','939549','108724','251912','852548','324328','913938','87573','850610','306768','838831','497929','80262','732551','594659','863062');


select count(track_uri) from tracks where artist_uri in (select distinct artist_uri from artist_genres) -- count songs with artists that contain genres

create table similarities(
    artist_uri TEXT,
    artist_uri2 TEXT,
    similarity REAL
);
.tables
select count(*) from similarities

select * from similarities order by similarity desc limit 100

-- select count(*) from seq2_simple where track_uri1 = 'spotify:track:0KKkJNfGyhkQ5aFogxQAPU' AND track_uri2 = 'spotify:track:5meZvaHT6pQx4AZP1f8lN3'


select acousticness from track_features as tf where acousticness != 0.0 limit 30;
select instrumentalness from track_features as tf where instrumentalness != 0.0 limit 30;

select avg(acousticness) from track_features where acousticness != 0.0;