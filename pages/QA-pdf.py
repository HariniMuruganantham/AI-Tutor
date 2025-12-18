import streamlit as st
import os
from uuid import uuid4
from PyPDF2 import PdfReader
from typing_extensions import List, TypedDict, Annotated

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

from langgraph.graph import StateGraph

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in environment variables.")
    st.stop()

# --------------------------------------------------
# Streamlit session state
# --------------------------------------------------
if "success" not in st.session_state:
    st.session_state.success = False

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# --------------------------------------------------
# LLM initialization (Groq)
# --------------------------------------------------
llm = init_chat_model(
    "llama-3.1-8b-instant",
    model_provider="groq"
)

# --------------------------------------------------
# Prompt template
# --------------------------------------------------
template = """
Use the following pieces of context to answer the question at the end.
If you don't know the answer, say that you don't know. Do not make up answers.

{context}

Question: {question}

Helpful Answer:
"""

prompt = PromptTemplate.from_template(template)

# --------------------------------------------------
# Embeddings
# --------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --------------------------------------------------
# PDF processing helpers
# --------------------------------------------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        add_start_index=True
    )
    return splitter.split_text(text)


def get_retriever(text_chunks):
    index = faiss.IndexFlatL2(
        len(embeddings.embed_query("dimension check"))
    )

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )

    ids = [str(uuid4()) for _ in text_chunks]
    vector_store.add_texts(text_chunks, ids=ids)

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 1}
    )

# --------------------------------------------------
# LangGraph state definitions
# --------------------------------------------------
class Search(TypedDict):
    query: Annotated[str, ..., "Search query"]


class State(TypedDict):
    question: str
    query: Search
    context: List[Document]
    answer: str

# --------------------------------------------------
# Graph nodes
# --------------------------------------------------
def analyze_query(state: State):
    structured_llm = llm.with_structured_output(Search)
    query = structured_llm.invoke(state["question"])
    return {"query": query}


def retrieve(state: State):
    retrieved_docs = st.session_state.retriever.invoke(
        state["query"]["query"]
    )
    return {"context": retrieved_docs}


def generate(state: State):
    context_text = "\n\n".join(
        doc.page_content for doc in state["context"]
    )
    messages = prompt.invoke(
        {
            "question": state["question"],
            "context": context_text
        }
    )
    response = llm.invoke(messages)
    return {"answer": response.content}

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
def summary():
    st.title("📄 PDF Question Answering & Summarization")

    pdf_docs = st.file_uploader(
        "Upload PDF files",
        accept_multiple_files=True,
        type=["pdf"]
    )

    if st.button("Submit & Process") and pdf_docs:
        with st.spinner("Processing PDFs..."):
            raw_text = get_pdf_text(pdf_docs)
            chunks = get_text_chunks(raw_text)
            st.session_state.retriever = get_retriever(chunks)
            st.session_state.success = True
            st.success(
                f"Processed {len(pdf_docs)} PDF(s) into {len(chunks)} chunks"
            )

    if st.session_state.success:
        user_query = st.text_area("Enter your question")

        if user_query and st.button("Generate Answer"):
            with st.spinner("Generating answer..."):
                create_summary(user_query)

# --------------------------------------------------
# Graph execution
# --------------------------------------------------
def create_summary(topic):
    graph_builder = StateGraph(State)

    graph_builder.add_node("analyze_query", analyze_query)
    graph_builder.add_node("retrieve", retrieve)
    graph_builder.add_node("generate", generate)

    graph_builder.add_edge("analyze_query", "retrieve")
    graph_builder.add_edge("retrieve", "generate")
    graph_builder.set_entry_point("analyze_query")

    graph = graph_builder.compile()
    result = graph.invoke({"question": topic})

    st.subheader("Answer")
    st.write(result["answer"])

# --------------------------------------------------
# Run app
# --------------------------------------------------
summary()
