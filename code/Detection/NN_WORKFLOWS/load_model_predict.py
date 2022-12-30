from tensorflow import keras

import sys
from NN_UTILS import *

from sklearn.metrics import *


#this modul is given to accept a given model -> need absolut folder path!
#it tests with the model on given test data
#the result history and the new model are placed in the test data folder (since the data there was tested)
#folder needs to be provided before!
#this modul is designed to be used with a bash script


#for loading the model
PATH_TO_MODEL = str(sys.argv[1])





PATH_TO_TEST_MAPS = str(sys.argv[2])
RESOLUTION_X = int(str(sys.argv[3]))


OUTPUT_PATH = str(sys.argv[4])
#outname is for the pkl of the history
OUTPUT_NAME = str(sys.argv[5])


print("read model from: " +  str(PATH_TO_MODEL))


print("Get input from csv path: --------------------------------------------------------------------------------")
print("CSV_PATH to test data: " + str(PATH_TO_TEST_MAPS))

#test/validation dataset
tupel_list = get_vector_maps_labels(PATH_TO_TEST_MAPS)



model = keras.models.load_model(PATH_TO_MODEL)

x_test, y_test = get_NN_train_input(tupel_list, RESOLUTION_X, RESOLUTION_X)

pred = model.predict(x_test)


print(y_test)
print(pred)

list_CM = confusion_matrix(y_test,pred)

acc = accuracy_score(y_test,pred)
prec = precision_score(y_test,pred)
recall = recall_score(y_test,pred)


print(list_CM)
print(acc)
print(prec)
print(recall)
