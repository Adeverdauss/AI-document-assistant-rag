import os
import json
import pickle

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from pdf_loader import load_pdf
from chunker import split_text

VECTOR_PATH = "vector_db/index.faiss"
CHUNK_PATH = "vector_db/chunks.pkl"
DOC_INFO_PATH = "vector_db/document_info.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def add_document(pdf_path):

    index = faiss.read_index(VECTOR_PATH)

    with open(CHUNK_PATH, "rb") as f:
        chunks = pickle.load(f)

    documents = load_pdf(pdf_path)

    chunk_id = len(chunks)

    new_chunks = []

    texts = []

    for doc in documents:

        parts = split_text(
            doc["text"],
            chunk_size=800,
            overlap=150
        )

        for text in parts:

            item = {

                "chunk_id": chunk_id,

                "document": os.path.basename(pdf_path),

                "page": doc["page"],

                "text": text

            }

            new_chunks.append(item)

            texts.append(text)

            chunk_id += 1

    embeddings = model.encode(

        texts,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    index.add(

        embeddings.astype(np.float32)

    )

    chunks.extend(new_chunks)

    faiss.write_index(index, VECTOR_PATH)

    with open(CHUNK_PATH, "wb") as f:

        pickle.dump(chunks, f)

    # update document list

    if os.path.exists(DOC_INFO_PATH):

        with open(DOC_INFO_PATH, "r", encoding="utf8") as f:

            info = json.load(f)

    else:

        info = []

    info.append({

        "document": os.path.basename(pdf_path),

        "pages": len(documents),

        "chunks": len(new_chunks)

    })

    with open(DOC_INFO_PATH, "w", encoding="utf8") as f:

        json.dump(

            info,

            f,

            indent=4

        )

    return {

        "status": "success",

        "pages": len(documents),

        "chunks": len(new_chunks)

    }