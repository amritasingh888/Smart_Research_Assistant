import os
import re

from PyPDF2 import PdfReader
from docx import Document


class ResearchLoader:

    def __init__(self):
        pass

    # -----------------------------
    # CLEAN TEXT
    # -----------------------------

    def clean_text(self, text):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # -----------------------------
    # PDF
    # -----------------------------

    def load_pdf(self, file_path):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return {
            "text": self.clean_text(text),
            "pages": len(reader.pages)
        }

    # -----------------------------
    # DOCX
    # -----------------------------

    def load_docx(self, file_path):

        doc = Document(file_path)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
        )

        return {
            "text": self.clean_text(text),
            "pages": 1
        }

    # -----------------------------
    # TXT
    # -----------------------------

    def load_txt(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            text = f.read()

        return {
            "text": self.clean_text(text),
            "pages": 1
        }

    # -----------------------------
    # MAIN LOADER
    # -----------------------------

    def load_document(
            self,
            file_path):

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension == ".pdf":

            result = self.load_pdf(
                file_path
            )

        elif extension == ".docx":

            result = self.load_docx(
                file_path
            )

        elif extension == ".txt":

            result = self.load_txt(
                file_path
            )

        else:

            raise ValueError(
                f"Unsupported File: {extension}"
            )

        result["file_name"] = (
            os.path.basename(
                file_path
            )
        )

        result["file_size_mb"] = round(
            os.path.getsize(
                file_path
            ) / (1024 * 1024),
            2
        )

        result["word_count"] = len(
            result["text"].split()
        )

        result["character_count"] = len(
            result["text"]
        )

        return result

    # -----------------------------
    # RESEARCH METADATA
    # -----------------------------

    def extract_metadata(
            self,
            text):

        lines = text.split("\n")

        title = ""

        for line in lines:

            if len(line.strip()) > 20:

                title = line.strip()

                break

        return {
            "title": title,
            "total_words": len(
                text.split()
            ),
            "total_characters": len(
                text
            )
        }