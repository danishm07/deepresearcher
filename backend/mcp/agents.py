import json
from backend.agents.chat_single_paper import run_conversational_agent
from backend.agents.summarizer_agent import summarize_text
from backend.tools.dataset_extractor import extract_dataset_mentions, extract_github_links, build_dataset_card
from backend.database.memory import store_paper
from backend.mcp.plugin_registry import register_plugin
from backend.search.arxiv_search import search_arxiv
from backend.agents.chat_single_paper import chat_single_paper_plugin


STORAGE_PATH = "frontend/storage.json"

@register_plugin("load_saved_papers")
def load_saved_papers(input_data):
    # Simply loads saved papers, ignoring input_data
    with open(STORAGE_PATH, "r") as f:
        papers = json.load(f)
    # Return papers in a dict as expected by next step
    return papers

@register_plugin("search_arxiv")
def search_arxiv_plugin(input_data):
    query = input_data.get("query", "")
    results = search_arxiv(query)
    print(f"[search_arxiv_plugin] Query: {query} → {len(results)} results")
    return results

@register_plugin("summarize_and_extract")
def summarize_and_extract(input_data):
    print(f"[summarize_and_extract] Type of input: {type(input_data)}")
    if isinstance(input_data, dict):
        # If accidentally passed a single paper dict, wrap it
        papers = [input_data]
    else:
        papers = input_data  # assume it's a list of paper dicts

    results = []
    for paper in papers:
        summary = summarize_text(paper.get("summary", ""))
        mentions = extract_dataset_mentions(paper.get("summary", ""))
        github_links = extract_github_links(paper.get("summary", ""))
        dataset_cards = build_dataset_card(mentions, github_links)

        store_paper(paper.get("id", "unknown"), {
            "title": paper.get("title", ""),
            "summary": summary,
            "source": paper.get("source", "unknown"),
            "source_url": paper.get("url", None),
            "authors": paper.get("authors", [])
        })

        results.append({
            "id": paper.get("id", paper.get("url", "unknown_id")), 
            "title": paper.get("title", ""),
            "summary": summary,
            "datasets": dataset_cards,
            "source_url": paper.get("url", None),
            "authors": paper.get("authors", [])
        })
    print(f"[summarize_and_extract] Returning {len(results)} summarized papers")
    return {"papers": results} 
# Register chat_single_paper plugin in registry

@register_plugin("chat_single_paper")
def chat_single_paper_plugin(input_data):
    query = input_data.get("query", "")
    context_dict = input_data.get("context", {})
    context_text = context_dict.get("full_text") or context_dict.get("summary", "")

    print(f"[chat_single_paper] Query: {query}")
    print(f"[chat_single_paper] Context (preview): {context_text[:100]}...")

    result = run_conversational_agent(context_text, query)

    print(f"[chat_single_paper] Answer: {result}")

    return {
        "result": result
    }
