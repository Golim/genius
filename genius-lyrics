#!/usr/bin/env python3

import os
import dbus
import argparse
import requests
import importlib
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

DEBUG = False

def debug(s):
    if DEBUG:
        print(f'DEBUG: {s}')

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
    return song.split("-")[0]


def string_similarity(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()

    count = 0

    for word in s1.split():
        if word in s2.split():
            count += 1
    
    return count / len(s1.split())

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

    try:
        return html.find("div", class_="lyrics").get_text()
    except:
        # This could lead to an infinite loop, but who knows
        return get_lyric(url)

def main(song):
    song = clean_song_name(song)

    response = search_song(song)

    if response.status_code == 200:
        if len(response.json()["response"]["hits"]) == 0:
            print("Not found")
            return

        result = response.json()["response"]["hits"][0]["result"]

        title = result["full_title"]
        
        if string_similarity(song, title) < 0.5:
            print("The result could be wrong")
            print("Song found: ", title)
            i = input("Do you want to continue? [y/N] ")
            if not i.lower() in ("yes", "y"):
                print("You can search directly for the song by using --song \"song name\"")
                return

            print("\n\n")
        
        url = result["url"]

        lyric = get_lyric(url)

        print(f'Lyric for: {title}')
        print(lyric)

    else:
        print("Error: " + str(response.status_code))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='GENIUS', description="Find the lyrics of the song you are listening to directly from your Linux terminal")

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    
    parser.add_argument('-s', '--song', help='search for a specific song', action='store', type=str)
    
    parser.add_argument('--debug', help='print debug information', action='store_true')

    argcomplete = importlib.util.find_spec("argcomplete")
    if argcomplete is not None:
        import argcomplete
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    if args.song is not None:
        song = args.song
    else:
        song = get_current_song_info()
    
    if args.debug:
        DEBUG = True

    debug(f'Song: {song}')

    if "GENIUS_TOKEN" in os.environ:
        main(song)
    else:
        print("You have to set the environment variable GENIUS_TOKEN with your token, get yours here: https://genius.com/api-clients")
