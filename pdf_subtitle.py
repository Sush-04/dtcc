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

def find_title_order(full_text, titles):
    title_positions = []
    for title in titles:
        match = re.search(re.escape(title), full_text, re.IGNORECASE)
        if match:
            title_positions.append((match.start(), title))
    title_positions.sort()
    ordered_titles = [title for _, title in title_positions]
    return ordered_titles

def generate_report(pdf_path, titles_with_subtitles):
    # Extract the full text from the PDF
    full_text = extract(pdf_path)
    print(full_text)
    
    # Find the order of the titles in the full text
    ordered_titles = find_title_order(full_text, titles_with_subtitles.keys())
    
    # Open the CSV file for writing
    csv_path = 'report.csv'
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title/SubTitle", "Has Content"])
        
        for i in range(len(ordered_titles)):
            start_title = re.escape(ordered_titles[i])
            end_title = re.escape(ordered_titles[i + 1]) if i + 1 < len(ordered_titles) else None
            
            if end_title:
                pattern = re.compile(rf'{start_title}(.*?){end_title}', re.DOTALL | re.IGNORECASE)
            else:
                pattern = re.compile(rf'{start_title}(.*)', re.DOTALL | re.IGNORECASE)
            
            match = pattern.search(full_text)
            title_content = match.group(1).strip() if match else ""
            # print(title_content)
            
            # Get the subtitles for this title
            subtitles = titles_with_subtitles.get(ordered_titles[i], [])
            
            if subtitles:
                # Content between title and first subtitle
                start_subtitle = re.escape(subtitles[0])
                sub_pattern = re.compile(rf'{start_title}(.*?){start_subtitle}', re.DOTALL | re.IGNORECASE)
                sub_match = sub_pattern.search(full_text)
                content = sub_match.group(1).strip() if sub_match else ""
                has_content = bool(content)
                writer.writerow([ordered_titles[i], "Yes" if has_content else "No"])
                
                # Content between consecutive subtitles
                for j in range(len(subtitles) - 1):
                    start_subtitle = re.escape(subtitles[j])
                    end_subtitle = re.escape(subtitles[j + 1])
                    
                    sub_pattern = re.compile(rf'{start_subtitle}(.*?){end_subtitle}', re.DOTALL | re.IGNORECASE)
                    sub_match = sub_pattern.search(full_text)
                    content = sub_match.group(1).strip() if sub_match else ""
                    has_content = bool(content)
                    
                    writer.writerow([subtitles[j], "Yes" if has_content else "No"])
                
                # Content between the last subtitle and the next title
                start_subtitle = re.escape(subtitles[-1])
                if end_title:
                    sub_pattern = re.compile(rf'{start_subtitle}(.*?){end_title}', re.DOTALL | re.IGNORECASE)
                else:
                    sub_pattern = re.compile(rf'{start_subtitle}(.*)', re.DOTALL | re.IGNORECASE)
                sub_match = sub_pattern.search(full_text)
                content = sub_match.group(1).strip() if sub_match else ""
                has_content = bool(content)
                
                writer.writerow([subtitles[-1], "Yes" if has_content else "No"])
            else:
                # No subtitles, content between title and next title
                has_content = bool(title_content)
                writer.writerow([ordered_titles[i], "Yes" if has_content else "No"])
        
# Usage example
pdf_path = "C:/Users/sush/Downloads/test.pdf"  # Path to the PDF file
titles_with_subtitles = {
    "abc": ["bcd"],
    "efg": ["ghi"],
    "hij": [],  # No subtitles for this title
    "ijk": []   # No subtitles for this title
}
generate_report(pdf_path, titles_with_subtitles)
