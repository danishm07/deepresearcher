#using chromadb, a vector database, to store embeddings, which will be used to search for similar documents

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

#initializing the chroma db client, or the vector databse
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("papers")

#to either create or collect a collection
#in this case collections are documents
collection = client.get_or_create_collection("papers")

#loading up the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#this model will be used to convert text to embeddings
#embeddings can be used to search for similar documents, in our case papers

def embed_text(text):
    return embedding_model.encode([text])[0]

def store_paper(paper_id, metadata):
    embedding = embed_text(metadata["summary"])
    # Safely join authors list if it exists
    if "authors" in metadata and isinstance(metadata["authors"], list):
        metadata["authors"] = ", ".join(metadata["authors"])

    collection.add(
        documents=[metadata["summary"]],
        embeddings=[embedding],
        ids=[paper_id],
        metadatas=[metadata]
    )


def search_papers(query, k=3):
    embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=k
    )
    return results

