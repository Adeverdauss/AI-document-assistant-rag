from google import genai

from config import *

client = genai.Client(
    api_key=GEMINI_API_KEY
)

SYSTEM_PROMPT = """
Kamu adalah AI Document Assistant.

Jawablah HANYA berdasarkan context.

ATURAN:

1. Jangan mengarang.

2. Jawaban harus berasal dari context.

3. Jika terdapat beberapa angka,
pilih angka yang paling sesuai dengan pertanyaan.

4. Jika informasi tidak ada,
jawab:

'Informasi tersebut tidak ditemukan pada dokumen.'

5. Setelah menjawab,
tambahkan sumber dalam format:

Sumber:
- Nama Dokumen
- Halaman

Jawaban maksimal 2 paragraf.
"""


def generate_answer(question, contexts):

    prompt = f"""
{SYSTEM_PROMPT}

=========================
CONTEXT
=========================

{contexts}

=========================
QUESTION
=========================

{question}

=========================
ANSWER
=========================
"""

    response = client.models.generate_content(

        model=LLM_MODEL,

        contents=prompt

    )

    return response.text