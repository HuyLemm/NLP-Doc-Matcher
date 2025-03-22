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

  const handleCrawl = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/crawl/${category}/?n=${numArticles}`
      );
      setMessage(response.data.message);
    } catch (error) {
      setMessage("❌ Có lỗi xảy ra!");
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
    onDrop: (acceptedFiles) => setFiles(acceptedFiles),
  });

  const handleUpload = async () => {
    if (files.length === 0) {
      alert("⚠ Vui lòng chọn file để tải lên!");
      return;
    }
    const formData = new FormData();
    files.forEach((file) => formData.append("file", file));

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      alert(response.data.message);
    } catch (error) {
      alert("❌ Có lỗi xảy ra khi tải lên file!");
    }
  };

  return (
    <div className="container">
      <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          📊 Crawl Bài Viết & Tải Lên File
        </h1>

        {/* Chọn số lượng bài báo */}
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

        {/* Chọn chuyên mục */}
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

        {/* Nút Crawl */}
        <button
          onClick={handleCrawl}
          disabled={loading}
          className="w-full px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition duration-300"
        >
          {loading ? "⏳ Đang crawl..." : "🚀 Crawl Dữ Liệu"}
        </button>

        {message && <p className="text-green-500 text-center mt-2">{message}</p>}

        {/* Khu vực Upload */}
        <div
          {...getRootProps()}
          className="mt-6 p-4 border-2 border-dashed border-gray-400 text-gray-600 bg-gray-50 text-center rounded-lg cursor-pointer hover:bg-gray-100 transition"
        >
          <input {...getInputProps()} />
          <p>📂 Kéo & thả file vào đây hoặc bấm để chọn file</p>
        </div>

        <button
          onClick={handleUpload}
          className="w-full px-4 py-2 mt-4 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-300"
        >
          📤 Tải lên file
        </button>
      </div>
    </div>
  );
}
