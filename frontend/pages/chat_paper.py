import streamlit as st
import requests
import json

# 📄 Load stored papers
with open("frontend/storage.json") as f:
    papers = json.load(f)

# 🧭 Choose paper
st.set_page_config(layout="wide")
st.title("🧠 Chat With an Entire Paper")

paper_map = {paper["title"]: paper for paper in papers}
selected_title = st.selectbox("📘 Choose a paper", list(paper_map.keys()))
selected_paper = paper_map[selected_title]

# 🛠️ App layout
col1, col2 = st.columns([2, 3])

if not selected_paper.get("full_text") and selected_paper.get("pdf_path"):
    try:
        full_text = extract_text_from_pdf(selected_paper["pdf_path"])
        selected_paper["full_text"] = full_text

        # Save updated papers to storage.json
        with open("frontend/storage.json", "w") as f:
            json.dump(papers, f, indent=2)
        st.success("✅ Full text extracted from PDF!")
    except Exception as e:
        st.warning(f"⚠️ Failed to extract PDF text: {e}")

# 🧠 Vernacular toggle
with col1:
    st.subheader("💬 Chat")
    vernacular_mode = st.toggle("Simplify Responses (Vernacular Mode)", value=False)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for entry in st.session_state.chat_history:
        st.chat_message("user").write(entry["user"])
        st.chat_message("assistant").write(entry["assistant"])

    question = st.chat_input("Ask something about this paper...")
    if question:
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://localhost:8000/run-agent",
                json={
                    "agent_name": "chat_entire_paper",
                    "query": question,
                    "vernacular": vernacular_mode,
                    "context": {
                        "title": selected_paper["title"],
                        "summary": selected_paper.get("summary", ""),
                        "full_text": selected_paper.get("full_text", "")
                    },
                },
            )

            if response.status_code == 200:
                data = response.json()
                result = data["results"]["context"].get("answer", "❌ No answer returned.")
                st.chat_message("user").write(question)
                st.chat_message("assistant").write(result)

                st.session_state.chat_history.append({
                    "user": question,
                    "assistant": result
                })
            else:
                st.error("❌ Agent failed to respond.")

# 📑 Paper display
with col2:
    st.subheader("📄 Paper Viewer")
    st.markdown("You are chatting with the full content of this paper:")
    st.text_area(
        label="Full Text of the Paper",
        value=selected_paper.get("full_text", "⚠️ No full_text found. Did you parse the PDF?"),
        height=600,
        disabled=True
    )
