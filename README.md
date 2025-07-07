


> **Advanced-Multimodal-RAG- research assistant**

---


## 1. Project Overview

**Advanced-Multimodal-RAG-Assistant** is a robust Retrieval-Augmented Generation (RAG) framework designed to overcome the knowledge and modality limitations of standard Large Language Models (LLMs). Leveraging **Google’s Gemini API** (including `gemini-2.5-flash` and `models/embedding-001`), this assistant enables intelligent Q\&A over a hybrid knowledge base of **text documents and images**, making it ideal for research and domain-specific tasks.

---

## 2. Problem Statement & Motivation

### ❌ Limitations in Traditional LLMs:

* **Knowledge Cutoff**: LLMs lack awareness of recent or domain-specific content.
* **Hallucination**: They sometimes generate inaccurate or misleading responses.
* **Text-Only Focus**: Most RAG systems ignore visual data like charts, scanned notes, or diagrams.

### ✅ Our Solution:

The **Advanced-Multimodal-RAG-Assistant** addresses these issues through:

* **Augmented Retrieval** from a user-defined knowledge base.
* **Fact-grounded Response Generation** via Gemini.
* **Multimodal Support**, extracting context from both text and images.
* **Scalable Architecture**, easily extensible to support other data types.

---

## 3. Key Features

* 📄 **Multi-format Support**: Ingests PDFs, DOCXs, TXTs, and images (PNG, JPG, JPEG, GIF).
* 🧠 **Vision-to-Text Conversion**: Uses Gemini's vision model to describe image content.
* ✂️ **Efficient Chunking**: Segments documents for semantic coherence.
* 🧲 **Gemini-based Embeddings**: Generates high-quality vector representations.
* 🗂️ **Persistent Vector Store**: Uses ChromaDB to store and retrieve data efficiently.
* 🎯 **Context-Aware Q\&A**: Answers grounded in retrieved content—reducing hallucinations.
* 🧩 **Modular Design**: Extensible codebase with clearly separated responsibilities.
* 💻 **User-Friendly UI**: Built with Streamlit for document upload and question-answering.
* 📊 **Performance Evaluation**: Integrated Ragas evaluation module.

---

## 4. Architecture & Workflow

### 4.1 Modular Design Philosophy

The project follows **Separation of Concerns**, enhancing:

* 🔧 Maintainability
* 🧪 Testability
* ⚙️ Scalability

📁 Directory Overview:

```
Advanced-Multimodal-RAG-Assistant/
├── config/
├── src/
│   ├── data_ingestion/
│   ├── embeddings/
│   ├── vector_db/
│   ├── retrieval/
│   ├── generation/
│   ├── core/
│   └── evaluation/
├── app/
│   └── main.py
├── data/raw/
├── .env
├── requirements.txt
```

---

### 4.2 Core Workflow Explained

#### 🔄 **Indexing Phase (Offline):**

1. **Load Documents** → PDF, DOCX, TXT, and images from `data/raw/`
2. **Image Captioning** → Gemini generates descriptive text for visuals.
3. **Text Chunking** → RecursiveCharacterTextSplitter ensures contextual segmentation.
4. **Vector Embedding** → Text chunks & image descriptions embedded via `models/embedding-001`
5. **Storage** → Embeddings + metadata saved in ChromaDB

#### 💬 **Querying Phase (Online):**

1. **User Query** → Received via Streamlit UI
2. **Embedding & Retrieval** → Most relevant content retrieved from vector DB
3. **Prompt Construction** → Query + retrieved context combined
4. **Response Generation** → Gemini generates grounded answers via `gemini-2.5-flash`
5. **Answer Display** → Streamlit UI presents result + sources

---

### 4.3 Module Breakdown

| Module                 | Description                                                        |
| ---------------------- | ------------------------------------------------------------------ |
| `config/settings.py`   | Centralized configuration & API keys (via `.env`)                  |
| `data_ingestion/`      | Handles document loading, image captioning, and chunking           |
| `embeddings/`          | Generates embeddings using Gemini embedding model                  |
| `vector_db/`           | Manages persistent vector store via ChromaDB                       |
| `retrieval/`           | Retrieves top-k relevant content for a query                       |
| `generation/`          | Constructs prompt and generates answer                             |
| `core/rag_pipeline.py` | Orchestrates the full RAG pipeline                                 |
| `evaluation/`          | Uses Ragas to evaluate metrics like faithfulness and relevancy     |
| `app/main.py`          | Streamlit UI for uploading docs and interacting with the assistant |

---

## 5. Tech Stack

* **Language**: Python 3.9+
* **LLM API**: Google Gemini (`gemini-2.5-flash`, `models/embedding-001`)
* **Frameworks**: LangChain, Streamlit
* **Vector DB**: ChromaDB (local + persistent)
* **Parsers**: `pypdf`, `python-docx`, `Pillow`
* **Environment**: `python-dotenv`
* **Evaluation**: `ragas` (optional)

---

## 6. Setup & Installation

### 🔧 Step-by-Step:

1. **Clone Repo**

```bash
git clone https://github.com/your-username/Advanced-Multimodal-RAG-Assistant.git
cd Advanced-Multimodal-RAG-Assistant
```

2. **Create Virtual Environment**

```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

If `requirements.txt` not available:

```bash
pip install -U google-generativeai langchain langchain-google-genai pypdf python-docx pillow chromadb python-dotenv streamlit ragas
```

4. **Set Up API Key**
   Create `.env` file:

```
GEMINI_API_KEY="YOUR_API_KEY"
```

5. **Prepare Data Folder**

```bash
mkdir -p data/raw
# Place documents/images here
```

📁 Example:

```
data/raw/
├── neural_network_paper.pdf
├── pg132-images.txt
└── diagram_heart.png
```

---

## 7. Usage Guide

### ▶️ Run the App

```bash
streamlit run app/main.py
```

### 🧾 Index Files

* Use the sidebar to trigger **"Index Uploaded Documents"**
* Backend processes files → captions images → generates embeddings

### ❓ Outputs 

* Input your question in the chat bar
* The assistant responds using Gemini-powered grounded answers

![Output 1: ](https://i.postimg.cc/446K2TJF/Screenshot-2025-07-07-183851.png)

![Output 1: ](https://i.postimg.cc/VkLDLRGm/Screenshot-2025-07-07-183940.png)

---


## 8. Contributing

Pull requests are welcome! 

```bash
# Workflow
git checkout -b feature/YourFeature
# Make changes
git commit -m "Add Your Feature"
git push origin feature/YourFeature
# Submit PR
```

---

## 10. License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

