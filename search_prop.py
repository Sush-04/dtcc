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

def extract_page_content_with_properties(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    blocks = page.get_text("dict")["blocks"]
    content = []
    for block in blocks:
        for line in block["lines"]:
            for span in line["spans"]:
                content.append({
                    "text": span["text"],
                    "size": span["size"],
                    "flags": span["flags"]
                })
    doc.close()
    return content

def is_bold(span_flags):
    # Check if the text is bold
    return bool(span_flags & 2)

def is_significantly_larger(size, average_size, threshold=1.5):
    # Check if the size is significantly larger than the average size
    return size > average_size * threshold

def extract_content_between_pages(pdf_path, start_page, end_page, next_bookmark_title=None):
    content = ""
    average_size = 0
    size_count = 0
    
    for page_num in range(start_page, end_page + 1):
        page_content = extract_page_content_with_properties(pdf_path, page_num)
        
        # Calculate the average font size
        for span in page_content:
            average_size += span["size"]
            size_count += 1
    average_size = average_size / size_count if size_count else 0
         # Extracting text and analyzing font properties
    for span in page_content:
            text = span["text"]
            size = span["size"]
            flags = span["flags"]
            if is_significantly_larger(size, average_size) and is_bold(flags):
                if content.strip():  # If there's already content, stop at the new title
                    return content.strip()
            content += text + "\n"
    
   
    
    if next_bookmark_title:
        page_content = extract_page_content_with_properties(pdf_path, end_page)
        for span in page_content:
            text = span["text"]
            size = span["size"]
            flags = span["flags"]
            if is_significantly_larger(size, average_size) and is_bold(flags):
                next_title_pos = re.search(re.escape(next_bookmark_title), text, re.IGNORECASE)
                if next_title_pos:
                    content = content[:next_title_pos.start()].strip()
                    break
    
    return content.strip()

def generate_report(pdf_path, output_folder):
    bookmarks = extract_bookmarks(pdf_path)
    print(bookmarks)
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
pdf_path = "C:/Users/sush/Downloads/bookmarked__with_subtitles.pdf" 
output_folder = "C:/Users/sush/Downloads/my_folder"
generate_report(pdf_path, output_folder)
