# 📚 PDF Insight AI – RAG Document Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://archit-pdf-insight-ai.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-lightgrey.svg)](https://python.langchain.com/)
[![Gemini API](https://img.shields.io/badge/Google-Gemini_API-orange.svg)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-teal.svg)](https://www.trychroma.com/)

**PDF Insight AI** is a Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF and DOCX documents and have intelligent, context-aware conversations with their data. 

<img width="1920" height="1013" alt="Screenshot 2026-04-26 125838" src="https://github.com/user-attachments/assets/ec945438-f4b1-4d21-9278-f5e7cb96e69e" />
<br>
Built using the LangChain ecosystem and Google's Gemini API, this tool chunks, embeds, and semantically searches through your documents to provide highly accurate answers based purely on the uploaded knowledge base.

## ✨ Key Features
- **Multi-File Support:** Upload multiple `.pdf` or `.docx` files simultaneously. The app aggregates them into a single, cohesive knowledge base.
- **Conversational Memory:** The chatbot remembers chat history, allowing you to ask natural, follow-up questions without repeating context.
- **Advanced Semantic Search:** Utilizes **ChromaDB** to store vector embeddings and perform fast, highly relevant similarity searches over document content.
- **State-of-the-Art LLM Integration:** Powered by the **Google Gemini 2.5 Flash** model for rapid natural language understanding and response generation.
- **Clean UI:** Designed with **Streamlit** for a seamless, responsive, and intuitive user experience.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Framework:** LangChain (Core, Community, Google GenAI)
* **Vector Database:** ChromaDB
* **LLM & Embeddings:** Google Gemini API (`gemini-2.5-flash`, `gemini-embedding-001`)
* **Document Parsing:** PyPDF, Docx2txt

---

## 🚀 Live Demo
Try the application live here: **[PDF Insight AI on Streamlit Cloud](https://archit-pdf-insight-ai.streamlit.app)**

*(Note: The live demo runs on a free-tier API key. If you encounter a `429 Resource Exhausted` error, please wait 60 seconds and try your query again.)*

---

## 💻 Local Setup & Installation

To run this project locally on your own machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/architsingh7/PDF-Insight-AI.git](https://github.com/architsingh7/PDF-Insight-AI.git)
cd PDF-Insight-AI
```
2. Install Dependencies
It is recommended to use a virtual environment. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Set Up API Keys
You will need a free Google Gemini API key to run the models. Get one from Google AI Studio.
Create a .env file in the root directory (or use your system's environment variables) and add your key:
```
GOOGLE_API_KEY="your-api-key-here"
```
6. Run the Application
Launch the Streamlit server:
```
streamlit run app.py
```
The application will automatically open in your default web browser at http://localhost:8501.

## 💡 How It Works (The RAG Pipeline)<br>
1. **Ingestion:** Documents are loaded using PyPDFLoader and Docx2txtLoader.<br>
2. **Chunking:** Text is split into manageable, overlapping 1000-character chunks using RecursiveCharacterTextSplitter to maintain context.<br>
3. **Embedding:** Chunks are passed through Google's embedding model to generate high-dimensional vector representations.<br>
4. **Storage:** Vectors are stored locally in ChromaDB.<br>
5. **Retrieval & Generation:** When a user asks a question, the app rewrites it based on chat history, searches ChromaDB for the top 3 most relevant chunks, and feeds that context to the Gemini LLM to generate a precise answer.<br>

## 👨‍💻 Author<br>
Archit Singh -<br>
* [GitHub](https://github.com/architsingh7)<br>
* [LinkedIn](https://www.linkedin.com/in/architdeveloper/)
