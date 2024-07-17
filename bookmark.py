import fitz  # PyMuPDF

def extract_bookmarks(pdf_path):
    bookmarks = []
    doc = fitz.open(pdf_path)
    
    # The TOC (table of contents) is a list of lists with the structure [level, title, page]
    toc = doc.get_toc()
    print(toc)
    
    for item in toc:
        level, title, page = item
        bookmarks.append({
            "page": page,
            "title": title,
            # "level": level
        })
    
    doc.close()
    return bookmarks

# Example usage
pdf_path = "C:/Users/sush/Downloads/Arul-Jessica-A-FlowCV-Resume-20240417 (1).pdf"
bookmarks = extract_bookmarks(pdf_path)
for bookmark in bookmarks:
    print(f"Page {bookmark['page']}: {bookmark['title']} ")
