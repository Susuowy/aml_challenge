from utils import *
from keras.layers import Flatten, Dense
from tensorflow.keras.applications.vgg16 import VGG16
from keras.models import Model


def get_model():
    vgg16 = VGG16(input_shape=[WIDTH, HEIGHT, 3], weights='imagenet', include_top=False)

    # Freeze all all but 3 last layers
    for layer in vgg16.layers:
        layer.trainable = False

    x = Flatten()(vgg16.output)
    pred = Dense(NUM_CLASSES, activation='softmax')(x)

    model = Model(inputs=vgg16.input, outputs=pred)
    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

    return model


if __name__ == '__main__':
    train_XY, validation_XY, test_X = get_data_from_memory()
    vgg16 = get_model()

    vgg16.fit(
        train_XY,
        batch_size=BATCH_SIZE,
        validation_data=validation_XY,
        epochs=6,
        verbose=True,
        callbacks=get_callbacks()
    )

    make_predictions_from_memory(vgg16, test_X)
