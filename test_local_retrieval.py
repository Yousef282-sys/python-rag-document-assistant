# Test loading the persisted ChromaDB vector store locally.

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Define the local ChromaDB path.
PROJECT_ROOT = Path(__file__).resolve().parent
CHROMA_PATH = PROJECT_ROOT / "backend" / "data" / "vector_store" / "chroma_db_v2"

# Load the same embedding model used during the Colab pipeline.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the persisted ChromaDB database.
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

# Load the existing collection.
collection = client.get_collection(name="python_tutorial_v2")

print(f"ChromaDB path: {CHROMA_PATH}")
print(f"Number of stored documents: {collection.count()}")

# Test semantic retrieval with a simple question.
question = "What is a Python dictionary?"

query_embedding = embedding_model.encode(
    [question],
    normalize_embeddings=True
)[0]

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=3
)

print("\nTop retrieved results:\n")

for i in range(len(results["documents"][0])):
    metadata = results["metadatas"][0][i]
    document = results["documents"][0][i]

    print(f"Result {i + 1}")
    print(f"Source: {metadata['source']}")
    print(f"Section: {metadata['section']}")
    print(f"Distance: {results['distances'][0][i]:.4f}")
    print(f"Text: {document[:300]}...")
    print("-" * 80)