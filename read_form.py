import pytesseract
from PIL import Image
import spacy
import fitz  # PyMuPDF
import io

# Path to tesseract executable (modify according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

def ocr_image(image_path):
    """Perform OCR on an image and return extracted text."""
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def ocr_pdf(pdf_path):
    """Perform OCR on a PDF and return extracted text."""
    text = ""
    document = fitz.open(pdf_path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        
        # Convert pixmap to image
        img_byte_arr = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Perform OCR on the image
        text += pytesseract.image_to_string(Image.open(io.BytesIO(img_byte_arr)))
    return text

def extract_entities(text, target_entities=None):
    """Extract specified named entities from text using SpaCy."""
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents if target_entities is None or ent.label_ in target_entities}
    return entities

def process_image(image_path, target_entities=None):
    """Extract specified entities from an image file."""
    text = ocr_image(image_path)
    return extract_entities(text, target_entities)

def process_pdf(pdf_path, target_entities=None):
    """Extract specified entities from a PDF file."""
    text = ocr_pdf(pdf_path)
    return extract_entities(text, target_entities)

# Example usage
# image_path = 'example_image.png'  # Path to your image file
pdf_path = "C:/Users/sush/OneDrive/app_form.pdf"  # Path to your PDF file

# Define the entities you want to extract
target_entities = ['Full Name', "Father's Name ", 'DATE']

# Extract entities from image
# image_entities = process_image(image_path, target_entities)
# print("Entities extracted from image:", image_entities)

# Extract entities from PDF
pdf_entities = process_pdf(pdf_path, target_entities)
print("Entities extracted from PDF:", pdf_entities)
