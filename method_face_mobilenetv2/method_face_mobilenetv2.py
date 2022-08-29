import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image


def prepare_image(image_path):
    img = image.load_img(image_path, target_size=(300, 300, 3))
    img = image.img_to_array(img)
    return np.expand_dims(img, axis=0) / 255.


def method_face_mobilenetv2(image_path):
    model_path = "models/mobilenetv2.h5"
    model = keras.models.load_model(model_path)

    image = prepare_image(image_path).reshape(-1, 300, 300, 3)

    output = model.predict(image, batch_size=1)

    if output[0][0] > 0.5:
        print("Real!", output[0][0])
        return "Real", output[0][0]
    else:
        print("Fake!", 1 - output[0][0])
        return "Fake", 1 - output[0][0]
