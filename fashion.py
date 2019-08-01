import time
import tensorflow as tf
import cv2
import numpy as np
from keras.callbacks import ModelCheckpoint


# read in the data, x is for image inputs, y is for output labels, and we have separated
# them into training and test data
(xTrain, yTrain), (xTest, yTest) = tf.keras.datasets.fashion_mnist.load_data()


# Displays set of images from training data, pausing for 1 second between each
for i in range(0, 10):
     cv2.imshow("Fashion", xTrain[i])
     cv2.waitKey(20)
     # plt.imshow(xTrain[i])
     # plt.show()
     time.sleep(1)

# Normalizes the data so it is floating point between 0 and 1.0
xTrain = xTrain.astype('float32') / 255
xTest = xTest.astype('float32') / 255

# Splits training into training and validation, first 5000 are validation
(xTrain, xValid) = xTrain[5000:], xTrain[:5000]
(yTrain, yValid) = yTrain[5000:], yTrain[:5000]

# Reshape input data from (28, 28) to (28, 28, 1)
w, h = 28, 28
xTrain = xTrain.reshape(xTrain.shape[0], w, h, 1)
xValid = xValid.reshape(xValid.shape[0], w, h, 1)
xTest = xTest.reshape(xTest.shape[0], w, h, 1)

# One-hot encode the labels (so exactly one is expected to be on at the output
yTrain = tf.keras.utils.to_categorical(yTrain, 10)
yValid = tf.keras.utils.to_categorical(yValid, 10)
yTest = tf.keras.utils.to_categorical(yTest, 10)


# Build the model
model = tf.keras.Sequential()

# Must define the input shape in the first layer of the neural network
model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(28,28,1)))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.3))

model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.3))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

# Take a look at the model summary
model.summary()

model.compile(loss='categorical_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])

# Now we train the network, having it store the new network weights after each pass through the training data

# checkpointer = ModelCheckpoint(filepath='model.weights.best.hdf5', verbose = 1, save_best_only=True)
model.fit(xTrain,
         yTrain,
         batch_size=64,
         epochs=10,
         validation_data=(xValid, yValid))
         # callbacks=[checkpointer])


# Load the weights with the best validation accuracy
# model.load_weights('model.weights.best.hdf5')

# Evaluate the model on test set
score = model.evaluate(xTest, yTest, verbose=0)

# Print test accuracy
print('\n', 'Test accuracy:', score[1])