import json
from pathlib import Path

import numpy as np
from openai import OpenAI


ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = ROOT / "data" / "documents"
INDEX_FILE = ROOT / "data" / "memory_index.json"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

EMBEDDING_MODEL = "nomic-embed-text:latest"


def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def build_index():
    records = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        # Split documents into smaller chunks.
        paragraphs = [
            p.strip()
            for p in content.split("\n\n")
            if p.strip()
        ]

        for number, paragraph in enumerate(paragraphs, start=1):
            records.append({
                "source": file_path.name,
                "chunk": number,
                "text": paragraph,
                "embedding": get_embedding(paragraph)
            })

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

    INDEX_FILE.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )

    print(f"Indexed {len(records)} document chunks.")
    print(f"Saved index to: {INDEX_FILE}")


def search_documents(question, top_k=3):
    if not INDEX_FILE.exists():
        return {
            "success": False,
            "error": "Memory index not found. Build the index first.",
            "results": []
        }

    try:
        records = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

        if not records:
            return {
                "success": False,
                "error": "The memory index is empty.",
                "results": []
            }

        query_vector = np.array(get_embedding(question), dtype=float)

        scored_results = []

        for record in records:
            document_vector = np.array(
                record["embedding"], dtype=float
            )

            denominator = (
                np.linalg.norm(query_vector)
                * np.linalg.norm(document_vector)
            )

            similarity = (
                float(np.dot(query_vector, document_vector) / denominator)
                if denominator else 0.0
            )

            scored_results.append({
                "source": record["source"],
                "chunk": record["chunk"],
                "text": record["text"],
                "similarity": similarity
            })

        scored_results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        return {
            "success": True,
            "results": scored_results[:top_k]
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "results": []
        }


if __name__ == "__main__":
    build_index()
