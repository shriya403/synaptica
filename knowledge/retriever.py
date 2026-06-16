from langchain_ollama import ChatOllama

from knowledge.vector_store import search_chroma


llm = ChatOllama(model="llama3.2", temperature=0.2)


def build_context(results):
    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents)


async def answer_from_docs(question, collection_name, top_k=3):
    results = search_chroma(
        query=question,
        collection_name=collection_name,
        top_k=top_k,
    )

    context = build_context(results)

    prompt = f"""
You are Synaptica RAG Agent.

Answer the question using ONLY the document context below.

If the answer is not present in the context, say:
"I could not find this information in the selected document."

Document Context:
{context}

Question:
{question}

Answer:
"""

    response = await llm.ainvoke(prompt)

    return {
        "question": question,
        "answer": response.content,
        "sources": results.get("metadatas", [[]])[0],
        "context_used": context,
    }