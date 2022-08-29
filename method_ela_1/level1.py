import PIL.Image
from PIL.ExifTags import TAGS


# finding metadata of the image
def find_metadata(img_path):
    img = PIL.Image.open(img_path)
    res = ''
    try:
        info = img.getexif()
        flag = 0
        for (tag, value) in info.items():
            if "Software" == TAGS.get(tag, tag):  # checking for software traces
                flag = 1
                res = res + f"Found Software Traces...\nSoftware Signature: {value}\n"
                print(res)
        if flag == 0:
            res = res + "No Software Signature Found. Seems like real image..."
            print(res)
            return res

    except Exception as e:
        res = res + f'Failed to load metadata, error : {e}'
        print(res)
        return res
    return res
