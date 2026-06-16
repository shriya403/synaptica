import asyncio

from knowledge.retriever import answer_from_docs


async def main():
    question = "What is this document about?"

    result = await answer_from_docs(question)

    print("QUESTION:")
    print(result["question"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    print(result["sources"])


asyncio.run(main())