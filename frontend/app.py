import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Deep Research Bot", page_icon="🧠")

BACKEND_URL = "http://localhost:8000/run-agent"
STORAGE_PATH = "frontend/storage.json"

def load_saved():
    if os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH) as f:
            return json.load(f)
    return 

def save_to_storage(data):
    with open(STORAGE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

st.title("Alexandria - Research Agent 🥀")
st.write("Search papers, extract datasets, and organize your research.")

# Ensure state is initialized
if "results" not in st.session_state:
    st.session_state.results = []

query = st.text_input("Enter a research query")
agent_name = st.selectbox("Choose an agent", ["example_agent", "chat_single_paper"])

if st.button("Run Agent") and query:
    with st.spinner("Running agent..."):
        response = requests.post(BACKEND_URL, json={"query": query, "agent_name": agent_name})
        raw_results = response.json()["results"]
        st.write("🔍 Raw results:", raw_results)


        if isinstance(raw_results, dict) and "papers" in raw_results:
            st.session_state.results = raw_results["papers"]
            st.write(f"Found {len(st.session_state.results)} papers.")
        else:
            st.session_state.results = raw_results
            st.write("No papers found or unexpected response format.")

# Display results
if st.session_state.results:
    bookmarks = load_saved() or []

    for r in st.session_state.results:
        with st.expander(f"📄 {r['title']}", expanded=True):
            st.markdown(f"**Summary**: {r['summary']}")
            st.write("---")
            st.markdown("### 📦 Datasets")
            for d in r['datasets']:
                st.info(f"**{d['dataset_name']}**\n_{d['example_context']}_")
                for url in d['github_repos']:
                    st.markdown(f"- [GitHub Repo]({url})")

            # Save button
            if st.button(f"🔖 Save {r['title']}", key=f"bookmark_{r['title']}"):
                if not any(b["title"] == r["title"] for b in bookmarks):
                    bookmarks.append(r)
                    save_to_storage(bookmarks)
                    st.success("Saved!")
