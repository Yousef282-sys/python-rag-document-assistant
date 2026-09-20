import os
from api_client import ask_question
import streamlit as st



st.set_page_config(
    page_title="PyDocs AI",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background: #0b1120;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #243044;
    }

    .brand {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 28px;
    }

    .hero {
        text-align: center;
        padding: 55px 20px 25px 20px;
    }

    .hero-icon {
        font-size: 54px;
        margin-bottom: 10px;
    }

    .hero h1 {
        color: #f8fafc;
        font-size: 38px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #94a3b8;
        font-size: 16px;
    }

    .source-card {
        background: #172033;
        border: 1px solid #29364d;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #cbd5e1;
        font-size: 13px;
    }

    .info-card {
        background: #172033;
        border: 1px solid #29364d;
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
    }

    .info-title {
        color: #f8fafc;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .info-text {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.5;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 14px;
    }

    .stButton button {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="brand">?? PyDocs AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Python Documentation Assistant</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ?? Knowledge Base")
    st.markdown(
        '<div class="info-card">'
        '<div class="info-title">Official Python Tutorial</div>'
        '<div class="info-text">Answers are grounded in the provided Python documentation.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ?? System")
    st.caption("Embedding: all-MiniLM-L6-v2")
    st.caption("Vector DB: ChromaDB")
    st.caption("LLM: Qwen3 4B")


if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.messages:
    st.markdown(
        '<div class="hero">'
        '<div class="hero-icon">??</div>'
        '<h1>Python Documentation Assistant</h1>'
        '<p>Ask questions and get answers grounded in the official Python tutorial.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ?? Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("What is a Python dictionary?")

    with col2:
        st.info("How does a for loop work?")

    with col3:
        st.info("How do I handle exceptions?")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            st.markdown("**?? Sources**")
            for source in message["sources"]:
                st.markdown(
                    f'<div class="source-card">?? {source}</div>',
                    unsafe_allow_html=True,
                )


question = st.chat_input("Ask something about Python...")


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("?? Searching the Python documentation..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/query",
                    json={"question": question},
                    timeout=180,
                )
                response.raise_for_status()

                data = response.json()
                answer = data.get("answer", "")
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:
                    st.markdown("**?? Sources**")
                    for source in sources:
                        st.markdown(
                            f'<div class="source-card">?? {source}</div>',
                            unsafe_allow_html=True,
                        )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception as exc:
                error_message = (
                    "?? I couldn't connect to the backend. "
                    "Make sure the FastAPI server is running."
                )
                st.error(error_message)
                st.caption(str(exc))

