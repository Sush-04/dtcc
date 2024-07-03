from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path =r'C:\Users\sush\Downloads\test2.jpg'
with Image.open(image_path) as img:
    text = pytesseract.image_to_string(img)
    print("yes")
    print(text)
print(text)




# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'