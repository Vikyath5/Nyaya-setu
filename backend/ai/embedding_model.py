"""Utilities for generating semantic text embeddings.

This module is intentionally import-friendly so it can be reused by other
components such as similarity engines, ranking pipelines, and API routes.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer


# Embeddings are dense numeric vectors that capture sentence meaning.
# In semantic similarity search, texts with related meaning produce vectors that
# are closer together (for example, by cosine similarity).
#
# The model is loaded once at import time so API requests and internal calls do
# not pay model initialization cost repeatedly.
_EMBEDDING_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_embedding(text: str) -> list[float]:
    """Generate and return a JSON-serializable embedding for input text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("text must be a non-empty string")

    # Return a Python list so FastAPI responses and downstream JSON handling
    # can serialize embeddings without additional conversion.
    embedding = _EMBEDDING_MODEL.encode(cleaned_text, convert_to_numpy=True)
    return embedding.tolist()


if __name__ == "__main__":
    sample_text = "My employer has not paid my salary for three months."
    embedding = get_embedding(sample_text)

    print(f"Embedding length: {len(embedding)}")
    print(f"First values: {embedding[:10]}")
