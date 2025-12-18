import streamlit as st

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="AI Tutor | Learning Companion",
    page_icon="🎓",
    layout="wide"
)

# -------------------- Header Section --------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            color: #2E86C1;
            text-align: center;
        }
        .sub-title {
            font-size: 1.2rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-box {
            padding: 1.5rem;
            border-radius: 12px;
            background-color: #F4F6F7;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
            height: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🎓 Learning Companion</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Your AI-powered tutor for smart learning, testing, and career roadmaps</div>',
    unsafe_allow_html=True
)

# -------------------- Intro Section --------------------
st.markdown(
    """
    **Learning Companion** is an intelligent AI tutor built using **RAG, FAISS, Hugging Face, and Groq**.
    It helps you understand content deeply by summarizing, testing, answering questions,
    and guiding you with structured learning roadmaps.
    """
)

st.divider()

# -------------------- Features Section --------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-box">
        <h4>📘 Summarization</h4>
        <p>Generate topic-based summaries from books, PDFs, and notes using semantic search.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-box">
        <h4>📝 Test Generator</h4>
        <p>Automatically create quizzes and evaluate answers with AI-driven feedback.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-box">
        <h4>❓ Q&A Assistant</h4>
        <p>Ask questions from your learning material using RAG-based retrieval.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="feature-box">
        <h4>🗺️ Roadmaps</h4>
        <p>Get field-based learning roadmaps for careers in tech and AI.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------- Navigation Hint --------------------
st.divider()
st.info(
    "👉 Use the **sidebar** to navigate between Summarizer, Q&A, Test Generator, and Roadmap modules.",
    icon="ℹ️"
)

# -------------------- Footer --------------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray;">
        Built by Harini • Powered by RAG, FAISS, Hugging Face & Groq
    </p>
    """,
    unsafe_allow_html=True
)
