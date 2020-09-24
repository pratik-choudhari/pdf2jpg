from pdf2image import convert_from_path
from pdf2image.exceptions import PDFSyntaxError, PDFInfoNotInstalledError, PDFPageCountError, PDFPopplerTimeoutError


def getImages(pdf: str):
    """
    return images from pdf
    :param pdf: pdf file path
    :return: list of PIL images or error codes
    Error codes:
    1=>PDF format error
    2=>PDF doesn't exist
    3=>PDF read but no images
    """
    try:
        images = convert_from_path(pdf)
    except (PDFSyntaxError, PDFInfoNotInstalledError):
        return 1
    except (PDFPageCountError, PDFPopplerTimeoutError):
        return 2
    if images:
        for img in images:
            img.show()
    else:
        return 3


def resize_images(images: list):
    pass


if __name__ == '__main__':
    print(getImages('data/sem8_examack.pdf'))
