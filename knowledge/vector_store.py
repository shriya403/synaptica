import re
import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "chroma_db"

model = SentenceTransformer("all-MiniLM-L6-v2")


def sanitize_collection_name(filename):
    name = filename.lower()
    name = re.sub(r"[^a-z0-9_-]", "_", name)
    name = name[:50]
    return f"doc_{name}"


def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection(collection_name):
    client = get_client()
    return client.get_or_create_collection(name=collection_name)


def add_chunks_to_chroma(chunks, source_name):
    collection_name = sanitize_collection_name(source_name)
    collection = get_collection(collection_name)

    ids = []
    embeddings = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"{collection_name}_{i}")
        embeddings.append(model.encode(chunk).tolist())
        metadatas.append(
            {
                "source": source_name,
                "collection": collection_name,
                "chunk_index": i,
            }
        )

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    return {
        "chunks_stored": len(chunks),
        "collection_name": collection_name,
    }


def search_chroma(query, collection_name, top_k=3):
    collection = get_collection(collection_name)
    query_embedding = model.encode(query).tolist()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )


def list_collections():
    client = get_client()
    collections = client.list_collections()

    return [
        collection.name
        for collection in collections
    ]