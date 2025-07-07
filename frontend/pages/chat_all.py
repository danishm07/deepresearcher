"""""

import streamlit as st
from ...backend.agents.conversational_agent import ask_question

st.title("🧠 Research Chat Agent")
st.markdown("Ask a question based on your saved research papers.")

query = st.text_input("Ask a question:")
if query:
    with st.spinner("Thinking..."):
        response = ask_question(query)
        st.markdown(response)
"""""