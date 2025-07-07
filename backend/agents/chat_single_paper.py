"""""

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
client = InferenceClient(token=os.getenv("HUGGINGFACE_API_TOKEN"))

def chat_about_paper(paper, question):
    context = f"Title: {paper['title']}\nSummary: {paper['summary']}"
    prompt = f"""
#You are an expert research assistant. Answer questions using only this paper.

#---PAPER---
#{context}

#---QUESTION---
#{question}

#Answer:
"""

    response = client.text_generation(
        prompt,
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",  
        max_new_tokens=300,
        temperature=0.7
    )

    return response.strip()
"""""


from transformers import pipeline
from backend.mcp.plugin_registry import register_plugin

qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def run_conversational_agent(context: str, query: str) -> str:
    if not context.strip():
        return "No context available to answer the question."

    try:
        result = qa_pipeline({
            "context": context,
            "question": query
        })
        return result["answer"]
    except Exception as e:
        return f"Error while answering: {str(e)}"

@register_plugin("chat_single_paper")
def chat_single_paper_plugin(input_data):
    query = input_data.get("query", "")
    context_dict = input_data.get("context", {})
    context_text = context_dict.get("full_text") or context_dict.get("summary", "")
    result = run_conversational_agent(context_text, query)
    return {"result": result}
