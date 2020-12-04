from Compress_and_Convert import CNC, compress_images

ch = int(input("1. Convert PDF to JPG\n2. Convert JPG to PDF\nEnter your choice:"))
path = input("Enter file/folder path:")
cnc = CNC(path, r"poppler-20.11.0\bin")
if ch == 1:
    quality = input('Input quality factor(1-100): ')
    images = cnc.get_images()
    compress_images(images, {"quality": int(quality)})
elif ch == 2:
    res = cnc.to_pdf()
    if res:
        print("IMG to PDF successful")
else:
    exit()
# C:\Users\pratik\Documents\pdf2jpg\data\pdfs\gre_aidi_fellowships.pdf