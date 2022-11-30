import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

secrets = open("secrets.txt")
CLIENT_ID: str = secrets.readline()[:-1]
CLIENT_SECRET: str = secrets.readline()
secrets.close()

# ALBUM_URI: str = "1nqz3cEjuvCMo8RHLBI9kM"
# async def main(ident: str, secret: str, album_uri: str) -> None:
#     async with spotify.Client(ident, secret) as client:
#         album = await client.get_album(album_uri)

#         async for track in album:
#             print(repr(track))

# asyncio.run(main(CLIENT_ID, CLIENT_SECRET, ALBUM_URI))

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
def list_tracks(query):
    artist = spotify.search(query, 1, 0, "artist")["artists"]["items"][0]
    artist_id = artist["uri"]
    artist_genres = artist["genres"]
    artist_name = artist["name"]
    print(artist_id, artist_name, artist_genres)

    results = spotify.artist_albums(artist_id, album_type="album")
    albums = results['items']
    # while results['next']:
    #     results = spotify.next(results)
    #     albums.extend(results['items'])

    for album in albums:
        string = album["id"] + "->" + album["name"] + ": "
        a = spotify.album(album["uri"])
        for song in a["tracks"]["items"]:
            string += song["name"] + " | "
        print(string)

list_tracks("TWICE")
list_tracks("Sabaton")