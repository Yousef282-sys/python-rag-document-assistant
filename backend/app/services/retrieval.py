from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHROMA_PATH = PROJECT_ROOT / "backend" / "data" / "vector_store" / "chroma_db_v2"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "python_tutorial_v2"

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = chroma_client.get_collection(name=COLLECTION_NAME)


def retrieve_documents(question: str, top_k: int = 3):
    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True,
    )[0]

    return collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
    )


def build_context(results) -> str:
    context_parts = []

    for i in range(len(results["documents"][0])):
        document = results["documents"][0][i]
        metadata = results["metadatas"][0][i]

        context_parts.append(
            f"[Source: {metadata['source']} | Section: {metadata['section']}]\n"
            f"{document}"
        )

    return "\n\n---\n\n".join(context_parts)


def retrieve_context(question: str, top_k: int = 3) -> str:
    results = retrieve_documents(question, top_k=top_k)
    return build_context(results)
