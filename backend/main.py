# rag_qa_fastapi/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline
import os
import pdfplumber
import io

app = FastAPI()

# CORS 설정 (프론트엔드와 연동 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = None  # 전역 문서 검색기 객체

# PDF 업로드 및 벡터화
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # 텍스트 분할
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = splitter.create_documents([text])

    # 임베딩 및 벡터 DB 생성 (Hugging Face 기반)
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    global retriever
    retriever = vectorstore.as_retriever()

    return {
        "message": "PDF 업로드 및 인덱싱이 완료되었습니다.",
        "extracted_text_preview": text[:1000] 
    }

# 사용자 질문 처리리
@app.get("/ask")
async def ask_question(q: str):
    if retriever is None:
        return {"error": "아직 문서가 업로드되지 않았습니다."}

    
    pipe = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=512)
    llm = HuggingFacePipeline(pipeline=pipe)

   
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Answer the following question based on the given context.
        Context: {context}
        Question: {question}
        Answer:
        """
    )

    # 체인 구성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    result = qa_chain.run(q)
    return {"answer": result}
