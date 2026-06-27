import os
import json
import pickle

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from pdf_loader import load_pdf
from chunker import split_text

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print(MODEL_NAME)

# =====================================================
# CONFIG
# =====================================================

PDF_FOLDER = "uploads"
OUTPUT_FOLDER = "vector_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 300
BATCH_SIZE = 16

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

# =====================================================
# LOAD MODEL
# =====================================================

print("=" * 60)
print("Loading Embedding Model...")
print("=" * 60)

model = SentenceTransformer(MODEL_NAME)

print("Model Loaded\n")

# =====================================================
# LOAD PDF
# =====================================================

documents = []

print("=" * 60)
print("Loading PDF...")
print("=" * 60)

pdf_files = [

    f for f in os.listdir(PDF_FOLDER)

    if f.endswith(".pdf")

]

for file in pdf_files:

    path = os.path.join(PDF_FOLDER, file)

    print(f"Loading : {file}")

    pages = load_pdf(path)

    print(f"Pages : {len(pages)}")

    documents.extend(pages)

print()

print(f"Total Pages : {len(documents)}")

# =====================================================
# CREATE CHUNKS
# =====================================================

print()
print("=" * 60)
print("Creating Chunks...")
print("=" * 60)

chunks = []

chunk_id = 0

for doc in documents:

    texts = split_text(

        doc["text"],

        chunk_size=CHUNK_SIZE,

        overlap=CHUNK_OVERLAP

    )

    for text in texts:

        text = text.strip()

        if len(text) == 0:

            continue

        chunks.append({

            "chunk_id": chunk_id,

            "page": doc["page"],

            "document": doc["document"],

            "text": text

        })

        chunk_id += 1

print(f"Total Chunks : {len(chunks)}")

# =====================================================
# EMBEDDING
# =====================================================

print()
print("=" * 60)
print("Generating Embeddings...")
print("=" * 60)

texts = [

    c["text"]

    for c in chunks

]

all_embeddings = []

for i in range(

    0,

    len(texts),

    BATCH_SIZE

):

    batch = texts[

        i:i+BATCH_SIZE

    ]

    emb = model.encode(

        batch,

        batch_size=BATCH_SIZE,

        convert_to_numpy=True,

        normalize_embeddings=True,

        show_progress_bar=False

    )

    all_embeddings.append(emb)

    print(

        f"Batch {i//BATCH_SIZE+1} / {(len(texts)-1)//BATCH_SIZE+1}"

    )

embeddings = np.vstack(all_embeddings)

print()

print("Embedding Shape :", embeddings.shape)

# =====================================================
# CREATE FAISS
# =====================================================

print()
print("=" * 60)
print("Creating FAISS...")
print("=" * 60)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(

    embeddings.astype(np.float32)

)

print("Vector Stored :", index.ntotal)

# =====================================================
# SAVE INDEX
# =====================================================

print()
print("=" * 60)
print("Saving Database...")
print("=" * 60)

faiss.write_index(

    index,

    os.path.join(

        OUTPUT_FOLDER,

        "index.faiss"

    )

)

with open(

    os.path.join(

        OUTPUT_FOLDER,

        "chunks.pkl"

    ),

    "wb"

) as f:

    pickle.dump(

        chunks,

        f

    )

metadata = {

    "embedding_model": MODEL_NAME,

    "dimension": int(dimension),

    "total_pages": len(documents),

    "total_chunks": len(chunks)

}

with open(

    os.path.join(

        OUTPUT_FOLDER,

        "metadata.json"

    ),

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        metadata,

        f,

        indent=4,

        ensure_ascii=False

    )

document_info = []

for file in pdf_files:

    pages = load_pdf(

        os.path.join(

            PDF_FOLDER,

            file

        )

    )

    document_info.append({

        "document": file,

        "pages": len(pages)

    })

with open(

    os.path.join(

        OUTPUT_FOLDER,

        "document_info.json"

    ),

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        document_info,

        f,

        indent=4,

        ensure_ascii=False

    )

print()
print("=" * 60)
print("DONE")
print("=" * 60)