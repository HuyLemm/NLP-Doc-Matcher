import fitz  # PyMuPDF
import openpyxl
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from docx import Document
import re
import os

def extract_text_from_pdf(pdf_path):
    """Trích xuất nội dung từ PDF, áp dụng OCR nếu cần"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    # Nếu PDF không có text, dùng OCR
    if not text.strip():
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text.strip()

def extract_text_from_docx(docx_path):
    """Trích xuất nội dung từ Word"""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_text_from_excel(excel_path):
    """Trích xuất nội dung từ Excel"""
    wb = openpyxl.load_workbook(excel_path)
    text = ""
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for row in ws.iter_rows(values_only=True):
            text += " ".join(str(cell) for cell in row if cell) + "\n"
    return text.strip()

def clean_text(text):
    """Chuẩn hóa văn bản trước khi lưu"""
    text = text.replace("\n", " ").strip()
    text = re.sub(r'\s+', ' ', text)  # Xóa khoảng trắng thừa
    return text


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    elif ext in ['.xls', '.xlsx']:
        return extract_text_from_excel(file_path)
    else:
        raise ValueError("Unsupported file format")