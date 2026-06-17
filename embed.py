from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_documents, build_chunks

def embed_and_store(all_chunks):
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it already exists (for re-runs)
    try:
        client.delete_collection("njit_guide")
    except:
        pass
    
    collection = client.create_collection("njit_guide")
    
    print(f"Embedding {len(all_chunks)} chunks...")
    texts = [chunk["text"] for chunk in all_chunks]
    sources = [chunk["source"] for chunk in all_chunks]
    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    
    embeddings = model.encode(texts, show_progress_bar=True)
    
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )
    
    print(f"Stored {len(all_chunks)} chunks in ChromaDB!")
    return collection, model

def retrieve(query, collection, model, k=4):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    documents = load_documents("sources")
    all_chunks = build_chunks(documents)
    collection, model = embed_and_store(all_chunks)
    
    print("\n--- Testing Retrieval ---\n")
    test_queries = [
        "What are free parking options near NJIT?",
        "How do disability accommodations work at NJIT?",
        "What food places near NJIT have student discounts?"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        results = retrieve(query, collection, model)
        for r in results:
            print(f"  Source: {r['source']} | Distance: {r['distance']:.3f}")
            print(f"  Text: {r['text'][:150]}...")
            print()