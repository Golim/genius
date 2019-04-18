#!/usr/bin/env python3

import os
import dbus
import requests
from bs4 import BeautifulSoup

def get_current_song_info():
    # kudos to jooon from this stackoverflow question http://stackoverflow.com/a/33923095
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        'org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2')
    spotify_properties = dbus.Interface(spotify_bus,
                                        'org.freedesktop.DBus.Properties')
    metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    artist = str(metadata['xesam:artist'][0])
    title = str(metadata['xesam:title'])

    return (artist + " " + title)

def clean_song_name(song):
    # Genius search function does not love this words:
    song = song.replace("Version", "")
    song = song.replace("version", "")
    song = song.replace("Remastered", "")
    song = song.replace("remastered", "")
    song = song.replace("Studio", "")
    song = song.replace("studio", "")
    song = song.replace("Original", "")
    song = song.replace("original", "")
    song = song.replace("-", "")
    song = song.replace("(", "")
    song = song.replace(")", "")
    song = song.replace("[", "")
    song = song.replace("]", "")
    song = song.replace("  ", " ")

    return song

def search_song(query):
    url = 'https://api.genius.com'
    path = '/search'
    params = {'q': query}
    token = os.environ["GENIUS_TOKEN"]
    authorization = "Bearer {}".format(token)
    headers = {'Authorization': authorization}
    r = requests.get(
        url + path,
        params=params,
        headers=headers
    )
    return(r)


def get_lyric(url):
    token = os.environ["GENIUS_TOKEN"]
    authorization = "Bearer {}".format(token)
    headers = {'Authorization': authorization}
    r = requests.get(
        url,
        headers=headers
    )

    html = BeautifulSoup(r.text, "html.parser")
    lyric = html.find("div", class_="lyrics").get_text()

    return(lyric)


def main():
    song = get_current_song_info()

    song = clean_song_name(song)

    response = search_song(song)

    if response.status_code == 200:
        result = response.json()["response"]["hits"][0]["result"]

        title = result["full_title"]
        url = result["url"]

        lyric = get_lyric(url)

        print("Lyric for: " + title)
        print(lyric)

    else:
        print("Error: " + str(response.status_code))

if __name__ == "__main__":
    main()