# Copyright (C) 2020, WeirdData
# Author: Rohit Suratekar
#
# specific subtitle

import pandas as pd
from SecretColors import Palette
import matplotlib.pyplot as plt

p = Palette()

FILE_LOG = "log.csv"


def plot_loss():
    df = pd.read_csv(FILE_LOG, sep=";")
    fig, ax1 = plt.subplots()

    color1 = p.blue(shade=40)
    color2 = p.red(shade=40)

    ax1.plot(df['epoch'].values, df['loss'].values,
             color=color1, lw=3)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylabel('Loss', color=color1)
    plt.xlabel("Epoch")

    ax2 = ax1.twinx()
    ax2.plot(df['epoch'].values, df['accuracy'].values,
             color=color2, lw=3)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylabel('Accuracy', color=color2)

    plt.title("Training Progress")
    plt.savefig("plot.png", dpi=150)
    plt.show()


def run():
    plot_loss()
