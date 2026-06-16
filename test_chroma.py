from knowledge.ingest import extract_pdf_text, chunk_text
from knowledge.vector_store import add_chunks_to_chroma, search_chroma

text = extract_pdf_text("uploads/sample.pdf")
chunks = chunk_text(text)

count = add_chunks_to_chroma(chunks, source_name="sample.pdf")

print("Chunks stored:", count)

results = search_chroma("What is this document about?", top_k=2)

print("\nSearch Results:")
print(results["documents"])