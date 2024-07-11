import fitz  # PyMuPDF

def remove_watermarks_and_page_numbers(pdf_path, output_path, watermark_texts=[], page_number_region=None):
    doc = fitz.open(pdf_path)
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text_instances = page.search_for("\n".join(watermark_texts))
        
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(1, 1, 1))  # Add redaction annotation
        
        if page_number_region:
            rect = fitz.Rect(page_number_region)
            page.add_redact_annot(rect, fill=(1, 1, 1))  # Add redaction annotation for page numbers
        
        page.apply_redactions()  # Apply redactions

    doc.save(output_path)

# Usage example
pdf_path = "C:/Users/sush/Downloads/c4611_sample_explain.pdf"
output_path = "C:/Users/sush/Downloads/abc.pdf"
watermark_texts = ["pdf sample"]  # List of watermark texts to remove
page_number_region = [0, 800, 600, 850]  # Approximate region for page numbers (left, top, right, bottom)

remove_watermarks_and_page_numbers(pdf_path, output_path, watermark_texts, page_number_region)
