from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def get_vectorstore(docs):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return vectorstore
