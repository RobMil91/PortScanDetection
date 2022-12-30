#this file is to take objects in format of Aggregation_map and train and test on them
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import numpy as np

def compile_model_test():
  model = Sequential()
  # the model takes each input shape individually!!!! so theres X amount of theses shapes, but they have to be all 32x32
  model.add(Dense(10, input_shape=(32,32), activation ='relu'))
  model.add(Dense(10, activation ='relu'))
  model.add(Dense(1))
  model.compile(loss='binary_crossentropy',
			optimizer='rmsprop',
			metrics=['accuracy'])
  return model

def compile_model_image_classify():
  #  input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS) : batch size is inferred
  input_shape = (32,32,1)
  model = Sequential()
  # the model takes each input shape individually!!!! so theres X amount of theses shapes, but they have to be all 32x32
  model.add(Conv2D(10, kernel_size=(3, 3), input_shape=input_shape))
  model.add(Dense(1))
  model.compile(loss='binary_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy'])

  return model



def compile_model_image_classify_complex():
  #  input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS) : batch size is inferred
  input_shape = (32,32,1)
  model = Sequential()
  # the model takes each input shape individually!!!! so theres X amount of theses shapes, but they have to be all 32x32
  x = model.add(Conv2D(1024, kernel_size=(3, 3), input_shape=input_shape))
  model.add(Flatten())
  model.add(Activation('relu'))
  model.add(Dropout(0.5))
  model.add(Dense(1))
  model.add(Activation('sigmoid'))
  model.compile(loss='binary_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy'])

  return model


def compile_model_shape_depth_ONE():
  #  input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS) : batch size is inferred
  input_shape = (32,32,1)
  model = Sequential()
  # the model takes each input shape individually!!!! so theres X amount of theses shapes, but they have to be all 32x32
  x = model.add(Conv2D(1024, kernel_size=(3, 3), input_shape=input_shape))
  model.add(Flatten())
  model.add(Activation('relu'))
  model.add(Dropout(0.5))
  model.add(Dense(1))
  model.add(Activation('sigmoid'))
  model.compile(loss='binary_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy'])

  return model


from keras import *
import tensorflow as tf 

# def compile_model_1test():
#   x = Input(shape=(32,32))
#   y = tf.square(x)  # This op will be treated like a layer
#   model = Model(x, y)
#   model.compile(loss='binary_crossentropy',
#   optimizer='rmsprop',
#   metrics=['accuracy'])

#   return model
