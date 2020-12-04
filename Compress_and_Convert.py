import sys
from os import listdir
from os.path import isfile, join, isdir
from requests import get
from zipfile import ZipFile
from tqdm import tqdm
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFSyntaxError, PDFInfoNotInstalledError, PDFPageCountError, PDFPopplerTimeoutError


def compress_images(og_imgs: list, params: dict):
    if type(og_imgs) == int:
        print("Error reading file or quality factor out of bounds")
        return False
    elif not (0 < params['quality'] < 101):
        print("Quality factor out of bounds")
        return False
    else:
        print("Saving images...")
    if not isdir("data/images"):
        os.mkdir("data/images")
    for i in tqdm(range(len(og_imgs))):
        try:
            og_imgs[i].save(fp=f"data/images/{i}.jpg", optimize=True, quality=params['quality'])
        except Exception as e:
            print(f"error saving file: {e}")
            return False
    print("Successfully saved")
    return True


def setup_poppler():
    try:
        print('Downloading...')
        resp = get(r"https://github.com/oschwartz10612/poppler-windows/releases/download/v20.11.0/Release-20.11.0.zip")

        with open("poppler.zip", "wb") as f:
            f.write(resp.content)

        print('Extracting...')
        with ZipFile("poppler.zip", "r") as zp:
            zp.extractall()
    except Exception as e:
        return False
    else:
        print("Poppler set up successful")
        return True


class CNC:
    def __init__(self, path: str, poppler_path: str):
        self.FILE_PATH = path
        self.POPPLER_PATH = poppler_path
        if not isdir(self.POPPLER_PATH):
            print("Poppler not found, installing now")
            if not setup_poppler():
                print("error is setting up poppler")
                sys.exit()

    def get_images(self):
        """
        return images from pdf
        :return: list of PIL images or error codes
        Error codes:
        1=>PDF format error
        2=>Poppler timeout
        3=>PDF read but no images
        """
        try:
            print("Reading pdf file...")
            images = convert_from_path(self.FILE_PATH, poppler_path=self.POPPLER_PATH)
        except (PDFSyntaxError, PDFInfoNotInstalledError, PDFPageCountError):
            return 1
        except PDFPopplerTimeoutError:
            return 2
        if images:
            print(f"Total {len(images)} images from {len(images)} pages in pdf")
            return images
        else:
            return 3

    def to_pdf(self):
        try:
            img_paths = [join(self.FILE_PATH, f) for f in listdir(self.FILE_PATH)
                         if
                         (isfile(join(self.FILE_PATH, f)) and (f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")))]
        except [FileNotFoundError, OSError]:
            print("Not a valid path")
            return False
        if not img_paths:
            print("No images found")
            return False
        img_data = []
        for img in img_paths:
            img_data.append(Image.open(img))
        try:
            img_data[0].save(r"data/pdfs/converted.pdf", "PDF", resolution=100.0, save_all=True, append_images=img_data)
        except AttributeError:
            print("Error saving pdf")
        else:
            return True


if __name__ == '__main__':
    pass
    # cnc = CNC('data/pdfs/gre_aidi_fellowships.pdf', r"C:\Users\pratik\Documents\poppler-20.11.0\bin")
    # images = cnc.get_images()
    # compress_images(images, {"quality": 90})
