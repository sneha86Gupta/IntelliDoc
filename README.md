<div align="center">

<img src="https://img.shields.io/badge/IntelliDoc-AI%20Powered-1D9E75?style=for-the-badge&logoColor=white" alt="IntelliDoc"/>

# IntelliDoc

**AI-Powered Retrieval-Augmented Question Generation System**

An intelligent educational platform that analyzes academic documents, extracts semantic topics, and generates context-aware questions using RAG.

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini%20API-4285F4?style=flat-square&logo=google&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

</div>

---

## ✦ Overview

IntelliDoc combines **FastAPI**, **ChromaDB**, **Sentence Transformers**, **LangChain**, and the **Gemini LLM API** to create an intelligent, scalable document analysis system. Upload a PDF or DOCX, explore semantically extracted topics, and generate AI-driven educational questions — all through an interactive web interface.

---

## ✦ Features

| | Feature | Description |
|---|---|---|
| 📄 | **Document Upload** | PDF and DOCX support with automatic text and heading extraction |
| 🔢 | **Semantic Chunking** | Smart content splitting with dense vector embeddings |
| 🧠 | **Topic Extraction** | KMeans clustering for automatic semantic topic identification |
| 🗄️ | **Vector Retrieval** | ChromaDB-powered similarity search across all chunks |
| ✨ | **AI Question Gen** | RAG pipeline with Gemini LLM for context-aware questions |
| 📤 | **PDF Export** | Export generated questions as a downloadable PDF |

---

## ✦ Tech Stack

<details>
<summary><b>Backend</b></summary>
<br/>

| Package | Role |
|---|---|
| `Python` | Core language |
| `FastAPI` | REST API framework |
| `LangChain` | LLM orchestration |
| `PyMuPDF` | PDF text extraction |
| `python-docx` | DOCX text extraction |
| `ReportLab` | PDF export generation |

</details>

<details>
<summary><b>AI & Retrieval</b></summary>
<br/>

| Package | Role |
|---|---|
| `Gemini API` | LLM for question generation |
| `Sentence Transformers` | Embedding model (`all-MiniLM-L6-v2`) |
| `ChromaDB` | Vector database for semantic search |
| `KMeans (sklearn)` | Topic clustering |

</details>

<details>
<summary><b>Frontend</b></summary>
<br/>

| Technology | Role |
|---|---|
| `HTML` | Page structure |
| `TailwindCSS` | Styling |
| `JavaScript` | Dynamic rendering |

</details>

---

## ✦ How It Works

```
 User uploads PDF/DOCX
        │
        ▼
 Text + heading extraction  (PyMuPDF / python-docx)
        │
        ▼
 Semantic chunking
        │
        ▼
 Embedding generation       (all-MiniLM-L6-v2)
        │
        ▼
 Vector storage             (ChromaDB)
        │
        ▼
 KMeans topic clustering
        │
        ▼
 User selects a topic
        │
        ▼
 Semantic similarity search (ChromaDB)
        │
        ▼
 RAG prompt construction
        │
        ▼
 AI question generation     (Gemini API)
        │
        ▼
 Display + PDF export
```

---

## ✦ Project Structure

```bash
IntelliDoc/
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── exports/
│   ├── constants/
│   ├── main.py
│   ├── config.py
│   └── dependencies.py
│
├── database/
│   └── chroma_client.py
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── *.html
│
├── uploads/
├── requirements.txt
└── README.md
```

---

## ✦ Installation

### 1 — Clone the repository

```bash
git clone https://github.com/your-username/intellidoc.git
cd intellidoc
```

### 2 — Create a virtual environment

```bash
python -m venv venv
```

<details>
<summary>Activate on Windows</summary>

```bash
venv\Scripts\activate
```

</details>

<details>
<summary>Activate on Linux / macOS</summary>

```bash
source venv/bin/activate
```

</details>

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5 — Run the server

```bash
uvicorn backend.main:app --reload
```

> Frontend available at **http://127.0.0.1:8000**

---

## ✦ API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/upload` | `POST` | Upload and process a PDF or DOCX document |
| `/topics` | `GET` | Retrieve semantically clustered topics |
| `/questions` | `POST` | Generate AI questions for a selected topic |
| `/export` | `POST` | Export generated questions as a PDF |

---

## ✦ Roadmap

- [ ] Adaptive learning analytics
- [ ] Personalized recommendations
- [ ] Multilingual support
- [ ] Conversational AI tutor
- [ ] Multi-document retrieval
- [ ] Cloud deployment & scalability

---

## ✦ Core Modules

<details>
<summary><b>Document Processing</b></summary>
<br/>

- Text extraction from PDF and DOCX files
- Heading detection and metadata extraction
- Smart chunking for embedding preparation

</details>

<details>
<summary><b>Embedding & Retrieval</b></summary>
<br/>

- Embedding generation using `all-MiniLM-L6-v2`
- Semantic similarity search via ChromaDB
- Persistent vector storage

</details>

<details>
<summary><b>Topic Extraction</b></summary>
<br/>

- Semantic clustering with KMeans
- Automatic topic label identification
- Frontend-ready topic list output

</details>

<details>
<summary><b>RAG Pipeline</b></summary>
<br/>

- Relevant chunk retrieval from ChromaDB
- Context-aware prompt construction
- AI response generation via Gemini API

</details>

---

<div align="center">

**IntelliDoc** demonstrates how RAG, semantic embeddings, vector databases, and generative AI can be integrated to build an intelligent educational platform for automated learning support.

<br/>

![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-1D9E75?style=flat-square)

</div>
