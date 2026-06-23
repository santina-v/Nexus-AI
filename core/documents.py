import fitz  # PyMuPDF
from core.ai import ChatEngine

class DocumentAnalyzer:
    def __init__(self):
        self.ai = ChatEngine()

    def extract_text_from_pdf(self, file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def extract_text_from_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def analyze(self, file_path):
        if file_path.endswith(".pdf"):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith(".txt"):
            text = self.extract_text_from_txt(file_path)
        else:
            return "Unsupported file type. Use PDF or TXT."

        # Limit text to first 3000 characters to keep it fast
        text = text[:3000]

        prompt = f"Please summarize this document clearly:\n\n{text}"
        summary = self.ai.chat(prompt)
        return summary