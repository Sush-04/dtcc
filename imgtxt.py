# from PIL import Image
# from pytesseract import pytesseract
# path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# def txt(path):
#     pytesseract.tesseract_cmd = path_to_tesseract
#     img = Image.open(path)
#     print(img)
#     text = pytesseract.image_to_string(img)
#     if text:
#         return(text)
#     else:
#         return("No text found")

# path = 'test4.jpeg'
# res = txt(path)
# print(res)
from PIL import Image
from pytesseract import pytesseract
import fitz  # PyMuPDF
from io import BytesIO

# Set the path to the Tesseract executable
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from image data (bytes)
def extract_text_from_image(image_data):
    img = Image.open(BytesIO(image_data))  # Open the image from bytes
    text = pytesseract.image_to_string(img)
    return text if text else "No text found"

# Function to extract images from a PDF and extract text from those images
def extract_text_from_pdf_images(pdf_path):
    doc = fitz.open(pdf_path)
    image_texts = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]  # Get image data as bytes
            text = extract_text_from_image(image_bytes)
            image_texts.append({
                "page_num": page_num + 1,
                "image_index": img_index,
                "text": text
            })

    doc.close()
    return image_texts

# Example usage
pdf_path = "path/to/your/pdf_with_images.pdf"
image_texts = extract_text_from_pdf_images(pdf_path)

# Print extracted text from images
for image_text in image_texts:
    print(f"Page {image_text['page_num']}, Image {image_text['image_index']}:")
    print(image_text['text'])
    print("="*80)
