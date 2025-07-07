import arxiv
#basicallly using the arxiv python package to search for papers
#arxiv is a repo of research papers in computer science, physics, mathematics, and more
def search_arxiv(query, max_results=5):
    print(f"🔎 Searching arXiv for: {query}")
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []
    for result in search.results():
        paper_id = result.entry_id.split('/')[-1] 
        results.append({
            "id": paper_id,
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": result.published.strftime("%Y-%m-%d"),
            "primary_category": result.primary_category,
            "pdf_url": result.pdf_url,  
            "url": f"https://arxiv.org/abs/{paper_id}"  
        })
   
    print(f"✅ Found {len(results)} results")
    return results

