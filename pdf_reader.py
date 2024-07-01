import fitz  # PyMuPDF
import re
import csv

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        full_text += page.get_text("text") + "\n"
        # image_list = page.get_images(page)

    
    return full_text

def generate_report(pdf_path, titles):
    # Extract the full text from the PDF
    full_text = extract_text_from_pdf(pdf_path)
    
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
            writer.writerow([titles[i], match])
        
        # Check content for the last title till the end of the document
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
pdf_path = "C:/Users/sush/Downloads/trial1.pdf"  # Path to the PDF file
titles = ["abc", "bcd", "cde", "def","efg"]
# generate_report(pdf_path, titles)
# print("Report generated: report.csv")
print(extract_text_from_pdf(pdf_path))
# generate_report(pdf_path,titles)