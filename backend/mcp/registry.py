#yaml allows for users and developers to create their own custom rules and policies
#registry refers to the collection of these rules and policies, which along with the mcp agent, can be used to ecreate custom workflows
#this registry also gives us flexibility to add new agents, tools, and workflows in the future
from backend.mcp.plugin_registry import PLUGIN_REGISTRY, register_plugin
import yaml 
#from backend.search.arxiv_search import search_arxiv
#from backend.search.semantic_scholar_search import search_semantic_scholar
#from backend.agents.summarizer_agent import summarize_text
#from backend.tools.dataset_extractor import extract_dataset_mentions, extract_github_links, build_dataset_card
#from backend.database.memory import search_papers, store_paper
#from backend.mcp.agents import (
    #load_saved_papers,
    #mcp_chat_single_paper,)

import os
from backend.mcp import agents
import backend.mcp.agents 


def load_yaml_workflow(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def execute_workflow(agent_yaml, inputs):
    steps = agent_yaml.get("steps", [])

    if not isinstance(inputs, dict):
        raise ValueError("inputs must be a dictionary with 'query' and optionally 'context'.")

    input_data = inputs
    print(f"🚀 Starting workflow: {agent_yaml.get('name', 'Unnamed Agent')}")
    print(f"📝 Initial input: {input_data}")

    for step_name in steps:
        if step_name not in PLUGIN_REGISTRY:
            raise ValueError(f"Step '{step_name}' not found in PLUGIN_REGISTRY.")

        plugin_func = PLUGIN_REGISTRY[step_name]
        print(f"\n➡️ Running step: {step_name} with input type: {type(input_data)}")

        try:
            input_data = plugin_func(input_data)
            print(f"✅ Step '{step_name}' output type: {type(input_data)}")
        except Exception as e:
            print(f"❌ Error in step '{step_name}': {e}")
            raise e

    print("\n🎯 Final result of workflow:", input_data)
    return input_data

print("📦 Registered Plugins:", list(PLUGIN_REGISTRY.keys()))