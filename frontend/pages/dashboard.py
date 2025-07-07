import streamlit as st
import json
import os

st.set_page_config(page_title="Saved Papers Dashboard", page_icon="📚")

STORAGE_PATH = "frontend/storage.json"

st.set_page_config(layout="wide")
st.title("📚 Saved Research Papers Dashboard")

# Load saved papers from local JSON
if os.path.exists(STORAGE_PATH):
    with open(STORAGE_PATH) as f:
        saved = json.load(f)
else:
    st.warning("No saved papers found yet.")
    st.stop()

all_tags = set()
for paper in saved:
    tags = paper.get("tags", [])
    if isinstance(tags, list):
        all_tags.update(tags)


selected_tag = st.sidebar.selectbox("Filter by Tag", ["All"] + sorted(all_tags))

# Display in grid format
cols = st.columns(2)
i = 0
updated_saved = []
for paper in saved:
    tags = paper.get("tags", [])
    if selected_tag != "All" and selected_tag not in tags:
        updated_saved.append(paper)
        continue

    with cols[i % 2]:
        st.markdown("---")
        st.subheader(f"📄 {paper['title']}")
        st.markdown(f"**Summary**: {paper['summary']}")

        if 'authors' in paper:
            st.markdown(f"👥 **Authors**: {paper['authors']}")

        if 'source_url' in paper and paper['source_url']:
            st.markdown(f"[🔗 View Original Paper]({paper['source_url']})", unsafe_allow_html=False)

        if paper.get("datasets"):
            if paper["datasets"]:
                st.markdown("### 📦 Datasets")
                for ds in paper["datasets"]:
                    st.markdown(f"- **{ds['dataset_name']}**: _{ds['example_context']}_")
                    for gh in ds.get("github_repos", []):
                        st.markdown(f"  - [🐙 GitHub Link]({gh})", unsafe_allow_html=False)
            else:
                st.markdown("❌ No datasets found.")

        # Tags input
        unique_tag_key = f"tags_{paper['id']}_{i}"
        new_tags = st.text_input(
            f"Add tags (comma separated) for {paper['title']}",
            ", ".join(tags),
            key=unique_tag_key
        )
        paper['tags'] = [tag.strip() for tag in new_tags.split(",") if tag.strip()]
        

        # Delete button
        if st.button(f"🗑️ Delete", key=f"delete_{paper['id']}"):
            continue  # Skip saving this paper (i.e., delete it)

        updated_saved.append(paper)
    i += 1

# Save updates
with open(STORAGE_PATH, "w") as f:
    json.dump(updated_saved, f, indent=2)

