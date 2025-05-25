# 📚 Document Q&A System (RAG 기반)

문서 기반 질의응답 기능을 제공하는 RAG(Retrieval-Augmented Generation) 방식의 웹 애플리케이션입니다.
사용자가 업로드한 PDF 문서를 읽고, 자연어 질문에 대해 Hugging Face에서 제공하는 오픈소스 LLM을 활용해 정확한 답변을 생성합니다.


![Image](https://github.com/user-attachments/assets/b6cb901f-f3ff-4dff-9512-8655fef2218c)

![Image](https://github.com/user-attachments/assets/52d82fca-269c-450f-9942-b4837cc9b59d)

![Image](https://github.com/user-attachments/assets/a74b3351-11d9-43bd-8b6a-9b832540732d)

![Image](https://github.com/user-attachments/assets/35c95a4c-6ebd-454e-9088-17f97216bc7f)

---

## ✨ 주요 기능

- ✅ PDF 업로드 및 텍스트 추출
- ✅ 문서 내용을 벡터 임베딩 후 벡터 데이터베이스 저장
- ✅ 사용자의 자연어 질문에 대해 관련 문서를 검색 후 LLM에 전달
- ✅ 문맥에 기반한 GPT 답변 생성
- ✅ 프론트엔드에서 실시간 응답 확인

---

## 🧠 기술 스택

### 🖥️ 프론트엔드
- React + TypeScript
- Vite – 빠른 개발 서버 환경
- Axios – REST API 통신

### ⚙️ 백엔드
- FastAPI – 고성능 비동기 RESTful API 서버
- PyMuPDF – PDF 텍스트 추출
- OpenAI API – GPT 기반 자연어 처리
- FAISS – 벡터 유사도 검색 (문서 검색용)

---

## 🔄 RAG 기반 질의응답 구조

1. PDF 업로드 → 텍스트 추출
2. 문서 분할 및 임베딩 생성
3. FAISS를 이용한 유사 문서 검색
4. 관련 문서를 GPT에게 전달하여 답변 생성
5. 응답 반환 및 사용자에게 표시

```mermaid
graph TD
    A[PDF 업로드] --> B[텍스트 추출]
    B --> C[문서 분할 및 임베딩]
    C --> D[FAISS 벡터 저장]
    E[사용자 질문] --> F[질문 임베딩]
    F --> G[관련 문서 검색]
    G --> H[GPT 응답 생성]
    H --> I[프론트엔드 출력]
