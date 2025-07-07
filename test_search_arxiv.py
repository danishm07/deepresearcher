from backend.mcp.agents import search_arxiv_plugin

plugin_result = search_arxiv_plugin({"query": "ai in space"})
print(type(plugin_result))
print(f"Returned {len(plugin_result)} papers" if isinstance(plugin_result, list) else plugin_result)
