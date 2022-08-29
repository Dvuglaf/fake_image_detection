import argparse
import ela
import level1
import numpy as np
import torch
from PIL import Image
from model import IMDModel


def infer(img_path, model, device):
    print("Performing Level 1 analysis...")
    pred1 = level1.find_metadata(img_path=img_path)

    print("Performing Level 2 analysis...")
    ela.ela(img_path=img_path)

    img = Image.open("temp/ela_img.jpg")
    img = img.resize((128, 128))
    img = np.array(img, dtype=np.float32).transpose((2, 0, 1)) / 255.0
    img = np.expand_dims(img, axis=0)

    out = model(torch.from_numpy(img).to(device=device))
    y_pred = torch.max(out, dim=1)[1]

    pred2 = "Real" if y_pred else "Fake"  # auth -> 1 and tp -> 0

    return pred1, pred2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image Manipulation Detection')

    req_args = parser.add_argument_group('Required Args')
    req_args.add_argument('-p', '--path', type=str, metavar='img_path', dest='img_path', required=True,
                          help='Image Path')

    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # selecting device
    print("Working on", device)

    model_path = "models/model_c1.pth"
    model = torch.load(model_path, map_location=device)
    print(infer(model=model, img_path=args.img_path, device=device))
