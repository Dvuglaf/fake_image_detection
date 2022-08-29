import numpy as np
from tensorflow import keras
from PIL import Image, ImageChops, ImageEnhance


def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file_name.jpg'

    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality=quality)
    temp_image = Image.open(temp_filename)

    ela_image = ImageChops.difference(image, temp_image)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff

    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image


def prepare_image(image_path):
    image_size = (128, 128)
    return np.array(convert_to_ela_image(image_path, 90).resize(image_size)).flatten() / 255.0


def method_ela_2(image_path):
    model_path = "models/method_ela_2.h5"
    model = keras.models.load_model(model_path)

    image = prepare_image(image_path).reshape(1, 128, 128, 3)

    output = model.predict(image, batch_size=1).reshape((2, ))

    if output[0] < output[1]:
        print("Real!", output[1])
        return "Real", output[1]
    else:
        print("Fake!", output[0])
        return "Fake", output[0]
