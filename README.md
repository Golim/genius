# Genius
Find the lyrics of the song you are listening to directly from your linux terminal

## Requirements
- Python 3
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## How to use
    git clone https://github.com/golim/genius
    cd genius
    chmod +x genius.py

Set an environment variable called `GENIUS_TOKEN` with the token you can request [here](https://genius.com/api-clients) and reboot.

    ./genius.py

### Use it globally
    sudo cp genius.py /usr/local/bin/genius

## Screenshot
![Screenshot](img/screenshot.png)

## Warning
Due to the stupid search function of genius it may happen that the script finds the wrong song