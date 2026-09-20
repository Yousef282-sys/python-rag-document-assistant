# Test the complete local RAG pipeline:
# ChromaDB retrieval -> context building -> Ollama generation.

from pathlib import Path

import chromadb
import requests
from sentence_transformers import SentenceTransformer


# Define the project and vector store paths.
PROJECT_ROOT = Path(__file__).resolve().parent
CHROMA_PATH = PROJECT_ROOT / "backend" / "data" / "vector_store" / "chroma_db_v2"

# Define the local Ollama configuration.
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:4b"

# Load the same embedding model used to create the vector store.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the persisted ChromaDB database.
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

# Load the existing collection.
collection = client.get_collection(name="python_tutorial_v2")


def retrieve_documents(question, top_k=3):
    """Retrieve the most relevant documentation chunks."""

    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True,
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
    )

    return results


def build_context(results):
    """Build a compact context from the retrieved chunks."""

    context_parts = []

    for i in range(len(results["documents"][0])):
        document = results["documents"][0][i]
        metadata = results["metadatas"][0][i]

        context_parts.append(
            f"[Source: {metadata['source']} | Section: {metadata['section']}]\n"
            f"{document}"
        )

    return "\n\n---\n\n".join(context_parts)


def generate_answer(question, context):
    """Generate a short answer using only the retrieved context."""

    prompt = f"""
You are a Python learning assistant.

Use ONLY the documentation in CONTEXT to answer the QUESTION.

Rules:
- Answer in 2 or 3 short sentences.
- Do not explain your reasoning.
- Do not show thinking.
- Do not use outside knowledge.
- If the context is insufficient, say:
  "I couldn't find enough information in the provided Python documentation."
- End with exactly one citation in this format:
  [source: filename]

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {
            "num_predict": 100,
        },
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["response"].strip()


# Define the test question.
question = "What is a Python dictionary?"

# Retrieve relevant documentation.
results = retrieve_documents(question, top_k=3)

# Build the RAG context.
context = build_context(results)

# Generate the grounded answer.
answer = generate_answer(question, context)

# Display the final result.
print("\n" + "=" * 70)
print("QUESTION")
print("=" * 70)
print(question)

print("\n" + "=" * 70)
print("RAG ANSWER")
print("=" * 70)
print(answer)

print("\n" + "=" * 70)
print("RETRIEVED SOURCES")
print("=" * 70)

for metadata in results["metadatas"][0]:
    print(f"- {metadata['source']} | {metadata['section']}")