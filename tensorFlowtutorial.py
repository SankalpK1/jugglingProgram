from numpy import loadtxt
from keras.models import load_model
import numpy as np
# load model
model = load_model('1b_pattern_model.h5')
# summarize model.
model.summary()
# load dataset
dataset = loadtxt("1_1.csv", delimiter=",")
print(dataset.shape)

# split into input (X) and output (Y) variables
X = dataset[:, 0:5]
Y = dataset[:, 5]
# evaluate the model
X = np.expand_dims(X, axis=0)


score = model.evaluate(X, Y, verbose=0)
print(score[1])