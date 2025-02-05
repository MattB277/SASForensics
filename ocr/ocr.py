from PIL import Image
import pytesseract
import numpy as np

def ocr(filename):

    # path where your tesseract is installed
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img1 = np.array(Image.open(filename))
    text = pytesseract.image_to_string(img1)
    return text