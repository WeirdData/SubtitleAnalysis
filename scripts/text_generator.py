# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# specific subtitle

import json
import os
from string import digits, ascii_lowercase
import numpy as np
from nltk.tokenize import TweetTokenizer
from tensorflow import keras
import tensorflow as tf

from scripts.common import get_text_from_folder

ALLOWED_CHARS = f"{digits}{ascii_lowercase}?!,."

FILE_ID = "ids.json"
FILE_LOG = "log.csv"
FILE_MODEL = "model.h5"
FILE_TXT = "../input/subtitles/subtext_got.txt"
SEQ_LENGTH = 15
TEMPERATURE = 0.6
BATCH_SIZE = 100
EMBEDDING = 128
EPOCHS = 1
UNITS = 128


def get_data():
    return get_text_from_folder("data/bbt")
    # with open(FILE_TXT) as f:
    #     return f.readlines()[0]


def filter_char(word: str):
    w = list(str(word))
    w = [x for x in w if x in ALLOWED_CHARS]
    if len(set(w)) == 1:
        if list(set(w))[0] == ".":
            return "."
    w = "".join(w)
    if w.startswith("www"):
        return ""
    if "x" in w:
        tmp = w.split("x")
        try:
            float(tmp[0])
            return ""
        except ValueError:
            pass
    try:
        float(w)
        return ""
    except ValueError:
        pass
    if len(w) == 6:
        try:
            bytes.fromhex(w)
            return ""
        except ValueError:
            pass
    return w


def prepare_data():
    tk = TweetTokenizer()
    data = get_data()
    data = data.lower()
    data = tk.tokenize(data)
    data = [filter_char(x) for x in data if len(filter_char(x)) > 0]
    vocab = sorted(list(set(data)))
    # Start IDs from 1 so that we can use 0 for dropout
    char2id = {x: i + 1 for i, x in enumerate(vocab)}
    del vocab
    with open(FILE_ID, "w") as f:
        json.dump(char2id, f, sort_keys=True)
    data = [char2id[x] for x in data]
    return data, len(char2id) + 1


def predict_text(words, no_of_words):
    words = [x.lower() for x in words]
    with open(FILE_ID) as f:
        ids = json.load(f)
    words = [ids[x] for x in words]
    id2text = {v: k for k, v in ids.items()}
    model = get_model(len(ids) + 1, 1)
    old_model = keras.models.load_model(FILE_MODEL)
    model.set_weights(old_model.get_weights())
    current_words = words
    working_words = [x for x in current_words]
    while len(working_words) < SEQ_LENGTH:
        working_words.insert(0, 0)
    for _ in range(no_of_words):
        while len(working_words) > SEQ_LENGTH:
            working_words.pop(0)
        predictions = model.predict(np.asarray([working_words]))[0]
        predictions = np.log(predictions) / TEMPERATURE
        prediction_id = tf.random.categorical(predictions, num_samples=1)[
            -1, 0].numpy()
        current_words.append(prediction_id)
        working_words.append(prediction_id)

    final_words = [id2text[x] for x in current_words if x != 0]
    print(" ".join(final_words))


def get_model(vocab, batch):
    model = keras.Sequential()
    model.add(
        keras.layers.Embedding(vocab + 1, EMBEDDING, batch_size=batch)
    )
    model.add(keras.layers.GRU(UNITS, return_sequences=True, stateful=True,
                               recurrent_initializer='glorot_uniform'))
    model.add(keras.layers.GaussianDropout(0.3))
    model.add(keras.layers.GRU(UNITS, stateful=True, return_sequences=True,
                               recurrent_initializer='glorot_uniform'))
    model.add(keras.layers.Dense(EMBEDDING,
                                 activation=keras.activations.relu))
    model.add(keras.layers.Dense(vocab + 1,
                                 activation=keras.activations.softmax))
    keras.utils.plot_model(model, "model.png", show_shapes=True)
    return model


def train_model():
    def dense_1_step(batch):
        # Shift features and labels one step relative to each other.
        return batch[:-1], batch[1:]

    data, vocab = prepare_data()
    dataset = tf.data.Dataset.from_tensor_slices(data)
    dataset = dataset.batch(SEQ_LENGTH + 1, drop_remainder=True).map(
        dense_1_step)
    dataset = dataset.shuffle(10000).batch(BATCH_SIZE, drop_remainder=True)

    model = get_model(vocab, BATCH_SIZE)
    try:
        os.remove(FILE_LOG)
    except FileNotFoundError:
        pass
    csv_logger = keras.callbacks.CSVLogger(FILE_LOG,
                                           append=True,
                                           separator=';')
    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.sparse_categorical_crossentropy)

    model.fit(dataset, epochs=EPOCHS, shuffle=False, callbacks=[csv_logger])
    model.save(FILE_MODEL)


def run():
    train_model()
    # predict_text(["how", "about"], 20)
