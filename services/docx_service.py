import docx

class DocxService:
    @staticmethod
    def extract_text(file_path):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])