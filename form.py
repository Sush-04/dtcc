import pytesseract
from PIL import Image
import re

def extract_form_data(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    
    # patteren defifnition
    patterns = {
        "Name": r"Name:\s*(.*)",
        "Date of Birth": r"Date of Birth:\s*(.*)",
        "Address": r"Address:\s*(.*)",
        "Phone": r"Phone:\s*(.*)",
        "Email": r"Email:\s*(.*)"
    }
    
    # Extract the values using the patterns
    form_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            form_data[field] = match.group(1).strip()
    
    return form_data

# eg
# "C:\Users\sush\Pictures\Screenshots\Screenshot 2024-07-15 115015.png"
image_path = "C:/Users/sush/Downloads/form.png"
form_data = extract_form_data(image_path)
print(form_data)
