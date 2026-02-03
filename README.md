# 🤖 Hybrid RAG System using Knowledge Graph and FAISS

## 📌 Overview
This project implements a **Hybrid Retrieval-Augmented Generation (RAG) system** that combines the strengths of a **Knowledge Graph (KG)** and **unstructured document retrieval (PDFs)** to deliver **accurate, explainable, and hallucination-free answers**.

The system intelligently decides whether a question requires:
- **Exact factual retrieval** from structured data (via Knowledge Graph), or
- **Contextual summarization** from unstructured documents (via RAG).

A local open-source LLM (**LLaMA 3 via Ollama**) is used for answer generation, ensuring privacy and offline capability.

---

## 🎯 Key Features
- 🔗 Knowledge Graph–based factual answering
- 📄 PDF-based contextual question answering
- 🔍 FAISS-powered semantic vector search
- 🧠 Local LLM inference using Ollama (LLaMA 3)
- 🚫 Hallucination prevention via strict context grounding
- 📚 Source file attribution for transparency
- 📊 Confidence/accuracy indicator for better UX
- 💬 Interactive Streamlit-based chat UI

---

## 🏗️ System Architecture (High-Level)


---

## 📂 Project Structure


---

## 📂 Project Structure

Hybrid-RAG-KG-System/
│
├── python_rag/
│ ├── rag_core.py # Core RAG + KG logic
│ ├── rag_ui.py # Streamlit UI
│
├── scripts/
│ ├── build_index.py # Script to generate embeddings & FAISS index
│
├── utils/
│ ├── chunking.py # Text chunking utilities
│
├── data_samples/
│ ├── sample_structured.json
│ ├── sample_semistructured.json
│ ├── sample_pdf_chunk.json
│ ├── sample_triples.json
│
├── README.md
├── requirements.txt
├── .gitignore



---

## 🧠 Query Handling Strategy

The system classifies queries into three categories:

### 1️⃣ Fact-Based Queries
Examples:
- *What is the hire date of Employee_1?*
- *What is the salary of Employee_2?*

➡️ Answered directly from **Knowledge Graph**  
➡️ No LLM usage → no hallucination

---

### 2️⃣ Relation-Based Queries
Examples:
- *Who sent the email to chris.germany@enron.com?*

➡️ Resolved using **KG relationship triples**

---

### 3️⃣ Descriptive Queries
Examples:
- *Describe how artificial intelligence is mentioned in Microsoft.*
- *Explain the jobs initiative.*

➡️ Answered using **PDF chunks + LLM summarization**

---

### 🚫 Out-of-Scope Queries
If the information is not present in the data, the system clearly responds:
> *“The information is not available in the provided documents.”*

---

## 🛠️ Technologies Used

| Component | Technology |
|--------|-----------|
| Programming Language | Python |
| Vector Database | FAISS |
| Embeddings | Sentence Transformers (MiniLM) |
| LLM | Ollama (LLaMA 3) |
| UI | Streamlit |
| Chunking | LangChain |
| KG Storage (optional) | Neo4j |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AquibAhmadrja/AI-Knowledge-Graph-Builder-For-Enterprises.git
cd Hybrid-RAG-KG-System


Install Dependencies
pip install -r requirements.txt

Run Ollama (Local LLM)
ollama run llama3

Build FAISS Index (One-Time)
python scripts/create_faiss_index.py

python scripts/build_index.py
streamlit run python_rag/rag_ui.py

📦 Note on FAISS Index & Embeddings

Due to size constraints and best practices:

FAISS indices and embeddings are not stored in GitHub

They are generated locally using the provided build script

This approach ensures:

Clean repository

Reproducibility

Industry-standard workflow

📊 Performance & Accuracy

High precision for factual queries via Knowledge Graph

Contextually grounded descriptive answers via RAG

No hallucinations due to strict prompt enforcement

Confidence indicator shown in UI for user trust

🚀 Future Enhancements

Knowledge Graph visualization in UI

Advanced ML-based query classification

Incremental FAISS updates

Multi-document reasoning

Analytics dashboard for usage insights

🧾 Conclusion

This project demonstrates a robust, scalable, and explainable Hybrid RAG architecture suitable for enterprise-level question answering systems. By combining structured knowledge with unstructured document retrieval, it achieves both accuracy and interpretability, going beyond traditional RAG implementations.

👤 Author

[Aquib Ahmad rja]
Hybrid RAG & Knowledge Graph Project