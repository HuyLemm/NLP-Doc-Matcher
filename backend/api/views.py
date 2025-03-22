from rest_framework.decorators import api_view
from rest_framework.response import Response
from crawl.crawl_manager import start_crawling
from extract.extract_text import extract_text_from_file
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import threading
import json

@api_view(["GET"])
def crawl_articles(request, category):
    num_articles = int(request.GET.get("n", 10))
    result = start_crawling([category], num_articles)
    return Response({"message": f"Đã crawl xong {len(result)} bài từ {category}!"})

@api_view(["POST"])
def upload_file(request):
    file = request.FILES["file"]
    file_name = default_storage.save(file.name, ContentFile(file.read()))
    file_path = default_storage.path(file_name)

    extracted_text = extract_text_from_file(file_path)

    return Response({"message": "Tải lên thành công!", "content": extracted_text})


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
