# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# specific subtitle

import json
import os

import numpy as np
from nltk.tokenize import word_tokenize
from tensorflow import keras
from scripts.common import get_text

REMOVE_WORDS = ["/font", "00FF00", "00FFFF", "00ff00", "00ffff", "01x09",
                '1x02', '1x04', '1x05', '1x06', '1x07', '1x08', '1x10',
                "29â\x80\x94", "#", "38b0de"]

FILE_ID = "ids.json"
FILE_LOG = "log.csv"
FILE_MODEL = "model.h5"
FILE_TXT = "../input/subtitles/subtext_got.txt"
SEQ_LENGTH = 7
TEMPERATURE = 0.5
BATCH_SIZE = 100


def get_data():
    return get_text("data/bbt", 1)
    # with open(FILE_TXT) as f:
    #     return f.readlines()[0]


def prepare_data():
    data = get_data()
    data = data.lower()
    data = word_tokenize(data)
    data = [x for x in data if x not in REMOVE_WORDS]
    vocab = sorted(list(set(data)))
    # Start IDs from 1 so that we can use 0 for dropout
    char2id = {x: i + 1 for i, x in enumerate(vocab)}
    del vocab
    with open(FILE_ID, "w") as f:
        json.dump(char2id, f, sort_keys=True)
    data = [char2id[x] for x in data]
    seq_data = []
    for i in range(0, len(data) - SEQ_LENGTH):
        seq_data.append(data[i:i + SEQ_LENGTH + 1])

    seq_data = np.asarray(seq_data)
    return seq_data, len(char2id) + 1


def get_model(vocab_size, seq_length):
    model = keras.Sequential([
        keras.layers.Embedding(input_dim=vocab_size,
                               output_dim=100,
                               input_length=seq_length),
        keras.layers.LSTM(64, return_sequences=True),
        keras.layers.Dropout(0.2),
        keras.layers.LSTM(64),
        keras.layers.Dense(128, activation=keras.activations.relu),
        keras.layers.Dense(vocab_size, activation=keras.activations.softmax)
    ])
    keras.utils.plot_model(model, "model.png", show_shapes=True)
    return model


def train_model():
    training, vocab_size = prepare_data()
    model = get_model(vocab_size, SEQ_LENGTH)
    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.CategoricalCrossentropy(),
                  metrics=keras.metrics.Accuracy())
    try:
        os.remove(FILE_LOG)
    except FileNotFoundError:
        pass
    csv_logger = keras.callbacks.CSVLogger(FILE_LOG,
                                           append=True,
                                           separator=';')
    model.fit(training[:, :-1],
              keras.utils.to_categorical(training[:, -1],
                                         num_classes=vocab_size),
              epochs=10,
              shuffle=True,
              batch_size=BATCH_SIZE,
              callbacks=[csv_logger])

    model.save(FILE_MODEL)


def predict_text(words, no_of_words):
    words = [x.lower() for x in words]
    with open(FILE_ID) as f:
        ids = json.load(f)
    words = [ids[x] for x in words]
    id2text = {v: k for k, v in ids.items()}
    model = keras.models.load_model(FILE_MODEL)  # type: keras.Model
    current_words = words
    for _ in range(no_of_words):
        predictions = model.predict(np.asarray([current_words]))[0]
        predictions = np.asarray(predictions).astype('float64')
        predictions = np.log(predictions) / TEMPERATURE
        exp_pred = np.exp(predictions)
        preds = exp_pred / np.sum(exp_pred)
        probas = np.random.multinomial(1, preds, 1)
        prediction_id = np.argmax(probas)
        current_words.append(prediction_id)

    final_words = [id2text[x] for x in current_words]
    print(" ".join(final_words))


def run():
    # train_model()
    predict_text(["physics"], 20)
