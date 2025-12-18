# AI Tutor – Intelligent Learning Assistant

## Overview

**AI Tutor** is an AI-powered learning platform designed to help users **learn faster and smarter** by interacting with educational content. The system can **summarize content**, **generate tests**, **answer questions**, and **create field-based learning roadmaps** using modern **Generative AI** techniques.

The project leverages **Retrieval-Augmented Generation (RAG)** with a **vector database (FAISS)** to ensure accurate, context-aware responses from large language models.

---

## Core Features

### 1. Topic-Based Summarization

* Upload or provide learning material (books, notes, documents)
* Generates **concise summaries** for specific topics
* Uses semantic search to extract only relevant sections

### 2. Test Generator & Evaluation

* Automatically generates quizzes and tests from learning content
* Supports MCQs and descriptive questions
* Evaluates user answers and provides:

  * Scores
  * Correct answers
  * Improvement suggestions

### 3. Question Answering (Q&A)

* Ask questions directly from uploaded content
* Answers are generated using **RAG** to avoid hallucinations
* Context is retrieved from the vector database before response generation

### 4. Field-Based Roadmap Generator

* Generates structured learning roadmaps for domains such as:

  * Software Development
  * DevOps / Cloud
  * Data Science
  * AI / Machine Learning
* Includes:

  * Step-by-step learning paths
  * Core concepts
  * Resource recommendations

---

## System Architecture

```
User Input
   ↓
Document Loader
   ↓
Text Chunking
   ↓
Embeddings (Hugging Face)
   ↓
Vector Store (FAISS)
   ↓
Retriever
   ↓
LLM (Groq)
   ↓
Final Response
```

---

## Tech Stack

### AI & ML

* **Retrieval-Augmented Generation (RAG)**
* **Hugging Face** – embeddings and NLP models
* **Groq** – fast LLM inference
* **FAISS** – vector database for semantic search

### Backend

* Python
* LangChain (for RAG pipeline orchestration)

### Development Tools

* Visual Studio Code
* Git & GitHub
* **Streamlit** – interactive web UI for user interaction

---

## Project Structure

```
AI-Tutor/
├── app.py                 # Streamlit application entry point
├── pages/
│   ├── summarizer.py      # Topic-based summarization logic
│   ├── test_generator.py  # Test generation & evaluation
│   ├── qa_engine.py       # RAG-based Q&A system
│   └── roadmap.py         # Field-based roadmap generator
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Tutor
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set the following environment variables:

* `GROQ_API_KEY`
* `HUGGINGFACE_API_TOKEN`

### 5. Run the Application (Streamlit)

```bash
streamlit run app.py
```

## How It Works

* Documents are split into semantic chunks
* Chunks are converted into embeddings using Hugging Face models
* Embeddings are stored in FAISS for fast similarity search
* Relevant context is retrieved for each query
* Groq LLM generates accurate, grounded responses

---

## Use Cases

* Students preparing for exams
* Self-learners exploring new domains
* Educators creating tests and summaries
* Career-focused learners needing structured roadmaps

---

## Future Enhancements

* Web-based frontend (React / Streamlit)
* User authentication
* Progress tracking
* Multi-language support
* Cloud deployment

---

## Author

**Harini**

---

## Note

This project is actively evolving and serves as a hands-on implementation of modern AI-powered education systems using free and open-source tools.
