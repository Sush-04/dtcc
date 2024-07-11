import fitz  
import csv
import re

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

def extract_page_content(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    text = page.get_text("text")
    images = page.get_images(full=True)
    if images:
        text += " <image>"
    doc.close()
    return text

def extract_content_between_pages(pdf_path, start_page, end_page, next_bookmark_title=None):
    content = ""
    for page_num in range(start_page, end_page + 1):
        content += extract_page_content(pdf_path, page_num) + "\n"
    
    if next_bookmark_title:
        next_title_pos = re.search(re.escape(next_bookmark_title), content, re.IGNORECASE)
        if next_title_pos:
            content = content[:next_title_pos.start()].strip()
    
    return content.strip()

def generate_report(pdf_path, output_folder):
    bookmarks = extract_bookmarks(pdf_path)
    csv_path = output_folder + '/report.csv'
    
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
                    end_page = next_start_page 
            else:
                next_title = None
                end_page = page_count

            content = extract_content_between_pages(pdf_path, start_page, end_page, next_title).strip()
            
            match = re.search(re.escape(title), content, re.IGNORECASE)
            if match:
                content_after_title = content[match.end():].strip()
                has_content = bool(content_after_title)
                
                if has_content:
                    pdf = fitz.open()
                    new_page = pdf.new_page()
                    new_page.insert_text((72, 72), content_after_title)
                    clean_title = re.sub(r'[^A-Za-z0-9 ]+', '', title)

                    content_file_path = output_folder + '/' + clean_title.replace(' ', '_') + '.pdf'
                    pdf.save(content_file_path)
                    pdf.close()
                
                writer.writerow([title, start_page, "Yes" if has_content else "No"])
            else:
                writer.writerow([title, start_page, "No"])

        doc.close()

# Example usage
pdf_path = "C:/Users/sush/Downloads/sample_test.pdf" 
output_folder = "C:/Users/sush/Downloads/my_folder"
generate_report(pdf_path, output_folder)
