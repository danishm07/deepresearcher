from transformers import pipeline

#here we're using the Huggingface transformers library to load a pre-trained summarization model
#we'll use this with hf code agents, which are code agents that automatically generate code based on natural language prompts
#kinda sicks

#loading up the summarization pipeline
#once loaded, this can be reused to summarize text
from backend.mcp.plugin_registry import register_plugin

summarizer = pipeline("summarization", model="google/pegasus-xsum")

def summarize_text(text, max_length=128, min_length=30):
    if not text or not text.strip():
        return "No summary available."
    try:
        result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {str(e)}"

@register_plugin("summarize_text")
def summarize_text_plugin(input_data):
    text = input_data.get("context", {}).get("full_text", "")
    summary = summarize_text(text)
    input_data["context"]["summary"] = summary
    return input_data
