from PIL import Image
from pytesseract import pytesseract
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def txt(path):
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(path)
    print(img)
    text = pytesseract.image_to_string(img)
    if text:
        return(text)
    else:
        return("No text found")

path = 'test4.jpeg'
res = txt(path)
print(res)