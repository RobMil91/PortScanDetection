


from matplotlib.colors import from_levels_and_colors
import pandas as pandas
from NN import *
from simple_CNN import *

from NN_UTILS import *

from keras.utils import plot_model

import sys


# this modul is needed to train on given csv folder 
#it returns the model in keras saving format and the history
#they are given on the specified output folder, that needs to be initalizsed

if(str(sys.argv[1]) == "--help"):
    print("argv1 == PATH_AGGREGATION_MAPS")
    print("argv2 == model resolution")



PATH_TO_MAPS = str(sys.argv[1])
RESOLUTION_X = int(str(sys.argv[2]))
epochs = int(str(sys.argv[3]))
batch_size = int(str(sys.argv[4]))
validation_split = float(str(sys.argv[5]))
OUTPUT_PATH = str(sys.argv[6])
OUTPUT_NAME = str(sys.argv[7])
PATH_TO_TEST_MAPS = str(sys.argv[8])

print("epochs are: " + str(epochs))
print("batch_size is: " + str(batch_size))
print("validation_splitis: " + str(validation_split))
print("Get input from csv path: --------------------------------------------------------------------------------")
print("CSV_PATH: " + str(PATH_TO_MAPS))

tupel_list_train = get_vector_maps_labels(PATH_TO_MAPS)
tupel_list_validation = get_vector_maps_labels(PATH_TO_TEST_MAPS)

print("Get model: --------------------------------------------------------------------------------")

model = getModel(RESOLUTION_X)

print("Get info on input data: --------------------------------------------------------------------------------")


#z scoring happens HERE!
(x_train, y_train) = get_NN_train_input(tupel_list_train, RESOLUTION_X, RESOLUTION_X)
(x_val_test, y_val_test)= get_NN_train_input(tupel_list_validation, RESOLUTION_X, RESOLUTION_X)


# print(x_train.shape)

# # print(x_train[0].shape)

# print(y_train.shape)
# # print(y_train[0])


#needed to shuffle learn data and test data
X,Y = shuffle(x_train, y_train)
X_val,Y_val = shuffle(x_val_test, y_val_test)






# y_train = y_train.reshape(len(y_train))

# print(y_train.shape)

# split_test_train((x_train, y_train))



        #   epochs=20,
        #   batch_size=128)

history = model.fit(x=X, y=Y,
          batch_size=batch_size, 
          epochs=epochs,verbose=1,
          validation_data=(X_val, Y_val),
        #   shuffle=True
          )



#save the history of the current run
save_compl_history(history, OUTPUT_PATH, OUTPUT_NAME)

outpath_model = OUTPUT_PATH + OUTPUT_NAME
print(outpath_model)
model.save(outpath_model)



#debug statement for checking the different layers
# print(model.summary())