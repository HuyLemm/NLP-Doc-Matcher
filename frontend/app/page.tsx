// Updated frontend Home component
"use client";

import { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";

export default function Home() {
  const [numArticles, setNumArticles] = useState(10);
  const [category, setCategory] = useState("tuoitre");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [mode, setMode] = useState<number | null>(null); // 1 = crawl, 2 = upload + extract, 3 = upload + compare

  const handleCrawl = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/crawl/${category}/?n=${numArticles}`
      );
      setMessage(response.data.message);
    } catch (error) {
      setMessage("❌ Có lỗi xảy ra khi crawl!");
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc", ".docx"],
      "application/vnd.ms-excel": [".xls", ".xlsx"],
    },
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) setFiles([acceptedFiles[0]]);
    },
  });

  const handleUpload = async (forComparison = false) => {
    if (files.length === 0) return alert("⚠ Vui lòng chọn file để tải lên!");

    const formData = new FormData();
    formData.append("file", files[0]);

    const endpoint = forComparison
      ? "http://127.0.0.1:8000/api/compare/"
      : "http://127.0.0.1:8000/api/upload/";

    try {
      const response = await axios.post(endpoint, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(response.data.message || "✅ Thành công!");
    } catch (error) {
      setMessage("❌ Có lỗi xảy ra khi tải lên file!");
    }
  };

  return (
    <div className="container">
      <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          📊 Hệ Thống Xử Lý Văn Bản
        </h1>

        {/* Chọn chức năng */}
        <div className="mb-6 flex justify-center gap-4">
          <button
            onClick={() => {
              setMode(1);
              setMessage("");
              setFiles([]);
            }}
            className={`px-4 py-2 rounded-lg font-semibold border ${
              mode === 1 ? "bg-blue-500 text-white" : "bg-white text-blue-500 border-blue-500"
            }`}
          >
            🚀 Crawl báo
          </button>
          <button
            onClick={() => {
              setMode(2);
              setMessage("");
              setFiles([]);
            }}
            className={`px-4 py-2 rounded-lg font-semibold border ${
              mode === 2 ? "bg-green-500 text-white" : "bg-white text-green-500 border-green-500"
            }`}
          >
            📤 Upload & Extract
          </button>
          <button
            onClick={() => {
              setMode(3);
              setMessage("");
              setFiles([]);
            }}
            className={`px-4 py-2 rounded-lg font-semibold border ${
              mode === 3 ? "bg-purple-500 text-white" : "bg-white text-purple-500 border-purple-500"
            }`}
          >
            🔍 Upload & So Sánh
          </button>
        </div>

        {mode === 1 && (
          <>
            <div className="mb-4">
              <label className="block text-lg font-medium text-gray-700">
                📄 Số lượng bài viết:
              </label>
              <input
                type="number"
                value={numArticles}
                onChange={(e) => setNumArticles(Number(e.target.value))}
                className="w-full p-2 border border-gray-300 rounded mt-1 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div className="mb-4">
              <label className="block text-lg font-medium text-gray-700">
                📰 Chọn chuyên mục:
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded mt-1 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="tuoitre">Tuổi Trẻ</option>
                <option value="thanhnien">Thanh Niên</option>
                <option value="nld">Người Lao Động</option>
                <option value="sggp">Sài Gòn Giải Phóng</option>
              </select>
            </div>
            <button
              onClick={handleCrawl}
              disabled={loading}
              className="w-full px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition duration-300"
            >
              {loading ? "⏳ Đang crawl..." : "🚀 Crawl Dữ Liệu"}
            </button>
          </>
        )}

        {(mode === 2 || mode === 3) && (
          <>
            <div
              {...getRootProps()}
              className="mt-4 p-4 border-2 border-dashed border-gray-400 text-gray-600 bg-gray-50 text-center rounded-lg cursor-pointer hover:bg-gray-100 transition"
            >
              <input {...getInputProps()} />
              <p>📂 Kéo & thả file vào đây hoặc bấm để chọn file</p>
            </div>
            {files.length > 0 && (
              <div className="mt-4 flex items-center justify-between bg-gray-100 p-3 rounded shadow">
                <span className="text-sm text-gray-700">
                  📄 Đã chọn: <strong>{files[0].name}</strong>
                </span>
                <button
                  onClick={() => setFiles([])}
                  className="ml-4 px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
                >
                  ❌ Gỡ file
                </button>
              </div>
            )}
            <button
              onClick={() => handleUpload(mode === 3)}
              className="w-full px-4 py-2 mt-4 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-300"
            >
              {mode === 3 ? "🔍 So Sánh File" : "📤 Tải lên & Extract"}
            </button>
          </>
        )}

        {message && <p className="text-green-600 text-center mt-4 font-medium">✅ {message}</p>}
      </div>
    </div>
  );
}
