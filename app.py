import gradio as gr
from embed import embed_and_store, retrieve
from ingest import load_documents, build_chunks
from query import ask

print("Loading documents and building vector store...")
documents = load_documents("sources")
all_chunks = build_chunks(documents)
collection, model = embed_and_store(all_chunks)
print("Ready!")

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question, collection, model)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks() as demo:
    gr.Markdown("# NJIT Unofficial Freshman Guide")
    gr.Markdown("Ask anything about surviving freshman year at NJIT!")
    inp = gr.Textbox(label="Your question", placeholder="e.g. Where can I park for free near NJIT?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=3)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()