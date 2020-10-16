# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# Game of thrones specific analysis

import os

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import tensorflowjs as tfjs
import json
from SecretColors import Palette
from nltk.tokenize import NLTKWordTokenizer
from tensorflow.keras import layers, Sequential

from common import get_text

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
palette = Palette()

WP_TOK = NLTKWordTokenizer()
BATCH_SIZE = 50
TEMPERATURE = 0.6
SEQ_LENGTH = 6
CHECKPOINT_DIR = './training_checkpoints'
JS_DIR = "./jsmodel"
ID_FILE = "ids.json"


def get_data():
    text = get_text("data/got", 1)
    return text


def get_model(no_of_words, batch_size) -> keras.Model:
    model = Sequential(
        [
            layers.Embedding(no_of_words, 500,
                             batch_input_shape=[batch_size, None]),
            layers.LSTM(50,
                        return_sequences=True,
                        recurrent_initializer="glorot_uniform",
                        stateful=True),
            layers.LSTM(50, return_sequences=True),
            layers.Dense(no_of_words)
        ]
    )
    return model


def loss(labels, logits):
    return keras.losses.sparse_categorical_crossentropy(labels, logits,
                                                        from_logits=True)


def train_model():
    checkpoint_prefix = os.path.join(CHECKPOINT_DIR, "ckpt_{epoch}")
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True)
    vocab_size, dataset = get_dataset()
    model = get_model(vocab_size, BATCH_SIZE)
    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=loss)
    keras.utils.plot_model(model, f"model.png", show_shapes=True)

    model.fit(dataset,
              epochs=15,
              verbose=1,
              callbacks=[checkpoint_callback])


def test_model(input_words):
    input_words = [x.lower() for x in input_words]
    final_string = [x for x in input_words]
    with open(ID_FILE) as f:
        char2idx = json.load(f)
    idx2char = {char2idx[v]: v for v in char2idx}

    input_words = [char2idx[x] for x in input_words]
    input_words = tf.expand_dims(input_words, axis=0)

    model = get_model(len(char2idx), 1)
    model.load_weights(tf.train.latest_checkpoint(CHECKPOINT_DIR))
    model.build(tf.TensorShape([1, None]))

    tfjs.converters.save_keras_model(model, JS_DIR)
    model.reset_states()
    for _ in range(25):
        prediction = model.predict(input_words)
        prediction = tf.squeeze(prediction, 0)
        prediction = prediction / TEMPERATURE
        predicted_id = tf.random.categorical(prediction, num_samples=1)[
            -1, 0].numpy()
        final_string.append(idx2char[predicted_id])
        input_words = tf.expand_dims([predicted_id], 0)

    sentences = []
    current = ""
    for f in final_string:
        current += f" {f}"
        if f in [".", "?", "!"]:
            sentences.append(current)
            current = ""

    return "\n".join(sentences)


def get_dataset():
    def _simple_shift(chunk):
        """
        Creates the input and output
        """
        return chunk[:-1], chunk[1:]

    data = WP_TOK.tokenize(get_data().lower())
    vocab = sorted(set(data))
    char2idx = {x: i for i, x in enumerate(vocab)}
    labeled_txt = np.array([char2idx[x] for x in data])
    data = tf.data.Dataset.from_tensor_slices(labeled_txt)
    sequences = data.batch(SEQ_LENGTH + 1, drop_remainder=True)
    data = sequences.map(_simple_shift)
    data = data.batch(BATCH_SIZE, drop_remainder=True)
    with open(ID_FILE, "w") as f:
        json.dump(char2idx, f, sort_keys=True)
    return len(vocab), data


def run():
    train_model()
    # prediction = test_model(["Kings", "Landing"])
    # print(prediction)
    # test = "I am Here.\n who's there? ahh!"
    # print(WP_TOK.tokenize(test))
