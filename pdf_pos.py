import fitz
import re
import csv

def extract(pdf_path):
    pdf_dummy = fitz.open(pdf_path)
    all_content = ""

    for page_num in range(pdf_dummy.page_count):
        page = pdf_dummy.load_page(page_num)
        
        # Extract text
        text = page.get_text("text")
        
        # Check for images
        images = page.get_images(full=True)
        if images:
            # If images exist, mark them somehow in your processing
            text += " <image>"
        
        all_content += text + "\n"

    return all_content

def find_title_order(full_text, titles):
    title_positions = []
    for title in titles:
        match = re.search(re.escape(title), full_text, re.IGNORECASE)
        if match:
            title_positions.append((match.start(), title))
    title_positions.sort()
    ordered_titles = [title for _, title in title_positions]
    return ordered_titles

def generate_report(pdf_path, titles):
    full_text = extract(pdf_path)
    print(full_text)
    ordered_titles = find_title_order(full_text, titles)
    
    csv_path = 'report.csv'
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Has Content", "Content"])
        
        for i in range(len(ordered_titles) - 1):
            start_title = re.escape(ordered_titles[i])
            end_title = re.escape(ordered_titles[i + 1])
            
            # Use iterative search to handle content between titles
            start_pos = full_text.find(start_title)
            # print(start_pos)
            # print(len(start_title))
            end_pos = full_text.find(end_title, start_pos + len(start_title))
            # print(end_pos)
            if start_pos != -1 and end_pos != -1:
                content = full_text[start_pos + len(start_title):end_pos].strip()
                
                # Check if content contains <image> marker
                if "<image>" in content:
                    has_content = True  # Consider <image> as content
                else:
                    has_content = bool(content)
            else:
                content = ""
                has_content = False
            
            writer.writerow([ordered_titles[i], "Yes" if has_content else "No", content])
        
        # Handle the last title separately
        start_title = re.escape(ordered_titles[-1])
        start_pos = full_text.find(start_title)
        
        if start_pos != -1:
            content = full_text[start_pos + len(start_title):].strip()
            print(content)
            
            # Check if content contains <image> marker
            if "<image>" in content:
                has_content = True  # Consider <image> as content
            else:
                has_content = bool(content)
        else:
            content = ""
            has_content = False
        
        writer.writerow([ordered_titles[-1], "Yes" if has_content else "No", content])

# Usage example
pdf_path = "C:/Users/sush/Downloads/trial1.pdf"  # Path to the PDF file
titles = ["Abc", "Cde", "Bcd", "efg", "Def"]
generate_report(pdf_path, titles)

