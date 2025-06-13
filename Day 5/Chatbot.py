import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema.runnable import Runnable
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
import tempfile

# ---------------------------
# Step 1: Set Gemini API Key
# ---------------------------
GOOGLE_API_KEY = "AIzaSyCaAF8nMeqTfcbcNPPMG6RDiUht5N8sJZs"  # Replace this
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ---------------------------
# Step 2: Streamlit UI
# ---------------------------
st.set_page_config(page_title="📄 PDF/DOC RAG Chatbot", page_icon="🤖")
st.title("🤖 Chatbot for PDF/DOC using Gemini + LangChain")
st.markdown("Upload a PDF or DOC file and ask questions about it.")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

# ---------------------------
# Step 3: File Processing
# ---------------------------
if uploaded_file is not None:
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name

        # Load and parse document
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif uploaded_file.name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            st.error("Unsupported file format.")
            st.stop()

        documents = loader.load()

        # Split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        # Embedding model
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Create vector store
        vectorstore = FAISS.from_documents(docs, embeddings)

        # Create retriever
        retriever = vectorstore.as_retriever()

        # Prompt for RAG
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert assistant who answers questions based on uploaded documents."
            ),
            HumanMessagePromptTemplate.from_template("{question}")
        ])

        # Language model
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

        # Final RAG chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=False
        )

        # ---------------------------
        # Step 4: Chat UI
        # ---------------------------
        question = st.text_input("Ask a question about the uploaded file:")
        if st.button("Ask"):
            if question.strip() == "":
                st.warning("Please enter a question.")
            else:
                try:
                    response = chain.run(question)
                    st.success("✅ Answer generated!")
                    st.markdown(f"**Answer:** {response}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    except Exception as e:
        st.error(f"❌ File processing failed: {str(e)}")
