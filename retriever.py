import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from config import *

print("Loading Embedding Model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Loading FAISS Index...")

index = faiss.read_index(
    VECTOR_DB_PATH
)

print("Loading Chunks...")

with open(
    CHUNK_PATH,
    "rb"
) as f:

    chunks = pickle.load(f)

print("Retriever Ready")

def reload():

    global index

    global chunks

    index = faiss.read_index(

        VECTOR_DB_PATH

    )

    with open(

        CHUNK_PATH,

        "rb"

    ) as f:

        chunks = pickle.load(f)

    print(

        "Retriever Reloaded"

    )


def retrieve(question, top_k=TOP_K):

    embedding = embedding_model.encode(

        [question],

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    scores, indices = index.search(

        embedding.astype(np.float32),

        top_k

    )

    results = []

    for score, idx in zip(

        scores[0],

        indices[0]

    ):

        item = chunks[idx].copy()

        item["score"] = float(score)

        item["source"] = {

            "document": item["document"],

            "page": item["page"],

            "chunk_id": item["chunk_id"]

        }

        results.append(item)

    return results