import fitz  
import csv
import re

def extract_bookmarks(pdf_path):
    bookmarks = []
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    #here im getting the actual bookmarked values
    for item in toc:
        level, title, page = item
        bookmarks.append({
            "page": page,
            "title": title,
        })
    
    doc.close()
    return bookmarks

def extract_page_content(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)  
    #for text
    text = page.get_text("text")
    #for image
    images = page.get_images(full=True)
    if images:
        text += " <image>"
    doc.close()
    return text

def extract_content_between_pages(pdf_path, start_page, end_page):
    content = ""
    
    for page_num in range(start_page, end_page + 1):
        content += extract_page_content(pdf_path, page_num) + "\n"
    return content.strip()

def generate_report(pdf_path, output_folder):
    bookmarks = extract_bookmarks(pdf_path)
    csv_path = 'report.csv'
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Page", "Has Content"])
        
        for i, bookmark in enumerate(bookmarks):
            title = bookmark['title']
            start_page = bookmark['page']
            end_page = bookmarks[i + 1]['page'] - 1 if i + 1 < len(bookmarks) else fitz.open(pdf_path).page_count
            
            content = extract_content_between_pages(pdf_path, start_page, end_page).strip()
            
            
            match = re.search(re.escape(title), content, re.IGNORECASE)
            if match:
                # here im extracting content after the title
                content_after_title = content[match.end():].strip()
                has_content = bool(content_after_title)
                
                if has_content:
                    # storing it in a pdf
                    pdf = fitz.open()
                    new_page = pdf.new_page()
                    new_page.insert_text((72, 72), content_after_title)
                    content_file_path = f"{output_folder}/{title.replace(' ', '_')}.pdf"
                    pdf.save(content_file_path)
                    pdf.close()
                else:
                    content_file_path = ""
                
                writer.writerow([title, start_page, "Yes" if has_content else "No"])
            else:
                writer.writerow([title, start_page, "No"])
            
# eg
pdf_path = "C:/Users/sush/Downloads/Bookmarked_PDF_Revised.pdf" 
output_folder = "C:/Users/sush/Downloads/my_folder"  
generate_report(pdf_path, output_folder)
