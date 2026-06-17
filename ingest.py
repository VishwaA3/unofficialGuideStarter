import os

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({"source": filename, "text": text})
    return documents

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_chunks(documents): 
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 0:
                all_chunks.append({
                    "source": doc["source"],
                    "chunk_index": i,
                    "text": chunk.strip()
                })
    return all_chunks

if __name__ == "__main__":
    documents = load_documents("sources")
    print(f"Loaded {len(documents)} documents")
    
    all_chunks = build_chunks(documents)
    print(f"Total chunks: {len(all_chunks)}")
    
    print("\n--- 5 Sample Chunks ---\n")
    for chunk in all_chunks[:5]:
        print(f"Source: {chunk['source']}")
        print(f"Index: {chunk['chunk_index']}")
        print(f"Text: {chunk['text']}")
        print(f"Length: {len(chunk['text'])} characters")
        print("-" * 40)