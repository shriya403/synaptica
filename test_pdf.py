from knowledge.ingest import extract_pdf_text

pdf_path = "uploads/sample.pdf"

text = extract_pdf_text(pdf_path)

print(text[:1000])