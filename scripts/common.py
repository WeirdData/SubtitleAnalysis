# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# All Common functions


import os
import re
from typing import List

import nltk

from scripts.models import Subtitle, Line


def parse_subtitle(filename: str) -> Subtitle:
    """
    Parses the downloaded subtitle file to Subtitle Object.
    Subtitle file should have following format
    Line 1: Timestamp (e.g. 00:01:54,955 --> 00:01:57,957 )
    Line 2: Text or Line
    Line 3 (if any): Next line or text
    :param filename: Name of the subtitle file
    :return: Subtitle Object
    """
    # ISO-8859-1 encoding is needed for these srt files
    with open(filename, encoding="ISO-8859-1") as f:
        all_lines = []
        temp = []

        def _add(line_list):
            full_line = " ".join(line_list)
            # Remove the advertise lines
            if "www.my-subs.com" not in full_line.lower():
                if "www.ydy.com" not in full_line.lower():
                    all_lines.append(Line(line_list))

        for line in f:
            if "-->" in line:
                if len(temp) > 1:
                    _add(temp)
                temp = [line.strip()]
            else:
                if len(line.strip()) > 0:
                    temp.append(line.strip())
        # For last line
        _add(temp)

    return Subtitle(all_lines)


def get_all_files(folder):
    names = []
    for file in os.listdir(folder):
        names.append(f"{folder}/{file}")
    return names


def get_text(folder: str, season: int = None) -> str:
    file_list = []
    for file in get_all_files(folder):
        if season is not None:
            if f"S{season:02d}" in file:
                file_list.append(file)
        else:
            file_list.append(file)

    all_subtitles = []
    for file in file_list:
        all_subtitles.append(parse_subtitle(file))

    all_text = [x.text for x in all_subtitles]
    return " ".join(all_text)


def get_common_words(folder: str, season: int = None) -> List[str]:
    return nltk.tokenize.word_tokenize(get_text(folder, season))


def frequent_sentence(folder: str, season: int = None):
    txt = get_text(folder, season)
    tok = nltk.tokenize.sent_tokenize(txt)
    # Remove punctuations
    tok = [re.sub('[^A-Za-z0-9]+', ' ', x).strip() for x in tok]
    fq = nltk.FreqDist(tok)
    print(fq.most_common(10))


def frequent_words(tagged: list, allowed: list, use_stem: bool = False) -> \
        nltk.FreqDist:
    n = [x[0] for x in tagged if x[1] in allowed and str(x[0]).isalnum()]
    # Get the stem word
    if use_stem:
        ps = nltk.stem.PorterStemmer()
        n = [ps.stem(x).lower() for x in n]
    # Now check distribution
    fq = nltk.FreqDist(n)
    return fq
