// Page.tsx
"use client";

import { useState } from "react";
import CrawlSection from "./CrawlSection";
import UploadExtract from "./UploadExtract";
import UploadCompare from "./UploadCompare";

export default function Page() {
  const [mode, setMode] = useState<number | null>(null); // 1 = crawl, 2 = extract, 3 = compare
  const [message, setMessage] = useState("");

  return (
    <div className="container">
      <div className="w-full max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          📊 Hệ Thống Xử Lý Văn Bản
        </h1>

        {/* Nút chọn chức năng */}
        <div className="mb-6 flex justify-center gap-4">
          <button
            onClick={() => setMode(1)}
            className={`px-4 py-2 rounded-lg font-semibold border ${
              mode === 1
                ? "bg-blue-500 text-white"
                : "bg-white text-blue-500 border-blue-500"
            }`}
          >
            🚀 Crawl báo
          </button>
          <button
            onClick={() => setMode(2)}
            className={`px-4 py-2 rounded-lg font-semibold border ${
              mode === 2
                ? "bg-green-500 text-white"
                : "bg-white text-green-500 border-green-500"
            }`}
          >
            📤 Upload & Extract
          </button>
          <button
            onClick={() => setMode(3)}
            className={`px-4 py-2 rounded-lg font-semibold border ${
              mode === 3
                ? "bg-purple-500 text-white"
                : "bg-white text-purple-500 border-purple-500"
            }`}
          >
            🔍 Upload & So Sánh
          </button>
        </div>

        {/* Khu vực chức năng */}
        {mode === 1 && <CrawlSection setMessage={setMessage}/>}
        {mode === 2 && <UploadExtract/>}
        {mode === 3 && <UploadCompare/>}

        {message && (
          <p className="text-green-600 text-center mt-4 font-medium">
            ✅ {message}
          </p>
        )}
      </div>
    </div>
  );
}
