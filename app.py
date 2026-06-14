import os
import streamlit as st
from dotenv import load_dotenv
from rag_engine import RAGEngine
from vector_store import load_vector_store

# --- PAGE CONFIG ---
st.set_page_config(page_title="CampusFlow", layout="centered")
st.title("🤖 CampusFlow – Your own campus assisstant")
st.markdown("Hello and Greetings of the day!")

# --- ENV VARS ---
load_dotenv()

# --- INIT RAG ---
if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine(load_vector_store("faiss_index"))

# --- SESSION STATE DEFAULTS ---
st.session_state.setdefault("query", "")
st.session_state.setdefault("response", "")
st.session_state.setdefault("follow_ups", [])
st.session_state.setdefault("input_text", "")

# --- UI ---
col1, col2 = st.columns([5, 1])

with col1:
    input_text = st.text_input(
        label="Ask your query",
        value=st.session_state.input_text,
        placeholder="Type your query and press Enter...",
        label_visibility="collapsed",
        key="input_text"
    )

with col2:
    if st.button("❌ Clear", use_container_width=True):
        # Clear variables & rerun
        for key in ["query", "response", "follow_ups", "input_text"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- HANDLE INPUT ON ENTER ---
if input_text and input_text != st.session_state.query:
    st.session_state.query = input_text

    with st.spinner("Generating answer..."):
        response = st.session_state.rag.query(input_text)

        if "💬 Follow-up suggestion:" in response:
            main_answer, follow_up_text = response.split("💬 Follow-up suggestion:", 1)
            follow_ups = [line.strip(" 1234567890.-•") for line in follow_up_text.strip().split("\n") if line.strip()]
        else:
            main_answer = response
            follow_ups = []

        st.session_state.response = main_answer
        st.session_state.follow_ups = follow_ups

# --- OUTPUT ---
if st.session_state.response:
    st.markdown("### 🤖 Answer:")
    st.markdown(st.session_state.response)

# --- FOLLOW-UP AS TEXT (embedded above in markdown) ---
if st.session_state.follow_ups:
    st.markdown("### 💬 Follow-up suggestions:")
    for follow_up in st.session_state.follow_ups:
        st.markdown(f"- {follow_up}")
