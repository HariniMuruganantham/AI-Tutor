import streamlit as st
import os
import base64
from datetime import datetime

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in environment variables.")
    st.stop()

# --------------------------------------------------
# Initialize LLM (Groq)
# --------------------------------------------------
llm = init_chat_model(
    "llama-3.1-8b-instant",
    model_provider="groq"
)

# --------------------------------------------------
# Prompt Template
# --------------------------------------------------
prompt = PromptTemplate.from_template(
    """
You are an expert curriculum designer and technical educator.
Your task is to create a detailed learning roadmap for the domain: {domain}.

Generate a comprehensive, topic-based (not time-based) roadmap that progresses
from absolute basics to advanced expert level.

Format the roadmap with:

# 🚀 [Domain] Learning Roadmap

## 📚 Foundation Level
🔹 **Topic 1**:
   - Key concepts
   - Practical applications
   - Resources (books/courses)

🔹 **Topic 2**:
   - Key concepts
   - Practical applications
   - Resources

## 🏗️ Intermediate Level
🔸 **Topic 1**:
   - Key concepts
   - Practical applications
   - Resources

## 🎯 Advanced Level
🔺 **Topic 1**:
   - Key concepts
   - Practical applications
   - Resources

## 🏫 Expert Level
🌟 **Topic 1**:
   - Key concepts
   - Practical applications
   - Resources

Include emojis to make it visually appealing and use clear section headers.
"""
)

# --------------------------------------------------
# Core logic
# --------------------------------------------------
def generate_roadmap(domain: str) -> str:
    chain = prompt | llm
    response = chain.invoke({"domain": domain})
    return response.content


def create_download_link(val: bytes, filename: str) -> str:
    b64 = base64.b64encode(val).decode()
    return (
        f'<a href="data:application/octet-stream;base64,{b64}" '
        f'download="{filename}.pdf">Download PDF</a>'
    )

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
def main():
    st.title("🧭 Roadmap Generator")
    st.write(
        "Enter your domain of interest to generate a detailed, "
        "topic-based learning roadmap with emoji-enhanced markdown."
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        domain = st.text_input(
            "Enter your domain of interest:",
            placeholder="Data Science, Cybersecurity, Digital Marketing..."
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button(
            "✨ Generate Roadmap",
            use_container_width=True
        )

    if generate_btn:
        if not domain:
            st.warning("⚠️ Please enter a domain or topic of interest.")
            return

        with st.spinner(f"🚀 Generating {domain} roadmap..."):
            try:
                roadmap = generate_roadmap(domain)

                st.success("✅ Roadmap generated successfully!")
                st.markdown("---")

                with st.expander("📝 View Roadmap", expanded=True):
                    st.markdown(roadmap)

                st.download_button(
                    label="📥 Download Markdown",
                    data=roadmap,
                    file_name=f"{domain.lower().replace(' ', '_')}_roadmap.md",
                    mime="text/markdown"
                )

                st.markdown("---")
                st.markdown(
                    f"**🗓️ Generated on**: "
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# --------------------------------------------------
# Run app
# --------------------------------------------------
main()
