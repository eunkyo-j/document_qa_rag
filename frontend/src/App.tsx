import React, { useState } from "react";
import axios from "axios";

function App() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const handleUpload = async () => {
    if (!pdfFile) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", pdfFile);
    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("✅ 업로드 성공!\n" + res.data.extracted_text_preview);
    } catch (err) {
      alert("❌ 업로드 실패");
    }
    setUploading(false);
  };

  const handleAsk = async () => {
    if (!question) return;
    setAsking(true);
    try {
      const res = await axios.get("http://localhost:8000/ask", {
        params: { q: question },
      });
      setAnswer(res.data.answer);
    } catch (err) {
      alert("❌ 질문 실패");
    }
    setAsking(false);
  };

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <div className="max-w-xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-xl font-bold mb-4">PDF파일을 업로드하고 질문해보세요!</h1>

        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
          className="mb-2"
        />
        <button
          onClick={handleUpload}
          disabled={uploading || !pdfFile}
          className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
        >
          {uploading ? "업로드 중..." : "📤 PDF 업로드"}
        </button>

        <div className="mt-4">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="무엇이 궁금한가요?"
            rows={6}
            className="w-full p-2 border rounded mb-2 h-32"
          />
          <button
            onClick={handleAsk}
            disabled={asking || !question}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            {asking ? "질문 중..." : "💬 질문하기"}
          </button>
        </div>

        {answer && (
          <div className="mt-6 p-4 bg-gray-50 border rounded">
            <strong>🧠 답변:</strong>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
