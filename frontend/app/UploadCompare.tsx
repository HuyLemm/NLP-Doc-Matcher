"use client";

import { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";

export default function UploadCompare() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc", ".docx"],
      "application/vnd.ms-excel": [".xls", ".xlsx"],
    },
    multiple: false,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
        setResults([]);
        setMessage(null);
      }
    },
  });

  const handleCompare = async () => {
    if (!file) return alert("⚠ Vui lòng chọn file!");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/compare/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResults(res.data.results || []);
      setMessage(res.data.message || "✅ So sánh hoàn tất!");
    } catch (error) {
      setMessage("❌ Lỗi khi so sánh với cơ sở dữ liệu.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-4">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className="p-4 border-2 border-dashed border-gray-400 text-gray-600 bg-gray-50 text-center rounded-lg cursor-pointer hover:bg-gray-100 transition"
      >
        <input {...getInputProps()} />
        <p>📂 Kéo & thả file vào đây hoặc bấm để chọn</p>
      </div>

      {/* File info */}
      {file && (
        <div className="mt-4 flex items-center justify-between bg-gray-100 p-3 rounded shadow">
          <span className="text-sm text-gray-700">
            📄 Đã chọn: <strong>{file.name}</strong>
          </span>
          <button
            onClick={() => {
              setFile(null);
              setResults([]);
              setMessage(null);
            }}
            className="ml-4 px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
          >
            ❌ Gỡ file
          </button>
        </div>
      )}

      {/* Compare button */}
      <button
        onClick={handleCompare}
        disabled={!file || loading}
        className="w-full px-4 py-2 mt-4 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition"
      >
        {loading ? "🔍 Đang so sánh..." : "🔍 So Sánh File"}
      </button>

      {/* Message */}
      {message && (
        <p className="mt-4 text-center text-blue-600 font-semibold">{message}</p>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-bold mb-2 text-gray-800 text-center">
            📋 Top {results.length} văn bản tương tự nhất:
          </h3>
          <ul className="space-y-4">
            {results.map((item, idx) => (
              <li
                key={idx}
                className="bg-gray-100 p-4 rounded shadow-sm border-l-4 border-purple-500"
              >
                <p className="text-sm text-gray-800">
                  <strong>📌 Nguồn:</strong> {item.source}
                </p>
                <p className="text-sm text-gray-800">
                  <strong>🗂 Chuyên mục:</strong> {item.category}
                </p>
                <p className="text-sm text-gray-800">
                  <strong>📈 Similarity:</strong>{" "}
                  <span className="text-purple-600 font-semibold">
                    {(item.similarity * 100).toFixed(2)}%
                  </span>
                </p>
                <p className="text-sm text-gray-700 mt-2 line-clamp-3">
                  <strong>📝 Nội dung:</strong> {item.text}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
