# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# Main file to handle all the functions
# Put all the subtitle files in 'data' folder. You can use download.py to
# download subtitles if you want.

import nltk

from common import frequent_words

# Change following according to your data folder.
# Do not put subtitles in sub-folders. Pull all of them together and keep in
# single folder
DATA_FOLDER = "data/got"


def get_stats(words: list):
    # Get tags
    tagged = nltk.pos_tag(words)
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WP', 'WRB']
    adj_tags = ['JJ', 'JJR', 'JJS']
    avb_tags = ['RB', 'RBR', 'RBR']
    nouns = frequent_words(tagged, noun_tags)
    print(nouns.most_common(10))
