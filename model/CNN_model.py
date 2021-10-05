from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, LayerNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import tensorflow as tf



image_gen = ImageDataGenerator(
    rescale=1 / 255,
    rotation_range=0.2,
    #featurewise_center=True,
    #featurewise_std_normalization=True,
)  # Rescale the image by normalizing it.

image_shape = (40, 120, 1)
model = Sequential()

## FIRST SET OF LAYERS


model.add(Conv2D(filters=16, kernel_size=(3, 3), input_shape=image_shape, activation='relu', ))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(tf.keras.layers.LayerNormalization(axis=1))
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', ))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', ))
model.add(MaxPool2D(pool_size=(2, 2)))


model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(11, activation='softmax'))

model.summary()


from tensorflow.keras.optimizers import Adam

opt = Adam(learning_rate=0.001)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

batch_size = 8

train_image_gen = image_gen.flow_from_directory('./../data/train',
                                                target_size=image_shape[:2],
                                                color_mode='grayscale',
                                                batch_size=batch_size,
                                                class_mode='categorical')

test_image_gen = image_gen.flow_from_directory('./../data/test',
                                               target_size=image_shape[:2],
                                               batch_size=batch_size,
                                               color_mode='grayscale',
                                               class_mode='categorical')

train_image_gen.class_indices

results = model.fit(train_image_gen, epochs=50,
                    steps_per_epoch=12,
                    validation_data=test_image_gen,
                    validation_steps=4)

pd.DataFrame(results.history).plot(figsize=(8, 5))
model.save('50epochs_7classes_normal.h5')


"""
from tensorflow.keras.utils import image_dataset_from_directory
i = image_dataset_from_directory("./../data/train")

[met for met in dir(i) if met[:1] != "_"]
i.as_numpy_iterator()
ii = _
next(ii)
o = _
type(o)
u= o[0][0]
image_gen.fit(o[0])

"""

