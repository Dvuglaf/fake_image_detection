from tensorflow import keras
import numpy as np
import cv2


def prepare_image(image_path):
    return np.array(cv2.resize(cv2.imread(image_path), (224, 224)))[..., ::-1] / 255.0


def method_face_spoffnet(image_path):
    model_path = "models/spoffnet.h5"
    model = keras.models.load_model(model_path)

    image = prepare_image(image_path).reshape(-1, 224, 224, 3)

    output = model.predict(image, batch_size=1)

    if output[0][0] < 0.5:
        print("Real!", 1 - output[0][0])
        return "Real", 1 - output[0][0]
    else:
        print("Fake!", output[0][0])
        return "Fake", output[0][0]
