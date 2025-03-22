from django.urls import path
from .views import crawl_articles, upload_file, crawl_from_sources

urlpatterns = [
    path("crawl/<str:category>/", crawl_articles, name="crawl_articles"),
    path("crawl/all/", crawl_from_sources, name="crawl_from_sources"),
    path("upload/", upload_file, name="upload_file"),
]
