from knowledge.ingest import extract_pdf_text, chunk_text

text = extract_pdf_text("uploads/sample.pdf")
chunks = chunk_text(text)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])