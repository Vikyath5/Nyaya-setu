"""
Similarity Engine for NyayaSetu

Finds semantically similar past legal cases using sentence embeddings
and cosine similarity.
"""

import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.ai.embedding_model import get_embedding


EMBEDDING_FILE = "models/case_embeddings.pkl"


class SimilarityEngine:

    def __init__(self):

        # Check if embedding file exists
        if not os.path.exists(EMBEDDING_FILE):
            raise FileNotFoundError(
                f"{EMBEDDING_FILE} not found. Run the embedding generation script first."
            )

        # Check if file is empty
        if os.path.getsize(EMBEDDING_FILE) == 0:
            raise ValueError(
                f"{EMBEDDING_FILE} is empty. Regenerate embeddings before starting the server."
            )

        # Load embeddings safely
        try:
            with open(EMBEDDING_FILE, "rb") as f:
                data = pickle.load(f)

        except Exception as e:
            raise RuntimeError(
                "Failed to load case embeddings. The file may be corrupted."
            ) from e

        self.cases = data.get("cases", [])

        if not self.cases:
            raise ValueError(
                "No cases found inside case_embeddings.pkl. Regenerate embeddings."
            )

        # Extract embeddings matrix
        self.embeddings = np.array([
            case["embedding"] for case in self.cases
        ])

    def find_similar_cases(self, case_description: str, top_k: int = 5):

        if not case_description:
            return []

        # Generate query embedding
        query_embedding = np.array(
            get_embedding(case_description)
        ).reshape(1, -1)

        # Compute cosine similarity
        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        # Get top similar cases
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []

        for idx in top_indices:

            case = self.cases[idx]

            results.append({
                "case_id": case.get("case_id"),
                "case_type": case.get("case_type"),
                "text": case.get("text"),
                "similarity_score": float(similarities[idx])
            })

        return results