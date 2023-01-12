from tensorflow import keras

from keras.utils import plot_model
import sys
from NN_UTILS import *

import timeit

#needs to be configured from comments below!

#this modul is given to accept a given model -> need absolut folder path!
#it tests with the model on given test data
#the result history and the new model are placed in the test data folder (since the data there was tested)
#folder needs to be provided before!
#this modul is designed to be used with a bash script


#for loading the model
PATH_TO_MODEL = str(sys.argv[1])





PATH_TO_TEST_MAPS = str(sys.argv[2])
RESOLUTION_X = int(str(sys.argv[3]))
epochs = int(str(sys.argv[4]))
batch_size = int(str(sys.argv[5]))
validation_split = float(str(sys.argv[6]))


OUTPUT_PATH = str(sys.argv[7])
#outname is for the pkl of the history
OUTPUT_NAME = str(sys.argv[8])

NEW_MODEL_NAME = ""

print("read model from: " +  str(PATH_TO_MODEL))

print("epochs are: " + str(epochs))

print("batch_size is: " + str(batch_size))


print("validation_splitis: " + str(validation_split))


print("Get input from csv path: --------------------------------------------------------------------------------")
print("CSV_PATH to test data: " + str(PATH_TO_TEST_MAPS))

#test/validation dataset
tupel_list = get_vector_maps_labels(PATH_TO_TEST_MAPS)


#this function only accepts absolut paths / returns model
model = keras.models.load_model(PATH_TO_MODEL)

#write path for the model picture
# outpath = PATH_TO_MODEL + '/model.jpg'

# #optional model print
# plot_model(model, to_file=outpath, rankdir="LR", show_layer_names=False, show_layer_activations=True, show_dtype=False,dpi=400)



print("Normalizsing data: --------------------------------------------------------------------------------")
#z scoring happens HERE!
#y_train are the labels! however if validation split is 1.0 it is all validation data
(x_test, y_test) = get_NN_train_input(tupel_list, RESOLUTION_X, RESOLUTION_X)



# history = model.fit(x=x_test, y=y_test,
#           batch_size=batch_size, 
#           epochs=epochs,verbose=1,
#           validation_split=validation_split,
#           shuffle=True
#           )


# history = model.fit(
# x_train,
# y_train,
# batch_size=64,
# epochs=2,
# # We pass some validation for
# # monitoring validation loss and metrics
# # at the end of each epoch
# validation_data=(x_val, y_val),
# )



# runtime_of_predication = timeit.timeit(model.predict)
# runtime_of_predication = timeit.timeit(model.predict(x_test, verbose=1))

# print(runtime_of_predication)

# print("--------------------------------------------------load model----------------------")

# time0 = timeit.timeit('keras.models.load_model(PATH_TO_MODEL)','from __main__ import keras, PATH_TO_MODEL', number = 1)

# print("loaded model model: " + str(time0))


# print("--------------------------------------------------measure Start----------------------")


# time1 = timeit.timeit('get_NN_train_input(tupel_list, RESOLUTION_X, RESOLUTION_X)', 'from __main__ import get_NN_train_input, tupel_list, RESOLUTION_X', number=1)

# print("read aggr map an normalizsed: " + str(time1))

# time2 = timeit.timeit('model.predict(x_test)', 'from __main__ import model, x_test', number=1)


# print("predicted with model: " + str(time2))


# print("entire time taken, to read map(s) and predict: " + str(time1 + time2))


# print("--------------------------------------------------measure End----------------------")



# mysetup = 'from __main__ import model, x_test, get_NN_train_input, tupel_list, RESOLUTION_X, keras, PATH_TO_MODEL'

# # code snippet whose execution time is to be measured
# mycode = '''



model = keras.models.load_model(PATH_TO_MODEL)

x_test = get_NN_train_input(tupel_list, RESOLUTION_X, RESOLUTION_X)

pred = model.predict(x_test)


# '''
 
# # timeit statement
# print (timeit.timeit(setup = mysetup,
#                      stmt = mycode, 
#                      number = 10000))



# prediction = model.predict(x_test, verbose=1) 


# # #these are the 2 arrays that predicted and returned
# print(prediction.flatten()) 
# print(y_test)



# print('Test loss:', score[0]) 
# print('Test accuracy:', score[1])



# save_compl_history(history, OUTPUT_PATH, OUTPUT_NAME)


#needed to save complete model
# outpath_model = OUTPUT_PATH + "folder_of_model"
# print(outpath_model)
# model.save(outpath_model)










# PATH_TO_TEST_DATA = str(sys.argv[2])


# model.predict()








# outpath = OUTPUT_PATH + OUTPUT_NAME

# print("wrote_new_model_TO: " + str(outpath))


