


import pandas as pandas
from Utils_Workflow import *
from NN import *
from simple_CNN import *
#this file is to calculatethe input for the CNN

from NN_UTILS import *

from keras.utils import plot_model

import sys

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


print("epochs are: " + str(epochs))

print("batch_size is: " + str(batch_size))


print("validation_splitis: " + str(validation_split))


print("Get input from csv path: --------------------------------------------------------------------------------")
print("CSV_PATH: " + str(PATH_TO_MAPS))




tupel_list = get_vector_maps_labels(PATH_TO_MAPS)

print("Get model: --------------------------------------------------------------------------------")

model = getModel(RESOLUTION_X)

# outpath = OUTPUT_PATH + '/model.jpg'

# plot_model(model, to_file=outpath, rankdir="TB", show_dtype=False, show_layer_names=False, show_layer_activations=False,dpi=400)

print("Get info on input data: --------------------------------------------------------------------------------")


#z scoring happens HERE!
(x_train, y_train) = get_NN_train_input(tupel_list, RESOLUTION_X, RESOLUTION_X)


print(x_train.shape)

print(y_train.shape)



history = model.fit(x=x_train, y=y_train,
          batch_size=batch_size, 
          epochs=epochs,verbose=1,
          validation_split=validation_split,
          shuffle=True
          )



#save the history of the current run
save_compl_history(history, OUTPUT_PATH, OUTPUT_NAME)

outpath_model = OUTPUT_PATH + OUTPUT_NAME
print(outpath_model)
model.save(outpath_model)


with open(OUTPUT_PATH + OUTPUT_NAME + '_metadata_input.txt', 'a') as f1:

    f1.write("x_train.shape: " + str(x_train.shape) + os.linesep)
    f1.write("y_train.shape: " + str(y_train.shape) + os.linesep)



#debug statement for checking the different layers
# print(model.summary())