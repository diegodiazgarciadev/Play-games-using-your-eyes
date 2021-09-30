from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import tensorflow as tf


image_gen = ImageDataGenerator(rescale=1 / 255, rotation_range=0.2)  # Rescale the image by normalizing it.
image_shape = (40, 120, 1)
model = Sequential()

## FIRST SET OF LAYERS


model.add(Conv2D(filters=16, kernel_size=(3, 3), input_shape=image_shape, activation='relu', ))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=image_shape, activation='relu', ))
model.add(MaxPool2D(pool_size=(2, 2)))


model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(6, activation='softmax'))

model.describe()


from tensorflow.keras.optimizers import Adam

opt = Adam(learning_rate=0.001)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

batch_size = 8

train_image_gen = image_gen.flow_from_directory('../data/train',
                                                target_size=image_shape[:2],
                                                batch_size=batch_size,
                                                class_mode='categorical')

test_image_gen = image_gen.flow_from_directory('../data/test',
                                               target_size=image_shape[:2],
                                               batch_size=batch_size,
                                               class_mode='categorical')

results = model.fit(train_image_gen, epochs=100,
                    #steps_per_epoch=12,
                    validation_data=test_image_gen,
                    validation_steps=4)

pd.DataFrame(results.history).plot(figsize=(8, 5))
model.save('100epochs_6classes.h5')