"use client";

import { useState } from "react";
import axios from "axios";

export default function CrawlSection({ setMessage }: { setMessage: (msg: string) => void }) {
  const [numArticles, setNumArticles] = useState(10);
  const [category, setCategory] = useState("tuoitre");
  const [loading, setLoading] = useState(false);

  const handleCrawl = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/crawl/${category}/?n=${numArticles}`
      );
      setMessage(response.data.message || "✅ Crawl thành công!");
    } catch {
      setMessage("❌ Có lỗi xảy ra khi crawl!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-4">
        <label className="block text-lg font-medium text-gray-700">📄 Số lượng bài viết:</label>
        <input
          type="number"
          value={numArticles}
          onChange={(e) => setNumArticles(Number(e.target.value))}
          className="w-full p-2 border border-gray-300 rounded mt-1 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div className="mb-4">
        <label className="block text-lg font-medium text-gray-700">📰 Chọn chuyên mục:</label>
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
    </div>
  );
}
