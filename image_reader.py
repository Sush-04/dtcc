from PIL import Image
from pytesseract import pytesseract
import fitz
import csv
import re
import os
from io import BytesIO

path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def txt(image_data):
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(BytesIO(image_data))
    text = pytesseract.image_to_string(img)
    return text if text else "No text found"

def extract_bookmarks(pdf_path):
    bookmarks = []
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    for item in toc:
        level, title, page = item
        bookmarks.append({
            "page": page,
            "title": title,
        })
    doc.close()
    return bookmarks

def extract_page_content_and_links(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    text = page.get_text("text")
    
    # Extract hyperlinks and their positions
    links = page.get_links()
    link_data = []
    for link in links:
        if 'uri' in link:
            uri = link['uri']
            rect = link['from']
            link_data.append((uri, rect))
    
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        text += " " + txt(image_bytes)
    
    doc.close()
    return text, link_data

def remove_first_pattern_after_title(content, title):
    title_pos = re.search(re.escape(title), content, re.IGNORECASE)
    if not title_pos:
        return content
    
    content_after_title = content[title_pos.end():]
    pattern = r'\([A-Za-z]\)'
    pattern_pos = re.search(pattern, content_after_title)
    if pattern_pos:
        content_after_pattern = content_after_title[pattern_pos.end():]
        return content_after_pattern.strip()
    
    return content_after_title.strip()

def extract_content_between_pages(pdf_path, start_page, end_page, next_bookmark_title=None):
    content = ""
    all_links = []
    for page_num in range(start_page, end_page + 1):
        page_content, page_links = extract_page_content_and_links(pdf_path, page_num)
        content += page_content + "\n"
        all_links.extend(page_links)
    
    if next_bookmark_title:
        next_title_pos = re.search(re.escape(next_bookmark_title), content, re.IGNORECASE)
        if next_title_pos:
            content = content[:next_title_pos.start()].strip()
    
    return content.strip(), all_links

def generate_report(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    bookmarks = extract_bookmarks(pdf_path)
    csv_path = os.path.join(output_folder, 'report.csv')
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Page", "Has Content"])
        
        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        
        for i, bookmark in enumerate(bookmarks):
            title = bookmark['title']
            start_page = bookmark['page']
            
            if i + 1 < len(bookmarks):
                next_bookmark = bookmarks[i + 1]
                next_title = next_bookmark['title']
                next_start_page = next_bookmark['page']
                
                if start_page == next_start_page:
                    end_page = start_page
                else:
                    end_page = next_start_page - 1
            else:
                next_title = None
                end_page = page_count

            content, links = extract_content_between_pages(pdf_path, start_page, end_page, next_title)
            content = remove_first_pattern_after_title(content, title)
            has_content = bool(content.strip())
            
            if has_content:
                pdf = fitz.open()
                new_page = pdf.new_page()
                new_page.insert_text((72, 72), content)
                
                # Add hyperlinks back to the new PDF
                for uri, rect in links:
                    new_page.insert_link({
                        "uri": uri,
                        "from": rect
                    })
                
                clean_title = re.sub(r'[^A-Za-z0-9 ]+', '', title)
                content_file_path = os.path.join(output_folder, clean_title.replace(' ', '_') + '.pdf')
                pdf.save(content_file_path)
                pdf.close()
            
            writer.writerow([title, start_page, "Yes" if has_content else "No"])

        doc.close()

# Example usage
pdf_path = "C:/Users/sush/Downloads/Arul-Jessica-A-FlowCV-Resume-20240417 (1).pdf" 
output_folder = "C:/Users/sush/Downloads/my_folder"
generate_report(pdf_path, output_folder)
