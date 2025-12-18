<div align="center">
🤖 AI Tutor – Intelligent Learning Assistant
Learn smarter. Learn faster. Learn with AI.














</div>
👋 Welcome

AI Tutor is an AI-powered learning companion that helps users study efficiently and interactively.
It enables topic-based summarization, test generation, question answering, and learning roadmap creation using modern Generative AI techniques.

Built using Retrieval-Augmented Generation (RAG) and FAISS, AI Tutor focuses on accuracy, relevance, and grounded responses.

✨ Features
📘 Topic-Based Summarization

Upload books, notes, or documents

Generate concise summaries for selected topics

Semantic search ensures only relevant content is used

📝 Test Generator & Evaluation

Auto-generate tests from learning material

Supports:

Multiple Choice Questions (MCQs)

Descriptive questions

Provides:

Scores

Correct answers

Improvement feedback

❓ Context-Aware Q&A

Ask questions directly from uploaded content

Uses RAG to retrieve context before answering

Minimizes hallucinations and improves reliability

🗺️ Field-Based Learning Roadmaps

Generates structured learning paths for:

Software Development

DevOps / Cloud

Data Science

AI / Machine Learning

Includes concepts, steps, and resource suggestions

🧠 Architecture Overview
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
AI Tutor Response

🛠️ Tech Stack
🤖 AI & ML

Retrieval-Augmented Generation (RAG)

Hugging Face (Embeddings & NLP models)

Groq (High-speed LLM inference)

FAISS (Vector database)

⚙️ Backend

Python

LangChain

🎨 UI & Tools

Streamlit

Visual Studio Code

Git & GitHub

📂 Project Structure
AI-Tutor/
├── app.py                 # Streamlit entry point
├── pages/
│   ├── summarizer.py      # Topic-based summarization
│   ├── test_generator.py  # Test generation & evaluation
│   ├── qa_engine.py       # RAG-powered Q&A
│   └── roadmap.py         # Learning roadmap generator
├── requirements.txt
└── README.md

🚀 Getting Started
🔹 Clone the Repository
git clone <repository-url>
cd AI-Tutor

🔹 Create Virtual Environment
python -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows

🔹 Install Dependencies
pip install -r requirements.txt

🔹 Set Environment Variables
GROQ_API_KEY
HUGGINGFACE_API_TOKEN

▶️ Run the Application
streamlit run app.py

🎯 Use Cases

🎓 Students preparing for exams

🌱 Self-learners exploring new domains

👩‍🏫 Educators creating tests & summaries

🚀 Career-focused learners building structured paths

🔮 Roadmap

User authentication

Learning progress tracking

Multi-language support

React-based frontend

Cloud deployment

👩‍💻 Author

Harini

💡 Notes

This project demonstrates a real-world application of Generative AI, combining RAG, vector databases, and LLMs using free and open-source tools.
The project is actively evolving.

⭐ If you find this project useful, consider starring the repository.
