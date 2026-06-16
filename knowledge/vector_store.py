import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "synaptica_docs"

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():
    client = get_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def reset_collection():
    client = get_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks_to_chroma(chunks, source_name="document.pdf", reset=True):
    if reset:
        collection = reset_collection()
    else:
        collection = get_collection()

    ids = []
    embeddings = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"{source_name}_{i}")
        embeddings.append(model.encode(chunk).tolist())
        metadatas.append(
            {
                "source": source_name,
                "chunk_index": i,
            }
        )

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    return len(chunks)


def search_chroma(query, top_k=3):
    collection = get_collection()
    query_embedding = model.encode(query).tolist()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )