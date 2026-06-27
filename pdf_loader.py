import fitz
import os


def load_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for i, page in enumerate(doc):

        text = page.get_text("text")

        pages.append({

            "page": i + 1,

            "document": os.path.basename(pdf_path),

            "text": text.strip()

        })

    return pages