import requests
#now we're using another resource called Semantic Scholar
#Schemantic Scholar is a free, AI-powered research tool for scientific literature, developed at the Allen Institute for AI.

def search_semantic_scholar(query, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,abstract,authors,url,year,venue"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []

    data = response.json()
    papers = []
    for paper in data.get("data", []):
        papers.append({
            "title": paper["title"],
            "authors": [a["name"] for a in paper["authors"]],
            "summary": paper.get("abstract", "No abstract available."),
            "url": paper.get("url"),
            "year": paper.get("year"),
            "venue": paper.get("venue", "Unknown")
        })
    return papers