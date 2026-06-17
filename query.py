import os
from groq import Groq
from dotenv import load_dotenv
from embed import embed_and_store, retrieve
from ingest import load_documents, build_chunks

load_dotenv()

def build_system_prompt():
    return """You are a helpful assistant for incoming NJIT freshmen.
Answer questions using ONLY the information provided in the context below.
If the context does not contain enough information to answer the question, 
say "I don't have enough information on that in my documents."
Always end your response with a "Sources:" section listing the document names you used.
Do not make up information or use outside knowledge."""

def ask(question, collection, model):
    chunks = retrieve(question, collection, model, k=4)
    
    context = ""
    sources = []
    for chunk in chunks:
        context += chunk["text"] + "\n\n"
        if chunk["source"] not in sources:
            sources.append(chunk["source"])
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    
    answer = response.choices[0].message.content
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    print("Loading documents and building vector store...")
    documents = load_documents("sources")
    all_chunks = build_chunks(documents)
    collection, model = embed_and_store(all_chunks)
    
    print("\nReady! Testing with sample questions...\n")
    
    test_questions = [
        "What are free parking options near NJIT?",
        "What is the weather like on Mars?",
    ]
    
    for question in test_questions:
        print(f"Question: {question}")
        result = ask(question, collection, model)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 50)