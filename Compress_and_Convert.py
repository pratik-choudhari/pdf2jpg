from pdf2image import convert_from_path
from pdf2image.exceptions import PDFSyntaxError, PDFInfoNotInstalledError, PDFPageCountError, PDFPopplerTimeoutError
from tqdm import tqdm


def compress_images(og_imgs: list, params: dict):
    for i in tqdm(range(len(og_imgs))):
        try:
            og_imgs[i].save(fp=f"data/images/{i}.jpg", optimize=True, quality=params['quality'])
        except Exception as e:
            print(f"error saving file: {e}")
            return False
    return True


class CNC:
    def __init__(self, pdf_path: str, poppler_path: str):
        self.PDF_PATH = pdf_path
        self.POPPLER_PATH = poppler_path

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
            images = convert_from_path(self.PDF_PATH, poppler_path=self.POPPLER_PATH)
        except (PDFSyntaxError, PDFInfoNotInstalledError, PDFPageCountError):
            return 1
        except PDFPopplerTimeoutError:
            return 2
        if images:
            print(f"Total {len(images)} images in pdf")
            return images
        else:
            return 3


if __name__ == '__main__':
    cnc = CNC('data/pdfs/gre_aidi_fellowships.pdf', r"C:\Users\pratik\Documents\poppler-20.11.0\bin")
    images = cnc.get_images()
    compress_images(images, {"quality": 90})
