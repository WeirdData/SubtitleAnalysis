# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# Main file to handle all the functions
# Put all the subtitle files in 'data' folder. You can use download.py to
# download subtitles if you want.

import os
from typing import List
import re

import nltk


class Units(int):
    @property
    def seconds(self) -> float:
        return self.__int__() / 1000

    @property
    def minutes(self) -> float:
        return self.seconds / 60

    @property
    def hours(self) -> float:
        return self.minutes / 60


class Line:
    def __init__(self, data):
        try:
            int(data[-1])
            data = data[:-1]
        except ValueError:
            pass
        self._raw = data
        self.timestamp = data[0]
        self.line = self._sanitize(" ".join(data[1:]))

    @staticmethod
    def _sanitize(text: str):
        """
        Some of the text in these particular subtitle files include italics
        words which are included in the <i></i> html tags. These were
        creating problems in tagging. Hence we will just remove them here.
        :param text:
        :return:
        """
        return text.replace("<i>", "").replace("</i>", "").replace("-", " ")

    @staticmethod
    def _time_convert(time: str):
        other, mil = time.split(",")
        hour, minute, seconds = other.split(":")

        total = int(mil)
        total += int(seconds) * 1000
        total += int(minute) * 1000 * 60
        total += int(hour) * 1000 * 60 * 60

        return total

    @property
    def start_time(self) -> Units:
        return Units(self._time_convert(self.timestamp.split("-->")[0]))

    @property
    def end_time(self) -> Units:
        return Units(self._time_convert(self.timestamp.split("-->")[1]))


class Subtitle:
    """
    Simple class to hold the subtitle data
    """

    def __init__(self, lines):
        self.lines = lines

    @property
    def text(self) -> str:
        """Returns all the subtitle lines joined by space
        """
        return " ".join([x.line for x in self.lines])

    @staticmethod
    def _convert_units(ms: Units, unit: str):
        if unit == "ms":
            return ms.__int__()
        elif unit == "s":
            return ms.seconds
        elif unit == "min":
            return ms.minutes
        elif unit == "h":
            return ms.hours
        else:
            raise ValueError(f"Unknown unit '{unit}'. Currently only "
                             f"following units are supported: ms, s, min, h")

    def start_times(self, unit: str = "ms") -> list:
        """
        Start time of all of the subtitles (in milliseconds)
        :param unit: In which unit you want (ms, s, min, h)
        :return: List of times
        """
        return [self._convert_units(x.start_time, unit) for x in self.lines]

    def end_times(self, unit: str = "ms") -> list:
        """
        End time of all of the subtitles (in milliseconds)
        :param unit: In which unit you want (ms, s, min, h)
        :return: List of times
        """
        return [self._convert_units(x.end_time, unit) for x in self.lines]


FILE = "data/Game.Of.Thrones.S01E01.srt"


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
            full_line = " ".join(temp)
            # Remove the advertise lines
            if "www.my-subs.com" not in full_line.lower():
                all_lines.append(Line(temp))

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


def get_all_files():
    names = []
    for file in os.listdir("data"):
        names.append(f"data/{file}")
    return names


def get_text(season: int = None) -> str:
    file_list = []
    for file in get_all_files():
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


def get_common_words(season: int = None) -> List[str]:
    return nltk.tokenize.word_tokenize(get_text(season))


def frequent_sentence(season: int = None):
    txt = get_text(season)
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


def get_stats(words: list):
    # Get tags
    tagged = nltk.pos_tag(words)
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WP', 'WRB']
    adj_tags = ['JJ', 'JJR', 'JJS']
    avb_tags = ['RB', 'RBR', 'RBR']
    nouns = frequent_words(tagged, avb_tags, True)
    print(nouns.most_common(10))


g = get_common_words()
get_stats(g)
