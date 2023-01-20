import pandas as pd
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation, Conv2D, Flatten, MaxPooling2D, Dropout
from tensorflow.keras import backend as K
from sklearn.utils import shuffle
from tensorflow.keras.callbacks import TensorBoard

import tensorflow as tf


def getModel(resolution):

    input_shape = (resolution, resolution, 1)
    model = keras.Sequential()
    model.add(Conv2D(32, (2, 2), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (2, 2)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (2, 2)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        metrics=['accuracy',
                 tf.keras.metrics.Precision(name="precision"),
                 tf.keras.metrics.Recall(name="recall"),
                 tf.keras.metrics.FalsePositives(name="FP"),
                 tf.keras.metrics.FalseNegatives(name="FN"),
                 tf.keras.metrics.TruePositives(name="TP"),
                 tf.keras.metrics.TrueNegatives(name="TN"),
                 ]
    )
    return model
