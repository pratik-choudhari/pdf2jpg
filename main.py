from Compress_and_Convert import CNC, compress_images

pdf_path = input('Enter full pdf path: ')
quality = input('Input quality factor(1-100): ')
cnc = CNC(pdf_path, r"C:\Users\pratik\Documents\poppler-20.11.0\bin")
images = cnc.get_images()
compress_images(images, {"quality": int(quality)})

# C:\Users\pratik\Documents\pdf2jpg\data\pdfs\gre_aidi_fellowships.pdf