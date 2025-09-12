from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a list of texts."""
    return model.encode(texts).tolist()
