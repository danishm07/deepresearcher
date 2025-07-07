import streamlit as st
import requests
import json

st.set_page_config(layout="centered")
st.title("🧠 Chat About a Paper")

with open("frontend/storage.json") as f:
    papers = json.load(f)

paper_map = {paper["title"]: paper for paper in papers}
selected_title = st.selectbox("Choose a paper", list(paper_map.keys()))
selected_paper = paper_map[selected_title]

question = st.chat_input("Ask something about this paper...")
if question:
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:8000/run-agent",
            json={
                "agent_name": "chat_single_paper",
                "query": question,
                "context": {
                    "title": selected_paper["title"],
                    "summary": selected_paper["summary"],
                    "full_text": selected_paper.get("full_text", "")
                },
            },
        )

        if response.status_code == 200:
            st.markdown("### 💬 Answer")
            answer = response.json().get("results", {}).get("result")
            print(f"🔍 Raw response: {response.json()}")
            if answer:
                st.write(answer)
            else:
                st.write("❌ No answer returned.")
