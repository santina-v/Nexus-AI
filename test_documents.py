from core.documents import DocumentAnalyzer

analyzer = DocumentAnalyzer()
result = analyzer.analyze("sample.txt")
print("Summary:", result)