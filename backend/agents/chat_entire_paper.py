import os
from backend.mcp.plugin_registry import register_plugin
from dotenv import load_dotenv
load_dotenv()
from huggingface_hub import InferenceClient

@register_plugin("chat_entire_paper")
def chat_entire_paper_plugin(input_data):
    query = input_data.get("query", "")
    context = input_data.get("context", {})
    paper_text = context.get("full_text") or context.get("summary", "")
    vernacular = input_data.get("vernacular", False)

    prompt = f"Explain in simple terms: {query}" if vernacular else query
    user_message = f"Context:\n{paper_text}\n\nQuestion: {prompt}"

    client = InferenceClient(
        provider="together",
        api_key=os.environ["HF_TOKEN"],
    )

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"❌ Could not generate an answer. API error: {str(e)}"

    context["answer"] = answer
    return {
        "query": query,
        "context": context
    }
