import fitz  
import re
import csv

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

def generate_report(pdf_path, titles):
    # Extract the full text from the PDF
    full_text = extract(pdf_path)
    
    # Open the CSV file for writing
    csv_path = 'report.csv'
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Has Content"])
        
        for i in range(len(titles) - 1):
            start_title = re.escape(titles[i])
            end_title = re.escape(titles[i + 1])
            # print(start_title)
            # print(end_title)
            
            # Use regular expression to find the content between titles
            pattern = re.compile(rf'{start_title}(.*){end_title}', re.DOTALL | re.IGNORECASE)
            match = pattern.search(full_text)
            has_content = False
            
            if match:
                content = match.group(1).strip()
                has_content = bool(content)
            
            writer.writerow([titles[i], "Yes" if has_content else "No"])
            writer.writerow([titles[i], content])
        
        #for the last one alone
        start_title = re.escape(titles[-1])
        pattern = re.compile(rf'{start_title}(.*)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(full_text)
        has_content = False
        
        if match:
            content = match.group(1).strip()
            has_content = bool(content)
        
        writer.writerow([titles[-1], content])
        writer.writerow([titles[-1], "Yes" if has_content else "No"])

# Usage example
pdf_path = "pdf_path"  # Path to the PDF file
titles = ["title1", "title2"]
# generate_report(pdf_path, titles)
# print("Report generated: report.csv")
# print(extract_text_with_image_indicators(pdf_path))
generate_report(pdf_path,titles)