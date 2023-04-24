# Case-based Recommendation for Music Playlists
## *Alexander Stradnic - 119377263*

## Running the code
A sample of the first 100 playlists is available to query from `spotify_sample.db`.
The full dataset is downloadable at this Google Drive [link](https://drive.google.com/file/d/1eM-8cyl2LFau2Tolkj2VqEh9S0pxkRXm/view?usp=share_link). If this file is used, rename `db_path` in to `spotify.db`.

`case.py` and `sim.py` are available to execute on this dataset. Simply run the desired file.

1. Search a song by its title.
2. Select the desired song by entering its index from the returned list. If you want to query again, enter '-1'.
3. A list of track URIs will then be generated and returned in the console.
4. Copy this list into the [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference/reorder-or-replace-playlists-tracks), in the *uris* field.
5. Create a new playlist on your Spotify Account.
6. Copy the playlist ID from the address bar (https://open.spotify.com/playlist/ `<your_playlist_id>`) and paste it into the *playlist_uri* field on the Web API page.
7. By pressing *Try it* on the Web API page, your playlist should be populated with the generated songs.

In order to change properties or playlist length, change the appropriate value in the file before running the file.
- `var_weight, beta, stdN` are global variables at the top of `case.py`, with `k, N` being function parameters
- `sim.py` only has `N` as a function parameter
- `track_uri` string can be entered directly into both functions as a parameter instead of searching by track name

Full codebase including webapp available at http://github.com/nimitzpro/matsubara
