import streamlit as st
import os
import json
from typing import List, Dict

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in environment variables.")
    st.stop()

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "score" not in st.session_state:
    st.session_state.score = None

# --------------------------------------------------
# Initialize Embeddings & LLM
# --------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = init_chat_model(
    "llama-3.1-8b-instant",
    model_provider="groq"
)

# --------------------------------------------------
# PDF Processing
# --------------------------------------------------
def extract_text_from_pdfs(pdf_files):
    text = ""
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def split_text_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]


def create_vector_store(chunks):
    return FAISS.from_documents(chunks, embeddings)

# --------------------------------------------------
# Question Generation
# --------------------------------------------------
def generate_questions(topic: str, vector_store, num_questions: int = 10):
    docs = vector_store.similarity_search(topic, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = PromptTemplate.from_template(
        """
You are an expert quiz maker.

Generate {num_questions} multiple choice questions based on the context below.
Each question must have 4 options (a, b, c, d) and exactly one correct answer.

Return ONLY valid JSON in the following structure:

{
  "questions": [
    {
      "question": "question text",
      "options": {
        "a": "option a",
        "b": "option b",
        "c": "option c",
        "d": "option d"
      },
      "correct_answer": "a"
    }
  ]
}

Context:
{context}

Topic:
{topic}
"""
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "num_questions": num_questions,
            "context": context,
            "topic": topic,
        }
    )

    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        st.error("❌ Failed to parse quiz questions. Please try again.")
        return None

# --------------------------------------------------
# Quiz Display & Evaluation
# --------------------------------------------------
def display_quiz(questions_data):
    st.session_state.user_answers = {}

    for i, question in enumerate(questions_data["questions"], 1):
        st.write(f"**Question {i}:** {question['question']}")
        options = question["options"]

        st.session_state.user_answers[f"q{i}_correct"] = question["correct_answer"]

        user_answer = st.radio(
            f"Select your answer for Question {i}:",
            options=["a", "b", "c", "d"],
            key=f"q{i}",
            format_func=lambda x: f"{x}) {options[x]}",
        )

        st.session_state.user_answers[f"q{i}_user"] = user_answer
        st.write("---")


def evaluate_answers():
    correct = 0
    total = len(
        [k for k in st.session_state.user_answers if k.endswith("_correct")]
    )

    for i in range(1, total + 1):
        if (
            st.session_state.user_answers.get(f"q{i}_user")
            == st.session_state.user_answers.get(f"q{i}_correct")
        ):
            correct += 1

    score = (correct / total) * 100 if total > 0 else 0
    st.session_state.score = score
    return score

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
def main():
    st.title("📝 PDF Quiz Generator")
    st.write("Upload PDFs, choose a topic, and test your knowledge.")

    # Step 1: Upload PDFs
    with st.expander("Step 1: Upload PDF Files", expanded=True):
        pdf_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if pdf_files and st.button("Process PDFs"):
            with st.spinner("Processing PDFs..."):
                text = extract_text_from_pdfs(pdf_files)
                chunks = split_text_into_chunks(text)
                st.session_state.vector_store = create_vector_store(chunks)
                st.session_state.pdf_processed = True
                st.success("✅ PDFs processed successfully!")

    # Step 2: Generate Questions
    if st.session_state.pdf_processed:
        with st.expander("Step 2: Generate Questions", expanded=True):
            topic = st.text_input(
                "Enter a topic from the PDF:",
                placeholder="e.g., machine learning, operating systems",
            )

            if topic and st.button("Generate Quiz"):
                with st.spinner("Generating quiz..."):
                    questions_data = generate_questions(
                        topic, st.session_state.vector_store
                    )
                    if questions_data:
                        st.session_state.questions_data = questions_data
                        st.session_state.questions_generated = True
                        st.success("✅ Quiz generated successfully!")

    # Step 3: Take Quiz
    if st.session_state.questions_generated:
        with st.expander("Step 3: Take the Quiz", expanded=True):
            display_quiz(st.session_state.questions_data)

            if st.button("Submit Answers"):
                score = evaluate_answers()
                st.success(f"🎯 Your score: {score:.1f}%")

                st.write("### Correct Answers")
                for i, question in enumerate(
                    st.session_state.questions_data["questions"], 1
                ):
                    correct = st.session_state.user_answers[f"q{i}_correct"]
                    st.write(
                        f"Question {i}: {correct}) "
                        f"{question['options'][correct]}"
                    )

    # Reset
    if st.session_state.pdf_processed and st.button("Start Over"):
        st.session_state.clear()
        st.rerun()

# --------------------------------------------------
# Run App
# --------------------------------------------------
main()
