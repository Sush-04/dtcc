import fitz  # PyMuPDF

def extract_text_with_image_indicators(pdf_path):
    pdf_document = fitz.open(pdf_path)
    all_content = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Extract text from the page
        text = page.get_text("text")
        
        # Check if there are images on the page
        images = page.get_images(full=True)
        
        # Indicator for image presence
        if images:
            text += " <image>"
        
        # Append to the overall content list
        all_content.append(text.strip())

    return all_content

# Example usage
pdf_path = "C:/Users/sush/Downloads/trial1.pdf"  # Path to the PDF file
extracted_content = extract_text_with_image_indicators(pdf_path)

# Print the extracted content preserving order with image indicators
print("Extracted Content with Image Indicators:")
for page_num, content in enumerate(extracted_content, start=1):
    # print(f"Page {page_num}:")
    print(content)
    print()
