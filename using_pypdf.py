import fitz  # PyMuPDF
import PyPDF4
import csv
import re

def extract_bookmarks_with_fit(pdf_path):
    bookmarks = []
    doc = fitz.open(pdf_path)
    
    # The TOC (table of contents) is a list of lists with the structure [level, title, page]
    toc = doc.get_toc()
    
    for item in toc:
        level, title, page = item
        bookmarks.append({
            "page": page,
            "title": title,
        })
    
    doc.close()
    return bookmarks

def extract_page_content_with_fit(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)  # page_num in TOC is 1-based, fitz is 0-based
    text = page.get_text("text")
    images = page.get_images(full=True)
    if images:
        text += " <image>"
    doc.close()
    return text

def extract_content_between_pages_with_fit(pdf_path, start_page, end_page):
    content = ""
    for page_num in range(start_page, end_page + 1):
        content += extract_page_content_with_fit(pdf_path, page_num) + "\n"
    return content.strip()

def generate_report_with_fit_and_pypdf4(pdf_path, output_folder):
    bookmarks = extract_bookmarks_with_fit(pdf_path)
    csv_path = 'report_combined.csv'
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Page", "Has Content", "Content File with Fitz", "Content File with PyPDF4"])
        
        for i, bookmark in enumerate(bookmarks):
            title = bookmark['title']
            start_page = bookmark['page']
            end_page = bookmarks[i + 1]['page'] - 1 if i + 1 < len(bookmarks) else fitz.open(pdf_path).page_count
            
            content_fit = extract_content_between_pages_with_fit(pdf_path, start_page, end_page).strip()
            
            # Check if the title is present in the content extracted using fitz
            match_fit = re.search(re.escape(title), content_fit, re.IGNORECASE)
            if match_fit:
                # Extract content after the title using fitz
                content_after_title_fit = content_fit[match_fit.end():].strip()
                has_content_fit = bool(content_after_title_fit)
                
                if has_content_fit:
                    # Save content as a separate PDF using fitz
                    new_pdf_name_fit = f"{output_folder}/{title.replace(' ', '_')}_fitz.pdf"
                    new_doc_fit = fitz.open()
                    new_page_fit = new_doc_fit.new_page()
                    new_page_fit.insert_text((100, 100), content_after_title_fit)
                    new_doc_fit.save(new_pdf_name_fit)
                else:
                    new_pdf_name_fit = ""
            else:
                has_content_fit = False
                new_pdf_name_fit = ""
            
            # Extract content between pages using PyPDF4
            content_pypdf4 = extract_content_between_pages_pypdf4(pdf_path, start_page, end_page).strip()
            
            # Check if the title is present in the content extracted using PyPDF4
            match_pypdf4 = re.search(re.escape(title), content_pypdf4, re.IGNORECASE)
            if match_pypdf4:
                # Extract content after the title using PyPDF4
                content_after_title_pypdf4 = content_pypdf4[match_pypdf4.end():].strip()
                has_content_pypdf4 = bool(content_after_title_pypdf4)
                
                if has_content_pypdf4:
                    # Create a new PDF document named after the title using PyPDF4
                    new_pdf_writer_pypdf4 = PyPDF4.PdfWriter()
                    new_pdf_writer_pypdf4.add_blank_page()
                    new_pdf_writer_pypdf4.add_text(content_after_title_pypdf4)
                    new_pdf_name_pypdf4 = f"{output_folder}/{title.replace(' ', '_')}_pypdf4.pdf"
                    with open(new_pdf_name_pypdf4, 'wb') as new_file_pypdf4:
                        new_pdf_writer_pypdf4.write(new_file_pypdf4)
                else:
                    new_pdf_name_pypdf4 = ""
            else:
                has_content_pypdf4 = False
                new_pdf_name_pypdf4 = ""
            
            writer.writerow([title, start_page, "Yes" if has_content_fit else "No", new_pdf_name_fit, new_pdf_name_pypdf4])

def extract_content_between_pages_pypdf4(pdf_path, start_page, end_page):
    content = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF4.PdfReader(pdf_file)
        for page_num in range(start_page - 1, end_page):
            page = pdf_reader.pages[page_num]
            content += page.extract_text() + "\n"
    return content.strip()

# Usage example
pdf_path = "C:/Users/sush/Downloads/bookmarked__with_subtitles.pdf" 
output_folder = "C:/Users/sush/Downloads/my_folder"  
generate_report_with_fit_and_pypdf4(pdf_path, output_folder)
