import json
import os
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity

from backend.ai.embedding_model import EmbeddingModel


class SimilarityEngine:
    """
    SimilarityEngine

    Retrieves semantically similar cases using
    embedding-based vector similarity.
    """

    def __init__(self, dataset_path: str = None):

        if dataset_path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            dataset_path = os.path.join(base_dir, "dataset", "indian_cases.json")

        try:
            with open(dataset_path, "r", encoding="utf-8") as f:
                self.cases = json.load(f)
        except Exception:
            self.cases = []

        self.embedding_model = EmbeddingModel()

        # Precompute embeddings for dataset
        self.case_embeddings = []

        for case in self.cases:
            summary = case.get("summary", "")
            embedding = self.embedding_model.embed(summary)
            self.case_embeddings.append(embedding)

    # ------------------------------------
    # Find similar cases
    # ------------------------------------

    def find_similar_cases(
        self,
        user_query: str,
        top_k: int = 5
    ) -> List[Dict]:

        if not user_query:
            return []

        query_embedding = self.embedding_model.embed(user_query)

        similarities = cosine_similarity(
            [query_embedding],
            self.case_embeddings
        )[0]

        results = []

        for idx, score in enumerate(similarities):

            case = self.cases[idx]

            results.append({
                "summary": case.get("summary", ""),
                "case_type": case.get("case_type", ""),
                "outcome": case.get("outcome", ""),
                "resolution_time_months": case.get("resolution_time_months", 12),
                "similarity": round(float(score), 3)
            })

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        return results[:top_k]