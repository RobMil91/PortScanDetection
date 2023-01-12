
from simple_CNN import *
from NN_UTILS import *
import sys

# this modul is needed to train on given folder with csvs contained as vectors 
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


print("epochs are: " + str(epochs))
print("batch_size is: " + str(batch_size))
print("validation_splitis: " + str(validation_split))
print("Get input from csv path: --------------------------------------------------------------------------------")
print("CSV_PATH: " + str(PATH_TO_MAPS))

# print(map_represenation.shape)
print("Get model: --------------------------------------------------------------------------------")

model = getModel(RESOLUTION_X)

print("Get info on input data: --------------------------------------------------------------------------------")

#extract the maps and labels from folder
tupel_list = get_vector_maps_labels(PATH_TO_MAPS)

#z scoring happens HERE!
(x_train, y_train) = get_NN_train_input(tupel_list, RESOLUTION_X, RESOLUTION_X)


print(x_train.shape)
print(y_train.shape)
print(x_train[0].shape)


X,Y = shuffle(x_train, y_train)



history = model.fit(x=X, y=Y,
          batch_size=batch_size, 
          epochs=epochs,verbose=1,
          validation_split=validation_split,
          )

#save the history of the current classification
print("---LOG: saving the history to PATH: " + str(OUTPUT_PATH))
save_compl_history(history, OUTPUT_PATH, OUTPUT_NAME)


outpath_model = OUTPUT_PATH + OUTPUT_NAME + "_model"

print("---LOG: saving the history to Model: " + str(outpath_model))
model.save(outpath_model)


with open(OUTPUT_PATH + OUTPUT_NAME + '_metadata.txt', 'a') as f1:
    f1.write("x_train.shape: " + str(x_train.shape) + os.linesep)
    f1.write("y_train.shape: " + str(y_train.shape) + os.linesep)

#debug statement for checking the different layers
print(model.summary())