import os
import requests
from dotenv import load_dotenv
from tools.semantic_context_retriever import find_relevant_passages

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_TOKEN")
HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  

def ask_question(question):
    relevant_papers = find_relevant_passages(question)

    context_blocks = []
    for paper in relevant_papers:
        context_blocks.append(f"Title: {paper['title']}\nSummary: {paper['summary']}")

    context = "\n\n".join(context_blocks)
    prompt = f"""
You are a helpful assistant. Based on the following paper summaries, answer the user's question and cite relevant paper titles.

---CONTEXT---
{context}

---QUESTION---
{question}

Answer:
"""

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 300
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]['generated_text'].split("Answer:")[-1].strip()
    else:
        return f"❌ Error: {response.status_code} — {response.text}"