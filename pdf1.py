import fitz
import re
import csv
from PIL import Image
from pytesseract import pytesseract
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract(pdf_path):
    pdf_dummy = fitz.open(pdf_path)
    all_content = ""

    for page_num in range(pdf_dummy.page_count):
        page = pdf_dummy.load_page(page_num)
        
        # for text alone
        text = page.get_text("text")
        
        # this is for my image checking
        images = page.get_images(full=True)
        
        # this is to replace the image with an indicator
        if images:
            text += " <image>"
        
        # add this text , image in order
        all_content += text + "\n"

    return all_content

def find_title_order(full_text, titles):
    title_positions = []
    for title in titles:
        match = re.search(re.escape(title), full_text, re.IGNORECASE)
        if match:
            # print(match.start())
            title_positions.append((match.start(), title))
    title_positions.sort()
    # print(title_positions)
    ordered_titles = [title for _, title in title_positions]
    # print(ordered_titles)
    return ordered_titles

def generate_report(pdf_path, titles):
    # Extract the full text from the PDF
    full_text = extract(pdf_path)
    
    # Find the order of the titles in the full text
    ordered_titles = find_title_order(full_text, titles)
    
    # Open the CSV file for writing
    csv_path = 'report.csv'
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Has Content"])
        
        for i in range(len(ordered_titles) - 1):
            start_title = re.escape(ordered_titles[i])
            end_title = re.escape(ordered_titles[i + 1])
            
            # Use regular expression to find the content between titles
            pattern = re.compile(rf'{start_title}(.*?){end_title}', re.DOTALL | re.IGNORECASE)
            match = pattern.search(full_text)
            has_content = False
            
            if match:
                content = match.group(1).strip()
                has_content = bool(content)
            
            writer.writerow([ordered_titles[i], "Yes" if has_content else "No"])
            writer.writerow([ordered_titles[i], content])
        
        # For the last one alone
        start_title = re.escape(ordered_titles[-1])
        pattern = re.compile(rf'{start_title}(.*)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(full_text)
        has_content = False
        
        if match:
            content = match.group(1).strip()
            has_content = bool(content)
        
        writer.writerow([ordered_titles[-1], "Yes" if has_content else "No"])
        writer.writerow([ordered_titles[-1], content])

# Usage example
pdf_path = "C:/Users/sush/Downloads/trial1.pdf"  # Path to the PDF file
titles = ["abc", "cde","bcd","efg","def"]
generate_report(pdf_path, titles)
