import json
import pickle
import os
from backend.ai.embedding_model import get_embedding

INPUT_FILE = "backend/dataset/indian_cases.json"
OUTPUT_FILE = "models/case_embeddings.pkl"


def generate_embeddings():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    embedded_cases = []

    for case in cases:
        text = case["summary"]

        embedding = get_embedding(text)

        embedded_cases.append({
            "case_id": case["case_id"],
            "case_type": case["case_type"],
            "text": text,
            "embedding": embedding
        })

    os.makedirs("models", exist_ok=True)

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump({"cases": embedded_cases}, f)

    print("Embeddings generated successfully!")
    print("Total cases:", len(embedded_cases))


if __name__ == "__main__":
    generate_embeddings()