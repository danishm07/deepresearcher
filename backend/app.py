from search.arxiv_search import search_arxiv
from search.semantic_scholar_search import search_semantic_scholar

from agents.summarizer_agent import summarize_text

from database.memory import search_papers, store_paper

from tools.dataset_extractor import extract_dataset_mentions, extract_github_links, build_dataset_card
#calling the search functions from the arxiv_search and semantic_scholar_search modules

from mcp.agents import summarize_and_extract

if __name__ == "__main__":
    query = input("Enter a research topic: ")

    print("\nFetching from arXiv...\n")
    arxiv_papers = search_arxiv(query)
    for i, paper in enumerate(arxiv_papers):
        paper['source'] = 'arXiv'
        result = summarize_and_extract(f"arxiv-{i}", paper)
        print(f"Title: {result['title']}\nSummary: {result['summary']}")
        if result['datasets']:
            print("📦 Datasets Found:")
            for card in result['datasets']:
                print(f"- {card['dataset_name']} (via: {card['example_context']})")

    print("\nFetching from Semantic Scholar...\n")
    semscholar_papers = search_semantic_scholar(query)
    for i, paper in enumerate(semscholar_papers):
        paper['source'] = 'SemanticScholar'
        result = summarize_and_extract(f"sem-{i}", paper)
        print(f"Title: {result['title']}\nSummary: {result['summary']}")
        if result['datasets']:
            print("📦 Datasets Found:")
            for card in result['datasets']:
                print(f"- {card['dataset_name']} (via: {card['example_context']})")

    print("\nSemantic Search — Ask a follow-up:\n")
    followup = input("Search for something related: ")
    hits = search_papers(followup)
    for result, meta in zip(hits['documents'][0], hits['metadatas'][0]):
        print(f"\n🔎 Title: {meta['title']}\n📝 Summary: {result}\n📚 Source: {meta['source']}")