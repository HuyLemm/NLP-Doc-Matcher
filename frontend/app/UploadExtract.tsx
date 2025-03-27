// UploadExtractSection.tsx
"use client";

import { useDropzone } from "react-dropzone";
import { useState } from "react";
import axios from "axios";

export default function UploadExtract() {
  const [files, setFiles] = useState<File[]>([]);
  const [message, setMessage] = useState("");

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

  const handleUpload = async () => {
    if (files.length === 0) return alert("⚠ Vui lòng chọn file để tải lên!");

    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(response.data.message || "✅ Thành công!");
    } catch (error) {
      setMessage("❌ Có lỗi xảy ra khi tải lên file!");
    }
  };

  return (
    <div>
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
        onClick={handleUpload}
        className="w-full px-4 py-2 mt-4 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-300"
      >
        📤 Tải lên & Extract
      </button>
      {message && <p className="text-green-600 text-center mt-4 font-medium">✅ {message}</p>}
    </div>
  );
}
