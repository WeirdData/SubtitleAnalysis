# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# Downloads ENGLISH subtitles of all episodes
#
# This script is generated for https://my-subs.co for other sites, it will
# not work. This script was tested on 20 April 2020. You should check CSS
# descriptors used during the time of use and change them if needed.
#
# NOTE:
# In case website is updated its design, this script will NOT work

import pathlib
import random
import time

import bs4
import requests
from bs4 import BeautifulSoup

# If you want to use this script to download English subtitle for some other
# serial, change POSTFIX and URL in _get_episode_url function
#
# my-subs.co URL is divided into following parts
# {BASE_URL}/{URL_EXTRA}-{EPISODE)-{SEASON}-{POSTFIX}
# e.g. https://my-subs.co/versions-629-0-1-game-of-thrones-subtitles
BASE_URL = "https://my-subs.co"
# You should visit their website and check following parts of URL

# GOT : 629, BBT: 2093, BB: 2574
URL_EXTRA = "versions-2574"

# POSTFIX = "game-of-thrones-subtitles"
POSTFIX = "breaking-bad-subtitles"

SEASONS = list(range(1, 6))  # Season list for downloading
EPISODES = list(range(1, 18))  # List of episodes to download, usually give
# highest number of episodes from any season. Unknown episodes will be ignored

# This will be used as a prefix for all downloaded files
NAME = "Breaking.Bad"
FOLDER = "data/bb"  # Where you want to put downloaded files

pathlib.Path(FOLDER).mkdir(parents=True, exist_ok=True)

version_style = "background-color: #f5f5f5; margin-bottom: 10px; padding: 3px; padding-left: 0;"


# Use start_analysis function to download specific subtitle

def _get_episode_url(season: int, episode: int):
    """
    Returns URL of given downloading page
    If using this script for different serial, adjust the return URL below
    :param season: Season number
    :param episode: Episode Number
    :return:
    """
    return f"{BASE_URL}/{URL_EXTRA}-{episode}-{season}-{POSTFIX}"


def _download_srt(row: bs4.element.Tag, season: int, episode: int):
    for link in row.find_all("a", attrs={"rel": "nofollow"}):
        url = f"{BASE_URL}/{link['href']}"
        con = requests.get(url)
        s = f"0{season}" if season < 10 else str(season)
        e = f"0{episode}" if episode < 10 else str(episode)
        with open(f"{FOLDER}/{NAME}.S{s}E{e}.srt", "wb") as f:
            f.write(con.content)
        return True


def _analyse_version(version: bs4.element.Tag, season: int, episode: int):
    # Only analyse English rows
    for row in version.find_all("div", attrs={"class": "row"}):
        if row.find_all("span", attrs={"class": "flag-icon flag-icon-gb"}):
            # Only analyse subtitles which are complete
            if row.find_all(text="Completed"):
                if _download_srt(row, season, episode):
                    return True


def start_analysis(season: int, episode: int):
    print(f"Checking for season {season}, episode {episode}...")
    url = _get_episode_url(season, episode)
    page = requests.get(url)
    if page.status_code == 404:
        print("No such episode found, skipping")
        return
    soup = BeautifulSoup(page.content, 'html.parser')
    all_versions = soup.find_all("div",
                                 attrs={"style": version_style})

    for version in all_versions:
        eng = version.find_all("span", attrs={
            "class": "flag-icon flag-icon-gb",
            "title": "english"
        })
        # Only get subtitle versions which have english translation
        if len(eng) > 0:
            if _analyse_version(version, season, episode):
                print("Downloading Completed.")
                return


if __name__ == "__main__":
    # Download all seasons with episodes
    for sn in SEASONS:
        for ep in EPISODES:
            start_analysis(sn, ep)
            num = random.randint(5, 10)
            print(f"Delaying next download for {num} seconds")
            time.sleep(num)
