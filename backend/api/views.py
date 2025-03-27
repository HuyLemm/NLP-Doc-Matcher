from rest_framework.decorators import api_view
from rest_framework.response import Response
from crawl.crawl_manager import start_crawling
from extract.extract_text import extract_text_from_fileobj
from database.database import save_business_document
from similarity.compare_uploaded import compare_uploaded_document
import threading

@api_view(["GET"])
def crawl_articles(request, category):
    num_articles = int(request.GET.get("n", 10))
    result = start_crawling([category], num_articles)
    return Response({"message": f"Đã crawl xong {len(result)} bài từ {category}!"})


@api_view(["POST"])
def upload_file(request):
    file = request.FILES["file"]
    extracted_text = extract_text_from_fileobj(file)

    doc_info = {
        "file_name": file.name,
        "file_type": file.content_type,
        "content": extracted_text,
        "source": "user_upload"
    }

    save_business_document(doc_info)

    return Response({"message": f"Tải lên và lưu '{file.name}' thành công!"})


@api_view(["POST"])
def crawl_from_sources(request):
    try:
        data = request.data
        sources = data.get("sources", [])
        num_articles = int(data.get("num_articles", 5))

        if not sources:
            return Response({"error": "Vui lòng chọn ít nhất một nguồn báo."}, status=400)

        threading.Thread(target=start_crawling, args=(sources, num_articles)).start()
        return Response({"message": "Crawl đã bắt đầu!", "sources": sources})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def compare_uploaded_file(request):
    try:
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "❌ Không có file được gửi."}, status=400)

        # 1. Trích xuất nội dung từ file
        extracted_text = extract_text_from_fileobj(file)
        if not extracted_text.strip():
            return Response({"error": "⚠ Không trích xuất được nội dung từ file."}, status=400)

        # 2. So sánh với cơ sở dữ liệu
        results = compare_uploaded_document(extracted_text, top_k=5)

        return Response({
            "message": "✅ So sánh thành công!",
            "results": results
        })

    except Exception as e:
        return Response({
            "error": f"❌ Lỗi hệ thống: {str(e)}"
        }, status=500)

