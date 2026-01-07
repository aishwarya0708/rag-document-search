import os
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.config import settings

os.environ["COHERE_API_KEY"] = settings.COHERE_API_KEY

def split_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

class AeroAssistRAG:
    def __init__(self):
        self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
        self.llm = ChatCohere(model="command-r-08-2024") 
        self.vectorstore = None
        self.load_vectorstore()

    def load_vectorstore(self):
        if os.path.exists(settings.VECTORSTORE_DIR) and os.listdir(settings.VECTORSTORE_DIR):
            self.vectorstore = Chroma(
                persist_directory=settings.VECTORSTORE_DIR,
                embedding_function=self.embeddings
            )

    def ingest_documents(self):
        documents = []
        for filename in os.listdir(settings.DOCUMENTS_DIR):
            filepath = os.path.join(settings.DOCUMENTS_DIR, filename)
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    chunks = split_text(content, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
                    for chunk in chunks:
                        documents.append(Document(page_content=chunk, metadata={"source": filename}))
        
        if not documents:
            return 0
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=settings.VECTORSTORE_DIR
        )
        return len(documents)

    def query(self, question):
        if not self.vectorstore:
            return "No documents loaded. Please upload documents first.", []
        
        docs = self.vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""
        
        response = self.llm.invoke(prompt)
        return response.content, docs

    def get_document_count(self):
        if self.vectorstore:
            return self.vectorstore._collection.count()
        return 0