from sentence_transformers import SentenceTransformer, util
import json

STORAGE_PATH = "frontend/storage.json"
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_saved_papers():
    with open(STORAGE_PATH) as f:
        return json.load(f)

def find_relevant_passages(query, top_k=3):
    papers = load_saved_papers()
    corpus = [paper["summary"] for paper in papers]
    query_embedding = model.encode(query, convert_to_tensor=True)
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)[0]
    results = [papers[hit["corpus_id"]] for hit in hits]
    return results
