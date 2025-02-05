from PIL import Image
import pytesseract
import numpy as np

filename = 'C:\\Users\\48575\\Desktop\\react\\sh06-main\\ocr\\ocr1.jpg'
img1 = np.array(Image.open(filename))
text = pytesseract.image_to_string(img1)
print(text)