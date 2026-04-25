import streamlit as st
import os
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="PDF Insight AI", page_icon="📚")
st.title("PDF Insight AI")

def process_uploaded_files(uploaded_files):
    all_splits = []
    for uploaded_file in uploaded_files:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        if uploaded_file.name.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif uploaded_file.name.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
            continue
        
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
        splits = text_splitter.split_documents(documents)
        all_splits.extend(splits) 
    return all_splits

def build_rag_chain(splits):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 

    context_q_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given a chat history and latest user question which might reference context in chat history, formulate a standalone question which can be understood without the chat history. Do not answer the question, just formulate it if needed and otherwise return as it is."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, context_q_prompt)

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Use the following context to answer the user's question.\n\nContext:{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    return create_retrieval_chain(history_aware_retriever, question_answer_chain)

with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Upload PDF or DOCX files", type=["pdf", "docx"], accept_multiple_files=True)
    
    if uploaded_files:
        current_file_names = "-".join([f.name for f in uploaded_files])
        if "current_files" not in st.session_state or st.session_state.current_files != current_file_names:
            with st.spinner("Processing documents..."):
                splits = process_uploaded_files(uploaded_files)
                if splits:
                    st.session_state.rag_chain = build_rag_chain(splits)
                    st.session_state.current_files = current_file_names
                    st.session_state.chat_history = [] 
                    st.success(f"{len(uploaded_files)} Document(s) processed and ready!")

if "rag_chain" not in st.session_state:
    st.info("Please upload one or more documents in the sidebar to start chatting.")
else:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    if user_input := st.chat_input("Ask a question about your documents..."):
        st.chat_message("user").markdown(user_input)
        
        with st.spinner("Thinking..."):
            response = st.session_state.rag_chain.invoke({
                "input": user_input,
                "chat_history": st.session_state.chat_history
            })
            answer = response["answer"]
            
        st.chat_message("assistant").markdown(answer)
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        st.session_state.chat_history.append(AIMessage(content=answer))